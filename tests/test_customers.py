# get app.py from parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from app import create_app

import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import logging

fake = Faker()

# create mock customer with randomized data
def create_test_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()

    mock_customer = MagicMock()
    mock_customer.id = fake.random_number(digits=3)
    mock_customer.name = first_name + " " + last_name
    mock_customer.email = fake.email()
    mock_customer.phone = fake.basic_phone_number()
    mock_customer.username = first_name[0] + last_name
    mock_customer.password = fake.password(length=12)

    # ensure we are getting expected string values 🙄
    mock_customer.__getitem__.side_effect = lambda key: getattr(mock_customer, key) 
    return mock_customer

# payload for create customer endpoint
def create_customer_payload(mock_customer):
    return {
        "name": mock_customer.name,
        "phone": mock_customer.phone,
        "email": mock_customer.email,
        "username": mock_customer.username,
        "password": mock_customer.password
    }

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()


    # test successful creation of customer
    @patch('services.customerService.create_customer')
    def test_create_customer(self, mock_create):
        mock_customer = create_test_customer()
        mock_create.return_value = mock_customer
        payload = create_customer_payload(mock_customer)
        
        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_customer.id)


    # test get all customers
    def test_get_customers(self):
        response = self.app.get('/customers/')
        self.assertEqual(response.status_code, 200)
    

    # test get one customer by id
    @patch('services.customerService.create_customer')
    @patch('services.customerService.get_customer')
    def test_get_customer(self, mock_create, mock_get):
        # create mock customer
        mock_customer = create_test_customer()
        mock_create.return_value = mock_customer
        payload = create_customer_payload(mock_customer)
        create_response = self.app.post('/customers/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        # get customer with mock customer's id
        mock_get.return_value = mock_customer
        get_response = self.app.get(f'/customers/{mock_customer.id}')
        logging.debug(f"GET ONE RESPONSE: {get_response.json}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(mock_customer.name, get_response.json["name"])

    # test update customer endpoint
    @patch('services.customerService.create_customer')
    @patch('services.customerService.update_customer')
    def test_update_customer(self, mock_create, mock_update):
        # create mock customer
        mock_customer = create_test_customer()
        mock_create.return_value = mock_customer
        payload = create_customer_payload(mock_customer)
        response = self.app.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)

        # update mock customer's email
        new_email = fake.email()
        mock_customer.email = new_email
        mock_update.return_value = mock_customer
        update_payload = {"email": new_email}
        response = self.app.put(f'/customers/{mock_customer.id}', json=update_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["email"], mock_customer.email)
    

    # test delete customer endpoint
    @patch('services.customerService.create_customer')
    @patch('services.customerService.delete_customer')
    def test_delete_customer(self, mock_create, mock_delete):
        # create mock customer
        mock_customer = create_test_customer()
        mock_create.return_value = mock_customer
        payload = create_customer_payload(mock_customer)
        response = self.app.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)

        # delete mock customer
        mock_delete.return_value = {
            "status": "success",
            "message": f"Customer with ID {mock_customer.id} has been removed"
        }
        response = self.app.delete(f'/customers/{mock_customer.id}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], f"Customer with ID {mock_customer.id} has been removed")


    # test login endpoint
    @patch('services.customerService.get_token')
    def test_success_authenticate(self, mock_token):
        mock_token.return_value = '123456789'
        payload = {
            "username": fake.user_name(),
            'password': fake.password()
        }

        response = self.app.post('/login/', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['token'], '123456789')