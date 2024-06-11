from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    """
    Represents a financial transaction.

    Attributes:
        id (int): The primary key and unique identifier for the transaction.
        transaction_id (str): A unique identifier for the transaction.
        transaction_amount (float): The amount of the transaction.
        merchant_id (str): The identifier for the merchant involved in the transaction.
        client_id (str): The identifier for the client involved in the transaction.
        phone_number (str): The phone number associated with the transaction.
        ip_address (str): The IP address from which the transaction was made.
        email_address (str): The email address associated with the transaction.
        amount (float): The total amount of the transaction.
    """

    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    transaction_amount = Column(Float)
    merchant_id = Column(String)
    client_id = Column(String)
    phone_number = Column(String)
    ip_address = Column(String)
    email_address = Column(String)
    amount = Column(Float)


class Rule(Base):
    """
    Represents a rule to be applied to transactions.

    Attributes:
        id (int): The primary key and unique identifier for the rule.
        description (str): A brief description of the rule.
        rule (str): The rule logic expressed as a string.
    """

    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    rule = Column(Text, nullable=False)
