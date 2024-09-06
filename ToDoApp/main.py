from fastapi import FastAPI
import models
from database import engine
from routers import flowers, order

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(flowers.router)

