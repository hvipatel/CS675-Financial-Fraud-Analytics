output "student_id" {
  value = var.student_id
}

output "bucket" {
  description = "Your S3 workspace bucket."
  value       = aws_s3_bucket.workspace.bucket
}

output "athena_workgroup" {
  description = "Run your Athena queries in this workgroup."
  value       = aws_athena_workgroup.wg.name
}

output "glue_database" {
  description = "Define your tables in this Glue database."
  value       = aws_glue_catalog_database.db.name
}

output "emr_application_id" {
  description = "EMR Serverless app id (null unless enable_emr = true)."
  value       = var.enable_emr ? aws_emrserverless_application.spark[0].id : null
}

output "emr_exec_role_arn" {
  description = "EMR execution role you pass when submitting jobs (from the instructor)."
  value       = var.emr_exec_role_arn
}

output "notebook_workgroup" {
  description = "Athena-for-Spark workgroup for the browser notebook (null unless enable_notebook = true)."
  value       = var.enable_notebook ? aws_athena_workgroup.spark[0].name : null
}

output "notebook_console_url" {
  description = "Open this in the AWS console to use your PySpark notebook (null unless enable_notebook = true)."
  value       = var.enable_notebook ? "https://${var.region}.console.aws.amazon.com/athena/home?region=${var.region}#/notebook-editor" : null
}
