import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import crud
from app.schemas.transaction import TransactionCreate
from app.services.rule_engine import apply_rules
from app.responses import StandardResponse
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the log format
)
# Create a logger
logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/check-transaction", response_model=StandardResponse)
async def check_transaction(
    transaction: TransactionCreate, db: Session = Depends(get_db)
):
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

    # Async rule evaluation
    loop = asyncio.get_event_loop()
    check = await loop.run_in_executor(None, apply_rules, transaction_dict, rules)

    if check["has_succeeded"]:
        logger.info("Transaction approved: %s", transaction)
        return StandardResponse(
            status="approved", status_code=200, message="Transaction approved"
        )
    else:
        rejection_message = f"Transaction rejected: {check['message']}"
        logger.info("Transaction rejected: %s", transaction)
        return StandardResponse(
            status="rejected", status_code=400, message=rejection_message
        )


@router.post("/save-transaction")
def save_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Save a transaction to the database.

    Args:
        transaction (TransactionCreate): The transaction to save.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        TransactionCreate: The saved transaction.
    """
    db_transaction = crud.create_transaction(db, transaction)
    logger.info("Transaction saved: %s", db_transaction)
    return db_transaction
