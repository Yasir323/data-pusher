from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data_pusher.schemas.destinations import Destination, DestinationResponse
from data_pusher.database import SessionLocal
from data_pusher import crud

destination_router = APIRouter(prefix="/destinations")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@destination_router.post("/", response_model=DestinationResponse)
def create_destination_for_account(destination: Destination,
                                   db: Session = Depends(get_db)):
    db_destination = crud.create_destination(db, destination=destination)
    return DestinationResponse(
        account_id=db_destination.account_id,
        destination_id=db_destination.id,
        url=db_destination.url,
        http_method=db_destination.http_method,
        headers=db_destination.headers
    )


@destination_router.get("/", response_model=list[DestinationResponse])
def read_all_destinations(db: Session = Depends(get_db)):
    db_destinations = crud.get_all_destinations(db)
    return [
        DestinationResponse(
            account_id=dest.account_id,
            destination_id=dest.id,
            url=dest.url,
            http_method=dest.http_method,
            headers=dest.headers
        ) for dest in db_destinations
    ]


@destination_router.get("/accounts/{account_id}/", response_model=list[DestinationResponse])
def get_destinations_for_account(account_id: int, db: Session = Depends(get_db)):
    db_destinations = crud.get_destinations_by_account(db, account_id=account_id)
    return [
        DestinationResponse(
            account_id=dest.account_id,
            destination_id=dest.id,
            url=dest.url,
            http_method=dest.http_method,
            headers=dest.headers
        ) for dest in db_destinations
    ]


@destination_router.get("/{destination_id}", response_model=DestinationResponse)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return DestinationResponse(
        account_id=db_destination.account_id,
        destination_id=db_destination.id,
        url=db_destination.url,
        http_method=db_destination.http_method,
        headers=db_destination.headers
    )


@destination_router.put("/{destination_id}", response_model=DestinationResponse)
def update_destination(destination_id: int, destination: Destination,
                       db: Session = Depends(get_db)):
    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    updated_destination = crud.update_destination(db, destination_id=destination_id, destination=destination)
    return DestinationResponse(
        account_id=updated_destination.account_id,
        destination_id=updated_destination.id,
        url=updated_destination.url,
        http_method=updated_destination.http_method,
        headers=updated_destination.headers
    )


@destination_router.delete("/{destination_id}", response_model=DestinationResponse)
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    deleted_destination = crud.delete_destination(db, destination_id=destination_id)
    return DestinationResponse(
        account_id=deleted_destination.account_id,
        destination_id=deleted_destination.id,
        url=deleted_destination.url,
        http_method=deleted_destination.http_method,
        headers=deleted_destination.headers
    )
