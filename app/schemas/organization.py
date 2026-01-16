from pydantic import BaseModel, Field

from app.schemas.activity import ActivityRead


class OrganizationPhoneRead(BaseModel):
    """Схема телефона организации."""

    id: int = Field(..., description="Идентификатор", examples=[1])
    phone: str = Field(..., description="Номер телефона", examples=["2-222-222"])

    model_config = {"from_attributes": True}


class OrganizationBase(BaseModel):
    """Базовая схема организации."""

    name: str = Field(
        ...,
        description="Название организации",
        examples=['ООО "Рога и Копыта"'],
    )


class OrganizationRead(OrganizationBase):
    """Схема организации для чтения."""

    id: int = Field(..., description="Уникальный идентификатор", examples=[1])
    building_id: int = Field(..., description="ID здания", examples=[1])
    phones: list[OrganizationPhoneRead] = Field(
        default_factory=list, description="Список телефонов"
    )
    activities: list[ActivityRead] = Field(
        default_factory=list, description="Виды деятельности"
    )

    model_config = {"from_attributes": True}


class OrganizationList(BaseModel):
    """Список организаций с пагинацией."""

    items: list[OrganizationRead] = Field(..., description="Список организаций")
    total: int = Field(..., description="Общее количество", examples=[100])
    page: int = Field(..., description="Текущая страница", examples=[1])
    size: int = Field(..., description="Размер страницы", examples=[10])
    pages: int = Field(..., description="Всего страниц", examples=[10])
