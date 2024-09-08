
# resource "aws_iam_role_policy_attachment" "eks_worker_node_unlimited_access" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterAccess"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_administrator_access" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_container_registry_read_only_access" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_describe_instances" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2DescribeInstances"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_create_tags" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2CreateTags"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_read_write_all" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ssm_full_access" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_cloudwatch_logs_full_access" {
#   policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_vpc_full_access" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_instance_profile" {
#   policy_arn = "arn:aws:iam::aws:policy/AWS_EC2InstanceProfileForImageBuilder"
#   role       = var.cluster_iam_role_name
# }

# resource "aws_iam_role_policy_attachment" "eks_worker_node_ec2_read_write" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadWriteAccess"
#   role       = var.cluster_iam_role_name
# }