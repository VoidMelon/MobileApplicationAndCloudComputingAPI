from enum import Enum
from datetime import datetime
from typing import List

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from model.base import Base

from marshmallow import Schema, fields

metadata = Base.metadata

friendship = Table(
    "friendship",
    Base.metadata,
    Column("friend_to", String, ForeignKey("users.id"), primary_key=True),
    Column("user", String, ForeignKey("users.id"), primary_key=True),
)

pending = Table(
    "pending",
    Base.metadata,
    Column("waiting", String, ForeignKey("users.id"), primary_key=True),
    Column("for_confirmation", String, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    email_verified: Mapped[str] = mapped_column(nullable=False)
    sign_up_date: Mapped[datetime] = mapped_column(nullable=False)
    sessions: Mapped[List["Session"]] = relationship(
        back_populates="creator", cascade="all, delete-orphan")  # One directional no parameters on the relationship() function

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
    creator_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="sessions")
    avgSpeed: Mapped[float] = mapped_column(nullable=False)
    number_of_step: Mapped[int] = mapped_column(nullable=False)
    totalDistance: Mapped[float] = mapped_column(nullable=False)
    environment_data: Mapped[List["EnvironmentData"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    session_type: Mapped["Type"] = relationship()  # One Directional One-To-One Relationship
    session_type_id: Mapped[int] = mapped_column(ForeignKey("session_type.id"))


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


class EnvironmentDataSchema(Schema):
    id = fields.Integer()
    temperature = fields.Float()
    humidity = fields.Float()
    pressure = fields.Float()
    latitude = fields.Float()
    longitude = fields.Float()
    date_of_measurement = fields.DateTime()
    session_id = fields.Integer()


class SessionSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    date_of_creation = fields.DateTime()
    date_of_end = fields.DateTime()
    creator_id = fields.String()
    session_type_id = fields.Integer()


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    email_verified = fields.Boolean()
    sign_up_date = fields.DateTime()
