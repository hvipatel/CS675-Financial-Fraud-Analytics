# Instructor: per-student IAM roles

You apply this ONCE, up front. For each student in the roster it creates three roles:

- **`ds-student-<id>`** - the role the student works as (creds you hand out). Scoped so the student can only:
  - create and use S3 buckets named `ds-<id>-*`,
  - create and manage EMR Serverless apps tagged `Owner=<id>` and run jobs on them,
  - create and use their own Athena workgroups (`ds-<id>` for SQL, `ds-<id>-spark` for notebooks) and their own Glue database `ds_<id>`,
  - pass only their own EMR and Spark execution roles,
  - read the shared Glue catalog (for instructor-shared datasets).
- **`ds-emr-exec-<id>`** - the role EMR Serverless assumes to run that student's Spark jobs; reads and writes only `ds-<id>-*` buckets.
- **`ds-spark-exec-<id>`** - the role Athena assumes to run that student's notebook Spark sessions; same S3 and Glue scope.

Isolation model: S3 by name prefix (`ds-<id>-*`), EMR Serverless by `Owner=<id>` tag, Athena and Glue by resource name. Each student is one set of Terraform resources you can grep for.

## Teacher lifecycle

| Stage | What you do |
|-------|-------------|
| **Provision** (once) | Set the roster, `terraform apply`, optionally mint per-student access keys. |
| **Hand out** | Give each student their role ARNs (and access keys, if minted). |
| **During the course** | Students work in `../student-workspace/` on their own. Add or remove a student by editing the roster and re-applying - `for_each` touches only that student. |
| **End of course** | Delete or rotate the access keys, then `terraform destroy` to remove all per-student roles. |

## Provision

```bash
cp terraform.tfvars.example terraform.tfvars   # set your roster (dummy usernames are fine)
terraform init
terraform plan
terraform apply
terraform output students     # -> per-student role ARNs to hand out
```

Give each student their `student_role_arn`, plus their `emr_exec_role_arn` (passed when submitting EMR jobs) and `spark_exec_role_arn` (passed when enabling the notebook). State is local by default; see `00-provider.tf` to point at your own S3 backend instead.

## Hand out logins and credentials (optional)

Set `create_student_users = true` to also make one IAM **user + access key per student**, straight from the roster - the scoped policy attaches to the user, so the keys work immediately (no assume-role step). Dummy usernames are fine for testing (any valid lowercase id of letters, digits, hyphens, e.g. `student1`, `team-a`).

```bash
terraform apply -var 'create_student_users=true'
terraform output -json student_credentials   # SENSITIVE - per-student access_key_id + secret_access_key
```

Distribute each student their key pair securely, and **delete or rotate the keys after the course**. The roster is a `for_each` list, so adding or removing usernames and re-applying creates or removes only those users and roles.

### Web-console logins (for the browser notebook)

Access keys cover the CLI. To also let students **sign in to the AWS web console** - which the browser Athena-for-Spark notebook (`make notebook`) requires - set `enable_console_login = true` (needs `create_student_users = true`):

```bash
terraform apply -var 'create_student_users=true' -var 'enable_console_login=true'
terraform output -json student_console_logins   # SENSITIVE - console_url, username, initial_password
```

Each student gets a console username and a one-time password (they must set their own on first login; the student policy grants that). The sign-in URL is the same for everyone. Consider requiring MFA for real cohorts.

Your own identity needs `iam:CreateLoginProfile` (and the matching `Get`/`Update`/`DeleteLoginProfile` for the full lifecycle) to create these. An **AdministratorAccess** identity has it; a narrowly scoped provisioning user may not.

## Destroy (end of course)

```bash
terraform destroy -var 'create_student_users=true'   # match the flags you applied with
```

This removes all per-student roles, users, and keys. Have students `make destroy` their own workspaces first (that clears their S3 buckets and EMR apps).

## Notes

- Verified end to end against a live account (apply -> student provision -> Athena query -> EMR Spark job -> notebook Spark session -> full destroy, no leftovers). Still run a `plan` in your own account first.
- IAM policy changes take up to ~60s to propagate. If you tweak the student policy and a student hits a transient `AccessDenied` immediately after, wait a minute and retry. Applied once up front, this never surfaces.
- EMR Serverless can't be name-scoped at create time, so ownership is enforced with the `Owner=<id>` tag; the student workspace sets that tag automatically.
- Trust defaults to the account root; set `assume_role_principal_arns` to each student's real principal to tighten.
- Region is `us-east-2`. Add account-level AWS Budgets as a cost backstop (the student Athena workgroup already caps per-query scans).
