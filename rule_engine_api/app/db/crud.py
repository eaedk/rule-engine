from sqlalchemy.orm import Session
from app.db import models
from app.schemas import transaction


def get_rules(db: Session):
    return db.query(models.Rule).all()


def create_transaction(db: Session, transaction: transaction.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
