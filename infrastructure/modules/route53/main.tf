module "zones" {
  source  = "terraform-aws-modules/route53/aws//modules/zones"
  version = "4.1.0"

  zones = {
    "${var.domain_name}" = {
      comment = var.domain_name
    }
  }
  tags = var.tags
}