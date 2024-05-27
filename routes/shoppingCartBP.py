from flask import Blueprint
from controllers.shoppingCartController import save, find_all, get_shopping_cart

shopping_cart_blueprint = Blueprint("shopping_cart_bp", __name__)

shopping_cart_blueprint.route('/', methods=['POST'])(save)
shopping_cart_blueprint.route('/<shopping_cart_id>', methods=['GET'])(get_shopping_cart) # view shopping cart at id

# TO-DO:
    # add items to card '/add/<product_id>'
    # remove item from cart '/remove/<product_id>'
    # update item quantity '/update/<product_id>?qty=<qty>' <--??
    # empty cart '/empty/<shopping_cart_id>'
    # checkout '/checkout/<shopping_cart_id>'
    # save cart?? - just save on its own; the difference is it doesn't get deleted

    