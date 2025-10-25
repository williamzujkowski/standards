# Serverless - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [AWS Lambda Fundamentals](#aws-lambda-fundamentals)
- [Serverless Frameworks](#serverless-frameworks)
- [Event Sources and Triggers](#event-sources-and-triggers)
- [Cold Start Optimization](#cold-start-optimization)
- [State Management](#state-management)
- [Observability and Monitoring](#observability-and-monitoring)
- [Security Best Practices](#security-best-practices)
- [Testing Strategies](#testing-strategies)
- [Cost Optimization](#cost-optimization)
- [Basic Usage](#basic-usage)

---

## Code Examples

### Example 0

```python
# Initialization (runs once per cold start)
import json
import boto3
import os
from aws_xray_sdk.core import patch_all

# Patch SDK clients for X-Ray tracing
patch_all()

# Initialize outside handler (connection reuse)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    """
    Lambda handler function (runs per invocation).

    Args:
        event: Input event data (dict)
        context: Runtime information (LambdaContext)
    """
    try:
        # Extract request data
        body = json.loads(event['body'])
        user_id = body['user_id']

        # Business logic
        response = table.get_item(Key={'id': user_id})
        item = response.get('Item', {})

        # Return API Gateway response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### Example 1

```bash
# Create layer
mkdir -p layer/python
pip install requests -t layer/python/
cd layer && zip -r ../requests-layer.zip .

# Publish layer
aws lambda publish-layer-version \
  --layer-name requests-layer \
  --zip-file fileb://../requests-layer.zip \
  --compatible-runtimes python3.11
```

### Example 2

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.11
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  GetUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /users/{id}
            Method: get
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref UsersTable

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

### Example 3

```yaml
# serverless.yml
service: user-service

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    TABLE_NAME: ${self:service}-${self:provider.stage}-users
  iam:
    role:
      statements:
        - Effect: Allow
          Action: dynamodb:GetItem
          Resource: !GetAtt UsersTable.Arn

functions:
  getUser:
    handler: handler.get_user
    events:
      - http:
          path: users/{id}
          method: get
          cors: true

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH
```

### Example 4

```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class UserServiceStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string) {
    super(scope, id);

    // DynamoDB table
    const table = new dynamodb.Table(this, 'UsersTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // Lambda function
    const getUserFn = new lambda.Function(this, 'GetUserFunction', {
      runtime: lambda.Runtime.PYTHON_3_11,
      handler: 'app.lambda_handler',
      code: lambda.Code.fromAsset('src'),
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    table.grantReadData(getUserFn);

    // API Gateway
    const api = new apigateway.RestApi(this, 'UserApi', {
      restApiName: 'User Service',
    });
    const users = api.root.addResource('users');
    const user = users.addResource('{id}');
    user.addMethod('GET', new apigateway.LambdaIntegration(getUserFn));
  }
}
```

### Example 5

```python
# Event structure
{
  "httpMethod": "GET",
  "path": "/users/123",
  "pathParameters": {"id": "123"},
  "queryStringParameters": {"filter": "active"},
  "headers": {"Authorization": "Bearer token"},
  "body": null,
  "requestContext": {
    "requestId": "abc-123",
    "identity": {"sourceIp": "1.2.3.4"}
  }
}

# Response format
{
  "statusCode": 200,
  "headers": {"Content-Type": "application/json"},
  "body": "{\"id\": \"123\", \"name\": \"John\"}"
}
```

### Example 6

```python
# Event structure (ObjectCreated)
{
  "Records": [{
    "eventName": "ObjectCreated:Put",
    "s3": {
      "bucket": {"name": "my-bucket"},
      "object": {
        "key": "uploads/file.csv",
        "size": 1024
      }
    }
  }]
}

# Handler
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Process file
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = obj['Body'].read().decode('utf-8')
        # Transform and store
```

### Example 7

```python
# Event structure
{
  "Records": [{
    "messageId": "msg-123",
    "receiptHandle": "handle-456",
    "body": "{\"order_id\": \"789\"}",
    "attributes": {
      "ApproximateReceiveCount": "1",
      "SentTimestamp": "1609459200000"
    }
  }]
}

# Batch processing (1-10 messages)
def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        process_order(body['order_id'])

    # Partial batch failures (SQS FIFO)
    return {
        "batchItemFailures": [
            {"itemIdentifier": record['messageId']}
        ]
    }
```

### Example 8

```python
# Cron expression: rate(5 minutes) or cron(0 12 * * ? *)
{
  "version": "0",
  "id": "event-123",
  "detail-type": "Scheduled Event",
  "source": "aws.events",
  "time": "2024-01-15T12:00:00Z",
  "detail": {}
}

# Custom event
{
  "detail-type": "Order Placed",
  "source": "ecommerce.orders",
  "detail": {
    "order_id": "789",
    "customer_id": "456"
  }
}
```

### Example 9

```python
# Event structure (INSERT, MODIFY, REMOVE)
{
  "Records": [{
    "eventName": "INSERT",
    "dynamodb": {
      "Keys": {"id": {"S": "123"}},
      "NewImage": {
        "id": {"S": "123"},
        "status": {"S": "active"}
      },
      "SequenceNumber": "111",
      "SizeBytes": 26
    }
  }]
}
```

### Example 10

```bash
# Keep N instances warm (eliminates cold starts)
aws lambda put-provisioned-concurrency-config \
  --function-name my-function \
  --provisioned-concurrent-executions 10

# Auto-scaling with target utilization
aws application-autoscaling register-scalable-target \
  --service-namespace lambda \
  --resource-id function:my-function:alias:prod \
  --scalable-dimension lambda:function:ProvisionedConcurrentExecutions \
  --min-capacity 5 \
  --max-capacity 50
```

### Example 11

```bash
# Before: 50 MB (node_modules with dev deps)
npm install --production  # Exclude devDependencies
npm prune --production

# Python: Use slim packages
pip install boto3-stubs  # Type hints only, not runtime
pip install aws-lambda-powertools  # Lightweight utilities

# Exclude unnecessary files in .zip
zip -r function.zip . -x "*.git*" "tests/*" "*.md"
```

### Example 12

```python
# Bad: Import everything upfront
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def lambda_handler(event, context):
    # Only uses pandas
    df = pd.DataFrame(event['data'])
    return df.to_json()

# Good: Import only when needed
def lambda_handler(event, context):
    import pandas as pd  # Lazy import
    df = pd.DataFrame(event['data'])
    return df.to_json()
```

### Example 13

```python
# Initialize outside handler (reused across invocations)
import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_NAME']
)

def lambda_handler(event, context):
    conn = pool.connection()  # Fast: reuses existing connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    conn.close()
    return results
```

### Example 15

```yaml
# Reduces Java cold starts by 90% (pre-initializes JVM)
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: java17
      SnapStart:
        ApplyOn: PublishedVersions
```

### Example 16

```python
# /tmp directory: 512 MB - 10 GB (configurable)
# Persists across warm invocations, deleted on cold start

def lambda_handler(event, context):
    cache_file = '/tmp/data.json'

    # Check cache
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    # Fetch and cache
    data = fetch_from_api()
    with open(cache_file, 'w') as f:
        json.dump(data, f)

    return data
```

### Example 17

```python
# Session state, user preferences, counters
table = boto3.resource('dynamodb').Table('sessions')

# Store state
table.put_item(Item={
    'session_id': 'abc-123',
    'user_id': '456',
    'cart': ['item1', 'item2'],
    'ttl': int(time.time()) + 3600  # Expire in 1 hour
})

# Retrieve state
response = table.get_item(Key={'session_id': 'abc-123'})
state = response.get('Item', {})
```

### Example 18

```python
# Store files, reports, ML models
s3 = boto3.client('s3')

# Save processed result
s3.put_object(
    Bucket='results-bucket',
    Key=f'reports/{report_id}.pdf',
    Body=pdf_bytes,
    ContentType='application/pdf'
)

# Generate presigned URL (temporary access)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'results-bucket', 'Key': f'reports/{report_id}.pdf'},
    ExpiresIn=3600
)
```

### Example 19

```python
# Redis/Memcached for high-throughput caching
import redis

# Initialize (VPC required)
redis_client = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=6379,
    decode_responses=True
)

def lambda_handler(event, context):
    user_id = event['user_id']

    # Check cache
    cached = redis_client.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)

    # Fetch from DB and cache
    user = fetch_user_from_db(user_id)
    redis_client.setex(f'user:{user_id}', 300, json.dumps(user))
    return user
```

### Example 20

```json
// Long-running workflows (up to 1 year)
{
  "Comment": "Order processing workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:validate",
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:payment",
      "Next": "ShipOrder",
      "Catch": [{
        "ErrorEquals": ["PaymentFailed"],
        "Next": "RefundOrder"
      }]
    }
  }
}
```

### Example 21

```python
import json
import logging
import os
from aws_lambda_powertools import Logger

# AWS Lambda Powertools logger
logger = Logger(service="user-service")

@logger.inject_lambda_context
def lambda_handler(event, context):
    # Structured logs (JSON) with correlation ID
    logger.info("Processing request", extra={
        "user_id": event.get('user_id'),
        "action": "get_profile"
    })

    try:
        result = process_request(event)
        logger.info("Request successful", extra={"result_size": len(result)})
        return result
    except Exception as e:
        logger.exception("Request failed", extra={"error": str(e)})
        raise
```

### Example 22

```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries (boto3, requests, etc.)
patch_all()

@xray_recorder.capture('process_order')
def process_order(order_id):
    # Custom subsegment
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation('order_id', order_id)
    subsegment.put_metadata('order_details', {'items': 3, 'total': 99.99})

    # Traced automatically
    dynamodb.get_item(Key={'id': order_id})
    requests.post('https://api.example.com/notify')

    return {'status': 'completed'}
```

### Example 23

```python
import boto3
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    # Business metric
    order_total = event['total']

    cloudwatch.put_metric_data(
        Namespace='ECommerce',
        MetricData=[
            {
                'MetricName': 'OrderValue',
                'Value': order_total,
                'Unit': 'None',
                'Dimensions': [
                    {'Name': 'Environment', 'Value': 'production'},
                    {'Name': 'Region', 'Value': 'us-east-1'}
                ]
            }
        ]
    )
```

### Example 24

```yaml
# SAM template
Resources:
  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${FunctionName}-errors'
      MetricName: Errors
      Namespace: AWS/Lambda
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 1
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: FunctionName
          Value: !Ref MyFunction
      AlarmActions:
        - !Ref SNSTopic
```

### Example 25

```yaml
# Least-privilege role (one per function)
Resources:
  FunctionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: DynamoDBAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                Resource: !GetAtt UsersTable.Arn
```

### Example 26

```python
import boto3
import os
import json

# AWS Secrets Manager
secrets_client = boto3.client('secretsmanager')

def get_secret(secret_name):
    response = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

def lambda_handler(event, context):
    # Retrieve DB credentials
    db_secret = get_secret(os.environ['DB_SECRET_ARN'])

    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user=db_secret['username'],
        password=db_secret['password'],
        database=db_secret['dbname']
    )
```

### Example 27

```yaml
# Access RDS/ElastiCache in private subnets
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      VpcConfig:
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
        SubnetIds:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
      # Add NAT Gateway for internet access

  LambdaSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Lambda function security group
      VpcId: !Ref VPC
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          DestinationSecurityGroupId: !Ref RDSSecurityGroup
```

### Example 28

```python
from jsonschema import validate, ValidationError

# Define schema
request_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["user_id", "email"]
}

def lambda_handler(event, context):
    try:
        # Validate input
        body = json.loads(event['body'])
        validate(instance=body, schema=request_schema)

        # Sanitize for SQL injection
        user_id = body['user_id'].replace("'", "''")

        # Process request
        return process_user(user_id)
    except ValidationError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input', 'details': str(e)})
        }
```

### Example 29

```python
# test_handler.py
import json
import pytest
from moto import mock_dynamodb
import boto3
from app import lambda_handler

@mock_dynamodb
def test_get_user_success():
    # Setup mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='users',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # Insert test data
    table.put_item(Item={'id': '123', 'name': 'John Doe'})

    # Mock event
    event = {
        'httpMethod': 'GET',
        'pathParameters': {'id': '123'}
    }

    # Invoke handler
    response = lambda_handler(event, None)

    # Assert
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['name'] == 'John Doe'

@mock_dynamodb
def test_get_user_not_found():
    event = {'pathParameters': {'id': '999'}}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
```

### Example 30

```python
# test_integration.py
import boto3
import requests
import os

# Requires deployed stack
API_URL = os.environ['API_URL']
lambda_client = boto3.client('lambda')

def test_api_gateway_integration():
    # Call real API
    response = requests.get(f'{API_URL}/users/123')
    assert response.status_code == 200
    assert response.json()['id'] == '123'

def test_lambda_invocation():
    # Direct Lambda invocation
    response = lambda_client.invoke(
        FunctionName='my-function',
        Payload=json.dumps({'user_id': '123'})
    )

    result = json.loads(response['Payload'].read())
    assert result['statusCode'] == 200
```

### Example 31

```bash
# Start local API Gateway + Lambda
sam local start-api --env-vars env.json

# Invoke function directly
sam local invoke GetUserFunction --event events/get-user.json

# Generate sample events
sam local generate-event s3 put > events/s3-put.json
sam local generate-event sqs receive-message > events/sqs.json

# Debug with breakpoints
sam local start-api --debug-port 5858
# Attach debugger (VS Code, PyCharm)
```

### Example 32

```bash
# Right-size memory (CPU scales linearly with memory)
# Use AWS Lambda Power Tuning tool
git clone https://github.com/alexcasalboni/aws-lambda-power-tuning
sam deploy --guided

# Run tuning
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:... \
  --input '{
    "lambdaARN": "arn:aws:lambda:...:function:my-function",
    "powerValues": [128, 256, 512, 1024, 2048],
    "num": 50,
    "payload": {}
  }'

