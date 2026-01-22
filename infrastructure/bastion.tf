module "bastion" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 5.0"

  name = "${local.name}-bastion"

  instance_type          = "t3.micro"
  vpc_security_group_ids = [module.bastion_sg.security_group_id]
  subnet_id              = module.vpc.public_subnets[0]

  create_iam_instance_profile = true
  iam_role_description        = "IAM role for Bastion"
  iam_role_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }

  tags = local.common_tags
}

module "bastion_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-bastion-sg"
  description = "Bastion security group"
  vpc_id      = module.vpc.vpc_id

  egress_rules = ["all-all"]

  tags = local.common_tags
}
