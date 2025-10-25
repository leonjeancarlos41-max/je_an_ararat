# app/routes/endpoints.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.data import store, User, Task, Product
from pydantic import BaseModel, Field

router = APIRouter()

# --- Schemas for requests ---
class CreateUser(BaseModel):
    name: str = Field(..., min_length=1)
    email: str

class UpdateUser(BaseModel):
    name: str | None
    email: str | None

class CreateTask(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = ""
    owner_id: str | None

class UpdateTask(BaseModel):
    title: str | None
    description: str | None
    completed: bool | None
    owner_id: str | None

class CreateProduct(BaseModel):
    name: str = Field(..., min_length=1)
    price: float

# --- User endpoints ---
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUser):
    new_id = store.new_id()
    user = User(id=new_id, name=payload.name, email=payload.email)
    store.users[new_id] = user
    return user

@router.get("/users", response_model=List[User])
def list_users():
    return list(store.users.values())

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, payload: UpdateUser):
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = user.copy(update=payload.dict(exclude_unset=True))
    store.users[user_id] = User(**updated.dict())
    return store.users[user_id]

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    if user_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")
    # remove user's tasks as well
    tasks_to_remove = [tid for tid, t in store.tasks.items() if t.owner_id == user_id]
    for tid in tasks_to_remove:
        del store.tasks[tid]
    del store.users[user_id]
    return

# --- Task endpoints ---
@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask):
    new_id = store.new_id()
    task = Task(id=new_id, title=payload.title, description=payload.description or "", completed=False, owner_id=payload.owner_id)
    store.tasks[new_id] = task
    return task

@router.get("/tasks", response_model=List[Task])
def list_tasks():
    return list(store.tasks.values())

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = store.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: UpdateTask):
    task = store.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.copy(update=payload.dict(exclude_unset=True))
    store.tasks[task_id] = Task(**updated.dict())
    return store.tasks[task_id]

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    if task_id not in store.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del store.tasks[task_id]
    return

# --- Product endpoints (simple CRUD) ---
@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(payload: CreateProduct):
    new_id = store.new_id()
    product = Product(id=new_id, name=payload.name, price=payload.price)
    store.products[new_id] = product
    return product

@router.get("/products", response_model=List[Product])
def list_products():
    return list(store.products.values())

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = store.products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    if product_id not in store.products:
        raise HTTPException(status_code=404, detail="Product not found")
    del store.products[product_id]
    return
