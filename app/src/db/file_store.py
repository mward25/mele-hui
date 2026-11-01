from pathlib import Path

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FileStore(Base):
    __tablename__ = "file_store"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bucket: Mapped[str] = mapped_column(String, default="captures")
    filename: Mapped[str] = mapped_column(String, nullable=False)

    pages: Mapped[list["Page"]] = relationship(back_populates="file_store")

    @property
    def full_path(self) -> Path:
        from .events import STORAGE_ROOT

        return STORAGE_ROOT / self.bucket / str(self.id) / self.filename
