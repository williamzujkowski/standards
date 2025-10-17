# Main Terraform Configuration Template
# This template demonstrates a complete multi-tier application infrastructure

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
  
  backend "s3" {
    bucket         = "your-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Provider Configuration
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

# Local Variables
locals {
  environment = terraform.workspace != "default" ? terraform.workspace : var.environment
  
  common_tags = {
    Environment = local.environment
    Project     = var.project_name
    Terraform   = "true"
    CreatedAt   = timestamp()
  }
  
  # Environment-specific configuration
  config = {
    dev = {
      instance_type     = "t3.micro"
      min_size          = 1
      max_size          = 2
      db_instance_class = "db.t3.micro"
      enable_backup     = false
    }
    staging = {
      instance_type     = "t3.small"
      min_size          = 2
      max_size          = 4
      db_instance_class = "db.t3.small"
      enable_backup     = true
    }
    prod = {
      instance_type     = "t3.medium"
      min_size          = 3
      max_size          = 10
      db_instance_class = "db.r6g.large"
      enable_backup     = true
    }
  }
  
  current_config = local.config[local.environment]
}

# Data Sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Random ID for unique naming
resource "random_id" "suffix" {
  byte_length = 4
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  
  name = "${var.project_name}-${local.environment}-vpc"
  cidr = var.vpc_cidr
  
  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = [for k, v in slice(data.aws_availability_zones.available.names, 0, 3) : cidrsubnet(var.vpc_cidr, 8, k)]
  public_subnets  = [for k, v in slice(data.aws_availability_zones.available.names, 0, 3) : cidrsubnet(var.vpc_cidr, 8, k + 100)]
  database_subnets = [for k, v in slice(data.aws_availability_zones.available.names, 0, 3) : cidrsubnet(var.vpc_cidr, 8, k + 200)]
  
  enable_nat_gateway     = true
  single_nat_gateway     = local.environment != "prod"
  enable_dns_hostnames   = true
  enable_dns_support     = true
  
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true
  
  tags = local.common_tags
}

# Security Groups
resource "aws_security_group" "alb" {
  name_prefix = "${var.project_name}-${local.environment}-alb-"
  description = "Security group for Application Load Balancer"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP from internet"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS from internet"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${local.environment}-alb-sg"
    }
  )
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "app" {
  name_prefix = "${var.project_name}-${local.environment}-app-"
  description = "Security group for application servers"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "Allow traffic from ALB"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${local.environment}-app-sg"
    }
  )
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "database" {
  name_prefix = "${var.project_name}-${local.environment}-db-"
  description = "Security group for database"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
    description     = "Allow PostgreSQL from app servers"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${local.environment}-db-sg"
    }
  )
  
  lifecycle {
    create_before_destroy = true
  }
}

# KMS Key for Encryption
resource "aws_kms_key" "main" {
  description             = "KMS key for ${var.project_name} ${local.environment}"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  
  tags = local.common_tags
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.project_name}-${local.environment}"
  target_key_id = aws_kms_key.main.key_id
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-${local.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = local.environment == "prod"
  enable_http2              = true
  enable_cross_zone_load_balancing = true
  
  access_logs {
    bucket  = aws_s3_bucket.logs.id
    prefix  = "alb"
    enabled = true
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-${local.environment}-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  deregistration_delay = 30
  
  tags = local.common_tags
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix   = "${var.project_name}-${local.environment}-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = local.current_config.instance_type
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }
  
  block_device_mappings {
    device_name = "/dev/xvda"
    
    ebs {
      volume_size           = 30
      volume_type           = "gp3"
      encrypted             = true
      kms_key_id            = aws_kms_key.main.arn
      delete_on_termination = true
    }
  }
  
  user_data = base64encode(templatefile("${path.module}/user-data.sh", {
    environment  = local.environment
    project_name = var.project_name
  }))
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  
  monitoring {
    enabled = true
  }
  
  tag_specifications {
    resource_type = "instance"
    tags = merge(
      local.common_tags,
      {
        Name = "${var.project_name}-${local.environment}-app"
      }
    )
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-${local.environment}-asg"
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.app.arn]
  
  min_size         = local.current_config.min_size
  max_size         = local.current_config.max_size
  desired_capacity = local.current_config.min_size
  
  health_check_type         = "ELB"
  health_check_grace_period = 300
  force_delete              = false
  wait_for_capacity_timeout = "10m"
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  enabled_metrics = [
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupMinSize",
    "GroupMaxSize",
    "GroupTotalInstances",
  ]
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-${local.environment}-app"
    propagate_at_launch = true
  }
  
  dynamic "tag" {
    for_each = local.common_tags
    
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
  
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [desired_capacity]
  }
}

# Auto Scaling Policies
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project_name}-${local.environment}-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.project_name}-${local.environment}-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project_name}-${local.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "${var.project_name}-${local.environment}-low-cpu"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "20"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_down.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

# RDS Database
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"
  
  identifier = "${var.project_name}-${local.environment}-db"
  
  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = local.current_config.db_instance_class
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.main.arn
  
  db_name  = var.db_name
  username = var.db_username
  port     = 5432
  
  multi_az               = local.environment == "prod"
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.database.id]
  
  backup_retention_period = local.current_config.enable_backup ? 30 : 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  skip_final_snapshot = local.environment != "prod"
  deletion_protection = local.environment == "prod"
  
  tags = local.common_tags
}

# S3 Bucket for Logs
resource "aws_s3_bucket" "logs" {
  bucket = "${var.project_name}-${local.environment}-logs-${random_id.suffix.hex}"
  
  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.main.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  rule {
    id     = "log-expiration"
    status = "Enabled"
    
    expiration {
      days = 90
    }
    
    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

# IAM Role for EC2 Instances
resource "aws_iam_role" "app" {
  name = "${var.project_name}-${local.environment}-app-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "app_ssm" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "app_cloudwatch" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "app" {
  name = "${var.project_name}-${local.environment}-app-profile"
  role = aws_iam_role.app.name
  
  tags = local.common_tags
}
