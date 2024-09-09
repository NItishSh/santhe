module "kube_prometheus_stack" {
  source  = "terraform-module/release/helm"
  version = "2.6.0"

  namespace  = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  app = {
    name          = "kube-prometheus-stack"
    version       = "62.6.0"
    chart         = "kube-prometheus-stack"
    force_update  = true
    wait          = false
    recreate_pods = false
    deploy        = 1
  }

  values = []

  set = []

  set_sensitive = []
}
