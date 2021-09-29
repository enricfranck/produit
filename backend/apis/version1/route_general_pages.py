from db.repository.products import list_products
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    product = list_products(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": product}
    )
