FROM python:3.14

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Copy dependency files
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

# Install dependencies with cache mount (no bind mounts)
RUN --mount=type=cache,id=s/cbb42f24-bd0b-40e5-946f-8becad8a1a75-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./scripts /app/scripts

COPY ./app /app/app

# Sync the project with cache mount
RUN --mount=type=cache,id=s/cbb42f24-bd0b-40e5-946f-8becad8a1a75-/root/.cache/uv,target=/root/.cache/uv \
    uv sync

# Make scripts executable
RUN chmod +x /app/scripts/prestart.sh

# Run migrations and start server
CMD ["sh", "-c", "bash scripts/prestart.sh && fastapi run --workers 4 app/main.py"]
