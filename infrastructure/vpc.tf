locals {
  # Extract the number of bits from the VPC CIDR
  vpc_bits = tonumber(split("/", var.vpc_cidr)[1])

  # Calculate available bits for subnetting
  available_bits = 32 - local.vpc_bits

  # Number of subnet types
  num_subnet_types = 4

  # Calculate bits needed for subnetting
  subnet_bits = ceil(log(local.num_subnet_types, 2))

  # Calculate bits for each subnet
  subnet_mask_bits = local.available_bits - local.subnet_bits

  # Calculate the number of subnets per type
  num_subnets_per_type = pow(2, local.subnet_bits)

  # Calculate the offset for each subnet type
  subnet_offsets = [
    for i in range(local.num_subnet_types) :
    i * local.num_subnets_per_type
  ]
}
data "aws_availability_zones" "available" {}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.13.0"
  name    = local.name
  cidr    = var.vpc_cidr

  azs                          = local.azs
  private_subnets              = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, local.subnet_mask_bits, k)]
  public_subnets               = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, local.subnet_mask_bits, k + local.subnet_offsets[1])]
  intra_subnets                = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, local.subnet_mask_bits, k + local.subnet_offsets[2])]
  database_subnets             = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, local.subnet_mask_bits, k + local.subnet_offsets[3])]
  create_database_subnet_group = true
  enable_nat_gateway           = true
  single_nat_gateway           = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
  tags = local.common_tags
}

