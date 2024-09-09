resource "kubernetes_manifest" "clusterissuer_letsencrypt_prod" {
  depends_on = [
    module.cert_manager
  ]

  manifest = {
    apiVersion = "cert-manager.io/v1"
    kind       = "ClusterIssuer"
    metadata = {
      name = "letsencrypt-prod"
    }
    spec = {
      acme = {
        email = var.issuer_email
        privateKeySecretRef = {
          name = "letsencrypt-prod"
        }
        server = "https://acme-v02.api.letsencrypt.org/directory"
        solvers = [
          {
            http01 = {
              ingress = {
                class = "nginx"
              }
            }
          }
        ]
      }
    }
  }
}
