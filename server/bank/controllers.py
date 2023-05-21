# fastapi
from fastapi import APIRouter
from fastapi_sqlalchemy import db

# starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette import status

# schemas
from server.bank.schemas.request_schemas import EntrySchema, TransferSchema

# models
from server.models import BankAccount, Entry, Transfer

from datetime import datetime

router = APIRouter(
    prefix="/bank",
    tags=["bank"],
    dependencies=[],
    responses={
        400: {"description": "Bad request"}
    },
)


@router.get("/accounts/")
def get_bank_accounts(request: Request):
    user_id = request.state.user_id
    banks = db.session.query(BankAccount).filter(
        BankAccount.user_id == user_id
    ).all()
    return [bank.dict() for bank in banks or []]


@router.get("/accounts/{account_id}/")
def get_a_bank_account(request: Request, account_id: str):
    user_id = request.state.user_id
    bank = db.session.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == user_id
    ).first()
    if not bank:
        return JSONResponse({
            "details": "pass a valid bank account_id"
        }, status_code=status.HTTP_404_NOT_FOUND)
    return bank.dict()


@router.get("/accounts/{account_id}/statements/")
def get_account_statements(request: Request, account_id: str):
    return {}


@router.get("/accounts/{account_id}/statements/{statement_id}/")
def get_an_account_statement(request: Request, account_id: str, statement_id: str):
    return {}


@router.get("/accounts/{account_id}/entries/")
def get_entries(request: Request, account_id: str):
    user_id = request.state.user_id

    bank = db.session.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == user_id
    ).first()
    if not bank:
        return JSONResponse({
            "details": "pass a valid bank account_id"
        }, status_code=status.HTTP_404_NOT_FOUND)

    entries = db.session.query(Entry).filter(
        Entry.bank_account_id == account_id,
        Entry.entry_type == "deposit"
    ).all()
    return [entry.dict() for entry in entries]


@router.post("/accounts/{account_id}/deposit/")
def deposit_amount(request: Request, account_id: str, payload: EntrySchema):
    user_id = request.state.user_id

    bank = db.session.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == user_id
    ).first()
    if not bank:
        return JSONResponse({
            "details": "pass a valid bank account_id"
        }, status_code=status.HTTP_404_NOT_FOUND)

    entry = Entry(
        amount=payload.amount,
        entry_type="deposit",
        bank_account_id=bank.id,
        created_at=datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()

    bank.amount = bank.amount + payload.amount
    db.session.add(bank)
    db.session.commit()
    return entry.dict()


@router.post("/accounts/{account_id}/withdraw/")
def withdraw_amount(request: Request, account_id: str, payload: EntrySchema):
    user_id = request.state.user_id

    bank = db.session.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == user_id
    ).first()
    if not bank:
        return JSONResponse({
            "details": "pass a valid bank account_id"
        }, status_code=status.HTTP_404_NOT_FOUND)

    # TODO: check for balance availability
    if bank.amount < payload.amount:
        return JSONResponse({
            "details": "insufficient balance"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    entry = Entry(
        amount=payload.amount,
        entry_type="withdraw",
        bank_account_id=bank.id,
        created_at=datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()

    bank.amount = bank.amount - payload.amount
    db.session.add(bank)
    db.session.commit()
    return entry.dict()


@router.post("/accounts/{account_id}/transfer/")
def transfer_amount(request: Request, account_id: str, destination_account_id: str, payload: TransferSchema):
    user_id = request.state.user_id

    source_bank = db.session.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == user_id
    ).first()
    if not source_bank:
        return JSONResponse({
            "details": "pass a valid bank account_id"
        }, status_code=status.HTTP_404_NOT_FOUND)

    # TODO: check for balance availability
    if source_bank.amount < payload.amount:
        return JSONResponse({
            "details": "insufficient balance"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    if account_id == destination_account_id:
        return JSONResponse({
            "details": "can't transfer to same bank account"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    destination_bank = db.session.query(BankAccount).filter(
        BankAccount.id == destination_account_id
    ).first()

    transfer = Transfer(
        amount=payload.amount,
        source_bank_account_id=source_bank.id,
        destination_bank_account_id=destination_bank.id,
        created_at=datetime.utcnow()
    )
    db.session.add(transfer)
    db.session.commit()

    # TODO: decrease amount in source_bank
    source_bank.amount = source_bank.amount - payload.amount
    db.session.add(source_bank)
    db.session.commit()

    # TODO: increase amount in destination_bank
    destination_bank.amount = destination_bank.amount + payload.amount
    db.session.add(destination_bank)
    db.session.commit()

    return transfer.dict()
