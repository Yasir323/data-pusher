import asyncio

import httpx
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from data_pusher.crud import get_destinations_by_account
from data_pusher.database import SessionLocal, Account

data_router = APIRouter(prefix="/server/incoming_data")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@data_router.post("/")
async def handle_incoming_data(request: Request, db: Session = Depends(get_db)):
    headers = request.headers
    if "CL-X-TOKEN" not in headers:
        return {"message": "Un Authenticate"}

    token = headers["CL-X-TOKEN"]
    account = db.query(Account).filter(Account.token == token).first()
    if not account:
        return {"message": "Un Authenticate"}

    data = await request.json()
    destinations = get_destinations_by_account(db, account_id=account.id)

    async with httpx.AsyncClient() as client:
        tasks = []
        for destination in destinations:
            if destination.http_method == "GET":
                tasks.append(asyncio.create_task(client.get(destination.url, params=data, headers=destination.headers)))
            elif destination.http_method == "POST":
                tasks.append(asyncio.create_task(client.post(destination.url, json=data, headers=destination.headers)))
            elif destination.http_method == "PUT":
                tasks.append(asyncio.create_task(client.put(destination.url, json=data, headers=destination.headers)))
            elif destination.http_method == "PATCH":
                tasks.append(asyncio.create_task(client.patch(destination.url, json=data, headers=destination.headers)))
            elif destination.http_method == "DELETE":
                tasks.append(asyncio.create_task(client.delete(destination.url, headers=destination.headers)))
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    return {"message": "Success"}
