import math

from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlalchemy import select, func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.responses import UNAUTHORIZED_RESPONSE
from app.db.session import get_db
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, organization_activity
from app.schemas.organization import OrganizationList, OrganizationRead

router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.get(
    "",
    response_model=OrganizationList,
    summary="Список всех организаций",
    description="Возвращает список всех организаций с пагинацией.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def get_organizations(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Получить список всех организаций с пагинацией.

    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)
    """
    offset = (page - 1) * size

    count_result = await db.execute(select(func.count(Organization.id)))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/search",
    response_model=OrganizationList,
    summary="Поиск организаций по названию",
    description="Ищет организации по частичному совпадению названия.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def search_organizations_by_name(
    name: str = Query(..., min_length=1, description="Поисковый запрос по названию", examples=["Рога"]),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Поиск организаций по названию.

    Ищет организации, название которых содержит указанную строку (без учёта регистра).

    - **name**: поисковый запрос (минимум 1 символ)
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)
    """
    offset = (page - 1) * size
    search_pattern = f"%{name}%"

    count_result = await db.execute(
        select(func.count(Organization.id))
        .where(Organization.name.ilike(search_pattern))
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Organization)
        .where(Organization.name.ilike(search_pattern))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/by-building/{building_id}",
    response_model=OrganizationList,
    summary="Организации в здании",
    description="Возвращает список всех организаций, находящихся в указанном здании.",
    responses={
        **UNAUTHORIZED_RESPONSE,
        404: {
            "description": "Здание не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Здание с id=999 не найдено"}
                }
            },
        },
    },
)
async def get_organizations_by_building(
    building_id: int = Path(..., description="ID здания", ge=1, examples=[1]),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Получить список организаций в конкретном здании.

    - **building_id**: ID здания
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)

    Возвращает организации с информацией:
    - **id**: уникальный идентификатор
    - **name**: название организации
    - **phones**: список телефонов
    - **activities**: виды деятельности
    """
    # Проверяем существование здания
    building = await db.get(Building, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Здание с id={building_id} не найдено",
        )

    offset = (page - 1) * size

    # Получаем общее количество организаций в здании
    count_result = await db.execute(
        select(func.count(Organization.id)).where(
            Organization.building_id == building_id
        )
    )
    total = count_result.scalar() or 0

    # Получаем организации с телефонами и видами деятельности
    result = await db.execute(
        select(Organization)
        .where(Organization.building_id == building_id)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/by-activity/{activity_id}",
    response_model=OrganizationList,
    summary="Организации по виду деятельности",
    description="Возвращает список организаций, которые относятся к указанному виду деятельности.",
    responses={
        **UNAUTHORIZED_RESPONSE,
        404: {
            "description": "Вид деятельности не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Вид деятельности с id=999 не найден"}
                }
            },
        },
    },
)
async def get_organizations_by_activity(
    activity_id: int = Path(..., description="ID вида деятельности", ge=1, examples=[1]),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Получить список организаций по виду деятельности.

    - **activity_id**: ID вида деятельности
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)

    Возвращает организации с информацией:
    - **id**: уникальный идентификатор
    - **name**: название организации
    - **phones**: список телефонов
    - **activities**: виды деятельности
    """
    # Проверяем существование вида деятельности
    activity = await db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вид деятельности с id={activity_id} не найден",
        )

    offset = (page - 1) * size

    # Получаем общее количество организаций с этим видом деятельности
    count_result = await db.execute(
        select(func.count(func.distinct(Organization.id)))
        .select_from(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id == activity_id)  # type: ignore
    )
    total = count_result.scalar() or 0

    # Получаем организации
    result = await db.execute(
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id == activity_id)  # type: ignore
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().unique().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


