module "ec2-instance" {
  count   = local.need_bastion ? 1 : 0
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.0"
  name    = "${local.name}-bastion"
  # create_spot_instance = true
  # spot_price           = "0.60"
  # spot_type            = "persistent"
  instance_type = "t2.micro"
  monitoring    = true
  subnet_id     = module.vpc.intra_subnets[0]
  vpc_security_group_ids = [
    module.security_group_instance.security_group_id,
    module.security_group_postgresql.security_group_id
  ]
  create_iam_instance_profile = true
  iam_role_description        = "IAM role for EC2 instance"
  iam_role_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }
  tags = merge(local.common_tags, { Name = "${local.name}-bastion" })
}
module "security_group_instance" {
  count   = local.need_bastion ? 1 : 0
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-ec2"
  description = "Security Group for EC2 Instance Egress"

  vpc_id = module.vpc.vpc_id

  egress_rules = ["https-443-tcp"]

  tags = local.common_tags
}

module "vpc_endpoints" {
  count   = local.need_bastion ? 1 : 0
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "~> 5.0"

  vpc_id = module.vpc.vpc_id

  endpoints = { for service in toset(["ssm", "ssmmessages", "ec2messages"]) :
    replace(service, ".", "_") =>
    {
      service             = service
      subnet_ids          = module.vpc.intra_subnets
      private_dns_enabled = true
      tags                = { Name = "${local.name}-${service}" }
    }
  }

  create_security_group      = true
  security_group_name_prefix = "${local.name}-vpc-endpoints-"
  security_group_description = "VPC endpoint security group"
  security_group_rules = {
    ingress_https = {
      description = "HTTPS from subnets"
      cidr_blocks = module.vpc.intra_subnets_cidr_blocks
    }
  }

  tags = local.common_tags
}
