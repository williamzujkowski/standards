# Output Definitions
# These outputs expose important resource information for other modules or external consumption

# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnets
}

output "database_subnet_ids" {
  description = "List of database subnet IDs"
  value       = module.vpc.database_subnets
}

output "nat_gateway_ids" {
  description = "List of NAT Gateway IDs"
  value       = module.vpc.natgw_ids
}

# Load Balancer Outputs
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = aws_lb.main.arn
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = aws_lb.main.zone_id
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = aws_lb_target_group.app.arn
}

output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

# Auto Scaling Outputs
output "autoscaling_group_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.app.name
}

output "autoscaling_group_arn" {
  description = "ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.app.arn
}

output "launch_template_id" {
  description = "ID of the launch template"
  value       = aws_launch_template.app.id
}

output "launch_template_latest_version" {
  description = "Latest version of the launch template"
  value       = aws_launch_template.app.latest_version
}

# Database Outputs
output "db_instance_id" {
  description = "ID of the RDS instance"
  value       = module.rds.db_instance_id
}

output "db_instance_endpoint" {
  description = "Connection endpoint for the RDS instance"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "db_instance_address" {
  description = "Address of the RDS instance"
  value       = module.rds.db_instance_address
  sensitive   = true
}

output "db_instance_port" {
  description = "Port of the RDS instance"
  value       = module.rds.db_instance_port
}

output "db_instance_name" {
  description = "Name of the database"
  value       = module.rds.db_instance_name
}

output "db_instance_username" {
  description = "Master username for the database"
  value       = module.rds.db_instance_username
  sensitive   = true
}

output "db_subnet_group_name" {
  description = "Name of the DB subnet group"
  value       = module.vpc.database_subnet_group_name
}

# Security Group Outputs
output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = aws_security_group.alb.id
}

output "app_security_group_id" {
  description = "ID of the application security group"
  value       = aws_security_group.app.id
}

output "database_security_group_id" {
  description = "ID of the database security group"
  value       = aws_security_group.database.id
}

# IAM Outputs
output "app_role_arn" {
  description = "ARN of the application IAM role"
  value       = aws_iam_role.app.arn
}

output "app_role_name" {
  description = "Name of the application IAM role"
  value       = aws_iam_role.app.name
}

output "app_instance_profile_arn" {
  description = "ARN of the instance profile"
  value       = aws_iam_instance_profile.app.arn
}

# KMS Outputs
output "kms_key_id" {
  description = "ID of the KMS key"
  value       = aws_kms_key.main.key_id
}

output "kms_key_arn" {
  description = "ARN of the KMS key"
  value       = aws_kms_key.main.arn
}

output "kms_alias_name" {
  description = "Name of the KMS key alias"
  value       = aws_kms_alias.main.name
}

# S3 Outputs
output "logs_bucket_id" {
  description = "ID of the logs S3 bucket"
  value       = aws_s3_bucket.logs.id
}

output "logs_bucket_arn" {
  description = "ARN of the logs S3 bucket"
  value       = aws_s3_bucket.logs.arn
}

# CloudWatch Outputs
output "high_cpu_alarm_arn" {
  description = "ARN of the high CPU alarm"
  value       = aws_cloudwatch_metric_alarm.high_cpu.arn
}

output "low_cpu_alarm_arn" {
  description = "ARN of the low CPU alarm"
  value       = aws_cloudwatch_metric_alarm.low_cpu.arn
}

# Connection Information (for convenience)
output "connection_info" {
  description = "Connection information for the infrastructure"
  value = {
    application_url = "http://${aws_lb.main.dns_name}"
    database_host   = module.rds.db_instance_address
    database_port   = module.rds.db_instance_port
    database_name   = module.rds.db_instance_name
  }
  sensitive = true
}

