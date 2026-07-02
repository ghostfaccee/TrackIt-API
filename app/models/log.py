from sqlalchemy import Integer, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key = True, index = True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable = False)
    date = Column(DateTime(timezone = True), server_default = func.now())
    completed = Column(Boolean, default = True)

    habit = relationship('Habit', back_populates = 'logs')
