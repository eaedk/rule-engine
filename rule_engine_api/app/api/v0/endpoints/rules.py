# app/api/v0/endpoints/rules.py

from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import crud
from app.schemas.rule import Rule, RuleCreate, RuleUpdate

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
    if isinstance(rules, list):
        return crud.create_multiple_rules(db, rules)
    else:
        return crud.create_rule(db, rules)


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
    db_rule = crud.get_rule(db, rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule


@router.get("/", response_model=List[Rule])
def read_rules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rules = crud.get_rules(db, skip=skip, limit=limit)
    return rules


@router.put("/{rule_id}", response_model=Rule)
def update_existing_rule(rule_id: int, rule: RuleUpdate, db: Session = Depends(get_db)):
    db_rule = crud.update_rule(db, rule_id, rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule


@router.delete("/{rule_id}", response_model=Rule)
def delete_existing_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = crud.delete_rule(db, rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule
