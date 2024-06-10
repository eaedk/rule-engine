# app/api/v0/endpoints/transaction.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import crud
from app.schemas.transaction import TransactionCreate
from app.services.rule_engine import apply_rules
from app.responses import StandardResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/check-transaction", response_model=StandardResponse)
def check_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Check a transaction against rules and return approval status.

    Args:
        transaction (TransactionCreate): The transaction to check.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        StandardResponse: Standardized response containing status information.
    """
    rules = crud.get_rules(db)
    transaction_dict = transaction.dict()
    check = apply_rules(transaction_dict, rules)
    if check["has_succeeded"]:
        return StandardResponse(
            status="approved", status_code=200, message="Transaction approved"
        )
    else:
        rejection_message = f"Transaction rejected:{check['message']}"
        return StandardResponse(
            status="rejected", status_code=400, message=rejection_message
        )


@router.post("/save-transaction")
def save_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.create_transaction(db, transaction)
    return db_transaction
