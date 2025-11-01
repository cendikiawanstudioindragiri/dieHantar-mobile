
from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
import json

# Inisialisasi Firebase Admin SDK
initialize_app()

@https_fn.on_request()
def reviewsAPI(req: https_fn.Request) -> https_fn.Response:
    """
    Handles GET and POST requests for reviews.
    GET: Fetches reviews for a given restaurantId.
    POST: Submits a new review.
    """
    if req.method == "GET":
        restaurant_id = req.args.get("restaurantId")
        if not restaurant_id:
            return https_fn.Response("Missing restaurantId parameter", status=400)

        db = firestore.client()
        reviews_ref = db.collection(f"restaurants/{restaurant_id}/reviews")
        reviews = [doc.to_dict() for doc in reviews_ref.stream()]
        
        return https_fn.Response(json.dumps({"success": True, "reviews": reviews}),
                                 content_type="application/json")

    elif req.method == "POST":
        # Autentikasi akan dibahas di langkah selanjutnya
        # Untuk saat ini, kita akan melewati verifikasi token
        
        try:
            review_data = req.get_json()
            restaurant_id = review_data.get("restaurantId")
            if not restaurant_id:
                return https_fn.Response("Missing restaurantId in request body", status=400)

            db = firestore.client()
            db.collection(f"restaurants/{restaurant_id}/reviews").add(review_data)
            
            return https_fn.Response(json.dumps({"success": True}),
                                     content_type="application/json",
                                     status=201)
        except Exception as e:
            return https_fn.Response(f"Error submitting review: {e}", status=500)

    return https_fn.Response("Method not allowed", status=405)

