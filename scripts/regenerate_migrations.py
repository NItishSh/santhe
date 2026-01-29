import os
import subprocess
import sys
import shutil

SERVICES = [
    "user-service",
    "cart-management-service",
    "product-catalog-service",
    "order-management-service",
    "payment-service",
    "pricing-service",
    "notification-service",
    "logistics-management-service",
    "feedback-and-support-service",
    "compliance-and-audit-service",
    "analytics-and-reporting-service",
    "review-and-rating-service"
]

def run_cmd(cmd, cwd=None, env=None):
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd, env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        # Continue mostly, or exit?
        # For bulk ops, maybe print error and continue
        pass

def main():
    base_dir = os.getcwd()
    venv_dir = os.path.join(base_dir, "temp_migration_venv")
    
    # 1. Setup Venv
    if not os.path.exists(venv_dir):
        print("🔨 Creating venv...")
        run_cmd(f"python3 -m venv {venv_dir}")
    
    # Pip path
    pip = os.path.join(venv_dir, "bin", "pip")
    alembic = os.path.join(venv_dir, "bin", "alembic")
    
    # Install base deps (shared across most)
    print("📦 Installing base dependencies...")
    run_cmd(f"{pip} install alembic sqlalchemy psycopg pydantic pydantic-settings fastapi uvicorn")

    # 2. Iterate Services
    for service in SERVICES:
        print(f"\n--------------------------------------------------")
        print(f"🛠  Processing {service}...")
        service_dir = os.path.join(base_dir, "services", service)
        
        # Install service specifics (requirements.txt)
        req_file = os.path.join(service_dir, "requirements.txt")
        if os.path.exists(req_file):
            print(f"📥 Installing requirements for {service}...")
            # We filter out some conflicting or unnecessary ones if needed, but for now try direct install
            run_cmd(f"{pip} install -r requirements.txt", cwd=service_dir)
            
        # Clean old versions
        versions_dir = os.path.join(service_dir, "migrations", "versions")
        if os.path.exists(versions_dir):
            print(f"🧹 Use 'rm' to clean {versions_dir}/*.py")
            run_cmd(f"rm -f {versions_dir}/*.py")
        
        # DB Connection String
        db_name = service.replace("-", "_") + "_db"
        # We assume postgres is forwarded to localhost:5432
        db_url = f"postgresql+psycopg://postgres:postgres@localhost:5432/{db_name}"
        
        # Environment
        env = os.environ.copy()
        env["DATABASE_URL"] = db_url
        env["PYTHONPATH"] = service_dir # Ensure src is importable
        
        # Run Alembic
        # We need to run it from the service directory so alembic.ini is found
        print(f"🔄 Generating migration for {service}...")
        run_cmd(f"{alembic} revision --autogenerate -m 'initial_schema'", cwd=service_dir, env=env)
        
    print("\n✅ All migrations regenerated locally.")

if __name__ == "__main__":
    main()
