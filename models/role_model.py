from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from src.base import Base
from typing import Any, List
from pydantic import BaseModel, Json, ValidationError

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    metas = Column(JSON, default={})
    users = relationship('User', secondary='user_roles', back_populates='roles')

class RoleCreate(BaseModel):
    name: str
    metas: Json[Any] = None