from fastapi import FastAPI
from models import ToDo
from lifespan import lifespan
from dependency import SessionDependency
from schema import (GetToDoResponse, CreateToDoResponse, CreateToDoRequest, UpdateToDoResponse, UpdateToDoRequest,
                    DeleteToDoResponse)
import crud
from constants import STATUS_DELETED
from datetime import datetime

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
async def create_todo(todo_request: CreateToDoRequest, session: SessionDependency):
    todo = ToDo(
        title=todo_request.title,
        description=todo_request.description,
        important=todo_request.important
    )
    await crud.add_item(session, todo)
    return todo.id_dict


@app.patch('/api/v1/todo/{todo_id}', response_model=UpdateToDoResponse, tags=['ToDo'])
async def update_todo(todo_id: int, todo_request: UpdateToDoRequest, session: SessionDependency):
    todo_json = todo_request.model_dump(exclude_unset=True)
    if todo_request.done:
        todo_json['end_time'] = datetime.now()
    todo = await crud.get_item_by_id(session, ToDo, todo_id)
    for field, value in todo_json.items():
        setattr(todo, field, value)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.delete('/api/v1/todo/{todo_id}', response_model=DeleteToDoResponse, tags=['ToDo'])
async def delete_todo(todo_id: int, session: SessionDependency):
    todo = await crud.get_item_by_id(session, ToDo, todo_id)
    await crud.delete_item(todo, session)
    return STATUS_DELETED

