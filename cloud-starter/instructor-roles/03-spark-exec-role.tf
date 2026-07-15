# One Athena-for-Spark execution role per student. Athena assumes this role to run
# the student's notebook Spark sessions; it is scoped to the student's own S3
# buckets + Glue database. This is what powers the browser notebook UI (Athena for
# Apache Spark) - the student passes this ARN when creating their Spark workgroup.
# Created before the student role (04) because the student policy PassRoles it.

data "aws_iam_policy_document" "spark_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["athena.amazonaws.com"]
    }
    # Confused-deputy guard: only Athena in THIS account may assume the role.
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }
}

resource "aws_iam_role" "spark_exec" {
  for_each           = toset(var.students)
  name               = "${var.resource_prefix}-spark-exec-${each.key}"
  assume_role_policy = data.aws_iam_policy_document.spark_assume.json
}

data "aws_iam_policy_document" "spark_exec_policy" {
  for_each = toset(var.students)

  # Read/write only the student's own buckets (data, notebook state, results).
  statement {
    sid     = "OwnBucketData"
    actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket", "s3:GetBucketLocation"]
    resources = [
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*",
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*/*",
    ]
  }

  # Read the shared catalog + create/read tables in their own Glue database from
  # inside the notebook (so a notebook can register a table over a dataset).
  statement {
    sid = "GlueCatalog"
    actions = [
      "glue:GetDatabase", "glue:GetDatabases", "glue:GetTable", "glue:GetTables",
      "glue:GetPartition", "glue:GetPartitions",
      "glue:CreateTable", "glue:UpdateTable", "glue:DeleteTable", "glue:BatchCreatePartition",
    ]
    resources = ["*"]
  }

  # Notebook Spark session logs.
  statement {
    sid = "SessionLogs"
    actions = [
      "logs:CreateLogGroup", "logs:CreateLogStream",
      "logs:PutLogEvents", "logs:DescribeLogStreams", "logs:DescribeLogGroups",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "spark_exec" {
  for_each = toset(var.students)
  name     = "spark-exec"
  role     = aws_iam_role.spark_exec[each.key].id
  policy   = data.aws_iam_policy_document.spark_exec_policy[each.key].json
}
