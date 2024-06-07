from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
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
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    rule = Column(Text, nullable=False)
