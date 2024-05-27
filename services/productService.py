from sqlalchemy.orm import Session
from database import db
from models.product import Product

# Creates new product
def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(
                name=product_data['name'], 
                price=product_data['price'],
                stock_quantity=product_data['stock_quantity'])
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product
    
    
# Get all products in database
def find_all(page=1, per_page=10):
    query = db.select(Product).limit(per_page).offset((page-1)*per_page)
    products = db.session.execute(query).scalars().all()
    return products

# TO-DO: update product at id

# TO-DO: delete product at id