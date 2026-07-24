from fastapi import FastAPI
from .routers import pdf
from database.database import engine,Base
from database import models
app=FastAPI()

Base.metadata.create_all(engine)

app.include_router(pdf.router)
