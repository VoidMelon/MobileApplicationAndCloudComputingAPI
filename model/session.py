from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship

from model.environment import EnvironmentData
from model.session_type import Type
from model.user import User


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = 'sessions'
    session_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    date_of_creation: Mapped[datetime] = mapped_column(nullable=False)
    date_of_end: Mapped[datetime] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="sessions")
    environment_data: Mapped[List["EnvironmentData"]] = relationship(back_populates="session")
    session_type: Mapped["Type"] = relationship()  # One Directional One-To-One Relationship
