FROM python:3.14-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt ./
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY pytest.ini ./
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
