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
