from db.database import get_db
from fastapi import APIRouter,Depends,HTTPException
from models.todo_model import Todo
from sqlalchemy.orm import Session
from utils.auth_util import verify_token
from schemas.todo_schemas import TodoCreate, UpdateTodo

todo_router = APIRouter()

@todo_router.post("/create")
def create_todo(todo: TodoCreate, user=Depends(verify_token), db: Session  = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        db_todo = Todo(title=todo.title, description=todo.description,
                        status=todo.status, user_id=user_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "data": db_todo,
            "message": "Todo created successfully",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }



@todo_router.get("/get-all")
def get_todos(user=Depends(verify_token),db: Session = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        todos = db.query(Todo).filter(Todo.user_id == user_id).all()
        return {
            "data": todos,
            "message": "Todos fetched successfully",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }

# Get a Todo by ID


@todo_router.get("/get/{todo_id}")
def get_todo(todo_id: int, user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {
            "data": todo,
            "message": "Todo fetched successfully",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }

# Update a Todo


@todo_router.put("/{todo_id}")
def update_todo(todo_id: int, todo_update: UpdateTodo, user = Depends(verify_token), db: Session = Depends(get_db)):
    try: 
        user_id = user.get("user_id")
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if todo_update.title is not None:
            todo.title = todo_update.title
        if todo_update.description is not None:
            todo.description = todo_update.description
        if todo_update.status is not None:
            todo.status = todo_update.status
        db.commit()
        db.refresh(todo)
        return {
            "data": todo,
            "message": "Todo updated successfully",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }

# Delete a Todo


@todo_router.delete("/{todo_id}")
def delete_todo(todo_id: int, user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.delete(todo)
        db.commit()
        return {
            "message": "Todo deleted",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }