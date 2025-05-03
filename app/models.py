from pydantic import BaseModel, condecimal

class SpeedUpdate(BaseModel):
    speed: condecimal(ge=0, le=100)
    
