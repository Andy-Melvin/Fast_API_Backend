from fastapi import APIRouter, Depends, HTTPException, Form
from passlib.context import CryptContext
from sqlalchemy.sql import select
from app.database import database
from app.models import users

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.post("/register/")
async def register(username: str = Form(...), password: str = Form(...), phone_number: str = Form(...)):
    query = select(users).where(users.c.username == username)
    existing_user = await database.fetch_one(query)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = pwd_context.hash(password)
    query = users.insert().values(username=username, password=hashed_password, phone_number=phone_number)
    await database.execute(query)
    return {"message": "User registered successfully"}


@auth_router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    query = select(users).where(users.c.username == username)
    user = await database.fetch_one(query)

    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": f"Welcome back, {username}!"}