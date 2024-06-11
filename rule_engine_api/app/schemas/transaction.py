from pydantic import BaseModel


class TransactionBase(BaseModel):
    """
    Base model for transactions.

    Attributes:
        transaction_id (str): Unique identifier for the transaction.
        transaction_amount (float): The amount involved in the transaction.
        merchant_id (str): Identifier for the merchant involved in the transaction.
        client_id (str): Identifier for the client involved in the transaction.
        phone_number (str): Phone number associated with the transaction.
        ip_address (str): IP address from where the transaction originated.
        email_address (str): Email address associated with the transaction.
        amount (float): Amount of the transaction.
    """

    transaction_id: str
    transaction_amount: float
    merchant_id: str
    client_id: str
    phone_number: str
    ip_address: str
    email_address: str
    amount: float


class TransactionCreate(TransactionBase):
    """
    Model for creating a new transaction.

    Inherits from:
        TransactionBase: The base model for transactions.
    """

    pass


class Transaction(TransactionBase):
    """
    Model representing a transaction with an ID.

    Attributes:
        id (int): Unique identifier for the transaction.

    Config:
        from_attributes (bool): Allow population from ORM attributes.
    """

    id: int

    class Config:
        from_attributes = True
