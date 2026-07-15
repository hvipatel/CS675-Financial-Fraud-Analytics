# One EMR Serverless execution role per student. EMR Serverless assumes this role
# to run that student's Spark jobs; it is scoped to the student's own S3 buckets.
# Created before the student role (04) because the student policy PassRoles it.

data "aws_iam_policy_document" "emr_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["emr-serverless.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "emr_exec" {
  for_each           = toset(var.students)
  name               = "${var.resource_prefix}-emr-exec-${each.key}"
  assume_role_policy = data.aws_iam_policy_document.emr_assume.json
}

data "aws_iam_policy_document" "emr_exec_policy" {
  for_each = toset(var.students)

  # Read/write only the student's own buckets (<prefix>-<id>-*).
  statement {
    sid     = "OwnBucketData"
    actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"]
    resources = [
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*",
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*/*",
    ]
  }

  # Read the shared Glue catalog (for Athena/Spark table metadata).
  statement {
    sid = "GlueCatalogRead"
    actions = [
      "glue:GetDatabase", "glue:GetDatabases",
      "glue:GetTable", "glue:GetTables",
      "glue:GetPartition", "glue:GetPartitions",
    ]
    resources = ["*"]
  }

  # Write job logs to CloudWatch.
  statement {
    sid = "JobLogs"
    actions = [
      "logs:CreateLogGroup", "logs:CreateLogStream",
      "logs:PutLogEvents", "logs:DescribeLogStreams", "logs:DescribeLogGroups",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "emr_exec" {
  for_each = toset(var.students)
  name     = "emr-exec"
  role     = aws_iam_role.emr_exec[each.key].id
  policy   = data.aws_iam_policy_document.emr_exec_policy[each.key].json
}
