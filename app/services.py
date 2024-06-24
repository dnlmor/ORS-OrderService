# app/services.py
from .models import Order, OrderItem
from .database import db_session
from .utils import calculate_total_amount, validate_order_status
from sqlalchemy.exc import IntegrityError

class OrderService:
    @staticmethod
    def create_order(user_id, items):
        try:
            total_amount = calculate_total_amount(items)
            order = Order(user_id=user_id, status='PENDING', total_amount=total_amount)
            
            for item in items:
                order_item = OrderItem(
                    dish_id=item.dish_id,
                    quantity=item.quantity,
                    price=item.price
                )
                order.items.append(order_item)
            
            db_session.add(order)
            db_session.commit()
            return order
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Failed to create order")

    @staticmethod
    def update_order_status(id, status):
        order = Order.query.get(id)
        if not order:
            raise ValueError("Order not found")
        
        validate_order_status(status)
        order.status = status
        db_session.commit()
        return order

    @staticmethod
    def get_order_by_id(id):
        order = Order.query.get(id)
        if not order:
            raise ValueError("Order not found")
        return order

    @staticmethod
    def list_orders():
        return Order.query.all()

    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).all()
