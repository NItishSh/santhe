module "ec2-instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.0"
  name    = "${var.name_prefix}-bastion"
  # create_spot_instance = true
  # spot_price           = "0.60"
  # spot_type            = "persistent"
  instance_type = "t2.micro"
  monitoring    = true
  subnet_id     = var.vpc_details.intra_subnets[0]
  vpc_security_group_ids = [
    module.security_group_instance.security_group_id,
    # module.security_group_postgresql.security_group_id
  ]
  create_iam_instance_profile = true
  iam_role_description        = "IAM role for EC2 instance"
  iam_role_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }
  tags = merge(var.tags, { Name = "${var.name_prefix}-bastion" })
}
module "security_group_instance" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${var.name_prefix}-ec2"
  description = "Security Group for EC2 Instance Egress"

  vpc_id = var.vpc_details.vpc_id

  egress_rules = ["https-443-tcp"]

  tags = var.tags
}

module "vpc_endpoints" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "~> 5.0"

  vpc_id = var.vpc_details.vpc_id

  endpoints = { for service in toset(["ssm", "ssmmessages", "ec2messages"]) :
    replace(service, ".", "_") =>
    {
      service             = service
      subnet_ids          = var.vpc_details.intra_subnets
      private_dns_enabled = true
      tags                = { Name = "${var.name_prefix}-${service}" }
    }
  }

  create_security_group      = true
  security_group_name_prefix = "${var.name_prefix}-vpc-endpoints-"
  security_group_description = "VPC endpoint security group"
  security_group_rules = {
    ingress_https = {
      description = "HTTPS from subnets"
      cidr_blocks = var.vpc_details.intra_subnets_cidr_blocks
    }
  }

  tags = var.tags
}
