from apis.base import api_router
from core.config import settings
from db.base import Base
from db.repository import users
from db.session import engine
from db.session import SessionLocal
from db.utils import check_db_connected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    user = users.get_user_by_email(email=settings.FIRST_SUPERUSER, db=db)
    if not user:
        user_in: UserCreate = UserCreate(
            username="longrich",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = users.create_supper_admin(user_in, db)


def include_router(app):
    app.include_router(api_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    db = SessionLocal()
    include_router(app)
    configure_static(app)
    create_tables()
    init_db(db)
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()
