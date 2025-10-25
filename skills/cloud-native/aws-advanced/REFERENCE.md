# AWS Advanced Patterns - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [Step Functions Complete Examples](#step-functions-complete-examples)
- [EventBridge Advanced Patterns](#eventbridge-advanced-patterns)
- [Lambda Layers Implementation](#lambda-layers-implementation)
- [API Gateway Advanced Features](#api-gateway-advanced-features)
- [DynamoDB Single-Table Design](#dynamodb-single-table-design)
- [SQS/SNS Messaging Patterns](#sqssns-messaging-patterns)
- [Cost Optimization Implementations](#cost-optimization-implementations)
- [Observability Full Examples](#observability-full-examples)

---

## Step Functions Complete Examples

### Sequential Workflow (Full Implementation)

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

### Parallel Execution Pattern

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

### Map State (Dynamic Parallelism)

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

### Saga Pattern (Compensating Transactions)

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

### Step Functions SDK Integration

**Node.js - AWS SDK v3:**

```javascript
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

**Python - Boto3:**

```python
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

---

## EventBridge Advanced Patterns

### Complex Event Pattern Matching

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

### EventBridge Publisher Implementation

**Node.js:**

```javascript
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

**Python:**

```python
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

### EventBridge Schema Registry

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

---

## Lambda Layers Implementation

### Python Layer Build Script

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

### Node.js Layer Build Script

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

### Using Layers in Lambda Functions

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

---

## API Gateway Advanced Features

### Custom Authorizer (JWT Token)

```javascript
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

### Request-Based Authorizer

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

  const allowedIps = result.Item.allowedIps || [];
  return allowedIps.length === 0 || allowedIps.includes(sourceIp);
}
```

### VTL Mapping Templates

**Request Transformation:**

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

**Response Transformation:**

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

---

## DynamoDB Single-Table Design

### Complete Access Pattern Implementation

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

// 5. Get order with items
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

### DynamoDB Streams Processing

```javascript
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const handler = async (event) => {
  for (const record of event.Records) {
    const { eventName, dynamodb } = record;

    if (eventName === 'INSERT' || eventName === 'MODIFY') {
      const newImage = unmarshall(dynamodb.NewImage);

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
  if (order.SK === 'METADATA' && order.status === 'completed') {
    await sendOrderCompletionEmail(order);
    await updateAnalytics(order);
  }
}
```

### DynamoDB Transactions

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

---

## SQS/SNS Messaging Patterns

### FIFO Queue Implementation

```javascript
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';

const client = new SQSClient({ region: 'us-east-1' });

async function sendMessage(orderId, orderData) {
  const command = new SendMessageCommand({
    QueueUrl: process.env.QUEUE_URL,
    MessageBody: JSON.stringify(orderData),
    MessageGroupId: `order-${orderId}`,
    MessageDeduplicationId: `${orderId}-${Date.now()}`,
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

### Fan-Out Pattern (SNS → SQS)

```yaml
OrderTopic:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: OrderEvents

InventoryQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: InventoryQueue
    VisibilityTimeout: 300
    RedrivePolicy:
      deadLetterTargetArn: !GetAtt InventoryDLQ.Arn
      maxReceiveCount: 3

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
```

### SNS Publisher (Python)

```python
import boto3
import json

sns_client = boto3.client('sns', region_name='us-east-1')

def publish_order_event(event_type: str, order_data: dict):
    """Publish order event to SNS topic"""
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

### Dead-Letter Queue Consumer

```javascript
import { SQSClient, DeleteMessageCommand } from '@aws-sdk/client-sqs';

const client = new SQSClient({ region: 'us-east-1' });

export const handler = async (event) => {
  for (const record of event.Records) {
    try {
      const message = JSON.parse(record.body);
      await processMessage(message);

      await client.send(new DeleteMessageCommand({
        QueueUrl: process.env.QUEUE_URL,
        ReceiptHandle: record.receiptHandle
      }));

    } catch (error) {
      console.error('Processing failed:', error);
      throw error;
    }
  }
};

async function processMessage(message) {
  const alreadyProcessed = await checkProcessingStatus(message.id);
  if (alreadyProcessed) {
    console.log('Message already processed:', message.id);
    return;
  }

  await performBusinessLogic(message);
  await recordProcessingComplete(message.id);
}
```

---

## Cost Optimization Implementations

### DynamoDB Auto Scaling

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

### S3 Lifecycle Policies

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

---

## Observability Full Examples

### X-Ray Distributed Tracing

```javascript
import AWSXRay from 'aws-xray-sdk-core';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

// Instrument AWS SDK
const client = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  const segment = AWSXRay.getSegment();
  const subsegment = segment.addNewSubsegment('processOrder');

  try {
    subsegment.addAnnotation('orderId', event.orderId);
    subsegment.addAnnotation('customerId', event.customerId);
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
```

### CloudWatch Embedded Metric Format (EMF)

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

### Structured Logging

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

## Additional Resources

See the official AWS documentation for:

- [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [Lambda Layers Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
