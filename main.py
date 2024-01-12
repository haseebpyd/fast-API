
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
