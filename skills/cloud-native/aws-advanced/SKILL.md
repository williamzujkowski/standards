---
name: aws-advanced-patterns
category: cloud-native
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
  - serverless
  - cloud-concepts
  - aws-fundamentals
tags:
  - aws
  - step-functions
  - eventbridge
  - lambda-layers
  - dynamodb
  - observability
version: 1.0.0
---

# AWS Advanced Patterns

Master advanced AWS serverless architectures, event-driven patterns, and enterprise-grade cloud solutions.

## Level 1: Quick Reference

### AWS Advanced Services Overview

**Orchestration & Events:**
- **Step Functions**: State machine orchestration for complex workflows
- **EventBridge**: Serverless event bus for event-driven architectures
- **Lambda Layers**: Shared code and dependencies across functions

**Data & Storage:**
- **DynamoDB Advanced**: Single-table design, streams, global tables
- **S3 Advanced**: Event notifications, object lifecycle, intelligent tiering

**Integration:**
- **API Gateway Advanced**: Custom authorizers, usage plans, WebSocket APIs
- **SQS/SNS Patterns**: FIFO queues, DLQ, fan-out, message filtering

**Observability:**
- **CloudWatch**: Custom metrics, composite alarms, insights
- **X-Ray**: Distributed tracing, service maps, annotations

### Common Patterns Quick Reference

```yaml
# Event-Driven Architecture
Pattern: Publisher → EventBridge → Subscribers
Use Case: Microservices decoupling, cross-account events
Key Services: EventBridge, Lambda, SQS

# Orchestrated Workflow
Pattern: API → Step Functions → Lambda/Services
Use Case: Multi-step processes, saga pattern, ETL
Key Services: Step Functions, Lambda, DynamoDB

# Fan-Out Processing
Pattern: SNS Topic → Multiple SQS Queues → Lambda
Use Case: Parallel processing, multi-tenant systems
Key Services: SNS, SQS, Lambda

# CQRS Pattern
Pattern: Write DB → DynamoDB Streams → Read DB
Use Case: Read/write separation, materialized views
Key Services: DynamoDB Streams, Lambda, ElastiCache

# Saga Pattern
Pattern: Step Functions → Compensating Transactions
Use Case: Distributed transactions, rollback logic
Key Services: Step Functions, Lambda, DynamoDB
```

### Essential Checklist

**Security:**
- [ ] IAM least privilege policies (resource-level permissions)
- [ ] Secrets Manager for credentials (automatic rotation)
- [ ] VPC endpoints for private connectivity
- [ ] Encryption at rest and in transit
- [ ] WAF rules for API Gateway

**Cost Optimization:**
- [ ] Lambda reserved concurrency for predictable workloads
- [ ] DynamoDB on-demand vs provisioned capacity
- [ ] S3 Intelligent-Tiering for variable access patterns
- [ ] CloudWatch Logs retention policies
- [ ] Cost allocation tags for all resources

**Reliability:**
- [ ] Multi-AZ deployments
- [ ] Dead-letter queues (DLQ) for failed messages
- [ ] Circuit breakers in Step Functions
- [ ] Exponential backoff with jitter
- [ ] Chaos engineering tests

**Observability:**
- [ ] X-Ray tracing enabled on all Lambda functions
- [ ] Custom CloudWatch metrics for business KPIs
- [ ] Structured logging (JSON format)
- [ ] Distributed tracing correlation IDs
- [ ] Alarms for error rates and latency

---

## Level 2: Implementation Guide

### AWS Step Functions: State Machine Orchestration

Step Functions provides serverless orchestration for complex workflows with built-in error handling, retries, and parallel execution.

#### State Machine Patterns

**Sequential Workflow:**
```json
{
  "Comment": "Order Processing Workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ValidateOrder",
      "Next": "ProcessPayment",
      "Catch": [{
        "ErrorEquals": ["ValidationError"],
        "ResultPath": "$.error",
        "Next": "NotifyValidationFailure"
      }],
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2.0
      }]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "ProcessPayment",
        "Payload": {
          "orderId.$": "$.orderId",
          "amount.$": "$.amount"
        }
      },
      "ResultPath": "$.paymentResult",
      "Next": "UpdateInventory"
    },
    "UpdateInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:UpdateInventory",
      "End": true
    },
    "NotifyValidationFailure": {
      "Type": "Task",
      "Resource": "arn:aws:sns:us-east-1:123456789012:ValidationFailures",
      "End": true
    }
  }
}
```

