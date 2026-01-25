import os

services_dir = "services"
dependency = "pydantic-settings"

fixed_count = 0

for service in os.listdir(services_dir):
    service_path = os.path.join(services_dir, service)
    if os.path.isdir(service_path):
        req_path = os.path.join(service_path, "requirements.txt")
        
        if os.path.exists(req_path):
            with open(req_path, "r") as f:
                content = f.read()
            
            if dependency not in content:
                print(f"Adding {dependency} to {service}")
                with open(req_path, "a") as f:
                    if not content.endswith("\n") and content.strip():
                        f.write("\n")
                    f.write(f"{dependency}\n")
                fixed_count += 1
            else:
                print(f"{dependency} already in {service}")

print(f"Updated {fixed_count} requirements.txt files.")
