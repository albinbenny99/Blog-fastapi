from fastapi import FastAPI,Depends,status,Response
from . import schemas
from . import models 
from .database import engine
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from typing import List
from .hashing import Hash


app=FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
  new_blog=models.Blog(title=request.title,body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def  destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'deatil':f"Blog  with id {id} is not available" }
    return blog



@app.post('/user',response_model=schemas.ShowUser)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@app.get('/user/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    