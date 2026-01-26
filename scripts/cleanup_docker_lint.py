import os

def cleanup_dockerfile(path):
    if not os.path.exists(path):
        return

    with open(path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    for line in lines:
        if line.strip() == "RUN pip install ruff":
            changed = True
            continue # Skip this line
        new_lines.append(line)

    if changed:
        print(f"Cleaning redundant install in {path}")
        with open(path, 'w') as f:
            f.writelines(new_lines)

def main():
    services_dir = "services"
    for service_name in os.listdir(services_dir):
        service_path = os.path.join(services_dir, service_name)
        if os.path.isdir(service_path):
            dockerfile_path = os.path.join(service_path, "Dockerfile")
            cleanup_dockerfile(dockerfile_path)

if __name__ == "__main__":
    main()
