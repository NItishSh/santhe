locals {
  domain       = "${var.product}.store"
  name         = "${var.environment}-${var.region}-${var.product}"
  azs          = slice(data.aws_availability_zones.available.names, 0, 3)
  need_bastion = true
  common_tags = {
    environment   = var.environment
    region        = var.region
    name          = local.name
    project       = "${var.product}-app"
    cost-center   = "marketing"
    owner         = "team@${local.domain}"
    compliance    = "gdpr"
    cost-tracking = "true"
  }
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
      db_name               = "${local.name}-database"
      username              = "${local.name}_admin"
    }
  )
}
