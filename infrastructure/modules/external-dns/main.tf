# https://artifacthub.io/packages/helm/external-dns/external-dns
# https://kubernetes-sigs.github.io/external-dns/v0.13.4/tutorials/aws/#iam-policy
# https://www.dae.mn/blog/setting-up-external-dns-for-an-eks-cluster-with-terraform
data "external" "thumb" {
  program = ["kubergrunt", "eks", "oidc-thumbprint", "--issuer-url", var.cluster_oidc_issuer_url]
}

resource "aws_iam_openid_connect_provider" "default" {
  url = var.cluster_oidc_issuer_url
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = [data.external.thumb.result.thumbprint]
}
module "eks-external-dns" {
    source  = "lablabs/eks-external-dns/aws"
    version = "0.9.0"
    cluster_identity_oidc_issuer =  var.cluster_oidc_issuer_url
    cluster_identity_oidc_issuer_arn = aws_iam_openid_connect_provider.default.arn
    policy_allowed_zone_ids = [
        var.route_53_zone_id  # zone id of your hosted zone
    ]
    settings = {
    "policy" = "sync" # syncs DNS records with ingress and services currently on the cluster.
  }
}