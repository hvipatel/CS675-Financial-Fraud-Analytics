#!/usr/bin/env bash
# Run sample_query.sql in your Athena workgroup, wait, and print the results.
set -euo pipefail

WG="$(terraform output -raw athena_workgroup)"
DB="$(terraform output -raw glue_database)"

qid=$(aws athena start-query-execution \
  --work-group "$WG" \
  --query-execution-context "Database=$DB" \
  --query-string "$(cat sample_query.sql)" \
  --query 'QueryExecutionId' --output text)

echo "Submitted query $qid to workgroup $WG (database $DB) ..."
while :; do
  state=$(aws athena get-query-execution --query-execution-id "$qid" \
    --query 'QueryExecution.Status.State' --output text)
  case "$state" in
    SUCCEEDED|FAILED|CANCELLED) break ;;
  esac
  sleep 2
done

echo "Status: $state"
if [ "$state" = "SUCCEEDED" ]; then
  aws athena get-query-results --query-execution-id "$qid" --output table
else
  aws athena get-query-execution --query-execution-id "$qid" \
    --query 'QueryExecution.Status.StateChangeReason' --output text
fi
