from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .page import Page
    from .setlist_song import SetlistSong


class Song(Base):
    __tablename__ = "song"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    pages: Mapped[list["Page"]] = relationship(back_populates="song")
    setlist_songs: Mapped[list["SetlistSong"]] = relationship(back_populates="song")
