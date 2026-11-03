from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Setlist(Base):
    __tablename__ = "setlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    setlist_songs: Mapped[list["SetlistSong"]] = relationship(
        back_populates="setlist", order_by="SetlistSong.position"
    )
