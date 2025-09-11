FROM ghcr.io/astral-sh/uv:0.8.17-python3.12-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    PYTHONUNBUFFERED=1
    
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

RUN rm -rf /root/.cache

FROM ghcr.io/astral-sh/uv:0.8.17-python3.12-alpine AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app /app

CMD ["uv", "run", "test_api", "--host", "0.0.0.0", "--port", "8000"]