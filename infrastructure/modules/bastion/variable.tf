variable "name_prefix" {
  type = string
}
variable "vpc_details" {
  description = "Configuration for the VPC where the EKS cluster will be deployed."
  type = object({
    vpc_id                    = string
    intra_subnets             = list(string)
    intra_subnets_cidr_blocks = list(string)
  })

  default = {
    vpc_id                    = ""
    intra_subnets             = []
    intra_subnets_cidr_blocks = []
  }
}

variable "tags" {
  type = map(any)
}