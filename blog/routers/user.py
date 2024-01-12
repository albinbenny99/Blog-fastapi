from fastapi import APIRouter
from ..hashing import Hash
from .. import schemas,database,models
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,Response
from ..repository import user


router=APIRouter(
    prefix="/user",
    
    tags=['User']
)

@router.post('/',response_model=schemas.ShowUser)
def create_user(request:schemas.User,db:Session=Depends(database.get_db)):
    return user.create(request,db)
    
@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db:Session=Depends(database.get_db)):
    return user.show(id,db)