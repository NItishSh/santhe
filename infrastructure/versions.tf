terraform {
  required_version = ">= 1.9.0"

  backend "s3" {
    bucket         = "santhe-terraform-state" # Ensure this bucket exists
    key            = "santhe/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "santhe-terraform-locks" # Ensure this table exists
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}
