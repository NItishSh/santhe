module "eks_al2023" {
  source                                   = "terraform-aws-modules/eks/aws"
  version                                  = "20.24.0"
  cluster_name                             = var.cluster_name
  cluster_version                          = var.cluster_version
  enable_cluster_creator_admin_permissions = true

  # EKS Addons
  cluster_addons = var.cluster_addons

  vpc_id                   = var.vpc_details.vpc_id
  subnet_ids               = var.vpc_details.private_subnets
  control_plane_subnet_ids = var.vpc_details.intra_subnets

  eks_managed_node_groups = {
    node_group = {
      # Starting on 1.30, AL2023 is the default AMI type for EKS managed node groups
      instance_types = ["t3.medium", "t3.large", "t3.xlarge", "t3.2xlarge", "m6i.large", "m6i.xlarge", "m6i.2xlarge"]

      min_size = var.scaling_details.min_size
      max_size = var.scaling_details.max_size
      # This value is ignored after the initial creation
      # https://github.com/bryantbiggs/eks-desired-size-hack
      desired_size = var.scaling_details.desired_size
    }
  }

  tags = var.tags
}
module "ingress" {
  source     = "./modules/ingress-nginx"
  domain     = var.domain
  depends_on = [module.eks_al2023]
}
module "cert_manager" {
  source       = "./modules/cert-manager"
  domain       = var.domain
  issuer_email = "csnitish@gmial.com" //TODO: add a appropriate email here.
  depends_on   = [module.ingress]
}
module "external_dns" {
  source                  = "./modules/external-dns"
  domain                  = var.domain
  cluster_name            = module.eks_al2023.cluster_name
  eks_cluster_oidc_issuer = module.eks_al2023.cluster_oidc_issuer_url
  depends_on              = [module.cert_manager]
}
module "kube_prometheus_stack" {
  source     = "./modules/kube-prometheus-stack"
  depends_on = [module.external_dns]
}
module "eck" {
  source     = "./modules/eck"
  depends_on = [module.kube_prometheus_stack]
}
