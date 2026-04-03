from fastapi import FastAPI
from routes.auth_routes import user_router
from routes.todo_routes import todo_router

app = FastAPI()

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
def root(): 
    return {"message": "Welcome to the Todo API!"}

