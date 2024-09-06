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
