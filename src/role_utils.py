from sqlalchemy.orm import Session
from models.role_model import Role

def create_default_roles(db: Session):
    print("Creating default roles")
    default_roles = ["administrator", "staff", "developper", "client"]
    add_roles(default_roles, db)

def add_role(role_name: str, db: Session):
    if db.query(Role).filter(Role.name == role_name).first() is None:
        db_role = Role(name=role_name)
        db.add(db_role)
        db.commit()

def add_roles(role_names: list, db: Session):
    for role_name in role_names:
        add_role(role_name, db)

def delete_role(role_name: str, db: Session):
    role = db.query(Role).filter(Role.name == role_name).first()
    if role:
        db.delete(role)
        db.commit()

def update_role(role_name: str, new_name: str, db: Session):
    role = db.query(Role).filter(Role.name == role_name).first()
    if role:
        role.name = new_name
        db.commit()