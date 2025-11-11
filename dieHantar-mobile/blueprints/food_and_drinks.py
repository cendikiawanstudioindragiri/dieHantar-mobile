from flask import Blueprint, jsonify
from firebase_config import get_firestore_client
from logger_config import get_logger

food_and_drinks_bp = Blueprint('food_and_drinks', __name__)
logger = get_logger(__name__)

@food_and_drinks_bp.route('/food-categories')
def get_food_categories():
    logger.info('Fetching food categories from Firestore.')
    try:
        db = get_firestore_client()
        categories_ref = db.collection('food_categories')
        categories = []
        for doc in categories_ref.stream():
            category = doc.to_dict()
            category['id'] = doc.id
            categories.append(category)
        logger.info(f'Successfully fetched {len(categories)} food categories.')
        return jsonify(categories)
    except Exception as e:
        logger.error(f'Error fetching food categories: {e}', exc_info=True)
        return jsonify({"error": "An error occurred while fetching food categories."}), 500
