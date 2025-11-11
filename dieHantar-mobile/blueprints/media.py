# blueprints/media.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.datastructures import FileStorage
from logger_config import get_logger
from .auth_service import token_required
from . import media_service as service

media_bp = Blueprint('media', __name__, url_prefix='/api/v1/media')
logger = get_logger('MediaBlueprint')

@media_bp.route('/upload/profile', methods=['POST'])
@token_required
def upload_profile_picture(uid):
    """
    Endpoint untuk upload foto profil pengguna.
    Accepts: multipart/form-data dengan file field 'image'
    """
    try:
        # Validasi file dalam request
        if 'image' not in request.files:
            return jsonify({
                "success": False, 
                "message": "File 'image' tidak ditemukan dalam request."
            }), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({
                "success": False, 
                "message": "Tidak ada file yang dipilih."
            }), 400

        # Upload file
        uploaded_file = service.upload_file(
            file=file,
            uploaded_by=uid,
            file_type='image',
            folder='profile_pictures',
            create_thumb=True
        )

        # Update user profile dengan URL foto profil baru
        from firebase_config import get_firestore_client
        db = get_firestore_client()
        user_ref = db.collection('users').document(uid)
        user_ref.update({
            'profile_picture_url': uploaded_file.download_url,
            'profile_picture_id': uploaded_file.id,
            'profile_thumbnail_url': uploaded_file.metadata.get('thumbnail_url')
        })

        logger.info(f"Profile picture uploaded successfully for UID {uid}: {uploaded_file.filename}")
        return jsonify({
            "success": True,
            "message": "Foto profil berhasil diupload.",
            "data": {
                "file_id": uploaded_file.id,
                "download_url": uploaded_file.download_url,
                "thumbnail_url": uploaded_file.metadata.get('thumbnail_url'),
                "file_size": uploaded_file.file_size
            }
        }), 201

    except service.FileUploadError as e:
        logger.warning(f"File upload error for UID {uid}: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error uploading profile picture for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengupload foto profil."
        }), 500

@media_bp.route('/upload/food', methods=['POST'])
@token_required
def upload_food_image(uid):
    """
    Endpoint untuk upload gambar makanan (untuk merchant).
    Accepts: multipart/form-data dengan file field 'image' dan optional 'food_id'
    """
    try:
        if 'image' not in request.files:
            return jsonify({
                "success": False, 
                "message": "File 'image' tidak ditemukan dalam request."
            }), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({
                "success": False, 
                "message": "Tidak ada file yang dipilih."
            }), 400

        # Optional: food_id untuk mengaitkan gambar dengan item makanan tertentu
        food_id = request.form.get('food_id')

        # Upload file
        uploaded_file = service.upload_file(
            file=file,
            uploaded_by=uid,
            file_type='image',
            folder='food_images',
            create_thumb=True
        )

        # Update food item jika food_id disediakan
        if food_id:
            from firebase_config import get_firestore_client
            db = get_firestore_client()
            food_ref = db.collection('foods').document(food_id)
            food_doc = food_ref.get()
            
            if food_doc.exists:
                # Add to existing images array atau replace image_url
                food_ref.update({
                    'image_url': uploaded_file.download_url,
                    'image_id': uploaded_file.id,
                    'thumbnail_url': uploaded_file.metadata.get('thumbnail_url'),
                    'updated_at': service.datetime.utcnow()
                })

        logger.info(f"Food image uploaded successfully by UID {uid}: {uploaded_file.filename}")
        return jsonify({
            "success": True,
            "message": "Gambar makanan berhasil diupload.",
            "data": {
                "file_id": uploaded_file.id,
                "download_url": uploaded_file.download_url,
                "thumbnail_url": uploaded_file.metadata.get('thumbnail_url'),
                "file_size": uploaded_file.file_size,
                "food_id": food_id
            }
        }), 201

    except service.FileUploadError as e:
        logger.warning(f"Food image upload error for UID {uid}: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error uploading food image for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengupload gambar makanan."
        }), 500

