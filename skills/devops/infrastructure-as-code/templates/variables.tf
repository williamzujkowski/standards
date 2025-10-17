# Variable Definitions with Validation and Documentation

# Project Configuration
variable "project_name" {
  description = "Name of the project (used for resource naming and tagging)"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# AWS Configuration
variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
  
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]{1}$", var.aws_region))
    error_message = "AWS region must be a valid region code (e.g., us-east-1)."
  }
}

variable "secondary_region" {
  description = "Secondary AWS region for disaster recovery"
  type        = string
  default     = null
}

# Network Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
  
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
  
  validation {
    condition     = tonumber(split("/", var.vpc_cidr)[1]) <= 16
    error_message = "VPC CIDR block must be /16 or larger."
  }
}

variable "availability_zones" {
  description = "List of availability zones for subnet distribution"
  type        = list(string)
  default     = []
  
  validation {
    condition     = length(var.availability_zones) == 0 || length(var.availability_zones) >= 2
    error_message = "Must specify at least 2 availability zones or leave empty for automatic selection."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = []
  
  validation {
    condition = alltrue([
      for cidr in var.private_subnet_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "All private subnet CIDRs must be valid IPv4 CIDR blocks."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = []
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use single NAT Gateway for cost savings (not recommended for production)"
  type        = bool
  default     = false
}

# Compute Configuration
variable "instance_type" {
  description = "EC2 instance type for application servers"
  type        = string
  default     = "t3.micro"
  
  validation {
    condition = can(regex("^[a-z][0-9][a-z]?\\.[a-z0-9]+$", var.instance_type))
    error_message = "Instance type must be a valid EC2 instance type (e.g., t3.micro, m5.large)."
  }
}

variable "min_size" {
  description = "Minimum number of instances in Auto Scaling Group"
  type        = number
  default     = 1
  
  validation {
    condition     = var.min_size >= 1
    error_message = "Minimum size must be at least 1."
  }
}

variable "max_size" {
  description = "Maximum number of instances in Auto Scaling Group"
  type        = number
  default     = 10
  
  validation {
    condition     = var.max_size >= var.min_size
    error_message = "Maximum size must be greater than or equal to minimum size."
  }
}

variable "desired_capacity" {
  description = "Desired number of instances in Auto Scaling Group (leave null to use min_size)"
  type        = number
  default     = null
  
  validation {
    condition     = var.desired_capacity == null || (var.desired_capacity >= var.min_size && var.desired_capacity <= var.max_size)
    error_message = "Desired capacity must be between min_size and max_size."
  }
}

variable "ami_id" {
  description = "AMI ID for EC2 instances (leave empty to use latest Amazon Linux 2)"
  type        = string
  default     = ""
  
  validation {
    condition     = var.ami_id == "" || can(regex("^ami-[a-f0-9]{8,17}$", var.ami_id))
    error_message = "AMI ID must be a valid AMI identifier or empty."
  }
}

variable "key_pair_name" {
  description = "Name of SSH key pair for EC2 instances"
  type        = string
  default     = null
}

# Database Configuration
variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "appdb"
  
  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9_]*$", var.db_name))
    error_message = "Database name must start with a letter and contain only alphanumeric characters and underscores."
  }
}

variable "db_username" {
  description = "Master username for database"
  type        = string
  default     = "dbadmin"
  sensitive   = true
  
  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9_]*$", var.db_username))
    error_message = "Database username must start with a letter and contain only alphanumeric characters and underscores."
  }
}

variable "db_password" {
  description = "Master password for database (use AWS Secrets Manager in production)"
  type        = string
  default     = null
  sensitive   = true
  
  validation {
    condition     = var.db_password == null || length(var.db_password) >= 8
    error_message = "Database password must be at least 8 characters long."
  }
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
  
  validation {
    condition     = can(regex("^db\\.[a-z0-9]+\\.[a-z0-9]+$", var.db_instance_class))
    error_message = "Database instance class must be a valid RDS instance type."
  }
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS instance (GB)"
  type        = number
  default     = 20
  
  validation {
    condition     = var.db_allocated_storage >= 20 && var.db_allocated_storage <= 65536
    error_message = "Allocated storage must be between 20 GB and 65536 GB."
  }
}

