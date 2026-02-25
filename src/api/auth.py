from fastapi import APIRouter, HTTPException, Response, Request

from src.repositories.user import UsersRepository
from src.db import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags =["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    # Hashing password
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, first_name=data.first_name, last_name=data.last_name)
    async with async_session_maker() as session:
        repo = UsersRepository(session)
        existing = await repo.get_one_or_none(email=data.email)
        if existing:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        await repo.add_one(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def register_user(
    data: UserRequestAdd,
    responce: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="User with this email doesn't exist")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Wrong password")   
        access_token = AuthService().create_access_token({"user_id": user.id})
        responce.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(
    request: Request,      
):
    async with async_session_maker() as session:
        token = request.cookies.get("access_token", None)
        print(type(token))
        return token
        