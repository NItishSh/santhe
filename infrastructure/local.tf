locals {
  domain      = "${var.product}.store"
  name        = "${var.environment}-${var.region}-${var.product}"
  ecr_enabled = var.environment == "sbx" && var.region == "ap-south-1" ? 1 : 0
  common_tags = {
    environment   = var.environment
    region        = var.region
    name          = local.name
    project       = "${var.product}-app"
    cost-center   = "marketing"
    owner         = "team@${local.domain}"
    compliance    = ""
    cost-tracking = "true"
  }
}
