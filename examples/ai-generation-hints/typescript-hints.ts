// templates/ai-generation-hints/typescript-hints.ts
/**
 * AI Generation Hints for TypeScript - Standards-Compliant Code Templates
 * 
 * Usage:
 * @generate typescript:[component-type] with:[CS:typescript + FE:react + TS:jest]
 */

// Result type for error handling (CS:error-handling)
type Result<T, E = Error> = 
  | { success: true; value: T }
  | { success: false; error: E };

// Utility functions for Result type
const Result = {
  ok: <T>(value: T): Result<T> => ({ success: true, value }),
  err: <E = Error>(error: E): Result<never, E> => ({ success: false, error }),
  isOk: <T, E>(result: Result<T, E>): result is { success: true; value: T } => 
    result.success,
  isErr: <T, E>(result: Result<T, E>): result is { success: false; error: E } => 
    !result.success,
};

/**
 * Standard React Component Template (FE:react)
 * 
 * AI Instructions:
 * - Use functional components with hooks
 * - Include proper TypeScript types
 * - Implement error boundaries
 * - Add loading and error states
 * - Include accessibility attributes
 * - Memoize expensive computations
 */
import React, { useState, useEffect, useMemo, useCallback } from 'react';

interface StandardComponentProps {
  id: string;
  data?: unknown;
  onAction?: (result: Result<unknown>) => void;
  className?: string;
}

export const StandardComponent: React.FC<StandardComponentProps> = React.memo(({
  id,
  data,
  onAction,
  className = '',
}) => {
  // State management with proper typing
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [processedData, setProcessedData] = useState<unknown>(null);

  // Memoized computations (FE:performance)
  const expensiveComputation = useMemo(() => {
    if (!data) return null;
    // Expensive computation here
    return processData(data);
  }, [data]);

  // Callbacks with proper memoization
  const handleAction = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await performAction(id, processedData);
      
      if (Result.isOk(result)) {
        onAction?.(result);
      } else {
        setError(result.error);
      }
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);
      onAction?.(Result.err(error));
    } finally {
      setLoading(false);
    }
  }, [id, processedData, onAction]);

  // Effects with cleanup
  useEffect(() => {
    let cancelled = false;

    const loadData = async () => {
      if (!id) return;

      setLoading(true);
      try {
        const result = await fetchData(id);
        if (!cancelled) {
          if (Result.isOk(result)) {
            setProcessedData(result.value);
          } else {
            setError(result.error);
          }
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      cancelled = true;
    };
  }, [id]);

  // Render with accessibility (WD:accessibility)
  if (loading) {
    return (
      <div role="status" aria-live="polite" aria-busy="true">
        <span className="sr-only">Loading...</span>
        {/* Loading spinner component */}
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" aria-live="assertive">
        <p>Error: {error.message}</p>
        <button onClick={() => setError(null)}>Dismiss</button>
      </div>
    );
  }

  return (
    <div className={`standard-component ${className}`}>
      {/* Component content */}
      <button
        onClick={handleAction}
        disabled={loading}
        aria-busy={loading}
      >
        Perform Action
      </button>
    </div>
  );
});

StandardComponent.displayName = 'StandardComponent';

/**
 * Standard API Service Template (CS:api + SEC:api)
 * 
 * AI Instructions:
 * - Include proper error handling
 * - Implement request/response typing
 * - Add authentication headers
 * - Include retry logic
 * - Add request cancellation
 */

interface RequestConfig {
  headers?: Record<string, string>;
  timeout?: number;
  retries?: number;
  signal?: AbortSignal;
}

class StandardAPIService {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;
  private authToken?: string;