async def get_activity_ids_by_name_with_children(
    db: AsyncSession, activity_name: str
) -> list[int]:
    """
    Найти виды деятельности по названию и получить их ID вместе с дочерними (до 3 уровней).
    """
    # Находим все виды деятельности с таким названием
    result = await db.execute(
        select(Activity.id, Activity.level).where(Activity.name.ilike(f"%{activity_name}%"))
    )
    found_activities = result.all()

    if not found_activities:
        return []

    all_ids: set[int] = set()

    for activity_id, level in found_activities:
        all_ids.add(activity_id)

        # Уровень 2: дочерние (если текущий уровень 1 или 2)
        if level <= 2:
            child_result = await db.execute(
                select(Activity.id).where(Activity.parent_id == literal(activity_id))
            )
            level2_ids = [row[0] for row in child_result.all()]
            all_ids.update(level2_ids)

            # Уровень 3: внуки (если текущий уровень 1)
            if level == 1 and level2_ids:
                grandchild_result = await db.execute(
                    select(Activity.id).where(Activity.parent_id.in_(level2_ids))
                )
                level3_ids = [row[0] for row in grandchild_result.all()]
                all_ids.update(level3_ids)

    return list(all_ids)


@router.get(
    "/search-by-activity",
    response_model=OrganizationList,
    summary="Поиск организаций по виду деятельности (с вложенными)",
    description="Ищет организации по названию вида деятельности, включая все вложенные виды деятельности.",
    responses={
        **UNAUTHORIZED_RESPONSE,
        404: {
            "description": "Вид деятельности не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Вид деятельности 'Космос' не найден"}
                }
            },
        },
    },
)
async def search_organizations_by_activity_tree(
    activity_name: str = Query(..., min_length=1, description="Название вида деятельности", examples=["Еда"]),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Поиск организаций по названию вида деятельности с учётом вложенных уровней.

    Например, при поиске по виду деятельности «Еда» (уровень 1) будут найдены
    все организации с видами деятельности: Еда, Мясная продукция, Молочная продукция,
    Сыры, Йогурты и т.д.

    - **activity_name**: название вида деятельности (поиск по частичному совпадению)
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)
    """
    # Получаем все ID: найденные + дочерние + внуки
    all_activity_ids = await get_activity_ids_by_name_with_children(db, activity_name)

    if not all_activity_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вид деятельности '{activity_name}' не найден",
        )

    offset = (page - 1) * size

    # Получаем общее количество организаций
    count_result = await db.execute(
        select(func.count(func.distinct(Organization.id)))
        .select_from(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(all_activity_ids))
    )
    total = count_result.scalar() or 0

    # Получаем организации
    result = await db.execute(
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(all_activity_ids))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .distinct()
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().unique().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


# Радиус Земли в метрах
EARTH_RADIUS_METERS = 6_371_000


@router.get(
    "/in-radius",
    response_model=OrganizationList,
    summary="Организации в радиусе",
    description="Возвращает список организаций, находящихся в заданном радиусе от указанной точки.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def get_organizations_in_radius(
    latitude: float = Query(
        ..., description="Широта центральной точки", ge=-90, le=90, examples=[55.753215]
    ),
    longitude: float = Query(
        ..., description="Долгота центральной точки", ge=-180, le=180, examples=[37.622504]
    ),
    radius: float = Query(
        ..., description="Радиус поиска в метрах", gt=0, le=50000, examples=[1000]
    ),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Получить список организаций в заданном радиусе от точки.

    Использует формулу Haversine для вычисления расстояния между точками на сфере.

    - **latitude**: широта центральной точки (-90 до 90)
    - **longitude**: долгота центральной точки (-180 до 180)
    - **radius**: радиус поиска в метрах (макс. 50 км)
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)
    """
    offset = (page - 1) * size

    # Формула Haversine для расчёта расстояния в метрах
    lat_rad = func.radians(latitude)
    lon_rad = func.radians(longitude)
    building_lat_rad = func.radians(Building.latitude)
    building_lon_rad = func.radians(Building.longitude)

    # Разница координат
    dlat = building_lat_rad - lat_rad
    dlon = building_lon_rad - lon_rad

    # Формула Haversine
    a = (
        func.power(func.sin(dlat / 2), 2)
        + func.cos(lat_rad) * func.cos(building_lat_rad) * func.power(func.sin(dlon / 2), 2)
    )
    distance = 2 * EARTH_RADIUS_METERS * func.asin(func.sqrt(a))

    # Получаем ID зданий в радиусе
    buildings_in_radius = (
        select(Building.id)
        .where(distance <= radius)
        .subquery()
    )

    # Получаем общее количество организаций
    count_result = await db.execute(
        select(func.count(Organization.id))
        .where(Organization.building_id.in_(select(buildings_in_radius.c.id)))
    )
    total = count_result.scalar() or 0

    # Получаем организации
    result = await db.execute(
        select(Organization)
        .where(Organization.building_id.in_(select(buildings_in_radius.c.id)))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/in-bbox",
    response_model=OrganizationList,
    summary="Организации в прямоугольной области",
    description="Возвращает список организаций, находящихся в прямоугольной области, заданной двумя точками.",
    responses={**UNAUTHORIZED_RESPONSE},
)
async def get_organizations_in_bbox(
    min_latitude: float = Query(
        ..., description="Широта юго-западной точки", ge=-90, le=90, examples=[55.73]
    ),
    min_longitude: float = Query(
        ..., description="Долгота юго-западной точки", ge=-180, le=180, examples=[37.58]
    ),
    max_latitude: float = Query(
        ..., description="Широта северо-восточной точки", ge=-90, le=90, examples=[55.78]
    ),
    max_longitude: float = Query(
        ..., description="Долгота северо-восточной точки", ge=-180, le=180, examples=[37.65]
    ),
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationList:
    """
    Получить список организаций в прямоугольной области (bounding box).

    Область задаётся двумя точками: юго-западной (min) и северо-восточной (max).

    - **min_latitude**: широта юго-западной точки
    - **min_longitude**: долгота юго-западной точки
    - **max_latitude**: широта северо-восточной точки
    - **max_longitude**: долгота северо-восточной точки
    - **page**: номер страницы (начиная с 1)
    - **size**: количество элементов на странице (1-100)
    """
    offset = (page - 1) * size

    # Получаем ID зданий в прямоугольнике
    buildings_in_bbox = (
        select(Building.id)
        .where(
            Building.latitude.between(min_latitude, max_latitude),
            Building.longitude.between(min_longitude, max_longitude),
        )
        .subquery()
    )

    # Получаем общее количество организаций
    count_result = await db.execute(
        select(func.count(Organization.id))
        .where(Organization.building_id.in_(select(buildings_in_bbox.c.id)))
    )
    total = count_result.scalar() or 0

    # Получаем организации
    result = await db.execute(
        select(Organization)
        .where(Organization.building_id.in_(select(buildings_in_bbox.c.id)))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .offset(offset)
        .limit(size)
        .order_by(Organization.id)
    )
    organizations = result.scalars().all()

    pages = math.ceil(total / size) if total > 0 else 0

    return OrganizationList(
        items=[OrganizationRead.model_validate(org) for org in organizations],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
    summary="Информация об организации",
    description="Возвращает полную информацию об организации по её ID.",
    responses={
        **UNAUTHORIZED_RESPONSE,
        404: {
            "description": "Организация не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Организация с id=999 не найдена"}
                }
            },
        },
    },
)
async def get_organization_by_id(
    organization_id: int = Path(..., description="ID организации", ge=1, examples=[1]),
    db: AsyncSession = Depends(get_db),
) -> OrganizationRead:
    """
    Получить информацию об организации по ID.

    - **organization_id**: ID организации

    Возвращает полную информацию:
    - **id**: уникальный идентификатор
    - **name**: название организации
    - **building_id**: ID здания
    - **phones**: список телефонов
    - **activities**: виды деятельности
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с id={organization_id} не найдена",
        )

    return OrganizationRead.model_validate(organization)