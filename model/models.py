from enum import Enum
from datetime import datetime
from typing import List

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from model.base import Base

metadata = Base.metadata

friendship = Table(
    "friendship",
    Base.metadata,
    Column("friend_to", Integer, ForeignKey("users.id"), primary_key=True),
    Column("user", Integer, ForeignKey("users.id"), primary_key=True),
)

pending = Table(
    "pending",
    Base.metadata,
    Column("waiting", Integer, ForeignKey("users.id"), primary_key=True),
    Column("for_confirmation", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    email_verified: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    sign_up_date: Mapped[datetime] = mapped_column(nullable=False)
    sessions: Mapped[List["Session"]] = relationship(
        back_populates="creator")  # One directional no parameters on the relationship() function

    # Self-Referential Many-To-Many for modelling friend list and pending

    friend_to: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendship,
        primaryjoin=id == friendship.c.user,
        secondaryjoin=id == friendship.c.friend_to,
        back_populates="users"
    )
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendship,
        primaryjoin=id == friendship.c.friend_to,
        secondaryjoin=id == friendship.c.user,
        back_populates="friend_to"
    )
    waiting: Mapped[List["User"]] = relationship(
        "User",
        secondary=pending,
        primaryjoin=id == pending.c.for_confirmation,
        secondaryjoin=id == pending.c.waiting,
        back_populates="for_confirmation"
    )
    for_confirmation: Mapped[List["User"]] = relationship(
        "User",
        secondary=pending,
        primaryjoin=id == pending.c.waiting,
        secondaryjoin=id == pending.c.for_confirmation,
        back_populates="waiting"
    )


class SessionType(Enum):
    OUTDOOR_RUNNING = 'Outdoor Running'
    INDOOR_RUNNING = 'Indoor Running'
    GYM = 'Gym'
    CALISTHENICS = 'Calisthenics'
    OUTDOOR_TRAINING = 'Outdoor Training'
    SWIMMING = 'Swimming'


class Type(Base):
    __tablename__ = 'session_type'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type: Mapped[SessionType]


class Session(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    date_of_creation: Mapped[datetime] = mapped_column(nullable=False)
    date_of_end: Mapped[datetime] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="sessions")
    environment_data: Mapped[List["EnvironmentData"]] = relationship(back_populates="session")
    session_type: Mapped["Type"] = relationship()  # One Directional One-To-One Relationship


class EnvironmentData(Base):
    __tablename__ = 'environment_data'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    date_of_measurement: Mapped[datetime] = mapped_column(nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id'))
    session: Mapped["Session"] = relationship(back_populates="environment_data")