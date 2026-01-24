output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "rds_endpoint" {
  description = "RDS Endpoint"
  value       = module.db.db_instance_endpoint
}

output "bastion_public_ip" {
  description = "Public IP of Bastion Host"
  value       = module.bastion.public_ip
}

output "ecr_repository_url" {
  description = "ECR Repository URL"
  value       = local.ecr_enabled == 1 ? module.ecr[0].repository_url : var.ecr_repository_url
}
