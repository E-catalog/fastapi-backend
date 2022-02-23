FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev

COPY fastapi-backend /app/fastapi-backend

CMD [ "uvicorn", "--factory", "backend.app:app", "--host 0.0.0.0", "--port 8000"]
