from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import UserAuthSchema



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
async def register_user(user_data: UserAuthSchema):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True, secure=True)
    return access_token


@router.post("/logout")
async def login_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"detail": "Logged out successfully"}

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user



