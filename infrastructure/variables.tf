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
