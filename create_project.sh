#!/bin/bash

# Create directory structure
mkdir -p rule_engine_api/app/{api/v0,core,db,schemas,services}
touch rule_engine_api/{docker-compose.yml,Dockerfile,.env,requirements.txt}
touch rule_engine_api/app/{main.py,__init__.py}
touch rule_engine_api/app/api/{__init__.py}
touch rule_engine_api/app/api/v0/{__init__.py,endpoints.py}
touch rule_engine_api/app/core/{__init__.py,config.py}
touch rule_engine_api/app/db/{__init__.py,models.py,session.py,crud.py}
touch rule_engine_api/app/schemas/{__init__.py,transaction.py}
touch rule_engine_api/app/services/{__init__.py,rule_engine.py}

# Populate files with initial content

# .env file content
cat <<EOL > rule_engine_api/.env
POSTGRES_DB=rule_engine_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql://\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@db:5432/\${POSTGRES_DB}
EOL

# requirements.txt content
cat <<EOL > rule_engine_api/requirements.txt
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic
EOL

# docker-compose.yml content
cat <<EOL > rule_engine_api/docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: \${POSTGRES_DB}
      POSTGRES_USER: \${POSTGRES_USER}
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - rule_engine_network

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - rule_engine_network

volumes:
  postgres_data:

networks:
  rule_engine_network:
    driver: bridge
EOL

# Dockerfile content
cat <<EOL > rule_engine_api/Dockerfile
FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

# config.py content
cat <<EOL > rule_engine_api/app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
EOL

# session.py content
cat <<EOL > rule_engine_api/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
EOL

# models.py content
cat <<EOL > rule_engine_api/app/db/models.py
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
EOL

# crud.py content
cat <<EOL > rule_engine_api/app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models, schemas

def get_rules(db: Session):
    return db.query(models.Rule).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
EOL

# transaction.py content
cat <<EOL > rule_engine_api/app/schemas/transaction.py
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
        orm_mode = True
EOL

# rule_engine.py content
cat <<EOL > rule_engine_api/app/services/rule_engine.py
from typing import List

def apply_rules(transaction: dict, rules: List[str]) -> bool:
    for rule in rules:
        try:
            if not eval(rule, {"transaction": transaction}):
                return False
        except Exception as e:
            # Log the exception or handle it as needed
            return False
    return True
EOL

# endpoints.py content
cat <<EOL > rule_engine_api/app/api/v0/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db import models, crud
from app.schemas import transaction as transaction_schema
from app.services.rule_engine import apply_rules

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/check-transaction")
def check_transaction(transaction: transaction_schema.TransactionCreate, db: Session = Depends(get_db)):
    rules = [rule.rule for rule in crud.get_rules(db)]
    transaction_dict = transaction.dict()
    if apply_rules(transaction_dict, rules):
        return {"status": "approved"}
    else:
        return {"status": "rejected"}

@router.post("/save-transaction")
def save_transaction(transaction: transaction_schema.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.create_transaction(db, transaction)
    return db_transaction
EOL

# main.py content
cat <<EOL > rule_engine_api/app/main.py
from fastapi import FastAPI
from app.api.v0 import endpoints
from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(endpoints.router, prefix="/v0")
EOL

echo "Directory structure and files have been created successfully."
