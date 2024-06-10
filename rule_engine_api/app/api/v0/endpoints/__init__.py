# app/api/v0/endpoints/__init__.py

from fastapi import APIRouter
from app.api.v0.endpoints import transaction, rules

api_router = APIRouter()
api_router.include_router(
    transaction.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
