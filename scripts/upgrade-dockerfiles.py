import os

services_dir = "services"

fixed_count = 0

for service in os.listdir(services_dir):
    service_path = os.path.join(services_dir, service)
    if os.path.isdir(service_path):
        dockerfile_path = os.path.join(service_path, "Dockerfile")
        
        if os.path.exists(dockerfile_path):
            with open(dockerfile_path, "r") as f:
                content = f.read()
            
            if "FROM python:3.9-slim" in content:
                print(f"Upgrading Dockerfile for {service} to Python 3.11")
                new_content = content.replace("FROM python:3.9-slim", "FROM python:3.11-slim")
                with open(dockerfile_path, "w") as f:
                    f.write(new_content)
                fixed_count += 1

print(f"Upgraded {fixed_count} Dockerfiles to Python 3.11.")
