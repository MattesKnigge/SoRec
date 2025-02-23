# app/models.py
from pydantic import BaseModel, validator

class SpeedInput(BaseModel):
    speed: float

    @validator('speed')
    def validate_speed(cls, value):
        if value > 100:
            raise ValueError("Speeds above 100% are not allowed!")
        if value < 0:
            raise ValueError("Speeds below 0% are not allowed!")
        return value

class Operation(BaseModel):
    path: str
    value: float

class PatchRequest(BaseModel):
    operations: list[Operation]
