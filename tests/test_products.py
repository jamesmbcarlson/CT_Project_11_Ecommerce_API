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


# create mock product with randomized data
def create_test_product():
    mock_product = MagicMock()
    mock_product.id = fake.random_number(digits=3)
    mock_product.name = fake.word()
    mock_product.price = float(fake.random_number(digits=2))
    mock_product.stock_quantity = fake.random_number(digits=2)

    # ensure we are getting expected values 🙄
    mock_product.__getitem__.side_effect = lambda key: getattr(mock_product, key) 
    return mock_product

# payload for create product endpoint
def create_product_payload(mock_product):
    return {
        "name": mock_product.name,
        "price": mock_product.price,
        "stock_quantity": mock_product.stock_quantity
    }

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()


    # test successful creation of product
    @patch('services.productService.create_product')
    def test_create_product(self, mock_create):
        mock_product = create_test_product()
        mock_create.return_value = mock_product
        payload = create_product_payload(mock_product)
        
        response = self.app.post('/products/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_product.id)


    # test get all products
    def test_get_products(self):
        response = self.app.get('/products/')
        self.assertEqual(response.status_code, 200)
    

    # test get one product by id
    @patch('services.productService.create_product')
    @patch('services.productService.get_product')
    def test_get_product(self, mock_create, mock_get):
        # create mock product
        mock_product = create_test_product()
        mock_create.return_value = mock_product
        payload = create_product_payload(mock_product)
        create_response = self.app.post('/products/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        # get product with mock product's id
        mock_get.return_value = mock_product
        get_response = self.app.get(f'/products/{mock_product.id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(mock_product.name, get_response.json["name"])


    # test update product endpoint
    @patch('services.productService.create_product')
    @patch('services.productService.update_product')
    def test_update_product(self, mock_create, mock_update):
        # create mock product
        mock_product = create_test_product()
        mock_create.return_value = mock_product
        payload = create_product_payload(mock_product)
        response = self.app.post('/products/', json=payload)
        self.assertEqual(response.status_code, 201)

        # update mock product's name
        new_name = fake.word()
        mock_product.name = new_name
        mock_update.return_value = mock_product
        update_payload = {"name": new_name}
        response = self.app.put(f'/products/{mock_product.id}', json=update_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], mock_product.name)
    

    # test delete product endpoint
    @patch('services.productService.create_product')
    @patch('services.productService.delete_product')
    def test_delete_product(self, mock_create, mock_delete):
        # create mock product
        mock_product = create_test_product()
        mock_create.return_value = mock_product
        payload = create_product_payload(mock_product)
        response = self.app.post('/products/', json=payload)
        self.assertEqual(response.status_code, 201)

        # delete mock product
        mock_delete.return_value = {
            "status": "success",
            "message": f"Product with ID {mock_product.id} has been removed"
        }
        response = self.app.delete(f'/products/{mock_product.id}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], f"Product with ID {mock_product.id} has been removed")