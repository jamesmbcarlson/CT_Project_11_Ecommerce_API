from flask import Blueprint
from controllers.productController import save, find_all, get_product

product_blueprint = Blueprint("product_bp", __name__)

product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(find_all) # view all products
product_blueprint.route('/<product_id>', methods=['GET'])(get_product) # view product at id
product_blueprint.route('/update/<product_id>', methods=['PUT'])() # update product at id
product_blueprint.route('/delete/<product_id>', methods=['DELETE'])() # delete product at id
