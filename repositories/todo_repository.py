from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, And
from pydantic import BaseModel
from typing import Dict
import os

from dotenv import load_dotenv
    
load_dotenv()

SA_FILE_PATH = os.getenv("SA_FILE_PATH")

# Initialize Firestore client for database operations
firestore_db = firestore.Client.from_service_account_json(SA_FILE_PATH)

class TodoCreate(BaseModel):
    title: str

class Todo(TodoCreate):
    id: int
    completed: bool = False

class TodoRepository:
    def __init__(self):
        self.todos: Dict[str, Todo] = {}

    def create_todo(self, todo: TodoCreate) -> Todo:
        new_todo = Todo(id=len(self.todos) + 1, **todo.model_dump())
        self.todos[new_todo.id] = new_todo
        return new_todo

    def get_todos(self) -> list[Todo]:
        return list(self.todos.values())

    def get_todo(self, todo_id: int) -> Todo | None:
        todo = self.todos.get(todo_id, False)
        if todo:
            return todo
        else:
            return None

    def update_todo(self, todo_id: int, updated_todo: TodoCreate) -> Todo | None:
        todo = self.todos.get(todo_id, False)
        if todo:
            todo.title = updated_todo.title
            return todo
        else:
            return None

    def delete_todo(self, todo_id: int) -> bool:
        try:
            del self.todos[todo_id]
            return True
        except KeyError:
            return False