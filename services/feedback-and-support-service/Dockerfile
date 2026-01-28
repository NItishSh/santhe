# Stage 1: Builder
FROM python:3.13-slim-bookworm AS builder
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt
COPY . .

# Run tests (Build fails if tests fail)
ENV PYTHONPATH=.
ENV DATABASE_URL="sqlite:///:memory:"
RUN SECRET_KEY="test_secret" pytest


# Stage: Lint
FROM builder AS lint
RUN ruff check .

# Stage 2: Runtime
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app code
COPY src/ src/
COPY migrations/ migrations/
COPY alembic.ini .
COPY config/ config/

# Change ownership
RUN chown -R appuser:appgroup /app
USER 1001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
