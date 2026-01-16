# OrgAtlas

Тестовое задание для компании Secunda.

Ссылка на вакансию: https://hh.ru/vacancy/129352952

## Быстрый запуск

1. Клонируйте репозиторий

```shell
git clone https://github.com/lavrocoder/OrgAtlas
```

2. Создайте файл `.env` на основе `.env.example`

```shell
cp .env.example .env
```

3. Запустите развёртывание через Docker-compose

```shell
docker-compose up -d --build
```

Админка будет доступна по ссылке http://127.0.0.1:8000/admin (без авторизации)

Её нет в ТЗ, но я добавил её для удобства. 

Её можно выключить в файле `.env`

Документация будет доступна по ссылкам:
1. http://127.0.0.1:8000/redoc
2. http://127.0.0.1:8000/docs

Используйте ключ для авторизации указанный в `.env`.

Swagger UI поддерживает авторизации. Но в своих запросах вам нужно передавать заголовок `X-API-Key`

Автоматически:
1. Проведутся миграции
2. Заполнятся тестовые данные

## Эндпоинты
1. Список всех организаций находящихся в конкретном здании.
   - GET /api/v1/organizations/by-building/{building_id}
2. Список всех организаций, которые относятся к указанному виду деятельности
   - GET /api/v1/organizations/by-activity/{activity_id}
3. Список организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте. 
   - GET /api/v1/organizations/in-radius
   - GET /api/v1/organizations/in-bbox
4. Список зданий
   - GET /api/v1/buildings
5. вывод информации об организации по её идентификатору
   - GET /api/v1/organizations
   - GET /api/v1/organizations/{organization_id}
6. искать организации по виду деятельности. Например, поиск по виду деятельности «Еда», которая находится на первом уровне дерева, и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри. Т.е. в результатах поиска должны отобразиться организации с видом деятельности Еда, Мясная продукция, Молочная продукция.
   - GET /api/v1/organizations/search-by-activity
7. поиск организации по названию
   - GET /api/v1/organizations/search


## Полезные команды во время разработки
- `alembic init app/alembic` - Инициализирует alembic
- `docker run -d --name orgatlas_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=orgatlas -p 5432:5432 postgres:16-alpine` - Создаёт БД для разработки
- `alembic revision --autogenerate -m "Initial tables"` - Создаёт миграцию
- `alembic upgrade head` - Проводит миграцию
- `uvicorn app.main:app --reload` - Запуск сайта
