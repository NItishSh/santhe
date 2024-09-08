variable "tags" {
  type = map(any)
}
variable "name" {
  type = string
}
variable "db_config" {
  description = "Configuration for the PostgreSQL database"
  type = object({
    engine                = string
    engine_version        = string
    family                = string
    major_engine_version  = string
    instance_class        = string
    allocated_storage     = number
    max_allocated_storage = number
    db_name               = string
    username              = string
  })
  default = null
}
variable "vpc_details" {
  type = object({
    vpc_id         = string
    vpc_cidr_block = string
    intra_subnets  = list(string)
  })
  default = {
    vpc_id         = ""
    vpc_cidr_block = ""
    intra_subnets  = []
  }
}