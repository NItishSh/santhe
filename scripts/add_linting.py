import os

def upgrade_python_service(service_dir):
    # 1. Add ruff to requirements.txt
    req_path = os.path.join(service_dir, "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r") as f:
            reqs = f.read()
        if "ruff" not in reqs:
            print(f"Adding ruff to {req_path}")
            with open(req_path, "a") as f:
                f.write("\nruff\n")
    
    # 2. Add lint stage to Dockerfile
    docker_path = os.path.join(service_dir, "Dockerfile")
    if os.path.exists(docker_path):
        with open(docker_path, "r") as f:
            content = f.read()
        
        # Check if lint stage already exists
        if "AS lint" in content:
            print(f"Lint stage already exists in {docker_path}")
            return

        # Find insertion point: After 'AS builder' block and before next 'FROM'
        # We look for the start of the Runtime stage
        if "# Stage 2: Runtime" in content:
             # Standard pattern we've seen
            insertion_point = content.find("# Stage 2: Runtime")
            
            lint_stage = """
# Stage: Lint
FROM builder AS lint
RUN pip install ruff
RUN ruff check .

"""
            new_content = content[:insertion_point] + lint_stage + content[insertion_point:]
            
            print(f"Adding lint stage to {docker_path}")
            with open(docker_path, "w") as f:
                f.write(new_content)
        else:
            print(f"Could not find '# Stage 2: Runtime' marker in {docker_path}, skipping Dockerfile update.")

def main():
    services_dir = "services"
    for service in os.listdir(services_dir):
        service_path = os.path.join(services_dir, service)
        if os.path.isdir(service_path):
            upgrade_python_service(service_path)

if __name__ == "__main__":
    main()
