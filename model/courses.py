from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

courses_router = APIRouter(tags=["Courses"])

@courses_router.get("/courses/")
async def get_courses(db=Depends(get_db)):
    db[0].execute("SELECT course_id, course_name, course_code FROM courses")
    return [{"course_id": row[0], "course_name": row[1], "course_code": row[2]} for row in db[0].fetchall()]

@courses_router.post("/courses/")
async def create_course(course_name: str = Form(...), course_code: str = Form(...), db=Depends(get_db)):
    db[0].execute("INSERT INTO courses (course_name, course_code) VALUES (%s, %s)", (course_name, course_code))
    db[1].commit()
    return {"message": "Course created successfully"}

@courses_router.put("/courses/{course_id}")
async def update_course(course_id: int, course_name: str = Form(...), course_code: str = Form(...), db=Depends(get_db)):
    db[0].execute("UPDATE courses SET course_name = %s, course_code = %s WHERE course_id = %s", (course_name, course_code, course_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Course updated successfully"}
    raise HTTPException(status_code=404, detail="Course not found")

@courses_router.delete("/courses/{course_id}")
async def delete_course(course_id: int, db=Depends(get_db)):
    db[0].execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Course deleted successfully"}
    raise HTTPException(status_code=404, detail="Course not found")
