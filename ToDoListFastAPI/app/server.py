from fastapi import FastAPI

import auth
from models import ToDo, User, Token
from lifespan import lifespan
from dependency import SessionDependency, TokenDependency
from schema import (GetToDoResponse, CreateToDoResponse, CreateToDoRequest, UpdateToDoResponse, UpdateToDoRequest,
                    DeleteToDoResponse, CreateUserRequest, CreateUserResponse, LoginRequest, LoginResponse)
import crud
from constants import STATUS_DELETED
from datetime import datetime
from sqlalchemy import select
from fastapi import HTTPException, status

app = FastAPI(
    title="ToDoList on FastAPI",
    terms_of_service="",
    description="A simple ToDoList application built using FastAPI.",
    lifespan=lifespan
)


@app.get('/api/v1/todo/{todo_id}', response_model=GetToDoResponse, tags=['ToDo'])
async def get_todo(session: SessionDependency, todo_id: int):
    todo_item = await crud.get_item_by_id(session, ToDo, todo_id)
    return todo_item.to_dict


@app.post('/api/v1/todo', response_model=CreateToDoResponse, tags=['ToDo'])
async def create_todo(todo_request: CreateToDoRequest,
                      session: SessionDependency,
                      token: TokenDependency
                      ):
    todo = ToDo(
        title=todo_request.title,
        description=todo_request.description,
        important=todo_request.important,
        user_id=token.user_id
    )
    await crud.add_item(session, todo)
    return todo.id_dict


@app.patch('/api/v1/todo/{todo_id}', response_model=UpdateToDoResponse, tags=['ToDo'])
async def update_todo(todo_id: int, todo_request: UpdateToDoRequest,
                      session: SessionDependency, token: TokenDependency):
    todo_json = todo_request.model_dump(exclude_unset=True)
    if todo_request.done:
        todo_json['end_time'] = datetime.now()
    todo = await crud.get_item_by_id(session, ToDo, todo_id)
    if todo.user_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    for field, value in todo_json.items():
        setattr(todo, field, value)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.delete('/api/v1/todo/{todo_id}', response_model=DeleteToDoResponse, tags=['ToDo'])
async def delete_todo(todo_id: int, session: SessionDependency):
    todo = await crud.get_item_by_id(session, ToDo, todo_id)
    await crud.delete_item(todo, session)
    return STATUS_DELETED


@app.post('/api/v1/user', response_model=CreateUserResponse, tags=["User"])
async def create_user(user_request: CreateUserRequest, session: SessionDependency):
    user_request_dict = user_request.model_dump()
    user_request_dict["password"] = auth.hash_password(user_request_dict["password"])
    user = User(**user_request_dict)
    await crud.add_item(session, user)
    return user.id_dict


@app.post('/api/v1/login', response_model=LoginResponse, tags=["Login"])
async def login(login_request: LoginRequest, session: SessionDependency):
    user_query = select(User).where(User.name == login_request.name)
    user = await session.scalar(user_query)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not auth.check_password(login_request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    token = Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.to_dict
