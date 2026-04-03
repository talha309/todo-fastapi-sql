from sqlalchemy import Column, String, Integer, Boolean,ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column (Integer, primary_key=True, autoincrement=True, index=True)
    username = Column (String, unique=True, nullable=False)
    email = Column (String, unique=True, nullable=False)
    password = Column (String, nullable=False)


class Todo(Base):
    __tablename__ = "todos"
    id = Column (Integer, primary_key=True, autoincrement=True, index=True)
    title = Column (String, nullable=False)
    description = Column (String, nullable=True)
    status = Column (Boolean, default=False)
    created_at = Column (DateTime, default=datetime.utcnow)
    user_id = Column (Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

