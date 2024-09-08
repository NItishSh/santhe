output "intra_subnets_cidr_blocks" {
  value = module.vpc.intra_subnets_cidr_blocks
}
output "private_subnets" {
  value = module.vpc.private_subnets
}
output "vpc_cidr_block" {
  value = module.vpc.vpc_cidr_block
}
output "vpc_id" {
  value = module.vpc.vpc_id
}
output "intra_subnets" {
  value = module.vpc.intra_subnets
}