variable "db_multi_az" {
  description = "Enable Multi-AZ deployment for RDS"
  type        = bool
  default     = false
}

variable "db_backup_retention_period" {
  description = "Number of days to retain database backups"
  type        = number
  default     = 7
  
  validation {
    condition     = var.db_backup_retention_period >= 0 && var.db_backup_retention_period <= 35
    error_message = "Backup retention period must be between 0 and 35 days."
  }
}

# Security Configuration
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the application"
  type        = list(string)
  default     = ["0.0.0.0/0"]
  
  validation {
    condition = alltrue([
      for cidr in var.allowed_cidr_blocks : can(cidrhost(cidr, 0))
    ])
    error_message = "All allowed CIDR blocks must be valid IPv4 CIDR blocks."
  }
}

variable "enable_encryption" {
  description = "Enable encryption for all resources"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS key ID for encryption (leave empty to create new key)"
  type        = string
  default     = null
  
  validation {
    condition = var.kms_key_id == null || can(regex("^arn:aws:kms:[a-z0-9-]+:[0-9]{12}:key/[a-f0-9-]+$", var.kms_key_id))
    error_message = "KMS key ID must be a valid KMS key ARN or null."
  }
}

# Monitoring Configuration
variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
  default     = false
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 30
  
  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653], var.log_retention_days)
    error_message = "Log retention days must be a valid CloudWatch Logs retention value."
  }
}

variable "alarm_email" {
  description = "Email address for CloudWatch alarms"
  type        = string
  default     = null
  
  validation {
    condition     = var.alarm_email == null || can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.alarm_email))
    error_message = "Alarm email must be a valid email address."
  }
}

# Tagging Configuration
variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
  
  validation {
    condition = alltrue([
      for k, v in var.tags : can(regex("^[a-zA-Z0-9+\\-=._:/@]+$", k))
    ])
    error_message = "Tag keys must contain only alphanumeric characters and +-=._:/@"
  }
}

variable "cost_center" {
  description = "Cost center for billing allocation"
  type        = string
  default     = null
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = null
}

# Feature Flags
variable "enable_cdn" {
  description = "Enable CloudFront CDN"
  type        = bool
  default     = false
}

variable "enable_waf" {
  description = "Enable AWS WAF"
  type        = bool
  default     = false
}

variable "enable_autoscaling" {
  description = "Enable Auto Scaling"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable AWS Backup"
  type        = bool
  default     = false
}

# Advanced Configuration
variable "custom_user_data" {
  description = "Custom user data script for EC2 instances"
  type        = string
  default     = null
}

variable "additional_security_group_ids" {
  description = "Additional security group IDs to attach to instances"
  type        = list(string)
  default     = []
}

variable "instance_metadata_options" {
  description = "Metadata options for EC2 instances"
  type = object({
    http_endpoint               = string
    http_tokens                 = string
    http_put_response_hop_limit = number
  })
  default = {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
}

# Complex Type Example
variable "ingress_rules" {
  description = "List of ingress rules for security groups"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = []
}

# Map Type Example
variable "application_config" {
  description = "Application-specific configuration"
  type        = map(string)
  default     = {}
  sensitive   = true
}

# Local Values (computed from variables)
locals {
  # Derive availability zones if not provided
  azs = length(var.availability_zones) > 0 ? var.availability_zones : slice(data.aws_availability_zones.available.names, 0, 3)
  
  # Determine instance count
  instance_count = var.desired_capacity != null ? var.desired_capacity : var.min_size
  
  # Environment-specific settings
  is_production = var.environment == "prod"
  
  # Common tags
  common_tags = merge(
    {
      Environment = var.environment
      Project     = var.project_name
      Terraform   = "true"
      ManagedBy   = "terraform"
    },
    var.cost_center != null ? { CostCenter = var.cost_center } : {},
    var.owner != null ? { Owner = var.owner } : {},
    var.tags
  )
  
  # Resource naming
  name_prefix = "${var.project_name}-${var.environment}"
  
  # Feature flags with environment overrides
  enable_multi_az     = local.is_production || var.db_multi_az
  enable_encryption   = local.is_production || var.enable_encryption
  backup_retention    = local.is_production ? max(var.db_backup_retention_period, 30) : var.db_backup_retention_period
}
