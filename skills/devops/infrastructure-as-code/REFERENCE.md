# Infrastructure As Code - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [1. Terraform Fundamentals](#1.-terraform-fundamentals)
- [Project Structure](#project-structure)
- [Provider Configuration](#provider-configuration)
- [Resources and Data Sources](#resources-and-data-sources)
- [2. Module Development](#2.-module-development)
- [Module Structure](#module-structure)
- [Module Versioning](#module-versioning)
- [3. State Management](#3.-state-management)
- [S3 Backend Configuration](#s3-backend-configuration)
- [Backend Initialization Script](#backend-initialization-script)

---

## Code Examples

### Example 0

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   └── database/
├── backend.tf
├── providers.tf
└── versions.tf
```

### Example 1

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

# providers.tf
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Terraform   = "true"
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

provider "aws" {
  alias  = "secondary"
  region = var.secondary_region
}
```

### Example 2

```hcl
# Data source - query existing resources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Resource - create new infrastructure
resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = module.vpc.private_subnets[0]

  vpc_security_group_ids = [aws_security_group.app.id]

  user_data = templatefile("${path.module}/user-data.sh", {
    environment = var.environment
    app_version = var.app_version
  })

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    encrypted             = true
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [ami]
  }

  tags = {
    Name = "${var.environment}-app-server"
  }
}
```

### Example 3

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-private-${count.index + 1}"
      Type = "private"
    }
  )
}

# modules/vpc/variables.tf
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = []

  validation {
    condition     = length(var.private_subnet_cidrs) <= 10
    error_message = "Maximum of 10 private subnets allowed."
  }
}

variable "availability_zones" {
  description = "Availability zones for subnets"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "private_subnet_cidrs" {
  description = "CIDR blocks of private subnets"
  value       = aws_subnet.private[*].cidr_block
}
```

### Example 4

```hcl
# Using local modules
module "vpc" {
  source = "../../modules/vpc"

  vpc_name             = "${var.environment}-vpc"
  vpc_cidr             = var.vpc_cidr
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones   = var.availability_zones

  tags = local.common_tags
}

# Using registry modules with version pinning
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.environment}-postgres"

  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 100

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  subnet_ids             = module.vpc.private_subnet_ids
  vpc_security_group_ids = [aws_security_group.database.id]

  backup_retention_period = var.environment == "prod" ? 30 : 7
  skip_final_snapshot     = var.environment != "prod"
  deletion_protection     = var.environment == "prod"

  tags = local.common_tags
}
```

### Example 5

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "services/api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abcd1234-..."

    # Prevent accidental state deletion
    skip_credentials_validation = false
    skip_metadata_api_check     = false
    skip_region_validation      = false
  }
}
```

### Example 6

```bash
#!/bin/bash
# scripts/init-backend.sh

set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
STATE_BUCKET="company-terraform-state"
LOCK_TABLE="terraform-state-locks"

# Create S3 bucket for state
aws s3api create-bucket \
  --bucket "$STATE_BUCKET" \
  --region "$AWS_REGION" \
  --create-bucket-configuration LocationConstraint="$AWS_REGION"

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket "$STATE_BUCKET" \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket "$STATE_BUCKET" \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms"
      },
      "BucketKeyEnabled": true
    }]
  }'

# Block public access
aws s3api put-public-access-block \
  --bucket "$STATE_BUCKET" \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name "$LOCK_TABLE" \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region "$AWS_REGION"

echo "Backend resources created successfully"
```

### Example 7

```bash
# View state
terraform state list
terraform state show aws_instance.web

# Move resources between modules
terraform state mv module.old_vpc.aws_vpc.main module.new_vpc.aws_vpc.main

# Remove resource from state (doesn't destroy)
terraform state rm aws_instance.legacy

# Pull remote state locally
terraform state pull > terraform.tfstate.backup

# Push local state to remote
terraform state push terraform.tfstate

# Refresh state
terraform refresh

# Replace resource (force recreation)
terraform apply -replace=aws_instance.web
```

### Example 8

```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch workspace
terraform workspace select prod

# List workspaces
terraform workspace list

# Show current workspace
terraform workspace show
```

### Example 9

```hcl
# main.tf
locals {
  environment = terraform.workspace

  # Environment-specific configuration
  config = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
      db_instance   = "db.t3.micro"
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 2
      max_size      = 4
      db_instance   = "db.t3.small"
    }
    prod = {
      instance_type = "t3.medium"
      min_size      = 3
      max_size      = 10
      db_instance   = "db.r6g.large"
    }
  }

  current_config = local.config[local.environment]

  common_tags = {
    Environment = local.environment
    Terraform   = "true"
    Project     = var.project_name
  }
}

resource "aws_instance" "app" {
  count         = local.current_config.min_size
  ami           = data.aws_ami.ubuntu.id
  instance_type = local.current_config.instance_type

  tags = merge(
    local.common_tags,
    {
      Name = "${local.environment}-app-${count.index + 1}"
    }
  )
}
```

### Example 10

```bash
# Validate syntax and configuration
terraform validate

# Check for errors in expressions
terraform validate -json | jq

# Format code
terraform fmt -recursive -diff

# Check if formatting is needed (CI)
terraform fmt -check -recursive
```

### Example 11

```hcl
# .tflint.hcl
plugin "terraform" {
  enabled = true
  version = "0.5.0"
  source  = "github.com/terraform-linters/tflint-ruleset-terraform"
}

plugin "aws" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_required_version" {
  enabled = true
}

rule "terraform_required_providers" {
  enabled = true
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_typed_variables" {
  enabled = true
}

rule "terraform_unused_declarations" {
  enabled = true
}

rule "terraform_deprecated_interpolation" {
  enabled = true
}

rule "aws_resource_missing_tags" {
  enabled = true
  tags    = ["Environment", "Terraform", "Project"]
}
```

### Example 12

```go
// test/vpc_test.go
package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVPCCreation(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"vpc_name":             "test-vpc",
			"vpc_cidr":             "10.0.0.0/16",
			"availability_zones":   []string{"us-east-1a", "us-east-1b"},
			"private_subnet_cidrs": []string{"10.0.1.0/24", "10.0.2.0/24"},
		},
	}

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

	vpcId := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcId)

	vpcCidr := terraform.Output(t, terraformOptions, "vpc_cidr")
	assert.Equal(t, "10.0.0.0/16", vpcCidr)

	subnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
	assert.Len(t, subnetIds, 2)
}
```

### Example 13

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main, develop]
    paths:
      - 'infrastructure/**'
  pull_request:
    branches: [main]
    paths:
      - 'infrastructure/**'

env:
  TF_VERSION: 1.6.0
  AWS_REGION: us-east-1

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format
        run: terraform fmt -check -recursive
        working-directory: infrastructure

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: infrastructure

      - name: Terraform Validate
        run: terraform validate
        working-directory: infrastructure

      - name: TFLint
        uses: terraform-linters/setup-tflint@v4
        with:
          tflint_version: latest

      - name: Run TFLint
        run: tflint --recursive
        working-directory: infrastructure

  plan:
    needs: validate
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -no-color -out=tfplan
          terraform show -no-color tfplan > plan.txt
        working-directory: infrastructure

      - name: Comment Plan
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('infrastructure/plan.txt', 'utf8');
            const output = `#### Terraform Plan\n\`\`\`\n${plan}\n\`\`\``;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

  apply:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure

      - name: Terraform Apply
        run: terraform apply -auto-approve
        working-directory: infrastructure
```

### Example 14

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply

variables:
  TF_VERSION: 1.6.0
  TF_ROOT: ${CI_PROJECT_DIR}/infrastructure
  TF_STATE_NAME: default

before_script:
  - apk add --no-cache curl
  - curl -o /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip
  - unzip /tmp/terraform.zip -d /usr/local/bin/
  - chmod +x /usr/local/bin/terraform

cache:
  paths:
    - ${TF_ROOT}/.terraform

validate:
  stage: validate
  script:
    - cd ${TF_ROOT}
    - terraform fmt -check -recursive
    - terraform init -backend=false
    - terraform validate
  only:
    changes:
      - infrastructure/**/*

plan:
  stage: plan
  script:
    - cd ${TF_ROOT}
    - terraform init
    - terraform plan -out=tfplan
    - terraform show -no-color tfplan > plan.txt
  artifacts:
    paths:
      - ${TF_ROOT}/tfplan
      - ${TF_ROOT}/plan.txt
    expire_in: 1 week
  only:
    - merge_requests

apply:
  stage: apply
  script:
    - cd ${TF_ROOT}
    - terraform init
    - terraform apply -auto-approve
  dependencies:
    - plan
  only:
    - main
  when: manual
  environment:
    name: production
```

### Example 15

```hcl
# providers.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.azure_subscription_id
}

# main.tf
# AWS Resources
resource "aws_s3_bucket" "data" {
  bucket = "${var.project_name}-data-${var.environment}"

  tags = local.common_tags
}

# Azure Resources
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}"
  location = var.azure_location

  tags = local.common_tags
}

resource "azurerm_storage_account" "data" {
  name                     = "${var.project_name}data${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = local.common_tags
}
```

### Example 16

```hcl
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket" "data" {
  name          = "${var.project_name}-data-${var.environment}"
  location      = var.gcp_region
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  labels = {
    environment = var.environment
    terraform   = "true"
    project     = var.project_name
  }
}

resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-${var.environment}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "private" {
  name          = "${var.project_name}-private-${var.environment}"
  ip_cidr_range = var.gcp_subnet_cidr
  region        = var.gcp_region
  network       = google_compute_network.vpc.id

  private_ip_google_access = true
}
```

### Example 17

```hcl
# Using AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/master-password"
}

resource "aws_db_instance" "main" {
  identifier = "${var.environment}-postgres"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class

  username = var.db_username
  password = data.aws_secretsmanager_secret_version.db_password.secret_string

  # Other configuration...
}

# Using environment variables
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# Store in terraform.tfvars (git-ignored)
# db_password = "actual-password"

# Or pass via environment: TF_VAR_db_password=password terraform apply
```

### Example 18

```hcl
# Least privilege IAM policy
data "aws_iam_policy_document" "app" {
  statement {
    sid    = "AllowS3Read"
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.data.arn,
      "${aws_s3_bucket.data.arn}/*",
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:RequestedRegion"
      values   = [var.aws_region]
    }
  }

  statement {
    sid    = "AllowKMSDecrypt"
    effect = "Allow"

    actions = [
      "kms:Decrypt",
      "kms:DescribeKey",
    ]

    resources = [aws_kms_key.data.arn]
  }
}

resource "aws_iam_policy" "app" {
  name        = "${var.environment}-app-policy"
  description = "Policy for ${var.environment} application"
  policy      = data.aws_iam_policy_document.app.json
}
```

### Example 19

```hcl
# KMS key for encryption
resource "aws_kms_key" "data" {
  description             = "KMS key for ${var.environment} data encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = local.common_tags
}

resource "aws_kms_alias" "data" {
  name          = "alias/${var.environment}-data"
  target_key_id = aws_kms_key.data.key_id
}

# S3 bucket with encryption
resource "aws_s3_bucket" "data" {
  bucket = "${var.project_name}-data-${var.environment}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
    bucket_key_enabled = true
  }
}

# RDS encryption
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-postgres"

  storage_encrypted = true
  kms_key_id        = aws_kms_key.data.arn

  # Other configuration...
}
```

### Example 20

```bash
#!/bin/bash
# scripts/detect-drift.sh

set -euo pipefail

ENVIRONMENT="${1:-dev}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"

echo "Detecting drift in $ENVIRONMENT environment..."

# Select workspace
terraform workspace select "$ENVIRONMENT"

# Refresh state
terraform refresh

# Generate plan
terraform plan -detailed-exitcode -out=drift-plan.tfplan > drift-plan.txt 2>&1 || EXIT_CODE=$?

# Exit codes: 0 = no changes, 1 = error, 2 = changes detected
if [ "${EXIT_CODE:-0}" -eq 2 ]; then
  echo "⚠️  Drift detected in $ENVIRONMENT!"

  # Parse changes
  CHANGES=$(grep -E '^\s+(~|\+|\-)' drift-plan.txt | wc -l)

  MESSAGE="Drift detected in $ENVIRONMENT environment: $CHANGES changes found"

  # Send notification
  if [ -n "$SLACK_WEBHOOK" ]; then
    curl -X POST "$SLACK_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{\"text\":\"$MESSAGE\",\"attachments\":[{\"text\":\"$(cat drift-plan.txt)\"}]}"
  fi

  echo "$MESSAGE"
  cat drift-plan.txt

  exit 2
elif [ "${EXIT_CODE:-0}" -eq 1 ]; then
  echo "❌ Error running terraform plan"
  exit 1
else
  echo "✅ No drift detected in $ENVIRONMENT"
  exit 0
fi
```

### Example 21

```bash
#!/bin/bash
# scripts/remediate-drift.sh

set -euo pipefail

ENVIRONMENT="${1:-dev}"
AUTO_APPROVE="${AUTO_APPROVE:-false}"

echo "Remediating drift in $ENVIRONMENT environment..."

terraform workspace select "$ENVIRONMENT"

if [ "$AUTO_APPROVE" = "true" ]; then
  terraform apply -auto-approve
else
  terraform apply
fi

echo "✅ Drift remediated in $ENVIRONMENT"
```

### Example 23

```hcl
variable "ingress_rules" {
  description = "Ingress rules for security group"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = []
}

resource "aws_security_group" "app" {
  name        = "${var.environment}-app-sg"
  description = "Security group for application"
  vpc_id      = module.vpc.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = local.common_tags
}
```

### Example 24

```hcl
locals {
  # Create map from list
  subnet_map = {
    for idx, subnet in aws_subnet.private :
    "private-${idx}" => subnet.id
  }

  # Filter and transform
  production_instances = {
    for name, instance in aws_instance.app :
    name => instance.id
    if instance.tags["Environment"] == "prod"
  }

  # Multiple attributes
  server_configs = [
    for idx in range(var.server_count) : {
      name = "server-${idx + 1}"
      ip   = cidrhost(var.vpc_cidr, idx + 10)
    }
  ]
}
```

### Example 25

```hcl
# Create resource only in production
resource "aws_cloudwatch_log_group" "app" {
  count = var.environment == "prod" ? 1 : 0

  name              = "/aws/app/${var.environment}"
  retention_in_days = 90

  tags = local.common_tags
}

# Conditional module
module "cdn" {
  source = "./modules/cloudfront"
  count  = var.enable_cdn ? 1 : 0

  domain_name = var.domain_name

  # Other configuration...
}
```

---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
