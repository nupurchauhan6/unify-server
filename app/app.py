from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.event import event
from app.routes.user import user
from app.routes.file import file

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://unify-amber.vercel.app"
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
app.include_router(file)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your website!"}
