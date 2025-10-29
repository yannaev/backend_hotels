import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm, HotelsOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    hotel: Mapped[list["HotelsOrm"]] = relationship(back_populates="rooms")

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        secondary="rooms_facilities", back_populates="rooms", passive_deletes=True
    )
