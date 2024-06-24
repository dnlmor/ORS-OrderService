# tests/test_models.py
import unittest
from app.models import Order, OrderItem
from app.database import db_session

class TestOrderModel(unittest.TestCase):
    def setUp(self):
        self.order = Order(user_id=1, status='PENDING', total_amount=24.98)
        self.order_item = OrderItem(dish_id=1, quantity=2, price=9.99)

    def test_create_order(self):
        db_session.add(self.order)
        db_session.commit()
        self.assertIsNotNone(self.order.id)

    def test_create_order_item(self):
        self.order.items.append(self.order_item)
        db_session.add(self.order)
        db_session.commit()
        self.assertIsNotNone(self.order_item.id)
        self.assertEqual(self.order_item.order_id, self.order.id)

    def tearDown(self):
        db_session.remove()

if __name__ == '__main__':
    unittest.main()
