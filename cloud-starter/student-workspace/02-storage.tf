# Your S3 workspace bucket: holds your data, scripts, Athena results, and job outputs.
locals {
  bucket = "${var.resource_prefix}-${var.student_id}-workspace"
}

resource "aws_s3_bucket" "workspace" {
  bucket        = local.bucket
  force_destroy = true # so `make destroy` can delete the bucket even if it still has objects
}

resource "aws_s3_bucket_public_access_block" "workspace" {
  bucket                  = aws_s3_bucket.workspace.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
