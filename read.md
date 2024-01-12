# Run the FastAPI application using uvicorn main:app --reload and deploy.


# Run the Streamlit client using streamlit run streamlit_client.py.


# Run the Python console client using python python_console_client.py.



# Firsly Create a Envirment and activate 
- conda create --name munnahero python=3.12
- conda env list
- conda activate mmunnahero
- python --version

# The FastAPI framework: 
- pip install fastapi

# The Uvicorn web server: 
- pip install uvicorn

# The Pydantic Setting: 
- pip install pydantic pydantic-settings

# The sqlalchemy setup: 
- pip install sqlalchemy 

# The sqlalchemy setup: 
- psycopg2-binary

# The HTTPie text web clien: 
- pip install httpie

# The multidict 
- pip install multidict

# The Requests synchronous web client package
- pip install requests




# The requirements: 
- pip install -r requirements.txt

above dependencies may isntall and also install in requirements 


### 1. Set up the PostgreSQL Database and SQLAlchemy Models
# database.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://Shafiqmuhammad:Txe6XCp4FIQc@ep-ancient-wildflower-403825.ap-southeast-1.aws.neon.tech/fastapi?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

### 2. Create FastAPI CRUD Endpoints
# main.py


from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Todo
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todo).all()
        return todos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating todo: {str(e)}")
    
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo_create: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo = Todo(**todo_create.dict())
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return TodoResponse(**todo.__dict__)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating todo: {str(e)}")

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    print(db.query(Todo))
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    try:
        db.query(Todo).filter(Todo.id == todo_id).update(updated_todo.dict())
        db.commit()
        return TodoResponse(**db_todo.__dict__)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating todo: {str(e)}")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        db.delete(db_todo)
        db.commit()
        return {"message": "Todo deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting todo: {str(e)}")


### 3. Implement Streamlit Client
# streamlit_client.py



### 4. Python Console Client
# python_console_client.py



### 5. TypeScript Node.js Console Client
# nodejs_console_client.ts



### 6. Unit Tests using Pytest
Create tests for the FastAPI endpoints and their functionality.
# test_api.py




 