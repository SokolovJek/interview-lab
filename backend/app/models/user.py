from sqlalchemy import Column, String, Boolean

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    hash = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
