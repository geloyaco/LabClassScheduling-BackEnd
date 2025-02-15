from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db
from typing import List

users_router = APIRouter(tags=["Users"])

@users_router.get("/users/", response_model=List[dict])
async def get_users(db=Depends(get_db)):
    query = "SELECT user_id, full_name, email, role_id, is_active FROM users"
    db[0].execute(query)
    users = [{"user_id": row[0], "full_name": row[1], "email": row[2], "role_id": row[3], "is_active": row[4]} for row in db[0].fetchall()]
    return users

@users_router.post("/users/", response_model=dict)
async def create_user(full_name: str = Form(...), email: str = Form(...), password_hash: str = Form(...), role_id: int = Form(...), db=Depends(get_db)):
    query = "INSERT INTO users (full_name, email, password_hash, role_id) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (full_name, email, password_hash, role_id))
    db[1].commit()
    return {"message": "User created successfully"}

@users_router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, full_name: str = Form(...), email: str = Form(...), role_id: int = Form(...), is_active: bool = Form(...), db=Depends(get_db)):
    query = "UPDATE users SET full_name = %s, email = %s, role_id = %s, is_active = %s WHERE user_id = %s"
    db[0].execute(query, (full_name, email, role_id, is_active, user_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@users_router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db=Depends(get_db)):
    query = "DELETE FROM users WHERE user_id = %s"
    db[0].execute(query, (user_id,))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
