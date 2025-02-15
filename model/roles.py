# model/roles.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

roles_router = APIRouter(tags=["Roles"])

# Get all roles
@roles_router.get("/roles/", response_model=list)
async def read_roles(
    db=Depends(get_db)
):
    query = "SELECT role_id, role_name FROM roles"
    db[0].execute(query)
    roles = [{"role_id": role[0], "role_name": role[1]} for role in db[0].fetchall()]
    return roles

# Get a specific role by ID
@roles_router.get("/roles/{role_id}", response_model=dict)
async def read_role(
    role_id: int,
    db=Depends(get_db)
):
    query = "SELECT role_id, role_name FROM roles WHERE role_id = %s"
    db[0].execute(query, (role_id,))
    role = db[0].fetchone()
    if role:
        return {"role_id": role[0], "role_name": role[1]}
    raise HTTPException(status_code=404, detail="Role not found")

# Create a new role
@roles_router.post("/roles/", response_model=dict)
async def create_role(
    role_name: str = Form(...),
    db=Depends(get_db)
):
    query = "INSERT INTO roles (role_name) VALUES (%s)"
    db[0].execute(query, (role_name,))
    
    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_role_id = db[0].fetchone()[0]
    db[1].commit()

    return {"role_id": new_role_id, "role_name": role_name}

# Update an existing role
@roles_router.put("/roles/{role_id}", response_model=dict)
async def update_role(
    role_id: int,
    role_name: str = Form(...),
    db=Depends(get_db)
):
    query = "UPDATE roles SET role_name = %s WHERE role_id = %s"
    db[0].execute(query, (role_name, role_id))
    
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Role updated successfully"}
    
    raise HTTPException(status_code=404, detail="Role not found")

# Delete a role
@roles_router.delete("/roles/{role_id}", response_model=dict)
async def delete_role(
    role_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the role exists
        query_check_role = "SELECT role_id FROM roles WHERE role_id = %s"
        db[0].execute(query_check_role, (role_id,))
        existing_role = db[0].fetchone()

        if not existing_role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Delete the role
        query_delete_role = "DELETE FROM roles WHERE role_id = %s"
        db[0].execute(query_delete_role, (role_id,))
        db[1].commit()

        return {"message": "Role deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()
