# Santhe Platform Infrastructure

This project sets up the infrastructure for the Santhe platform, connecting farmers directly with middlemen for agricultural product sales. The infrastructure is designed using Terraform to provision AWS resources, including VPCs, subnets, and an EKS cluster, ensuring compliance with GDPR, CIS, and PCI standards.

## Project Structure

- **VPC and Subnets**: Configured using the Terraform AWS VPC module
- **EKS Cluster**: Managed using the Terraform AWS EKS module
- **Route 53**: Configured for domain management
- **Encryption and Security**: Ensured through AWS services and best practices

## Prerequisites

- Terraform (version 1.0 or later): https://www.terraform.io/downloads.html
- AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
- An AWS account with appropriate permissions

## Configuration

### Variables

| Variable | Description |
|----------|-------------|
| `region` | AWS region for deploying resources |
| `environment` | Environment name/id (`sbx`, `qa`, `uat`, `pre-prd`, `prd`) |
| `vpc_cidr` | CIDR block for the VPC (defined in each environment-specific `.tfvars` file) |

### Workspaces

The project utilizes Terraform workspaces to manage different environments and regions. To create and switch between workspaces:

example:
```
terraform workspace new sbx-us-west-2 
terraform workspace select sbx-us-west-2
```

### CIDR Allocation

CIDR blocks are allocated per environment, with specific ranges reserved for sbx (20%) and prd (80%). Refer to the internal documentation or configuration files for detailed information on CIDR allocation and block splitting.

## Usage

1. Clone the Repository:
```
git clone <repository-url> 
cd <repository-directory>
```

2. Initialize Terraform:
```
terraform init
```


3. Create and Select Workspaces:
```
terraform workspace new <workspace-name> 
terraform workspace select <workspace-name>
```


4. Apply Configuration:
```
terraform apply -var-file="variables.<workspace-name>.tfvars"
```


## Documentation

- Terraform AWS VPC Module: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
- Terraform AWS EKS Module: https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest
- AWS Route 53: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html

## Local Development (Kubernetes & Microservices)

This section details how to run the full Santhe platform locally using Kind (Kubernetes in Docker).

### Prerequisites
- **Docker Desktop** (or Colima/Rancher Desktop)
- **Kind**: `brew install kind`
- **Kubectl**: `brew install kubectl`
- **Helm**: `brew install helm`

### Quick Start
To spin up the entire environment (Cluster + Istio + Postgres + 11 Microservices + Frontend):

```bash
chmod +x scripts/*.sh
./scripts/setup-local.sh
```

This script will:
1. Create a Kind cluster (`santhe-local`).
2. Install **Istio** (Service Mesh) and **PostgreSQL**.
3. Build all microservices and the web frontend.
4. Deploy them to the cluster with auto-configured DB connections.

### Accessing the Application
- **Frontend**: http://localhost:8080
- **API Gateway**: http://localhost:8080/api (via Next.js rewriting to Ingress)

### Managing Services
To update a specific service (rebuild image + redeploy + run migrations):

```bash
./scripts/deploy-service.sh <service-name>
# Example:
./scripts/deploy-service.sh user-service
```

### Database & Migrations
Each microservice has its own logical database in the shared Postgres instance. Schema changes are managed via **Alembic**.

#### Migration Workflow
1. **Modify Models**: Edit `src/models.py` in the service.
2. **Generate Migration**: Run the helper script to generate the migration file based on the difference between your models and the running DB.
   ```bash
   ./scripts/generate-migrations.sh <service-name>
   # Example:
   ./scripts/generate-migrations.sh user-service
   ```
   *This command runs inside the pod to ensure environment consistency and copies the new migration file to your local `services/<svc>/migrations/versions` folder.*

3. **Review & Commit**: Check the generated file in `services/<svc>/migrations/versions/`.
4. **Deploy**:
   ```bash
   ./scripts/deploy-service.sh <service-name>
   ```
   *The deployment process triggers a Helm Hook that runs `alembic upgrade head` BEFORE the new application pods start.*

### Cleanup
To destroy the local cluster and free up resources:

```bash
./scripts/destroy-local.sh
```


## Contributing

Contributions are welcome! To contribute to this project:

1. Fork the Repository: Click the “Fork” button at the top right of the repository page.

2. Create a Feature Branch:
```git checkout -b feature/my-new-feature```

3. Make Changes and Commit:
```git commit -am 'Add new feature'```

4. Push to the Branch:
```git push origin feature/my-new-feature```

5. Submit a Pull Request: Go to the original repository and submit a pull request with your changes.

Please ensure your contributions adhere to the project’s coding standards and guidelines.
