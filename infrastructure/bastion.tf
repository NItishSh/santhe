resource "aws_instance" "bastion" {
  count         = local.need_bastion ? 1 : 0
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnets[0]
  vpc_security_group_ids = [
    aws_security_group.bastion_sg.id,
    module.security_group.security_group_id
  ]

  tags = merge(local.common_tags, { Name = "${local.name}-bastion" })
  lifecycle {
    ignore_changes = [instance_state]
  }
  depends_on = [module.vpc]
}
module "security_group" {
  count  = local.need_bastion ? 1 : 0
  source = "terraform-aws-modules/security-group/aws"

  name        = "${local.name}-bastion-sg"
  description = "Security group for bastion host"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = ["0.0.0.0/0"] # need to change this to specific ip/32 
    },
  ]
  egress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = [module.vpc.vpc_cidr_block]
    },
  ]

  tags = local.common_tags
}
