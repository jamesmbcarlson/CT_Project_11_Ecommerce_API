from flask import Blueprint
from controllers.orderController import create_order, find_all, get_order

order_blueprint = Blueprint("order_bp", __name__)

order_blueprint.route('/', methods=['POST'])(create_order)
order_blueprint.route('/', methods=['GET'])(find_all)
order_blueprint.route('/<order_id>', methods=['GET'])(get_order) # view order at id

# TO-DO: track order
    # Your order is on its way! Expected Delivery: 5/30/24
    # Your order has been completed!
    # Your order has been cancelled

# view all orders for customer id
# '/customer/<customer_id>'

# order_blueprint.route('/cancel/<order_id>', methods=['PUT'])() # cancel order at id