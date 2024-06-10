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
    fail_message = ""
    for rule in rules:
        try:
            if not eval(rule.rule, {"transaction": transaction}):
                fail_message += f"\n{rule.description}"
        except Exception as e:
            fail_message += f"\n'{rule.description}' ==> {e}"

    return {
        "has_succeeded": not fail_message,
        "message": fail_message,
    }
