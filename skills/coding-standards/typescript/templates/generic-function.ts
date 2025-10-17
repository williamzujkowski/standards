/**
 * Generic Function Examples - TypeScript Best Practices
 *
 * This file demonstrates proper usage of generic functions with constraints,
 * multiple type parameters, and advanced generic patterns.
 */

// ===== Basic Generic Function =====

/**
 * Returns the first element of an array
 */
function first<T>(array: T[]): T | undefined {
  return array[0];
}

// Usage
const numbers = [1, 2, 3];
const firstNumber = first(numbers); // Type: number | undefined

const strings = ['a', 'b', 'c'];
const firstString = first(strings); // Type: string | undefined


// ===== Generic Function with Constraints =====

/**
 * Finds an item in an array by a specific property
 */
function findByProperty<T extends Record<string, unknown>, K extends keyof T>(
  items: T[],
  key: K,
  value: T[K]
): T | undefined {
  return items.find((item) => item[key] === value);
}

// Usage
interface IUser {
  id: number;
  name: string;
  email: string;
}

const users: IUser[] = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
];

const user = findByProperty(users, 'id', 1); // Type: IUser | undefined


// ===== Generic Function with Multiple Type Parameters =====

/**
 * Maps an array of items using a transformation function
 */
function mapArray<TInput, TOutput>(
  items: TInput[],
  mapper: (item: TInput, index: number) => TOutput
): TOutput[] {
  return items.map(mapper);
}

// Usage
const numbers2 = [1, 2, 3];
const doubled = mapArray(numbers2, (num) => num * 2); // Type: number[]
const stringified = mapArray(numbers2, (num) => num.toString()); // Type: string[]


// ===== Generic Function with Default Type Parameters =====

/**
 * Creates a response object with data and metadata
 */
interface IResponse<TData = unknown, TMeta = Record<string, unknown>> {
  data: TData;
  meta: TMeta;
  timestamp: Date;
}

function createResponse<TData, TMeta = Record<string, unknown>>(
  data: TData,
  meta?: TMeta
): IResponse<TData, TMeta> {
  return {
    data,
    meta: meta ?? ({} as TMeta),
    timestamp: new Date(),
  };
}

// Usage
const userResponse = createResponse({ id: 1, name: 'Alice' }); // Type: IResponse<{id: number, name: string}, Record<string, unknown>>
const pageResponse = createResponse([1, 2, 3], { page: 1, total: 100 }); // Type: IResponse<number[], {page: number, total: number}>


// ===== Generic Function with Conditional Types =====

/**
 * Unwraps a Promise type or returns the type as-is
 */
type Awaited<T> = T extends Promise<infer U> ? U : T;

function unwrap<T>(value: T): Awaited<T> {
  if (value instanceof Promise) {
    // This is simplified; in practice, you'd need async/await
    throw new Error('Cannot synchronously unwrap Promise');
  }
  return value as Awaited<T>;
}


// ===== Generic Function with Branded Types =====

/**
 * Branded types for type-safe identifiers
 */
type UserId = number & { readonly __brand: 'UserId' };
type ProductId = number & { readonly __brand: 'ProductId' };

function createUserId(id: number): UserId {
  return id as UserId;
}

function getUserById<T extends UserId>(id: T): IUser | undefined {
  // Type-safe: only accepts UserId, not plain numbers or ProductId
  return users.find((user) => user.id === id);
}

// Usage
const userId = createUserId(1);
const foundUser = getUserById(userId); // OK

// const productId = 1; // Error: Argument of type 'number' is not assignable to parameter of type 'UserId'


// ===== Generic Factory Function =====

/**
 * Generic factory for creating instances with validation
 */
interface IValidatable {
  validate(): boolean;
}

function createValidated<T extends IValidatable>(
  Constructor: new (...args: unknown[]) => T,
  ...args: unknown[]
): T {
  const instance = new Constructor(...args);
  if (!instance.validate()) {
    throw new Error(`Validation failed for ${Constructor.name}`);
  }
  return instance;
}

// Usage
class ValidatedUser implements IValidatable {
  constructor(public name: string, public email: string) {}

  public validate(): boolean {
    return this.name.length > 0 && this.email.includes('@');
  }
}

const validUser = createValidated(ValidatedUser, 'Alice', 'alice@example.com'); // Type: ValidatedUser


// ===== Generic Function with Type Guards =====

/**
 * Type guard to check if a value is of a specific type
 */
function isArray<T>(value: unknown): value is T[] {
  return Array.isArray(value);
}

function processValue<T>(value: T | T[]): T[] {
  if (isArray<T>(value)) {
    return value; // Type: T[]
  }
  return [value]; // Type: T[]
}


// ===== Generic Async Function =====

/**
 * Generic async function for fetching data
 */
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return (await response.json()) as T;
}

// Usage
interface IApiResponse {
  data: IUser[];
  total: number;
}

// const apiResponse = await fetchData<IApiResponse>('https://api.example.com/users');


// ===== Generic Function with Variadic Tuples =====

/**
 * Merges multiple objects into one
 */
function merge<T extends object[]>(...objects: T): UnionToIntersection<T[number]> {
  return Object.assign({}, ...objects) as UnionToIntersection<T[number]>;
}

// Helper type for merging
type UnionToIntersection<U> = (U extends unknown ? (k: U) => void : never) extends (
  k: infer I
) => void
  ? I
  : never;

// Usage
const merged = merge({ a: 1 }, { b: 2 }, { c: 3 }); // Type: {a: number} & {b: number} & {c: number}


// ===== Export for Module Usage =====

export {
  first,
  findByProperty,
  mapArray,
  createResponse,
  unwrap,
  createUserId,
  getUserById,
  createValidated,
  isArray,
  processValue,
  fetchData,
  merge,
};

export type { IResponse, UserId, ProductId, Awaited };
