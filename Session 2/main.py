from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session,select,update
from database import engine
from models import Book,BookCreate

app = FastAPI()

def get_db():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        return JSONResponse({"msg":"something here"},status_code=500) 


@app.post('/books')
def add_book(book:BookCreate,db:Session=Depends(get_db)):
    book = Book(**book.dict())
    db.add(book)
    print("not reaching here")
    db.commit()
    db.refresh(book)
    return JSONResponse({"msg":"created"},status_code=201)    
    
@app.get('/books',response_model=list[Book])
def get_books(db:Session=Depends(get_db)): 
    return db.exec(select(Book)).all()

@app.put('/books/{id}',response_model=Book)
def update_book(id:int,book:BookCreate,db:Session=Depends(get_db)):
    db_book=db.get(Book,id)
    
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
    db_book = db.get(Book,id)

    if not db_book:
        return JSONResponse({"error":"Book not found"})

    db.delete(db_book)
    db.commit()
    return JSONResponse({"status":"Deleted"},status_code=203)

@app.get('/books/{id}')
def get_detail_book(id:int,db:Session=Depends(get_db)):
    db_book = db.get(Book,id)

    if not db_book:
        return JSONResponse({"error":"Book not found"})

    return db_book