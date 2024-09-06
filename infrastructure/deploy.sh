#!/bin/bash
set -eou pipefail

# Define valid environments and regions
valid_environments=("sbx" "prd" "qa" "uat" "pre-prd")
valid_regions=("ap-south-2" "ap-south-1" )

# Function to validate input
validate_input() {
  local input="$1"
  local valid_list=("${!2}")
  if [[ ! " ${valid_list[@]} " =~ " ${input} " ]]; then
    echo "Invalid input: ${input}. Valid options are: ${valid_list[*]}"
    exit 1
  fi
}

# Prompt for environment and region
read -p "Enter the environment (e.g., sbx, prd): " environment
validate_input "$environment" valid_environments[@]

read -p "Enter the region (e.g., ap-south-1, ap-south-2): " region
validate_input "$region" valid_regions[@]

# Define the workspace name and .tfvars file
workspace="${environment}-${region}"
tfvars_file="${workspace}.tfvars"

# Initialize Terraform
terraform init

# Check if the workspace exists, if not create it
if terraform workspace list | grep -q "^${workspace}$"; then
  echo "Workspace ${workspace} already exists. Selecting it."
else
  terraform workspace new "$workspace"
fi
terraform workspace select "$workspace"

# Check if the .tfvars file exists
if [ ! -f "$tfvars_file" ]; then
  echo "Error: The file $tfvars_file does not exist. Please create it before proceeding."
  exit 1
fi

# Optionally plan
read -p "Do you want to run 'terraform plan'? (y/n): " plan_option
if [[ "$plan_option" =~ ^[Yy]$ ]]; then
  terraform plan -var-file="$tfvars_file"
fi

# Apply Terraform configuration
# terraform apply -var-file="$tfvars_file"