# Environment Information
output "environment" {
  description = "Current environment name"
  value       = local.environment
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

output "availability_zones" {
  description = "Availability zones used"
  value       = module.vpc.azs
}

# Resource Counts
output "resource_counts" {
  description = "Count of created resources"
  value = {
    private_subnets  = length(module.vpc.private_subnets)
    public_subnets   = length(module.vpc.public_subnets)
    database_subnets = length(module.vpc.database_subnets)
    nat_gateways     = length(module.vpc.natgw_ids)
  }
}

# Tags Output
output "common_tags" {
  description = "Common tags applied to all resources"
  value       = local.common_tags
}

# Cost Allocation
output "cost_allocation_tags" {
  description = "Tags used for cost allocation"
  value = {
    Environment = local.environment
    Project     = var.project_name
    CostCenter  = var.cost_center
  }
}

# Terraform Metadata
output "terraform_workspace" {
  description = "Current Terraform workspace"
  value       = terraform.workspace
}

output "terraform_version" {
  description = "Terraform version used"
  value       = "~> ${replace(terraform.version, "/^([0-9]+\\.[0-9]+).*/", "$1")}"
}

# Module Outputs for Chaining
output "vpc_outputs" {
  description = "All VPC module outputs (for module chaining)"
  value = {
    vpc_id              = module.vpc.vpc_id
    private_subnet_ids  = module.vpc.private_subnets
    public_subnet_ids   = module.vpc.public_subnets
    database_subnet_ids = module.vpc.database_subnets
  }
}

output "security_outputs" {
  description = "Security-related outputs (for module chaining)"
  value = {
    alb_sg_id      = aws_security_group.alb.id
    app_sg_id      = aws_security_group.app.id
    database_sg_id = aws_security_group.database.id
    kms_key_id     = aws_kms_key.main.id
  }
}

# Computed Values
output "full_resource_name_prefix" {
  description = "Full resource name prefix used across all resources"
  value       = local.name_prefix
}

output "is_production" {
  description = "Whether this is a production environment"
  value       = local.is_production
}

# Advanced Outputs with Conditions
output "cdn_endpoint" {
  description = "CloudFront distribution endpoint (if enabled)"
  value       = var.enable_cdn ? "https://example.cloudfront.net" : null
}

output "waf_acl_id" {
  description = "WAF ACL ID (if enabled)"
  value       = var.enable_waf ? "example-waf-acl-id" : null
}

# JSON Output for External Consumption
output "infrastructure_json" {
  description = "Complete infrastructure information in JSON format"
  value = jsonencode({
    environment = local.environment
    region      = var.aws_region
    vpc = {
      id   = module.vpc.vpc_id
      cidr = module.vpc.vpc_cidr_block
    }
    load_balancer = {
      dns_name = aws_lb.main.dns_name
      url      = "http://${aws_lb.main.dns_name}"
    }
    database = {
      endpoint = module.rds.db_instance_endpoint
      name     = module.rds.db_instance_name
    }
    auto_scaling = {
      group_name = aws_autoscaling_group.app.name
      min_size   = aws_autoscaling_group.app.min_size
      max_size   = aws_autoscaling_group.app.max_size
    }
  })
  sensitive = true
}

# Preconditions Example (Terraform 1.5+)
output "validated_environment" {
  description = "Environment name after validation"
  value       = var.environment
  
  precondition {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

# Post-Apply Instructions
output "post_apply_instructions" {
  description = "Instructions to follow after Terraform apply"
  value = <<-EOT
    Infrastructure has been successfully deployed!
    
    Next Steps:
    1. Configure DNS to point to ALB: ${aws_lb.main.dns_name}
    2. Update application configuration with database endpoint
    3. Deploy application code to Auto Scaling Group
    4. Configure monitoring dashboards
    5. Set up alerting for CloudWatch alarms
    
    Database Connection:
      Host: ${module.rds.db_instance_address}
      Port: ${module.rds.db_instance_port}
      Database: ${module.rds.db_instance_name}
      
    Application URL: http://${aws_lb.main.dns_name}
  EOT
}
