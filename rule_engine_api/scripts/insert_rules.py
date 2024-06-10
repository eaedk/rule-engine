# scripts/insert_rules.py

from app.db.session import SessionLocal, engine
from app.db.models import Rule, Base


# from db.session import SessionLocal, engine
# from db.models import Rule, Base

Base.metadata.create_all(bind=engine)

rules = [
    {
        "description": "Amount less than 1,500,000",
        "rule": "transaction['amount'] < 1500000",
    },
    {
        "description": "Email address ends with .ci",
        "rule": "transaction['email_address'].endswith('.ci')",
    },
]

db = SessionLocal()
for rule_data in rules:
    rule = Rule(**rule_data)
    db.add(rule)
db.commit()
db.close()
