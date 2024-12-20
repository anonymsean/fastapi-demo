
from sqlmodel import SQLModel, Field, Relationship

class BooksWriter(SQLModel):
    title:str
    author_name:str
    year:int
    book_type:str
    price:float
    class Config:
        json_schema_extra={
            "example":{
                "title":"Python Crash Course",
                "author_name":"Eric Matthes",
                "year":2019,
                "book_type":"Fiction",
                "price":19.99,
                "Author_id":1
            }
        }

class Book(BooksWriter,table=True):
    book_id:int|None=Field(default=None,primary_key=True)
    author_id:int=Field(foreign_key="author.author_id")
    author: "Author" = Relationship(back_populates="books")

class AuthorWriter(SQLModel):
    name:str
    nationality:str
    class Config:
        json_schema_extra={
            "example":{
                "name":"Eric Matthes",
                "nationality":"American"
            }
        }

class AuthorReader(AuthorWriter):
    author_id:int
    books:list[Book]=[]

class Author(AuthorWriter,table=True):
    author_id:int|None=Field(default=None,primary_key=True)
    books:list[Book]=Relationship(back_populates="author")

class UserWriter(SQLModel):
    user_name:str
    user_password:str

class User(SQLModel,table=True):
    user_id:int|None=Field(default=None,primary_key=True)
    user_name:str=Field(unique=True,include=True)
    password_hash:str

class UserReader(SQLModel):
    user_id:int
    user_name:str

if __name__ =="__main__":
    book=Book(book_id=1,title="Python Crash Course",author_name="Eric Matthes",year=2019,author_id=1,book_type="Fiction",price=19.99)
    print(book.model_dump_json())