**Parallel Execution:**
```json
{
  "Comment": "Parallel Data Processing",
  "StartAt": "ParallelProcessing",
  "States": {
    "ParallelProcessing": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "ProcessImageResize",
          "States": {
            "ProcessImageResize": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ResizeImage",
              "End": true
            }
          }
        },
        {
          "StartAt": "ExtractMetadata",
          "States": {
            "ExtractMetadata": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ExtractMetadata",
              "End": true
            }
          }
        },
        {
          "StartAt": "VirusScan",
          "States": {
            "VirusScan": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789012:function:VirusScan",
              "End": true
            }
          }
        }
      ],
      "Next": "AggregateResults",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "ResultPath": "$.error",
        "Next": "HandleFailure"
      }]
    },
    "AggregateResults": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:AggregateResults",
      "End": true
    },
    "HandleFailure": {
      "Type": "Fail",
      "Cause": "Parallel processing failed"
    }
  }
}
```

**Map State (Dynamic Parallelism):**
```json
{
  "Comment": "Process batch of items",
  "StartAt": "ProcessBatch",
  "States": {
    "ProcessBatch": {
      "Type": "Map",
      "ItemsPath": "$.items",
      "MaxConcurrency": 10,
      "Iterator": {
        "StartAt": "ProcessItem",
        "States": {
          "ProcessItem": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ProcessItem",
            "Retry": [{
              "ErrorEquals": ["States.TaskFailed"],
              "IntervalSeconds": 1,
              "MaxAttempts": 2,
              "BackoffRate": 2.0
            }],
            "End": true
          }
        }
      },
      "ResultPath": "$.results",
      "Next": "GenerateReport"
    },
    "GenerateReport": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:GenerateReport",
      "End": true
    }
  }
}
```

**Saga Pattern (Compensating Transactions):**
```json
{
  "Comment": "Distributed transaction with rollback",
  "StartAt": "ReserveInventory",
  "States": {
    "ReserveInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ReserveInventory",
      "ResultPath": "$.reservation",
      "Next": "ChargeCustomer",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "ResultPath": "$.error",
        "Next": "TransactionFailed"
      }]
    },
    "ChargeCustomer": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ChargeCustomer",
      "ResultPath": "$.charge",
      "Next": "SendConfirmation",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "ResultPath": "$.error",
        "Next": "ReleaseInventory"
      }]
    },
    "SendConfirmation": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:SendConfirmation",
      "End": true,
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "ResultPath": "$.error",
        "Next": "RefundCustomer"
      }]
    },
    "ReleaseInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ReleaseInventory",
      "Next": "TransactionFailed"
    },
    "RefundCustomer": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:RefundCustomer",
      "Next": "ReleaseInventory"
    },
    "TransactionFailed": {
      "Type": "Fail",
      "Cause": "Transaction failed and compensated"
    }
  }
}
```

**Step Functions SDK Integration (AWS SDK v3):**
```javascript
// Node.js - AWS SDK v3
import { SFNClient, StartExecutionCommand } from '@aws-sdk/client-sfn';

const client = new SFNClient({ region: 'us-east-1' });

async function startWorkflow(orderId, orderData) {
  const command = new StartExecutionCommand({
    stateMachineArn: process.env.STATE_MACHINE_ARN,
    name: `order-${orderId}-${Date.now()}`,
    input: JSON.stringify({
      orderId,
      ...orderData,
      timestamp: new Date().toISOString()
    })
  });

  try {
    const response = await client.send(command);
    console.log('Execution started:', response.executionArn);
    return response;
  } catch (error) {
    console.error('Failed to start execution:', error);
    throw error;
  }
}
```

```python
# Python - Boto3
import boto3
import json
from datetime import datetime

sfn_client = boto3.client('stepfunctions', region_name='us-east-1')

def start_workflow(order_id: str, order_data: dict):
    """Start Step Functions workflow execution"""
    execution_input = {
        'orderId': order_id,
        **order_data,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    try:
        response = sfn_client.start_execution(
            stateMachineArn=os.environ['STATE_MACHINE_ARN'],
            name=f'order-{order_id}-{int(datetime.now().timestamp())}',
            input=json.dumps(execution_input)
        )
        print(f"Execution started: {response['executionArn']}")
        return response
    except Exception as e:
        print(f"Failed to start execution: {str(e)}")
        raise
```

### EventBridge: Event-Driven Architecture

EventBridge enables building scalable, loosely-coupled event-driven systems with built-in schema registry and cross-account support.

#### Event Patterns

**Basic Event Pattern:**
```json
{
  "source": ["myapp.orders"],
  "detail-type": ["OrderPlaced"],
  "detail": {
    "status": ["pending"],
    "amount": [{ "numeric": [">", 100] }]
  }
}
```

**Advanced Pattern Matching:**
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running", "stopped"],
    "instance-type": [{ "prefix": "t3." }]
  }
}
```

**Content-Based Filtering:**
```json
{
  "source": ["myapp.users"],
  "detail-type": ["UserRegistered"],
  "detail": {
    "userType": ["premium"],
    "region": ["us-east-1", "us-west-2"],
    "$or": [
      { "age": [{ "numeric": [">=", 18] }] },
      { "verified": [true] }
    ]
  }
}
```

**EventBridge Publisher (AWS SDK v3):**
```javascript
// Node.js - AWS SDK v3
import { EventBridgeClient, PutEventsCommand } from '@aws-sdk/client-eventbridge';

