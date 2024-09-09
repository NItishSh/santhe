resource "kubernetes_manifest" "eck_operator" {
  manifest = {
    apiVersion = operators.coreos.com / v1alpha1
    kind       = Subscription
    metadata = {
      name      = eck
      namespace = operators
    }
    spec = {
      channel         = stable
      name            = elastic-cloud-eck
      source          = operatorhubio-catalog
      sourceNamespace = olm
    }
  }
}
