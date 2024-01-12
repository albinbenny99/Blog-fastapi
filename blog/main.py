from fastapi import FastAPI,Depends,status,Response
from . import schemas
from . import models 
from .database import engine,get_db
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from typing import List
from .hashing import Hash
from .routers import blog,user,authentication

app=FastAPI(
  
)
models.Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)






