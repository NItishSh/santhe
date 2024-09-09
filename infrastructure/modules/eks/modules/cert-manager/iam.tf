#https://github.com/terraform-aws-modules/terraform-aws-iam/blob/89fe17a6549728f1dc7e7a8f7b707486dfb45d89/examples/iam-role-for-service-accounts-eks/main.tf#L160
# module "cert_manager_irsa_role" {
#   source = "../../modules/iam-role-for-service-accounts-eks"

#   role_name                     = "cert-manager"
#   attach_cert_manager_policy    = true
#   cert_manager_hosted_zone_arns = ["arn:aws:route53:::hostedzone/IClearlyMadeThisUp"]

#   oidc_providers = {
#     ex = {
#       provider_arn               = module.eks.oidc_provider_arn
#       namespace_service_accounts = ["kube-system:cert-manager"]
#     }
#   }

#   tags = local.tags
# }
