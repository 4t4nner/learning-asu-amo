# Базовый образ Python для задач машинного обучения
FROM python:3.11-slim

ARG USER_ID=1000
ARG GROUP_ID=1000

# Создаём группу и пользователя с указанными UID/GID
RUN addgroup --gid $GROUP_ID mluser && \
    adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID mluser

# Установка рабочей директории
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R mluser:mluser /app

USER mluser


# Копирование исходного кода
# COPY . .

# Команда для запуска приложения
# CMD ["python", "train_model.py"]