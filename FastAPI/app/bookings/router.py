from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings() -> list[BookingSchema]:
    return await BookingDAO.find_all()


@router.get("/{booking_id}")
def get_booking(booking_id: int):
    pass
