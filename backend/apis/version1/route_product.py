from typing import List
from uuid import UUID

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.products import create_new_product
from db.repository.products import delete_product_by_id
from db.repository.products import list_products
from db.repository.products import retreive_product
from db.repository.products import update_product_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.products import ProductCreate
from schemas.products import ShowProduct
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/create_product/", response_model=ShowProduct)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    product = create_new_product(job=product, db=db, owner_id=current_user.id)
    return product


@router.get(
    "/get/{id}", response_model=ShowProduct
)  # if we keep just "{id}" . it would stat catching all routes
def read_product(id: int, db: Session = Depends(get_db)):
    product = retreive_product(id=id, db=db)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with this id {id} does not exist",
        )
    return product


@router.get("/all", response_model=List[ShowProduct])
def read_products(db: Session = Depends(get_db)):
    products = list_products(db=db)
    return products


@router.put("/update/{id}")
def update_product(id: UUID, job: ProductCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_product_by_id(id=id, job=job, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id {id} not found",
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_product(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    product = retreive_product(id=id, db=db)
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with {id} does not exist",
        )
    print(product.owner_id, current_user.id, current_user.is_superuser)
    if product.owner_id == current_user.id or current_user.is_superuser:
        delete_product_by_id(id=id, db=db, owner_id=current_user.id)
        return {"msg": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/detail/{id}")
def product_detail(id: UUID, request: Request, db: Session = Depends(get_db)):
    product = retreive_product(id=id, db=db)
    return templates.TemplateResponse(
        "products/detail.html", {"request": request, "product": product}
    )
