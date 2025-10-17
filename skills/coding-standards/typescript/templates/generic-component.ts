/**
 * Generic Component Template
 *
 * Demonstrates advanced TypeScript patterns including:
 * - Generic classes and methods
 * - Type constraints
 * - Discriminated unions
 * - Builder pattern
 * - Type-safe event handling
 */

// Base types and interfaces
export interface Identifiable {
  readonly id: string;
}

export interface Timestamped {
  readonly createdAt: Date;
  readonly updatedAt: Date;
}

export interface Entity extends Identifiable, Timestamped {
  readonly version: number;
}

// Generic Repository Pattern
export interface Repository<T extends Identifiable> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

export class InMemoryRepository<T extends Identifiable> implements Repository<T> {
  private readonly storage = new Map<string, T>();

  async findById(id: string): Promise<T | null> {
    return this.storage.get(id) ?? null;
  }

  async findAll(): Promise<T[]> {
    return Array.from(this.storage.values());
  }

  async save(entity: T): Promise<T> {
    this.storage.set(entity.id, entity);
    return entity;
  }

  async delete(id: string): Promise<boolean> {
    return this.storage.delete(id);
  }

  async findWhere(predicate: (entity: T) => boolean): Promise<T[]> {
    return Array.from(this.storage.values()).filter(predicate);
  }

  clear(): void {
    this.storage.clear();
  }
}

// Generic Service with validation
export interface Validator<T> {
  validate(data: unknown): data is T;
  getErrors(): string[];
}

export class Service<T extends Entity> {
  constructor(
    private readonly repository: Repository<T>,
    private readonly validator?: Validator<T>
  ) {}

  async create(data: Omit<T, keyof Entity>): Promise<T> {
    const entity = {
      ...data,
      id: this.generateId(),
      createdAt: new Date(),
      updatedAt: new Date(),
      version: 1,
    } as T;

    if (this.validator && !this.validator.validate(entity)) {
      throw new ValidationError(this.validator.getErrors());
    }

    return this.repository.save(entity);
  }

  async update(id: string, updates: Partial<T>): Promise<T> {
    const existing = await this.repository.findById(id);
    if (!existing) {
      throw new NotFoundError(`Entity with id ${id} not found`);
    }

    const updated = {
      ...existing,
      ...updates,
      updatedAt: new Date(),
      version: existing.version + 1,
    } as T;

    if (this.validator && !this.validator.validate(updated)) {
      throw new ValidationError(this.validator.getErrors());
    }

    return this.repository.save(updated);
  }

  async delete(id: string): Promise<void> {
    const deleted = await this.repository.delete(id);
    if (!deleted) {
      throw new NotFoundError(`Entity with id ${id} not found`);
    }
  }

  async findById(id: string): Promise<T> {
    const entity = await this.repository.findById(id);
    if (!entity) {
      throw new NotFoundError(`Entity with id ${id} not found`);
    }
    return entity;
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }
}

// Custom errors
export class ValidationError extends Error {
  constructor(public readonly errors: string[]) {
    super(`Validation failed: ${errors.join(', ')}`);
    this.name = 'ValidationError';
  }
}

export class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NotFoundError';
  }
}

// Generic event system with type safety
export type EventMap = Record<string, any>;

export interface EventEmitter<T extends EventMap> {
  on<K extends keyof T>(event: K, listener: (data: T[K]) => void): this;
  off<K extends keyof T>(event: K, listener: (data: T[K]) => void): this;
  emit<K extends keyof T>(event: K, data: T[K]): void;
}

export class TypedEventEmitter<T extends EventMap> implements EventEmitter<T> {
  private readonly listeners = new Map<keyof T, Set<(data: any) => void>>();

  on<K extends keyof T>(event: K, listener: (data: T[K]) => void): this {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
    return this;
  }

  off<K extends keyof T>(event: K, listener: (data: T[K]) => void): this {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.delete(listener);
    }
    return this;
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(listener => listener(data));
    }
  }
}

// Generic builder pattern
export interface Builder<T> {
  build(): T;
}

export class EntityBuilder<T extends Entity> implements Builder<T> {
  private data: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    return this;
  }

  setMultiple(values: Partial<T>): this {
    Object.assign(this.data, values);
    return this;
  }

  build(): T {
    const entity = {
      ...this.data,
      id: this.data.id ?? this.generateId(),
      createdAt: this.data.createdAt ?? new Date(),
      updatedAt: this.data.updatedAt ?? new Date(),
      version: this.data.version ?? 1,
    };

    this.validate(entity);
    return entity as T;
  }

  private validate(entity: Partial<T>): asserts entity is T {
    const required: (keyof Entity)[] = ['id', 'createdAt', 'updatedAt', 'version'];
    const missing = required.filter(key => !(key in entity));

    if (missing.length > 0) {
      throw new ValidationError([`Missing required fields: ${missing.join(', ')}`]);
    }
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }
}

// Example usage
export interface User extends Entity {
  readonly username: string;
  readonly email: string;
  readonly role: 'admin' | 'user' | 'guest';
}

// Define user-specific events
export interface UserEvents {
  created: User;
  updated: { user: User; changes: Partial<User> };
  deleted: { id: string };
}

// Usage example
export function example() {
  const repository = new InMemoryRepository<User>();
  const service = new Service<User>(repository);
  const events = new TypedEventEmitter<UserEvents>();

  // Type-safe event listeners
  events.on('created', user => {
    console.log('User created:', user.username);
  });

  events.on('updated', ({ user, changes }) => {
    console.log('User updated:', user.username, changes);
  });

  // Builder pattern
  const user = new EntityBuilder<User>()
    .set('username', 'alice')
    .set('email', 'alice@example.com')
    .set('role', 'admin')
    .build();

  return { repository, service, events, user };
}