@media_bp.route('/upload/document', methods=['POST'])
@token_required
def upload_document(uid):
    """
    Endpoint untuk upload dokumen (KTP, SIM driver, dll).
    Accepts: multipart/form-data dengan file field 'document' dan 'document_type'
    """
    try:
        if 'document' not in request.files:
            return jsonify({
                "success": False, 
                "message": "File 'document' tidak ditemukan dalam request."
            }), 400

        file = request.files['document']
        if file.filename == '':
            return jsonify({
                "success": False, 
                "message": "Tidak ada file yang dipilih."
            }), 400

        # Wajib ada document_type untuk klasifikasi
        document_type = request.form.get('document_type')
        if not document_type:
            return jsonify({
                "success": False, 
                "message": "Document type harus disediakan (ktp, sim, stnk, dll)."
            }), 400

        # Validasi document_type yang diizinkan
        allowed_doc_types = ['ktp', 'sim', 'stnk', 'npwp', 'contract', 'permit']
        if document_type.lower() not in allowed_doc_types:
            return jsonify({
                "success": False, 
                "message": f"Document type tidak valid. Yang diizinkan: {', '.join(allowed_doc_types)}"
            }), 400

        # Upload file
        uploaded_file = service.upload_file(
            file=file,
            uploaded_by=uid,
            file_type='document',
            folder=f'documents/{document_type.lower()}',
            create_thumb=False  # Dokumen tidak perlu thumbnail
        )

        # Simpan reference dokumen ke profile user/driver
        from firebase_config import get_firestore_client
        db = get_firestore_client()
        
        # Update di collection users atau drivers tergantung context
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            # Update atau create documents field
            documents_field = f"documents.{document_type.lower()}"
            user_ref.update({
                documents_field: {
                    'file_id': uploaded_file.id,
                    'download_url': uploaded_file.download_url,
                    'uploaded_at': uploaded_file.uploaded_at,
                    'status': 'pending_review'  # Admin perlu review dokumen
                }
            })

        logger.info(f"Document uploaded successfully by UID {uid}: {document_type} - {uploaded_file.filename}")
        return jsonify({
            "success": True,
            "message": f"Dokumen {document_type.upper()} berhasil diupload.",
            "data": {
                "file_id": uploaded_file.id,
                "download_url": uploaded_file.download_url,
                "document_type": document_type,
                "file_size": uploaded_file.file_size,
                "status": "pending_review"
            }
        }), 201

    except service.FileUploadError as e:
        logger.warning(f"Document upload error for UID {uid}: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error uploading document for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengupload dokumen."
        }), 500

@media_bp.route('/files', methods=['GET'])
@token_required
def get_my_files(uid):
    """
    Endpoint untuk mendapatkan daftar file yang diupload oleh user.
    Query parameters:
    - type: filter berdasarkan file type (image/document)
    - limit: maksimal file yang dikembalikan (default 50)
    """
    try:
        file_type = request.args.get('type')
        limit = min(int(request.args.get('limit', 50)), 100)  # Max 100 files

        files = service.get_user_files(
            user_id=uid,
            file_type=file_type,
            limit=limit
        )

        files_data = [file.to_dict() for file in files]

        return jsonify({
            "success": True,
            "data": {
                "files": files_data,
                "total": len(files_data),
                "filter": {
                    "type": file_type,
                    "limit": limit
                }
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting files for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengambil daftar file."
        }), 500

@media_bp.route('/files/<string:file_id>', methods=['GET'])
@token_required
def get_file_info_endpoint(uid, file_id):
    """
    Endpoint untuk mendapatkan informasi detail file berdasarkan ID.
    """
    try:
        file_info = service.get_file_info(file_id)
        
        if not file_info:
            return jsonify({
                "success": False, 
                "message": "File tidak ditemukan."
            }), 404

        # Validasi permission: hanya uploader yang bisa akses detail file
        if file_info.uploaded_by != uid:
            return jsonify({
                "success": False, 
                "message": "Anda tidak memiliki akses ke file ini."
            }), 403

        return jsonify({
            "success": True,
            "data": file_info.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"Error getting file info {file_id} for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengambil informasi file."
        }), 500

@media_bp.route('/files/<string:file_id>', methods=['DELETE'])
@token_required
def delete_file_endpoint(uid, file_id):
    """
    Endpoint untuk menghapus file berdasarkan ID.
    """
    try:
        success = service.delete_file(file_id, uid)
        
        if success:
            return jsonify({
                "success": True,
                "message": "File berhasil dihapus."
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Gagal menghapus file."
            }), 500

    except service.FileUploadError as e:
        logger.warning(f"Delete file error {file_id} for UID {uid}: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error deleting file {file_id} for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat menghapus file."
        }), 500

