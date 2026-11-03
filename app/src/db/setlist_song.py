from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SetlistSong(Base):
    __tablename__ = "setlist_song"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    setlist_id: Mapped[int] = mapped_column(ForeignKey("setlist.id"), nullable=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    setlist: Mapped["Setlist"] = relationship(back_populates="setlist_songs")
    song: Mapped["Song"] = relationship(back_populates="setlist_songs")
