from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

from fastapi_sqlalchemy import db

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    bank_accounts = relationship("BankAccount")

    def dict(self): return {
        "id": self.id,
        "email": self.email,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "bank_accounts": self.bank_accounts,
    }


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))

    entries = relationship("Entry")
    # transfers = relationship("Transfer")
    # statements = relationship("Statement")

    def dict(self):
        credits = db.session.query(Transfer).filter(
            Transfer.destination_bank_account_id == self.id
        ).all()
        debits = db.session.query(Transfer).filter(
            Transfer.source_bank_account_id == self.id
        ).all()

        return {
            "id": self.id,
            "amount": self.amount,
            "user_id": self.user_id,
            "entries": self.entries,
            "credits": credits,
            "debits": debits,
            # "statements": self.statements,
        }


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False, default=0)
    entry_type = Column(String, nullable=False)  # deposit/withdraw

    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"))

    created_at = Column(DateTime, nullable=False)

    def dict(self): return {
        "id": self.id,
        "amount": self.amount,
        "entry_type": self.entry_type,
        "bank_account_id": self.bank_account_id,
        "created_at": self.created_at,
    }


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False, default=0)

    source_bank_account_id = Column(
        Integer,
        ForeignKey("bank_accounts.id")
    )
    source_bank_account = relationship(
        "BankAccount",
        foreign_keys=[source_bank_account_id]
    )

    destination_bank_account_id = Column(
        Integer,
        ForeignKey("bank_accounts.id")
    )
    destination_bank_account = relationship(
        "BankAccount",
        foreign_keys=[destination_bank_account_id]
    )

    created_at = Column(DateTime, nullable=False)

    def dict(self): return {
        "id": self.id,
        "amount": self.amount,
        "source_bank_account_id": self.source_bank_account_id,
        "destination_bank_account_id": self.destination_bank_account_id,
        "created_at": self.created_at,
    }


# class Statement(Base):
#     __tablename__ = "statements"

#     id = Column(Integer, primary_key=True, index=True)
#     month = Column(Integer, nullable=False)
#     year = Column(Integer, nullable=False)

#     bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"))

#     created_at = Column(DateTime, nullable=False)

#     def dict(self): return {
#         "id": self.id,
#         "month": self.month,
#         "year": self.year,
#         "bank_account_id": self.bank_account_id,
#         "created_at": self.created_at,
#     }
