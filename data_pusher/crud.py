from typing import Optional, Type, List

from sqlalchemy.orm import Session
from .database import Account, Destination
from .schemas.accounts import Account as AccountSchema
from .schemas.destinations import Destination as DestinationSchema
from .utils import generate_token


def create_account(db: Session, account: AccountSchema) -> Account:
    token = generate_token()
    db_account = Account(email=account.email, name=account.name, token=token, website=str(account.website))
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_all_accounts(db: Session) -> List[Type[Account]]:
    return db.query(Account).all()


def get_account(db: Session, account_id: int) -> Optional[Type[Account]]:
    return db.query(Account).filter(Account.id == account_id).first()


def update_account(db: Session, account_id: int, account: AccountSchema) -> Optional[Type[Account]]:
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account:
        db_account.email = account.email
        db_account.name = account.name
        db_account.website = str(account.website)
        db.commit()
        db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: int) -> Optional[Type[Account]]:
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account


def get_account_by_email(db: Session, email: str) -> Optional[Type[Account]]:
    return db.query(Account).filter(Account.email == email).first()


# Destination CRUD Operations
def create_destination(db: Session, destination: DestinationSchema) -> Destination:
    db_destination = Destination(
        account_id=destination.account_id,
        url=str(destination.url),
        http_method=destination.http_method.value,
        headers=destination.headers
    )
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination


def get_all_destinations(db: Session) -> List[Type[Destination]]:
    return db.query(Destination).all()


def get_destination(db: Session, destination_id: int) -> Optional[Type[Destination]]:
    return db.query(Destination).filter(Destination.id == destination_id).first()


def update_destination(db: Session, destination_id: int, destination: DestinationSchema) -> Optional[Type[Destination]]:
    db_destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if db_destination:
        db_destination.url = str(destination.url)
        db_destination.http_method = destination.http_method.value
        db_destination.headers = destination.headers
        db.commit()
        db.refresh(db_destination)
    return db_destination


def delete_destination(db: Session, destination_id: int) -> Optional[Type[Destination]]:
    db_destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if db_destination:
        db.delete(db_destination)
        db.commit()
    return db_destination


def get_destinations_by_account(db: Session, account_id: int) -> List[Type[Destination]]:
    return db.query(Destination).filter(Destination.account_id == account_id).all()
