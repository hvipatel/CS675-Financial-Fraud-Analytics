terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # State is local by default. To share it across machines, uncomment and point at
  # your own S3 bucket + DynamoDB lock table, then re-run `terraform init`.
  # backend "s3" {
  #   bucket         = "<your-state-bucket>"
  #   key            = "ds-studio/instructor-roles.tfstate"
  #   region         = "us-east-2"
  #   dynamodb_table = "<your-lock-table>"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = "ds-studio"
      Course    = "CS-675"
      Component = "instructor-roles"
      ManagedBy = "Terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
