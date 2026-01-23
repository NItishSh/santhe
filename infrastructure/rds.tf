locals {
  db_config = merge(
    var.db_config,
    {
      engine                = "postgres"
      engine_version        = "14"
      family                = "postgres14"
      major_engine_version  = "14"
      instance_class        = var.db_instance_class
      allocated_storage     = var.db_allocated_storage
      max_allocated_storage = 100
      db_name               = var.db_name
      username              = var.db_username
    }
  )
}

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${local.name}-rds"

  engine               = local.db_config.engine
  engine_version       = local.db_config.engine_version
  family               = local.db_config.family
  major_engine_version = local.db_config.major_engine_version
  instance_class       = local.db_config.instance_class

  allocated_storage     = local.db_config.allocated_storage
  max_allocated_storage = local.db_config.max_allocated_storage

  db_name  = local.db_config.db_name
  username = local.db_config.username
  port     = 5432

  multi_az               = true
  db_subnet_group_name   = "${local.name}-db-subnet-group"
  vpc_security_group_ids = [module.security_group_postgresql.security_group_id]

  maintenance_window      = "Mon:00:00-Mon:03:00"
  backup_window           = "03:00-06:00"
  backup_retention_period = 7
  skip_final_snapshot     = var.environment == "prd" ? false : true
  deletion_protection     = var.environment == "prd" ? true : false

  subnet_ids = module.vpc.database_subnets

  tags = local.common_tags
}

module "security_group_postgresql" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-rds-sg"
  description = "PostgreSQL security group"
  vpc_id      = module.vpc.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
  ]

  tags = local.common_tags
}
