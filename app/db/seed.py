"""Скрипт для заполнения БД тестовыми данными."""

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, OrganizationPhone, organization_activity


async def seed_database() -> None:
    """Заполняет БД тестовыми данными."""
    async with async_session_maker() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(text("SELECT COUNT(*) FROM buildings"))
        if result.scalar() > 0:
            print("База данных уже содержит данные. Пропускаем заполнение.")
            return

        await seed_activities(session)
        await seed_buildings(session)
        await seed_organizations(session)
        await session.commit()
        print("База данных успешно заполнена тестовыми данными!")


async def seed_activities(session: AsyncSession) -> None:
    """Создаёт виды деятельности (3 уровня вложенности)."""
    activities_data = [
        # Уровень 1
        {"id": 1, "name": "Еда", "parent_id": None, "level": 1},
        {"id": 2, "name": "Автомобили", "parent_id": None, "level": 1},
        {"id": 3, "name": "Строительство", "parent_id": None, "level": 1},
        {"id": 4, "name": "IT-услуги", "parent_id": None, "level": 1},
        # Уровень 2 - Еда
        {"id": 5, "name": "Мясная продукция", "parent_id": 1, "level": 2},
        {"id": 6, "name": "Молочная продукция", "parent_id": 1, "level": 2},
        {"id": 7, "name": "Кондитерские изделия", "parent_id": 1, "level": 2},
        # Уровень 2 - Автомобили
        {"id": 8, "name": "Легковые", "parent_id": 2, "level": 2},
        {"id": 9, "name": "Грузовые", "parent_id": 2, "level": 2},
        # Уровень 2 - Строительство
        {"id": 10, "name": "Жилое строительство", "parent_id": 3, "level": 2},
        {"id": 11, "name": "Коммерческое строительство", "parent_id": 3, "level": 2},
        # Уровень 2 - IT
        {"id": 12, "name": "Разработка ПО", "parent_id": 4, "level": 2},
        {"id": 13, "name": "Системное администрирование", "parent_id": 4, "level": 2},
        # Уровень 3 - Легковые автомобили
        {"id": 14, "name": "Запчасти", "parent_id": 8, "level": 3},
        {"id": 15, "name": "Аксессуары", "parent_id": 8, "level": 3},
        {"id": 16, "name": "Автосервис", "parent_id": 8, "level": 3},
        # Уровень 3 - Молочная продукция
        {"id": 17, "name": "Сыры", "parent_id": 6, "level": 3},
        {"id": 18, "name": "Йогурты", "parent_id": 6, "level": 3},
        # Уровень 3 - Разработка ПО
        {"id": 19, "name": "Веб-разработка", "parent_id": 12, "level": 3},
        {"id": 20, "name": "Мобильная разработка", "parent_id": 12, "level": 3},
    ]

    for data in activities_data:
        session.add(Activity(**data))
    await session.flush()
    print(f"Создано {len(activities_data)} видов деятельности")


async def seed_buildings(session: AsyncSession) -> None:
    """Создаёт здания с координатами в Москве."""
    buildings_data = [
        {
            "id": 1,
            "address": "г. Москва, ул. Ленина, д. 1",
            "latitude": 55.753215,
            "longitude": 37.622504,
        },
        {
            "id": 2,
            "address": "г. Москва, ул. Тверская, д. 15",
            "latitude": 55.764012,
            "longitude": 37.605126,
        },
        {
            "id": 3,
            "address": "г. Москва, Кутузовский проспект, д. 32",
            "latitude": 55.740193,
            "longitude": 37.534592,
        },
        {
            "id": 4,
            "address": "г. Москва, ул. Арбат, д. 10",
            "latitude": 55.752023,
            "longitude": 37.591494,
        },
        {
            "id": 5,
            "address": "г. Москва, Садовое кольцо, д. 5",
            "latitude": 55.767220,
            "longitude": 37.638572,
        },
        {
            "id": 6,
            "address": "г. Москва, ул. Новый Арбат, д. 21",
            "latitude": 55.752834,
            "longitude": 37.583192,
        },
        {
            "id": 7,
            "address": "г. Москва, Проспект Мира, д. 45",
            "latitude": 55.784512,
            "longitude": 37.633841,
        },
        {
            "id": 8,
            "address": "г. Москва, ул. Большая Якиманка, д. 22",
            "latitude": 55.735123,
            "longitude": 37.614782,
        },
    ]

    for data in buildings_data:
        session.add(Building(**data))
    await session.flush()
    print(f"Создано {len(buildings_data)} зданий")


