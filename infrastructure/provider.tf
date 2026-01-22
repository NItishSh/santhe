terraform {
  required_version = ">= 1.0"

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
      version = "2.15.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.32.0"
    }
  }
}
provider "aws" {
  region = var.region
  assume_role {
    role_arn = var.assume_role_arn
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}
