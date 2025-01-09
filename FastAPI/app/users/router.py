from fastapi import APIRouter, HTTPException
from app.users.service import UserService
from app.users.schemas import UserRegisterSchema


router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/register")
async def register_user(user_data: UserRegisterSchema):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = ge