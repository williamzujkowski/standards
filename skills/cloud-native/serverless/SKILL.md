---
name: serverless
category: cloud-native
difficulty: intermediate
tags: [aws-lambda, serverless, cloud-functions, faas, event-driven]
related: [kubernetes, microservices, monitoring]
version: 1.0.0
---

# Serverless Computing

## Level 1: Quick Reference

### Serverless Benefits and Tradeoffs

**Benefits:**
- **Zero Server Management**: No OS patching, scaling, or capacity planning
- **Automatic Scaling**: Scales from zero to thousands of concurrent executions
- **Pay-Per-Use**: Only charged for actual execution time (100ms granularity)
- **Built-in HA**: Multi-AZ deployment by default
- **Fast Time-to-Market**: Focus on code, not infrastructure

**Tradeoffs:**
- **Cold Starts**: 100ms-5s latency for new container initialization
- **Execution Limits**: 15 min max (Lambda), 60 min (Cloud Functions)
- **Vendor Lock-in**: Platform-specific APIs and deployment models
- **Debugging Complexity**: Distributed tracing across ephemeral environments
- **State Management**: Stateless by design, requires external persistence

### Common Serverless Patterns

**1. API Backend (HTTP Trigger)**
```
Client → API Gateway → Lambda → Database
- RESTful APIs, GraphQL endpoints
- Authentication/authorization at gateway
- Response caching, throttling, API keys
```

**2. Event-Driven Processing (Event Trigger)**
```
S3 Upload → Lambda → Process File → Store Result
SQS Queue → Lambda → Transform Data → Publish Event
DynamoDB Stream → Lambda → Aggregate Metrics
```

**3. Scheduled Tasks (Cron Trigger)**
```
EventBridge Rule (cron) → Lambda → Cleanup/Report/Backup
- Data aggregation (hourly, daily)
- Automated backups and archival
- Health checks and monitoring
```

**4. Stream Processing**
```
Kinesis/Kafka → Lambda → Real-time Analytics → Dashboard
- Log processing and filtering
- Clickstream analysis
- IoT data ingestion
```

### Essential Serverless Checklist

**Architecture:**
- [ ] Function size < 50 MB (Lambda), memory 128-10240 MB
- [ ] Single responsibility per function
- [ ] Async patterns for long-running tasks (SQS, Step Functions)
- [ ] Idempotent handlers (retry-safe)

**Cold Start Optimization:**
- [ ] Provisioned concurrency for latency-sensitive APIs
- [ ] Minimize dependencies (slim packages)
- [ ] Initialize SDK clients outside handler
- [ ] Use compiled languages (Go, Rust) for sub-100ms starts

**Timeouts and Concurrency:**
- [ ] Set appropriate timeout (default 3s, max 15min Lambda)
- [ ] Configure reserved/unreserved concurrency limits
- [ ] Use SQS for rate limiting and backpressure
- [ ] Monitor throttles and errors (CloudWatch alarms)

**Security:**
- [ ] Least-privilege IAM roles (one per function)
- [ ] Secrets in AWS Secrets Manager/Parameter Store
- [ ] VPC configuration for database access (increases cold start)
- [ ] Environment variable encryption (AWS KMS)

**Observability:**
- [ ] Structured logging (JSON) with correlation IDs
- [ ] X-Ray tracing for distributed requests
- [ ] Custom CloudWatch metrics (business KPIs)
- [ ] Alerting on error rates, duration, throttles

**Cost Optimization:**
- [ ] Right-size memory (CPU scales with memory)
- [ ] Use ARM (Graviton2) for 20% cost reduction
- [ ] Delete unused functions and versions
- [ ] Monitor invocation count and duration trends

---

## Level 2: Implementation Guide

### AWS Lambda Fundamentals

**Runtime Lifecycle:**
1. **INIT Phase** (cold start):
   - Download deployment package from S3
   - Start runtime (Python, Node.js, Java, Go, etc.)
   - Execute initialization code (outside handler)
   - Load dependencies and establish connections
   - Typical duration: 100ms-5s

2. **INVOKE Phase**:
   - Execute handler function
   - Process event payload
   - Return response or error
   - Billed duration: rounded up to nearest 1ms

3. **SHUTDOWN Phase**:
   - Runtime shutdown after inactivity (~10-15 min)
   - Connections closed, temp files deleted

**Lambda Handler Pattern:**
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

**Lambda Layers:**
- Shared code libraries across multiple functions
- Max 5 layers per function, 250 MB total (unzipped)
- Common use cases: SDKs, custom libraries, config files

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

**Deployment Packages:**
- **Zip Archive**: Up to 50 MB (direct upload), 250 MB (S3)
- **Container Image**: Up to 10 GB (ECR), cold start +1-2s

**Multi-Cloud Comparison:**

