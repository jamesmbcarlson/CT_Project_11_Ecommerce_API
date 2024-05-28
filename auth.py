from flask_httpauth import HTTPTokenAuth
from utils.util import decode_token
from services import customerService
import logging

token_auth = HTTPTokenAuth()

logging.basicConfig(level=logging.DEBUG)

@token_auth.verify_token
def verify(token):
    logging.debug(f"Verifying token: {token}")
    customer_id = decode_token(token)
    logging.debug(f"Decoded customer ID: {customer_id}")
    if customer_id:
        customer = customerService.get_customer(customer_id)
        logging.debug(f"Retrieved customer: {customer}")
        return customer
    else:
        return None
    
@token_auth.error_handler
def handle_error(status_code):
    return {"error": "Invalid Token. Please try again"}, status_code