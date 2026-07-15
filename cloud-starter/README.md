# Cloud Starter - Big Data Analytics on AWS

A small, publishable starter for running analytics on large data in AWS. It gives each student their own isolated sandbox (S3 storage + interactive SQL, with optional Spark) that they build on step by step. This is the "easiest working version" for the CS-675 final project.

**No secrets here.** This directory is Terraform code + shell scripts only - no AWS keys, no credentials, no Terraform state. You run it against **your own** AWS account with **your own** credentials. State files, `terraform.tfvars`, and provider caches are gitignored, so nothing sensitive is ever published.

## Two parts

| Dir | Who runs it | What it does |
|-----|-------------|--------------|
| `instructor-roles/` | Instructor, once | Creates a per-student IAM role (and optionally an IAM user + access key) plus an EMR execution role, from a roster. Hands out scoped credentials. |
| `student-workspace/` | Each student | `make apply` to create their S3 bucket + Athena workgroup (+ optional EMR Serverless), `make query` (SQL), `make submit` (PySpark), `make destroy` when done. |

## How it works

- **Isolation:** each student can only touch S3 buckets named `ds-<id>-*` and EMR Serverless apps tagged `Owner=<id>`. One IAM role/user per student (greppable, simple).
- **Athena-first:** interactive SQL over S3 is the default analytics path - fastest feedback, scan-capped for cost. EMR Serverless (Spark) is one flag away for heavier PySpark, and a browser PySpark notebook (Athena for Spark) is another flag away for students who prefer a Jupyter-style UI over the CLI.
- **Cost guardrails:** Athena per-query scan cap, EMR capacity cap + idle auto-stop, and `make destroy` to tear everything down. (Add account-level AWS Budgets as a backstop.)

## Prerequisites

Install the **AWS CLI** and **Terraform 1.5+**, and configure AWS credentials. Each guide below is the single home for its detail - this README just links them:

- **New to AWS or the command line?** Start with [`AWS-SETUP.md`](AWS-SETUP.md): create an account, make an access key, install the AWS CLI and Terraform, verify your credentials, and learn the Terraform workflow.
- **Instructor** (you own the account): provision the roles and hand out credentials - see [`instructor-roles/Readme.md`](instructor-roles/Readme.md).
- **Student** (you were handed credentials): configure them and run your workspace - see [`student-workspace/Readme.md`](student-workspace/Readme.md).

## Deploy and test (end to end)

The one integrated flow across both dirs. Each step's detail is in the linked guides above.

```bash
# 1. Instructor: create roles/creds (once)
cd instructor-roles && terraform init && terraform apply
terraform apply -var 'create_student_users=true'      # optional: mint per-student keys
terraform output -json student_credentials            # hand out

# 2. Student: stand up your sandbox (with your creds)
cd ../student-workspace
echo 'student_id = "man3076"' > terraform.tfvars
make init && make apply

# 3. Put data in S3 and check it
make put SRC=./trips.parquet DST=data/trips.parquet
make ls

# 4. Run analytics: make query (SQL) | make submit (PySpark) | make notebook (browser)
#    Paths, flags, and options are in student-workspace/Readme.md.
make query

# 5. Tear down (saves cost)
make destroy
```

## Reusing the course's PySpark scripts

The local PySpark scripts in `../code-starter/work/` (word count, taxi analysis, data prep, classification) are reusable here as **EMR Serverless jobs** with two small changes: point inputs/outputs at `s3://...` paths, and let EMR provide the SparkSession (plain `SparkSession.builder.getOrCreate()`, drop the local-mode/event-log config). `student-workspace/sample_job.py` mirrors that pattern - copy a script, swap the paths, `make submit`.

## Status

End-to-end verified against a live AWS account with dummy students: instructor `apply` (roles + user + key), student `apply` (S3 + Athena + Glue + EMR + notebook), data upload, an Athena query, a real EMR Serverless PySpark job (SUCCESS, output written to S3), an Athena-for-Spark notebook session running PySpark, and full `destroy` of both dirs leaving zero leftover resources.

One thing to expect: IAM changes to the student policy take up to ~60s to propagate. If you tweak `instructor-roles/` and immediately re-run a student action, you may hit a transient `AccessDenied` - wait a minute and retry. In a normal cohort run (policy applied once, up front) this never surfaces.

Open follow-ups: AWS Budgets backstop, a curated shared dataset location. The EMR `release_label` (`emr-7.1.0`) is confirmed working.
