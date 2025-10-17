#!/usr/bin/env python3
"""
AWS Cost Optimization Script
Analyzes AWS resources and provides cost optimization recommendations
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict


class AWSCostOptimizer:
    """AWS cost optimization analyzer"""

    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ce_client = boto3.client('ce', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)

    def analyze_all(self) -> Dict[str, Any]:
        """Run all cost optimization checks"""
        print("Running AWS cost optimization analysis...")

        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'region': self.region,
            'recommendations': [],
            'estimated_savings': 0.0
        }

        # Run all analysis functions
        results['recommendations'].extend(self.analyze_lambda_functions())
        results['recommendations'].extend(self.analyze_dynamodb_tables())
        results['recommendations'].extend(self.analyze_s3_buckets())
        results['recommendations'].extend(self.analyze_cloudwatch_logs())

        # Calculate total estimated savings
        results['estimated_savings'] = sum(
            r.get('estimated_monthly_savings', 0)
            for r in results['recommendations']
        )

        return results

    def analyze_lambda_functions(self) -> List[Dict]:
        """Analyze Lambda functions for cost optimization"""
        print("Analyzing Lambda functions...")
        recommendations = []

        try:
            paginator = self.lambda_client.get_paginator('list_functions')

            for page in paginator.paginate():
                for func in page['Functions']:
                    func_name = func['FunctionName']

                    # Check memory configuration
                    memory = func['MemorySize']
                    if memory == 128:
                        # Get invocation metrics
                        stats = self._get_lambda_stats(func_name)
                        if stats['avg_duration'] > 2000:  # >2s with 128MB
                            recommendations.append({
                                'service': 'Lambda',
                                'resource': func_name,
                                'issue': 'Undersized memory allocation',
                                'recommendation': f'Increase memory from {memory}MB to 512MB for better performance',
                                'estimated_monthly_savings': -10,  # Cost increase but better performance
                                'priority': 'medium'
                            })

                    # Check for unused functions
                    if stats['invocations_30d'] == 0:
                        recommendations.append({
                            'service': 'Lambda',
                            'resource': func_name,
                            'issue': 'Unused function',
                            'recommendation': 'Delete unused function',
                            'estimated_monthly_savings': 5,
                            'priority': 'low'
                        })

                    # Check for ARM64 architecture
                    architectures = func.get('Architectures', ['x86_64'])
                    if 'arm64' not in architectures and memory >= 512:
                        recommendations.append({
                            'service': 'Lambda',
                            'resource': func_name,
                            'issue': 'Not using ARM64 (Graviton2)',
                            'recommendation': 'Migrate to ARM64 for 20% cost reduction',
                            'estimated_monthly_savings': 20,
                            'priority': 'high'
                        })

        except Exception as e:
            print(f"Error analyzing Lambda: {e}")

        return recommendations

    def analyze_dynamodb_tables(self) -> List[Dict]:
        """Analyze DynamoDB tables for cost optimization"""
        print("Analyzing DynamoDB tables...")
        recommendations = []

        try:
            paginator = self.dynamodb_client.get_paginator('list_tables')

            for page in paginator.paginate():
                for table_name in page['TableNames']:
                    table = self.dynamodb_client.describe_table(TableName=table_name)['Table']

                    billing_mode = table.get('BillingModeSummary', {}).get('BillingMode', 'PROVISIONED')

                    # Get table metrics
                    metrics = self._get_dynamodb_metrics(table_name)

                    # Check if on-demand would be cheaper
                    if billing_mode == 'PROVISIONED':
                        provisioned_cost = self._estimate_provisioned_cost(table)
                        ondemand_cost = self._estimate_ondemand_cost(metrics)

                        if ondemand_cost < provisioned_cost * 0.8:
                            savings = provisioned_cost - ondemand_cost
                            recommendations.append({
                                'service': 'DynamoDB',
                                'resource': table_name,
                                'issue': 'Inefficient billing mode',
                                'recommendation': f'Switch from provisioned to on-demand billing',
                                'estimated_monthly_savings': savings,
                                'priority': 'high'
                            })

                    # Check for unused tables
                    if metrics['read_ops_30d'] == 0 and metrics['write_ops_30d'] == 0:
                        recommendations.append({
                            'service': 'DynamoDB',
                            'resource': table_name,
                            'issue': 'Unused table',
                            'recommendation': 'Delete or export to S3 and delete',
                            'estimated_monthly_savings': 25,
                            'priority': 'medium'
                        })

                    # Check for auto-scaling
                    if billing_mode == 'PROVISIONED' and not self._has_autoscaling(table_name):
                        recommendations.append({
                            'service': 'DynamoDB',
                            'resource': table_name,
                            'issue': 'No auto-scaling configured',
                            'recommendation': 'Enable auto-scaling to optimize capacity',
                            'estimated_monthly_savings': 30,
                            'priority': 'high'
                        })

        except Exception as e:
            print(f"Error analyzing DynamoDB: {e}")

        return recommendations

    def analyze_s3_buckets(self) -> List[Dict]:
        """Analyze S3 buckets for cost optimization"""
        print("Analyzing S3 buckets...")
        recommendations = []

        try:
            buckets = self.s3_client.list_buckets()['Buckets']

            for bucket in buckets:
                bucket_name = bucket['Name']

                # Check lifecycle policies
                has_lifecycle = self._has_lifecycle_policy(bucket_name)
                if not has_lifecycle:
                    recommendations.append({
                        'service': 'S3',
                        'resource': bucket_name,
                        'issue': 'No lifecycle policy',
                        'recommendation': 'Implement lifecycle policy to transition old objects to cheaper storage',
                        'estimated_monthly_savings': 50,
                        'priority': 'high'
                    })

                # Check intelligent-tiering
                has_intelligent_tiering = self._has_intelligent_tiering(bucket_name)
                if not has_intelligent_tiering:
                    recommendations.append({
                        'service': 'S3',
                        'resource': bucket_name,
                        'issue': 'Not using Intelligent-Tiering',
                        'recommendation': 'Enable S3 Intelligent-Tiering for automatic cost optimization',
                        'estimated_monthly_savings': 40,
                        'priority': 'medium'
                    })

                # Check for old versions
                versioning = self._get_versioning_status(bucket_name)
                if versioning == 'Enabled':
                    recommendations.append({
                        'service': 'S3',
                        'resource': bucket_name,
                        'issue': 'Versioning enabled without lifecycle',
                        'recommendation': 'Add lifecycle rule to expire old versions',
                        'estimated_monthly_savings': 30,
                        'priority': 'medium'
                    })

        except Exception as e:
            print(f"Error analyzing S3: {e}")

        return recommendations

    def analyze_cloudwatch_logs(self) -> List[Dict]:
        """Analyze CloudWatch Logs for cost optimization"""
        print("Analyzing CloudWatch Logs...")
        recommendations = []

        try:
            logs_client = boto3.client('logs', region_name=self.region)
            paginator = logs_client.get_paginator('describe_log_groups')

            for page in paginator.paginate():
                for log_group in page['logGroups']:
                    log_group_name = log_group['logGroupName']

                    # Check retention policy
                    retention = log_group.get('retentionInDays')
                    if retention is None:
                        recommendations.append({
                            'service': 'CloudWatch Logs',
                            'resource': log_group_name,
                            'issue': 'No retention policy (infinite retention)',
                            'recommendation': 'Set retention policy to 30-90 days',
                            'estimated_monthly_savings': 15,
                            'priority': 'medium'
                        })
                    elif retention > 90:
                        recommendations.append({
                            'service': 'CloudWatch Logs',
                            'resource': log_group_name,
                            'issue': f'Long retention period ({retention} days)',
                            'recommendation': 'Reduce retention to 30-90 days or export to S3',
                            'estimated_monthly_savings': 10,
                            'priority': 'low'
                        })

                    # Check for empty log groups
                    stored_bytes = log_group.get('storedBytes', 0)
                    if stored_bytes == 0:
                        recommendations.append({
                            'service': 'CloudWatch Logs',
                            'resource': log_group_name,
                            'issue': 'Empty log group',
                            'recommendation': 'Delete unused log group',
                            'estimated_monthly_savings': 1,
                            'priority': 'low'
                        })

        except Exception as e:
            print(f"Error analyzing CloudWatch Logs: {e}")

        return recommendations

    def _get_lambda_stats(self, function_name: str) -> Dict:
        """Get Lambda function statistics"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=30)

        try:
            # Get invocations
            invocations = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=2592000,  # 30 days
                Statistics=['Sum']
            )

            # Get duration
            duration = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Duration',
                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=2592000,
                Statistics=['Average']
            )

            return {
                'invocations_30d': invocations['Datapoints'][0]['Sum'] if invocations['Datapoints'] else 0,
                'avg_duration': duration['Datapoints'][0]['Average'] if duration['Datapoints'] else 0
            }
        except Exception:
            return {'invocations_30d': 0, 'avg_duration': 0}

    def _get_dynamodb_metrics(self, table_name: str) -> Dict:
        """Get DynamoDB table metrics"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=30)

        try:
            read_ops = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/DynamoDB',
                MetricName='ConsumedReadCapacityUnits',
                Dimensions=[{'Name': 'TableName', 'Value': table_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=2592000,
                Statistics=['Sum']
            )

            write_ops = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/DynamoDB',
                MetricName='ConsumedWriteCapacityUnits',
                Dimensions=[{'Name': 'TableName', 'Value': table_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=2592000,
                Statistics=['Sum']
            )

            return {
                'read_ops_30d': read_ops['Datapoints'][0]['Sum'] if read_ops['Datapoints'] else 0,
                'write_ops_30d': write_ops['Datapoints'][0]['Sum'] if write_ops['Datapoints'] else 0
            }
        except Exception:
            return {'read_ops_30d': 0, 'write_ops_30d': 0}

    def _estimate_provisioned_cost(self, table: Dict) -> float:
        """Estimate provisioned capacity cost"""
        read_capacity = table.get('ProvisionedThroughput', {}).get('ReadCapacityUnits', 0)
        write_capacity = table.get('ProvisionedThroughput', {}).get('WriteCapacityUnits', 0)

        # Cost per hour: $0.00065 per RCU, $0.00325 per WCU
        monthly_cost = (read_capacity * 0.00065 + write_capacity * 0.00325) * 730
        return monthly_cost

    def _estimate_ondemand_cost(self, metrics: Dict) -> float:
        """Estimate on-demand cost"""
        # Cost: $1.25 per million reads, $6.25 per million writes
        read_cost = (metrics['read_ops_30d'] / 1000000) * 1.25
        write_cost = (metrics['write_ops_30d'] / 1000000) * 6.25
        return read_cost + write_cost

    def _has_autoscaling(self, table_name: str) -> bool:
        """Check if table has auto-scaling configured"""
        try:
            aas_client = boto3.client('application-autoscaling', region_name=self.region)
            targets = aas_client.describe_scalable_targets(
                ServiceNamespace='dynamodb',
                ResourceIds=[f'table/{table_name}']
            )
            return len(targets['ScalableTargets']) > 0
        except Exception:
            return False

    def _has_lifecycle_policy(self, bucket_name: str) -> bool:
        """Check if S3 bucket has lifecycle policy"""
        try:
            self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            return True
        except Exception:
            return False

    def _has_intelligent_tiering(self, bucket_name: str) -> bool:
        """Check if bucket uses intelligent-tiering"""
        try:
            config = self.s3_client.get_bucket_intelligent_tiering_configuration(
                Bucket=bucket_name,
                Id='EntireBucket'
            )
            return True
        except Exception:
            return False

    def _get_versioning_status(self, bucket_name: str) -> str:
        """Get S3 bucket versioning status"""
        try:
            response = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
            return response.get('Status', 'Disabled')
        except Exception:
            return 'Unknown'

    def generate_report(self, results: Dict) -> str:
        """Generate formatted report"""
        report_lines = [
            "=" * 80,
            "AWS COST OPTIMIZATION REPORT",
            "=" * 80,
            f"Generated: {results['timestamp']}",
            f"Region: {results['region']}",
            f"Total Estimated Monthly Savings: ${results['estimated_savings']:.2f}",
            "",
            "RECOMMENDATIONS:",
            "-" * 80
        ]

        # Group by priority
        by_priority = defaultdict(list)
        for rec in results['recommendations']:
            by_priority[rec['priority']].append(rec)

        for priority in ['high', 'medium', 'low']:
            if priority in by_priority:
                report_lines.append(f"\n{priority.upper()} PRIORITY:")
                for rec in by_priority[priority]:
                    report_lines.extend([
                        f"\nService: {rec['service']}",
                        f"Resource: {rec['resource']}",
                        f"Issue: {rec['issue']}",
                        f"Recommendation: {rec['recommendation']}",
                        f"Estimated Monthly Savings: ${rec['estimated_monthly_savings']:.2f}",
                        "-" * 40
                    ])

        report_lines.append("=" * 80)
        return "\n".join(report_lines)


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='AWS Cost Optimization Analyzer')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--output', default='cost-optimization-report.json', help='Output file')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')

    args = parser.parse_args()

    optimizer = AWSCostOptimizer(region=args.region)
    results = optimizer.analyze_all()

    if args.format == 'json':
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Report saved to {args.output}")
    else:
        report = optimizer.generate_report(results)
        output_file = args.output.replace('.json', '.txt')
        with open(output_file, 'w') as f:
            f.write(report)
        print(report)
        print(f"\nReport saved to {output_file}")


if __name__ == '__main__':
    main()
