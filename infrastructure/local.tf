locals {
  domain = "${var.product}.store"
  name   = "${var.environment}-${var.region}-${var.product}"
  # Only create ECR in production to act as the persistent/shared repo
  ecr_enabled = var.environment == "prd" && var.region == "ap-south-1" ? 1 : 0
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

  microservices = {
    "user-service"                    = { port = 8080 }
    "order-management-service"        = { port = 8080 }
    "product-catalog-service"         = { port = 8080 }
    "payment-service"                 = { port = 8080 }
    "notification-service"            = { port = 8080 }
    "logistics-management-service"    = { port = 8080 }
    "analytics-and-reporting-service" = { port = 8080 }
    "compliance-and-audit-service"    = { port = 8080 }
    "feedback-and-support-service"    = { port = 8080 }
    "pricing-service"                 = { port = 8080 }
    "review-and-rating-service"       = { port = 8080 }
  }
}
