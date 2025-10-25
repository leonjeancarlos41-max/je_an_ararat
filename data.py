# app/models/data.py
from typing import Dict
from pydantic import BaseModel, Field
from uuid import uuid4

# Pydantic models
class User(BaseModel):
    id: str
    name: str = Field(..., min_length=1)
    email: str

class Task(BaseModel):
    id: str
    title: str = Field(..., min_length=1)
    description: str = ""
    completed: bool = False
    owner_id: str | None = None

class Product(BaseModel):
    id: str
    name: str
    price: float

# Simple in-memory stores
class Store:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.tasks: Dict[str, Task] = {}
        self.products: Dict[str, Product] = {}

    def new_id(self) -> str:
        return uuid4().hex

store = Store()

# Helper to seed some data (optional)
def seed():
    if not store.users:
        u1_id = store.new_id()
        store.users[u1_id] = User(id=u1_id, name="Jean Ararat", email="jean@example.com")
    if not store.tasks:
        t1 = store.new_id()
        store.tasks[t1] = Task(id=t1, title="Primer tarea", description="Ejemplo", completed=False, owner_id=list(store.users.keys())[0])
    if not store.products:
        p1 = store.new_id()
        store.products[p1] = Product(id=p1, name="Lapicero", price=1.5)

# call seed on import (safe for demo)
seed()