const client = new EventBridgeClient({ region: 'us-east-1' });

async function publishEvent(eventType, detailData) {
  const event = {
    Time: new Date(),
    Source: 'myapp.orders',
    DetailType: eventType,
    Detail: JSON.stringify(detailData),
    EventBusName: 'default'
  };

  const command = new PutEventsCommand({
    Entries: [event]
  });

  try {
    const response = await client.send(command);
    if (response.FailedEntryCount > 0) {
      console.error('Failed entries:', response.Entries);
      throw new Error('Event publication failed');
    }
    return response;
  } catch (error) {
    console.error('EventBridge error:', error);
    throw error;
  }
}

// Usage
await publishEvent('OrderPlaced', {
  orderId: '12345',
  customerId: 'cust-789',
  amount: 150.00,
  status: 'pending'
});
```

```python
# Python - Boto3
import boto3
import json
from datetime import datetime
from typing import Dict, Any

eventbridge = boto3.client('events', region_name='us-east-1')

def publish_event(event_type: str, detail_data: Dict[str, Any]):
    """Publish event to EventBridge"""
    event = {
        'Time': datetime.utcnow(),
        'Source': 'myapp.orders',
        'DetailType': event_type,
        'Detail': json.dumps(detail_data),
        'EventBusName': 'default'
    }
    
    try:
        response = eventbridge.put_events(Entries=[event])
        if response['FailedEntryCount'] > 0:
            print(f"Failed entries: {response['Entries']}")
            raise Exception('Event publication failed')
        return response
    except Exception as e:
        print(f"EventBridge error: {str(e)}")
        raise

# Usage
publish_event('OrderPlaced', {
    'orderId': '12345',
    'customerId': 'cust-789',
    'amount': 150.00,
    'status': 'pending'
})
```

**EventBridge Schema Registry:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OrderPlaced",
  "type": "object",
  "properties": {
    "orderId": {
      "type": "string",
      "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    },
    "customerId": {
      "type": "string"
    },
    "amount": {
      "type": "number",
      "minimum": 0
    },
    "status": {
      "type": "string",
      "enum": ["pending", "confirmed", "shipped", "delivered"]
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "productId": { "type": "string" },
          "quantity": { "type": "integer", "minimum": 1 },
          "price": { "type": "number", "minimum": 0 }
        },
        "required": ["productId", "quantity", "price"]
      }
    }
  },
  "required": ["orderId", "customerId", "amount", "status"]
}
```

### Lambda Layers: Shared Dependencies

Lambda Layers enable sharing code, libraries, and custom runtimes across multiple functions, reducing deployment package size and promoting code reuse.

#### Creating Lambda Layers

**Python Layer Structure:**
```
python-layer/
├── python/
│   ├── lib/
│   │   └── python3.11/
│   │       └── site-packages/
│   │           ├── requests/
│   │           ├── boto3/
│   │           └── custom_utils.py
│   └── requirements.txt
└── build.sh
```

**Python Layer Build Script:**
```bash
#!/bin/bash
# build.sh

# Install dependencies
pip install -r requirements.txt -t python/lib/python3.11/site-packages/

# Create deployment package
zip -r layer.zip python/

# Publish layer
aws lambda publish-layer-version \
  --layer-name shared-dependencies \
  --description "Common Python dependencies" \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11 \
  --compatible-architectures x86_64 arm64
```

**Node.js Layer Structure:**
```
nodejs-layer/
├── nodejs/
│   ├── node_modules/
│   │   ├── aws-xray-sdk-core/
│   │   ├── @aws-sdk/
│   │   └── lodash/
│   ├── lib/
│   │   └── utils.js
│   └── package.json
└── build.sh
```

**Node.js Layer Build Script:**
```bash
#!/bin/bash
# build.sh

cd nodejs
npm install --production
cd ..

# Create deployment package
zip -r layer.zip nodejs/

# Publish layer
aws lambda publish-layer-version \
  --layer-name nodejs-dependencies \
  --description "Common Node.js dependencies" \
  --zip-file fileb://layer.zip \
  --compatible-runtimes nodejs20.x \
  --compatible-architectures x86_64 arm64
```

**Using Layers in Lambda Function:**
```javascript
// Lambda function using layer dependencies
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';
// Custom utility from layer
import { formatResponse, validateInput } from '/opt/nodejs/lib/utils';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  try {
    const data = JSON.parse(event.body);
    
    // Use layer utility
    const validation = validateInput(data);
    if (!validation.valid) {
      return formatResponse(400, { error: validation.message });
    }

    await docClient.send(new PutCommand({
      TableName: process.env.TABLE_NAME,
      Item: data
    }));

    return formatResponse(200, { message: 'Success' });
  } catch (error) {
    return formatResponse(500, { error: error.message });
  }
};
```

