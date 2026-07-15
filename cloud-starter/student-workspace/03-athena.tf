# Athena is the easy default: interactive SQL over large S3 data, no cluster.
# Your workgroup caps per-query scans (cost guardrail) and writes results to your bucket.
resource "aws_athena_workgroup" "wg" {
  name          = "${var.resource_prefix}-${var.student_id}"
  force_destroy = true

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true
    bytes_scanned_cutoff_per_query     = var.athena_scan_cap_bytes

    result_configuration {
      output_location = "s3://${aws_s3_bucket.workspace.bucket}/athena-results/"
    }
  }
}

# Your own Glue database, where you define tables over datasets you query.
resource "aws_glue_catalog_database" "db" {
  name = "${var.resource_prefix}_${var.student_id}"
}
