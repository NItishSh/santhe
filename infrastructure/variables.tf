variable "region" {
  type        = string
  description = "AWS region."
}
variable "environment" {
  description = "Environment name/id"
  type        = string

  validation {
    condition = contains([
      "sbx",
      "qa",
      "uat",
      "pre-prd",
      "prd"
    ], var.environment)

    error_message = "Allowed values for environment are 'sbx','qa','uat','pre-prd','prd'"
  }
}
variable "vpc_cidr" {
  type        = string
  description = "VPC cidr block"
}
variable "assume_role_arn" {
  type        = string
  description = "IAM role to assume for resource creation"
  # default     = "arn:aws:iam::123456789100:role/my-github-actions-role"
}
variable "db_config" {
  description = "Configuration for the PostgreSQL database"
  type = object({
    engine                = string
    engine_version        = string
    family                = string
    major_engine_version  = string
    instance_class        = string
    allocated_storage     = number
    max_allocated_storage = number
    db_name               = string
    username              = string
  })
  default = null
}
variable "product" {
  type    = string
  default = "santhe"
}

variable "issuer_email" {
  description = "Email address for ACME issuer"
  type        = string
  default     = "csnitish@gmail.com" # Fixed typo from gmial.com
}

variable "eks_instance_types" {
  description = "List of instance types for the EKS managed node group"
  type        = list(string)
  default     = ["t3.medium", "t3.large"]
}

variable "bastion_instance_type" {
  description = "Instance type for the bastion host"
  type        = string
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "Instance class for the RDS database"
  type        = string
  default     = "db.t4g.large"
}

variable "db_allocated_storage" {
  description = "Allocated storage for the RDS database (in GB)"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Name of the RDS database"
  type        = string
  default     = "santhe"
}

variable "db_username" {
  description = "Username for the RDS database"
  type        = string
  default     = "santhe_admin"
}

variable "istio_chart_version" {
  description = "Version of the Istio helm charts"
  type        = string
  default     = "1.20.2"
}

variable "eks_scaling_config" {
  description = "Scaling configuration for EKS node group"
  type = object({
    min_size     = number
    max_size     = number
    desired_size = number
  })
  default = {
    min_size     = 2
    max_size     = 5
    desired_size = 2
  }
}

variable "microservice_image_tags" {
  description = "Map of image tags for each microservice"
  type        = map(string)
  default     = {}
}
