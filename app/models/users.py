from app.core.database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(30), unique = True, index = True, nullable = False)
    email = Column(String(255), unique = True, nullable = True)
    hashed_pass = Column(String(255), nullable = False)

    habits = relationship('Habit', back_populates = 'user', cascade = 'all, delete-orphan')