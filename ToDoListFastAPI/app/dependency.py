import uuid

from models import Session, Token
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from config import TOKEN_TTL_SEC
from datetime import datetime, timedelta


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]


async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency):
    token_query = select(Token).where(
        Token.token == x_token,
        Token.created_at >= datetime.now() - timedelta(seconds=TOKEN_TTL_SEC)
    )
    token = await session.scalar(token_query)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token


TokenDependency = Annotated[Token, Depends(get_token)]



