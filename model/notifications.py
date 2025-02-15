from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

notifications_router = APIRouter(tags=["Notifications"])

@notifications_router.get("/notifications/")
async def get_notifications(db=Depends(get_db)):
    db[0].execute("SELECT notification_id, message, created_at FROM notifications")
    return [{"notification_id": row[0], "message": row[1], "created_at": row[2]} for row in db[0].fetchall()]

@notifications_router.post("/notifications/")
async def create_notification(message: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO notifications (message) VALUES (%s)", (message,))
    db[1].commit()
    return {"message": "Notification created successfully"}
