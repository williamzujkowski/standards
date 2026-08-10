---
name: patterns
description: "Applies architectural design patterns including microservices decomposition, event-driven architecture, hexagonal/ports-and-adapters, CQRS, and domain-driven design bounded contexts. Use when the user asks about system design, architectural patterns, service boundaries, event sourcing, CQRS, hexagonal architecture, or domain-driven design."
---

# Architecture Patterns

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start) (5 min) → Level 2: [Implementation](#level-2-implementation) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start

### Core Principles

1. **Separation of Concerns**: Each component owns a single responsibility
2. **Loose Coupling**: Services communicate through well-defined interfaces
3. **High Cohesion**: Related functionality lives together
4. **Dependency Inversion**: Depend on abstractions, not implementations

### Pattern Selection Guide

| Pattern | Best For | Trade-off |
|---------|----------|-----------|
| Hexagonal | Testable domain logic | More initial boilerplate |
| CQRS | Read/write asymmetry | Eventual consistency complexity |
| Event-Driven | Decoupled services | Debugging distributed flows |
| Microservices | Independent deployability | Operational overhead |
| Layered | Simple CRUD apps | Tight coupling risk at scale |

### Essential Checklist

- [ ] Define bounded contexts before splitting services
- [ ] Establish communication patterns (sync vs async)
- [ ] Design for failure (circuit breakers, retries, timeouts)
- [ ] Document architectural decision records (ADRs)
- [ ] Validate with fitness functions

---

## Level 2: Implementation

### Hexagonal Architecture (Ports & Adapters)

```typescript
// Domain layer — no framework dependencies
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
}

interface PaymentGateway {
  charge(amount: Money, method: PaymentMethod): Promise<PaymentResult>;
}

class PlaceOrderUseCase {
  constructor(
    private orders: OrderRepository,
    private payments: PaymentGateway
  ) {}

  async execute(cmd: PlaceOrderCommand): Promise<OrderId> {
    const order = Order.create(cmd.items, cmd.customerId);
    const payment = await this.payments.charge(order.total, cmd.paymentMethod);
    order.confirmPayment(payment.transactionId);
    await this.orders.save(order);
    return order.id;
  }
}

// Infrastructure adapter — implements the port
class PostgresOrderRepository implements OrderRepository {
  constructor(private pool: Pool) {}

  async save(order: Order): Promise<void> {
    await this.pool.query(
      "INSERT INTO orders (id, customer_id, total, status) VALUES ($1, $2, $3, $4)",
      [order.id, order.customerId, order.total.amount, order.status]
    );
  }

  async findById(id: string): Promise<Order | null> {
    const result = await this.pool.query("SELECT * FROM orders WHERE id = $1", [id]);
    return result.rows[0] ? Order.fromRow(result.rows[0]) : null;
  }
}
```

### CQRS (Command Query Responsibility Segregation)

```typescript
// Command side — validates and writes
class CreateProductHandler {
  constructor(
    private repo: ProductRepository,
    private eventBus: EventBus
  ) {}

  async handle(cmd: CreateProduct): Promise<void> {
    const product = Product.create(cmd.name, cmd.price, cmd.category);
    await this.repo.save(product);
    await this.eventBus.publish(new ProductCreated(product.id, product.name));
  }
}

// Query side — optimized read model
class ProductQueryService {
  constructor(private readDb: ReadDatabase) {}

  async search(filters: ProductFilters): Promise<ProductListItem[]> {
    return this.readDb.query(
      "SELECT id, name, price, category FROM product_read_model WHERE category = $1 ORDER BY name LIMIT $2",
      [filters.category, filters.limit]
    );
  }
}

// Event handler keeps read model in sync
class ProductReadModelUpdater {
  constructor(private readDb: ReadDatabase) {}

  async onProductCreated(event: ProductCreated): Promise<void> {
    await this.readDb.query(
      "INSERT INTO product_read_model (id, name) VALUES ($1, $2)",
      [event.productId, event.productName]
    );
  }
}
```

### Event-Driven Architecture

```typescript
// Domain event
interface DomainEvent {
  type: string;
  aggregateId: string;
  timestamp: Date;
  payload: Record<string, unknown>;
}

// Event producer
class OrderService {
  constructor(
    private repo: OrderRepository,
    private eventBus: EventBus
  ) {}

  async cancelOrder(orderId: string, reason: string): Promise<void> {
    const order = await this.repo.findById(orderId);
    order.cancel(reason);
    await this.repo.save(order);
    await this.eventBus.publish({
      type: "order.cancelled",
      aggregateId: orderId,
      timestamp: new Date(),
      payload: { reason, customerId: order.customerId },
    });
  }
}

// Decoupled consumers react independently
class NotificationService {
  @Subscribe("order.cancelled")
  async onOrderCancelled(event: DomainEvent): Promise<void> {
    await this.emailService.send(
      event.payload.customerId,
      "order-cancelled",
      { orderId: event.aggregateId, reason: event.payload.reason }
    );
  }
}

class InventoryService {
  @Subscribe("order.cancelled")
  async onOrderCancelled(event: DomainEvent): Promise<void> {
    await this.restoreStock(event.aggregateId);
  }
}
```

### Circuit Breaker Pattern

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure: Date | null = null;
  private state: "closed" | "open" | "half-open" = "closed";

  constructor(
    private threshold: number = 5,
    private resetTimeout: number = 30000
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (Date.now() - this.lastFailure!.getTime() > this.resetTimeout) {
        this.state = "half-open";
      } else {
        throw new Error("Circuit breaker is open");
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failures = 0;
    this.state = "closed";
  }

  private onFailure(): void {
    this.failures++;
    this.lastFailure = new Date();
    if (this.failures >= this.threshold) {
      this.state = "open";
    }
  }
}
```

### Integration Points

- Links to [Coding Standards](../../coding-standards/SKILL.md) for implementation patterns
- Links to [Testing Standards](../../testing/SKILL.md) for architecture testing strategies
- Links to [Security Practices](../../security-practices/SKILL.md) for secure architecture

---

## Level 3: Mastery Resources

### Architecture Decision Records (ADRs)

```markdown
# ADR-001: Use Event-Driven Architecture for Order Processing

## Status: Accepted

## Context
Order processing requires notifying multiple downstream services
(inventory, shipping, billing) without tight coupling.

## Decision
Adopt event-driven architecture with an event bus for inter-service communication.

## Consequences
- (+) Services can be deployed independently
- (+) New consumers can subscribe without modifying producers
- (-) Eventual consistency requires careful handling
- (-) Debugging distributed flows requires correlation IDs and distributed tracing
```

### Fitness Functions

```typescript
// Architectural fitness function — enforce dependency direction
import { Project, SyntaxKind } from "ts-morph";

function validateNoCoreToInfraImports(projectPath: string): boolean {
  const project = new Project({ tsConfigFilePath: `${projectPath}/tsconfig.json` });
  const coreFiles = project.getSourceFiles("src/core/**/*.ts");

  for (const file of coreFiles) {
    const imports = file.getImportDeclarations();
    for (const imp of imports) {
      const moduleSpecifier = imp.getModuleSpecifierValue();
      if (moduleSpecifier.includes("/infrastructure/") || moduleSpecifier.includes("/adapters/")) {
        console.error(`Violation: ${file.getFilePath()} imports from infrastructure`);
        return false;
      }
    }
  }
  return true;
}
```

### Reference Materials

- [Related Standards](../../docs/standards/)
- [Best Practices Guide](../../docs/guides/)

### Templates

See the `templates/` directory for starter configurations.
