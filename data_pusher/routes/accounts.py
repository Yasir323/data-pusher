from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data_pusher.schemas.accounts import AccountResponse, Account
from data_pusher.database import SessionLocal
from data_pusher import crud

account_router = APIRouter(prefix="/accounts")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@account_router.post("/", response_model=AccountResponse)
async def add_account(account: Account, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_account = crud.create_account(db, account=account)
    return AccountResponse(
        email=db_account.email,
        name=db_account.name,
        id_=db_account.id,
        token=db_account.token,
        website=db_account.website or ""
    )


@account_router.get("/", response_model=list[AccountResponse])
async def read_all_accounts(db: Session = Depends(get_db)):
    db_accounts = crud.get_all_accounts(db)
    return [
        AccountResponse(
            email=account.email,
            name=account.name,
            id_=account.id,
            token=account.token,
            website=account.website or ""
        ) for account in db_accounts
    ]


@account_router.get("/{account_id}", response_model=AccountResponse)
async def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(
        email=db_account.email,
        name=db_account.name,
        id_=db_account.id,
        token=db_account.token,
        website=db_account.website or ""
    )


@account_router.put("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account: Account, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    updated_account = crud.update_account(db, account_id=account_id, account=account)
    return AccountResponse(
        email=updated_account.email,
        name=updated_account.name,
        id_=updated_account.id,
        token=updated_account.token,
        website=updated_account.website or ""
    )


@account_router.delete("/{account_id}", response_model=AccountResponse)
async def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    deleted_account = crud.delete_account(db, account_id=account_id)
    return AccountResponse(
        email=deleted_account.email,
        name=deleted_account.name,
        id_=deleted_account.id,
        token=deleted_account.token,
        website=deleted_account.website or ""
    )
