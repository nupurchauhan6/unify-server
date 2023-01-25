from trycourier import Courier
from dotenv import load_dotenv
from app.models.user import User, TokenSchema
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.password import get_hashed_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

courier_client = Courier(auth_token=os.environ.get('COURIER_SECRET_KEY'))

client = AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.unify

user = APIRouter(prefix='/users', tags=['users'])


@user.post('/signup', summary="Create new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    user = jsonable_encoder(user)
    user['password'] = get_hashed_password(user['password'])

    fetched_user = await db["users"].find_one({"email": user['email']})
    if fetched_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist!"
        )

    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    courier_client.send_message(
        message={
            "to": {
                "email": created_user['email'],
            },
            "template": "PWXHN2Q7A7MDVTG660A92D42SSH7",
            "data": {
            },
        }
    )
    return created_user


@user.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await db["users"].find_one({"email": form_data.username})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password."
        )

    hashed_pass = user['password']

    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be verified."
        )

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }
