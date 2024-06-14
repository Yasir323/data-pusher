from fastapi import FastAPI

from data_pusher.routes.destinations import destination_router
from data_pusher.routes.accounts import account_router
from data_pusher.routes.data import data_router

from data_pusher.database import Base, engine


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()


app.include_router(destination_router)
app.include_router(account_router)
app.include_router(data_router)
