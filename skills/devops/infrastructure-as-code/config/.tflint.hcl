# TFLint Configuration
# This configuration enables comprehensive linting for Terraform code

# Global Configuration
config {
  # Disable default rules to enable explicit rule selection
  disabled_by_default = false
  
  # Enable module inspection (slower but more thorough)
  module = true
  
  # Force provider initialization for validation
  force = false
  
  # Varfile for validation
  varfile = ["terraform.tfvars"]
}

# Terraform Plugin
plugin "terraform" {
  enabled = true
  version = "0.5.0"
  source  = "github.com/terraform-linters/tflint-ruleset-terraform"
  
  # Plugin configuration
  preset = "recommended"
}

# AWS Plugin
plugin "aws" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
  
  # Deep checking (calls AWS APIs for validation)
  deep_check = false
}

# Azure Plugin (uncomment if using Azure)
# plugin "azurerm" {
#   enabled = true
#   version = "0.25.0"
#   source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
# }

# GCP Plugin (uncomment if using GCP)
# plugin "google" {
#   enabled = true
#   version = "0.26.0"
#   source  = "github.com/terraform-linters/tflint-ruleset-google"
# }

# Terraform Rules
rule "terraform_required_version" {
  enabled = true
}

rule "terraform_required_providers" {
  enabled = true
}

rule "terraform_naming_convention" {
  enabled = true
  
  # Variable naming
  variable {
    format = "snake_case"
  }
  
  # Resource naming
  resource {
    format = "snake_case"
  }
  
  # Data source naming
  data {
    format = "snake_case"
  }
  
  # Local value naming
  locals {
    format = "snake_case"
  }
  
  # Output naming
  output {
    format = "snake_case"
  }
  
  # Module naming
  module {
    format = "snake_case"
  }
}

rule "terraform_typed_variables" {
  enabled = true
}

rule "terraform_unused_declarations" {
  enabled = true
}

rule "terraform_unused_required_providers" {
  enabled = true
}

rule "terraform_deprecated_interpolation" {
  enabled = true
}

rule "terraform_deprecated_index" {
  enabled = true
}

rule "terraform_comment_syntax" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_module_pinned_source" {
  enabled = true
  
  # Module source style
  style = "flexible"
}

rule "terraform_standard_module_structure" {
  enabled = true
}

rule "terraform_workspace_remote" {
  enabled = true
}

# AWS-Specific Rules
rule "aws_resource_missing_tags" {
  enabled = true
  
  # Required tags
  tags = [
    "Environment",
    "Terraform",
    "Project"
  ]
  
  # Resources to exclude from tag checking
  exclude = [
    "aws_route_table",
    "aws_subnet"
  ]
}

rule "aws_db_instance_invalid_type" {
  enabled = true
}

rule "aws_instance_invalid_type" {
  enabled = true
}

rule "aws_elasticache_cluster_invalid_type" {
  enabled = true
}

rule "aws_iam_policy_document_gov_friendly_arns" {
  enabled = false  # Enable if working with AWS GovCloud
}

rule "aws_s3_bucket_public_access_block" {
  enabled = true
}

rule "aws_route_not_specified_target" {
  enabled = true
}

rule "aws_route_specified_multiple_targets" {
  enabled = true
}

# Security Rules
rule "aws_db_instance_default_parameter_group" {
  enabled = true
}

rule "aws_elasticache_cluster_default_parameter_group" {
  enabled = true
}

rule "aws_iam_policy_document_not_action_or_not_resource" {
  enabled = true
}

rule "aws_iam_role_policy_not_action_or_not_resource" {
  enabled = true
}

rule "aws_s3_bucket_versioning_disabled" {
  enabled = false  # Disabled to allow explicit choice
}

rule "aws_security_group_rule_invalid_cidr" {
  enabled = true
}

# Cost Optimization Rules
rule "aws_instance_previous_type" {
  enabled = true
}

rule "aws_db_instance_previous_type" {
  enabled = true
}

# Best Practices
rule "aws_cloudwatch_log_group_retention" {
  enabled = true
}

rule "aws_launch_configuration_ebs_block_device_encrypted" {
  enabled = true
}

rule "aws_ebs_volume_encrypted" {
  enabled = true
}

rule "aws_rds_cluster_encryption" {
  enabled = true
}

rule "aws_s3_bucket_encryption" {
  enabled = true
}

# Custom Rules (examples)
# These would need to be implemented as custom plugins

# rule "custom_naming_prefix" {
#   enabled = true
#   prefix  = "mycompany-"
# }

# rule "custom_required_tags" {
#   enabled = true
#   tags = [
#     "CostCenter",
#     "Owner",
#     "DataClassification"
#   ]
# }

# Ignore Patterns
# Exclude specific files or directories from linting
# ignore_module = {
#   "terraform-aws-modules/vpc/aws" = true
# }

# Custom Variable Files
# varfiles = [
#   "terraform.tfvars",
#   "environments/dev.tfvars",
#   "environments/prod.tfvars"
# ]
