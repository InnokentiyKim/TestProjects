import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class IdResponseBase(BaseModel):
    id: int

class StatusResponse(BaseModel):
    status: Literal['deleted']


class GetToDoResponse(BaseModel):
    id: int
    title: str
    description: str
    important: bool
    done: bool
    start_time: datetime
    end_time: datetime | None


class CreateToDoRequest(BaseModel):
    title: str
    description: str
    important: bool

class CreateToDoResponse(IdResponseBase):
    pass


class UpdateToDoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    important: bool | None = None
    done: bool | None = None

class UpdateToDoResponse(IdResponseBase):
    pass


class DeleteToDoResponse(StatusResponse):
    pass


class BaseUserRequest(BaseModel):
    name: str
    password: str

class CreateUserRequest(BaseUserRequest):
    pass

class CreateUserResponse(IdResponseBase):
    pass

class LoginRequest(BaseUserRequest):
    pass

class LoginResponse(BaseModel):
    token: uuid.UUID