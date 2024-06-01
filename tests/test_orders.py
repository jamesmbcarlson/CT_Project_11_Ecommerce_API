# get app.py from parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from app import create_app

import unittest
from unittest.mock import patch
from faker import Faker

fake = Faker()

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # test get all orders endpoint
    def test_get_orders(self):
        response = self.app.get('/orders/')
        self.assertEqual(response.status_code, 200)
    

    # test get one order by id endpoint
    @patch('services.orderService.get_order')
    def test_get_order(self, mock_get):
        mock_get.return_value = {
            "id": 1,
            "customer_id": 1,
            "products": [
                {"id": 1}
            ]
        }
        response = self.app.get('/orders/1')
        self.assertEqual(response.status_code, 200)
    
    # test track order endpoint
    @patch('services.orderService.track_order')
    def test_track_order(self, mock_track):
        mock_track.return_value = "Your order (ID 1) from 2024-05-31 will arrive today!"
        response = self.app.get('/orders/track/1')
        self.assertEqual(response.status_code, 200)