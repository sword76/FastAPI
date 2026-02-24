from fastapi import APIRouter, HTTPException

from pwdlib import PasswordHash

from src.repositories.user import UsersRepository
from src.db import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags =["Авторизация и аутентификация"])

pwd_context = PasswordHash.recommended()

@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    # Hashing password
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, first_name=data.first_name, last_name=data.last_name)
    async with async_session_maker() as session:
        repo = UsersRepository(session)
        existing = await repo.get_one_or_none(email=data.email)
        if existing:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        await repo.add_one(new_user_data)
        await session.commit()

    return {"status": "OK"}
