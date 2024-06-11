from sqlalchemy.orm import Session
from app.db import models
from app.schemas import transaction
from typing import List
from app.db.models import Rule
from app.schemas.rule import RuleCreate, RuleUpdate


def get_rules_(db: Session) -> List[Rule]:
    """
    Retrieve all rules from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[Rule]: A list of all rules in the database.
    """
    return db.query(models.Rule).all()


def create_transaction(
    db: Session, transaction: transaction.TransactionCreate
) -> models.Transaction:
    """
    Create a new transaction in the database.

    Args:
        db (Session): SQLAlchemy database session.
        transaction (TransactionCreate): The data for the new transaction.

    Returns:
        models.Transaction: The created transaction.
    """
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# app/db/crud.py


def create_rule(db: Session, rule: RuleCreate) -> Rule:
    """
    Create a new rule.

    Args:
        db (Session): SQLAlchemy database session.
        rule (RuleCreate): The data for the new rule.

    Returns:
        Rule: The created rule.
    """
    db_rule = Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def create_multiple_rules(db: Session, rules: List[RuleCreate]) -> List[Rule]:
    """
    Create multiple rules in a single operation.

    Args:
        db (Session): SQLAlchemy database session.
        rules (List[RuleCreate]): A list of data for the new rules.

    Returns:
        List[Rule]: A list of the created rules.
    """
    db_rules = [Rule(**rule.dict()) for rule in rules]
    db.bulk_save_objects(db_rules)
    db.commit()
    return db_rules


def get_rule(db: Session, rule_id: int) -> Rule:
    """
    Retrieve a rule by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        rule_id (int): The ID of the rule to retrieve.

    Returns:
        Rule: The rule with the specified ID, or None if not found.
    """
    return db.query(Rule).filter(Rule.id == rule_id).first()


def get_rules(db: Session, skip: int = 0, limit: int = 10) -> List[Rule]:
    """
    Retrieve a list of rules with pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.

    Returns:
        List[Rule]: A list of rules.
    """
    return db.query(Rule).offset(skip).limit(limit).all()


def update_rule(db: Session, rule_id: int, rule: RuleUpdate) -> Rule:
    """
    Update an existing rule.

    Args:
        db (Session): SQLAlchemy database session.
        rule_id (int): The ID of the rule to update.
        rule (RuleUpdate): The new data for the rule.

    Returns:
        Rule: The updated rule, or None if not found.
    """
    db_rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if db_rule:
        for key, value in rule.dict().items():
            setattr(db_rule, key, value)
        db.commit()
        db.refresh(db_rule)
    return db_rule


def delete_rule(db: Session, rule_id: int) -> Rule:
    """
    Delete an existing rule.

    Args:
        db (Session): SQLAlchemy database session.
        rule_id (int): The ID of the rule to delete.

    Returns:
        Rule: The deleted rule, or None if not found.
    """
    db_rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    return db_rule
