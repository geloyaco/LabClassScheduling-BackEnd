from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

schedules_router = APIRouter(tags=["Schedules"])

@ schedules_router.get("/schedules/")
async def get_schedules(db=Depends(get_db)):
    db[0].execute("SELECT schedule_id, course_id, instructor_id, lab_id, schedule_time FROM schedules")
    return [{"schedule_id": row[0], "course_id": row[1], "instructor_id": row[2], "lab_id": row[3], "schedule_time": row[4]} for row in db[0].fetchall()]

@schedules_router.post("/schedules/")
async def create_schedule(course_id: int = Form(...), instructor_id: int = Form(...), lab_id: int = Form(...), schedule_time: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO schedules (course_id, instructor_id, lab_id, schedule_time) VALUES (%s, %s, %s, %s)", (course_id, instructor_id, lab_id, schedule_time))
    db[1].commit()
    return {"message": "Schedule created successfully"}

@schedules_router.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int, db=Depends(get_db)):
    db[0].execute("DELETE FROM schedules WHERE schedule_id = %s", (schedule_id,))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Schedule deleted successfully"}
    raise HTTPException(status_code=404, detail="Schedule not found")
