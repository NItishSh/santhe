# https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx
module "ingress_nginx" {
  source  = "terraform-module/release/helm"
  version = "2.6.0"

  namespace  = "ingress-nginx"
  repository = "https://kubernetes-charts.storage.googleapis.com"
  app = {
    name             = "ingress-nginx"
    version          = "4.11.2"
    chart            = "ingress-nginx"
    force_update     = true
    wait             = true
    recreate_pods    = false
    deploy           = 1
    atomic           = true
    create_namespace = true
  }

  values = []

  set = [
    {
      name  = "controller.service.annotations.external-dns.alpha.kubernetes.io/hostname"
      value = var.domain
    }
  ]

  set_sensitive = []
}
