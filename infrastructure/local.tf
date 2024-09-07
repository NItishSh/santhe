locals {
  product      = "santhe"
  domain       = "${local.product}.store"
  name         = "${var.environment}-${var.region}-${local.product}"
  azs          = slice(data.aws_availability_zones.available.names, 0, 3)
  region       = var.region
  need_bastion = true
  # Extract the number of bits from the VPC CIDR
  vpc_bits = tonumber(split("/", var.vpc_cidr)[1])

  # Calculate available bits for subnetting
  available_bits = 32 - vpc_bits

  # Number of subnet types
  num_subnet_types = 4

  # Calculate bits needed for subnetting
  subnet_bits = ceil(log(num_subnet_types, 2))

  # Calculate bits for each subnet
  subnet_mask_bits = available_bits - subnet_bits

  # Calculate the number of subnets per type
  num_subnets_per_type = pow(2, subnet_bits)

  # Calculate the offset for each subnet type
  subnet_offsets = [
    for i in range(num_subnet_types) :
    i * num_subnets_per_type
  ]
  common_tags = {
    environment   = var.environment
    region        = var.region
    name          = local.name
    project       = "${local.product}-app"
    cost-center   = "marketing"
    owner         = "team@${local.domain}"
    compliance    = "gdpr"
    cost-tracking = "true"
  }
}
