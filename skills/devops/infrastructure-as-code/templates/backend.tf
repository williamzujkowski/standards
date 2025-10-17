# Backend Configuration for Remote State Storage
# This file configures Terraform to store state remotely in S3 with DynamoDB locking

terraform {
  backend "s3" {
    # S3 bucket for state storage
    bucket = "company-terraform-state"

    # Path to state file within bucket
    # Use a hierarchical structure for organization
    key = "environments/${var.environment}/terraform.tfstate"

    # AWS region for S3 bucket
    region = "us-east-1"

    # Enable server-side encryption
    encrypt = true

    # KMS key for encryption (optional, uses default if not specified)
    kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/abcd1234-5678-90ef-ghij-klmnopqrstuv"

    # DynamoDB table for state locking
    dynamodb_table = "terraform-state-locks"

    # Workspace key prefix for multi-workspace configurations
    workspace_key_prefix = "workspaces"

    # Security settings
    skip_credentials_validation = false
    skip_metadata_api_check     = false
    skip_region_validation      = false

    # ACL for state file (use 'bucket-owner-full-control' for cross-account)
    acl = "private"
  }
}

# Alternative: Backend configuration via backend config file
# Usage: terraform init -backend-config=backend-dev.hcl

# backend-dev.hcl
# bucket         = "company-terraform-state-dev"
# key            = "dev/terraform.tfstate"
# region         = "us-east-1"
# encrypt        = true
# dynamodb_table = "terraform-locks-dev"

# backend-prod.hcl
# bucket         = "company-terraform-state-prod"
# key            = "prod/terraform.tfstate"
# region         = "us-east-1"
# encrypt        = true
# dynamodb_table = "terraform-locks-prod"

# Terraform Cloud Backend (Alternative)
# terraform {
#   backend "remote" {
#     organization = "your-organization"
#
#     workspaces {
#       name = "production"
#     }
#   }
# }

# Azure Backend (Alternative)
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "terraform-state-rg"
#     storage_account_name = "terraformstate"
#     container_name       = "tfstate"
#     key                  = "prod.terraform.tfstate"
#   }
# }

# GCP Backend (Alternative)
# terraform {
#   backend "gcs" {
#     bucket  = "company-terraform-state"
#     prefix  = "terraform/state"
#   }
# }

# Consul Backend (Alternative for multi-region)
# terraform {
#   backend "consul" {
#     address = "consul.example.com"
#     scheme  = "https"
#     path    = "terraform/state"
#   }
# }

# Local Backend (Development Only - NOT for production)
# terraform {
#   backend "local" {
#     path = "terraform.tfstate"
#   }
# }

# Backend Initialization Script
# Run before first terraform init:
#
# #!/bin/bash
# # init-backend.sh
#
# AWS_REGION="us-east-1"
# STATE_BUCKET="company-terraform-state"
# LOCK_TABLE="terraform-state-locks"
# KMS_KEY_ALIAS="alias/terraform-state"
#
# # Create KMS key
# KMS_KEY_ID=$(aws kms create-key \
#   --description "Terraform state encryption key" \
#   --region $AWS_REGION \
#   --query 'KeyMetadata.KeyId' \
#   --output text)
#
# aws kms create-alias \
#   --alias-name $KMS_KEY_ALIAS \
#   --target-key-id $KMS_KEY_ID \
#   --region $AWS_REGION
#
# # Create S3 bucket
# aws s3api create-bucket \
#   --bucket $STATE_BUCKET \
#   --region $AWS_REGION \
#   --create-bucket-configuration LocationConstraint=$AWS_REGION
#
# # Enable versioning
# aws s3api put-bucket-versioning \
#   --bucket $STATE_BUCKET \
#   --versioning-configuration Status=Enabled
#
# # Enable encryption
# aws s3api put-bucket-encryption \
#   --bucket $STATE_BUCKET \
#   --server-side-encryption-configuration '{
#     "Rules": [{
#       "ApplyServerSideEncryptionByDefault": {
#         "SSEAlgorithm": "aws:kms",
#         "KMSMasterKeyID": "'$KMS_KEY_ID'"
#       },
#       "BucketKeyEnabled": true
#     }]
#   }'
#
# # Block public access
# aws s3api put-public-access-block \
#   --bucket $STATE_BUCKET \
#   --public-access-block-configuration \
#     BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
#
# # Enable logging
# aws s3api put-bucket-logging \
#   --bucket $STATE_BUCKET \
#   --bucket-logging-status '{
#     "LoggingEnabled": {
#       "TargetBucket": "'$STATE_BUCKET'-logs",
#       "TargetPrefix": "s3-access-logs/"
#     }
#   }'
#
# # Create DynamoDB table for locking
# aws dynamodb create-table \
#   --table-name $LOCK_TABLE \
#   --attribute-definitions AttributeName=LockID,AttributeType=S \
#   --key-schema AttributeName=LockID,KeyType=HASH \
#   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
#   --region $AWS_REGION \
#   --tags Key=Purpose,Value=TerraformStateLocking
#
# # Enable point-in-time recovery
# aws dynamodb update-continuous-backups \
#   --table-name $LOCK_TABLE \
#   --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
#   --region $AWS_REGION
#
# echo "Backend resources created successfully"
# echo "S3 Bucket: $STATE_BUCKET"
# echo "DynamoDB Table: $LOCK_TABLE"
# echo "KMS Key ID: $KMS_KEY_ID"

# State Migration
# To migrate from local to remote backend:
#
# 1. Add backend configuration to this file
# 2. Run: terraform init -migrate-state
# 3. Confirm migration when prompted
# 4. Verify: terraform state list
# 5. Delete local state file after verification

# State Locking
# The DynamoDB table prevents concurrent state modifications
# Lock entry format:
# {
#   "LockID": "bucket/path/to/terraform.tfstate-md5",
#   "Info": "{...}",
#   "Who": "user@host",
#   "Version": "1.6.0",
#   "Created": "2024-01-15T10:30:00Z",
#   "Operation": "OperationTypeApply",
#   "Path": "bucket/path/to/terraform.tfstate"
# }

# Force Unlock (Emergency Only)
# If a lock is stuck (e.g., process crashed):
# terraform force-unlock LOCK_ID

# Best Practices:
# 1. Never store backend config in version control (use -backend-config)
# 2. Enable versioning on state bucket
# 3. Enable encryption at rest
# 4. Use separate buckets per environment
# 5. Implement least-privilege IAM policies
# 6. Enable MFA delete protection for production
# 7. Set up bucket lifecycle policies
# 8. Monitor state file access with CloudTrail
# 9. Regular state backups
# 10. Document state recovery procedures
