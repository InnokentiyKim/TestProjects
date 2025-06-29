from sqlalchemy.exc import IntegrityError

from app.database import async_session_maker
from sqlalchemy import select, insert


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def update(cls, model_id, **data):
        async with async_session_maker() as session:
            instance = await cls.find_by_id(model_id)
            if instance:
                for key, value in data.items():
                    setattr(instance, key, value)
                try:
                    await session.commit()
                except IntegrityError:
                    return None
                return instance
            return None


    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            instance = await cls.find_by_id(model_id)
            if instance:
                await session.delete(instance)
                await session.commit()
                return True
            return False

