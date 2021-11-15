from fastapi import FastAPI
from sqlalchemy import engine
#from sqlalchemy.orm import Session
from . import models
from .database import engine
from .db import init_blacklist_file
if __name__ == '__main__':
    init_blacklist_file()
from .routers import user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user.router)
