locals {
  product      = "santhe"
  domain       = "${local.product}.store"
  name         = "${var.environment}-${var.region}-${local.product}"
  azs          = slice(data.aws_availability_zones.available.names, 0, 3)
  region       = var.region
  need_bastion = true
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
