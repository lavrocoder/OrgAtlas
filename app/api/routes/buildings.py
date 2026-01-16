import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import UNAUTHORIZED_RESPONSE
from app.db.session import get_db
from app.models.building import Building
from app.schemas.building import BuildingList, BuildingRead

router = APIRouter(prefix="/buildings", tags=["Здания"])


@router.get(
    "",
    response_model=BuildingList,
    summary="Список всех зданий",
    description="Возвращает список зданий с пагинацией.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def get_buildings(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> BuildingList:
    """
    Получить список зданий с пагинацией.

    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)

    Возвращает здания с информацией:
    - **id**: уникальный идентификатор
    - **address**: полный адрес здания
    - **latitude**: широта
    - **longitude**: долгота
    """
    offset = (page - 1) * size

    # Получаем общее количество
    count_result = await db.execute(select(func.count(Building.id)))
    total = count_result.scalar() or 0

    # Получаем страницу данных
    result = await db.execute(
        select(Building).offset(offset).limit(size).order_by(Building.id)
    )
    buildings = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return BuildingList(
        items=[BuildingRead.model_validate(b) for b in buildings],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )
