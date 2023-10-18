from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Table, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from src.base import Base
from typing import Any, List
from pydantic import BaseModel, Json, ValidationError
from models.role_model import RoleCreate
from datetime import datetime

# Define GenderEnum
class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"

# Association table for many-to-many relationship between User and Role
user_roles_association = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    pseudo = Column(String, nullable=True)
    birthday = Column(DateTime(timezone=True), nullable=True)
    gender = Column(SQLAlchemyEnum(GenderEnum), default=GenderEnum.NON_BINARY, nullable=False)
    phone = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    close = Column(Boolean, default=False)
    metas = Column(JSON, default={})
    personnal_mail = Column(String, nullable=True)
    school_mail = Column(String, nullable=True, default=lambda context: f"{context.current_parameters['firstname'].lower()}_{context.current_parameters['lastname'].lower()}@isdan-school.com")
    login = Column(String, nullable=True, default=lambda context: f"{context.current_parameters['firstname'].lower()}_{context.current_parameters['lastname'].lower()}")
    password = Column(String, nullable=False)
    user_personnal_token = Column(String, nullable=True)
    roles = relationship('Role', secondary=user_roles_association, back_populates='users')

    @property
    def age(self):
        if self.birthday:
            today = datetime.now().date()
            age = today.year - self.birthday.date().year - ((today.month, today.day) < (self.birthday.date().month, self.birthday.date().day))
            return age

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    password: str = None
    gender: GenderEnum = GenderEnum.NON_BINARY
    phone: str = None
    postal_code: str = None
    address: str = None
    city: str = None
    country: str = None
    metas: Json[Any] = None
    roles: List[RoleCreate] = []