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
  default = "arn:aws:iam::123456789100:role/my-github-actions-role"
}
