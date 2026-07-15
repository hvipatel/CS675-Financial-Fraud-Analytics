#!/usr/bin/env bash
# Upload sample_job.py to your bucket and run it on your EMR Serverless app.
# Requires enable_emr=true and your emr_exec_role_arn set.
set -euo pipefail

app="$(terraform output -raw emr_application_id)"
bucket="$(terraform output -raw bucket)"
role="$(terraform output -raw emr_exec_role_arn)"

if [ -z "$app" ] || [ "$app" = "null" ]; then
  echo "No EMR app. Re-apply with enable_emr=true first."; exit 1
fi
if [ -z "$role" ]; then
  echo "emr_exec_role_arn is empty. Set it (from the instructor) and re-apply."; exit 1
fi

aws s3 cp sample_job.py "s3://$bucket/jobs/sample_job.py"

run=$(aws emr-serverless start-job-run \
  --application-id "$app" \
  --execution-role-arn "$role" \
  --job-driver "{\"sparkSubmit\":{\"entryPoint\":\"s3://$bucket/jobs/sample_job.py\"}}" \
  --query 'jobRunId' --output text)

echo "Submitted job $run on app $app."
echo "Check status: aws emr-serverless get-job-run --application-id $app --job-run-id $run --query 'jobRun.state'"
