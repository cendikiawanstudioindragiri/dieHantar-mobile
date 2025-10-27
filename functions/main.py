
from flask import Flask, request, jsonify
from firebase_admin import auth, initialize_app
import functions_framework

# Initialize Firebase Admin SDK
initialize_app()

@functions_framework.http
def createOrderAPI(request):
    """
    HTTP Function to create a new order.
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"success": False, "message": "Authentication required."}), 401
        
        id_token = auth_header.split(' ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        if request.method != 'POST':
            return jsonify({"success": False, "message": "HTTP method must be POST."}), 405
        
        request_json = request.get_json(silent=True)
        if not request_json:
            return jsonify({"success": False, "message": "Request body cannot be empty."}), 400
        
        # In a real application, you would have a service to handle order creation
        # from services.order_service import create_new_order
        # result = create_new_order(uid, order_details)

        # For now, we'll simulate a successful order creation
        order_id = f"mock_order_{uid[:5]}"
        total_amount = 100000

        return jsonify({
            "success": True, 
            "order_id": order_id,
            "total_amount": total_amount
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500


@functions_framework.http
def cancelOrderAPI(request):
    """
    HTTP Function to cancel an order.
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"success": False, "message": "Authentication required."}), 401
            
        id_token = auth_header.split(' ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        if request.method != 'POST':
            return jsonify({"success": False, "message": "HTTP method must be POST."}), 405
             
        request_json = request.get_json(silent=True)
        order_id = request_json.get('order_id')
        reason = request_json.get('reason')

        if not order_id or not reason:
            return jsonify({"success": False, "message": "Order ID and reason for cancellation are required."}), 400

        # In a real application, you would have a service to handle order cancellation
        # from services.order_service import cancel_order
        # result = cancel_order(order_id, uid, reason)

        # For now, we'll simulate a successful cancellation
        return jsonify({"success": True, "message": "Order has been successfully canceled."}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500
