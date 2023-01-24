from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Event(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    userId: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    additionalDetails: str = Field(...)
    startTime: datetime = Field(...)
    endTime: datetime = Field(...)
    meetingLink: str = Field(...)
    meetingDetails: str = Field(...)
    registeredUsers: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "userId": "johndoe",
                "title": "Intro To Python",
                "description": "Beginner level course",
                "additionalDetails": "",
                "startTime": datetime.now(),
                "endTime": datetime.now(),
                "meetingLink": "",
                "meetingDetails": "",
                "registeredUsers": []
            }
        }
