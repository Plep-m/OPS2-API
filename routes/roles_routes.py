from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.role_model import Role, RoleCreate
from src.database import get_db
from src.role_utils import add_role, delete_role, update_role, add_roles

router = APIRouter()

@router.get("/roles/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles

@router.post("/role/add")
def post_role(role_create: RoleCreate, db: Session = Depends(get_db)):
    add_role(role_create.name, db)
    return {"message": "Role added successfully"}

@router.post("/roles/add")
def post_roles(role_names: List[str], db: Session = Depends(get_db)):
    add_roles(role_names, db)
    return {"message": "Roles added successfully"}

@router.post("/role/update")
def update_role_endpoint(role_name: str, new_name: str, db: Session = Depends(get_db)):
    update_role(role_name, new_name, db)
    return {"message": f"Role '{role_name}' updated successfully to '{new_name}'"}

@router.post("/role/delete")
def delete_role_endpoint(role_name: str, db: Session = Depends(get_db)):
    delete_role(role_name, db)
    return {"message": f"Role '{role_name}' deleted successfully"}