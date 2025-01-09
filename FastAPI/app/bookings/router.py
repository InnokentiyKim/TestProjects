from fastapi import APIRouter
from sqlalchemy import select
from app.bookings.service import BookingService
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.bookings.schemas import BookingSchema


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings() -> list[BookingSchema]:
    result = await BookingService.find_all()
    return result
        
