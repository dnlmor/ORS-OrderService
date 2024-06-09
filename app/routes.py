from flask import Blueprint, request, jsonify
from app.models import Order
from app import db

bp = Blueprint('routes', __name__)

@bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(user_id=data['user_id'], menu_item_id=data['menu_item_id'], quantity=data['quantity'], status='pending')
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'})

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'user_id': order.user_id, 'menu_item_id': order.menu_item_id, 'quantity': order.quantity, 'status': order.status} for order in orders])
