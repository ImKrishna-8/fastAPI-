from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
import models
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine,sessionLocal
from pydantic_models import bookRequest,bookResponse
import auth
from auth import get_current_user
app = FastAPI(title="KRISHNA DEBUG TEST")
app.include_router(auth.router)
print(app.routes)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

        

@app.get('/books',response_model=list[bookResponse])
def all_books( db:Session=Depends(get_db)):
    return db.execute(select(models.Book)).all()

@app.post('/books')
def add_book(book:bookRequest,db:Session=Depends(get_db),user: dict=Depends(get_current_user)):
    if user:
        db_book = models.Book(
            title=book.title,
            author=book.author,
            price=book.price
        )

        db.add(db_book)
        db.commit()
        return "Book added Succesfully"
    
@app.put('/books/{id}')
def update_book(id:int,book:bookRequest,db:Session=Depends(get_db),user: dict=Depends(get_current_user)):
    db_book=db.get(models.Book,id)
    
    if not db_book:
        return JSONResponse({"error":"Book not found"})
    
    update_book = book.dict(exclude_unset=True)

    for key,value in update_book.items():
        setattr(db_book,key,value)

 
    db.commit()
    db.refresh(db_book)
    return JSONResponse({"Success":"Updated"})

@app.delete('/books/{id}')
def delete_book(id:int,db:Session=Depends(get_db)):
    db_book = db.get(models.Book,id)

    if not db_book:
        return JSONResponse({"error":"Book not found"})

    db.delete(db_book)
    db.commit()
    return JSONResponse({"status":"Deleted"},status_code=203)