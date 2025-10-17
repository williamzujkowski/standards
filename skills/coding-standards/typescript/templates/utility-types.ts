/**
 * TypeScript Utility Types - Comprehensive Examples
 *
 * This file demonstrates built-in utility types and custom utility type patterns
 * for common type manipulation scenarios.
 *
 * @see https://www.typescriptlang.org/docs/handbook/utility-types.html
 */

// ===== Base Interface for Examples =====

interface IUser {
  id: number;
  name: string;
  email: string;
  age?: number;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
  updatedAt: Date;
}


// ===== Built-in Utility Types =====

/**
 * Partial<T> - Makes all properties optional
 */
type PartialUser = Partial<IUser>;
// Result: { id?: number; name?: string; email?: string; ... }

function updateUser(id: number, updates: Partial<IUser>): void {
  // Only provide the fields you want to update
  console.log(`Updating user ${id}:`, updates);
}


/**
 * Required<T> - Makes all properties required
 */
type RequiredUser = Required<IUser>;
// Result: { id: number; name: string; email: string; age: number; ... }


/**
 * Readonly<T> - Makes all properties readonly
 */
type ReadonlyUser = Readonly<IUser>;
// Result: { readonly id: number; readonly name: string; ... }

const immutableUser: ReadonlyUser = {
  id: 1,
  name: 'Alice',
  email: 'alice@example.com',
  role: 'admin',
  createdAt: new Date(),
  updatedAt: new Date(),
};
// immutableUser.name = 'Bob'; // Error: Cannot assign to 'name' because it is a read-only property


/**
 * Pick<T, K> - Creates a type by picking specific properties
 */
type UserCredentials = Pick<IUser, 'email' | 'id'>;
// Result: { email: string; id: number }


/**
 * Omit<T, K> - Creates a type by omitting specific properties
 */
type UserWithoutTimestamps = Omit<IUser, 'createdAt' | 'updatedAt'>;
// Result: { id: number; name: string; email: string; age?: number; role: ... }


/**
 * Record<K, T> - Creates an object type with keys K and values T
 */
type UserRoles = Record<'admin' | 'user' | 'guest', string[]>;
// Result: { admin: string[]; user: string[]; guest: string[] }

const permissions: UserRoles = {
  admin: ['read', 'write', 'delete'],
  user: ['read', 'write'],
  guest: ['read'],
};


/**
 * Exclude<T, U> - Excludes types from T that are assignable to U
 */
type NonAdminRole = Exclude<IUser['role'], 'admin'>;
// Result: 'user' | 'guest'


/**
 * Extract<T, U> - Extracts types from T that are assignable to U
 */
type AdminRole = Extract<IUser['role'], 'admin'>;
// Result: 'admin'


/**
 * NonNullable<T> - Excludes null and undefined from T
 */
type NonNullableAge = NonNullable<IUser['age']>;
// Result: number (age? becomes age)


/**
 * ReturnType<T> - Extracts the return type of a function
 */
function getUser(): IUser {
  return {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    role: 'admin',
    createdAt: new Date(),
    updatedAt: new Date(),
  };
}

type UserReturnType = ReturnType<typeof getUser>;
// Result: IUser


/**
 * Parameters<T> - Extracts parameter types of a function as a tuple
 */
function createUser(name: string, email: string, age?: number): IUser {
  return {
    id: Date.now(),
    name,
    email,
    age,
    role: 'user',
    createdAt: new Date(),
    updatedAt: new Date(),
  };
}

type CreateUserParams = Parameters<typeof createUser>;
// Result: [name: string, email: string, age?: number | undefined]


/**
 * ConstructorParameters<T> - Extracts constructor parameter types
 */
class UserModel {
  constructor(public name: string, public email: string) {}
}

type UserModelParams = ConstructorParameters<typeof UserModel>;
// Result: [name: string, email: string]


/**
 * InstanceType<T> - Extracts the instance type of a constructor
 */
type UserInstance = InstanceType<typeof UserModel>;
// Result: UserModel


// ===== Custom Utility Types =====

/**
 * DeepPartial<T> - Makes all properties and nested properties optional
 */
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

