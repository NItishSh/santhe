import os

SERVICES_DIR = "services"

DOCKERIGNORE_CONTENT = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.git
.gitignore
.pytest_cache/
.coverage
htmlcov/
tests/
"""

DOCKERFILE_TEMPLATE = """# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
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
RUN addgroup --system --gid 1001 appgroup && \\
    adduser --system --uid 1001 --gid 1001 appuser
WORKDIR /app
# Copy installed dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
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
"""

def apply_hardening():
    if not os.path.exists(SERVICES_DIR):
        print(f"Directory {SERVICES_DIR} not found.")
        return

    services = [d for d in os.listdir(SERVICES_DIR) if os.path.isdir(os.path.join(SERVICES_DIR, d))]
    
    for service in services:
        service_path = os.path.join(SERVICES_DIR, service)
        print(f"Processing {service}...")

        # 1. Create .dockerignore
        dockerignore_path = os.path.join(service_path, ".dockerignore")
        with open(dockerignore_path, "w") as f:
            f.write(DOCKERIGNORE_CONTENT)
        print(f"  - Created .dockerignore")

        # 2. Update Dockerfile
        dockerfile_path = os.path.join(service_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(DOCKERFILE_TEMPLATE)
        print(f"  - Updated Dockerfile")

if __name__ == "__main__":
    apply_hardening()
