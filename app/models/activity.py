from sqlalchemy import Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Activity(Base):
    """Вид деятельности"""

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название"
    )
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("activities.id"), nullable=True, index=True,
        comment="Родительская деятельность"
    )
    level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, comment="Уровень вложенности"
    )

    parent: Mapped["Activity | None"] = relationship(
        "Activity", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="parent"
    )

    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="check_activity_level"),
        {"comment": "Виды деятельности"},
    )

    def __str__(self) -> str:
        return self.name
