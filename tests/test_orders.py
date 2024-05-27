# get app.py from parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from app import create_app

import unittest
from unittest.mock import MagicMock, patch
from faker import Faker

fake = Faker()

class TestOrderEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # test successful creation of order
    @patch('services.orderService.save')
    def test_create_order(self, mock_save):
        customer_id = fake.random_digit_not_null()
        product_id = fake.random_digit_not_null()
        quantity = fake.random_digit_not_null()
        total_price = fake.pyfloat(None, 2, None, 0.0, 9999.99)
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.product_id = product_id
        mock_order.quantity = quantity
        mock_order.total_price = total_price
        mock_save.return_value = mock_order

        payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "total_price": total_price
            }
        
        response = self.app.post('/orders/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_order.id)

    # test creation of order without product_id
    @patch('services.orderService.save')
    def test_missing_product_id_payload(self, mock_save):
        customer_id = fake.random_digit_not_null()
        quantity = fake.random_digit_not_null()
        total_price = fake.pyfloat(None, 2, None, 0.0, 9999.99)
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.quantity = quantity
        mock_order.total_price = total_price
        mock_save.return_value = mock_order

        payload = {
                "customer_id": customer_id,
                "quantity": quantity,
                "total_price": total_price
            }

        response = self.app.post('/orders/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('product_id', response.json)

    # test creation of order with superfluous data
    @patch('services.orderService.save')
    def test_extra_data_order(self, mock_save):
        customer_id = fake.random_digit_not_null()
        product_id = fake.random_digit_not_null()
        quantity = fake.random_digit_not_null()
        total_price = fake.pyfloat(None, 2, None, 0.0, 9999.99)
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.product_id = product_id
        mock_order.quantity = quantity
        mock_order.total_price = total_price
        mock_save.return_value = mock_order

        payload = {
                "customer_id": customer_id,
                "quantity": quantity,
                "product_id": product_id,
                "total_price": total_price,
                "shipping": "Two-Day"
            }
        
        response = self.app.post('/orders/', json=payload)

        self.assertEqual(response.status_code, 400)