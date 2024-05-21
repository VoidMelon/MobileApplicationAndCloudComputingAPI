from datetime import datetime
from typing import List

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship

from model.session import Session


class Base(DeclarativeBase):
    pass


friendship = Table(
    "friendship",
    Base.metadata,
    Column("friend_to", Integer, ForeignKey("user.id"), primary_key=True),
    Column("user", Integer, ForeignKey("user.id"), primary_key=True),
)

pending = Table(
    "pending",
    Base.metadata,
    Column("waiting", Integer, ForeignKey("user.id"), primary_key=True),
    Column("for_confirmation", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    email_verified: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    sign_up_date: Mapped[datetime] = mapped_column(nullable=False)
    sessions: Mapped[List["Session"]] = relationship(back_populates="creator")  # One directional no parameters on the relationship() function


    # Self-Referential Many-To-Many for modelling friend list and pending


    friend_to: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendship,
        primaryjoin=id == friendship.c.user.id,
        secondaryjoin=id == friendship.c.friend_to.id,
        back_populates="users"
    )
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendship,
        primaryjoin=id == friendship.c.friend_to.id,
        secondaryjoin=id == friendship.c.user.id,
        back_populates="friend_to"
    )
    waiting: Mapped[List["User"]] = relationship(
        "User",
        secondary=pending,
        primaryjoin=id == pending.c.for_confirmation.id,
        secondaryjoin=id == pending.c.waiting.id,
        back_populates="for_confirmation"
    )
    for_confirmation: Mapped[List["User"]] = relationship(
        "User",
        secondary=pending,
        primaryjoin=id == pending.c.waiting.id,
        secondaryjoin=id == pending.c.for_confirmation.id,
        back_populates="waiting"
    )
