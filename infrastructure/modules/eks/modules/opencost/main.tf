# # https://www.automat-it.com/blog/monitoring-costs-of-containerized-workloads-in-eks-using-opencost-and-aws-managed-prometheus-grafana/
# ### Variables
# variable "amp_workspace_id" { type = string }
# variable "opencost_helm_version" { default = "1.29.0" }
# variable "opencost_service_account_name" { type = string }

# data "aws_iam_policy_document" "opencost-oidc-assume-role-policy" {
#   statement {
#     actions = ["sts:AssumeRoleWithWebIdentity"]
#     effect  = "Allow"

#     condition {
#       test     = "StringEquals"
#       variable = "${replace(var.iam_openid_provider_url, "https://", "")}:sub"
#       values   = ["system:serviceaccount:${var.namespace}:${var.opencost_service_account_name}"]
#     }

#     principals {
#       identifiers = [var.iam_openid_provider_arn]
#       type        = "Federated"
#     }
#   }
# }

# resource "aws_iam_role" "opencost-irsa-role" {
#   assume_role_policy = data.aws_iam_policy_document.opencost-oidc-assume-role-policy.json
#   name               = "${var.eks_cluster_name}-${var.opencost_service_account_name}-role"
# }

# resource "kubernetes_service_account" "opencost-irsa" {
#   automount_service_account_token = true
#   metadata {
#     name      = var.opencost_service_account_name
#     namespace = var.namespace
#     annotations = {
#       "eks.amazonaws.com/role-arn" = aws_iam_role.opencost-irsa-role.arn
#     }
#   }
# }

# ### Inline IAM Policy
# resource "aws_iam_role_policy" "eks-system-opencost" {
#   name = "opencost-policy"
#   role = aws_iam_role.opencost-irsa-role.id

#   policy = <<-EOF
#   {
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Effect": "Allow",
#         "Action": [
#           "aps:RemoteWrite",
#           "aps:GetSeries",
#           "aps:GetLabels",
#           "aps:GetMetricMetadata",
#           "aps:QueryMetrics"
#         ],
#         "Resource": "*"
#       }
#     ]
#   }

#   EOF
# }

# ### Opencost helm chart
# resource "helm_release" "opencost" {
#   name       = "opencost-charts"
#   repository = "https://opencost.github.io/opencost-helm-chart"
#   chart      = "opencost"
#   version    = var.opencost_helm_version

#   create_namespace = false
#   namespace        = var.namespace

#   values = [<<EOF

#     serviceAccount:
#       create: false
#       name: ${kubernetes_service_account.opencost-irsa.metadata[0].name}

#     opencost:
#       ui:
#         enabled: false
#       prometheus:
#         internal:
#           enabled: false
#         external:
#           enable: false
#         amp:
#           enabled: true  # If true, opencost will be configured to remote_write and query from Amazon Managed Service for Prometheus.
#           workspaceId: ${var.amp_workspace_id}

#       sigV4Proxy:
#         image: public.ecr.aws/aws-observability/aws-sigv4-proxy:1.7
#         name: aps
#         port: 8005
#         region: ${var.aws_region}
#         host: "aps-workspaces.${var.aws_region}.amazonaws.com" # The hostname for AMP service.

#       nodeSelector:
#         pool: system
#       tolerations:
#         - key: dedicated
#           operator: Equal
#           value: system
#           effect: NoSchedule

#     EOF
#   ]
# }