  constructor(baseURL: string, config?: { headers?: Record<string, string> }) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...config?.headers,
    };
  }

  /**
   * Set authentication token (SEC:auth)
   */
  setAuthToken(token: string): void {
    this.authToken = token;
  }

  /**
   * Standard request method with error handling and retries
   */
  private async request<T>(
    method: string,
    endpoint: string,
    data?: unknown,
    config?: RequestConfig
  ): Promise<Result<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const { retries = 3, timeout = 30000, signal, headers = {} } = config || {};

    // Merge headers with auth token (SEC:api)
    const requestHeaders = {
      ...this.defaultHeaders,
      ...headers,
      ...(this.authToken && { Authorization: `Bearer ${this.authToken}` }),
    };

    let lastError: Error | null = null;

    // Retry logic (CS:resilience)
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const response = await fetch(url, {
          method,
          headers: requestHeaders,
          body: data ? JSON.stringify(data) : undefined,
          signal: signal || controller.signal,
        });

        clearTimeout(timeoutId);

        // Response validation (CS:error-handling)
        if (!response.ok) {
          throw new APIError(
            `HTTP ${response.status}: ${response.statusText}`,
            response.status,
            await response.text()
          );
        }

        const responseData = await response.json() as T;
        
        // Validate response data (SEC:validation)
        if (!this.validateResponse(responseData)) {
          throw new ValidationError('Invalid response format');
        }

        return Result.ok(responseData);

      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        
        // Don't retry on client errors (4xx)
        if (error instanceof APIError && error.status >= 400 && error.status < 500) {
          return Result.err(error);
        }

        // Exponential backoff for retries
        if (attempt < retries) {
          await this.delay(Math.pow(2, attempt) * 1000);
          continue;
        }
      }
    }

    return Result.err(lastError || new Error('Unknown error'));
  }

  /**
   * Response validation (SEC:validation)
   */
  private validateResponse(data: unknown): boolean {
    // Add specific validation logic based on response type
    return data !== null && data !== undefined;
  }

  /**
   * Delay helper for retries
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Standard CRUD operations
   */
  async get<T>(endpoint: string, config?: RequestConfig): Promise<Result<T>> {
    return this.request<T>('GET', endpoint, undefined, config);
  }

  async post<T>(endpoint: string, data: unknown, config?: RequestConfig): Promise<Result<T>> {
    return this.request<T>('POST', endpoint, data, config);
  }

  async put<T>(endpoint: string, data: unknown, config?: RequestConfig): Promise<Result<T>> {
    return this.request<T>('PUT', endpoint, data, config);
  }

  async delete<T>(endpoint: string, config?: RequestConfig): Promise<Result<T>> {
    return this.request<T>('DELETE', endpoint, undefined, config);
  }
}

/**
 * Custom Error Classes (CS:error-handling)
 */
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public responseBody: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

class ValidationError extends Error {
  constructor(message: string, public field?: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

/**
 * React Hook Templates (FE:react)
 */

/**
 * Standard data fetching hook with caching
 */
function useStandardFetch<T>(
  endpoint: string,
  options?: {
    dependencies?: unknown[];
    cache?: boolean;
    cacheTime?: number;
  }
): {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const apiService = useMemo(() => new StandardAPIService('/api'), []);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    const result = await apiService.get<T>(endpoint);

    if (Result.isOk(result)) {
      setData(result.value);
    } else {
      setError(result.error);
    }

    setLoading(false);
  }, [endpoint, apiService]);

  useEffect(() => {
    fetchData();
  }, [...(options?.dependencies || []), fetchData]);

  return { data, loading, error, refetch: fetchData };
}

/**
 * Testing Templates (TS:jest)
 */

/**
 * Standard test template for React components
 */
const componentTestTemplate = `
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StandardComponent } from './StandardComponent';

describe('StandardComponent', () => {
  it('renders without crashing', () => {
    render(<StandardComponent id="test-id" />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles loading state', async () => {
    render(<StandardComponent id="test-id" />);
    
    // Initially shows loading
    expect(screen.getByRole('status')).toBeInTheDocument();
    
    // Wait for content to load
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });

  it('handles error state', async () => {
    // Mock API to return error
    global.fetch = jest.fn(() =>
      Promise.reject(new Error('API Error'))
    );

    render(<StandardComponent id="test-id" />);
    
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
      expect(screen.getByText(/API Error/i)).toBeInTheDocument();
    });
  });

  it('calls onAction callback', async () => {
    const onAction = jest.fn();
    render(<StandardComponent id="test-id" onAction={onAction} />);
    
    await waitFor(() => {
      expect(screen.getByRole('button')).not.toBeDisabled();
    });

    await userEvent.click(screen.getByRole('button'));
    
    await waitFor(() => {
      expect(onAction).toHaveBeenCalledWith(
        expect.objectContaining({ success: true })
      );
    });
  });
});
`;

// AI Generation Instructions
/**
 * When generating TypeScript/React code:
 * 
 * 1. Always use functional components with hooks (FE:react)
 * 2. Include proper TypeScript types for all props and state
 * 3. Use Result type for error handling
 * 4. Implement loading and error states
 * 5. Add accessibility attributes (ARIA)
 * 6. Memoize expensive computations
 * 7. Handle component cleanup in useEffect
 * 8. Include comprehensive tests (85%+ coverage)
 * 9. Follow RESTful API patterns
 * 10. Implement proper error boundaries
 * 
 * Example prompt usage:
 * @generate typescript:[user-list] with:[FE:react + CS:typescript + TS:jest]
 */

// Helper functions
declare function processData(data: unknown): unknown;
declare function performAction(id: string, data: unknown): Promise<Result<unknown>>;
declare function fetchData(id: string): Promise<Result<unknown>>;