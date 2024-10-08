data "aws_caller_identity" "current" {}
module "external_dns" {
  source  = "terraform-module/release/helm"
  version = "2.6.0"

  namespace  = "kube-system"
  repository = "https://charts.bitnami.com/bitnami"
  app = {
    name             = "external-dns"
    version          = "8.3.7"
    chart            = "external-dns"
    force_update     = true
    wait             = true
    recreate_pods    = false
    deploy           = 1
    atomic           = true
    create_namespace = true
  }

  values = []

  set = [
    {
      name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
      value = aws_iam_role.external_dns.arn
    },
    {
      name  = "provider"
      value = "aws"
    },
    {
      name  = "domainFilters[0]"
      value = var.domain
    }
  ]

  set_sensitive = []
}
