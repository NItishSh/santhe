variable "cluster_name" {
  type = string
}
variable "cluster_version" {
  type    = string
  default = "1.30"
}
variable "cluster_addons" {
  description = "A map of EKS addons to enable. Each addon is specified as a key-value pair where the key is the addon name and the value is an empty object."
  type        = map(object({}))
  default = {
    coredns                = {}
    eks-pod-identity-agent = {}
    kube-proxy             = {}
    vpc-cni                = {}
  }
}
variable "vpc_details" {
  description = "Configuration for the VPC where the EKS cluster will be deployed."
  type = object({
    vpc_id          = string
    private_subnets = list(string)
    intra_subnets   = list(string)
  })

  default = {
    vpc_id          = ""
    private_subnets = []
    intra_subnets   = []
  }
}
variable "scaling_details" {
  description = "Configuration for the auto-scaling group of the EKS managed node group."
  type = object({
    min_size     = number
    max_size     = number
    desired_size = number
  })

  validation {
    condition = alltrue([
      var.scaling_details.min_size >= 0,
      var.scaling_details.max_size > 0,
      var.scaling_details.desired_size >= 0,
      var.scaling_details.min_size <= var.scaling_details.max_size,
      var.scaling_details.min_size <= var.scaling_details.desired_size &&
      var.scaling_details.desired_size <= var.scaling_details.max_size
    ])
    error_message = "Scaling details must meet the following criteria:\n- min_size must be non-negative\n- max_size must be greater than 0\n- desired_size must be non-negative\n- min_size must not exceed max_size\n- desired_size must be between min_size and max_size"
  }

  default = {
    min_size     = 2
    max_size     = 5
    desired_size = 2
  }
}
variable "domain" {
  type = string
}
variable "tags" {
  type = map(any)
}
