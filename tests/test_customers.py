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

class TestCustomerEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # test successful creation of customer
    @patch('services.customerService.save')
    def test_create_customer(self, mock_save):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.email = email
        mock_customer.phone = phone
        mock_save.return_value = mock_customer

        payload = {
                "name": name,
                "phone": phone,
                "email": email
            }
        
        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_customer.id)

    # test creation of customer without email
    @patch('services.customerService.save')
    def test_missing_email_payload(self, mock_save):
        name = fake.name()
        phone = fake.phone_number()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.phone = phone
        mock_save.return_value = mock_customer

        payload = {
            "name": name,
            "phone": phone
        }

        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    # test creation of customer with superfluous data
    @patch('services.customerService.save')
    def test_extra_data_customer(self, mock_save):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.email = email
        mock_customer.phone = phone
        mock_save.return_value = mock_customer

        payload = {
                "name": name,
                "phone": phone,
                "email": email,
                "shoe_size" : 8
            }
        
        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 400)