# OPTIONAL elastic serverless Spark cluster. Only created when enable_emr = true.
# Capacity-capped and auto-stops when idle (cost guardrails).
resource "aws_emrserverless_application" "spark" {
  count         = var.enable_emr ? 1 : 0
  name          = "${var.resource_prefix}-${var.student_id}-spark"
  release_label = "emr-7.1.0"
  type          = "SPARK"

  maximum_capacity {
    cpu    = "${var.emr_max_cpu} vCPU"
    memory = "${var.emr_max_memory_gb} GB"
  }

  auto_start_configuration {
    enabled = true
  }
  auto_stop_configuration {
    enabled              = true
    idle_timeout_minutes = 15
  }
}
