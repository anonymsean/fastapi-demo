from fastapi import FastAPI
from sqlmodel import SQLModel
from router import authors, books, users, auth

app = FastAPI(title="Book API",version="1.1.0")
app.include_router(books.app)
app.include_router(authors.app)
app.include_router(users.app)
app.include_router(auth.app)

from db import engine

def startup():
    SQLModel.metadata.create_all(engine)

app.add_event_handler("startup",startup)

if __name__ == "__main__":
    print("test")
    import uvicorn
    uvicorn.run("book:app", reload=True)
