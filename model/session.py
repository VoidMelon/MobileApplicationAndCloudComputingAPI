from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from model.base import Base
#from .environment import EnvironmentData
#from model.session_type import Type
#from .user import User

metadata = Base.metadata


class Session(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    date_of_creation: Mapped[datetime] = mapped_column(nullable=False)
    date_of_end: Mapped[datetime] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    #creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #creator: Mapped["User"] = relationship(back_populates="sessions")
    #environment_data: Mapped[List["EnvironmentData"]] = relationship(back_populates="session")
    #session_type: Mapped["Type"] = relationship()  # One Directional One-To-One Relationship
