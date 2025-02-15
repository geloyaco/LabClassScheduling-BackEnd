from fastapi import APIRouter, Depends, HTTPException, Form
from .db import get_db

laboratories_router = APIRouter(tags=["Laboratories"])

@laboratories_router.get("/laboratories/")
async def get_laboratories(db=Depends(get_db)):
    db[0].execute("SELECT lab_id, lab_name, lab_color FROM laboratories")
    return [{"lab_id": row[0], "lab_name": row[1], "lab_color": row[2]} for row in db[0].fetchall()]

@laboratories_router.post("/laboratories/")
async def create_laboratory(lab_name: str = Form(...), lab_color: str = Form("#FF0000"), db=Depends(get_db)):
    db[0].execute("INSERT INTO laboratories (lab_name, lab_color) VALUES (%s, %s)", (lab_name, lab_color))
    db[1].commit()
    return {"message": "Laboratory created successfully"}

@laboratories_router.put("/laboratories/{lab_id}")
async def update_laboratory(lab_id: int, lab_name: str = Form(...), lab_color: str = Form(...), db=Depends(get_db)):
    db[0].execute("UPDATE laboratories SET lab_name = %s, lab_color = %s WHERE lab_id = %s", (lab_name, lab_color, lab_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Laboratory updated successfully"}
    raise HTTPException(status_code=404, detail="Laboratory not found")

@laboratories_router.delete("/laboratories/{lab_id}")
async def delete_laboratory(lab_id: int, db=Depends(get_db)):
    db[0].execute("DELETE FROM laboratories WHERE lab_id = %s", (lab_id,))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Laboratory deleted successfully"}
    raise HTTPException(status_code=404, detail="Laboratory not found")
