# kubectl create namespace argocd
# kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
# https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd
resource "helm_release" "argo_cd" {
  name             = "argo-cd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argo-cd"
  create_namespace = var.create_namespace
  atomic           = var.atomic
  timeout          = var.timeout

  set {
    name  = "server.config.managementServer.webconsole.enabled"
    value = "true"
  }

  set {
    name  = "server.config.managementServer.webconsole.host"
    value = "localhost"
  }
}