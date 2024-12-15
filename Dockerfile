FROM python:3.13-alpine AS base

WORKDIR /app

# Install system dependencies (ffmpeg and libopus)
RUN apk add --no-cache \
    ffmpeg \
    opus \
    opus-dev \
    build-base  # Required for pip package compilation

RUN pip install --no-cache-dir uv==0.5.4

COPY pyproject.toml pyproject.toml
RUN uv pip install -r pyproject.toml --no-cache-dir --system

COPY config/ config/
COPY src/ src/
COPY main.py main.py

CMD ["uv", "run", "python3", "-m", "main"]