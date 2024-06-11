from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import crud
from app.schemas.rule import Rule, RuleCreate, RuleUpdate
import logging

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


@router.post("/", response_model=Union[Rule, List[Rule]])
def create_new_rule(
    rules: Union[RuleCreate, List[RuleCreate]], db: Session = Depends(get_db)
):
    """
    Create a new rule or multiple rules.

    Args:
        rules (Union[RuleCreate, List[RuleCreate]]): A single rule or a list of rules to create.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        Union[Rule, List[Rule]]: The created rule(s).
    """
    logger.info("Creating new rule(s)")
    if isinstance(rules, list):
        created_rules = crud.create_multiple_rules(db, rules)
        logger.info("Multiple rules created successfully")
        return created_rules
    else:
        created_rule = crud.create_rule(db, rules)
        logger.info("Rule created successfully")
        return created_rule


@router.get("/{rule_id}", response_model=Rule)
def read_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Read a rule by its ID.

    Args:
        rule_id (int): The ID of the rule to read.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        Rule: The rule with the specified ID.
    """
    logger.info("Reading rule with ID: %s", rule_id)
    db_rule = crud.get_rule(db, rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule


@router.get("/", response_model=List[Rule])
def read_rules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Read multiple rules with pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        List[Rule]: List of rules.
    """
    logger.info("Reading rules with skip=%s and limit=%s", skip, limit)
    rules = crud.get_rules(db, skip=skip, limit=limit)
    return rules

@router.put("/{rule_id}", response_model=Rule)
def update_existing_rule(rule_id: int, rule: RuleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing rule by its ID.

    Args:
        rule_id (int): The ID of the rule to update.
        rule (RuleUpdate): The rule data to update.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        Rule: The updated rule.
    """
    logger.info("Updating rule with ID: %s", rule_id)
    db_rule = crud.update_rule(db, rule_id, rule)
    if db_rule is None:
        logger.error("Rule not found with ID: %s", rule_id)
        raise HTTPException(status_code=404, detail="Rule not found")
    logger.info("Rule updated successfully")
    return db_rule

@router.delete("/{rule_id}", response_model=Rule)
def delete_existing_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing rule by its ID.

    Args:
        rule_id (int): The ID of the rule to delete.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        Rule: The deleted rule.
    """
    logger.info("Deleting rule with ID: %s", rule_id)
    db_rule = crud.delete_rule(db, rule_id)
    if db_rule is None:
        logger.error("Rule not found with ID: %s", rule_id)
        raise HTTPException(status_code=404, detail="Rule not found")
    logger.info("Rule deleted successfully")
    return db_rule
