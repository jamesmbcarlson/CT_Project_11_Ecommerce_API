from flask import Blueprint
from controllers.customerController import save, find_all, get_customer

customer_blueprint = Blueprint("customer_bp", __name__)

customer_blueprint.route('/', methods=['POST'])(save) # create customer
customer_blueprint.route('/', methods=['GET'])(find_all) # view all
customer_blueprint.route('/<customer_id>', methods=['GET'])(get_customer) # view customer at id
customer_blueprint.route('/update/<customer_id>', methods=['PUT'])() # update customer at id
customer_blueprint.route('/delete/<customer_id>', methods=['DELETE'])() # delete customer at id
