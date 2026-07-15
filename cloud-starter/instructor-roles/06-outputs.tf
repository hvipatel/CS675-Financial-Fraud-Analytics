# One row per student: the role they assume, the EMR execution role their jobs use
# (passed when submitting an EMR Serverless job), and the Athena-for-Spark execution
# role their notebook sessions use (passed when creating their Spark workgroup).
output "students" {
  description = "Per-student role ARNs. Hand each student their student_role_arn, emr_exec_role_arn, and spark_exec_role_arn."
  value = {
    for id in var.students : id => {
      student_role_arn    = aws_iam_role.student[id].arn
      emr_exec_role_arn   = aws_iam_role.emr_exec[id].arn
      spark_exec_role_arn = aws_iam_role.spark_exec[id].arn
    }
  }
}

output "resource_prefix" {
  description = "Students must name their S3 buckets <resource_prefix>-<id>-* and tag EMR apps Owner=<id>."
  value       = var.resource_prefix
}
