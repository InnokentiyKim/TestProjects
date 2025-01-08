from fastapi import FastAPI, Query
import uvicorn
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings


app = FastAPI()
app.include_router(router_bookings)

@app.get("/hotels")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    stars: Optional[int] = Query(None, ge=1, le=5),
    has_spa: Optional[bool] = None
):
    return date_from, date_to


class BookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    

@app.post("/bookings")
def add_booking(booking: BookingSchema):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", )