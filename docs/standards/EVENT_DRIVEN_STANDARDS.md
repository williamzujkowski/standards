# Event-Driven Architecture Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** EVT

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Event-Driven Design Principles](#1-event-driven-design-principles)
2. [Event Schema and Contracts](#2-event-schema-and-contracts)
3. [Message Brokers and Queues](#3-message-brokers-and-queues)
4. [Event Sourcing Patterns](#4-event-sourcing-patterns)
5. [CQRS Implementation](#5-cqrs-implementation)
6. [Saga Patterns](#6-saga-patterns)
7. [Event Processing and Analytics](#7-event-processing-and-analytics)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Event-Driven Design Principles

### 1.1 Core Principles **[REQUIRED]**

```yaml
event_driven_principles:
  - "Events as first-class citizens"
  - "Loose coupling between services"
  - "Eventual consistency"
  - "Idempotent event processing"
  - "Event ordering guarantees"
  - "Schema evolution support"
```

### 1.2 Event Types and Classification

```json
{
  "event_types": {
    "domain_events": {
      "description": "Business events that occur in the domain",
      "examples": ["OrderCreated", "PaymentProcessed", "CustomerRegistered"],
      "characteristics": ["Immutable", "Past tense", "Business meaningful"]
    },
    "integration_events": {
      "description": "Events for cross-service communication",
      "examples": ["UserUpdated", "InventoryChanged", "NotificationSent"],
      "characteristics": ["Service boundaries", "Contract-based", "Versioned"]
    },
    "system_events": {
      "description": "Technical events for system monitoring",
      "examples": ["ServiceStarted", "HealthCheckFailed", "MemoryUsageHigh"],
      "characteristics": ["Technical", "Monitoring", "Operational"]
    }
  }
}
```

---

## 2. Event Schema and Contracts

### 2.1 Event Schema Standards **[REQUIRED]**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CloudEvent Schema",
  "type": "object",
  "required": ["specversion", "type", "source", "id", "time", "data"],
  "properties": {
    "specversion": {
      "type": "string",
      "enum": ["1.0"]
    },
    "type": {
      "type": "string",
      "pattern": "^[a-z0-9]+(?:\\.[a-z0-9]+)*\\.[A-Z][a-zA-Z0-9]*$",
      "description": "Event type in format: domain.aggregate.Event"
    },
    "source": {
      "type": "string",
      "format": "uri",
      "description": "Source system identifier"
    },
    "id": {
      "type": "string",
      "description": "Unique event identifier"
    },
    "time": {
      "type": "string",
      "format": "date-time",
      "description": "Event timestamp in RFC3339 format"
    },
    "subject": {
      "type": "string",
      "description": "Subject of the event"
    },
    "datacontenttype": {
      "type": "string",
      "default": "application/json"
    },
    "data": {
      "type": "object",
      "description": "Event payload"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "correlationId": {"type": "string"},
        "causationId": {"type": "string"},
        "version": {"type": "string"},
        "traceId": {"type": "string"}
      }
    }
  }
}
```

### 2.2 Schema Evolution **[REQUIRED]**

```typescript
// Event versioning strategy
interface EventVersioning {
  backwards_compatible_changes: [
    "Adding optional fields",
    "Adding new event types",
    "Expanding enum values"
  ];

  breaking_changes: [
    "Removing required fields",
    "Changing field types",
    "Removing event types",
    "Changing event semantics"
  ];

  evolution_strategy: {
    semantic_versioning: "Major.Minor.Patch";
    schema_registry: "Confluent Schema Registry or equivalent";
    compatibility_levels: ["BACKWARD", "FORWARD", "FULL"];
  };
}

// Example versioned event
interface OrderCreatedV1 {
  orderId: string;
  customerId: string;
  amount: number;
  items: OrderItem[];
}

interface OrderCreatedV2 {
  orderId: string;
  customerId: string;
  amount: number;
  currency: string; // New field
  items: OrderItem[];
  discounts?: Discount[]; // Optional field
}
```

---

## 3. Message Brokers and Queues

### 3.1 Apache Kafka Configuration **[REQUIRED]**

```yaml
# Kafka topic configuration
topics:
  order-events:
    partitions: 12
    replication_factor: 3
    config:
      retention.ms: 2592000000  # 30 days
      cleanup.policy: delete
      compression.type: snappy
      min.insync.replicas: 2
      segment.ms: 604800000     # 7 days

  customer-events:
    partitions: 6
    replication_factor: 3
    config:
      retention.ms: 7776000000  # 90 days
      cleanup.policy: delete
      compression.type: lz4

# Producer configuration
producer:
  acks: all
  retries: 2147483647
  max.in.flight.requests.per.connection: 5
  enable.idempotence: true
  compression.type: snappy
  batch.size: 16384
  linger.ms: 5

# Consumer configuration
consumer:
  enable.auto.commit: false
  auto.offset.reset: earliest
  isolation.level: read_committed
  max.poll.records: 500
  session.timeout.ms: 30000
```

### 3.2 RabbitMQ Configuration **[REQUIRED]**

```yaml
# RabbitMQ exchange and queue setup
exchanges:
  - name: "order.events"
    type: "topic"
    durable: true
    properties:
      alternate-exchange: "order.dead-letter"

  - name: "customer.events"
    type: "fanout"
    durable: true

queues:
  - name: "order.processing"
    durable: true
    properties:
      x-message-ttl: 3600000
      x-max-retries: 3
      x-dead-letter-exchange: "order.dead-letter"
      x-dead-letter-routing-key: "failed"

  - name: "order.dead-letter"
    durable: true
    properties:
      x-message-ttl: 2592000000  # 30 days

bindings:
  - exchange: "order.events"
    queue: "order.processing"
    routing_key: "order.created"
```

---

## 4. Event Sourcing Patterns

### 4.1 Event Store Implementation **[REQUIRED]**

```typescript
// Event store interface
interface EventStore {
  saveEvents(streamId: string, events: DomainEvent[], expectedVersion: number): Promise<void>;
  getEvents(streamId: string, fromVersion?: number): Promise<DomainEvent[]>;
  getAllEvents(fromPosition?: number): Promise<DomainEvent[]>;
  createSnapshot(streamId: string, snapshot: Snapshot): Promise<void>;
  getSnapshot(streamId: string): Promise<Snapshot | null>;
}

// Domain event base class
abstract class DomainEvent {
  constructor(
    public readonly id: string,
    public readonly aggregateId: string,
    public readonly version: number,
    public readonly timestamp: Date,
    public readonly correlationId?: string,
    public readonly causationId?: string
  ) {}

  abstract getEventType(): string;
}

// Example aggregate with event sourcing
class Order {
  private events: DomainEvent[] = [];

  constructor(
    public readonly id: string,
    private version: number = 0
  ) {}

  static fromHistory(events: DomainEvent[]): Order {
    const order = new Order(events[0].aggregateId);
    events.forEach(event => order.apply(event, false));
    return order;
  }

  createOrder(customerId: string, items: OrderItem[]): void {
    const event = new OrderCreatedEvent(
      crypto.randomUUID(),
      this.id,
      this.version + 1,
      new Date(),
      customerId,
      items
    );
    this.apply(event, true);
  }

  private apply(event: DomainEvent, isNew: boolean): void {
    // Apply event to aggregate state
    switch (event.getEventType()) {
      case 'OrderCreated':
        this.applyOrderCreated(event as OrderCreatedEvent);
        break;
      // ... other event handlers
    }

    if (isNew) {
      this.events.push(event);
    }
    this.version = event.version;
  }

  getUncommittedEvents(): DomainEvent[] {
    return [...this.events];
  }

  markEventsAsCommitted(): void {
    this.events = [];
  }
}

// Event store repository
class EventSourcedRepository<T> {
  constructor(
    private eventStore: EventStore,
    private aggregateFactory: (id: string) => T,
    private snapshotFrequency: number = 10
  ) {}

  async save(aggregate: any): Promise<void> {
    const events = aggregate.getUncommittedEvents();
    if (events.length === 0) return;

    await this.eventStore.saveEvents(
      aggregate.id,
      events,
      aggregate.version - events.length
    );

    aggregate.markEventsAsCommitted();

    // Create snapshot if needed
    if (aggregate.version % this.snapshotFrequency === 0) {
      const snapshot = this.createSnapshot(aggregate);
      await this.eventStore.createSnapshot(aggregate.id, snapshot);
    }
  }

  async getById(id: string): Promise<T | null> {
    // Try to load from snapshot first
    const snapshot = await this.eventStore.getSnapshot(id);
    let fromVersion = 0;
    let aggregate: T;

    if (snapshot) {
      aggregate = this.rehydrateFromSnapshot(snapshot);
      fromVersion = snapshot.version + 1;
    } else {
      aggregate = this.aggregateFactory(id);
    }

    // Load events since snapshot
    const events = await this.eventStore.getEvents(id, fromVersion);
    if (events.length === 0 && !snapshot) return null;

    // Apply events to reconstruct current state
    events.forEach(event => (aggregate as any).apply(event, false));

    return aggregate;
  }
}
```

---

## 5. CQRS Implementation

### 5.1 Command and Query Separation **[REQUIRED]**

```typescript
// Command side
interface Command {
  readonly id: string;
  readonly timestamp: Date;
  readonly correlationId?: string;
}

interface CommandHandler<T extends Command> {
  handle(command: T): Promise<void>;
}

class CreateOrderCommand implements Command {
  constructor(
    public readonly id: string,
    public readonly timestamp: Date,
    public readonly customerId: string,
    public readonly items: OrderItem[],
    public readonly correlationId?: string
  ) {}
}

class CreateOrderCommandHandler implements CommandHandler<CreateOrderCommand> {
  constructor(
    private orderRepository: EventSourcedRepository<Order>,
    private eventBus: EventBus
  ) {}

  async handle(command: CreateOrderCommand): Promise<void> {
    // Validate command
    await this.validateCommand(command);

    // Create aggregate
    const order = new Order(command.id);
    order.createOrder(command.customerId, command.items);

    // Save to event store
    await this.orderRepository.save(order);

    // Publish domain events
    const events = order.getUncommittedEvents();
    for (const event of events) {
      await this.eventBus.publish(event);
    }
  }

  private async validateCommand(command: CreateOrderCommand): Promise<void> {
    if (!command.customerId) {
      throw new ValidationError("Customer ID is required");
    }
    if (!command.items || command.items.length === 0) {
      throw new ValidationError("Order must have at least one item");
    }
  }
}

// Query side
interface Query {
  readonly id: string;
}

interface QueryHandler<TQuery extends Query, TResult> {
  handle(query: TQuery): Promise<TResult>;
}

class GetOrderQuery implements Query {
  constructor(
    public readonly id: string,
    public readonly orderId: string
  ) {}
}

interface OrderReadModel {
  id: string;
  customerId: string;
  status: string;
  totalAmount: number;
  items: OrderItemReadModel[];
  createdAt: Date;
  updatedAt: Date;
}

class GetOrderQueryHandler implements QueryHandler<GetOrderQuery, OrderReadModel | null> {
  constructor(private readModelRepository: ReadModelRepository) {}

  async handle(query: GetOrderQuery): Promise<OrderReadModel | null> {
    return await this.readModelRepository.findById(query.orderId);
  }
}

// Read model projections
class OrderProjection {
  constructor(private repository: ReadModelRepository) {}

  async on(event: OrderCreatedEvent): Promise<void> {
    const readModel: OrderReadModel = {
      id: event.aggregateId,
      customerId: event.customerId,
      status: 'Created',
      totalAmount: this.calculateTotal(event.items),
      items: event.items.map(item => ({
        productId: item.productId,
        quantity: item.quantity,
        price: item.price
      })),
      createdAt: event.timestamp,
      updatedAt: event.timestamp
    };

    await this.repository.save(readModel);
  }

  async on(event: OrderStatusChangedEvent): Promise<void> {
    const readModel = await this.repository.findById(event.aggregateId);
    if (readModel) {
      readModel.status = event.newStatus;
      readModel.updatedAt = event.timestamp;
      await this.repository.save(readModel);
    }
  }
}
```

---

## 6. Saga Patterns

### 6.1 Orchestration Saga **[REQUIRED]**

```typescript
// Saga orchestrator
abstract class Saga {
  protected state: SagaState = SagaState.NotStarted;
  protected currentStep: number = 0;

  abstract getSteps(): SagaStep[];
  abstract getCompensationSteps(): SagaStep[];

  async execute(): Promise<SagaResult> {
    this.state = SagaState.Running;
    const steps = this.getSteps();

    try {
      for (let i = 0; i < steps.length; i++) {
        this.currentStep = i;
        await steps[i].execute();
      }

      this.state = SagaState.Completed;
      return SagaResult.Success;

    } catch (error) {
      this.state = SagaState.Failed;
      await this.compensate();
      return SagaResult.Failed;
    }
  }

  private async compensate(): Promise<void> {
    const compensationSteps = this.getCompensationSteps();

    // Execute compensation steps in reverse order
    for (let i = this.currentStep; i >= 0; i--) {
      try {
        await compensationSteps[i].execute();
      } catch (error) {
        // Log compensation failure but continue
        console.error(`Compensation step ${i} failed:`, error);
      }
    }
  }
}

// Order processing saga
class OrderProcessingSaga extends Saga {
  constructor(
    private orderId: string,
    private paymentService: PaymentService,
    private inventoryService: InventoryService,
    private shippingService: ShippingService
  ) {
    super();
  }

  getSteps(): SagaStep[] {
    return [
      new ReserveInventoryStep(this.orderId, this.inventoryService),
      new ProcessPaymentStep(this.orderId, this.paymentService),
      new CreateShipmentStep(this.orderId, this.shippingService)
    ];
  }

  getCompensationSteps(): SagaStep[] {
    return [
      new CancelShipmentStep(this.orderId, this.shippingService),
      new RefundPaymentStep(this.orderId, this.paymentService),
      new ReleaseInventoryStep(this.orderId, this.inventoryService)
    ];
  }
}

interface SagaStep {
  execute(): Promise<void>;
}

class ReserveInventoryStep implements SagaStep {
  constructor(
    private orderId: string,
    private inventoryService: InventoryService
  ) {}

  async execute(): Promise<void> {
    await this.inventoryService.reserve(this.orderId);
  }
}

// Saga manager
class SagaManager {
  private sagas = new Map<string, Saga>();

  async startSaga(sagaId: string, saga: Saga): Promise<void> {
    this.sagas.set(sagaId, saga);

    try {
      const result = await saga.execute();

      if (result === SagaResult.Success) {
        await this.onSagaCompleted(sagaId);
      } else {
        await this.onSagaFailed(sagaId);
      }
    } finally {
      this.sagas.delete(sagaId);
    }
  }

  private async onSagaCompleted(sagaId: string): Promise<void> {
    // Emit saga completed event
    console.log(`Saga ${sagaId} completed successfully`);
  }

  private async onSagaFailed(sagaId: string): Promise<void> {
    // Emit saga failed event
    console.log(`Saga ${sagaId} failed and compensated`);
  }
}
```

### 6.2 Choreography Saga **[REQUIRED]**

```typescript
// Event-driven saga using choreography
class OrderCreatedHandler {
  constructor(private inventoryService: InventoryService) {}

  async handle(event: OrderCreatedEvent): Promise<void> {
    try {
      await this.inventoryService.reserve(event.aggregateId, event.items);

      // Publish success event
      const inventoryReservedEvent = new InventoryReservedEvent(
        crypto.randomUUID(),
        event.aggregateId,
        1,
        new Date(),
        event.items,
        event.id // causation ID
      );

      await this.eventBus.publish(inventoryReservedEvent);

    } catch (error) {
      // Publish failure event
      const inventoryReservationFailedEvent = new InventoryReservationFailedEvent(
        crypto.randomUUID(),
        event.aggregateId,
        1,
        new Date(),
        error.message,
        event.id
      );

      await this.eventBus.publish(inventoryReservationFailedEvent);
    }
  }
}

class InventoryReservedHandler {
  constructor(private paymentService: PaymentService) {}

  async handle(event: InventoryReservedEvent): Promise<void> {
    try {
      await this.paymentService.charge(event.aggregateId);

      const paymentProcessedEvent = new PaymentProcessedEvent(
        crypto.randomUUID(),
        event.aggregateId,
        1,
        new Date(),
        event.id
      );

      await this.eventBus.publish(paymentProcessedEvent);

    } catch (error) {
      // Compensate by releasing inventory
      const paymentFailedEvent = new PaymentFailedEvent(
        crypto.randomUUID(),
        event.aggregateId,
        1,
        new Date(),
        error.message,
        event.id
      );

      await this.eventBus.publish(paymentFailedEvent);
    }
  }
}
```

---

## 7. Event Processing and Analytics

### 7.1 Stream Processing **[REQUIRED]**

```typescript
// Real-time event processing with Kafka Streams
import { KafkaStreams } from 'kafka-streams';

class EventAnalyticsProcessor {
  private stream: KafkaStreams;

  constructor() {
    this.stream = new KafkaStreams({
      kafkaHost: 'localhost:9092',
      groupId: 'event-analytics',
      clientName: 'analytics-processor'
    });
  }

  async start(): Promise<void> {
    const orderEventsStream = this.stream.getKStream('order-events');
    const customerEventsStream = this.stream.getKStream('customer-events');

    // Real-time order metrics
    const orderMetrics = orderEventsStream
      .filter(event => event.type === 'OrderCreated')
      .window(60 * 1000) // 1-minute windows
      .groupBy(event => event.data.customerId)
      .aggregate(
        () => ({ count: 0, totalAmount: 0 }),
        (oldVal, event) => ({
          count: oldVal.count + 1,
          totalAmount: oldVal.totalAmount + event.data.amount
        })
      );

    orderMetrics.to('order-metrics-topic');

    // Customer behavior analysis
    const customerJourney = customerEventsStream
      .join(orderEventsStream, 'customerId', 'inner', 5 * 60 * 1000) // 5-minute window
      .map(([customerEvent, orderEvent]) => ({
        customerId: customerEvent.data.customerId,
        journey: {
          customerAction: customerEvent.type,
          orderAction: orderEvent.type,
          timestamp: orderEvent.timestamp
        }
      }));

    customerJourney.to('customer-journey-topic');

    await this.stream.start();
  }
}

// Complex Event Processing (CEP)
class ComplexEventProcessor {
  private patterns: EventPattern[] = [];

  addPattern(pattern: EventPattern): void {
    this.patterns.push(pattern);
  }

  async processEvent(event: DomainEvent): Promise<void> {
    for (const pattern of this.patterns) {
      if (await pattern.matches(event)) {
        await pattern.execute(event);
      }
    }
  }
}

interface EventPattern {
  matches(event: DomainEvent): Promise<boolean>;
  execute(event: DomainEvent): Promise<void>;
}

// Fraud detection pattern
class FraudDetectionPattern implements EventPattern {
  private suspiciousActivities = new Map<string, number>();

  async matches(event: DomainEvent): Promise<boolean> {
    return event.getEventType() === 'PaymentProcessed';
  }

  async execute(event: DomainEvent): Promise<void> {
    const paymentEvent = event as PaymentProcessedEvent;
    const customerId = paymentEvent.customerId;

    // Track payment frequency
    const currentCount = this.suspiciousActivities.get(customerId) || 0;
    this.suspiciousActivities.set(customerId, currentCount + 1);

    // Check for suspicious pattern (e.g., >5 payments in 1 hour)
    if (currentCount > 5) {
      const fraudAlertEvent = new FraudAlertEvent(
        crypto.randomUUID(),
        customerId,
        1,
        new Date(),
        'High frequency payments detected',
        event.id
      );

      await this.eventBus.publish(fraudAlertEvent);
    }

    // Clean up old entries (simplified)
    setTimeout(() => {
      this.suspiciousActivities.delete(customerId);
    }, 3600000); // 1 hour
  }
}
```

---

## Implementation Checklist

### Event-Driven Architecture

- [ ] Event schema standards defined
- [ ] Message broker configured
- [ ] Event versioning strategy implemented
- [ ] Dead letter queues configured
- [ ] Event replay capability implemented

### Event Sourcing

- [ ] Event store implemented
- [ ] Aggregate design patterns applied
- [ ] Snapshot mechanism configured
- [ ] Event replay functionality tested
- [ ] Projection rebuild capability ready

### CQRS Implementation

- [ ] Command and query separation clear
- [ ] Read model projections implemented
- [ ] Eventually consistent reads handled
- [ ] Query optimization applied
- [ ] Command validation comprehensive

### Saga Patterns

- [ ] Orchestration sagas implemented
- [ ] Choreography patterns defined
- [ ] Compensation logic tested
- [ ] Saga state persistence configured
- [ ] Timeout and retry mechanisms ready

### Event Processing

- [ ] Stream processing configured
- [ ] Complex event patterns defined
- [ ] Real-time analytics implemented
- [ ] Event correlation working
- [ ] Performance monitoring active

---

## Related Standards

- [Coding Standards](CODING_STANDARDS.md) - Event-driven code patterns
- [Observability Standards](OBSERVABILITY_STANDARDS.md) - Event monitoring and tracing
- [Model Context Protocol Standards](MODEL_CONTEXT_PROTOCOL_STANDARDS.md) - Event-driven MCP patterns
- [Data Engineering Standards](DATA_ENGINEERING_STANDARDS.md) - Event streaming infrastructure

---

**End of Event-Driven Architecture Standards**