**Custom Runtime Layer:**
```python
# bootstrap file for custom runtime
#!/opt/bin/python3.11

import sys
import os
import json

# Add layer libraries to path
sys.path.insert(0, '/opt/python/lib/python3.11/site-packages')

# Import AWS Lambda runtime interface client
import awslambdaric

# Import handler
from function import handler

# Start the runtime interface client
if __name__ == '__main__':
    awslambdaric.run(handler)
```

### API Gateway Advanced Patterns

#### Custom Authorizers (Lambda Authorizers)

**JWT Token Authorizer:**
```javascript
// custom-authorizer.js - AWS SDK v3
import { verify } from 'jsonwebtoken';

export const handler = async (event) => {
  const token = event.authorizationToken.replace('Bearer ', '');
  
  try {
    const decoded = verify(token, process.env.JWT_SECRET);
    
    // Generate IAM policy
    const policy = generatePolicy(decoded.sub, 'Allow', event.methodArn, {
      userId: decoded.sub,
      email: decoded.email,
      roles: decoded.roles
    });
    
    return policy;
  } catch (error) {
    console.error('Authorization failed:', error);
    throw new Error('Unauthorized');
  }
};

function generatePolicy(principalId, effect, resource, context = {}) {
  return {
    principalId,
    policyDocument: {
      Version: '2012-10-17',
      Statement: [{
        Action: 'execute-api:Invoke',
        Effect: effect,
        Resource: resource
      }]
    },
    context // Available as $context.authorizer.* in integration
  };
}
```

**Request-Based Authorizer:**
```javascript
export const handler = async (event) => {
  const apiKey = event.headers['x-api-key'];
  const sourceIp = event.requestContext.identity.sourceIp;
  
  // Validate API key and IP whitelist
  const isValid = await validateApiKey(apiKey, sourceIp);
  
  if (!isValid) {
    throw new Error('Unauthorized');
  }
  
  return {
    isAuthorized: true,
    context: {
      apiKeyId: apiKey,
      sourceIp: sourceIp
    }
  };
};

async function validateApiKey(apiKey, sourceIp) {
  // Check DynamoDB for valid API key and IP whitelist
  const { DynamoDBClient } = await import('@aws-sdk/client-dynamodb');
  const { DynamoDBDocumentClient, GetCommand } = await import('@aws-sdk/lib-dynamodb');
  
  const client = new DynamoDBClient({});
  const docClient = DynamoDBDocumentClient.from(client);
  
  const result = await docClient.send(new GetCommand({
    TableName: process.env.API_KEYS_TABLE,
    Key: { apiKey }
  }));
  
  if (!result.Item || !result.Item.active) {
    return false;
  }
  
  // Check IP whitelist
  const allowedIps = result.Item.allowedIps || [];
  return allowedIps.length === 0 || allowedIps.includes(sourceIp);
}
```

#### Usage Plans and API Keys

**CloudFormation Template:**
```yaml
ApiUsagePlan:
  Type: AWS::ApiGateway::UsagePlan
  Properties:
    UsagePlanName: StandardPlan
    Description: Standard API usage plan
    Throttle:
      BurstLimit: 100
      RateLimit: 50
    Quota:
      Limit: 10000
      Period: MONTH
    ApiStages:
      - ApiId: !Ref RestApi
        Stage: !Ref Stage

ApiKey:
  Type: AWS::ApiGateway::ApiKey
  Properties:
    Name: CustomerApiKey
    Description: API key for customer access
    Enabled: true

UsagePlanKey:
  Type: AWS::ApiGateway::UsagePlanKey
  Properties:
    KeyId: !Ref ApiKey
    KeyType: API_KEY
    UsagePlanId: !Ref ApiUsagePlan
```

#### Request/Response Transformations

**VTL Mapping Template (Request):**
```vtl
## Transform incoming request
#set($inputRoot = $input.path('$'))
{
  "body": {
    "userId": "$context.authorizer.userId",
    "requestId": "$context.requestId",
    "data": $input.json('$.data'),
    "timestamp": "$context.requestTime"
  },
  "metadata": {
    "sourceIp": "$context.identity.sourceIp",
    "userAgent": "$context.identity.userAgent"
  }
}
```

**VTL Mapping Template (Response):**
```vtl
## Transform response
#set($inputRoot = $input.path('$'))
{
  "statusCode": 200,
  "body": {
    "data": $input.json('$.result'),
    "requestId": "$context.requestId",
    "timestamp": "$context.requestTime"
  },
  "headers": {
    "X-Request-Id": "$context.requestId",
    "X-RateLimit-Remaining": "$context.authorizer.rateLimit"
  }
}
```

### DynamoDB Advanced Patterns

#### Single-Table Design

