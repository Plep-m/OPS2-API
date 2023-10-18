from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.tag_model import Tag, TagCreate
from src.database import get_db
from src.tag_utils import add_tag, add_tags, delete_tag, update_tag

router = APIRouter()


@router.get("/tags/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Tag).all()
    return roles

@router.post("/tag/add")
def post_role(tag_create: TagCreate, db: Session = Depends(get_db)):
    add_tag(tag_create.name, db)
    return {"message": "Tag added successfully"}

@router.post("/tags/add")
def post_tags(tag_names: List[str], db: Session = Depends(get_db)):
    add_tags(tag_names, db)
    return {"message": "Tags added successfully"}

@router.post("/tag/update")
def update_tag_endpoint(tag_name: str, new_name: str, db: Session = Depends(get_db)):
    update_tag(tag_name, new_name, db)
    return {"message": f"Tag '{tag_name}' updated successfully to '{new_name}'"}

@router.post("/tag/delete")
def delete_role_endpoint(tag_name: str, db: Session = Depends(get_db)):
    delete_tag(tag_name, db)
    return {"message": f"Tag '{tag_name}' deleted successfully"}