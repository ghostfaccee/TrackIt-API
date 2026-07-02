from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class StatsResponse(BaseModel):
    total_days: int
    streak: int
    last_logged: Optional[datetime] = None

    model_config = ConfigDict(from_attributes = True)
