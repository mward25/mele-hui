from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Page(Base):
    __tablename__ = "page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("file_store.id"), nullable=False)

    song: Mapped["Song"] = relationship(back_populates="pages")
    file_store: Mapped["FileStore"] = relationship(back_populates="pages")

    drawing_svg: Mapped[str | None] = mapped_column(Text, nullable=True)
