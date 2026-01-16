from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Параметры пагинации."""

    page: int = Field(
        default=1,
        ge=1,
        description="Номер страницы",
        examples=[1],
    )
    size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Количество элементов на странице",
        examples=[10],
    )

    @property
    def offset(self) -> int:
        """Смещение для SQL запроса."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Базовый ответ с пагинацией."""

    items: list[T] = Field(..., description="Список элементов")
    total: int = Field(..., description="Общее количество элементов", examples=[100])
    page: int = Field(..., description="Текущая страница", examples=[1])
    size: int = Field(..., description="Размер страницы", examples=[10])
    pages: int = Field(..., description="Всего страниц", examples=[10])
