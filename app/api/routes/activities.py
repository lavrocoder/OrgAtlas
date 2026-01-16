import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import UNAUTHORIZED_RESPONSE
from app.db.session import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityList, ActivityRead

router = APIRouter(prefix="/activities", tags=["Виды деятельности"])


@router.get(
    "",
    response_model=ActivityList,
    summary="Список всех видов деятельности",
    description="Возвращает список всех видов деятельности с пагинацией.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def get_activities(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> ActivityList:
    """
    Получить список всех видов деятельности с пагинацией.

    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)

    Возвращает виды деятельности с информацией:
    - **id**: уникальный идентификатор
    - **name**: название
    - **parent_id**: ID родительской деятельности (null для корневых)
    - **level**: уровень вложенности (1-3)
    """
    offset = (page - 1) * size

    # Получаем общее количество
    count_result = await db.execute(select(func.count(Activity.id)))
    total = count_result.scalar() or 0

    # Получаем страницу данных
    result = await db.execute(
        select(Activity).offset(offset).limit(size).order_by(Activity.level, Activity.id)
    )
    activities = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return ActivityList(
        items=[ActivityRead.model_validate(a) for a in activities],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )
