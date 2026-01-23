module "eks" {
  source = "terraform-aws-modules/eks/aws"
  # version = "21.15.1"

  name               = local.name
  kubernetes_version = "1.32"

  endpoint_public_access = true

  enable_cluster_creator_admin_permissions = true

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets

  eks_managed_node_groups = {
    default = {
      instance_types = var.eks_instance_types
      min_size       = var.eks_scaling_config.min_size
      max_size       = var.eks_scaling_config.max_size
      desired_size   = var.eks_scaling_config.desired_size
    }
  }

  tags = local.common_tags
}

# Data source for authentication
data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}

module "eks_blueprints_addons" {
  source  = "aws-ia/eks-blueprints-addons/aws"
  version = "1.23.0"

  cluster_name      = module.eks.cluster_name
  cluster_endpoint  = module.eks.cluster_endpoint
  cluster_version   = module.eks.cluster_version
  oidc_provider_arn = module.eks.oidc_provider_arn

  # Add-ons
  enable_metrics_server             = true
  enable_cluster_autoscaler         = true
  enable_external_dns               = true
  enable_cert_manager               = true
  enable_ingress_nginx              = false
  enable_aws_gateway_api_controller = true

  # Kube Prometheus Stack (Monitoring)
  enable_kube_prometheus_stack = true

  cert_manager = {
    route53_zone_id = module.zones.route53_zone_zone_id[local.domain]
  }

  external_dns = {
    route53_zone_arns = [module.zones.route53_zone_zone_arn[local.domain]]
  }

  tags = local.common_tags
}
