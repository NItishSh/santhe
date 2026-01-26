import os

def upgrade_dockerfile_timeout(path):
    if not os.path.exists(path):
        return

    with open(path, 'r') as f:
        content = f.read()

    # Target the standard pip install command we use
    target = "RUN pip install --no-cache-dir -r requirements.txt"
    replacement = "RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt"

    if target in content:
        new_content = content.replace(target, replacement)
        print(f"Upgrading timeout in {path}")
        with open(path, 'w') as f:
            f.write(new_content)
    # Also handle the case where it might already be modified or slightly different spacing?
    # For now, strict replacement is safer than regex unless we need flexibility.
    # The previous scripts ensured a standard format.

def main():
    services_dir = "services"
    for service_name in os.listdir(services_dir):
        service_path = os.path.join(services_dir, service_name)
        if os.path.isdir(service_path):
            dockerfile_path = os.path.join(service_path, "Dockerfile")
            upgrade_dockerfile_timeout(dockerfile_path)

if __name__ == "__main__":
    main()
