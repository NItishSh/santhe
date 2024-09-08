locals {
  domain = "${var.product}.store"
  name   = "${var.environment}-${var.region}-${var.product}"
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
}
