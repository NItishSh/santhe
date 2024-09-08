variable "name" {
  type = string
}
variable "vpc_cidr" {
  type = string
}
variable "tags" {
  type = map(any)
}
variable "num_subnet_types" {
  type    = number
  default = 4
}