from typing import Dict, List, Union
from app.db.models import Rule


def apply_rules(
    transaction: Dict[str, str], rules: List[Rule]
) -> Dict[str, Union[bool, str]]:
    """
    Apply rules to the transaction and return the evaluation result.

    Args:
        transaction (dict): Dictionary containing transaction data.
        rules (List[Rule]): List of Rule objects representing rules to be applied.

    Returns:
        dict: Dictionary containing the evaluation result with 'has_succeeded' flag and 'message'.
    """
    fail_messages = []
    for rule in rules:
        try:
            if not eval(rule.rule, {"transaction": transaction}):
                fail_messages.append(rule.description)
        except Exception as e:
            fail_messages.append(f"'{rule.description}' ==> {e}")

    return {
        "has_succeeded": len(fail_messages) == 0,
        "message": "\n".join(fail_messages),
    }
