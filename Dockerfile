FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv pip install --system --no-cache -r pyproject.toml && \
    uv pip install --system --no-cache pytest

COPY src/ ./src/
COPY tests/ ./tests/

CMD ["python3", "-m", "src.main"]
