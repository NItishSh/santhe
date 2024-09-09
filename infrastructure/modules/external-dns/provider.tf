terraform {
  required_version = "1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "2.15.0"
    }
    external = {
      source = "hashicorp/external"
      version = "2.3.3"
    }
  }
}
