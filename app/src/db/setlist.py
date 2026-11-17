from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .setlist_song import SetlistSong


class Setlist(Base):
    __tablename__ = "setlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    creation_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    setlist_songs: Mapped[list["SetlistSong"]] = relationship(back_populates="setlist", order_by="SetlistSong.position")
