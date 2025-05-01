FROM python:3.12-alpine AS builder

LABEL org.opencontainers.image.authors="konevsov.connect@gmail.com"

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.8.3

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-dev


FROM python:3.12-alpine AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./src .

RUN chmod +x prestart.sh

EXPOSE 8002

ENTRYPOINT ["./prestart.sh"]
ENTRYPOINT ["python", "main.py"]
