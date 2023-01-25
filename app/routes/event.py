from trycourier import Courier
from app.models.event import Event
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
import os
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
load_dotenv()

courier_client = Courier(auth_token=os.environ.get('COURIER_SECRET_KEY'))

client = AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.unify

event = APIRouter(prefix='/events', tags=['events'])


@event.post("/", response_description="Add new event", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(event: Event = Body(...)):

    event = jsonable_encoder(event)
    new_event = await db["events"].insert_one(event)

    created_event = await db["events"].find_one({"_id": new_event.inserted_id})
    fetched_user = await db["users"].find_one({"_id": created_event['userId']})

    courier_client.send_message(
        message={
            "to": {
                "email": fetched_user['email'],
            },
            "template": "C97B9RYGTJMQT8QAMK2Z7781EZF4",
            "data": {
                "firstName": fetched_user['firstName'],
                "eventName": created_event['title'],
                "meetingLink": created_event['meetingLink'],
                "startTime": created_event['startTime'],
                "endTime": created_event['endTime'],
                "meetingDetails": created_event['meetingDetails'],
            },
        }
    )

    return created_event


@event.get("/", response_description="List all events", response_model=List[Event])
async def list_events():
    return await db["events"].find().to_list(1000)


@event.get("/{userId}", response_description="Get a events by userId", response_model=List[Event])
async def list_events_by_userid(userId: str):
    return await db["events"].find({"userId": userId}).to_list(1000)


@event.get("/organized/{id}", response_model=List[Event])
async def list_organized_events(id: str):
    user = await db["users"].find_one({"_id": id})
    organizedEvents = user['organized']

    events = []
    for event_id in organizedEvents:
        events.append(await db["events"].find_one({"_id": event_id}))
    return events


@event.get("/subscribed/{id}", response_model=List[Event])
async def list_subscribed_events(id: str):
    user = await db["users"].find_one({"_id": id})
    subscribedEvents = user['subscribed']
    
    events = []
    for event_id in subscribedEvents:
        events.append(await db["events"].find_one({"_id": event_id}))
    return events
