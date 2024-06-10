# app/api/v0/endpoints/rules.py

from typing import List
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


@router.post("/", response_model=Rule)
def create_new_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db, rule)


@router.get("/{rule_id}", response_model=Rule)
def read_rule(rule_id: int, db: Session = Depends(get_db)):
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