# Admin-only endpoints untuk review dokumen
@media_bp.route('/admin/documents/pending', methods=['GET'])
@token_required
def get_pending_documents_review(uid):
    """
    Endpoint khusus admin untuk melihat dokumen yang butuh review.
    TODO: Implement proper admin role checking
    """
    try:
        # TODO: Check if user has admin role
        # For now, we'll implement basic version
        
        from firebase_config import get_firestore_client
        db = get_firestore_client()
        
        # Query users yang punya dokumen dengan status pending_review
        users_query = db.collection('users').where('documents', '!=', None).limit(50)
        
        pending_docs = []
        for user_doc in users_query.get():
            user_data = user_doc.to_dict()
            user_documents = user_data.get('documents', {})
            
            for doc_type, doc_info in user_documents.items():
                if doc_info.get('status') == 'pending_review':
                    pending_docs.append({
                        'user_id': user_doc.id,
                        'document_type': doc_type,
                        'file_id': doc_info.get('file_id'),
                        'download_url': doc_info.get('download_url'),
                        'uploaded_at': doc_info.get('uploaded_at'),
                        'user_email': user_data.get('email'),
                        'user_name': user_data.get('display_name', 'Unknown')
                    })

        return jsonify({
            "success": True,
            "data": {
                "pending_documents": pending_docs,
                "total": len(pending_docs)
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting pending documents for admin UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mengambil daftar dokumen pending."
        }), 500

@media_bp.route('/admin/documents/<string:user_id>/<string:document_type>/review', methods=['POST'])
@token_required
def review_document(uid, user_id, document_type):
    """
    Endpoint khusus admin untuk approve/reject dokumen user.
    Body: {"status": "approved|rejected", "notes": "optional notes"}
    """
    try:
        # TODO: Check if user has admin role
        
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False, 
                "message": "Request body kosong."
            }), 400

        status = data.get('status')
        notes = data.get('notes', '')

        if status not in ['approved', 'rejected']:
            return jsonify({
                "success": False, 
                "message": "Status harus 'approved' atau 'rejected'."
            }), 400

        # Update status dokumen
        from firebase_config import get_firestore_client
        db = get_firestore_client()
        
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({
                "success": False, 
                "message": "User tidak ditemukan."
            }), 404

        # Update document status
        document_field = f"documents.{document_type}"
        user_ref.update({
            f"{document_field}.status": status,
            f"{document_field}.reviewed_by": uid,
            f"{document_field}.reviewed_at": service.datetime.utcnow(),
            f"{document_field}.review_notes": notes
        })

        # TODO: Send notification to user about document review result

        logger.info(f"Document review completed by admin {uid}: {user_id}/{document_type} = {status}")
        return jsonify({
            "success": True,
            "message": f"Dokumen {document_type} untuk user {user_id} telah di-{status}."
        }), 200

    except Exception as e:
        logger.error(f"Error reviewing document for admin UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mereview dokumen."
        }), 500