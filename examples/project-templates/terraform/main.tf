# Terraform configuration following DEVOPS_PLATFORM_STANDARDS.md and CLOUD_NATIVE_STANDARDS.md

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
  
  # Backend configuration for state management
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Security: Server-side encryption
    server_side_encryption_configuration {
      rule {
        apply_server_side_encryption_by_default {
          sse_algorithm = "AES256"
        }
      }
    }
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
  
  # Security: Default tags for all resources
  default_tags {
    tags = local.common_tags
  }
  
  # Security: Assume role for least privilege
  assume_role {
    role_arn = var.terraform_role_arn
  }
}

# Local variables for common tags (per COST_OPTIMIZATION_STANDARDS.md)
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CostCenter  = var.cost_center
    Owner       = var.owner_email
    CreatedAt   = timestamp()
  }
  
  name_prefix = "${var.project_name}-${var.environment}"
}

# VPC Module following CLOUD_NATIVE_STANDARDS.md
module "vpc" {
  source = "./modules/vpc"
  
  name_prefix          = local.name_prefix
  vpc_cidr            = var.vpc_cidr
  availability_zones  = var.availability_zones
  
  # Network segmentation
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  database_subnet_cidrs = var.database_subnet_cidrs
  
  # Security
  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"
  enable_vpn_gateway = var.enable_vpn
  enable_flow_logs   = true
  
  tags = local.common_tags
}

# EKS Cluster following CLOUD_NATIVE_STANDARDS.md
module "eks" {
  source = "./modules/eks"
  
  cluster_name    = "${local.name_prefix}-eks"
  cluster_version = var.eks_cluster_version
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  # Node groups with auto-scaling
  node_groups = {
    general = {
      desired_capacity = var.eks_node_desired_capacity
      max_capacity     = var.eks_node_max_capacity
      min_capacity     = var.eks_node_min_capacity
      
      instance_types = ["t3.medium"]
      
      # Cost optimization: Spot instances
      capacity_type = var.environment == "production" ? "ON_DEMAND" : "SPOT"
      
      # Security: Launch template with security hardening
      launch_template = {
        name            = "${local.name_prefix}-eks-node"
        use_name_prefix = true
        
        block_device_mappings = {
          xvda = {
            device_name = "/dev/xvda"
            ebs = {
              volume_size           = 100
              volume_type           = "gp3"
              encrypted             = true
              kms_key_id           = module.kms.key_arn
              delete_on_termination = true
            }
          }
        }
        
        # Security: IMDSv2 required
        metadata_options = {
          http_endpoint               = "enabled"
          http_tokens                 = "required"
          http_put_response_hop_limit = 1
        }
      }
      
      tags = merge(local.common_tags, {
        NodeGroup = "general"
      })
    }
  }
  
  # RBAC configuration
  manage_aws_auth_configmap = true
  aws_auth_roles = var.eks_auth_roles
  
  # Encryption
  cluster_encryption_config = [{
    provider_key_arn = module.kms.key_arn
    resources        = ["secrets"]
  }]
  
  # Logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  tags = local.common_tags
}

# KMS Key for encryption (per MODERN_SECURITY_STANDARDS.md)
module "kms" {
  source = "./modules/kms"
  
  alias_name  = "alias/${local.name_prefix}"
  description = "KMS key for ${var.project_name} ${var.environment}"
  
  # Key rotation
  enable_key_rotation = true
  
  # Key policy
  key_administrators = var.kms_key_administrators
  key_users          = concat(var.kms_key_users, [module.eks.cluster_iam_role_arn])
  
  tags = local.common_tags
}

# RDS Database following DATA_ENGINEERING_STANDARDS.md
module "rds" {
  source = "./modules/rds"
  
  identifier = "${local.name_prefix}-db"
  
  # Engine configuration
  engine               = "postgres"
  engine_version       = var.rds_engine_version
  instance_class       = var.rds_instance_class
  allocated_storage    = var.rds_allocated_storage
  storage_encrypted    = true
  kms_key_id          = module.kms.key_arn
  
  # High availability
  multi_az               = var.environment == "production"
  backup_retention_period = var.environment == "production" ? 30 : 7
  
  # Security
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.database_subnet_ids
  allowed_security_group_ids = [module.eks.node_security_group_id]
  
  # Monitoring per OBSERVABILITY_STANDARDS.md
  enabled_cloudwatch_logs_exports = ["postgresql"]
  performance_insights_enabled    = true
  monitoring_interval            = 60
  
  # Cost optimization
  deletion_protection = var.environment == "production"
  skip_final_snapshot = var.environment != "production"
  
  tags = local.common_tags
}

# S3 Buckets for application data
module "s3_buckets" {
  source = "./modules/s3"
  
  buckets = {
    assets = {
      name = "${local.name_prefix}-assets"
      
      # Versioning for data protection
      versioning = {
        enabled = true
      }
      
      # Lifecycle rules for cost optimization
      lifecycle_rule = [
        {
          id      = "transition-old-versions"
          enabled = true
          
          noncurrent_version_transition = [
            {
              days          = 30
              storage_class = "STANDARD_IA"
            },
            {
              days          = 90
              storage_class = "GLACIER"
            }
          ]
          
          noncurrent_version_expiration = {
            days = 180
          }
        }
      ]
      
      # Security
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm     = "aws:kms"
            kms_master_key_id = module.kms.key_arn
          }
        }
      }
      
      # Public access block
      block_public_acls       = true
      block_public_policy     = true
      ignore_public_acls      = true
      restrict_public_buckets = true
    }
  }
  
  tags = local.common_tags
}

# Outputs for other modules/applications
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "s3_bucket_names" {
  description = "S3 bucket names"
  value       = module.s3_buckets.bucket_names
}