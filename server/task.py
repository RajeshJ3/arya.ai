# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# celery
from celery import Celery
from celery.beat import crontab

# python
from datetime import datetime

# models
from server.models import BankAccount, Entry, Transfer, Statement

# custom
from server.core.settings import (
    BROKER_URL,
    TIMEZONE,
    DATABASE_URL
)

session_maker = sessionmaker(bind=create_engine(DATABASE_URL))

celery = Celery("tasks", broker=BROKER_URL)
celery.conf.timezone = TIMEZONE


def generate_and_save_statement(account_id: int):
    session = session_maker()    

    # fetch bank
    bank = session.query(BankAccount).filter(
        BankAccount.id == account_id
    ).first()

    # fetch all transactions
    entries = session.query(Entry).filter(
        Entry.bank_account_id == account_id
    ).all()

    # fetch all credits
    credits = session.query(Transfer).filter(
        Transfer.destination_bank_account_id == account_id
    ).all()

    # fetch all debits
    debits = session.query(Transfer).filter(
        Transfer.source_bank_account_id == account_id
    ).all()

    # fetch MAB
    mab = bank.amount

    # fetch all no of transactions
    transactions_count = len(entries) + len(credits) + len(debits)

    data = {
        "entries": [entry.dict() for entry in entries],
        "credits": [credit.dict() for credit in credits],
        "debits": [debit.dict() for debit in debits],
        "mab": mab,
        "transactions_count": transactions_count,
    }

    now = datetime.now()

    statement = Statement(
        month=now.month,
        year=now.year,
        json_data=data,
        bank_account_id=int(account_id),
        created_at=datetime.utcnow()
    )
    session.add(statement)
    session.commit()

    session.close()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # Schedule: 7:00AM of each month
        crontab(day_of_month="1", hour=7, minute=0),
        triger_monthly_statement_generation.s(),
        name='triger-monthly-statement-generation'
    )


@celery.task
def triger_monthly_statement_generation():
    print("[triger_monthly_statement_generation] Task started")

    # fetch all banks
    with session_maker() as session:
        banks = session.query(BankAccount).all()

    # NOTE: this can be done better, by scheduling jobs for the bank accounts in batch.
    # generate statement for each bank account
    for bank in banks:
        generate_and_save_statement(bank.id)

    print("[triger_monthly_statement_generation] Task completed")
