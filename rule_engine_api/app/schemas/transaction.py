from pydantic import BaseModel

class TransactionBase(BaseModel):
    transaction_id: str
    transaction_amount: float
    merchant_id: str
    client_id: str
    phone_number: str
    ip_address: str
    email_address: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
