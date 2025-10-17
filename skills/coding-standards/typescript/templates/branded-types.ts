/**
 * Branded Types (Opaque Types) - TypeScript Pattern
 *
 * Branded types create distinct types from primitives to prevent
 * accidental mixing of logically different values that share the same
 * underlying primitive type (e.g., UserId vs ProductId, both numbers).
 *
 * Benefits:
 * - Type safety: Prevents passing wrong ID types to functions
 * - Self-documenting: Type names clearly indicate purpose
 * - Zero runtime cost: Types are erased during compilation
 *
 * @see https://egghead.io/blog/using-branded-types-in-typescript
 */

// ===== Basic Branded Type Pattern =====

/**
 * Brand symbol ensures type uniqueness at compile time
 */
declare const brand: unique symbol;

/**
 * Base branded type using intersection types
 */
type Brand<T, TBrand extends string> = T & { readonly [brand]: TBrand };

/**
 * Alternative branded type pattern using __brand property
 */
type Branded<T, TBrand extends string> = T & { readonly __brand: TBrand };


// ===== Entity ID Branded Types =====

/**
 * User ID type - cannot be confused with other IDs
 */
export type UserId = Brand<number, 'UserId'>;

/**
 * Product ID type
 */
export type ProductId = Brand<number, 'ProductId'>;

/**
 * Order ID type
 */
export type OrderId = Brand<string, 'OrderId'>;

/**
 * Organization ID type
 */
export type OrganizationId = Brand<string, 'OrganizationId'>;


// ===== Factory Functions (Smart Constructors) =====

/**
 * Creates a UserId with validation
 */
export function createUserId(id: number): UserId {
  if (id <= 0) {
    throw new Error('User ID must be positive');
  }
  return id as UserId;
}

/**
 * Creates a ProductId with validation
 */
export function createProductId(id: number): ProductId {
  if (id <= 0) {
    throw new Error('Product ID must be positive');
  }
  return id as ProductId;
}

/**
 * Creates an OrderId with format validation
 */
export function createOrderId(id: string): OrderId {
  const orderIdPattern = /^ORD-\d{8}$/;
  if (!orderIdPattern.test(id)) {
    throw new Error('Order ID must match format: ORD-12345678');
  }
  return id as OrderId;
}

/**
 * Creates an OrganizationId with UUID validation
 */
export function createOrganizationId(id: string): OrganizationId {
  const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!uuidPattern.test(id)) {
    throw new Error('Organization ID must be a valid UUID');
  }
  return id as OrganizationId;
}


// ===== Usage Examples =====

interface IUser {
  id: UserId;
  name: string;
  email: string;
}

interface IProduct {
  id: ProductId;
  name: string;
  price: number;
}

interface IOrder {
  id: OrderId;
  userId: UserId;
  productIds: ProductId[];
  total: number;
}

/**
 * Function that only accepts UserId (type-safe)
 */
export function getUserById(id: UserId): IUser | undefined {
  // Implementation would fetch user from database
  console.log(`Fetching user with ID: ${id}`);
  return undefined;
}

/**
 * Function that only accepts ProductId (type-safe)
 */
export function getProductById(id: ProductId): IProduct | undefined {
  console.log(`Fetching product with ID: ${id}`);
  return undefined;
}

/**
 * Creates an order (type-safe IDs prevent mixing)
 */
export function createOrder(userId: UserId, productIds: ProductId[]): OrderId {
  const orderId = createOrderId(`ORD-${Date.now().toString().slice(-8)}`);
  console.log(`Creating order ${orderId} for user ${userId}`);
  return orderId;
}

// ✅ Type-safe usage
const userId = createUserId(123);
const productId = createProductId(456);

getUserById(userId); // OK
getProductById(productId); // OK
createOrder(userId, [productId]); // OK

// ❌ These will cause compile-time errors:
// getUserById(456); // Error: number is not assignable to UserId
// getUserById(productId); // Error: ProductId is not assignable to UserId
// getProductById(userId); // Error: UserId is not assignable to ProductId


// ===== Value Object Branded Types =====

/**
 * Email address branded type with validation
 */
export type EmailAddress = Brand<string, 'EmailAddress'>;

export function createEmailAddress(email: string): EmailAddress {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    throw new Error('Invalid email address format');
  }
  return email.toLowerCase() as EmailAddress;
}

/**
 * URL branded type with validation
 */
export type URL = Brand<string, 'URL'>;

export function createURL(url: string): URL {
  try {
    new globalThis.URL(url);
    return url as URL;
  } catch {
    throw new Error('Invalid URL format');
  }
}

/**
 * Positive integer branded type
 */
