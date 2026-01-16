from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class Building(Base):
    """Здание"""

    __tablename__ = "buildings"
    __table_args__ = {"comment": "Здания"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="Адрес"
    )
    latitude: Mapped[float] = mapped_column(
        Float, nullable=False, comment="Широта"
    )
    longitude: Mapped[float] = mapped_column(
        Float, nullable=False, comment="Долгота"
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="building"
    )

    def __str__(self) -> str:
        return self.address
