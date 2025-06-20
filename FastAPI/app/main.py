from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)


class HotelResponseSchema(BaseModel):
    address: str
    name: str
    stars: int

@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None,
) -> list[HotelResponseSchema]:
    hotels = [
        {
            "address": "Gagarin st. 1, Altai",
            "name": "Super hotel",
            "stars": 5
        },
    ]
    return hotels

class BookingPostSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date

@app.post("/bookings")
def add_booking(booking: BookingPostSchema):
    pass
