from fastapi import HTTPException, status

class HabitNotFoundError(HTTPException):
    def __init__(self, habit_id: int):
        return super().__init__(status_code = status.HTTP_404_NOT_FOUND, detail = f'Habit with id {habit_id} not found')

class HabitNameEmptyError(HTTPException):
    def __init__(self):
        return super().__init__(status_code = status.HTTP_400_BAD_REQUEST, detail = f'Habit name cannot be empty')

class LogNotFoundError(HTTPException):
    def __init__(self, log_id: int):
        return super().__init__(status_code = status.HTTP_404_NOT_FOUND, detail = f'Log with id {log_id} not found')

