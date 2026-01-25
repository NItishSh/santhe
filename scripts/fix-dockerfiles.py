import os

services_dir = "services"
dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

fixed_count = 0

for service in os.listdir(services_dir):
    service_path = os.path.join(services_dir, service)
    if os.path.isdir(service_path):
        dockerfile_path = os.path.join(service_path, "Dockerfile")
        
        # Check if file exists and is empty, or doesn't exist
        should_write = False
        if not os.path.exists(dockerfile_path):
            should_write = True
        else:
            if os.path.getsize(dockerfile_path) == 0:
                should_write = True
        
        if should_write:
            print(f"fixing Dockerfile for {service}")
            with open(dockerfile_path, "w") as f:
                f.write(dockerfile_content)
            fixed_count += 1
        else:
            print(f"Skipping {service}, Dockerfile exists and is not empty.")

print(f"Fixed {fixed_count} Dockerfiles.")
