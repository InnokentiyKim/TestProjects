from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingDAO.find_all(id=user.id)


@router.get("/{booking_id}")
def get_booking(booking_id: int):
    pass
