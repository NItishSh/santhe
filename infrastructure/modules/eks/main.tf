module "eks_al2023" {
  source                                   = "terraform-aws-modules/eks/aws"
  version                                  = "20.24.0"
  cluster_name                             = var.cluster_name //"${local.name}-al2023"
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

  tags = var.tags
}
