from pydantic import BaseModel


class EntrySchema(BaseModel):
    amount: int = 1


class TransferSchema(BaseModel):
    amount: int = 1
