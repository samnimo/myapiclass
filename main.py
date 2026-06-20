from fastapi import FastAPI,Depends,HTTPException,status
from sqlmodel import SQLModel,Session,Field,select,create_engine
from typing  import Annotated
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None
    
    

class Register(SQLModel,table=True):

    StudentID: str = Field(index=True, primary_key=True)
    name: str = Field()
    Age : int = Field()
    Contact : str | None = Field(default = None)
    Email : str | None = Field(default = None)
    Fees : int | None = Field(default = None)
    Location : str | None = Field(default = None)

sqlite_filename = "student.db"
sqlite_db_url = f"sqlite:///{sqlite_filename}"

connect_arg =  {"check_same_thread": False}
# connect our database to the app 
engine =create_engine(sqlite_db_url, connect_args=connect_arg)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db():
     return SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def main():
    create_db()

@app.get("/")
def main():
    return "home page"

@app.post("/register")
def create_post(student:Register,session:SessionDep):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@app.get("/students")
def get_students(session: SessionDep):
    statement = select(Register)
    results = session.exec(statement).all()
    return results
