from pydantic import BaseModel

class DisasterData(BaseModel):

    location: str
    disaster_type: str

    rainfall: float = 0
    temperature: float = 0

    water_level: float = 0

    emergency_calls: int = 0

    social_reports: int = 0

    timestamp: str