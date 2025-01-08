from fastapi import APIRouter
from sqlalchemy import select
from app.bookings.service import BookingService
from app.database import async_session_maker
from app.bookings.models import Bookings


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings():
    result = await BookingService.find_by_id(1)
    return result
        
