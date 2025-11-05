FROM python:3.11-slim

WORKDIR /app

# зависимости
COPY ../lab1/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../lab1/pipeline.sh ../lab1/*.py .

# Даем права на выполнение
RUN chmod +x pipeline.sh

CMD ["./pipeline.sh"]