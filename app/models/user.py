from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    userId: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    subscribed: list = Field(...)
    hoisted: list = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "firstName": "John Doe",
                "lastName": "Doe",
                "email": "jdoe@gmail.com",
                "password": "",
                "userId": "johndoe",
                "subscribed": [],
                "hoisted": []
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
