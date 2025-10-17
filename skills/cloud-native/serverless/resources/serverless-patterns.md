# Common Serverless Architecture Patterns

## 1. API Backend Pattern

**Use Case:** RESTful API, GraphQL endpoint, mobile backend

**Architecture:**

```
Client → API Gateway → Lambda → DynamoDB/RDS
         ↓
      CloudFront (CDN)
         ↓
      WAF (Security)
```

**Key Components:**

- **API Gateway:** HTTP routing, throttling, API keys, CORS
- **Lambda:** Business logic execution
- **DynamoDB:** NoSQL database (PAY_PER_REQUEST)
- **CloudWatch:** Logs, metrics, alarms

**Best Practices:**

- Use Lambda Proxy integration for full control
- Enable X-Ray tracing for distributed debugging
- Implement API Gateway caching (TTL 60-3600s)
- Use Lambda Authorizers for custom authentication
- Configure throttling limits (burst, rate)

**Cost Optimization:**

- Cache frequent queries (API Gateway, ElastiCache)
- Use DynamoDB on-demand billing for variable traffic
- Implement exponential backoff for retries

---

## 2. Event-Driven Processing

**Use Case:** File upload processing, ETL pipelines, data transformation

**Architecture:**

```
S3 Upload → S3 Event → Lambda → Transform → Store (S3/DynamoDB)
                       ↓
                    SQS (DLQ for failures)
```

**Key Components:**

- **S3 Event Notifications:** Trigger on ObjectCreated, ObjectRemoved
- **Lambda:** Process files (parse CSV, resize images, transcode video)
- **SQS Dead Letter Queue:** Handle failures

**Patterns:**

### Fan-Out Pattern

```
S3 Event → SNS → Lambda 1 (Thumbnail)
           ↓
           └→ Lambda 2 (Metadata extraction)
           └→ Lambda 3 (Virus scan)
```

### Fan-In Pattern (with Step Functions)

```
S3 Event → Lambda (Orchestrator) → Step Functions
           ↓
           ├→ Lambda 1 (Process chunk 1)
           ├→ Lambda 2 (Process chunk 2)
           └→ Lambda 3 (Aggregate results)
```

**Best Practices:**

- Use S3 batch operations for bulk processing
- Implement idempotent handlers (S3 events may duplicate)
- Configure S3 event filtering (prefix, suffix)
- Set appropriate Lambda timeout (15 min max)
- Use Lambda layers for large dependencies (Pillow, FFmpeg)

---

## 3. Scheduled Tasks (Cron Jobs)

**Use Case:** Backup automation, report generation, data aggregation

**Architecture:**

```
EventBridge Rule (cron) → Lambda → Execute Task → Notify (SNS/SES)
```

**Cron Expressions:**

- `rate(5 minutes)` - Every 5 minutes
- `cron(0 12 * * ? *)` - Daily at noon UTC
- `cron(0 0 ? * MON *)` - Every Monday at midnight

**Example Use Cases:**

### Database Backup

```python
# EventBridge: cron(0 2 * * ? *) - 2 AM daily
def lambda_handler(event, context):
    rds = boto3.client('rds')
    snapshot_id = f"backup-{datetime.now().strftime('%Y%m%d')}"

    rds.create_db_snapshot(
        DBInstanceIdentifier='prod-db',
        DBSnapshotIdentifier=snapshot_id
    )
```

### Aggregation Pipeline

```python
# EventBridge: rate(1 hour)
def lambda_handler(event, context):
    # Aggregate logs from CloudWatch
    # Store metrics in DynamoDB
    # Publish dashboard to S3
```

**Best Practices:**

- Use idempotent task IDs (date-based)
- Configure CloudWatch alarms for task failures
- Implement retry logic with exponential backoff
- Use Step Functions for complex workflows

---

## 4. Stream Processing

**Use Case:** Real-time analytics, clickstream processing, IoT data ingestion

**Architecture:**

```
Kinesis Data Stream → Lambda (consumer) → Transform → Elasticsearch/S3
                                         ↓
                                      DynamoDB (state)
```

**Key Components:**

- **Kinesis Data Streams:** Real-time data ingestion (1 MB/s per shard)
- **Lambda:** Process records in batches (1-10,000 records)
- **Kinesis Data Firehose:** Direct load to S3/Redshift/Elasticsearch

**Batch Processing:**

```python
def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)

        # Process record
        process_event(data)

    # Return partial batch failures (Lambda retries only failed records)
    return {
        "batchItemFailures": [
            {"itemIdentifier": record['kinesis']['sequenceNumber']}
        ]
    }
```

**Best Practices:**

- Use batch processing (up to 10,000 records)
- Configure bisect batch on error (automatic retry)
- Set appropriate batch window (0-300 seconds)
- Monitor iterator age (lag indicator)
- Use enhanced fan-out for low-latency (dedicated throughput)

