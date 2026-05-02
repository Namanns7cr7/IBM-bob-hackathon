# FastAPI Basics

## What is FastAPI?

FastAPI is a modern, fast web framework for building APIs with Python. It uses Python type hints for automatic validation and documentation.

## Creating an API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

## Path Parameters

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

## Query Parameters

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

## Request Body with Pydantic

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
```

## Async Endpoints

FastAPI supports async/await for better performance:

```python
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = await database.fetch_user(user_id)
    return user
```

## Dependency Injection

```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db = Depends(get_db)):
    return db.get_users()
```

## Response Models

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    return get_user_from_db(user_id)
```

## Status Codes

```python
from fastapi import status

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    return save_user(user)
```

## Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

## Why FastAPI?

- **Fast**: High performance, on par with NodeJS and Go
- **Type Safety**: Uses Python type hints
- **Auto Documentation**: Generates interactive API docs
- **Easy to Learn**: Intuitive and simple
- **Async Support**: Built-in async/await support