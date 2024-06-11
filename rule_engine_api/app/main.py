# app/main.py

from fastapi import FastAPI
from app.api.v0.endpoints import api_router
from app.db.session import engine
from app.db.models import Base
from app.initial_data.insert_rules import insert_initial_rules

# Create all database tables based on the models defined
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include the API router with a prefix for versioning
app.include_router(api_router, prefix="/v0")

# Insert initial rules into the database
insert_initial_rules()
