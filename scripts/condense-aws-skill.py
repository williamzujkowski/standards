#!/usr/bin/env python3
"""
Condense AWS Advanced skill by replacing Level 2 sections with concise versions.
"""

CONDENSED_SECTIONS = """### API Gateway Advanced Patterns

**Custom Authorizers** - Lambda functions that validate tokens/API keys before allowing API access.
- **JWT Authorizer** - Verify JWT tokens, return IAM policy + context
- **Request Authorizer** - Validate custom headers, IP whitelist, API keys

**Usage Plans & Rate Limiting:**
- Throttle: Burst (max concurrent), Rate (requests/second)
- Quota: Monthly/daily limits per API key
- Associate API keys with usage plans

**VTL Mapping Templates** - Transform request/response without Lambda:
- Add `$context` variables (requestId, authorizer data, sourceIP)
- Access `$input` for payload manipulation
- Use for legacy system integration

See [REFERENCE.md](./REFERENCE.md) for authorizer implementations, VTL examples, and WebSocket APIs.

---

### DynamoDB Advanced Patterns

**Single-Table Design** - Store multiple entity types in one table using composite keys.

**Key Strategy:**
- `PK` (Partition Key): Entity type + ID (e.g., `USER#123`, `ORDER#456`)
- `SK` (Sort Key): Relationship or sub-entity (e.g., `PROFILE`, `ORDER#2024-01-15`)
- GSI for alternate access patterns (e.g., query by email, status)

**Common Patterns:**
- 1:N relationships - Same PK, different SK prefixes
- N:N relationships - Inverted index with GSI
- Hierarchical data - SK with begins_with queries

**DynamoDB Streams** - Capture changes (INSERT/MODIFY/REMOVE) for:
- Materialized views
- Cross-region replication
- Analytics/auditing
- Event-driven workflows

**Transactions** - ACID operations across up to 100 items:
- `TransactWriteItems` - Atomic writes with conditions
- `TransactGetItems` - Consistent reads
- Use for fund transfers, inventory management

See [REFERENCE.md](./REFERENCE.md) for complete access patterns, stream processors, and transaction examples.

---

### SQS/SNS Messaging Patterns

**FIFO Queues** - Guarantee ordering and exactly-once processing:
- `MessageGroupId` - Messages with same ID processed in order
- `MessageDeduplicationId` - Prevents duplicates (5-minute window)
- Throughput: 300 TPS (batching: 3,000 TPS)

**Fan-Out Pattern** (SNS → Multiple SQS):
- Publish once to SNS topic
- Multiple SQS queues subscribe with filter policies
- Each subscriber processes independently
- Use for microservices decoupling

**Dead-Letter Queues (DLQ):**
- Capture messages that fail after `maxReceiveCount` attempts
- Analyze failure patterns
- Replay after fixing root cause

**Best Practices:**
- Idempotent processing (track message IDs in DB)
- Exponential backoff for retries
- Monitor DLQ depth with CloudWatch alarms
- Use long polling (20s) to reduce empty receives

See [REFERENCE.md](./REFERENCE.md) for FIFO queue setup, SNS filter policies, and DLQ consumers.

---

### Cost Optimization Strategies

**Lambda:**
- Right-size memory (use AWS Lambda Power Tuning tool)
- Use ARM64 (Graviton2) for 20% cost reduction
- Reserved concurrency for predictable workloads
- Reduce cold starts with provisioned concurrency

**DynamoDB:**
- On-demand vs provisioned capacity analysis
- Auto-scaling for variable workloads
- DAX (DynamoDB Accelerator) for read-heavy apps
- Delete old data with TTL (no write cost)

**S3:**
- Intelligent-Tiering for variable access patterns
- Lifecycle policies (Standard → IA → Glacier → Deep Archive)
- Delete incomplete multipart uploads
- Request metrics to optimize access patterns

**General:**
- CloudWatch Logs retention policies (default: never expire)
- Use Cost Explorer and Budget alerts
- Tag all resources for cost allocation
- Enable Cost Anomaly Detection

See [REFERENCE.md](./REFERENCE.md) for auto-scaling configs, lifecycle policies, and cost analysis scripts.

---

### Observability and Monitoring

**X-Ray Distributed Tracing:**
- Instrument AWS SDK calls automatically
- Add subsegments for custom operations
- Annotations (indexed) for filtering traces
- Metadata (not indexed) for debugging context

**CloudWatch Custom Metrics (EMF):**
- Embedded Metric Format - log-based metrics (no PutMetricData API calls)
- Custom dimensions for business KPIs
- Composite alarms (AND/OR logic across multiple alarms)

**Structured Logging:**
```javascript
console.log(JSON.stringify({
  level: 'INFO',
  message: 'Order processed',
  orderId, customerId,
  timestamp: new Date().toISOString()
}));
```

**Best Practices:**
- Correlation IDs across service boundaries
- Log sampling for high-volume endpoints
- Use CloudWatch Insights for log analysis
- Set up dashboards for key metrics (latency, errors, throttles)

See [REFERENCE.md](./REFERENCE.md) for X-Ray instrumentation, EMF examples, and structured logger implementations.

---
"""

def main():
    skill_path = "/home/william/git/standards/skills/cloud-native/aws-advanced/SKILL.md"

    with open(skill_path, 'r') as f:
        lines = f.readlines()

    # Find section boundaries
    level2_start = None
    level3_start = None

    for i, line in enumerate(lines):
        if line.startswith("## Level 2: Implementation Guide"):
            level2_start = i
        elif line.startswith("## Level 3: Deep Dive Resources"):
            level3_start = i
            break

    if level2_start is None or level3_start is None:
        print("Could not find section boundaries")
        return 1

    # Keep everything before Level 2, insert condensed content, keep Level 3 onwards
    new_content = (
        ''.join(lines[:level2_start]) +
        "## Level 2: Implementation Guide\n\n" +
        "> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.\n\n" +
        CONDENSED_SECTIONS +
        '\n'.join(lines[level3_start:])
    )

    with open(skill_path, 'w') as f:
        f.write(new_content)

    print(f"✓ Condensed Level 2 from {level3_start - level2_start} to ~100 lines")
    print(f"✓ All detailed examples moved to REFERENCE.md")

    return 0

if __name__ == "__main__":
    exit(main())
