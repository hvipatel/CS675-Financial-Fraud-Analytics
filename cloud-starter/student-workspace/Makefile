.PHONY: help whoami init plan apply destroy query submit notebook ls put get rm

BUCKET = $(shell terraform output -raw bucket 2>/dev/null)

help:
	@echo "Creds:  make whoami  (check your AWS credentials are configured)"
	@echo "Infra:  make init | apply | destroy"
	@echo "Data:   make ls | put SRC=<file> DST=<key> | get SRC=<key> DST=<file> | rm P=<key>"
	@echo "Run:    make query  (Athena SQL)  |  make submit  (PySpark on EMR)  |  make notebook  (browser PySpark UI)"

# Check your credentials are configured. Expect an ARN ending in user/ds-student-<your-id>.
whoami:
	@aws sts get-caller-identity --query Arn --output text \
		&& echo "OK - if the ARN above ends in your ds-student-<id>, your credentials are set." \
		|| echo "FAILED - credentials not configured. See 'Set up and validate your AWS credentials' in Readme.md."

init:
	terraform init

plan:
	terraform plan

apply:
	terraform apply

destroy:
	terraform destroy

query:
	./run_query.sh

submit:
	./submit_job.sh

# Open your browser PySpark notebook (needs enable_notebook = true).
notebook:
	@echo "Workgroup: $$(terraform output -raw notebook_workgroup)"
	@echo "Open the AWS console, pick this workgroup in Athena's Notebook editor:"
	@echo "  $$(terraform output -raw notebook_console_url)"

# --- Data in S3 (BUCKET comes from `terraform output`) ---
ls:
	aws s3 ls "s3://$(BUCKET)/" --recursive --human-readable --summarize

# upload a file:  make put SRC=./trips.parquet DST=data/trips.parquet
# (upload a folder:  aws s3 cp ./mydir s3://$(BUCKET)/data/ --recursive)
put:
	aws s3 cp "$(SRC)" "s3://$(BUCKET)/$(DST)"

# download:  make get SRC=output/part.parquet DST=./part.parquet
get:
	aws s3 cp "s3://$(BUCKET)/$(SRC)" "$(DST)"

# delete a key:  make rm P=data/trips.parquet
# (delete a folder:  aws s3 rm s3://$(BUCKET)/data/ --recursive)
rm:
	aws s3 rm "s3://$(BUCKET)/$(P)"
