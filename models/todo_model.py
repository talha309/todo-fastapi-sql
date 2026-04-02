from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from db.database import Base

class Todo(Base):
    __tablename__ = "todos"
    id = Column (Integer, primary_key=True, autoincrement=True, index=True)
    title = Column (String, nullable=False)
    description = Column (String, nullable=True)
    status = Column (Boolean, default=False)
    created_at = Column (DateTime, default=datetime.utcnow)