from sqlalchemy import select, insert
from app.bookings.models import Bookings
from app.database import async_session_maker


class BaseService:
    
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    
    @classmethod
    async def find_one_or_none(cls, **filter_params):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_params)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_params):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_params)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()