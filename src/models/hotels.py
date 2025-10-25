import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm

class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    location: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="hotel",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