**Table Structure:**
```
PK                          SK                      GSI1PK              GSI1SK              Data
USER#123                    PROFILE                 EMAIL#john@ex.com   USER#123            {name, email, ...}
USER#123                    ORDER#456               USER#123            ORDER#2024-01-15    {orderId, amount, ...}
USER#123                    ORDER#789               USER#123            ORDER#2024-01-20    {orderId, amount, ...}
ORDER#456                   METADATA                STATUS#pending      ORDER#456           {status, created, ...}
ORDER#456                   ITEM#1                  PRODUCT#abc         ORDER#456           {productId, qty, ...}
ORDER#456                   ITEM#2                  PRODUCT#def         ORDER#456           {productId, qty, ...}
PRODUCT#abc                 DETAILS                 CATEGORY#electronics PRODUCT#abc        {name, price, ...}
```

**Access Patterns:**
```javascript
// AWS SDK v3
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, QueryCommand, GetCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

// 1. Get user profile
async function getUserProfile(userId) {
  const result = await docClient.send(new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: {
      PK: `USER#${userId}`,
      SK: 'PROFILE'
    }
  }));
  return result.Item;
}

// 2. Get all orders for user
async function getUserOrders(userId) {
  const result = await docClient.send(new QueryCommand({
    TableName: process.env.TABLE_NAME,
    KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
    ExpressionAttributeValues: {
      ':pk': `USER#${userId}`,
      ':sk': 'ORDER#'
    }
  }));
  return result.Items;
}

// 3. Get orders by status (using GSI)
async function getOrdersByStatus(status) {
  const result = await docClient.send(new QueryCommand({
    TableName: process.env.TABLE_NAME,
    IndexName: 'GSI1',
    KeyConditionExpression: 'GSI1PK = :status',
    ExpressionAttributeValues: {
      ':status': `STATUS#${status}`
    }
  }));
  return result.Items;
}

// 4. Get user by email (using GSI)
async function getUserByEmail(email) {
  const result = await docClient.send(new QueryCommand({
    TableName: process.env.TABLE_NAME,
    IndexName: 'GSI1',
    KeyConditionExpression: 'GSI1PK = :email',
    ExpressionAttributeValues: {
      ':email': `EMAIL#${email}`
    },
    Limit: 1
  }));
  return result.Items[0];
}

// 5. Get order with items (batch get)
async function getOrderWithItems(orderId) {
  const result = await docClient.send(new QueryCommand({
    TableName: process.env.TABLE_NAME,
    KeyConditionExpression: 'PK = :pk',
    ExpressionAttributeValues: {
      ':pk': `ORDER#${orderId}`
    }
  }));
  
  const metadata = result.Items.find(item => item.SK === 'METADATA');
  const items = result.Items.filter(item => item.SK.startsWith('ITEM#'));
  
  return { metadata, items };
}
```

#### DynamoDB Streams and Change Data Capture

**Stream Processor:**
```javascript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const handler = async (event) => {
  for (const record of event.Records) {
    const { eventName, dynamodb } = record;
    
    if (eventName === 'INSERT' || eventName === 'MODIFY') {
      const newImage = unmarshall(dynamodb.NewImage);
      
      // Process different entity types
      if (newImage.PK.startsWith('ORDER#')) {
        await processOrderChange(newImage, eventName);
      } else if (newImage.PK.startsWith('USER#')) {
        await processUserChange(newImage, eventName);
      }
    } else if (eventName === 'REMOVE') {
      const oldImage = unmarshall(dynamodb.OldImage);
      await processDelete(oldImage);
    }
  }
};

async function processOrderChange(order, eventName) {
  // Update materialized view, send notifications, etc.
  if (order.SK === 'METADATA' && order.status === 'completed') {
    await sendOrderCompletionEmail(order);
    await updateAnalytics(order);
  }
}
```

#### DynamoDB Transactions

**Transaction Example:**
```javascript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, TransactWriteCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

async function transferFunds(fromUserId, toUserId, amount) {
  const command = new TransactWriteCommand({
    TransactItems: [
      {
        Update: {
          TableName: process.env.TABLE_NAME,
          Key: { PK: `USER#${fromUserId}`, SK: 'BALANCE' },
          UpdateExpression: 'SET balance = balance - :amount',
          ConditionExpression: 'balance >= :amount',
          ExpressionAttributeValues: {
            ':amount': amount
          }
        }
      },
      {
        Update: {
          TableName: process.env.TABLE_NAME,
          Key: { PK: `USER#${toUserId}`, SK: 'BALANCE' },
          UpdateExpression: 'SET balance = balance + :amount',
          ExpressionAttributeValues: {
            ':amount': amount
          }
        }
      },
      {
        Put: {
          TableName: process.env.TABLE_NAME,
          Item: {
            PK: `TRANSACTION#${Date.now()}`,
            SK: 'METADATA',
            from: fromUserId,
            to: toUserId,
            amount: amount,
            timestamp: new Date().toISOString()
          }
        }
      }
    ]
  });

  try {
    await docClient.send(command);
    return { success: true };
  } catch (error) {
    if (error.name === 'TransactionCanceledException') {
      console.error('Transaction cancelled:', error.CancellationReasons);
    }
    throw error;
  }
}
```

### SQS/SNS Messaging Patterns

#### FIFO Queue with Deduplication

**Queue Configuration:**
```javascript
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';

