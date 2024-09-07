data "aws_availability_zones" "available" {}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = local.name
  cidr = var.vpc_cidr

  azs                          = local.azs
  private_subnets              = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, subnet_mask_bits, k)]
  public_subnets               = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, subnet_mask_bits, k + local.subnet_offsets[1])]
  intra_subnets                = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, subnet_mask_bits, k + local.subnet_offsets[2])]
  database_subnets             = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, subnet_mask_bits, k + local.subnet_offsets[3])]
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