async def seed_organizations(session: AsyncSession) -> None:
    """Создаёт организации с телефонами и видами деятельности."""
    # Получаем все activities для связывания
    organizations_data = [
        {
            "name": 'ООО "Рога и Копыта"',
            "building_id": 1,
            "phones": ["2-222-222", "3-333-333"],
            "activity_ids": [1, 5],  # Еда, Мясная продукция
        },
        {
            "name": 'ЗАО "Молочный рай"',
            "building_id": 1,
            "phones": ["4-444-444"],
            "activity_ids": [6, 17],  # Молочная продукция, Сыры
        },
        {
            "name": 'ООО "АвтоМир"',
            "building_id": 2,
            "phones": ["5-555-555", "8-800-555-35-35"],
            "activity_ids": [2, 8, 14],  # Автомобили, Легковые, Запчасти
        },
        {
            "name": 'ИП Петров "Автосервис"',
            "building_id": 2,
            "phones": ["6-666-666"],
            "activity_ids": [2, 8, 16],  # Автомобили, Легковые, Автосервис
        },
        {
            "name": 'ООО "СтройГрад"',
            "building_id": 3,
            "phones": ["7-777-777", "7-777-778"],
            "activity_ids": [3, 10],  # Строительство, Жилое строительство
        },
        {
            "name": 'АО "Бизнес-Строй"',
            "building_id": 3,
            "phones": ["8-888-888"],
            "activity_ids": [3, 11],  # Строительство, Коммерческое строительство
        },
        {
            "name": 'ООО "ТехноСофт"',
            "building_id": 4,
            "phones": ["+7-495-123-45-67"],
            "activity_ids": [4, 12, 19],  # IT-услуги, Разработка ПО, Веб-разработка
        },
        {
            "name": 'ИП Сидоров "Мобильные решения"',
            "building_id": 4,
            "phones": ["+7-495-987-65-43"],
            "activity_ids": [4, 12, 20],  # IT-услуги, Разработка ПО, Мобильная разработка
        },
        {
            "name": 'ООО "Сладкий мир"',
            "building_id": 5,
            "phones": ["9-999-999"],
            "activity_ids": [1, 7],  # Еда, Кондитерские изделия
        },
        {
            "name": 'ЗАО "ГрузовикСервис"',
            "building_id": 5,
            "phones": ["1-111-111", "1-111-112"],
            "activity_ids": [2, 9],  # Автомобили, Грузовые
        },
        {
            "name": 'ООО "Йогурт-Экспресс"',
            "building_id": 6,
            "phones": ["+7-499-111-22-33"],
            "activity_ids": [1, 6, 18],  # Еда, Молочная продукция, Йогурты
        },
        {
            "name": 'ООО "Админ-Про"',
            "building_id": 7,
            "phones": ["+7-495-222-33-44"],
            "activity_ids": [4, 13],  # IT-услуги, Системное администрирование
        },
        {
            "name": 'ООО "АвтоАксессуары+"',
            "building_id": 7,
            "phones": ["+7-495-333-44-55"],
            "activity_ids": [2, 8, 15],  # Автомобили, Легковые, Аксессуары
        },
        {
            "name": 'ИП Иванов "Мясной дом"',
            "building_id": 8,
            "phones": ["2-222-333"],
            "activity_ids": [1, 5],  # Еда, Мясная продукция
        },
        {
            "name": 'ООО "Полный цикл"',
            "building_id": 8,
            "phones": ["+7-495-444-55-66", "+7-495-444-55-67"],
            "activity_ids": [3, 4, 10, 12],  # Строительство, IT, Жилое, Разработка
        },
    ]

    for org_data in organizations_data:
        # Создаём организацию
        org = Organization(
            name=org_data["name"],
            building_id=org_data["building_id"],
        )
        session.add(org)
        await session.flush()

        # Добавляем телефоны
        for phone in org_data["phones"]:
            session.add(OrganizationPhone(phone=phone, organization_id=org.id))

        # Связываем с видами деятельности через связующую таблицу
        for activity_id in org_data["activity_ids"]:
            await session.execute(
                organization_activity.insert().values(
                    organization_id=org.id,
                    activity_id=activity_id,
                )
            )

    await session.flush()
    print(f"Создано {len(organizations_data)} организаций")


if __name__ == "__main__":
    asyncio.run(seed_database())
