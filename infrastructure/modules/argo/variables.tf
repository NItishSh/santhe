variable "cluster_id" {
  type = string
}
variable "region" {
  type = string
}
variable "cluster_iam_role_name" {
  type = string
}
variable "create_namespace" {
  type    = bool
  default = true
}
variable "atomic" {
  type    = bool
  default = true
}
variable "timeout" {
  type    = number
  default = 300
}