const client = new SQSClient({ region: 'us-east-1' });

async function sendMessage(orderId, orderData) {
  const command = new SendMessageCommand({
    QueueUrl: process.env.QUEUE_URL,
    MessageBody: JSON.stringify(orderData),
    MessageGroupId: `order-${orderId}`, // Ensures FIFO within group
    MessageDeduplicationId: `${orderId}-${Date.now()}`, // Prevents duplicates
    MessageAttributes: {
      OrderType: {
        DataType: 'String',
        StringValue: orderData.type
      },
      Priority: {
        DataType: 'Number',
        StringValue: String(orderData.priority)
      }
    }
  });

  try {
    const response = await client.send(command);
    console.log('Message sent:', response.MessageId);
    return response;
  } catch (error) {
    console.error('Failed to send message:', error);
    throw error;
  }
}
```

#### Fan-Out Pattern (SNS → Multiple SQS)

**CloudFormation Setup:**
```yaml
OrderTopic:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: OrderEvents
    DisplayName: Order Events Topic

InventoryQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: InventoryQueue
    VisibilityTimeout: 300
    RedrivePolicy:
      deadLetterTargetArn: !GetAtt InventoryDLQ.Arn
      maxReceiveCount: 3

NotificationQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: NotificationQueue

AnalyticsQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: AnalyticsQueue

# Subscribe queues to topic
InventorySubscription:
  Type: AWS::SNS::Subscription
  Properties:
    Protocol: sqs
    TopicArn: !Ref OrderTopic
    Endpoint: !GetAtt InventoryQueue.Arn
    FilterPolicy:
      eventType:
        - order_placed
        - order_cancelled

NotificationSubscription:
  Type: AWS::SNS::Subscription
  Properties:
    Protocol: sqs
    TopicArn: !Ref OrderTopic
    Endpoint: !GetAtt NotificationQueue.Arn
```

**SNS Publisher:**
```python
import boto3
import json

sns_client = boto3.client('sns', region_name='us-east-1')

def publish_order_event(event_type: str, order_data: dict):
    """Publish order event to SNS topic (fan-out to multiple queues)"""
    message = {
        'eventType': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'data': order_data
    }
    
    response = sns_client.publish(
        TopicArn=os.environ['ORDER_TOPIC_ARN'],
        Message=json.dumps(message),
        MessageAttributes={
            'eventType': {
                'DataType': 'String',
                'StringValue': event_type
            },
            'orderId': {
                'DataType': 'String',
                'StringValue': order_data['orderId']
            }
        }
    )
    
    return response['MessageId']
```

#### Dead-Letter Queue Pattern

**SQS Consumer with DLQ:**
```javascript
import { SQSClient, ReceiveMessageCommand, DeleteMessageCommand } from '@aws-sdk/client-sqs';

const client = new SQSClient({ region: 'us-east-1' });

export const handler = async (event) => {
  for (const record of event.Records) {
    try {
      const message = JSON.parse(record.body);
      
      // Process message
      await processMessage(message);
      
      // Delete from queue on success
      await client.send(new DeleteMessageCommand({
        QueueUrl: process.env.QUEUE_URL,
        ReceiptHandle: record.receiptHandle
      }));
      
    } catch (error) {
      console.error('Processing failed:', error);
      // Message will return to queue and eventually move to DLQ
      // after maxReceiveCount attempts
      throw error;
    }
  }
};

async function processMessage(message) {
  // Implement idempotent processing
  const alreadyProcessed = await checkProcessingStatus(message.id);
  if (alreadyProcessed) {
    console.log('Message already processed:', message.id);
    return;
  }
  
  // Process business logic
  await performBusinessLogic(message);
  
  // Mark as processed
  await recordProcessingComplete(message.id);
}
```

### Cost Optimization Strategies

#### Lambda Optimization

**Right-Sizing Memory:**
```javascript
// Use AWS Lambda Power Tuning to find optimal memory
// https://github.com/alexcasalboni/aws-lambda-power-tuning

// Example: 512MB might be more cost-effective than 128MB
// due to faster execution time
const OPTIMAL_MEMORY = 512; // MB

// Use ARM64 (Graviton2) for 20% cost reduction
// Architecture: arm64 in CloudFormation/SAM
```

**Reserved Concurrency for Predictable Workloads:**
```yaml
ProcessOrderFunction:
  Type: AWS::Lambda::Function
  Properties:
    ReservedConcurrentExecutions: 10 # Prevent throttling
    MemorySize: 512
    Timeout: 30
