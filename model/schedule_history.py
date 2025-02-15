from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

schedule_history_router = APIRouter(tags=["Schedule History"])

@schedule_history_router.get("/schedule_history/")
async def get_schedule_history(db=Depends(get_db)):
    db[0].execute("SELECT history_id, schedule_id, changes, timestamp FROM schedule_history")
    return [{"history_id": row[0], "schedule_id": row[1], "changes": row[2], "timestamp": row[3]} for row in db[0].fetchall()]

@schedule_history_router.post("/schedule_history/")
async def add_schedule_history(schedule_id: int = Form(...), changes: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO schedule_history (schedule_id, changes) VALUES (%s, %s)", (schedule_id, changes))
    db[1].commit()
    return {"message": "Schedule history recorded successfully"}
