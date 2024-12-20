
from db import get_session
from fastapi import Depends, HTTPException
from schema import AuthorWriter, Author, Book, BooksWriter, AuthorReader
from sqlmodel import Session,select
from fastapi import APIRouter
app=APIRouter()
@app.get("/api/authors")
def get_authors(session:Session=Depends(get_session)) -> list[Author]:
    return [author for author in(session.exec(select(Author)).all())]

@app.post("/api/authors")
def create_author(author:AuthorWriter,session:Session=Depends(get_session)) -> Author:
    new_author=Author.model_validate(author)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author

@app.get("/api/authors/{author_id}")
def get_author(author_id:int,session:Session=Depends(get_session)) -> AuthorReader:
    author=session.get(Author,author_id)
    if author:
        return Author.model_validate(author)
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/api/authors/{author_id}/books")
def create_book(author_id:int,book:BooksWriter,session:Session=Depends(get_session)) -> Book:
    author=session.get(Author,author_id)
    if author:
        new_book=Book.model_validate(book,update={"author_id":author.author_id})
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book
    raise HTTPException(status_code=404, detail="Author not found")