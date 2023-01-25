from typing import List
from trycourier import Courier
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel, Field
import os
from fastapi.encoders import jsonable_encoder

load_dotenv()

courier_client = Courier(auth_token=os.environ.get('COURIER_SECRET_KEY'))

file = APIRouter(prefix='/files', tags=['files'])


class MessageShare(BaseModel):
    message: str = Field(...)
    emailIds: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "message": "Test Message",
                "emailIds": [],
            }
        }


@file.post('/share', summary="Share a message")
async def share(message: MessageShare):
    message = jsonable_encoder(message)
    for emailId in message['emailIds']:
        courier_client.send_message(
            message={
                "to": {
                    "email": str(emailId),
                },
                "template": "EDX5BR8ZJ3MCEAKCQTCAH5TRF74T",
                "data": {
                    "message": message['message'],
                },
            }
        )
    return "Message sent successfully!"
