from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.event import event
from app.routes.user import user

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(event)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your website!"}
