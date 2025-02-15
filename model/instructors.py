from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

instructors_router = APIRouter(tags=["Instructors"])

@instructors_router.get("/instructors/")
async def get_instructors(db=Depends(get_db)):
    db[0].execute("SELECT instructor_id, full_name, email FROM instructors")
    return [{"instructor_id": row[0], "full_name": row[1], "email": row[2]} for row in db[0].fetchall()]

@instructors_router.post("/instructors/")
async def create_instructor(full_name: str = Form(...), email: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO instructors (full_name, email) VALUES (%s, %s)", (full_name, email))
    db[1].commit()
    return {"message": "Instructor created successfully"}

@instructors_router.put("/instructors/{instructor_id}")
async def update_instructor(instructor_id: int, full_name: str = Form(...), email: str = Form(...), db=Depends(get_db)):
    db[0].execute("UPDATE instructors SET full_name = %s, email = %s WHERE instructor_id = %s", (full_name, email, instructor_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Instructor updated successfully"}
    raise HTTPException(status_code=404, detail="Instructor not found")

@instructors_router.delete("/instructors/{instructor_id}")
async def delete_instructor(instructor_id: int, db=Depends(get_db)):
    db[0].execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Instructor deleted successfully"}
    raise HTTPException(status_code=404, detail="Instructor not found")
