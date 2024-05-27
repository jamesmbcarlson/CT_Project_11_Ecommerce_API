from datetime import datetime, timedelta, timezone
import jwt
import os

# Create a secret key constant variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'sub': customer_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token