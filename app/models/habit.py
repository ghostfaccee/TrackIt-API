from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False)
    description = Column(String(100), nullable = True)
    created_at = Column(DateTime(timezone = True), server_default = func.now())

    logs = relationship('Log', back_populates = 'habit', cascade = 'all, delete-orphan')

