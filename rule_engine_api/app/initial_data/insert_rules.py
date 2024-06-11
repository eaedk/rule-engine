# app/initial_data/insert_rules.py

from app.db.session import SessionLocal
from app.db.models import Rule

# Predefined rules to be inserted into the database
rules = [
    {
        "description": "Transaction amount must be less than 1,500,000",
        "rule": "transaction['amount'] < 1500000",
    },
    {
        "description": "Email address must be from Côte d'Ivoire (ends with .ci domain)",
        "rule": "transaction['email_address'].lower().endswith('.ci')",
    },
]


def insert_initial_rules():
    """
    Inserts predefined rules into the database if they do not already exist.
    """
    db = SessionLocal()
    try:
        for rule_data in rules:
            # Check if the rule already exists
            existing_rule = (
                db.query(Rule).filter_by(description=rule_data["description"]).first()
            )
            if not existing_rule:
                rule = Rule(**rule_data)
                db.add(rule)
        db.commit()
    finally:
        db.close()
