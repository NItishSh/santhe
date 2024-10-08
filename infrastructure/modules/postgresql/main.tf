locals {
  db_config = merge(
    var.db_config,
    {
      engine                = "postgres"
      engine_version        = "14"
      family                = "postgres14"
      major_engine_version  = "14"
      instance_class        = "db.t4g.large"
      allocated_storage     = 20
      max_allocated_storage = 100
      db_name               = "${var.name}-database"
      username              = "${var.name}_admin"
    }
  )
}

################################################################################
# RDS Module
################################################################################

module "db" {
  source     = "terraform-aws-modules/rds/aws"
  version    = "6.9.0"
  identifier = "${var.name}-rds"

  # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
  engine                = local.db_config.engine
  engine_version        = local.db_config.engine_version
  family                = local.db_config.family
  major_engine_version  = local.db_config.major_engine_version
  instance_class        = local.db_config.instance_class
  allocated_storage     = local.db_config.allocated_storage
  max_allocated_storage = local.db_config.max_allocated_storage
  db_name               = local.db_config.db_name
  username              = local.db_config.username
  port                  = 5432

  multi_az               = true
  db_subnet_group_name   = "${var.name}-db_subnet-group"
  vpc_security_group_ids = [module.security_group_postgresql.security_group_id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  backup_retention_period = 10
  skip_final_snapshot     = false
  deletion_protection     = true

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  create_monitoring_role                = true
  monitoring_interval                   = 60
  monitoring_role_name                  = "${var.name}-rds-monitoring-role"
  monitoring_role_use_name_prefix       = false
  monitoring_role_description           = "rds-monitoring-role for ${var.name}"

  parameters = [
    {
      name  = "autovacuum"
      value = "on" # Enable autovacuum for regular table maintenance
    },
    {
      name  = "client_encoding"
      value = "UTF8" # Set UTF8 encoding for internationalization support
    },
    {
      name  = "shared_buffers"
      value = "128MB" # Increase shared buffers for improved performance
    },
    {
      name  = "effective_cache_size"
      value = "1024MB" # Set cache size based on available memory
    }
  ]

  tags = var.tags
  db_option_group_tags = {
    "Sensitive" = "low"
  }
  db_parameter_group_tags = {
    "Sensitive" = "low"
  }

  parameter_group_name            = var.name
  parameter_group_use_name_prefix = false
  option_group_name               = var.name
  option_group_use_name_prefix    = false
}

################################################################################
# Supporting Resources
################################################################################

module "security_group_postgresql" {
  source      = "terraform-aws-modules/security-group/aws"
  version     = "5.2.0"
  name        = "${var.name}-rds-sg"
  description = "Complete PostgreSQL example security group"
  vpc_id      = var.vpc_details.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = var.vpc_details.vpc_cidr_block
    },
  ]

  tags = var.tags
}
