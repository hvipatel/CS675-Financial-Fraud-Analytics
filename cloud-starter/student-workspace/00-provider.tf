terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # Local state by default: each student keeps their own terraform.tfstate here.
}

provider "aws" {
  region = var.region

  # Owner tag is REQUIRED: your handed-out role only lets you create/manage
  # resources tagged Owner=<your id>. default_tags stamps it on everything.
  default_tags {
    tags = {
      Project   = "ds-studio"
      Course    = "CS-675"
      Component = "student-workspace"
      Owner     = var.student_id
      ManagedBy = "Terraform"
    }
  }
}
