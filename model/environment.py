from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base
#from .session import Session

metadata = Base.metadata


class EnvironmentData(Base):
    __tablename__ = 'environment_data'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    date_of_measurement: Mapped[datetime] = mapped_column(nullable=False)
    #session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id'))
    #session: Mapped["Session"] = mapped_column(back_populates="environment_data")
