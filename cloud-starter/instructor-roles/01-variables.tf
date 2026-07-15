variable "region" {
  description = "AWS region to create the per-student roles in."
  type        = string
  default     = "us-east-2"
}

variable "resource_prefix" {
  description = "Naming prefix for all per-student resources. A student may only touch resources named <prefix>-<id>-* (S3) or tagged Owner=<id> (EMR Serverless)."
  type        = string
  default     = "ds"
}

variable "students" {
  description = "List of student ids/usernames. Each gets one IAM role (assumed by the student), one EMR Serverless execution role (assumed by EMR to run their jobs), and one Athena-for-Spark execution role (assumed by Athena to run their notebook sessions)."
  type        = list(string)
  # Example: ["man3076", "jbeckford0057", ...]
}

variable "create_student_users" {
  description = "If true, also create an IAM user + access key per student (programmatic creds you hand out). The scoped student policy is attached directly to the user, so the keys work immediately - no assume-role step. Set false if students bring their own identities and only assume the role."
  type        = bool
  default     = false
}

variable "enable_console_login" {
  description = "If true (and create_student_users = true), also give each student a web-console password so they can sign in to the AWS console (needed for the browser Athena-for-Spark notebook). Passwords are output sensitively and a reset is required on first login."
  type        = bool
  default     = false
}

variable "assume_role_principal_arns" {
  description = "ARNs allowed to assume the per-student roles (e.g. each student's IAM user or an SSO principal). If empty, defaults to the account root so the instructor can grant assume access separately."
  type        = list(string)
  default     = []
}
