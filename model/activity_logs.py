from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

activity_logs_router = APIRouter(tags=["Activity Logs"])

@activity_logs_router.get("/activity_logs/")
async def get_activity_logs(db=Depends(get_db)):
    db[0].execute("SELECT log_id, user_id, action, timestamp FROM activity_logs")
    return [{"log_id": row[0], "user_id": row[1], "action": row[2], "timestamp": row[3]} for row in db[0].fetchall()]

@activity_logs_router.post("/activity_logs/")
async def create_activity_log(user_id: int = Form(...), action: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)", (user_id, action))
    db[1].commit()
    return {"message": "Activity log created successfully"}