interface INestedUser {
  profile: {
    name: string;
    address: {
      city: string;
      country: string;
    };
  };
}

type PartialNestedUser = DeepPartial<INestedUser>;
// Result: All nested properties are optional


/**
 * DeepReadonly<T> - Makes all properties and nested properties readonly
 */
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};


/**
 * Nullable<T> - Makes a type nullable (T | null)
 */
type Nullable<T> = T | null;

type NullableUser = Nullable<IUser>;
// Result: IUser | null


/**
 * Optional<T, K> - Makes specific properties optional
 */
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type UserWithOptionalEmail = Optional<IUser, 'email'>;
// Result: IUser with email as optional


/**
 * RequireAtLeastOne<T, K> - Requires at least one of the specified keys
 */
type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>;
  }[Keys];

type UserWithAtLeastOneContact = RequireAtLeastOne<
  { email?: string; phone?: string },
  'email' | 'phone'
>;


/**
 * Mutable<T> - Removes readonly from all properties
 */
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};

type MutableUser = Mutable<ReadonlyUser>;
// Result: All properties are writable


/**
 * ValueOf<T> - Extracts all value types from an object
 */
type ValueOf<T> = T[keyof T];

type UserValues = ValueOf<IUser>;
// Result: number | string | Date | 'admin' | 'user' | 'guest' | undefined


/**
 * PromiseType<T> - Unwraps a Promise type
 */
type PromiseType<T> = T extends Promise<infer U> ? U : T;

type UserPromise = Promise<IUser>;
type UnwrappedUser = PromiseType<UserPromise>;
// Result: IUser


/**
 * FunctionPropertyNames<T> - Extracts names of function properties
 */
type FunctionPropertyNames<T> = {
  [K in keyof T]: T[K] extends (...args: unknown[]) => unknown ? K : never;
}[keyof T];

interface IUserService {
  getUser: () => IUser;
  saveUser: (user: IUser) => void;
  data: IUser[];
}

type UserServiceMethods = FunctionPropertyNames<IUserService>;
// Result: 'getUser' | 'saveUser'


/**
 * NonFunctionPropertyNames<T> - Extracts names of non-function properties
 */
type NonFunctionPropertyNames<T> = {
  [K in keyof T]: T[K] extends (...args: unknown[]) => unknown ? never : K;
}[keyof T];

type UserServiceData = NonFunctionPropertyNames<IUserService>;
// Result: 'data'


/**
 * Writeable<T> - Makes all properties writable (opposite of Readonly)
 */
type Writeable<T> = { -readonly [P in keyof T]: T[P] };


/**
 * StrictOmit<T, K> - Omit with compile-time key checking
 */
type StrictOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;


/**
 * Merge<T, U> - Merges two types (U overrides T)
 */
type Merge<T, U> = Omit<T, keyof U> & U;

type ExtendedUser = Merge<IUser, { bio: string; avatarUrl: string }>;
// Result: IUser with additional bio and avatarUrl properties


// ===== Type Guards with Utility Types =====

/**
 * Type guard for checking if a value has a specific property
 */
function hasProperty<T, K extends string>(
  obj: T,
  key: K
): obj is T & Record<K, unknown> {
  return typeof obj === 'object' && obj !== null && key in obj;
}

// Usage
function processUser(user: unknown): void {
  if (hasProperty(user, 'name') && hasProperty(user, 'email')) {
    console.log(`User: ${user.name} (${user.email})`);
  }
}


// ===== Export All Types =====

export type {
  IUser,
  PartialUser,
  RequiredUser,
  ReadonlyUser,
  UserCredentials,
  UserWithoutTimestamps,
  UserRoles,
  NonAdminRole,
  AdminRole,
  NonNullableAge,
  UserReturnType,
  CreateUserParams,
  UserModelParams,
  UserInstance,
  DeepPartial,
  DeepReadonly,
  Nullable,
  Optional,
  RequireAtLeastOne,
  Mutable,
  ValueOf,
  PromiseType,
  FunctionPropertyNames,
  NonFunctionPropertyNames,
  Writeable,
  StrictOmit,
  Merge,
};

export { updateUser, getUser, createUser, UserModel, hasProperty, processUser };
