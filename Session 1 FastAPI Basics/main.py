from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id:int
    title:str
    author:str
    price:int

class BookUpdate(BaseModel):
    title:str
    author:str
    price:int

books = []

@app.get('/books')
def get_books(author:str | None = None):
    if author is None:
        return books
    result = [book for book in books if book.author == author]
    
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@app.post('/books')
def add_book(book:Book):
    print(type(book))
    books.append(book)
    return "Book added Succesfully"

@app.put('/books/{id}')
def update_book(id:int,book:BookUpdate):
    result = next((book for book in books if book.id == id),None)

    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    result.author = book.author
    result.title = book.title
    result.price = book.price

    return result