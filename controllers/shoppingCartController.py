from flask import request, jsonify
from schemas.shoppingCartSchema import shopping_cart_schema, shopping_carts_schema
from services import shoppingCartService
from marshmallow import ValidationError
from caching import cache
from auth import token_auth

# create new shopping cart
@token_auth.login_required
def save():
    try:
        raw_data = request.json
        logged_in_user = token_auth.current_user()
        raw_data['customer_id'] = logged_in_user.id
        shopping_cart_data = shopping_cart_schema.load(raw_data)
        shopping_cart_save = shoppingCartService.save(shopping_cart_data)
        return shopping_cart_schema.jsonify(shopping_cart_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

# get all shopping_carts
# @cache.cached(timeout=20) # took this out for smoother testing
def find_all():
    # get pagination parameters (or set to default)
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    shopping_carts = shoppingCartService.find_all(page, per_page)
    return shopping_carts_schema.jsonify(shopping_carts), 200

# get one shopping_cart by ID
def get_shopping_cart(shopping_cart_id):
    shopping_cart = shoppingCartService.get_shopping_cart(shopping_cart_id)
    if shopping_cart:
        return shopping_cart_schema.jsonify(shopping_cart)
    else:
        resp = {
            "status": "error",
            "message": f"A shopping_cart with ID {shopping_cart_id} does not exist"
        }
        return resp, 404
    

# TO-DO: / note -  Shopping carts should get deleted upon checkout; they should only remain saved if a user does not complete their checkout; after 48 hours, delete the cart