FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY pyproject.toml ./

# Устанавливаем pip и зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Копируем исходный код
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