```

#### DynamoDB Cost Optimization

**On-Demand vs Provisioned:**
```python
# Analyze usage patterns to choose capacity mode
def analyze_dynamodb_usage():
    """Determine if on-demand or provisioned is more cost-effective"""
    cloudwatch = boto3.client('cloudwatch')
    
    # Get read/write capacity units consumed
    read_metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedReadCapacityUnits',
        Dimensions=[{'Name': 'TableName', 'Value': 'OrdersTable'}],
        StartTime=datetime.now() - timedelta(days=30),
        EndTime=datetime.now(),
        Period=3600,
        Statistics=['Sum']
    )
    
    # Calculate costs
    # On-Demand: $1.25 per million reads, $6.25 per million writes
    # Provisioned: $0.00065 per RCU-hour, $0.00325 per WCU-hour
    
    # Switch to provisioned if usage is predictable and constant
```

**DynamoDB Auto Scaling:**
```yaml
ReadCapacityScalableTarget:
  Type: AWS::ApplicationAutoScaling::ScalableTarget
  Properties:
    MaxCapacity: 100
    MinCapacity: 5
    ResourceId: !Sub table/${OrdersTable}
    RoleARN: !GetAtt ScalingRole.Arn
    ScalableDimension: dynamodb:table:ReadCapacityUnits
    ServiceNamespace: dynamodb

ReadScalingPolicy:
  Type: AWS::ApplicationAutoScaling::ScalingPolicy
  Properties:
    PolicyName: ReadAutoScalingPolicy
    PolicyType: TargetTrackingScaling
    ScalingTargetId: !Ref ReadCapacityScalableTarget
    TargetTrackingScalingPolicyConfiguration:
      TargetValue: 70.0
      PredefinedMetricSpecification:
        PredefinedMetricType: DynamoDBReadCapacityUtilization
```

#### S3 Cost Optimization

**Intelligent-Tiering and Lifecycle Policies:**
```yaml
OrdersBucket:
  Type: AWS::S3::Bucket
  Properties:
    IntelligentTieringConfigurations:
      - Id: EntireBucket
        Status: Enabled
        Tierings:
          - AccessTier: ARCHIVE_ACCESS
            Days: 90
          - AccessTier: DEEP_ARCHIVE_ACCESS
            Days: 180
    LifecycleConfiguration:
      Rules:
        - Id: DeleteOldLogs
          Status: Enabled
          Prefix: logs/
          ExpirationInDays: 90
        - Id: TransitionToGlacier
          Status: Enabled
          Prefix: archives/
          Transitions:
            - TransitionInDays: 30
              StorageClass: GLACIER
```

### Observability and Monitoring

#### X-Ray Distributed Tracing

**Lambda Function with X-Ray:**
```javascript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';
import AWSXRay from 'aws-xray-sdk-core';

// Instrument AWS SDK
const client = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  // Create subsegment for custom operations
  const segment = AWSXRay.getSegment();
  const subsegment = segment.addNewSubsegment('processOrder');
  
  try {
    // Add annotations (indexed for filtering)
    subsegment.addAnnotation('orderId', event.orderId);
    subsegment.addAnnotation('customerId', event.customerId);
    
    // Add metadata (not indexed, but visible in traces)
    subsegment.addMetadata('orderDetails', event);
    
    const order = await getOrder(event.orderId);
    const processed = await processOrder(order);
    
    subsegment.close();
    return processed;
  } catch (error) {
    subsegment.addError(error);
    subsegment.close();
    throw error;
  }
};

async function getOrder(orderId) {
  // This call is automatically traced by X-Ray
  const result = await docClient.send(new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: { PK: `ORDER#${orderId}`, SK: 'METADATA' }
  }));
  return result.Item;
}
```

**Custom Tracing:**
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import boto3

# Patch all supported libraries
patch_all()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

@xray_recorder.capture('process_order')
def process_order(order_id):
    """Process order with X-Ray tracing"""
    
    # Add annotations
    xray_recorder.put_annotation('order_id', order_id)
    xray_recorder.put_annotation('service', 'order-processor')
    
    # Add metadata
    xray_recorder.put_metadata('processing_time', datetime.now().isoformat())
    
    try:
        # Subsegment for database operation
        with xray_recorder.capture('fetch_order'):
            response = table.get_item(Key={'PK': f'ORDER#{order_id}', 'SK': 'METADATA'})
            order = response['Item']
        
        # Subsegment for business logic
        with xray_recorder.capture('validate_order'):
            validate_order(order)
        
        return order
    except Exception as e:
        xray_recorder.put_metadata('error', str(e))
        raise
```

#### CloudWatch Custom Metrics

