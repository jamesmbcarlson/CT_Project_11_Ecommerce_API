from flask import request, jsonify
from sqlalchemy.exc import NoResultFound
from schemas.shoppingCartSchema import shopping_cart_schema, shopping_carts_schema, update_product_quantity_schema
from services import shoppingCartService
from marshmallow import ValidationError
from auth import token_auth

# create empty shopping cart -- must be logged in to shop!
@token_auth.login_required 
def create_cart():
    try:
        logged_in_user = token_auth.current_user()
        print("CREATE CART WITH ID", logged_in_user.id)
        shoppingCartService.create_cart(logged_in_user.id)
        return "Shopping cart created! Add your products!", 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

# get one shopping_cart by ID
def get_shopping_cart(cart_id):
    shopping_cart = shoppingCartService.get_cart(cart_id)
    if shopping_cart:
        return shopping_cart_schema.jsonify(shopping_cart)
    else:
        resp = {
            "status": "error",
            "message": f"A shopping cart with ID {cart_id} does not exist"
        }
        return resp, 404
    
def add_to_cart(product_id):
    # TO-DO: ADD VALIDATION
    try:
        shoppingCartService.add_to_cart(product_id)
        return "Product added!"
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404

def remove_from_cart(product_id):
    # TO-DO: ADD VALIDATION
    try:
        shoppingCartService.remove_from_cart(product_id)
        return "Product removed!"
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404

def update_item_qty(product_id):
    try:
        update_data = update_product_quantity_schema.load(request.json)
        shoppingCartService.update_item_qty(product_id, update_data)
        return "Product quantity modified!"
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404

def empty_cart():
    try:
        shoppingCartService.empty_cart()
        return "Your cart is now empty."
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404

def checkout():
    try:
        shoppingCartService.checkout()
        return "You have successfully placed an order!"
    except Exception as err:
        return jsonify({"error": str(err)}), 400

def set_active_cart(shopping_cart_id):
    # TO-DO: ADD VALIDATION
    shoppingCartService.set_current_cart(shopping_cart_id)
    return get_shopping_cart(shopping_cart_id)
    

# get all shopping_carts
def find_all():
    # get pagination parameters (or set to default)
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    shopping_carts = shoppingCartService.find_all(page, per_page)
    return shopping_carts_schema.jsonify(shopping_carts), 200