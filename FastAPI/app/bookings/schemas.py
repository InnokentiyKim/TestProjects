from datetime import date

from pydantic import BaseModel


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int

    class Config:
        from_attributes = True