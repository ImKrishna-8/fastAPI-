from fastapi import FastAPI,Depends,HTTPException
from database import sessionLocal,engine
import models
import auth
from pydantic_models import CreateBook,BookResponse
from auth import get_current_user
from sqlalchemy.orm import Session
app = FastAPI()
app.include_router(auth.router)

@app.on_event('startup')
def startup():
    models.Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post('/books',response_model=BookResponse,status_code=201)
def add_book(book:CreateBook,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        db_book = models.Book(title=book.title,author=book.author,price=book.price)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    raise HTTPException(status_code=401,detail='you dont have access')
    

@app.get('/books',response_model=list[BookResponse])
def get_all_books(db:Session=Depends(get_db)):
       return db.query(models.Book).all()

@app.get('/books/{id}')
def get_one(id:int,db:Session=Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == id).first()
    if not db_book:
          raise  HTTPException(status_code=404,detail='Book not found')
    return db_book

@app.put('/books/{id}',response_model=BookResponse)
def update_one(id:int,updated_book:CreateBook,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
     if user : 
        db_book = db.query(models.Book).filter(models.Book.id==id).first()
        if not db_book:
            raise  HTTPException(status_code=404,detail='Book not found')
        db_book.author = updated_book.author # type: ignore
        db_book.price = updated_book.price # type: ignore
        db_book.title = updated_book.title # type: ignore
        db.commit()
        db.refresh(db_book)
        return db_book
     raise HTTPException(status_code=401,detail='you dont have access')

@app.delete('/books/{id}')
def delete_book(id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
     if user:
        db_book = db.query(models.Book).filter(models.Book.id == id).first()
        if not db_book:
            raise HTTPException(status_code=404,detail='Book not found')
        
        db.delete(db_book)
        db.commit()
        return "Book deleted successfully"
     raise HTTPException(status_code=401,detail='You dont have access for it ')