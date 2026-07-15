# One IAM role per student. The student assumes this role (creds you hand out) to
# run terraform in their workspace dir (spin up their S3 + EMR Serverless app) and
# to submit jobs. Isolation: S3 by name (<prefix>-<id>-*), EMR by tag (Owner=<id>).

data "aws_iam_policy_document" "student_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type = "AWS"
      identifiers = length(var.assume_role_principal_arns) > 0 ? var.assume_role_principal_arns : [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
      ]
    }
  }
}

resource "aws_iam_role" "student" {
  for_each           = toset(var.students)
  name               = "${var.resource_prefix}-student-${each.key}"
  assume_role_policy = data.aws_iam_policy_document.student_assume.json
}

data "aws_iam_policy_document" "student_policy" {
  for_each = toset(var.students)

  # Create and use only their own buckets (<prefix>-<id>-*).
  statement {
    sid     = "OwnBuckets"
    actions = ["s3:*"] # full control, but ONLY of their own buckets (scoped below)
    resources = [
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*",
      "arn:aws:s3:::${var.resource_prefix}-${each.key}-*/*",
    ]
  }

  # Listing all buckets requires a "*" resource (read-only, harmless).
  statement {
    sid       = "ListBucketsGlobal"
    actions   = ["s3:ListAllMyBuckets", "s3:GetBucketLocation"]
    resources = ["*"]
  }

  # Manage EMR Serverless applications and jobs they own. EMR Serverless ARNs are
  # id-based (not name-based), so ownership is enforced with an Owner=<id> tag:
  # they may only create resources tagged Owner=<id> and only act on such resources.
  statement {
    sid       = "EmrCreateOwn"
    actions   = ["emr-serverless:CreateApplication", "emr-serverless:TagResource"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "aws:RequestTag/Owner"
      values   = [each.key]
    }
  }
  # Application-level actions: scoped by the Owner=<id> tag on the application (and
  # StartJobRun, whose resource IS the application, so the tag condition applies).
  statement {
    sid = "EmrManageOwn"
    actions = [
      "emr-serverless:GetApplication", "emr-serverless:UpdateApplication",
      "emr-serverless:StartApplication", "emr-serverless:StopApplication",
      "emr-serverless:DeleteApplication",
      "emr-serverless:StartJobRun",
    ]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/Owner"
      values   = [each.key]
    }
  }
  # Job-run actions act on the JOB RUN resource, which does NOT inherit the
  # application's Owner tag - so a tag condition can't apply. Scope to the job-run
  # ARN pattern instead. These are observe/cancel-only (no ability to create infra).
  statement {
    sid = "EmrJobRuns"
    actions = [
      "emr-serverless:GetJobRun", "emr-serverless:ListJobRuns",
      "emr-serverless:CancelJobRun", "emr-serverless:GetDashboardForJobRun",
    ]
    resources = ["arn:aws:emr-serverless:*:*:/applications/*/jobruns/*"]
  }
  # Listing applications cannot be resource-scoped (read-only).
  statement {
    sid       = "EmrList"
    actions   = ["emr-serverless:ListApplications", "emr-serverless:ListTagsForResource"]
    resources = ["*"]
  }

  # Pass ONLY their own EMR execution role when submitting jobs.
  statement {
    sid       = "PassOwnEmrRole"
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.emr_exec[each.key].arn]
    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"
      values   = ["emr-serverless.amazonaws.com"]
    }
  }

  # Run Athena queries AND Spark notebooks in their own workgroups (Athena is the
  # easy default path). Two workgroups: <prefix>-<id> (SQL) and <prefix>-<id>-spark
  # (Apache Spark notebook UI). athena:* here also covers the notebook/session/
  # calculation actions, which authorize against the workgroup resource.
  statement {
    sid     = "AthenaRun"
    actions = ["athena:*"] # full control, scoped to their own workgroups below
    resources = [
      "arn:aws:athena:*:*:workgroup/${var.resource_prefix}-${each.key}",
      "arn:aws:athena:*:*:workgroup/${var.resource_prefix}-${each.key}-spark",
      "arn:aws:athena:*:*:workgroup/primary",
    ]
  }
  # Create/manage only their own Athena workgroups (their workspace terraform makes them).
  statement {
    sid     = "AthenaOwnWorkgroup"
    actions = ["athena:CreateWorkGroup", "athena:UpdateWorkGroup", "athena:DeleteWorkGroup", "athena:TagResource"]
    resources = [
      "arn:aws:athena:*:*:workgroup/${var.resource_prefix}-${each.key}",
      "arn:aws:athena:*:*:workgroup/${var.resource_prefix}-${each.key}-spark",
    ]
  }

  # Pass ONLY their own Athena-for-Spark execution role, and only to Athena. Athena
  # assumes it to run their notebook Spark sessions; PassRole is checked when they
  # set it on the Spark workgroup.
  statement {
    sid       = "PassOwnSparkRole"
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.spark_exec[each.key].arn]
    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"
      values   = ["athena.amazonaws.com"]
    }
  }
  statement {
    sid = "AthenaList"
    # These Athena list/read actions require a "*" resource (not workgroup-scopable).
    actions = [
      "athena:ListWorkGroups", "athena:ListDataCatalogs",
      "athena:ListEngineVersions", "athena:ListTagsForResource",
    ]
    resources = ["*"]
  }

  # Own Glue database + its tables (for defining tables over datasets). Read the
  # rest of the catalog (e.g. instructor-shared datasets).
  statement {
    sid = "GlueOwnDatabase"
    actions = [
      "glue:CreateDatabase", "glue:DeleteDatabase", "glue:UpdateDatabase",
      "glue:CreateTable", "glue:DeleteTable", "glue:UpdateTable", "glue:BatchCreatePartition",
      "glue:GetDatabase", "glue:GetDatabases", "glue:GetTable", "glue:GetTables",
      "glue:GetPartition", "glue:GetPartitions",
      "glue:TagResource", "glue:UntagResource", "glue:GetTags",
    ]
    resources = [
      "arn:aws:glue:*:*:catalog",
      "arn:aws:glue:*:*:database/${var.resource_prefix}_${each.key}",
      "arn:aws:glue:*:*:table/${var.resource_prefix}_${each.key}/*",
      # Create/DeleteDatabase cascade-check these child resource types too.
      "arn:aws:glue:*:*:userDefinedFunction/${var.resource_prefix}_${each.key}/*",
    ]
  }
  # Reading shared datasets requires catalog-wide read (data-only, no writes).
  statement {
    sid       = "GlueCatalogReadAll"
    actions   = ["glue:GetDatabases", "glue:GetTables", "glue:GetTable", "glue:GetDatabase", "glue:GetTags"]
    resources = ["*"]
  }

  # Their own job/query logs.
  statement {
    sid       = "LogsRead"
    actions   = ["logs:GetLogEvents", "logs:DescribeLogStreams", "logs:DescribeLogGroups"]
    resources = ["*"]
  }

  # Change their own console password (required reset on first login when console
  # access is enabled). Scoped to their own IAM user.
  statement {
    sid       = "ChangeOwnPassword"
    actions   = ["iam:ChangePassword", "iam:GetUser"]
    resources = ["arn:aws:iam::*:user/${var.resource_prefix}-student-${each.key}"]
  }
  statement {
    sid       = "ReadPasswordPolicy"
    actions   = ["iam:GetAccountPasswordPolicy"]
    resources = ["*"]
  }
}

# Managed policy (not inline) so it fits IAM size limits and attaches to both the
# student role and - optionally - the student IAM user (05).
resource "aws_iam_policy" "student" {
  for_each = toset(var.students)
  name     = "${var.resource_prefix}-student-${each.key}"
  policy   = data.aws_iam_policy_document.student_policy[each.key].json
}

resource "aws_iam_role_policy_attachment" "student" {
  for_each   = toset(var.students)
  role       = aws_iam_role.student[each.key].name
  policy_arn = aws_iam_policy.student[each.key].arn
}
