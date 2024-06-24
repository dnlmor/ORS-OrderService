import unittest
from app.services import OrderService
from app.models import Order, OrderItem
from app.database import db_session

class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.order_data = {
            'user_id': 1,
            'items': [
                {'dish_id': 1, 'quantity': 2, 'price': 9.99},
                {'dish_id': 2, 'quantity': 1, 'price': 14.99}
            ]
        }

    def test_create_order(self):
        order = OrderService.create_order(**self.order_data)
        self.assertIsNotNone(order.id)
        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(order.total_amount, 34.97)
        self.assertEqual(len(order.items), 2)

    def test_update_order_status(self):
        order = OrderService.create_order(**self.order_data)
        updated_order = OrderService.update_order_status(order.id, 'PROCESSING')
        self.assertEqual(updated_order.status, 'PROCESSING')

    def tearDown(self):
        db_session.remove()

if __name__ == '__main__':
    unittest.main()
