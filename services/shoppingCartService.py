from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.order import Order
from models.customer import Customer
from models.product import Product

# Creates new shopping_cart
def save(shopping_cart_data):
    with Session(db.engine) as session:
        with session.begin():
           
            # Check that the customer_id is associated with a customer
            customer_id = shopping_cart_data['customer_id']
            customer = session.get(Customer, customer_id)

            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")
            
            # Create a new shopping_cart in the database
            new_shopping_cart = Order(customer_id=shopping_cart_data['customer_id'])
            session.add(new_shopping_cart)
            session.commit()

        session.refresh(new_shopping_cart)

        return new_shopping_cart
    
# TO-DO:
    # add items to card '/add/<product_id>'
    # remove item from cart '/remove/<product_id>'
    # update item quantity '/update/<product_id>?qty=<qty>' <--??
    # empty cart '/empty/<shopping_cart_id>'
    # checkout '/checkout/<shopping_cart_id>'