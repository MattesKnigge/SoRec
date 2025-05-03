from pydantic import BaseModel

class SpeedUpdate(BaseModel):
    speed: float
