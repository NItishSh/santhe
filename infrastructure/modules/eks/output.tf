output "cluster_iam_role_name" {
  value = module.eks_al2023.cluster_iam_role_name
}
output "cluster_id" {
  value = module.eks_al2023.cluster_id
}
output "cluster_name" {
  value = module.eks_al2023.cluster_name
}
output "cluster_ca_cert" {
  value = module.eks_al2023.cluster_certificate_authority_data
}
output "cluster_endpoint" {
  value = module.eks_al2023.cluster_endpoint
}