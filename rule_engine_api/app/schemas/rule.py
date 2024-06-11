# app/schemas/rule.py

from pydantic import BaseModel


class RuleBase(BaseModel):
    """
    Base model for rules.

    Attributes:
        description (str): A brief description of the rule.
        rule (str): The rule logic as a string.
    """

    description: str
    rule: str


class RuleCreate(RuleBase):
    """
    Model for creating a new rule.

    Inherits from:
        RuleBase: The base model for rules.
    """

    pass


class RuleUpdate(RuleBase):
    """
    Model for updating an existing rule.

    Inherits from:
        RuleBase: The base model for rules.
    """

    pass


class Rule(RuleBase):
    """
    Model representing a rule with an ID.

    Attributes:
        id (int): The unique identifier for the rule.

    Config:
        from_attributes (bool): Allow population from ORM attributes.
    """

    id: int

    class Config:
        from_attributes = True
