# module "cert_manager" {
#   source = "git::https://github.com/DNXLabs/terraform-aws-eks-cert-manager.git"

#   enabled = true

#   cluster_name                     = module.eks_al2023.cluster_id
#   cluster_identity_oidc_issuer     = module.eks_al2023.cluster_oidc_issuer_url
#   cluster_identity_oidc_issuer_arn = module.eks_al2023.oidc_provider_arn

#   dns01 = [
#     {
#       name           = "letsencrypt-prod"
#       namespace      = "default"
#       kind           = "ClusterIssuer"
#       dns_zone       = var.domain
#       region         = var.region
#       secret_key_ref = "letsencrypt-prod"
#       acme_server    = "https://acme-v02.api.letsencrypt.org/directory"
#       acme_email     = "your@email.com"
#     }
#   ]
# }