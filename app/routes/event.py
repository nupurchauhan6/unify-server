from app.models.event import Event
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
import os
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
load_dotenv()

client = AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.unify

event = APIRouter(prefix='/events', tags=['events'])


@event.post("/", response_description="Add new event", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(event: Event = Body(...)):

    event = jsonable_encoder(event)
    new_event = await db["events"].insert_one(event)

    created_event = await db["events"].find_one({"_id": new_event.inserted_id})
    return created_event


@event.get("/", response_description="List all events", response_model=List[Event])
async def list_events():
    return await db["events"].find().to_list(1000)


@event.get("/{userId}", response_description="Get a events by userId", response_model=List[Event])
async def list_events_by_userid(userId: str):
    return await db["events"].find({"userId": userId}).to_list(1000)
