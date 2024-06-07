from typing import List

def apply_rules(transaction: dict, rules: List[str]) -> bool:
    for rule in rules:
        try:
            if not eval(rule, {"transaction": transaction}):
                return False
        except Exception as e:
            # Log the exception or handle it as needed
            return False
    return True
