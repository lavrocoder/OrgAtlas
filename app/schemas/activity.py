from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    """Базовая схема вида деятельности."""

    name: str = Field(
        ...,
        description="Название вида деятельности",
        examples=["Мясная продукция"],
    )


class ActivityRead(ActivityBase):
    """Схема вида деятельности для чтения."""

    id: int = Field(..., description="Уникальный идентификатор", examples=[1])
    parent_id: int | None = Field(
        None, description="ID родительской деятельности", examples=[1]
    )
    level: int = Field(..., ge=1, le=3, description="Уровень вложенности (1-3)", examples=[1])

    model_config = {"from_attributes": True}


class ActivityList(BaseModel):
    """Список видов деятельности с пагинацией."""

    items: list[ActivityRead] = Field(..., description="Список видов деятельности")
    total: int = Field(..., description="Общее количество", examples=[20])
    page: int = Field(..., description="Текущая страница", examples=[1])
    size: int = Field(..., description="Размер страницы", examples=[10])
    pages: int = Field(..., description="Всего страниц", examples=[2])
