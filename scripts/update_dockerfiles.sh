#!/bin/bash
set -e

for svc in services/*; do
  if [ -d "$svc" ]; then
    echo "Processing $svc..."
    
    cat <<EOF > "$svc/Dockerfile"
# Stage 1: Build and Test
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables for testing
ENV PYTHONPATH=.
ENV DATABASE_URL="sqlite:///:memory:"
ENV SECRET_KEY="test_secret"

# Run tests
RUN pytest

# Stage 2: Final Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application artifacts from builder
COPY --from=builder /app/src /app/src
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/alembic.ini /app/alembic.ini
EOF

    # Copy config if exists in builder context (safer to assume it does if service needs it, but we can verify in context of stage 2 construction? No, stage 2 is fresh. We copy from builder /app/config.)
    # The simplest logic is: if $svc/config exists locally (which corresponds to /app/config in builder), then we add the COPY instruction from builder.
    
    if [ -d "$svc/config" ]; then
      echo "COPY --from=builder /app/config /app/config" >> "$svc/Dockerfile"
    fi
    
    cat <<EOF >> "$svc/Dockerfile"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

  fi
done
