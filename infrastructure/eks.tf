module "eks_al2023" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "20.24.0"
  cluster_name    = "${local.name}-al2023"
  cluster_version = "1.30"

  # EKS Addons
  cluster_addons = {
    coredns = {}
    # eks-pod-identity-agent = {}
    kube-proxy = {}
    vpc-cni    = {}
    # cert_manager = {}
    # external_dns = {}
  }

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets

  eks_managed_node_groups = {
    example = {
      # Starting on 1.30, AL2023 is the default AMI type for EKS managed node groups
      instance_types = ["m6i.large"]

      min_size = 2
      max_size = 5
      # This value is ignored after the initial creation
      # https://github.com/bryantbiggs/eks-desired-size-hack
      desired_size = 2

      # This is not required - demonstrates how to pass additional configuration to nodeadm
      # Ref https://awslabs.github.io/amazon-eks-ami/nodeadm/doc/api/
      cloudinit_pre_nodeadm = [
        {
          content_type = "application/node.eks.aws"
          content      = <<-EOT
            ---
            apiVersion: node.eks.aws/v1alpha1
            kind: NodeConfig
            spec:
              kubelet:
                config:
                  shutdownGracePeriod: 30s
                  featureGates:
                    DisableKubeletCloudCredentialProviders: true
          EOT
        }
      ]
    }
  }

  tags = local.common_tags
}
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
#       dns_zone       = local.domain
#       region         = var.region
#       secret_key_ref = "letsencrypt-prod"
#       acme_server    = "https://acme-v02.api.letsencrypt.org/directory"
#       acme_email     = "your@email.com"
#     }
#   ]
# }
