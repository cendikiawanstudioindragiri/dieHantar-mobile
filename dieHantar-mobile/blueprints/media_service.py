# blueprints/media_service.py

import os
import uuid
import magic
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Tuple
from PIL import Image
from werkzeug.datastructures import FileStorage
from firebase_admin import storage
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()

# Konfigurasi file upload
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB
IMAGE_QUALITY = 85
THUMBNAIL_SIZE = (300, 300)

@dataclass
class UploadedFile:
    id: str
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    upload_path: str
    download_url: str
    uploaded_by: str
    uploaded_at: datetime
    metadata: Optional[Dict] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'UploadedFile':
        return UploadedFile(**data)

class FileUploadError(Exception):
    """Custom exception untuk error upload file"""
    pass

def validate_file(file: FileStorage, file_type: str = 'image') -> None:
    """
    Validasi file yang akan diupload.
    
    Args:
        file: File yang akan diupload
        file_type: Tipe file yang diizinkan ('image' atau 'document')
    
    Raises:
        FileUploadError: Jika file tidak valid
    """
    if not file or not file.filename:
        raise FileUploadError("File tidak ditemukan atau nama file kosong.")

    # Validasi ekstensi file
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_type == 'image' and file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise FileUploadError(f"Ekstensi file tidak diizinkan. Hanya diizinkan: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
    
    if file_type == 'document' and file_ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise FileUploadError(f"Ekstensi file tidak diizinkan. Hanya diizinkan: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}")

    # Validasi ukuran file
    max_size = MAX_IMAGE_SIZE if file_type == 'image' else MAX_FILE_SIZE
    
    # Cek ukuran file dengan cara yang aman
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset ke awal file
    
    if file_size > max_size:
        size_mb = max_size / (1024 * 1024)
        raise FileUploadError(f"Ukuran file terlalu besar. Maksimal {size_mb:.1f}MB.")

    # Validasi MIME type menggunakan python-magic
    file_data = file.read(1024)  # Baca sedikit untuk deteksi
    file.seek(0)  # Reset ke awal
    
    mime_type = magic.from_buffer(file_data, mime=True)
    
    if file_type == 'image' and not mime_type.startswith('image/'):
        raise FileUploadError("File yang diupload bukan gambar yang valid.")

def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate nama file unik dengan UUID.
    
    Args:
        original_filename: Nama file asli
        prefix: Prefix untuk nama file
    
    Returns:
        str: Nama file unik
    """
    file_ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if prefix:
        return f"{prefix}_{timestamp}_{unique_id}.{file_ext}"
    return f"{timestamp}_{unique_id}.{file_ext}"

def optimize_image(file: FileStorage, quality: int = IMAGE_QUALITY) -> bytes:
    """
    Optimasi gambar untuk mengurangi ukuran file.
    
    Args:
        file: File gambar yang akan dioptimasi
        quality: Kualitas kompresi (1-100)
    
    Returns:
        bytes: Data gambar yang sudah dioptimasi
    """
    try:
        # Buka gambar dengan PIL
        image = Image.open(file)
        
        # Konversi ke RGB jika mode lain (misalnya RGBA)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Buat background putih untuk transparansi
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if len(image.split()) == 4 else None)
            image = background

        # Resize jika terlalu besar (max 1920x1920 untuk kualitas baik)
        max_dimension = 1920
        if image.width > max_dimension or image.height > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Save ke bytes dengan kompresi
        from io import BytesIO
        optimized_buffer = BytesIO()
        
        # Tentukan format berdasarkan ekstensi asli
        format_map = {
            'jpg': 'JPEG', 'jpeg': 'JPEG',
            'png': 'PNG', 'gif': 'GIF', 'webp': 'WEBP'
        }
        
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        save_format = format_map.get(file_ext, 'JPEG')
        
        if save_format == 'JPEG':
            image.save(optimized_buffer, format=save_format, quality=quality, optimize=True)
        else:
            image.save(optimized_buffer, format=save_format, optimize=True)
        
        return optimized_buffer.getvalue()
        
    except Exception as e:
        logger.error(f"Error optimizing image: {e}", exc_info=True)
        # Fallback: return original file data
        file.seek(0)
        return file.read()

def create_thumbnail(file: FileStorage, size: Tuple[int, int] = THUMBNAIL_SIZE) -> bytes:
    """
    Buat thumbnail untuk gambar.
    
    Args:
        file: File gambar
        size: Ukuran thumbnail (width, height)
    
    Returns:
        bytes: Data thumbnail
    """
    try:
        image = Image.open(file)
        
        # Konversi ke RGB jika diperlukan
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if len(image.split()) == 4 else None)
            image = background

        # Create thumbnail dengan aspect ratio yang dipertahankan
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        from io import BytesIO
        thumbnail_buffer = BytesIO()
        image.save(thumbnail_buffer, format='JPEG', quality=80, optimize=True)
        
        return thumbnail_buffer.getvalue()
        
    except Exception as e:
        logger.error(f"Error creating thumbnail: {e}", exc_info=True)
        return b''

def upload_to_firebase_storage(file_data: bytes, filename: str, folder: str = 'uploads') -> str:
    """
    Upload file ke Firebase Storage.
    
    Args:
        file_data: Data file dalam bytes
        filename: Nama file
        folder: Folder tujuan di storage
    
    Returns:
        str: Download URL file
    
    Raises:
        FileUploadError: Jika upload gagal
    """
    try:
        # Get Firebase Storage bucket
        bucket = storage.bucket()
        
        # Buat path file
        file_path = f"{folder}/{filename}"
        
        # Upload file
        blob = bucket.blob(file_path)
        blob.upload_from_string(file_data)
        
        # Make file publicly accessible
        blob.make_public()
        
        # Return public URL
        return blob.public_url
        
    except Exception as e:
        logger.error(f"Error uploading to Firebase Storage: {e}", exc_info=True)
        raise FileUploadError(f"Gagal mengupload file ke storage: {str(e)}")

def save_file_metadata(uploaded_file: UploadedFile) -> str:
    """
    Simpan metadata file ke Firestore.
    
    Args:
        uploaded_file: Object UploadedFile
    
    Returns:
        str: Document ID dari metadata yang tersimpan
    """
    try:
        file_ref = db.collection('uploaded_files').document(uploaded_file.id)
        file_ref.set(uploaded_file.to_dict())
        
        logger.info(f"File metadata saved for {uploaded_file.filename}")
        return uploaded_file.id
        
    except Exception as e:
        logger.error(f"Error saving file metadata: {e}", exc_info=True)
        raise FileUploadError(f"Gagal menyimpan metadata file: {str(e)}")

def upload_file(file: FileStorage, uploaded_by: str, file_type: str = 'image', 
                folder: str = 'uploads', create_thumb: bool = True) -> UploadedFile:
    """
    Upload file lengkap dengan validasi, optimasi, dan penyimpanan metadata.
    
    Args:
        file: File yang akan diupload
        uploaded_by: UID user yang mengupload
        file_type: Tipe file ('image' atau 'document')
        folder: Folder tujuan di storage
        create_thumb: Apakah perlu buat thumbnail (untuk image)
    
    Returns:
        UploadedFile: Object file yang sudah diupload
    
    Raises:
        FileUploadError: Jika upload gagal
    """
    # Validasi file
    validate_file(file, file_type)
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename, folder)
    
    try:
        # Proses berdasarkan tipe file
        if file_type == 'image':
            # Optimasi gambar
            optimized_data = optimize_image(file)
            file_data = optimized_data
            
            # Upload thumbnail jika diminta
            thumbnail_url = None
            if create_thumb:
                file.seek(0)  # Reset file pointer
                thumbnail_data = create_thumbnail(file)
                if thumbnail_data:
                    thumb_filename = f"thumb_{unique_filename}"
                    thumbnail_url = upload_to_firebase_storage(
                        thumbnail_data, thumb_filename, f"{folder}/thumbnails"
                    )
        else:
            # Untuk document, upload as-is
            file.seek(0)
            file_data = file.read()
        
        # Upload file utama ke Firebase Storage
        download_url = upload_to_firebase_storage(file_data, unique_filename, folder)
        
        # Buat object UploadedFile
        uploaded_file = UploadedFile(
            id=str(uuid.uuid4()),
            filename=unique_filename,
            original_filename=file.filename,
            file_type=file_type,
            file_size=len(file_data),
            upload_path=f"{folder}/{unique_filename}",
            download_url=download_url,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.utcnow(),
            metadata={
                'thumbnail_url': thumbnail_url if file_type == 'image' and create_thumb else None,
                'mime_type': magic.from_buffer(file_data[:1024], mime=True)
            }
        )
        
        # Simpan metadata ke Firestore
        save_file_metadata(uploaded_file)
        
        logger.info(f"File uploaded successfully: {unique_filename} by {uploaded_by}")
        return uploaded_file
        
    except Exception as e:
        logger.error(f"Error in upload_file: {e}", exc_info=True)
        raise FileUploadError(f"Gagal mengupload file: {str(e)}")

def delete_file(file_id: str, user_id: str) -> bool:
    """
    Hapus file dari storage dan metadata dari database.
    
    Args:
        file_id: ID file yang akan dihapus
        user_id: UID user (untuk validasi permission)
    
    Returns:
        bool: True jika berhasil dihapus
    
    Raises:
        FileUploadError: Jika gagal menghapus
    """
    try:
        # Ambil metadata file
        file_doc = db.collection('uploaded_files').document(file_id).get()
        
        if not file_doc.exists:
            raise FileUploadError("File tidak ditemukan.")
        
        file_data = file_doc.to_dict()
        
        # Validasi permission (hanya uploader yang bisa hapus)
        if file_data.get('uploaded_by') != user_id:
            raise FileUploadError("Anda tidak memiliki permission untuk menghapus file ini.")
        
        # Hapus dari Firebase Storage
        bucket = storage.bucket()
        
        # Hapus file utama
        main_blob = bucket.blob(file_data['upload_path'])
        if main_blob.exists():
            main_blob.delete()
        
        # Hapus thumbnail jika ada
        if file_data.get('metadata', {}).get('thumbnail_url'):
            thumb_path = file_data['upload_path'].replace('uploads/', 'uploads/thumbnails/thumb_')
            thumb_blob = bucket.blob(thumb_path)
            if thumb_blob.exists():
                thumb_blob.delete()
        
        # Hapus metadata dari Firestore
        db.collection('uploaded_files').document(file_id).delete()
        
        logger.info(f"File deleted successfully: {file_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {e}", exc_info=True)
        raise FileUploadError(f"Gagal menghapus file: {str(e)}")

def get_file_info(file_id: str) -> Optional[UploadedFile]:
    """
    Ambil informasi file berdasarkan ID.
    
    Args:
        file_id: ID file
    
    Returns:
        UploadedFile atau None jika tidak ditemukan
    """
    try:
        file_doc = db.collection('uploaded_files').document(file_id).get()
        
        if file_doc.exists:
            return UploadedFile.from_dict(file_doc.to_dict())
        return None
        
    except Exception as e:
        logger.error(f"Error getting file info {file_id}: {e}", exc_info=True)
        return None

def get_user_files(user_id: str, file_type: Optional[str] = None, limit: int = 50) -> list:
    """
    Ambil daftar file yang diupload oleh user tertentu.
    
    Args:
        user_id: UID user
        file_type: Filter berdasarkan tipe file (optional)
        limit: Maksimal file yang dikembalikan
    
    Returns:
        List[UploadedFile]: Daftar file
    """
    try:
        query = db.collection('uploaded_files').where('uploaded_by', '==', user_id)
        
        if file_type:
            query = query.where('file_type', '==', file_type)
        
        query = query.order_by('uploaded_at', direction='DESCENDING').limit(limit)
        
        files = []
        for doc in query.get():
            files.append(UploadedFile.from_dict(doc.to_dict()))
        
        return files
        
    except Exception as e:
        logger.error(f"Error getting user files for {user_id}: {e}", exc_info=True)
        return []