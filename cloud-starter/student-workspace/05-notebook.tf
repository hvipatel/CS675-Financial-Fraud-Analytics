# OPTIONAL browser notebook UI (Athena for Apache Spark). When enable_notebook =
# true this creates a Spark-enabled Athena workgroup. Open it in the AWS console
# (Athena -> Notebook editor) to get a Jupyter-style PySpark notebook backed by
# Athena's serverless Spark - no cluster to manage. Athena assumes your spark
# execution role (from the instructor) to run the sessions.
resource "aws_athena_workgroup" "spark" {
  count         = var.enable_notebook ? 1 : 0
  name          = "${var.resource_prefix}-${var.student_id}-spark"
  force_destroy = true

  configuration {
    # Spark workgroups don't support the SQL scan cap; keep the config minimal.
    execution_role = var.spark_exec_role_arn

    engine_version {
      selected_engine_version = "PySpark engine version 3"
    }

    result_configuration {
      output_location = "s3://${aws_s3_bucket.workspace.bucket}/notebook-results/"
    }
  }
}