---

## 5. Async Messaging (Queue Processing)

**Use Case:** Order processing, background jobs, rate limiting

**Architecture:**

```
Client → API Gateway → Lambda (Producer) → SQS → Lambda (Consumer)
                                           ↓
                                        DLQ (Dead Letter Queue)
```

**SQS Configuration:**

- **Standard Queue:** At-least-once delivery, unlimited throughput
- **FIFO Queue:** Exactly-once processing, 3000 TPS, ordered

**Consumer Pattern:**

```python
# Lambda polls SQS (batch size 1-10)
def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        try:
            process_message(body)
        except Exception as e:
            # Return failed message (Lambda will retry)
            return {
                "batchItemFailures": [
                    {"itemIdentifier": record['messageId']}
                ]
            }
```

**Best Practices:**

- Set visibility timeout > Lambda timeout
- Configure DLQ after 3-5 retries
- Use batch processing for efficiency
- Implement exponential backoff
- Monitor ApproximateAgeOfOldestMessage metric

---

## 6. Saga Pattern (Distributed Transactions)

**Use Case:** Multi-step workflows, order fulfillment, payment processing

**Architecture (Step Functions):**

```
Start → Reserve Inventory → Process Payment → Ship Order → Complete
        ↓ (failure)           ↓ (failure)      ↓ (failure)
        Compensate           Compensate       Compensate
```

**Step Functions State Machine:**

```json
{
  "StartAt": "ReserveInventory",
  "States": {
    "ReserveInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:reserve",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "ResultPath": "$.error",
        "Next": "ReleaseInventory"
      }],
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:payment",
      "Catch": [{
        "ErrorEquals": ["PaymentFailed"],
        "Next": "ReleaseInventory"
      }],
      "Next": "ShipOrder"
    },
    "ShipOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:ship",
      "End": true
    },
    "ReleaseInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:release",
      "End": true
    }
  }
}
```

**Best Practices:**

- Implement compensating transactions (rollback)
- Use Step Functions for orchestration (vs. Lambda)
- Store state in DynamoDB or Step Functions context
- Configure retry policies per step
- Monitor workflow execution history

---

## 7. Lambda at Edge (CloudFront Functions)

**Use Case:** URL rewriting, A/B testing, geolocation routing

**Architecture:**

```
Client → CloudFront → Lambda@Edge → Origin (S3/API)
         ↓
      Viewer Request → Modify Request
      Origin Response → Modify Response
```

**CloudFront Functions vs Lambda@Edge:**

| Feature | CloudFront Functions | Lambda@Edge |
|---------|---------------------|-------------|
| **Runtime** | JavaScript (ECMAScript 5.1) | Node.js, Python |
| **Max Duration** | <1 ms | 5s (viewer), 30s (origin) |
| **Use Cases** | URL rewrite, headers | Auth, image resize |
| **Cost** | $0.10/1M | $0.60/1M |

**Example: A/B Testing**

```javascript
// CloudFront Function (viewer request)
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // 50% traffic to variant B
    if (Math.random() < 0.5) {
        request.uri = uri.replace('/index.html', '/index-b.html');
    }

    return request;
}
```

---

## 8. WebSocket API (Real-Time Communication)

**Use Case:** Chat applications, live dashboards, collaborative editing

**Architecture:**

```
Client (WebSocket) → API Gateway WebSocket → Lambda
                     ↓
                  Connection Table (DynamoDB)
```

**Connection Lifecycle:**

```python
# $connect route
def connect_handler(event, context):
    connection_id = event['requestContext']['connectionId']

    # Store connection
    table.put_item(Item={
        'connectionId': connection_id,
        'userId': event['queryStringParameters']['userId']
    })

# $disconnect route
def disconnect_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    table.delete_item(Key={'connectionId': connection_id})

# $default route (message)
def message_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])

    # Broadcast to all connections
    api_gateway = boto3.client('apigatewaymanagementapi')
    for conn in get_all_connections():
        api_gateway.post_to_connection(
            ConnectionId=conn['connectionId'],
            Data=json.dumps(body)
        )
```

**Best Practices:**

- Store connection IDs in DynamoDB (TTL 2 hours)
- Handle stale connections gracefully
- Implement connection authorization ($connect route)
- Use SQS for fan-out broadcasting
- Monitor connection count and message rate

---

## Cost Comparison (Monthly)

**API Backend (10M requests, 200ms avg):**

- Lambda: $2.40
- API Gateway: $35
- DynamoDB: $5 (on-demand)
- **Total: ~$42**

**Event Processing (1M S3 uploads, 5s processing):**

- Lambda: $30
- S3: $23 (storage)
- **Total: ~$53**

**Cron Jobs (24 hourly tasks, 1s each):**

- Lambda: $0.01
- EventBridge: $0
- **Total: <$0.01**
