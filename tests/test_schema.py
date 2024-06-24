import unittest
from app import create_app
from app.models import db_session, Order, OrderItem

class TestSchema(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        db_session.remove()

    def test_create_order(self):
        response = self.client.post('/graphql', json={'query': '''
            mutation {
                createOrder(userId: 1, items: [
                    {dishId: 1, quantity: 2, price: 9.99},
                    {dishId: 2, quantity: 1, price: 14.99}
                ]) {
                    order {
                        id
                        userId
                        status
                        totalAmount
                        items {
                            dishId
                            quantity
                            price
                        }
                    }
                }
            }
        '''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_get_order(self):
        # First, create an order
        self.test_create_order()
        
        response = self.client.post('/graphql', json={'query': '''
            query {
                getOrder(id: 1) {
                    id
                    userId
                    status
                    totalAmount
                    items {
                        dishId
                        quantity
                        price
                    }
                }
            }
        '''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

if __name__ == '__main__':
    unittest.main()
