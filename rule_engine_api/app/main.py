# app/main.py

import os
from fastapi import FastAPI
from app.api.v0.endpoints import api_router
from app.db.session import engine
from app.db.models import Base
from app.initial_data.insert_rules import insert_initial_rules, read_rules_from_json

# Create all database tables based on the models defined
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include the API router with a prefix for versioning
app.include_router(api_router, prefix="/v0")

# Define the path to the JSON file containing initial rules
initial_rules_file = os.path.join(
    os.path.dirname(__file__), "initial_data", "initial_rules.json"
)

# Insert initial rules into the database
rules = read_rules_from_json(initial_rules_file)
insert_initial_rules(rules)
