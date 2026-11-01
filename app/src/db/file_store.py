from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FileStore(Base):
    __tablename__ = "file_store"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String, default="files/{{id}}/")
    filename: Mapped[str] = mapped_column(String)

    pages: Mapped[list["Page"]] = relationship(back_populates="file_store")
