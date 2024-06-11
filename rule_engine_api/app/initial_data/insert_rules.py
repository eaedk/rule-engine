# app/initial_data/insert_rules.py

import json
from app.db.session import SessionLocal
from app.db.models import Rule


def read_rules_from_json(file_path):
    """
    Read rules from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing rules.

    Returns:
        list: List of rules read from the JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def insert_initial_rules(rules):
    """
    Insert initial rules into the database.

    Args:
        rules (list): List of rules to insert into the database.
    """
    db = SessionLocal()
    try:
        for rule_data in rules:
            existing_rule = (
                db.query(Rule).filter_by(description=rule_data["description"]).first()
            )
            if not existing_rule:
                rule = Rule(**rule_data)
                db.add(rule)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    rules = read_rules_from_json("initial_rules.json")
    insert_initial_rules(rules)
