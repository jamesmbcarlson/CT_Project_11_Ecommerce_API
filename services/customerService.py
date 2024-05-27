from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token

# Creates new customer
def save(customer_data):
    with Session(db.engine) as session:
        with session.begin():
            # check if username is already in database
            customer_query = select(Customer).where(Customer.username == customer_data['username'])
            check_username = db.session.execute(customer_query).scalars().first()
            if check_username:
                raise ValueError("Username is already taken. Please create a unique username.")
            
            # add new customer to database
            new_customer = Customer(
                name=customer_data['name'], 
                email=customer_data['email'], 
                phone=customer_data['phone'],
                username=customer_data['username'],
                password=generate_password_hash(customer_data['password'])
                )
            session.add(new_customer)
            session.commit()
        session.refresh(new_customer)
        return new_customer
    
    
# Get all customers in database
def find_all():
    query = db.select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers

# Get one customer by ID
def get_customer(customer_id):
    return db.session.get(Customer, customer_id)

# TO-DO: update customer at id

# TO-DO: delete customer at id

# return token for valid login
def get_token(username, password):
    # query the customer table for given username
    query = db.select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalars().first()
    # validate password for paired username
    if customer is not None and check_password_hash(customer.password, password):
        auth_token = encode_token(customer.id)
        return auth_token
    else:
        return None