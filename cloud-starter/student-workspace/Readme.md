# Student workspace - the easiest working version

This is your sandbox. It stands up storage + an interactive query engine on AWS,
so you can run analytics on large data. It is the **easiest working version** on
purpose - get it running first, then use AI to extend it step by step, testing as
you go.

## What it creates

- **S3 bucket** `ds-<id>-workspace` - your storage (data, scripts, results).
- **Athena workgroup** `ds-<id>` - interactive SQL over S3 data (the easy default), scan-capped.
- **Glue database** `ds_<id>` - where you define tables over datasets.
- **EMR Serverless app** (optional, `enable_emr=true`) - an elastic serverless Spark cluster for PySpark.
- **Spark notebook workgroup** `ds-<id>-spark` (optional, `enable_notebook=true`) - a browser PySpark notebook.

## Pick your path

All three paths read the same data in your S3 bucket. Start with SQL; turn the
others on when you need them.

| You want to | Turn on | Run it with |
|-------------|---------|-------------|
| Query data with SQL | nothing (on by default) | `make query` |
| Run PySpark jobs at scale | `enable_emr = true` | `make submit` |
| Code in a browser notebook | `enable_notebook = true` | `make notebook` |

Your whole loop is the same each time: **provision** (`make apply`) -> **load data**
(`make put`) -> **run** (query / submit / notebook) -> **tear down** (`make destroy`).

## Set up and validate your AWS credentials

Your instructor hands you an **access key id** and a **secret access key** for your
`ds-student-<id>` account. Do this once, before anything else.

**1. Configure them in a named profile** (so they don't clash with other AWS setups):

```bash
aws configure --profile ds
#   AWS Access Key ID     [None]: <paste your access key id>
#   AWS Secret Access Key [None]: <paste your secret access key>
#   Default region name   [None]: us-east-2
#   Default output format [None]: json

export AWS_PROFILE=ds        # use this profile for the rest of the session
```

**2. Validate them** - run this and read the output:

```bash
make whoami       # or:  aws sts get-caller-identity
```

You should see your identity, with an ARN ending in **`user/ds-student-<your-id>`**.
That means your keys are saved and working. Two more quick checks:

```bash
aws configure get region --profile ds     # should print: us-east-2
aws s3 ls                                  # should run WITHOUT "AccessDenied" (empty list is fine)
```

**If validation fails**, match the error:

| Error | What it means | Fix |
|-------|---------------|-----|
| `Unable to locate credentials` | Profile not set or not exported | Re-run `aws configure --profile ds`, then `export AWS_PROFILE=ds` |
| `InvalidClientTokenId` / `SignatureDoesNotMatch` | Key or secret mistyped | Re-run `aws configure --profile ds` and paste carefully |
| ARN shows a different user | A different AWS profile is active | `export AWS_PROFILE=ds` (or check `echo $AWS_PROFILE`) |

## Setup (provision)

Once your credentials validate, set your id and apply:

```bash
echo 'student_id = "<your-username>"' > terraform.tfvars   # e.g. man3076
make init
make apply
```

## Run analytics (start here - Athena)

- Edit `sample_query.sql` (define a table over a dataset, then query it).
- Run it and see results:
  ```bash
  make query
  ```

## Working with your data in S3

`make apply` creates your bucket. Common operations:

```bash
make ls                                                # list everything in your bucket
make put SRC=./trips.parquet DST=data/trips.parquet    # upload a file
make get SRC=output/part-0.parquet DST=./out.parquet   # download a file
make rm  P=data/trips.parquet                          # delete a file

# folders:
aws s3 cp ./mydir s3://$(terraform output -raw bucket)/data/ --recursive   # upload a folder
aws s3 rm  s3://$(terraform output -raw bucket)/data/ --recursive          # delete a folder
```

Then point Athena (`sample_query.sql` LOCATION) or Spark (`sample_job.py` INPUT) at `s3://<your-bucket>/data/...`.

## Optional: PySpark on EMR Serverless

- Re-apply with EMR on and your execution role:
  ```bash
  # in terraform.tfvars:  enable_emr = true
  #                       emr_exec_role_arn = "<your emr_exec_role_arn from the instructor>"
  make apply
  ```
- Develop/test `sample_job.py` locally on a small sample first, then submit at scale:
  ```bash
  make submit
  ```

## Optional: browser notebook UI (Athena for Spark)

Prefer a Jupyter-style notebook over the CLI? Turn on an Athena-for-Spark workgroup
and you get a browser PySpark notebook - no cluster to manage. This path runs in the
AWS web console, so you need a console login from your instructor (the username and
password from `enable_console_login`), not just your access keys.

```bash
# in terraform.tfvars:  enable_notebook     = true
#                       spark_exec_role_arn = "<your spark_exec_role_arn from the instructor>"
make apply
make notebook            # prints your workgroup name + the console URL
```

Then in the AWS console open **Athena -> Notebook editor**, pick your
`ds-<id>-spark` workgroup, and create a notebook. Write PySpark cells against your
S3 data (`s3://<your-bucket>/data/...`) and run them interactively. Stop the
session when you step away - notebook sessions bill for compute while open.

## When you're done

```bash
make destroy
```
Tearing down when you're not using it keeps costs near zero. This deletes the
notebook workgroup too; end any open notebook session first.

## How to work: AI, step by step

Build this up incrementally with an AI assistant: change one thing (a column, a
filter, a new dataset, a join), test it (a quick Athena query or a local Spark run
on a sample), confirm it works, then move on. Keep your working scripts - they are
what you present at the demo.
