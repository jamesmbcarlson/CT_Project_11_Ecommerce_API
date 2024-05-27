from flask import Blueprint
from controllers.userController import login

login_blueprint = Blueprint("login_bp", __name__)

login_blueprint.route('/', methods=['POST'])(login)