from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.building import Building


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    """Организация"""

    __tablename__ = "organizations"
    __table_args__ = {"comment": "Организации"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(500), nullable=False, index=True, comment="Название"
    )
    building_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("buildings.id"), nullable=False, index=True,
        comment="Здание"
    )

    building: Mapped["Building"] = relationship("Building", back_populates="organizations")
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        "OrganizationPhone", back_populates="organization", cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", secondary=organization_activity, lazy="selectin"
    )

    def __str__(self) -> str:
        return self.name


class OrganizationPhone(Base):
    """Телефон организации"""

    __tablename__ = "organization_phones"
    __table_args__ = {"comment": "Телефоны организаций"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Номер телефона"
    )
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True,
        comment="Организация"
    )

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="phones"
    )

    def __str__(self) -> str:
        return self.phone
