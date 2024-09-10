# https://artifacthub.io/packages/helm/cert-manager/cert-manager
module "cert_manager" {
  source  = "terraform-module/release/helm"
  version = "2.6.0"

  namespace  = "kube-system"
  repository = "https://charts.jetstack.io"
  app = {
    name             = "cert-manager"
    version          = "v1.15.3"
    chart            = "cert-manager"
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
      name  = "crds.enabled"
      value = true
    },
    {
      name  = "crds.keep"
      value = true
    }
  ]

  set_sensitive = []
}
