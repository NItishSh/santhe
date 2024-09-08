module "zones" {
  source      = "./modules/rote53"
  domain_name = local.domain
  tags        = local.common_tags
}
module "vpc" {
  source   = "./modules/vpc"
  name     = local.name
  vpc_cidr = var.vpc_cidr
  tags     = local.common_tags
}

module "eks" {
  source          = "./modules/eks"
  cluster_name    = "${local.name}-al2023"
  cluster_version = "1.30"
  cluster_addons = {
    coredns                = {}
    eks-pod-identity-agent = {}
    kube-proxy             = {}
    vpc-cni                = {}
  }
  vpc_details = {
    vpc_id          = module.vpc.vpc_id
    private_subnets = module.vpc.private_subnets
    intra_subnets   = module.vpc.intra_subnets
  }
  scaling_details = {
    min_size     = 2
    max_size     = 5
    desired_size = 2
  }
  domain = local.domain
  tags   = local.common_tags
}

module "argo" {
  source                = "./modules/argo"
  cluster_id            = module.eks.cluster_id
  region                = var.region
  cluster_iam_role_name = module.eks.cluster_iam_role_name
}
module "postgresql" {
  source    = "./modules/postgresql"
  tags      = local.common_tags
  name      = local.name
  db_config = var.db_config
  vpc_details = {
    vpc_id         = module.vpc.vpc_id
    vpc_cidr_block = module.vpc.vpc_cidr_block
    intra_subnets  = module.vpc.intra_subnets
  }
}
module "bastion" {
  source      = "./modules/bastion"
  name_prefix = local.name
  vpc_details = {
    vpc_id                    = module.vpc.vpc_id
    intra_subnets             = module.vpc.intra_subnets
    intra_subnets_cidr_blocks = module.vpc.intra_subnets_cidr_blocks
  }
  tags = local.common_tags
}