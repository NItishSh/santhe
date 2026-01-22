module "zones" {
  source  = "terraform-aws-modules/route53/aws//modules/zones"
  version = "~> 2.10"

  zones = {
    "${local.domain}" = {
      comment = "Managed by Terraform"
    }
  }

  tags = local.common_tags
}
