from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.todo_model import User
from utils.auth_util import create_access_token, hash_password, verify_api_key, verify_password
from schemas.auth_schemas import LoginUser, UserCreate




user_router = APIRouter()




@user_router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_hash_password = hash_password(user.password)
        print("User Plain Password: ", user.password )
        print("User Hash Password: ",user_hash_password)
        valid_user = User(username=user.username, email=user.email,
                           password=user_hash_password)
        db.add(valid_user)
        db.commit()
        db.refresh(valid_user)

        token = create_access_token(data={"email": valid_user.email, "username": valid_user.username, "user_id": valid_user.id})
        return {
            "data": {
                "username": valid_user.username,
                "email": valid_user.email,
                "token": token
                },
            "message": "User registered and login successfully",
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
    


@user_router.post("/login", dependencies=[Depends(verify_api_key)])
def login_user(user:LoginUser, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        is_valid_password = verify_password(user.password, db_user.password)
        if is_valid_password == False:
            raise HTTPException(status_code=401, detail="Invalid password")
        token = create_access_token(data={"email": db_user.email, "username": db_user.username, "user_id": db_user.id})
        user_data = {
            "username": db_user.username,
            "email": db_user.email,
            "token": token
        }

        return {
            "data": user_data,
            "message": "User logged in successfully",
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