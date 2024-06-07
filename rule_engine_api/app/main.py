from fastapi import FastAPI
from app.api.v0 import endpoints
from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(endpoints.router, prefix="/v0")
