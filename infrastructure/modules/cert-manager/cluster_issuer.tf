resource "kubernetes_manifest" "clusterissuer_letsencrypt_prod" {
  depends_on = [
    helm_release.cert_manager
  ]

  manifest = {
    apiVersion = "cert-manager.io/v1"
    kind       = "ClusterIssuer"
    metadata = {
      name = "letsencrypt-prod"
    }
    spec = {
      acme = {
        email = var.ISSUER_EMAIL
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
