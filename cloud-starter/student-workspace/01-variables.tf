variable "student_id" {
  description = "Your username (e.g. man3076). Must match the id in your handed-out role."
  type        = string
}

variable "region" {
  description = "AWS region. Must match the region your instructor provisioned the roles in."
  type        = string
  default     = "us-east-2"
}

variable "resource_prefix" {
  description = "Naming prefix your resources must use. Must match the instructor's prefix (your role only allows <prefix>-<id>-* names)."
  type        = string
  default     = "ds"
}

variable "enable_emr" {
  description = "Set true to also spin up an EMR Serverless (Spark) app for PySpark jobs. Leave false if Athena SQL is enough."
  type        = bool
  default     = false
}

variable "emr_exec_role_arn" {
  description = "Your EMR Serverless execution role ARN (from the instructor). Required when enable_emr = true."
  type        = string
  default     = ""
}

variable "enable_notebook" {
  description = "Set true to add an Athena-for-Spark workgroup: a browser Jupyter-style PySpark notebook. Leave false if Athena SQL is enough."
  type        = bool
  default     = false
}

variable "spark_exec_role_arn" {
  description = "Your Athena-for-Spark execution role ARN (from the instructor). Required when enable_notebook = true."
  type        = string
  default     = ""
}

variable "athena_scan_cap_bytes" {
  description = "Per-query Athena scan cap (bytes). Default 1 TB - keeps runaway scans in check."
  type        = number
  default     = 1099511627776
}

variable "emr_max_cpu" {
  description = "Upper bound on total vCPUs the EMR Serverless app can scale to (cost guardrail)."
  type        = number
  default     = 100
}

variable "emr_max_memory_gb" {
  description = "Upper bound on total memory (GB) the EMR Serverless app can scale to (cost guardrail)."
  type        = number
  default     = 400
}
