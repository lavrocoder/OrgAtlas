from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    """Базовая схема здания."""

    address: str = Field(
        ...,
        description="Адрес здания",
        examples=["г. Москва, ул. Ленина, д. 1"],
    )
    latitude: float = Field(
        ...,
        description="Широта (географическая координата)",
        ge=-90,
        le=90,
        examples=[55.753215],
    )
    longitude: float = Field(
        ...,
        description="Долгота (географическая координата)",
        ge=-180,
        le=180,
        examples=[37.622504],
    )


class BuildingRead(BuildingBase):
    """Схема здания для чтения."""

    id: int = Field(..., description="Уникальный идентификатор здания", examples=[1])

    model_config = {"from_attributes": True}


class BuildingList(BaseModel):
    """Список зданий с пагинацией."""

    items: list[BuildingRead] = Field(..., description="Список зданий")
    total: int = Field(..., description="Общее количество зданий", examples=[100])
    page: int = Field(..., description="Текущая страница", examples=[1])
    size: int = Field(..., description="Размер страницы", examples=[10])
    pages: int = Field(..., description="Всего страниц", examples=[10])
