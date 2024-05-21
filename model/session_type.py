from enum import Enum
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class SessionType(Enum):
    OUTDOOR_RUNNING = 'Outdoor Running'
    INDOOR_RUNNING = 'Indoor Running'
    GYM = 'Gym'
    CALISTHENICS = 'Calisthenics'
    OUTDOOR_TRAINING = 'Outdoor Training'
    SWIMMING = 'Swimming'


class Type(Base):
    __tablename__ = 'session_type'
    id: [int] = mapped_column(autoincrement=True, primary_key=True)
    type: [SessionType]