**Embedded Metric Format (EMF):**
```javascript
export const handler = async (event) => {
  const startTime = Date.now();
  
  try {
    await processOrder(event);
    
    // Emit custom metrics using EMF
    console.log(JSON.stringify({
      _aws: {
        Timestamp: Date.now(),
        CloudWatchMetrics: [{
          Namespace: 'OrderProcessing',
          Dimensions: [['Environment', 'Service']],
          Metrics: [
            { Name: 'ProcessingTime', Unit: 'Milliseconds' },
            { Name: 'OrdersProcessed', Unit: 'Count' }
          ]
        }]
      },
      Environment: process.env.ENVIRONMENT,
      Service: 'OrderProcessor',
      ProcessingTime: Date.now() - startTime,
      OrdersProcessed: 1,
      OrderId: event.orderId,
      CustomerId: event.customerId
    }));
    
    return { statusCode: 200 };
  } catch (error) {
    // Emit error metric
    console.log(JSON.stringify({
      _aws: {
        Timestamp: Date.now(),
        CloudWatchMetrics: [{
          Namespace: 'OrderProcessing',
          Dimensions: [['Environment', 'Service']],
          Metrics: [{ Name: 'Errors', Unit: 'Count' }]
        }]
      },
      Environment: process.env.ENVIRONMENT,
      Service: 'OrderProcessor',
      Errors: 1,
      ErrorType: error.name
    }));
    
    throw error;
  }
};
```

**CloudWatch Composite Alarms:**
```yaml
HighErrorRateAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: HighErrorRate
    MetricName: Errors
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 300
    EvaluationPeriods: 2
    Threshold: 10
    ComparisonOperator: GreaterThanThreshold

HighLatencyAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: HighLatency
    MetricName: Duration
    Namespace: AWS/Lambda
    Statistic: Average
    Period: 300
    EvaluationPeriods: 2
    Threshold: 5000
    ComparisonOperator: GreaterThanThreshold

CompositeAlarm:
  Type: AWS::CloudWatch::CompositeAlarm
  Properties:
    AlarmName: ServiceDegraded
    AlarmDescription: Service is degraded (high errors OR high latency)
    AlarmRule: !Sub |
      ALARM(${HighErrorRateAlarm}) OR ALARM(${HighLatencyAlarm})
    ActionsEnabled: true
    AlarmActions:
      - !Ref SNSTopic
```

#### Structured Logging

**Best Practices:**
```javascript
class Logger {
  constructor(context) {
    this.context = context;
  }

  log(level, message, metadata = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      requestId: this.context.requestId,
      functionName: this.context.functionName,
      functionVersion: this.context.functionVersion,
      ...metadata
    };
    
    console.log(JSON.stringify(logEntry));
  }

  info(message, metadata) {
    this.log('INFO', message, metadata);
  }

  error(message, error, metadata) {
    this.log('ERROR', message, {
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack
      },
      ...metadata
    });
  }

  warn(message, metadata) {
    this.log('WARN', message, metadata);
  }
}

export const handler = async (event, context) => {
  const logger = new Logger(context);
  
  logger.info('Processing started', {
    orderId: event.orderId,
    customerId: event.customerId
  });
  
  try {
    const result = await processOrder(event);
    logger.info('Processing completed', { result });
    return result;
  } catch (error) {
    logger.error('Processing failed', error, {
      orderId: event.orderId
    });
    throw error;
  }
};
```

---

## Level 3: Deep Dive Resources

### Official AWS Documentation

**Step Functions:**
- [Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [State Machine Examples](https://github.com/aws-samples/aws-stepfunctions-examples)
- [Best Practices](https://docs.aws.amazon.com/step-functions/latest/dg/bp-general.html)

**EventBridge:**
- [User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [Event Patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [Schema Registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html)

**Lambda Layers:**
- [Working with Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [Creating Layers](https://docs.aws.amazon.com/lambda/latest/dg/creating-deleting-layers.html)

**DynamoDB:**
- [Single-Table Design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html)
- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
- [Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)

**Observability:**
- [X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [CloudWatch Embedded Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html)

### Books and Courses

**Books:**
- "AWS Lambda in Action" by Danilo Poccia
- "The DynamoDB Book" by Alex DeBrie
- "Serverless Architectures on AWS" by Peter Sbarski

**Courses:**
- AWS Certified Solutions Architect Professional
- A Cloud Guru: AWS Serverless
- Linux Academy: DynamoDB Deep Dive

### Architecture Patterns

**AWS Prescriptive Guidance:**
- [Serverless Patterns Collection](https://serverlessland.com/patterns)
- [EventBridge Patterns](https://serverlessland.com/event-driven-architecture)
- [Step Functions Workflows](https://serverlessland.com/workflows)

**Reference Architectures:**
- [AWS Samples Repository](https://github.com/aws-samples)
- [Serverless Application Repository](https://serverlessrepo.aws.amazon.com/)

### Bundled Resources

See included templates and scripts:
- `templates/step-functions-state-machine.json`
- `templates/eventbridge-patterns.json`
- `templates/lambda-layer-structure/`
- `templates/dynamodb-single-table.yaml`
- `templates/custom-authorizer.js`
- `scripts/cost-optimization.py`
