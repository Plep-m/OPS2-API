from sqlalchemy.orm import Session
from models.tag_model import Tag

def create_default_tags(db: Session):
    print("Creating default tags")
    default_tags = ["admin", "client", "technique", "vente"]
    add_tags(default_tags, db)

def add_tag(tag_name: str, db: Session):
    if db.query(Tag).filter(Tag.name == tag_name).first() is None:
        db_role = Tag(name=tag_name)
        db.add(db_role)
        db.commit()

def add_tags(tag_names: list, db: Session):
    for tag_name in tag_names:
        add_tag(tag_name, db)

def delete_tag(tag_name: str, db: Session):
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if tag:
        db.delete(tag)
        db.commit()

def update_tag(tag_name: str, new_name: str, db: Session):
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if tag:
        tag.name = new_name
        db.commit()