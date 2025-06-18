# Cost Optimization and FinOps Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** COST

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [FinOps Principles and Framework](#1-finops-principles-and-framework)
2. [Cloud Cost Management](#2-cloud-cost-management)
3. [Resource Optimization](#3-resource-optimization)
4. [Cost Monitoring and Alerting](#4-cost-monitoring-and-alerting)
5. [Budget Management](#5-budget-management)
6. [Cost Allocation and Chargeback](#6-cost-allocation-and-chargeback)
7. [Automation and Tooling](#7-automation-and-tooling)
8. [Procurement and Vendor Management](#8-procurement-and-vendor-management)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. FinOps Principles and Framework

### 1.1 Core FinOps Principles

#### Foundation Principles **[REQUIRED]**
```yaml
# FinOps principles configuration
finops_principles:
  collaboration:
    description: "Teams work together to optimize cloud costs"
    practices:
      - Cross-functional cost optimization teams
      - Shared responsibility for cloud costs
      - Regular cost review meetings
      - Cost-aware engineering culture

  accountability:
    description: "Teams own their cloud cost decisions"
    practices:
      - Cost allocation by team/project
      - Budget ownership at team level
      - Cost impact consideration in technical decisions
      - Regular cost reviews and retrospectives

  value_driven:
    description: "Optimize for business value, not just cost reduction"
    practices:
      - Cost per business metric tracking
      - Value-based cost optimization
      - Performance vs cost trade-off analysis
      - Customer impact consideration

  accessibility:
    description: "Cost data is accessible to all stakeholders"
    practices:
      - Self-service cost dashboards
      - Regular cost reports and insights
      - Cost training and education
      - Transparent cost allocation
```

#### FinOps Maturity Model **[REQUIRED]**
```python
# finops/maturity_assessment.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List
import json

class MaturityLevel(Enum):
    CRAWL = "crawl"
    WALK = "walk"
    RUN = "run"

@dataclass
class MaturityDimension:
    name: str
    description: str
    current_level: MaturityLevel
    target_level: MaturityLevel
    gap_analysis: List[str]
    improvement_actions: List[str]

class FinOpsMaturityAssessment:
    def __init__(self):
        self.dimensions = {
            "cost_visibility": MaturityDimension(
                name="Cost Visibility",
                description="Ability to see and understand cloud costs",
                current_level=MaturityLevel.CRAWL,
                target_level=MaturityLevel.RUN,
                gap_analysis=[],
                improvement_actions=[]
            ),
            "cost_allocation": MaturityDimension(
                name="Cost Allocation",
                description="Ability to allocate costs to teams/projects",
                current_level=MaturityLevel.CRAWL,
                target_level=MaturityLevel.WALK,
                gap_analysis=[],
                improvement_actions=[]
            ),
            "governance": MaturityDimension(
                name="Governance",
                description="Policies and controls for cloud spending",
                current_level=MaturityLevel.CRAWL,
                target_level=MaturityLevel.WALK,
                gap_analysis=[],
                improvement_actions=[]
            ),
            "optimization": MaturityDimension(
                name="Optimization",
                description="Ability to optimize costs continuously",
                current_level=MaturityLevel.CRAWL,
                target_level=MaturityLevel.RUN,
                gap_analysis=[],
                improvement_actions=[]
            )
        }

    def assess_cost_visibility(self) -> MaturityLevel:
        """Assess current cost visibility maturity."""
        criteria = {
            MaturityLevel.CRAWL: [
                "Basic cost dashboard available",
                "Monthly cost reports generated",
                "High-level cost breakdowns by service"
            ],
            MaturityLevel.WALK: [
                "Real-time cost monitoring",
                "Cost allocation by team/project",
                "Detailed resource-level cost visibility",
                "Historical trend analysis"
            ],
            MaturityLevel.RUN: [
                "Predictive cost forecasting",
                "Anomaly detection and alerting",
                "Cost optimization recommendations",
                "Self-service cost analytics"
            ]
        }

        # Implementation would assess against these criteria
        return MaturityLevel.CRAWL

    def assess_cost_allocation(self) -> MaturityLevel:
        """Assess cost allocation maturity."""
        criteria = {
            MaturityLevel.CRAWL: [
                "Basic tagging strategy",
                "Manual cost allocation process",
                "High-level cost center allocation"
            ],
            MaturityLevel.WALK: [
                "Automated tagging enforcement",
                "Resource-level cost allocation",
                "Chargeback/showback implementation",
                "Regular allocation accuracy reviews"
            ],
            MaturityLevel.RUN: [
                "Dynamic cost allocation",
                "Shared resource cost splitting",
                "Business metric-based allocation",
                "Automated dispute resolution"
            ]
        }

        return MaturityLevel.CRAWL

    def generate_improvement_roadmap(self) -> Dict[str, List[str]]:
        """Generate improvement roadmap based on maturity gaps."""
        roadmap = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_vision": []
        }

        for dimension in self.dimensions.values():
            if dimension.current_level == MaturityLevel.CRAWL:
                roadmap["immediate_actions"].extend([
                    f"Establish basic {dimension.name.lower()} capabilities",
                    f"Implement foundational {dimension.name.lower()} processes"
                ])

            if dimension.target_level == MaturityLevel.WALK:
                roadmap["short_term_goals"].extend([
                    f"Automate {dimension.name.lower()} processes",
                    f"Implement advanced {dimension.name.lower()} features"
                ])

            if dimension.target_level == MaturityLevel.RUN:
                roadmap["long_term_vision"].extend([
                    f"Achieve full automation in {dimension.name.lower()}",
                    f"Implement predictive {dimension.name.lower()} capabilities"
                ])

        return roadmap

# Usage
assessment = FinOpsMaturityAssessment()
roadmap = assessment.generate_improvement_roadmap()
print(json.dumps(roadmap, indent=2))
```

### 1.2 Organizational Structure

#### FinOps Team Structure **[REQUIRED]**
```yaml
# FinOps organizational structure
finops_organization:
  steering_committee:
    members:
      - CFO or Finance Director
      - CTO or Engineering Director
      - VP of Cloud/Infrastructure
      - Business Unit Leaders
    responsibilities:
      - Set cost optimization strategy
      - Review budget allocations
      - Approve major cost initiatives
      - Resolve cost disputes
    meeting_frequency: monthly

  finops_team:
    roles:
      - FinOps Practitioner (lead)
      - Cloud Cost Analyst
      - Engineering Cost Specialist
      - Business Analyst
    responsibilities:
      - Day-to-day cost optimization
      - Cost analysis and reporting
      - Tool management and automation
      - Training and enablement
    meeting_frequency: weekly

  engineering_champions:
    selection_criteria:
      - Strong technical background
      - Interest in cost optimization
      - Good communication skills
      - Influence within engineering teams
    responsibilities:
      - Promote cost-aware engineering
      - Implement cost optimization recommendations
      - Provide technical expertise
      - Bridge between FinOps and engineering
```

#### Roles and Responsibilities **[REQUIRED]**
```python
# finops/roles.py
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class ResponsibilityType(Enum):
    ACCOUNTABLE = "accountable"  # A - Accountable
    RESPONSIBLE = "responsible"  # R - Responsible
    CONSULTED = "consulted"     # C - Consulted
    INFORMED = "informed"       # I - Informed

@dataclass
class FinOpsRole:
    name: str
    description: str
    key_responsibilities: List[str]
    required_skills: List[str]
    reporting_to: str

class FinOpsRACI:
    """RACI matrix for FinOps responsibilities."""

    def __init__(self):
        self.roles = [
            "FinOps Practitioner",
            "Engineering Manager",
            "Finance Manager",
            "Product Manager",
            "DevOps Engineer"
        ]

        self.activities = {
            "cost_budgeting": {
                "FinOps Practitioner": ResponsibilityType.RESPONSIBLE,
                "Engineering Manager": ResponsibilityType.CONSULTED,
                "Finance Manager": ResponsibilityType.ACCOUNTABLE,
                "Product Manager": ResponsibilityType.CONSULTED,
                "DevOps Engineer": ResponsibilityType.INFORMED
            },
            "cost_monitoring": {
                "FinOps Practitioner": ResponsibilityType.ACCOUNTABLE,
                "Engineering Manager": ResponsibilityType.INFORMED,
                "Finance Manager": ResponsibilityType.INFORMED,
                "Product Manager": ResponsibilityType.INFORMED,
                "DevOps Engineer": ResponsibilityType.RESPONSIBLE
            },
            "resource_rightsizing": {
                "FinOps Practitioner": ResponsibilityType.CONSULTED,
                "Engineering Manager": ResponsibilityType.ACCOUNTABLE,
                "Finance Manager": ResponsibilityType.INFORMED,
                "Product Manager": ResponsibilityType.CONSULTED,
                "DevOps Engineer": ResponsibilityType.RESPONSIBLE
            },
            "cost_optimization": {
                "FinOps Practitioner": ResponsibilityType.RESPONSIBLE,
                "Engineering Manager": ResponsibilityType.ACCOUNTABLE,
                "Finance Manager": ResponsibilityType.CONSULTED,
                "Product Manager": ResponsibilityType.CONSULTED,
                "DevOps Engineer": ResponsibilityType.RESPONSIBLE
            }
        }

    def get_responsibilities(self, role: str) -> Dict[str, ResponsibilityType]:
        """Get all responsibilities for a specific role."""
        return {
            activity: responsibilities[role]
            for activity, responsibilities in self.activities.items()
            if role in responsibilities
        }

# Define specific roles
FINOPS_ROLES = {
    "finops_practitioner": FinOpsRole(
        name="FinOps Practitioner",
        description="Lead cost optimization initiatives and FinOps practice",
        key_responsibilities=[
            "Develop and implement FinOps strategy",
            "Analyze cloud spending patterns and trends",
            "Create cost optimization recommendations",
            "Manage FinOps tools and processes",
            "Facilitate cross-team cost discussions",
            "Track and report on cost KPIs"
        ],
        required_skills=[
            "Cloud cost management expertise",
            "Financial analysis skills",
            "Data analysis and visualization",
            "Project management",
            "Communication and collaboration"
        ],
        reporting_to="CFO or VP Engineering"
    ),

    "cloud_cost_analyst": FinOpsRole(
        name="Cloud Cost Analyst",
        description="Analyze cloud costs and provide insights",
        key_responsibilities=[
            "Perform detailed cost analysis",
            "Create cost reports and dashboards",
            "Identify cost anomalies and trends",
            "Support cost allocation processes",
            "Validate cost optimization savings"
        ],
        required_skills=[
            "Data analysis and SQL",
            "Cloud platform knowledge",
            "Excel/spreadsheet expertise",
            "Business intelligence tools",
            "Financial modeling"
        ],
        reporting_to="FinOps Practitioner"
    )
}
```

---

## 2. Cloud Cost Management

### 2.1 Multi-Cloud Cost Management

#### AWS Cost Management **[REQUIRED]**
```python
# aws/cost_management.py
import boto3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class AWSCostManager:
    def __init__(self, profile_name: Optional[str] = None):
        """Initialize AWS Cost Manager."""
        session = boto3.Session(profile_name=profile_name)
        self.ce_client = session.client('ce')  # Cost Explorer
        self.organizations_client = session.client('organizations')
        self.budgets_client = session.client('budgets')

    def get_cost_and_usage(self,
                          start_date: str,
                          end_date: str,
                          granularity: str = 'MONTHLY',
                          group_by: List[Dict] = None) -> Dict:
        """Get cost and usage data from Cost Explorer."""

        if group_by is None:
            group_by = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]

        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity,
            Metrics=['BlendedCost', 'UsageQuantity'],
            GroupBy=group_by
        )

        return response

    def get_rightsizing_recommendations(self) -> Dict:
        """Get EC2 rightsizing recommendations."""
        response = self.ce_client.get_rightsizing_recommendation(
            Service='AmazonEC2',
            Configuration={
                'BenefitsConsidered': True,
                'RecommendationTarget': 'SAME_INSTANCE_FAMILY'
            }
        )

        return response

    def get_savings_plans_utilization(self, time_period: Dict) -> Dict:
        """Get Savings Plans utilization and coverage."""
        response = self.ce_client.get_savings_plans_utilization(
            TimePeriod=time_period,
            Granularity='MONTHLY'
        )

        return response

    def analyze_cost_trends(self, days: int = 30) -> pd.DataFrame:
        """Analyze cost trends over specified period."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        response = self.get_cost_and_usage(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            granularity='DAILY'
        )

        # Convert to DataFrame for analysis
        data = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                data.append({
                    'Date': date,
                    'Service': service,
                    'Cost': cost
                })

        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])

        return df

    def create_cost_budget(self,
                          budget_name: str,
                          budget_limit: float,
                          time_unit: str = 'MONTHLY') -> Dict:
        """Create a cost budget with alerts."""
        account_id = boto3.client('sts').get_caller_identity()['Account']

        budget = {
            'BudgetName': budget_name,
            'BudgetLimit': {
                'Amount': str(budget_limit),
                'Unit': 'USD'
            },
            'TimeUnit': time_unit,
            'TimePeriod': {
                'Start': datetime.now().replace(day=1).date(),
                'End': (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).date()
            },
            'CostFilters': {},
            'BudgetType': 'COST'
        }

        # Create budget notifications
        notifications = [
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 80,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {
                        'SubscriptionType': 'EMAIL',
                        'Address': 'finops-team@company.com'
                    }
                ]
            },
            {
                'Notification': {
                    'NotificationType': 'FORECASTED',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 100,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {
                        'SubscriptionType': 'EMAIL',
                        'Address': 'finops-alerts@company.com'
                    }
                ]
            }
        ]

        response = self.budgets_client.create_budget(
            AccountId=account_id,
            Budget=budget,
            NotificationsWithSubscribers=notifications
        )

        return response

# Usage example
cost_manager = AWSCostManager()

# Analyze recent cost trends
trends_df = cost_manager.analyze_cost_trends(days=30)
print(f"Total cost last 30 days: ${trends_df['Cost'].sum():.2f}")

# Get rightsizing recommendations
rightsizing = cost_manager.get_rightsizing_recommendations()
potential_savings = sum([
    float(rec['EstimatedMonthlySavings']['Amount'])
    for rec in rightsizing.get('RightsizingRecommendations', [])
])
print(f"Potential monthly savings from rightsizing: ${potential_savings:.2f}")
```

#### Azure Cost Management **[REQUIRED]**
```python
# azure/cost_management.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.advisor import AdvisorManagementClient
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List

class AzureCostManager:
    def __init__(self, subscription_id: str):
        """Initialize Azure Cost Manager."""
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()

        self.cost_client = CostManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.consumption_client = ConsumptionManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.advisor_client = AdvisorManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

    def get_cost_analysis(self,
                         resource_group: str = None,
                         time_period_days: int = 30) -> pd.DataFrame:
        """Get cost analysis data."""

        # Define scope
        scope = f"/subscriptions/{self.subscription_id}"
        if resource_group:
            scope += f"/resourceGroups/{resource_group}"

        # Define time period
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=time_period_days)

        # Create query definition
        query_definition = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start_date.isoformat(),
                "to": end_date.isoformat()
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                },
                "grouping": [
                    {
                        "type": "Dimension",
                        "name": "ServiceName"
                    }
                ]
            }
        }

        # Execute query
        result = self.cost_client.query.usage(
            scope=scope,
            parameters=query_definition
        )

        # Convert to DataFrame
        data = []
        for row in result.rows:
            data.append({
                'Date': datetime.strptime(row[2], '%Y%m%d').date(),
                'Service': row[1],
                'Cost': float(row[0]),
                'Currency': row[3]
            })

        return pd.DataFrame(data)

    def get_advisor_recommendations(self) -> List[Dict]:
        """Get Azure Advisor cost recommendations."""
        recommendations = []

        # Get cost recommendations
        cost_recommendations = self.advisor_client.recommendations.list(
            filter="Category eq 'Cost'"
        )

        for rec in cost_recommendations:
            recommendations.append({
                'id': rec.name,
                'category': rec.category,
                'impact': rec.impact,
                'title': rec.short_description.problem,
                'description': rec.short_description.solution,
                'potential_savings': rec.extended_properties.get('annualSavingsAmount', 0),
                'resource_id': rec.resource_metadata.resource_id if rec.resource_metadata else None
            })

        return recommendations

    def analyze_reserved_instance_utilization(self) -> Dict:
        """Analyze Reserved Instance utilization."""
        # Get RI utilization for last 30 days
        utilization_data = self.consumption_client.reservations_summaries.list_by_reservation_order_and_reservation(
            reservation_order_id="your-reservation-order-id",  # Replace with actual ID
            reservation_id="your-reservation-id",  # Replace with actual ID
            grain="daily"
        )

        total_utilization = 0
        count = 0

        for data in utilization_data:
            if hasattr(data, 'utilization_percentage'):
                total_utilization += data.utilization_percentage
                count += 1

        avg_utilization = total_utilization / count if count > 0 else 0

        return {
            'average_utilization': avg_utilization,
            'optimization_opportunity': 100 - avg_utilization
        }

    def create_budget_alert(self,
                           budget_name: str,
                           budget_amount: float,
                           resource_group: str = None) -> Dict:
        """Create budget with alert notifications."""

        # Define scope
        scope = f"/subscriptions/{self.subscription_id}"
        if resource_group:
            scope += f"/resourceGroups/{resource_group}"

        # Budget definition
        budget_definition = {
            "properties": {
                "category": "Cost",
                "amount": budget_amount,
                "timeGrain": "Monthly",
                "timePeriod": {
                    "startDate": datetime.now().replace(day=1).strftime('%Y-%m-%d'),
                    "endDate": (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%Y-%m-%d')
                },
                "notifications": {
                    "notification1": {
                        "enabled": True,
                        "operator": "GreaterThan",
                        "threshold": 80,
                        "contactEmails": ["finops-team@company.com"],
                        "contactRoles": ["Owner"],
                        "contactGroups": []
                    },
                    "notification2": {
                        "enabled": True,
                        "operator": "GreaterThan",
                        "threshold": 100,
                        "contactEmails": ["finops-alerts@company.com"],
                        "contactRoles": ["Owner"],
                        "contactGroups": []
                    }
                }
            }
        }

        # Note: Budget creation would use Azure REST API or ARM templates
        # as the Python SDK doesn't fully support budget creation

        return {
            "budget_name": budget_name,
            "scope": scope,
            "amount": budget_amount,
            "status": "created"
        }

# Usage
azure_cost_manager = AzureCostManager("your-subscription-id")

# Analyze costs
cost_df = azure_cost_manager.get_cost_analysis(time_period_days=30)
print(f"Total Azure cost last 30 days: ${cost_df['Cost'].sum():.2f}")

# Get cost optimization recommendations
recommendations = azure_cost_manager.get_advisor_recommendations()
total_potential_savings = sum([rec['potential_savings'] for rec in recommendations])
print(f"Potential annual savings: ${total_potential_savings:.2f}")
```

#### Google Cloud Cost Management **[REQUIRED]**
```python
# gcp/cost_management.py
from google.cloud import billing_v1
from google.cloud import recommender_v1
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GCPCostManager:
    def __init__(self, project_id: str, billing_account_id: str):
        """Initialize GCP Cost Manager."""
        self.project_id = project_id
        self.billing_account_id = billing_account_id

        # Initialize clients
        self.billing_client = billing_v1.CloudBillingClient()
        self.recommender_client = recommender_v1.RecommenderClient()

    def get_billing_data(self, days: int = 30) -> pd.DataFrame:
        """Get billing data using BigQuery export."""
        from google.cloud import bigquery

        client = bigquery.Client(project=self.project_id)

        # Query billing export table
        query = f"""
        SELECT
            service.description as service_name,
            sku.description as sku_description,
            DATE(usage_start_time) as usage_date,
            SUM(cost) as total_cost,
            currency
        FROM `{self.project_id}.billing_export.gcp_billing_export_v1_{self.billing_account_id.replace('-', '_')}`
        WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
        GROUP BY 1, 2, 3, 5
        ORDER BY usage_date DESC, total_cost DESC
        """

        df = client.query(query).to_dataframe()
        return df

    def get_cost_recommendations(self) -> List[Dict]:
        """Get cost optimization recommendations."""
        recommendations = []

        # Get rightsizing recommendations
        parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"

        try:
            for recommendation in self.recommender_client.list_recommendations(parent=parent):
                impact = recommendation.primary_impact

                recommendations.append({
                    'id': recommendation.name,
                    'recommender': 'compute.instance.MachineTypeRecommender',
                    'description': recommendation.description,
                    'category': 'rightsizing',
                    'resource': recommendation.content.get('resource', ''),
                    'potential_savings': {
                        'currency': impact.cost_projection.cost.currency_code,
                        'amount': -impact.cost_projection.cost.units  # Negative means savings
                    },
                    'state': recommendation.state_info.state.name
                })
        except Exception as e:
            print(f"Error getting rightsizing recommendations: {e}")

        # Get idle resource recommendations
        idle_parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.IdleResourceRecommender"

        try:
            for recommendation in self.recommender_client.list_recommendations(parent=idle_parent):
                impact = recommendation.primary_impact

                recommendations.append({
                    'id': recommendation.name,
                    'recommender': 'compute.instance.IdleResourceRecommender',
                    'description': recommendation.description,
                    'category': 'idle_resources',
                    'resource': recommendation.content.get('resource', ''),
                    'potential_savings': {
                        'currency': impact.cost_projection.cost.currency_code,
                        'amount': -impact.cost_projection.cost.units
                    },
                    'state': recommendation.state_info.state.name
                })
        except Exception as e:
            print(f"Error getting idle resource recommendations: {e}")

        return recommendations

    def analyze_cost_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze cost trends from billing data."""
        # Convert usage_date to datetime
        df['usage_date'] = pd.to_datetime(df['usage_date'])

        # Daily cost trends
        daily_costs = df.groupby('usage_date')['total_cost'].sum().reset_index()
        daily_costs = daily_costs.sort_values('usage_date')

        # Service-wise cost breakdown
        service_costs = df.groupby('service_name')['total_cost'].sum().sort_values(ascending=False)

        # Growth analysis
        recent_week = daily_costs.tail(7)['total_cost'].mean()
        previous_week = daily_costs.iloc[-14:-7]['total_cost'].mean()
        growth_rate = ((recent_week - previous_week) / previous_week * 100) if previous_week > 0 else 0

        return {
            'total_cost': df['total_cost'].sum(),
            'daily_average': daily_costs['total_cost'].mean(),
            'top_services': service_costs.head(5).to_dict(),
            'growth_rate_percent': growth_rate,
            'currency': df['currency'].iloc[0] if len(df) > 0 else 'USD'
        }

    def create_budget_alert(self,
                           budget_name: str,
                           budget_amount: float,
                           alert_thresholds: List[float] = [0.8, 1.0]) -> Dict:
        """Create budget with alert notifications."""

        # Budget creation would typically be done via:
        # 1. Cloud Console UI
        # 2. gcloud CLI
        # 3. Terraform/Infrastructure as Code

        budget_config = {
            "displayName": budget_name,
            "budgetFilter": {
                "projects": [f"projects/{self.project_id}"]
            },
            "amount": {
                "specifiedAmount": {
                    "currencyCode": "USD",
                    "units": str(int(budget_amount))
                }
            },
            "thresholdRules": [
                {
                    "thresholdPercent": threshold,
                    "spendBasis": "CURRENT_SPEND"
                }
                for threshold in alert_thresholds
            ],
            "notificationsRule": {
                "pubsubTopic": f"projects/{self.project_id}/topics/budget-alerts",
                "schemaVersion": "1.0"
            }
        }

        return budget_config

# Usage
gcp_cost_manager = GCPCostManager("your-project-id", "your-billing-account-id")

# Get billing data
billing_df = gcp_cost_manager.get_billing_data(days=30)

# Analyze trends
trends = gcp_cost_manager.analyze_cost_trends(billing_df)
print(f"Total GCP cost last 30 days: ${trends['total_cost']:.2f}")
print(f"Week-over-week growth: {trends['growth_rate_percent']:.1f}%")

# Get recommendations
recommendations = gcp_cost_manager.get_cost_recommendations()
total_savings = sum([rec['potential_savings']['amount'] for rec in recommendations])
print(f"Potential monthly savings: ${total_savings:.2f}")
```

### 2.2 Cost Attribution and Tagging

#### Tagging Strategy **[REQUIRED]**
```yaml
# Standardized tagging strategy across cloud providers
tagging_strategy:
  mandatory_tags:
    - key: "Environment"
      values: ["production", "staging", "development", "test"]
      description: "Environment designation"

    - key: "Team"
      values: ["platform", "frontend", "backend", "data", "security"]
      description: "Owning team responsible for the resource"

    - key: "Project"
      description: "Project or product name"
      pattern: "^[a-z][a-z0-9-]*[a-z0-9]$"

    - key: "CostCenter"
      description: "Cost center for chargeback"
      pattern: "^CC-[0-9]{4}$"

    - key: "Application"
      description: "Application name"
      pattern: "^[a-z][a-z0-9-]*[a-z0-9]$"

  optional_tags:
    - key: "Owner"
      description: "Individual responsible for the resource"

    - key: "CreatedBy"
      description: "Who created the resource"

    - key: "Purpose"
      description: "Specific purpose of the resource"

    - key: "Schedule"
      description: "When resource should be running"
      values: ["24x7", "business-hours", "dev-hours"]

  automation_tags:
    - key: "AutoShutdown"
      values: ["enabled", "disabled"]
      description: "Whether resource can be automatically shutdown"

    - key: "Backup"
      values: ["required", "optional", "none"]
      description: "Backup requirements"

    - key: "Monitoring"
      values: ["standard", "enhanced", "minimal"]
      description: "Monitoring level required"

# Tag enforcement rules
tag_enforcement:
  aws:
    resource_types:
      - "ec2:instance"
      - "rds:db"
      - "s3:bucket"
      - "lambda:function"
    enforcement_method: "preventive"  # preventive, detective, corrective

  azure:
    resource_types:
      - "Microsoft.Compute/virtualMachines"
      - "Microsoft.Storage/storageAccounts"
      - "Microsoft.Sql/servers"
    enforcement_method: "policy"

  gcp:
    resource_types:
      - "compute.instances"
      - "storage.buckets"
      - "sql.instances"
    enforcement_method: "organization_policy"
```

#### Automated Tagging Implementation **[REQUIRED]**
```python
# tagging/automation.py
import boto3
from typing import Dict, List, Optional
import json
from datetime import datetime

class CloudTaggingManager:
    def __init__(self):
        self.aws_session = boto3.Session()
        self.mandatory_tags = [
            'Environment', 'Team', 'Project', 'CostCenter', 'Application'
        ]

    def validate_tags(self, tags: Dict[str, str]) -> List[str]:
        """Validate tags against tagging strategy."""
        violations = []

        # Check mandatory tags
        for required_tag in self.mandatory_tags:
            if required_tag not in tags:
                violations.append(f"Missing mandatory tag: {required_tag}")

        # Validate Environment tag values
        if 'Environment' in tags:
            valid_environments = ['production', 'staging', 'development', 'test']
            if tags['Environment'] not in valid_environments:
                violations.append(f"Invalid Environment value: {tags['Environment']}")

        # Validate CostCenter format
        if 'CostCenter' in tags:
            import re
            if not re.match(r'^CC-\d{4}$', tags['CostCenter']):
                violations.append(f"Invalid CostCenter format: {tags['CostCenter']}")

        return violations

    def get_untagged_resources(self, region: str = 'us-east-1') -> List[Dict]:
        """Find AWS resources missing mandatory tags."""
        ec2 = self.aws_session.client('ec2', region_name=region)
        untagged_resources = []

        # Check EC2 instances
        instances = ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] not in ['terminated', 'terminating']:
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    violations = self.validate_tags(tags)

                    if violations:
                        untagged_resources.append({
                            'ResourceType': 'EC2Instance',
                            'ResourceId': instance['InstanceId'],
                            'CurrentTags': tags,
                            'Violations': violations,
                            'Region': region
                        })

        # Check S3 buckets
        s3 = self.aws_session.client('s3')
        buckets = s3.list_buckets()

        for bucket in buckets['Buckets']:
            try:
                tags_response = s3.get_bucket_tagging(Bucket=bucket['Name'])
                tags = {tag['Key']: tag['Value'] for tag in tags_response.get('TagSet', [])}
            except s3.exceptions.NoSuchTagSet:
                tags = {}

            violations = self.validate_tags(tags)
            if violations:
                untagged_resources.append({
                    'ResourceType': 'S3Bucket',
                    'ResourceId': bucket['Name'],
                    'CurrentTags': tags,
                    'Violations': violations,
                    'Region': 'global'
                })

        return untagged_resources

    def apply_default_tags(self, resource_type: str, resource_id: str,
                          region: str, default_tags: Dict[str, str]) -> bool:
        """Apply default tags to a resource."""
        try:
            if resource_type == 'EC2Instance':
                ec2 = self.aws_session.client('ec2', region_name=region)

                # Convert dict to AWS tag format
                tag_list = [{'Key': k, 'Value': v} for k, v in default_tags.items()]

                ec2.create_tags(
                    Resources=[resource_id],
                    Tags=tag_list
                )

            elif resource_type == 'S3Bucket':
                s3 = self.aws_session.client('s3')

                # Convert dict to S3 tag format
                tag_set = [{'Key': k, 'Value': v} for k, v in default_tags.items()]

                s3.put_bucket_tagging(
                    Bucket=resource_id,
                    Tagging={'TagSet': tag_set}
                )

            return True

        except Exception as e:
            print(f"Error applying tags to {resource_id}: {e}")
            return False

    def generate_tagging_report(self) -> Dict:
        """Generate comprehensive tagging compliance report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_resources': 0,
                'compliant_resources': 0,
                'non_compliant_resources': 0,
                'compliance_percentage': 0
            },
            'violations_by_tag': {},
            'violations_by_resource_type': {},
            'untagged_resources': []
        }

        # Get untagged resources across all regions
        regions = ['us-east-1', 'us-west-2', 'eu-west-1']  # Add more regions as needed

        for region in regions:
            untagged = self.get_untagged_resources(region)
            report['untagged_resources'].extend(untagged)

        # Calculate summary statistics
        report['summary']['total_resources'] = len(report['untagged_resources'])
        report['summary']['non_compliant_resources'] = len(report['untagged_resources'])

        # Analyze violations
        for resource in report['untagged_resources']:
            resource_type = resource['ResourceType']
            if resource_type not in report['violations_by_resource_type']:
                report['violations_by_resource_type'][resource_type] = 0
            report['violations_by_resource_type'][resource_type] += 1

            for violation in resource['Violations']:
                if violation not in report['violations_by_tag']:
                    report['violations_by_tag'][violation] = 0
                report['violations_by_tag'][violation] += 1

        # Calculate compliance percentage
        if report['summary']['total_resources'] > 0:
            compliance_rate = (report['summary']['compliant_resources'] /
                             report['summary']['total_resources']) * 100
            report['summary']['compliance_percentage'] = round(compliance_rate, 2)

        return report

# Usage
tagging_manager = CloudTaggingManager()

# Generate tagging compliance report
report = tagging_manager.generate_tagging_report()
print(f"Tagging compliance: {report['summary']['compliance_percentage']:.1f}%")
print(f"Non-compliant resources: {report['summary']['non_compliant_resources']}")

# Apply default tags to non-compliant resources
default_tags = {
    'Environment': 'unknown',
    'Team': 'unassigned',
    'Project': 'legacy',
    'CostCenter': 'CC-9999',
    'Application': 'untagged'
}

for resource in report['untagged_resources'][:5]:  # Limit to first 5 for example
    success = tagging_manager.apply_default_tags(
        resource['ResourceType'],
        resource['ResourceId'],
        resource['Region'],
        default_tags
    )
    print(f"Applied default tags to {resource['ResourceId']}: {success}")
```

---

## 3. Resource Optimization

### 3.1 Compute Optimization

#### Right-sizing Analysis **[REQUIRED]**
```python
# optimization/rightsizing.py
import boto3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import statistics

class ComputeRightsizingAnalyzer:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.ce_client = boto3.client('ce')

    def get_instance_utilization(self, instance_id: str, days: int = 30) -> Dict:
        """Get CPU and memory utilization for an instance."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        # Get CPU utilization
        cpu_response = self.cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour intervals
            Statistics=['Average', 'Maximum']
        )

        # Get memory utilization (requires CloudWatch agent)
        try:
            memory_response = self.cloudwatch_client.get_metric_statistics(
                Namespace='CWAgent',
                MetricName='mem_used_percent',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average', 'Maximum']
            )
        except:
            memory_response = {'Datapoints': []}

        # Calculate utilization statistics
        cpu_values = [dp['Average'] for dp in cpu_response['Datapoints']]
        memory_values = [dp['Average'] for dp in memory_response['Datapoints']]

        return {
            'instance_id': instance_id,
            'cpu_utilization': {
                'average': statistics.mean(cpu_values) if cpu_values else 0,
                'p95': statistics.quantiles(cpu_values, n=20)[18] if len(cpu_values) > 20 else 0,
                'maximum': max(cpu_values) if cpu_values else 0
            },
            'memory_utilization': {
                'average': statistics.mean(memory_values) if memory_values else 0,
                'p95': statistics.quantiles(memory_values, n=20)[18] if len(memory_values) > 20 else 0,
                'maximum': max(memory_values) if memory_values else 0
            },
            'sample_count': len(cpu_values)
        }

    def analyze_rightsizing_opportunities(self) -> List[Dict]:
        """Analyze all instances for rightsizing opportunities."""
        recommendations = []

        # Get all running instances
        instances_response = self.ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )

        for reservation in instances_response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

                # Get utilization data
                utilization = self.get_instance_utilization(instance_id)

                # Determine rightsizing recommendation
                recommendation = self._generate_rightsizing_recommendation(
                    instance, utilization
                )

                if recommendation:
                    recommendations.append(recommendation)

        return recommendations

    def _generate_rightsizing_recommendation(self, instance: Dict, utilization: Dict) -> Dict:
        """Generate rightsizing recommendation based on utilization."""
        instance_id = instance['InstanceId']
        current_type = instance['InstanceType']

        cpu_avg = utilization['cpu_utilization']['average']
        cpu_p95 = utilization['cpu_utilization']['p95']
        memory_avg = utilization['memory_utilization']['average']

        # Define thresholds
        LOW_CPU_THRESHOLD = 20
        HIGH_CPU_THRESHOLD = 80
        LOW_MEMORY_THRESHOLD = 20
        HIGH_MEMORY_THRESHOLD = 80

        recommendation = None
        reason = []

        # Check for underutilization
        if cpu_avg < LOW_CPU_THRESHOLD and memory_avg < LOW_MEMORY_THRESHOLD:
            recommendation = 'downsize'
            reason.append(f"Low CPU utilization ({cpu_avg:.1f}%)")
            reason.append(f"Low memory utilization ({memory_avg:.1f}%)")

        # Check for overutilization
        elif cpu_p95 > HIGH_CPU_THRESHOLD or memory_avg > HIGH_MEMORY_THRESHOLD:
            recommendation = 'upsize'
            if cpu_p95 > HIGH_CPU_THRESHOLD:
                reason.append(f"High CPU utilization P95 ({cpu_p95:.1f}%)")
            if memory_avg > HIGH_MEMORY_THRESHOLD:
                reason.append(f"High memory utilization ({memory_avg:.1f}%)")

        if recommendation:
            # Get potential instance types and savings
            new_type, savings = self._calculate_savings(current_type, recommendation)

            return {
                'instance_id': instance_id,
                'current_type': current_type,
                'recommended_type': new_type,
                'recommendation': recommendation,
                'reason': '; '.join(reason),
                'potential_monthly_savings': savings,
                'utilization': utilization,
                'confidence': self._calculate_confidence(utilization)
            }

        return None

    def _calculate_savings(self, current_type: str, recommendation: str) -> Tuple[str, float]:
        """Calculate potential savings from rightsizing."""
        # Instance type to cost mapping (simplified - use real pricing API)
        instance_costs = {
            't3.micro': 8.47,
            't3.small': 16.93,
            't3.medium': 33.87,
            't3.large': 67.74,
            't3.xlarge': 135.48,
            't3.2xlarge': 270.96,
            'm5.large': 96.36,
            'm5.xlarge': 192.72,
            'm5.2xlarge': 385.44,
            'c5.large': 85.50,
            'c5.xlarge': 171.00,
            'c5.2xlarge': 342.00
        }

        current_cost = instance_costs.get(current_type, 100)  # Default cost

        # Simple recommendation logic (in practice, use more sophisticated analysis)
        if recommendation == 'downsize':
            # Recommend one size smaller
            size_map = {
                't3.small': 't3.micro',
                't3.medium': 't3.small',
                't3.large': 't3.medium',
                't3.xlarge': 't3.large',
                't3.2xlarge': 't3.xlarge',
                'm5.xlarge': 'm5.large',
                'm5.2xlarge': 'm5.xlarge'
            }
            new_type = size_map.get(current_type, current_type)
        else:  # upsize
            size_map = {
                't3.micro': 't3.small',
                't3.small': 't3.medium',
                't3.medium': 't3.large',
                't3.large': 't3.xlarge',
                't3.xlarge': 't3.2xlarge',
                'm5.large': 'm5.xlarge',
                'm5.xlarge': 'm5.2xlarge'
            }
            new_type = size_map.get(current_type, current_type)

        new_cost = instance_costs.get(new_type, current_cost)
        monthly_savings = current_cost - new_cost

        return new_type, monthly_savings

    def _calculate_confidence(self, utilization: Dict) -> str:
        """Calculate confidence level of recommendation."""
        sample_count = utilization['sample_count']

        if sample_count < 168:  # Less than 1 week of hourly data
            return 'low'
        elif sample_count < 720:  # Less than 1 month of hourly data
            return 'medium'
        else:
            return 'high'

    def generate_rightsizing_report(self) -> Dict:
        """Generate comprehensive rightsizing report."""
        recommendations = self.analyze_rightsizing_opportunities()

        # Calculate summary statistics
        total_instances = len(recommendations) if recommendations else 0
        downsize_opportunities = len([r for r in recommendations if r['recommendation'] == 'downsize'])
        upsize_recommendations = len([r for r in recommendations if r['recommendation'] == 'upsize'])
        total_potential_savings = sum([r['potential_monthly_savings'] for r in recommendations if r['potential_monthly_savings'] > 0])

        return {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_instances_analyzed': total_instances,
                'downsize_opportunities': downsize_opportunities,
                'upsize_recommendations': upsize_recommendations,
                'total_potential_monthly_savings': round(total_potential_savings, 2)
            },
            'recommendations': recommendations,
            'top_savings_opportunities': sorted(
                [r for r in recommendations if r['potential_monthly_savings'] > 0],
                key=lambda x: x['potential_monthly_savings'],
                reverse=True
            )[:10]
        }

# Usage
rightsizing_analyzer = ComputeRightsizingAnalyzer()
report = rightsizing_analyzer.generate_rightsizing_report()

print(f"Analyzed {report['summary']['total_instances_analyzed']} instances")
print(f"Found {report['summary']['downsize_opportunities']} downsize opportunities")
print(f"Potential monthly savings: ${report['summary']['total_potential_monthly_savings']:.2f}")

# Print top savings opportunities
for rec in report['top_savings_opportunities'][:5]:
    print(f"Instance {rec['instance_id']}: {rec['current_type']} -> {rec['recommended_type']} "
          f"(${rec['potential_monthly_savings']:.2f}/month)")
```

#### Auto-scaling Optimization **[REQUIRED]**
```python
# optimization/autoscaling.py
import boto3
from datetime import datetime, timedelta
import statistics
from typing import Dict, List

class AutoScalingOptimizer:
    def __init__(self):
        self.autoscaling_client = boto3.client('autoscaling')
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.ec2_client = boto3.client('ec2')

    def analyze_autoscaling_groups(self) -> List[Dict]:
        """Analyze all Auto Scaling groups for optimization opportunities."""
        optimizations = []

        # Get all Auto Scaling groups
        response = self.autoscaling_client.describe_auto_scaling_groups()

        for asg in response['AutoScalingGroups']:
            asg_name = asg['AutoScalingGroupName']

            # Analyze scaling patterns
            analysis = self._analyze_scaling_pattern(asg_name)

            # Generate optimization recommendations
            recommendations = self._generate_scaling_recommendations(asg, analysis)

            if recommendations:
                optimizations.append({
                    'asg_name': asg_name,
                    'current_config': {
                        'min_size': asg['MinSize'],
                        'max_size': asg['MaxSize'],
                        'desired_capacity': asg['DesiredCapacity']
                    },
                    'analysis': analysis,
                    'recommendations': recommendations
                })

        return optimizations

    def _analyze_scaling_pattern(self, asg_name: str, days: int = 30) -> Dict:
        """Analyze scaling patterns for an Auto Scaling group."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        # Get capacity metrics
        capacity_response = self.cloudwatch_client.get_metric_statistics(
            Namespace='AWS/AutoScaling',
            MetricName='GroupDesiredCapacity',
            Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour intervals
            Statistics=['Average', 'Maximum', 'Minimum']
        )

        # Get CPU utilization
        cpu_response = self.cloudwatch_client.get_metric_statistics(
            Namespace='AWS/AutoScaling',
            MetricName='GroupDesiredCapacity',  # This should be CPU metrics from instances
            Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Average']
        )

        capacity_values = [dp['Average'] for dp in capacity_response['Datapoints']]

        if capacity_values:
            analysis = {
                'avg_capacity': statistics.mean(capacity_values),
                'min_capacity': min(capacity_values),
                'max_capacity': max(capacity_values),
                'capacity_variance': statistics.variance(capacity_values) if len(capacity_values) > 1 else 0,
                'scaling_frequency': len([v for i, v in enumerate(capacity_values[1:])
                                        if abs(v - capacity_values[i]) > 0]),
                'utilization_pattern': self._determine_utilization_pattern(capacity_values)
            }
        else:
            analysis = {
                'avg_capacity': 0,
                'min_capacity': 0,
                'max_capacity': 0,
                'capacity_variance': 0,
                'scaling_frequency': 0,
                'utilization_pattern': 'insufficient_data'
            }

        return analysis

    def _determine_utilization_pattern(self, capacity_values: List[float]) -> str:
        """Determine the utilization pattern from capacity data."""
        if not capacity_values:
            return 'insufficient_data'

        avg_capacity = statistics.mean(capacity_values)
        variance = statistics.variance(capacity_values) if len(capacity_values) > 1 else 0

        # Simple pattern classification
        if variance < 0.5:
            return 'stable'
        elif variance < 2.0:
            return 'moderate_scaling'
        else:
            return 'high_scaling'

    def _generate_scaling_recommendations(self, asg: Dict, analysis: Dict) -> List[Dict]:
        """Generate scaling optimization recommendations."""
        recommendations = []
        current_min = asg['MinSize']
        current_max = asg['MaxSize']
        current_desired = asg['DesiredCapacity']

        avg_capacity = analysis['avg_capacity']
        max_capacity = analysis['max_capacity']
        pattern = analysis['utilization_pattern']

        # Check if min size is too high
        if current_min > avg_capacity * 1.2:
            recommendations.append({
                'type': 'reduce_min_size',
                'current_value': current_min,
                'recommended_value': max(1, int(avg_capacity * 0.8)),
                'reason': f'Min size ({current_min}) is higher than typical usage ({avg_capacity:.1f})',
                'potential_savings': self._calculate_savings(current_min - int(avg_capacity * 0.8))
            })

        # Check if max size is too low (causing performance issues)
        if current_max < max_capacity * 1.2 and pattern == 'high_scaling':
            recommendations.append({
                'type': 'increase_max_size',
                'current_value': current_max,
                'recommended_value': int(max_capacity * 1.5),
                'reason': f'Max size may be limiting scaling during peak demand',
                'potential_cost_impact': 'increased_capacity_costs'
            })

        # Check if max size is unnecessarily high
        if current_max > max_capacity * 2 and pattern in ['stable', 'moderate_scaling']:
            recommendations.append({
                'type': 'reduce_max_size',
                'current_value': current_max,
                'recommended_value': int(max_capacity * 1.3),
                'reason': f'Max size ({current_max}) is much higher than actual peak usage ({max_capacity})',
                'benefit': 'reduced_blast_radius'
            })

        return recommendations

    def _calculate_savings(self, instance_reduction: int) -> float:
        """Calculate potential savings from instance reduction."""
        # Simplified calculation - use actual instance pricing
        avg_instance_cost_per_month = 100  # $100/month per instance
        return instance_reduction * avg_instance_cost_per_month

    def optimize_scaling_policies(self, asg_name: str) -> Dict:
        """Analyze and optimize scaling policies."""
        # Get current scaling policies
        policies_response = self.autoscaling_client.describe_policies(
            AutoScalingGroupName=asg_name
        )

        current_policies = policies_response['ScalingPolicies']
        recommendations = []

        for policy in current_policies:
            if policy['PolicyType'] == 'StepScaling':
                # Analyze step scaling policy
                recommendations.extend(self._analyze_step_scaling_policy(policy))
            elif policy['PolicyType'] == 'TargetTrackingScaling':
                # Analyze target tracking policy
                recommendations.extend(self._analyze_target_tracking_policy(policy))

        return {
            'asg_name': asg_name,
            'current_policies': len(current_policies),
            'policy_recommendations': recommendations
        }

    def _analyze_step_scaling_policy(self, policy: Dict) -> List[Dict]:
        """Analyze step scaling policy for optimization."""
        recommendations = []

        step_adjustments = policy.get('StepAdjustments', [])

        # Check for overlapping or inefficient steps
        if len(step_adjustments) > 3:
            recommendations.append({
                'type': 'simplify_steps',
                'reason': 'Too many step adjustments can cause oscillation',
                'recommendation': 'Consider consolidating to 2-3 steps'
            })

        return recommendations

    def _analyze_target_tracking_policy(self, policy: Dict) -> List[Dict]:
        """Analyze target tracking policy for optimization."""
        recommendations = []

        target_value = policy['TargetValue']
        metric_type = policy['TargetTrackingConfiguration']['PredefinedMetricSpecification']['PredefinedMetricType']

        # Check CPU target values
        if metric_type == 'ASGAverageCPUUtilization':
            if target_value > 80:
                recommendations.append({
                    'type': 'adjust_cpu_target',
                    'current_value': target_value,
                    'recommended_value': 70,
                    'reason': 'High CPU target may cause performance issues'
                })
            elif target_value < 40:
                recommendations.append({
                    'type': 'adjust_cpu_target',
                    'current_value': target_value,
                    'recommended_value': 50,
                    'reason': 'Low CPU target may cause unnecessary scaling'
                })

        return recommendations

# Usage
asg_optimizer = AutoScalingOptimizer()

# Analyze all Auto Scaling groups
optimizations = asg_optimizer.analyze_autoscaling_groups()

total_savings = 0
for opt in optimizations:
    print(f"\nAuto Scaling Group: {opt['asg_name']}")
    print(f"Current config: Min={opt['current_config']['min_size']}, "
          f"Max={opt['current_config']['max_size']}, "
          f"Desired={opt['current_config']['desired_capacity']}")

    for rec in opt['recommendations']:
        print(f"- {rec['type']}: {rec['reason']}")
        if 'potential_savings' in rec:
            total_savings += rec['potential_savings']
            print(f"  Potential savings: ${rec['potential_savings']:.2f}/month")

print(f"\nTotal potential monthly savings: ${total_savings:.2f}")
```

### 3.2 Storage Optimization

#### Storage Cost Analysis **[REQUIRED]**
```python
# optimization/storage.py
import boto3
from datetime import datetime, timedelta
import json
from typing import Dict, List

class StorageOptimizer:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.ce_client = boto3.client('ce')

    def analyze_s3_storage_costs(self) -> Dict:
        """Analyze S3 storage costs and optimization opportunities."""
        buckets = self.s3_client.list_buckets()['Buckets']
        analysis = {
            'total_buckets': len(buckets),
            'bucket_analysis': [],
            'optimization_opportunities': [],
            'total_potential_savings': 0
        }

        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_analysis = self._analyze_bucket(bucket_name)
            analysis['bucket_analysis'].append(bucket_analysis)

            # Check for optimization opportunities
            opportunities = self._identify_storage_optimizations(bucket_analysis)
            if opportunities:
                analysis['optimization_opportunities'].extend(opportunities)

        # Calculate total potential savings
        analysis['total_potential_savings'] = sum([
            opp.get('potential_monthly_savings', 0)
            for opp in analysis['optimization_opportunities']
        ])

        return analysis

    def _analyze_bucket(self, bucket_name: str) -> Dict:
        """Analyze individual S3 bucket for cost optimization."""
        try:
            # Get bucket size and object count
            size_response = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=datetime.utcnow() - timedelta(days=1),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )

            objects_response = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='NumberOfObjects',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
                ],
                StartTime=datetime.utcnow() - timedelta(days=1),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )

            # Get lifecycle configuration
            try:
                lifecycle = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                has_lifecycle = True
                lifecycle_rules = len(lifecycle.get('Rules', []))
            except self.s3_client.exceptions.NoSuchLifecycleConfiguration:
                has_lifecycle = False
                lifecycle_rules = 0

            # Get versioning status
            try:
                versioning = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
                versioning_status = versioning.get('Status', 'Disabled')
            except:
                versioning_status = 'Disabled'

            # Get bucket size in bytes
            bucket_size = 0
            object_count = 0

            if size_response['Datapoints']:
                bucket_size = size_response['Datapoints'][0]['Average']

            if objects_response['Datapoints']:
                object_count = int(objects_response['Datapoints'][0]['Average'])

            # Analyze storage class distribution
            storage_classes = self._get_storage_class_distribution(bucket_name)

            return {
                'bucket_name': bucket_name,
                'size_bytes': bucket_size,
                'size_gb': bucket_size / (1024**3),
                'object_count': object_count,
                'has_lifecycle_policy': has_lifecycle,
                'lifecycle_rules_count': lifecycle_rules,
                'versioning_status': versioning_status,
                'storage_classes': storage_classes,
                'monthly_cost_estimate': self._estimate_monthly_cost(bucket_size, storage_classes)
            }

        except Exception as e:
            return {
                'bucket_name': bucket_name,
                'error': str(e),
                'size_bytes': 0,
                'size_gb': 0,
                'object_count': 0
            }

    def _get_storage_class_distribution(self, bucket_name: str) -> Dict:
        """Get distribution of objects across storage classes."""
        storage_classes = {
            'STANDARD': 0,
            'STANDARD_IA': 0,
            'GLACIER': 0,
            'DEEP_ARCHIVE': 0,
            'INTELLIGENT_TIERING': 0
        }

        try:
            # This is a simplified approach - in practice, you'd need to
            # iterate through all objects or use S3 Inventory
            paginator = self.s3_client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=bucket_name, MaxKeys=1000):  # Limit for example
                if 'Contents' in page:
                    for obj in page['Contents']:
                        storage_class = obj.get('StorageClass', 'STANDARD')
                        if storage_class in storage_classes:
                            storage_classes[storage_class] += obj['Size']
        except Exception as e:
            print(f"Error getting storage class distribution for {bucket_name}: {e}")

        return storage_classes

    def _estimate_monthly_cost(self, total_size_bytes: float, storage_classes: Dict) -> float:
        """Estimate monthly storage cost based on size and storage classes."""
        # S3 pricing (simplified - use actual regional pricing)
        pricing_per_gb = {
            'STANDARD': 0.023,
            'STANDARD_IA': 0.0125,
            'GLACIER': 0.004,
            'DEEP_ARCHIVE': 0.00099,
            'INTELLIGENT_TIERING': 0.0125
        }

        total_cost = 0
        total_gb = total_size_bytes / (1024**3)

        # If we have storage class breakdown, use it
        if any(storage_classes.values()):
            for storage_class, size_bytes in storage_classes.items():
                size_gb = size_bytes / (1024**3)
                cost = size_gb * pricing_per_gb.get(storage_class, 0.023)
                total_cost += cost
        else:
            # Assume all STANDARD storage
            total_cost = total_gb * pricing_per_gb['STANDARD']

        return total_cost

    def _identify_storage_optimizations(self, bucket_analysis: Dict) -> List[Dict]:
        """Identify storage optimization opportunities for a bucket."""
        opportunities = []
        bucket_name = bucket_analysis['bucket_name']
        size_gb = bucket_analysis.get('size_gb', 0)
        monthly_cost = bucket_analysis.get('monthly_cost_estimate', 0)

        # Skip small buckets (less than 1GB)
        if size_gb < 1:
            return opportunities

        # Check for missing lifecycle policy
        if not bucket_analysis.get('has_lifecycle_policy', False) and size_gb > 10:
            # Estimate savings from lifecycle policy
            potential_savings = monthly_cost * 0.3  # Assume 30% savings

            opportunities.append({
                'bucket_name': bucket_name,
                'type': 'lifecycle_policy',
                'description': 'Implement lifecycle policy to transition older objects to cheaper storage',
                'potential_monthly_savings': potential_savings,
                'implementation': {
                    'transition_to_ia_after_days': 30,
                    'transition_to_glacier_after_days': 90,
                    'transition_to_deep_archive_after_days': 365
                }
            })

        # Check for versioning without lifecycle
        if (bucket_analysis.get('versioning_status') == 'Enabled' and
            bucket_analysis.get('lifecycle_rules_count', 0) == 0):

            # Versioned objects can accumulate significant costs
            potential_savings = monthly_cost * 0.4  # Assume 40% savings

            opportunities.append({
                'bucket_name': bucket_name,
                'type': 'version_management',
                'description': 'Add lifecycle rules to delete old versions',
                'potential_monthly_savings': potential_savings,
                'implementation': {
                    'delete_non_current_versions_after_days': 30,
                    'delete_incomplete_multipart_uploads_after_days': 7
                }
            })

        # Check for inefficient storage class usage
        storage_classes = bucket_analysis.get('storage_classes', {})
        standard_storage = storage_classes.get('STANDARD', 0)

        if standard_storage > 0 and size_gb > 5:
            # Suggest Intelligent Tiering for large buckets with mixed access patterns
            current_standard_cost = (standard_storage / (1024**3)) * 0.023
            intelligent_tiering_cost = (standard_storage / (1024**3)) * 0.0125
            potential_savings = current_standard_cost - intelligent_tiering_cost

            if potential_savings > 5:  # Only suggest if savings > $5/month
                opportunities.append({
                    'bucket_name': bucket_name,
                    'type': 'intelligent_tiering',
                    'description': 'Consider Intelligent Tiering for mixed access patterns',
                    'potential_monthly_savings': potential_savings,
                    'implementation': 'Enable S3 Intelligent Tiering'
                })

        return opportunities

    def generate_lifecycle_policy(self, bucket_name: str,
                                 ia_days: int = 30,
                                 glacier_days: int = 90,
                                 deep_archive_days: int = 365) -> Dict:
        """Generate lifecycle policy for a bucket."""

        lifecycle_policy = {
            'Rules': [
                {
                    'ID': 'OptimizationRule',
                    'Status': 'Enabled',
                    'Filter': {'Prefix': ''},
                    'Transitions': [
                        {
                            'Days': ia_days,
                            'StorageClass': 'STANDARD_IA'
                        },
                        {
                            'Days': glacier_days,
                            'StorageClass': 'GLACIER'
                        },
                        {
                            'Days': deep_archive_days,
                            'StorageClass': 'DEEP_ARCHIVE'
                        }
                    ],
                    'NoncurrentVersionTransitions': [
                        {
                            'NoncurrentDays': 30,
                            'StorageClass': 'STANDARD_IA'
                        },
                        {
                            'NoncurrentDays': 90,
                            'StorageClass': 'GLACIER'
                        }
                    ],
                    'NoncurrentVersionExpiration': {
                        'NoncurrentDays': 365
                    },
                    'AbortIncompleteMultipartUpload': {
                        'DaysAfterInitiation': 7
                    }
                }
            ]
        }

        return lifecycle_policy

    def implement_optimization(self, opportunity: Dict) -> bool:
        """Implement a storage optimization opportunity."""
        bucket_name = opportunity['bucket_name']
        optimization_type = opportunity['type']

        try:
            if optimization_type == 'lifecycle_policy':
                implementation = opportunity['implementation']
                lifecycle_policy = self.generate_lifecycle_policy(
                    bucket_name,
                    implementation['transition_to_ia_after_days'],
                    implementation['transition_to_glacier_after_days'],
                    implementation['transition_to_deep_archive_after_days']
                )

                self.s3_client.put_bucket_lifecycle_configuration(
                    Bucket=bucket_name,
                    LifecycleConfiguration=lifecycle_policy
                )

                return True

            elif optimization_type == 'intelligent_tiering':
                # Enable Intelligent Tiering (requires S3 Inventory configuration)
                intelligent_tiering_config = {
                    'Id': 'EntireBucket',
                    'Filter': {'Prefix': ''},
                    'Status': 'Enabled',
                    'Tierings': [
                        {
                            'Days': 1,
                            'AccessTier': 'ARCHIVE_ACCESS'
                        },
                        {
                            'Days': 90,
                            'AccessTier': 'DEEP_ARCHIVE_ACCESS'
                        }
                    ]
                }

                # Note: This would require additional S3 API calls
                print(f"Would configure Intelligent Tiering for {bucket_name}")
                return True

        except Exception as e:
            print(f"Error implementing optimization for {bucket_name}: {e}")
            return False

# Usage
storage_optimizer = StorageOptimizer()

# Analyze all S3 storage
analysis = storage_optimizer.analyze_s3_storage_costs()

print(f"Analyzed {analysis['total_buckets']} S3 buckets")
print(f"Found {len(analysis['optimization_opportunities'])} optimization opportunities")
print(f"Total potential monthly savings: ${analysis['total_potential_savings']:.2f}")

# Show top opportunities
for opp in sorted(analysis['optimization_opportunities'],
                  key=lambda x: x.get('potential_monthly_savings', 0),
                  reverse=True)[:5]:
    print(f"\nBucket: {opp['bucket_name']}")
    print(f"Type: {opp['type']}")
    print(f"Description: {opp['description']}")
    print(f"Potential savings: ${opp.get('potential_monthly_savings', 0):.2f}/month")

# Implement top optimization
if analysis['optimization_opportunities']:
    top_opportunity = max(analysis['optimization_opportunities'],
                         key=lambda x: x.get('potential_monthly_savings', 0))

    print(f"\nImplementing top optimization for {top_opportunity['bucket_name']}...")
    success = storage_optimizer.implement_optimization(top_opportunity)
    print(f"Implementation {'successful' if success else 'failed'}")
```

---

## 4. Cost Monitoring and Alerting

### 4.1 Real-time Cost Monitoring

#### Cost Anomaly Detection **[REQUIRED]**
```python
# monitoring/anomaly_detection.py
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class CostAnomalyDetector:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.sns_client = boto3.client('sns')

    def get_historical_costs(self, days: int = 90, granularity: str = 'DAILY') -> pd.DataFrame:
        """Get historical cost data for anomaly detection."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.isoformat(),
                'End': end_date.isoformat()
            },
            Granularity=granularity,
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )

        # Convert to DataFrame
        data = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                data.append({
                    'Date': pd.to_datetime(date),
                    'Service': service,
                    'Cost': cost
                })

        df = pd.DataFrame(data)
        return df

    def detect_cost_anomalies(self, df: pd.DataFrame, contamination: float = 0.1) -> List[Dict]:
        """Detect cost anomalies using Isolation Forest."""
        anomalies = []

        # Group by service for individual analysis
        for service in df['Service'].unique():
            service_data = df[df['Service'] == service].copy()

            if len(service_data) < 7:  # Need at least a week of data
                continue

            # Feature engineering
            service_data['DayOfWeek'] = service_data['Date'].dt.dayofweek
            service_data['Month'] = service_data['Date'].dt.month
            service_data['Day'] = service_data['Date'].dt.day

            # Calculate rolling statistics
            service_data['RollingMean7'] = service_data['Cost'].rolling(window=7).mean()
            service_data['RollingStd7'] = service_data['Cost'].rolling(window=7).std()
            service_data['CostChange'] = service_data['Cost'].pct_change()

            # Prepare features for anomaly detection
            features = ['Cost', 'DayOfWeek', 'Month', 'Day', 'CostChange']
            feature_data = service_data[features].dropna()

            if len(feature_data) < 7:
                continue

            # Normalize features
            scaler = StandardScaler()
            normalized_features = scaler.fit_transform(feature_data)

            # Detect anomalies using Isolation Forest
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )

            anomaly_labels = iso_forest.fit_predict(normalized_features)
            anomaly_scores = iso_forest.score_samples(normalized_features)

            # Identify anomalies
            anomaly_indices = np.where(anomaly_labels == -1)[0]

            for idx in anomaly_indices:
                original_idx = feature_data.iloc[idx].name
                anomaly_data = service_data.loc[original_idx]

                # Calculate anomaly metrics
                cost = anomaly_data['Cost']
                rolling_mean = anomaly_data['RollingMean7']
                rolling_std = anomaly_data['RollingStd7']

                # Calculate z-score
                z_score = (cost - rolling_mean) / rolling_std if rolling_std > 0 else 0

                # Determine severity
                severity = self._determine_anomaly_severity(abs(z_score), cost)

                anomalies.append({
                    'date': anomaly_data['Date'].isoformat(),
                    'service': service,
                    'cost': cost,
                    'expected_cost': rolling_mean,
                    'cost_difference': cost - rolling_mean,
                    'cost_difference_percent': ((cost - rolling_mean) / rolling_mean * 100) if rolling_mean > 0 else 0,
                    'z_score': z_score,
                    'anomaly_score': anomaly_scores[idx],
                    'severity': severity,
                    'confidence': abs(anomaly_scores[idx])
                })

        # Sort by severity and cost impact
        anomalies.sort(key=lambda x: (x['severity'], abs(x['cost_difference'])), reverse=True)

        return anomalies

    def _determine_anomaly_severity(self, z_score: float, cost: float) -> str:
        """Determine the severity of a cost anomaly."""
        if z_score > 3 or cost > 1000:
            return 'critical'
        elif z_score > 2 or cost > 500:
            return 'high'
        elif z_score > 1.5 or cost > 100:
            return 'medium'
        else:
            return 'low'

    def create_cost_alert(self, anomaly: Dict) -> Dict:
        """Create a cost alert for an anomaly."""
        alert = {
            'alert_id': f"cost-anomaly-{int(datetime.now().timestamp())}",
            'timestamp': datetime.now().isoformat(),
            'type': 'cost_anomaly',
            'severity': anomaly['severity'],
            'title': f"Cost Anomaly Detected: {anomaly['service']}",
            'description': f"Unusual cost detected for {anomaly['service']} on {anomaly['date']}",
            'details': {
                'service': anomaly['service'],
                'date': anomaly['date'],
                'actual_cost': round(anomaly['cost'], 2),
                'expected_cost': round(anomaly['expected_cost'], 2),
                'difference': round(anomaly['cost_difference'], 2),
                'difference_percent': round(anomaly['cost_difference_percent'], 1),
                'z_score': round(anomaly['z_score'], 2)
            },
            'recommended_actions': self._generate_recommended_actions(anomaly)
        }

        return alert

    def _generate_recommended_actions(self, anomaly: Dict) -> List[str]:
        """Generate recommended actions for a cost anomaly."""
        actions = []
        service = anomaly['service']
        severity = anomaly['severity']

        if severity in ['critical', 'high']:
            actions.append(f"Immediately investigate {service} usage and recent changes")
            actions.append("Check for any new resource deployments or configuration changes")

        if anomaly['cost_difference'] > 0:  # Cost increase
            actions.extend([
                f"Review {service} resource utilization for scaling events",
                "Check for any data transfer or API usage spikes",
                "Verify that resources are properly tagged and allocated"
            ])
        else:  # Cost decrease (unusual)
            actions.extend([
                f"Verify {service} is functioning normally despite lower costs",
                "Check if resources were unexpectedly terminated or scaled down"
            ])

        actions.append("Update cost forecasts and budgets if this represents a new baseline")

        return actions

    def send_alert_notification(self, alert: Dict, sns_topic_arn: str) -> bool:
        """Send alert notification via SNS."""
        try:
            message = {
                'default': f"Cost Anomaly Alert: {alert['title']}",
                'email': self._format_email_alert(alert),
                'sms': f"Cost Alert: {alert['details']['service']} cost anomaly detected. "
                       f"${alert['details']['difference']:.2f} above expected."
            }

            self.sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(message),
                MessageStructure='json',
                Subject=f"Cost Anomaly Alert - {alert['severity'].upper()}"
            )

            return True

        except Exception as e:
            print(f"Error sending alert notification: {e}")
            return False

    def _format_email_alert(self, alert: Dict) -> str:
        """Format alert for email notification."""
        details = alert['details']

        email_body = f"""
        Cost Anomaly Detection Alert

        Alert ID: {alert['alert_id']}
        Severity: {alert['severity'].upper()}
        Timestamp: {alert['timestamp']}

        Service: {details['service']}
        Date: {details['date']}

        Cost Analysis:
        - Actual Cost: ${details['actual_cost']:.2f}
        - Expected Cost: ${details['expected_cost']:.2f}
        - Difference: ${details['difference']:.2f} ({details['difference_percent']:.1f}%)
        - Z-Score: {details['z_score']:.2f}

        Recommended Actions:
        """

        for i, action in enumerate(alert['recommended_actions'], 1):
            email_body += f"\n{i}. {action}"

        email_body += f"""

        Please investigate this anomaly and take appropriate action.

        This alert was generated automatically by the Cost Anomaly Detection system.
        """

        return email_body

    def run_anomaly_detection_pipeline(self, sns_topic_arn: str = None) -> Dict:
        """Run the complete anomaly detection pipeline."""
        # Get historical cost data
        print("Fetching historical cost data...")
        df = self.get_historical_costs(days=90)

        if df.empty:
            return {'status': 'error', 'message': 'No cost data available'}

        # Detect anomalies
        print("Detecting cost anomalies...")
        anomalies = self.detect_cost_anomalies(df)

        # Process alerts
        alerts_sent = 0
        critical_anomalies = []

        for anomaly in anomalies:
            if anomaly['severity'] in ['critical', 'high']:
                alert = self.create_cost_alert(anomaly)
                critical_anomalies.append(alert)

                if sns_topic_arn:
                    if self.send_alert_notification(alert, sns_topic_arn):
                        alerts_sent += 1

        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'total_anomalies': len(anomalies),
            'critical_anomalies': len(critical_anomalies),
            'alerts_sent': alerts_sent,
            'anomalies': anomalies[:10],  # Return top 10 anomalies
            'summary': {
                'total_services_analyzed': df['Service'].nunique(),
                'date_range': {
                    'start': df['Date'].min().isoformat(),
                    'end': df['Date'].max().isoformat()
                },
                'total_cost_analyzed': df['Cost'].sum()
            }
        }

# Usage
anomaly_detector = CostAnomalyDetector()

# Run anomaly detection
result = anomaly_detector.run_anomaly_detection_pipeline(
    sns_topic_arn='arn:aws:sns:us-east-1:123456789012:cost-alerts'
)

print(f"Anomaly detection completed: {result['status']}")
print(f"Total anomalies found: {result['total_anomalies']}")
print(f"Critical anomalies: {result['critical_anomalies']}")
print(f"Alerts sent: {result['alerts_sent']}")

# Display top anomalies
for anomaly in result['anomalies'][:5]:
    print(f"\n{anomaly['service']}: ${anomaly['cost']:.2f} "
          f"({anomaly['cost_difference_percent']:+.1f}%) on {anomaly['date']}")
```

### 4.2 Budget Management and Alerts

#### Advanced Budget Management **[REQUIRED]**
```python
# budgets/management.py
import boto3
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
from enum import Enum

class BudgetType(Enum):
    COST = "COST"
    USAGE = "USAGE"
    RI_UTILIZATION = "RI_UTILIZATION"
    RI_COVERAGE = "RI_COVERAGE"
    SAVINGS_PLANS_UTILIZATION = "SAVINGS_PLANS_UTILIZATION"
    SAVINGS_PLANS_COVERAGE = "SAVINGS_PLANS_COVERAGE"

class BudgetTimeUnit(Enum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"

class BudgetManager:
    def __init__(self):
        self.budgets_client = boto3.client('budgets')
        self.account_id = boto3.client('sts').get_caller_identity()['Account']

    def create_hierarchical_budgets(self,
                                   total_budget: float,
                                   budget_breakdown: Dict[str, float]) -> List[Dict]:
        """Create hierarchical budget structure."""
        budgets_created = []

        # Create master budget
        master_budget = self.create_budget(
            budget_name="Master-Budget",
            budget_amount=total_budget,
            time_unit=BudgetTimeUnit.MONTHLY,
            cost_filters={},
            alert_thresholds=[50, 80, 100, 120]
        )
        budgets_created.append(master_budget)

        # Create departmental budgets
        for department, amount in budget_breakdown.items():
            dept_budget = self.create_budget(
                budget_name=f"Budget-{department}",
                budget_amount=amount,
                time_unit=BudgetTimeUnit.MONTHLY,
                cost_filters={
                    'TagKey': 'Team',
                    'Values': [department]
                },
                alert_thresholds=[75, 90, 100]
            )
            budgets_created.append(dept_budget)

        # Create environment-based budgets
        environments = ['production', 'staging', 'development']
        env_budget_split = total_budget * 0.7  # 70% for env-specific budgets

        for env in environments:
            env_percentage = {'production': 0.6, 'staging': 0.25, 'development': 0.15}
            env_amount = env_budget_split * env_percentage[env]

            env_budget = self.create_budget(
                budget_name=f"Budget-{env.title()}-Environment",
                budget_amount=env_amount,
                time_unit=BudgetTimeUnit.MONTHLY,
                cost_filters={
                    'TagKey': 'Environment',
                    'Values': [env]
                },
                alert_thresholds=[80, 95, 100]
            )
            budgets_created.append(env_budget)

        return budgets_created

    def create_budget(self,
                     budget_name: str,
                     budget_amount: float,
                     time_unit: BudgetTimeUnit = BudgetTimeUnit.MONTHLY,
                     budget_type: BudgetType = BudgetType.COST,
                     cost_filters: Dict = None,
                     alert_thresholds: List[float] = None) -> Dict:
        """Create a comprehensive budget with alerts."""

        # Default alert thresholds
        if alert_thresholds is None:
            alert_thresholds = [80, 100]

        # Define time period
        now = datetime.now()
        if time_unit == BudgetTimeUnit.MONTHLY:
            start_date = now.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        else:
            start_date = now.replace(month=1, day=1)
            end_date = start_date.replace(year=start_date.year + 1)

        # Create budget definition
        budget = {
            'BudgetName': budget_name,
            'BudgetLimit': {
                'Amount': str(budget_amount),
                'Unit': 'USD'
            },
            'TimeUnit': time_unit.value,
            'TimePeriod': {
                'Start': start_date.date(),
                'End': end_date.date()
            },
            'BudgetType': budget_type.value,
            'CostFilters': cost_filters or {}
        }

        # Create notifications
        notifications = []
        for threshold in alert_thresholds:
            # Actual cost notification
            notifications.append({
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': threshold,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {
                        'SubscriptionType': 'EMAIL',
                        'Address': 'finops-team@company.com'
                    },
                    {
                        'SubscriptionType': 'SNS',
                        'Address': f'arn:aws:sns:us-east-1:{self.account_id}:budget-alerts'
                    }
                ]
            })

            # Forecasted cost notification (for thresholds >= 100%)
            if threshold >= 100:
                notifications.append({
                    'Notification': {
                        'NotificationType': 'FORECASTED',
                        'ComparisonOperator': 'GREATER_THAN',
                        'Threshold': threshold,
                        'ThresholdType': 'PERCENTAGE'
                    },
                    'Subscribers': [
                        {
                            'SubscriptionType': 'EMAIL',
                            'Address': 'finops-alerts@company.com'
                        }
                    ]
                })

        try:
            response = self.budgets_client.create_budget(
                AccountId=self.account_id,
                Budget=budget,
                NotificationsWithSubscribers=notifications
            )

            return {
                'budget_name': budget_name,
                'amount': budget_amount,
                'status': 'created',
                'notifications_count': len(notifications)
            }

        except Exception as e:
            return {
                'budget_name': budget_name,
                'amount': budget_amount,
                'status': 'failed',
                'error': str(e)
            }

    def create_dynamic_budget(self,
                             budget_name: str,
                             historical_months: int = 3,
                             growth_factor: float = 1.1,
                             cost_filters: Dict = None) -> Dict:
        """Create a budget based on historical spending patterns."""

        # Get historical cost data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=historical_months * 30)

        ce_client = boto3.client('ce')
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.isoformat(),
                'End': end_date.isoformat()
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[],
            Filter=cost_filters or {}
        )

        # Calculate average monthly cost
        monthly_costs = []
        for result in response['ResultsByTime']:
            if result['Total']:
                cost = float(result['Total']['BlendedCost']['Amount'])
                monthly_costs.append(cost)

        if not monthly_costs:
            average_cost = 1000  # Default budget
        else:
            average_cost = sum(monthly_costs) / len(monthly_costs)

        # Apply growth factor
        budget_amount = average_cost * growth_factor

        # Create the budget
        return self.create_budget(
            budget_name=budget_name,
            budget_amount=budget_amount,
            cost_filters=cost_filters,
            alert_thresholds=[80, 90, 100, 110]
        )

    def get_budget_status(self, budget_name: str) -> Dict:
        """Get current status of a budget."""
        try:
            response = self.budgets_client.describe_budget(
                AccountId=self.account_id,
                BudgetName=budget_name
            )

            budget = response['Budget']

            # Get budget utilization
            utilization_response = self.budgets_client.describe_budget_performance_history(
                AccountId=self.account_id,
                BudgetName=budget_name,
                TimePeriod={
                    'Start': datetime.now().replace(day=1).date(),
                    'End': datetime.now().date()
                }
            )

            # Calculate utilization
            budget_limit = float(budget['BudgetLimit']['Amount'])
            actual_spend = 0
            forecasted_spend = 0

            if utilization_response['BudgetPerformanceHistory']:
                history = utilization_response['BudgetPerformanceHistory'][0]
                if 'ActualCost' in history:
                    actual_spend = float(history['ActualCost']['Amount'])
                if 'ForecastedCost' in history:
                    forecasted_spend = float(history['ForecastedCost']['Amount'])

            utilization_percentage = (actual_spend / budget_limit) * 100 if budget_limit > 0 else 0

            return {
                'budget_name': budget_name,
                'budget_limit': budget_limit,
                'actual_spend': actual_spend,
                'forecasted_spend': forecasted_spend,
                'utilization_percentage': round(utilization_percentage, 2),
                'remaining_budget': budget_limit - actual_spend,
                'status': self._determine_budget_status(utilization_percentage),
                'time_unit': budget['TimeUnit'],
                'currency': budget['BudgetLimit']['Unit']
            }

        except Exception as e:
            return {
                'budget_name': budget_name,
                'status': 'error',
                'error': str(e)
            }

    def _determine_budget_status(self, utilization_percentage: float) -> str:
        """Determine budget status based on utilization."""
        if utilization_percentage >= 100:
            return 'exceeded'
        elif utilization_percentage >= 80:
            return 'warning'
        elif utilization_percentage >= 50:
            return 'on_track'
        else:
            return 'under_budget'

    def generate_budget_report(self) -> Dict:
        """Generate comprehensive budget report."""
        try:
            # Get all budgets
            response = self.budgets_client.describe_budgets(
                AccountId=self.account_id,
                MaxResults=100
            )

            budgets = response['Budgets']
            budget_statuses = []

            total_budget_limit = 0
            total_actual_spend = 0
            total_forecasted_spend = 0

            for budget in budgets:
                budget_name = budget['BudgetName']
                status = self.get_budget_status(budget_name)
                budget_statuses.append(status)

                if status['status'] != 'error':
                    total_budget_limit += status['budget_limit']
                    total_actual_spend += status['actual_spend']
                    total_forecasted_spend += status['forecasted_spend']

            # Calculate summary statistics
            exceeded_budgets = len([b for b in budget_statuses if b.get('status') == 'exceeded'])
            warning_budgets = len([b for b in budget_statuses if b.get('status') == 'warning'])

            return {
                'report_timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_budgets': len(budgets),
                    'total_budget_limit': round(total_budget_limit, 2),
                    'total_actual_spend': round(total_actual_spend, 2),
                    'total_forecasted_spend': round(total_forecasted_spend, 2),
                    'overall_utilization': round((total_actual_spend / total_budget_limit) * 100, 2) if total_budget_limit > 0 else 0,
                    'exceeded_budgets': exceeded_budgets,
                    'warning_budgets': warning_budgets
                },
                'budget_details': budget_statuses,
                'recommendations': self._generate_budget_recommendations(budget_statuses)
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _generate_budget_recommendations(self, budget_statuses: List[Dict]) -> List[str]:
        """Generate budget management recommendations."""
        recommendations = []

        exceeded_budgets = [b for b in budget_statuses if b.get('status') == 'exceeded']
        warning_budgets = [b for b in budget_statuses if b.get('status') == 'warning']
        under_budgets = [b for b in budget_statuses if b.get('status') == 'under_budget']

        if exceeded_budgets:
            recommendations.append(f"Immediate action required: {len(exceeded_budgets)} budgets exceeded")
            recommendations.append("Review cost drivers for exceeded budgets and implement controls")

        if warning_budgets:
            recommendations.append(f"Monitor closely: {len(warning_budgets)} budgets approaching limits")

        if under_budgets:
            recommendations.append(f"Consider reallocating funds from {len(under_budgets)} under-utilized budgets")

        if len(budget_statuses) < 5:
            recommendations.append("Consider creating more granular budgets for better cost control")

        return recommendations

# Usage
budget_manager = BudgetManager()

# Create hierarchical budget structure
budget_breakdown = {
    'platform': 15000,
    'frontend': 8000,
    'backend': 12000,
    'data': 10000,
    'security': 5000
}

budgets = budget_manager.create_hierarchical_budgets(
    total_budget=50000,
    budget_breakdown=budget_breakdown
)

print(f"Created {len(budgets)} budgets:")
for budget in budgets:
    print(f"- {budget['budget_name']}: ${budget['amount']:.2f} ({budget['status']})")

# Generate budget report
report = budget_manager.generate_budget_report()
print(f"\nBudget Report Summary:")
print(f"Total budgets: {report['summary']['total_budgets']}")
print(f"Overall utilization: {report['summary']['overall_utilization']:.1f}%")
print(f"Exceeded budgets: {report['summary']['exceeded_budgets']}")

for rec in report['recommendations']:
    print(f"- {rec}")
```

---

## Implementation Checklist

### FinOps Foundation
- [ ] FinOps principles documented and communicated
- [ ] Cross-functional team established
- [ ] Roles and responsibilities defined
- [ ] Maturity assessment completed
- [ ] Improvement roadmap created

### Cost Management
- [ ] Multi-cloud cost visibility implemented
- [ ] Tagging strategy enforced
- [ ] Cost allocation automated
- [ ] Historical analysis capabilities
- [ ] Cost forecasting implemented

### Resource Optimization
- [ ] Rightsizing analysis automated
- [ ] Auto-scaling optimization
- [ ] Storage lifecycle policies
- [ ] Reserved Instance/Savings Plans optimization
- [ ] Idle resource identification

### Monitoring and Alerting
- [ ] Real-time cost monitoring
- [ ] Anomaly detection system
- [ ] Budget management automation
- [ ] Alert escalation procedures
- [ ] Dashboard and reporting

### Automation and Tooling
- [ ] Cost optimization automation
- [ ] Policy enforcement automation
- [ ] Reporting automation
- [ ] Integration with existing tools
- [ ] API access for cost data

### Governance and Process
- [ ] Cost review processes
- [ ] Approval workflows
- [ ] Vendor management procedures
- [ ] Compliance monitoring
- [ ] Training and enablement

---

**End of Cost Optimization and FinOps Standards**
