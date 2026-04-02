from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from models.todo_model import Todo
from db.database import get_db, Base, engine
from dotenv import load_dotenv
import os
load_dotenv()


Base.metadata.create_all(bind=engine)
app = FastAPI()
# schemas
from typing import Any

class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
class CreateTodo(BaseModel):
    title: str
    description: Optional[str]
    status: bool = False
    created_at: Optional[datetime] = None
class ResponseTodo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: bool
    created_at: Optional[datetime] = None
    class Config:
        orm_mode = True
# routes
@app.get("/")
def start():
    return {
        "message":"welcome to todos."
    }
@app.post("/todo", response_model=ResponseTodo)
def create_todo(todo: CreateTodo, db: Session = Depends(get_db)):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        status=todo.status,
        created_at=todo.created_at or datetime.utcnow(),
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todo", response_model=List[ResponseTodo])
def read_all(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.get("/todo/id/{id}", response_model=ResponseTodo)
def read_by_id(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return todo

@app.get("/todo/title/", response_model=List[ResponseTodo])
def read_by_title(title: str, db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.title == title).all()
    if not todos:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return todos

@app.delete("/todo/id/{id}", response_model=ResponseTodo)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    db.delete(todo)
    db.commit()
    return todo

@app.delete("/todo/title/", response_model=List[ResponseTodo])
def delete_by_title(title: str, db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.title == title).all()
    if not todos:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    for t in todos:
        db.delete(t)
    db.commit()
    return todos
