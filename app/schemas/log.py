from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LogCreate(BaseModel):
    completed: bool = True

class LogResponse(BaseModel):
    id: int
    habit_id: int
    date: datetime
    completed: bool

    model_config = ConfigDict(from_attributes = True)
