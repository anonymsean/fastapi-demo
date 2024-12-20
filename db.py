from sqlmodel import create_engine,Session

engine=create_engine("sqlite:///books.db",echo=True,connect_args={"check_same_thread":False})
def get_session():
    with Session(engine) as session:
        yield session