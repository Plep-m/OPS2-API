from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.base import Base
from pydantic import BaseModel, Json, ValidationError

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class TagCreate(BaseModel):
    name: str