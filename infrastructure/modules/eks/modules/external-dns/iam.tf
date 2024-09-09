resource "aws_iam_role" "external_dns" {
  name = "external-dns"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(var.eks_cluster_oidc_issuer, "https://", "")}"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${replace(var.eks_cluster_oidc_issuer, "https://", "")}:sub" : "system:serviceaccount:kube-system:external-dns"
          }
        }
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "external_dns" {
  role       = aws_iam_role.external_dns.name
  policy_arn = aws_iam_policy.external_dns.arn
}

resource "aws_iam_policy" "external_dns" {
  name        = "external-dns-policy"
  description = "Policy for ExternalDNS to update Route53 records"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "route53:ChangeResourceRecordSets",
        ]
        Resource = [
          "arn:aws:route53:::hostedzone/*",
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "route53:ListHostedZones",
          "route53:ListResourceRecordSets",
        ]
        Resource = [
          "*",
        ]
      },
    ]
  })
}
# https://github.com/terraform-aws-modules/terraform-aws-iam/blob/89fe17a6549728f1dc7e7a8f7b707486dfb45d89/examples/iam-role-for-service-accounts-eks/main.tf#L160
# module "external_dns_irsa_role" {
#   source = "../../modules/iam-role-for-service-accounts-eks"

#   role_name                     = "external-dns"
#   attach_external_dns_policy    = true
#   external_dns_hosted_zone_arns = ["arn:aws:route53:::hostedzone/IClearlyMadeThisUp"]

#   oidc_providers = {
#     ex = {
#       provider_arn               = module.eks.oidc_provider_arn
#       namespace_service_accounts = ["kube-system:external-dns"]
#     }
#   }

#   tags = local.tags
# }
