
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.db.session import engine
from app.router import route
from app.db.base import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="True Lost API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="static")
app.include_router(route.router, prefix="/api/v1")