| Feature | AWS Lambda | Google Cloud Functions | Azure Functions |
|---------|-----------|----------------------|-----------------|
| **Max Duration** | 15 minutes | 60 minutes (2nd gen) | 10 minutes (Consumption) |
| **Memory** | 128 MB - 10 GB | 128 MB - 32 GB | 128 MB - 14 GB |
| **Cold Start** | 100-500ms (Python/Node) | 200-800ms | 150-600ms |
| **Concurrency** | 1000 default (soft limit) | 1000 per region | 200 per instance |
| **Pricing** | $0.20/1M requests + $0.0000166667/GB-s | $0.40/1M + $0.0000025/GB-s | $0.20/1M + $0.000016/GB-s |
| **Triggers** | 20+ (S3, DynamoDB, SQS, API Gateway) | 10+ (HTTP, Pub/Sub, Storage) | 15+ (HTTP, Queue, Blob) |

### Serverless Frameworks

**1. AWS SAM (Serverless Application Model):**
- CloudFormation extension for serverless resources
- Local testing with `sam local`
- Built-in CI/CD with CodePipeline integration

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

**2. Serverless Framework:**
- Multi-cloud support (AWS, Azure, GCP)
- Plugin ecosystem (offline, webpack, domain-manager)
- Environment-based deployments

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

**3. AWS CDK (Cloud Development Kit):**
- Infrastructure as code in Python/TypeScript/Java
- Higher-level constructs (L2/L3)
- Type safety and IDE autocomplete

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

### Event Sources and Triggers

**1. API Gateway (HTTP/REST):**
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

**2. S3 Events:**
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

**3. SQS (Queue):**
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

**4. EventBridge (Scheduled/Custom):**
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

**5. DynamoDB Streams:**
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


### Cold Start Optimization

**Understanding Cold Starts:**
- **Triggered by**: First invocation, scaling up, runtime updates
- **Components**: Download code → Start runtime → Init code → Invoke handler
- **Impact**: P99 latency spikes, user-facing API degradation

**Optimization Techniques:**

**1. Provisioned Concurrency:**
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

**2. Minimize Package Size:**
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

**3. Lazy Loading:**
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

**4. Connection Pooling:**
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

**5. Choose Fast Runtimes:**
```
Cold Start Benchmarks (512 MB):
- Go: 100-150ms
- Rust: 120-180ms
- Python 3.11: 200-300ms
- Node.js 20: 250-350ms
- Java 17: 1-2s (use Snapstart for sub-200ms)
- .NET 7: 500-800ms
```

**6. Lambda SnapStart (Java):**
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

### State Management

**Ephemeral Storage (Local):**
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

**DynamoDB (Key-Value):**
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

**S3 (Large Objects):**
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

**ElastiCache (Distributed Cache):**
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

**Step Functions (Workflow State):**
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

### Observability and Monitoring

**Structured Logging:**
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

**X-Ray Tracing:**
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

**Custom CloudWatch Metrics:**
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

**CloudWatch Alarms:**
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


### Security Best Practices

**IAM Roles and Permissions:**
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

**Secrets Management:**
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

**VPC Configuration:**
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

**Input Validation:**
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

### Testing Strategies

**Unit Tests:**
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

**Integration Tests:**
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

**Local Testing (SAM CLI):**
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

### Cost Optimization

**Memory Sizing:**
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

**ARM (Graviton2) Migration:**
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

**Monitoring Costs:**
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

**Cleanup and Governance:**
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

---

## Level 3: Deep Dive Resources

### Official Documentation
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Google Cloud Functions](https://cloud.google.com/functions/docs)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Serverless Framework](https://www.serverless.com/framework/docs)
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)

### Books and Courses
- **"Serverless Architectures on AWS"** by Peter Sbarski
- **"Production-Ready Serverless"** by Yan Cui
- **AWS Certified Solutions Architect** (includes serverless)
- **A Cloud Guru: AWS Lambda & Serverless**

### Tools and Libraries
- **AWS Lambda Powertools** (Python, TypeScript, Java)
- **Serverless Framework Plugins** (offline, webpack, prune)
- **Lumigo** (Observability and debugging)
- **Thundra** (APM for serverless)
- **AWS X-Ray** (Distributed tracing)

### Community Resources
- [Serverless Stack (SST)](https://sst.dev/)
- [Off-by-none Newsletter](https://offbynone.io/)
- [ServerlessLand Patterns](https://serverlessland.com/patterns)
- [AWS Samples GitHub](https://github.com/aws-samples)

### Bundled Resources
- `templates/lambda-function.py` - Production Lambda template
- `templates/sam-template.yaml` - SAM infrastructure template
- `templates/serverless.yml` - Serverless Framework config
- `templates/api-gateway.yaml` - API Gateway REST API
- `scripts/deploy-lambda.sh` - Automated deployment script
- `resources/serverless-patterns.md` - Common architecture patterns
