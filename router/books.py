from fastapi import HTTPException
from fastapi import Depends

from schema import BooksWriter, Book, User
from sqlmodel import Session,select
from db import get_session
from fastapi import APIRouter
from router.auth import get_current_user
app = APIRouter()
@app.get("/api/books")
def get_books(book_id:int|None=None,title:str|None=None,
              session:Session=Depends(get_session),
              get_user:User=Depends(get_current_user)) -> list[Book]:
    query=select(Book)
    if book_id:
        query=query.where(Book.book_id==book_id)
    if title:
        query=query.where(Book.title==title)
    return [book for book in session.exec(query).all()]

@app.get("/api/books/{book_id}",response_model=Book,status_code=201)
def get_book(book_id:int,session:Session=Depends(get_session),
             get_user:User=Depends(get_current_user)):
    book=session.get(Book,book_id)
    if book:
        return Book.model_validate(book)
    raise HTTPException(status_code=404, detail="Book not found")
@app.post("/api/books")
def create_book(book:BooksWriter,session:Session=Depends(get_session),
                get_user:User=Depends(get_current_user)) -> Book:
    new_book=Book(title=book.title,
                  author_name=book.author_name,
                  year=book.year,
                  book_type=book.book_type,
                  price=book.price,
                  author_id=1)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@app.delete("/api/books/{book_id}")
def delete_book(book_id:int,session:Session=Depends(get_session)) -> str:
    match=session.get(Book,book_id)
    if not match:
        raise HTTPException(status_code=404, detail="Book_id not found")
    session.delete(match)
    session.commit()
    return "delete success"

@app.put("/api/books/{book_id}")
def update_book(book_id:int,book:BooksWriter,session:Session=Depends(get_session)) -> Book:
    match=session.get(Book,book_id)
    if match:
        match.title=book.title
        match.author_name=book.author_name
        match.book_type=book.book_type
        match.year=book.year
        match.price=book.price
        session.commit()
        session.refresh(match)
        return Book.model_validate(match)
    else:
        raise HTTPException(status_code=404, detail="Book_id not found")