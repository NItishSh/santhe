resource "helm_release" "microservice" {
  for_each = local.microservices

  name             = each.key
  chart            = "${path.module}/../charts/microservice"
  namespace        = "default"
  create_namespace = true
  version          = "0.1.0"

  values = [
    yamlencode({
      image = {
        repository = "${module.ecr.repository_url}"
        # Tag format: <service-name>-<tag> (e.g., user-service-sha-123)
        # Default tag is 'latest' -> user-service-latest
        tag = "${each.key}-${lookup(var.microservice_image_tags, each.key, "latest")}"
      }
      service = {
        port = each.value.port
      }
      nameOverride     = each.key
      fullnameOverride = each.key
    })
  ]

  depends_on = [module.eks, module.ecr]
}
