from uuid import UUID

from db.models.products import Product
from schemas.products import ProductCreate
from sqlalchemy.orm import Session


def create_new_product(product: ProductCreate, db: Session, owner_id: int):
    product_object = Product(**product.dict(), url_image="https://localhost/" + product.nom + ".png", owner_id=owner_id)
    db.add(product_object)
    db.commit()
    db.refresh(product_object)
    return product_object


def retreive_product(id: UUID, db: Session):
    item = db.query(Product).filter(Product.id == id).first()
    return item


def list_products(db: Session):
    product = db.query(Product).all()
    return product


def update_product_by_id(id: int, product: ProductCreate, db: Session, owner_id):
    existing_product = db.query(Product).filter(Product.id == id)
    if not existing_product.first():
        return 0
    product.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_product.update(product.__dict__)
    db.commit()
    return 1


def delete_product_by_id(id: UUID, db: Session, owner_id):
    existing_job = db.query(Product).filter(Product.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
