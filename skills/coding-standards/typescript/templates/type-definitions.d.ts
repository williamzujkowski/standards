/**
 * Type Definition Template
 *
 * This file demonstrates best practices for creating TypeScript type definitions.
 * Use this as a reference when creating .d.ts files for your modules.
 */

// Module augmentation for extending existing types
declare module 'existing-module' {
  export interface ExistingInterface {
    newProperty: string;
  }
}

// Global type augmentation
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test';
      DATABASE_URL: string;
      API_KEY: string;
    }
  }
}

// Ambient module declarations for untyped packages
declare module 'untyped-package' {
  export function someFunction(arg: string): Promise<void>;
  export const someConstant: number;
}

// Utility type definitions
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type Maybe<T> = T | null | undefined;

// Branded types for type safety
export type UserId = string & { readonly __brand: 'UserId' };
export type Email = string & { readonly __brand: 'Email' };
export type Timestamp = number & { readonly __brand: 'Timestamp' };

// Result/Either type for error handling
export type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

// Async data state
export type AsyncData<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

// Deep readonly utility
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? DeepReadonly<T[P]>
    : T[P];
};

// Deep partial utility
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object
    ? DeepPartial<T[P]>
    : T[P];
};

// Type-safe object keys
export type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];

// Function type helpers
export type AsyncFunction<Args extends any[] = any[], Return = any> = (
  ...args: Args
) => Promise<Return>;

export type Callback<T = void> = (value: T) => void;
export type Predicate<T> = (value: T) => boolean;

// Opaque types
export type Opaque<T, K extends string> = T & { readonly __opaque: K };

// Example usage in a module
export interface User {
  readonly id: UserId;
  readonly email: Email;
  readonly name: string;
  readonly createdAt: Timestamp;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: Timestamp;
}

// Namespace for grouping related types
export namespace API {
  export interface Request<T = unknown> {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
    url: string;
    headers?: Record<string, string>;
    body?: T;
  }

  export interface Response<T = unknown> {
    status: number;
    data: T;
    headers: Record<string, string>;
  }

  export interface Error {
    code: string;
    message: string;
    details?: unknown;
  }
}

// Export empty object to make this a module
export {};
