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
from models.customer import Customer
from database import db

fake = Faker()

class TestShoppingCartEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()


    # test create cart
    @patch('services.customerService.get_token')
    @patch('auth.token_auth.current_user')
    def test_create_cart(self, mock_current_user, mock_cart):
        
        mock_user = MagicMock()
        mock_user.id = 3
        mock_current_user.return_value = mock_user

        mock_cart.return_value = "Shopping cart created! Add your products!"
        response = self.app.post('/cart/')
        logging.debug(f"TEST CREATE CART RESPONSE: {response.json}")
        self.assertEqual(response.status_code, 201)


    # test get one cart by id endpoint
    @patch('services.shoppingCartService.get_cart')
    def test_get_cart(self, mock_get):
        mock_get.return_value = {
            "id": 1,
            "customer_id": 1,
            "products": [
                {"id": 1}
            ]
        }
        response = self.app.get('/cart/1')
        self.assertEqual(response.status_code, 200)


    # test get all carts endpoint
    def test_get_carts(self):
        response = self.app.get('/cart/')
        self.assertEqual(response.status_code, 200)
    

    # test add to cart endpoint
    @patch('services.shoppingCartService.add_to_cart')
    def test_add_to_cart(self, mock_product):
        pass
    
    # test remove from cart endpoint
    @patch('services.shoppingCartService.remove_from_cart')
    def test_remove_from_cart(self, mock_product):
        pass
    
    # test update quantity endpoint
    @patch('services.shoppingCartService.update_item_qty')
    def test_update_qty(self, mock_product):
        pass

    # test empty cart endpoint
    @patch('services.shoppingCartService.empty_cart')
    def test_empty_cart(self, mock_cart):
        pass
    
    # test checkout endpoint
    @patch('services.shoppingCartService.checkout')
    def test_checkout(self, mock_cart):
        pass