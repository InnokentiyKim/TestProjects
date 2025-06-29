from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all_hotel_rooms(cls, hotel_id, **filter_by):
        return cls.find_all(hotel_id=hotel_id, **filter_by)


