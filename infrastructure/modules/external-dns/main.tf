# https://artifacthub.io/packages/helm/external-dns/external-dns
# https://kubernetes-sigs.github.io/external-dns/v0.13.4/tutorials/aws/#iam-policy
locals {
  account_id = data.aws_caller_identity.current.account_id
}
resource "aws_iam_policy" "external_dns_policy" {
  name        = "external_dns_policy"
  path        = "/"
  description = "external_dns_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "route53:ChangeResourceRecordSets"
        ],
        Resource = [
          "arn:aws:route53:::hostedzone/*",
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "route53:ListHostedZones",
          "route53:ListResourceRecordSets"
        ],
        Resource = [
          "*"
        ]
      }
    ]
  })
}
module "external_dns" {
  source  = "terraform-module/release/helm"
  version = "2.6.0"

  namespace  = "external-dns"
  repository = "https://kubernetes-sigs.github.io/external-dns/"
  app = {
    name          = "external-dns"
    version       = "v1.14.5"
    chart         = "external-dns"
    force_update  = true
    wait          = false
    recreate_pods = false
    deploy        = 1
  }

  values = [
    templatefile("${path.module}/values.yaml", {})
  ]

  set = [{
    name  = serviceAccount.annotations
    value = "eks.amazonaws.com/role-arn: arn:aws:iam::${local.account_id}:role/${EXTERNALDNS_ROLE_NAME}"
  }]

  set_sensitive = []
}