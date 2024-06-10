# app/schemas/rule.py

from pydantic import BaseModel


class RuleBase(BaseModel):
    description: str
    rule: str


class RuleCreate(RuleBase):
    pass


class RuleUpdate(RuleBase):
    pass


class Rule(RuleBase):
    id: int

    class Config:
        from_attributes = True
