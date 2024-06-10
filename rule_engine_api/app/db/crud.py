from sqlalchemy.orm import Session
from app.db import models
from app.schemas import transaction

from app.db.models import Rule
from app.schemas.rule import RuleCreate, RuleUpdate


def get_rules_(db: Session):
    return db.query(models.Rule).all()


def create_transaction(db: Session, transaction: transaction.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# app/db/crud.py


def create_rule(db: Session, rule: RuleCreate):
    db_rule = Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def get_rule(db: Session, rule_id: int):
    return db.query(Rule).filter(Rule.id == rule_id).first()


def get_rules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rule).offset(skip).limit(limit).all()


def update_rule(db: Session, rule_id: int, rule: RuleUpdate):
    db_rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if db_rule:
        for key, value in rule.dict().items():
            setattr(db_rule, key, value)
        db.commit()
        db.refresh(db_rule)
    return db_rule


def delete_rule(db: Session, rule_id: int):
    db_rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    return db_rule
