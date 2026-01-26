# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run tests (Build fails if tests fail)
ENV PYTHONPATH=.
ENV DATABASE_URL="sqlite:///:memory:"
ENV SECRET_KEY="test_secret"
RUN pytest

# Stage 2: Runtime
FROM python:3.11-slim

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
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
