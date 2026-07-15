# OPTIONAL: one IAM user + access key per student, created straight from the
# roster (create_student_users = true). Dummy usernames are fine - they are just
# strings. The same scoped policy from 04 is attached directly to the user, so the
# access keys work immediately (no assume-role step needed).
#
# NOTE on usernames: since S3 bucket names derive from the id (ds-<id>-*), keep ids
# lowercase and made of letters/digits/hyphens (e.g. student1, team-a, man3076).

resource "aws_iam_user" "student" {
  for_each = var.create_student_users ? toset(var.students) : []
  name     = "${var.resource_prefix}-student-${each.key}"
}

resource "aws_iam_user_policy_attachment" "student" {
  for_each   = var.create_student_users ? toset(var.students) : []
  user       = aws_iam_user.student[each.key].name
  policy_arn = aws_iam_policy.student[each.key].arn
}

resource "aws_iam_access_key" "student" {
  for_each = var.create_student_users ? toset(var.students) : []
  user     = aws_iam_user.student[each.key].name
}

# OPTIONAL web-console password per student (enable_console_login = true). Lets them
# sign in to the AWS console - required for the browser Athena-for-Spark notebook.
# A reset is required on first login; the student policy (04) grants the self-service
# password-change permissions this needs.
resource "aws_iam_user_login_profile" "student" {
  for_each                = (var.create_student_users && var.enable_console_login) ? toset(var.students) : []
  user                    = aws_iam_user.student[each.key].name
  password_length         = 20
  password_reset_required = true
}

# SENSITIVE. Retrieve with: terraform output -json student_credentials
# Distribute each student their access_key_id + secret_access_key securely, and
# delete/rotate the keys after the course.
output "student_credentials" {
  description = "Per-student AWS access keys (sensitive). Empty unless create_student_users = true."
  sensitive   = true
  value = var.create_student_users ? {
    for id in var.students : id => {
      access_key_id     = aws_iam_access_key.student[id].id
      secret_access_key = aws_iam_access_key.student[id].secret
    }
  } : {}
}

# SENSITIVE. Retrieve with: terraform output -json student_console_logins
# The console sign-in URL is the same for everyone; each student gets a username and
# a one-time password (they set their own on first login). Distribute securely.
output "student_console_logins" {
  description = "Per-student AWS console usernames + initial passwords (sensitive). Empty unless enable_console_login = true."
  sensitive   = true
  value = (var.create_student_users && var.enable_console_login) ? {
    for id in var.students : id => {
      console_url      = "https://${data.aws_caller_identity.current.account_id}.signin.aws.amazon.com/console"
      username         = aws_iam_user.student[id].name
      initial_password = aws_iam_user_login_profile.student[id].password
    }
  } : {}
}