# Results: Optimal memory for cost vs. performance
```

### Example 33

```yaml
# 20% cost reduction + 19% better performance
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.11
      Architectures:
        - arm64  # Change from x86_64
```

### Example 34

```bash
# Cost Explorer query (daily Lambda costs)
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity DAILY \
  --metrics BlendedCost \
  --filter file://lambda-filter.json

# lambda-filter.json
{
  "Dimensions": {
    "Key": "SERVICE",
    "Values": ["AWS Lambda"]
  }
}

# CloudWatch Insights: Top 10 expensive functions
fields @duration, @billedDuration, @memorySize
| filter @type = "REPORT"
| stats sum(@billedDuration) as totalDuration by @logStream
| sort totalDuration desc
| limit 10
```

### Example 35

```bash
# Delete unused function versions (keep latest + aliases)
aws lambda list-versions-by-function --function-name my-function \
  | jq -r '.Versions[] | select(.Version != "$LATEST") | .Version' \
  | tail -n +6 \
  | xargs -I {} aws lambda delete-function --function-name my-function:{}

# Tag functions for cost allocation
aws lambda tag-resource \
  --resource arn:aws:lambda:...:function:my-function \
  --tags Project=ecommerce,Environment=production
```

### Example 36

```python
// TODO: Add basic example for serverless
// This example demonstrates core functionality
```

---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
