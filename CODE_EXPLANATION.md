# Codebase Explanation

This document provides an overview of the "Santhe Platform" codebase, explaining its structure, key components, and workflows.

## Project Overview

The project aims to set up the infrastructure and services for the Santhe platform, a system connecting farmers and middlemen. It involves provisioning AWS resources using Terraform and deploying a set of microservices.

## Directory Structure

### `infrastructure/`

This directory contains the Infrastructure as Code (IaC) definitions using Terraform. It provisions AWS resources necessary for the platform.

- **`main.tf`**: The entry point for the Terraform configuration. It calls various modules to set up the VPC, EKS cluster, ECR, PostgreSQL, and Bastion host.
- **`modules/`**: Contains reusable Terraform modules for specific resources (e.g., `vpc`, `eks`, `route53`).
- **`deploy.sh`**: A shell script to automate the deployment process across different environments (sbx, prd, etc.) and regions.
- **`variables.tf`**: Defines input variables for the Terraform configuration.

### `services/`

This directory houses the source code for the platform's microservices. Each service is self-contained with its own `src`, `tests`, `config`, and `Dockerfile`.

Examples of services include:
- `user-service`
- `product-catalog-service`
- `order-management-service`
- `payment-service`

### `docs/`

Contains documentation for the project.
- **`features.md`**: Lists the features and responsibilities of each microservice.

### Root Files

- **`structure.sh`**: A utility script to generate the directory structure for new microservices. It creates standard folders (`src`, `tests`) and files (`main.py`, `Dockerfile`) for a predefined list of services.
- **`Jenkinsfile`**: Defines the CI/CD pipeline using Jenkins. It includes stages for linting, building, testing, static code analysis, packaging, and publishing Docker images.
- **`README.md`**: The main entry point for developers, explaining prerequisites and usage.

## Workflows

### Infrastructure Deployment

1.  Navigate to the `infrastructure` directory.
2.  Use `deploy.sh` to initialize and apply Terraform configurations for a specific environment and region.
    ```bash
    ./deploy.sh
    ```

### Service Generation

To scaffold the microservices structure:
1.  Run the `structure.sh` script from the root directory.
    ```bash
    ./structure.sh
    ```

### CI/CD Pipeline

The `Jenkinsfile` orchestrates the build and deployment process. It:
1.  Determines the version based on git tags and commit messages.
2.  Runs linting and tests inside Docker containers.
3.  Builds production Docker images.
4.  Publishes images and tags the release on successful builds (for main/develop branches).

## Note on Recent Changes

- The `infrastructure/modules/rote53` directory was renamed to `infrastructure/modules/route53` to fix a typo.
