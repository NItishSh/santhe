data "aws_caller_identity" "current" {}

################################################################################
# RDS Module
################################################################################

module "db" {
  source     = "terraform-aws-modules/rds/aws"
  identifier = "${local.name}-rds"

  # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
  engine                   = "postgres"
  engine_version           = "14"
  engine_lifecycle_support = "open-source-rds-extended-support-disabled"
  family                   = "postgres14" # DB parameter group
  major_engine_version     = "14"         # DB option group
  instance_class           = "db.t4g.large"

  allocated_storage     = 20
  max_allocated_storage = 100

  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  db_name  = "${local.name}-database"
  username = "${local.name}_admin"
  port     = 5432


  # Setting manage_master_user_password_rotation to false after it
  # has previously been set to true disables automatic rotation
  # however using an initial value of false (default) does not disable
  # automatic rotation and rotation will be handled by RDS.
  # manage_master_user_password_rotation allows users to configure
  # a non-default schedule and is not meant to disable rotation
  # when initially creating / enabling the password management feature
  manage_master_user_password_rotation              = true
  master_user_password_rotate_immediately           = false
  master_user_password_rotation_schedule_expression = "rate(15 days)"

  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.security_group.security_group_id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  create_monitoring_role                = true
  monitoring_interval                   = 60
  monitoring_role_name                  = "example-monitoring-role-name"
  monitoring_role_use_name_prefix       = true
  monitoring_role_description           = "Description for monitoring role"

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

  tags = local.common_tags
  db_option_group_tags = {
    "Sensitive" = "low"
  }
  db_parameter_group_tags = {
    "Sensitive" = "low"
  }

  parameter_group_name            = local.name
  parameter_group_use_name_prefix = false
  option_group_name               = local.name
  option_group_use_name_prefix    = false
}

################################################################################
# Supporting Resources
################################################################################

module "security_group" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "${local.name}-rds-sg"
  description = "Complete PostgreSQL example security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
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

################################################################################
# Outputs
################################################################################

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = aws_db_instance.this.address
}

output "db_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.this.arn
}

output "db_instance_identifier" {
  description = "The identifier of the RDS instance"
  value       = aws_db_instance.this.identifier
}

output "db_instance_tag" {
  description = "The tag of the RDS instance"
  value       = aws_db_instance.this.tag
}