export type PositiveInt = Brand<number, 'PositiveInt'>;

export function createPositiveInt(n: number): PositiveInt {
  if (!Number.isInteger(n) || n <= 0) {
    throw new Error('Value must be a positive integer');
  }
  return n as PositiveInt;
}

/**
 * Percentage (0-100) branded type
 */
export type Percentage = Brand<number, 'Percentage'>;

export function createPercentage(n: number): Percentage {
  if (n < 0 || n > 100) {
    throw new Error('Percentage must be between 0 and 100');
  }
  return n as Percentage;
}


// ===== Currency Branded Types =====

/**
 * USD currency type
 */
export type USD = Brand<number, 'USD'>;

/**
 * EUR currency type
 */
export type EUR = Brand<number, 'EUR'>;

/**
 * GBP currency type
 */
export type GBP = Brand<number, 'GBP'>;

export function createUSD(amount: number): USD {
  if (amount < 0) {
    throw new Error('Amount cannot be negative');
  }
  return Math.round(amount * 100) / 100 as USD; // Round to 2 decimal places
}

export function createEUR(amount: number): EUR {
  if (amount < 0) {
    throw new Error('Amount cannot be negative');
  }
  return Math.round(amount * 100) / 100 as EUR;
}

/**
 * Currency conversion (type-safe)
 */
export function convertUSDtoEUR(amount: USD, exchangeRate: number): EUR {
  return createEUR((amount as number) * exchangeRate);
}

// ❌ This will cause a compile-time error:
// function addCurrencies(a: USD, b: EUR): number {
//   return a + b; // Error: Cannot mix different currency types
// }


// ===== Date and Time Branded Types =====

/**
 * ISO date string branded type
 */
export type ISODateString = Brand<string, 'ISODateString'>;

export function createISODateString(date: Date): ISODateString {
  return date.toISOString() as ISODateString;
}

/**
 * Unix timestamp branded type
 */
export type UnixTimestamp = Brand<number, 'UnixTimestamp'>;

export function createUnixTimestamp(date: Date): UnixTimestamp {
  return Math.floor(date.getTime() / 1000) as UnixTimestamp;
}


// ===== Advanced: Branded Types with Constraints =====

/**
 * Non-empty string branded type
 */
export type NonEmptyString = Brand<string, 'NonEmptyString'>;

export function createNonEmptyString(str: string): NonEmptyString {
  if (str.trim().length === 0) {
    throw new Error('String cannot be empty');
  }
  return str as NonEmptyString;
}

/**
 * Hexadecimal color code branded type
 */
export type HexColor = Brand<string, 'HexColor'>;

export function createHexColor(color: string): HexColor {
  const hexPattern = /^#([0-9A-F]{3}|[0-9A-F]{6})$/i;
  if (!hexPattern.test(color)) {
    throw new Error('Invalid hex color format (expected #RGB or #RRGGBB)');
  }
  return color.toUpperCase() as HexColor;
}


// ===== Type Guards for Branded Types =====

/**
 * Type guard to check if a value is a valid UserId
 */
export function isUserId(value: unknown): value is UserId {
  return typeof value === 'number' && value > 0;
}

/**
 * Type guard to check if a value is a valid EmailAddress
 */
export function isEmailAddress(value: unknown): value is EmailAddress {
  if (typeof value !== 'string') return false;
  try {
    createEmailAddress(value);
    return true;
  } catch {
    return false;
  }
}


// ===== Utility: Unwrap Branded Type =====

/**
 * Extracts the underlying primitive type from a branded type
 */
export type Unwrap<T> = T extends Brand<infer U, string> ? U : T;

// Usage
type UnwrappedUserId = Unwrap<UserId>; // Result: number
type UnwrappedEmailAddress = Unwrap<EmailAddress>; // Result: string


// ===== Example: Real-World API Function =====

interface IApiResponse<T> {
  data: T;
  status: number;
}

/**
 * Type-safe API function that requires properly branded types
 */
export async function fetchUserOrders(
  userId: UserId,
  organizationId: OrganizationId
): Promise<IApiResponse<IOrder[]>> {
  // In a real implementation, this would make an HTTP request
  console.log(`Fetching orders for user ${userId} in org ${organizationId}`);

  return {
    data: [],
    status: 200,
  };
}

// ✅ Type-safe usage:
// const userId = createUserId(123);
// const orgId = createOrganizationId('550e8400-e29b-41d4-a716-446655440000');
// await fetchUserOrders(userId, orgId);

// ❌ These will cause compile-time errors:
// await fetchUserOrders(123, 'some-org-id'); // Error: Wrong types
// await fetchUserOrders(productId, orgId); // Error: ProductId is not UserId
