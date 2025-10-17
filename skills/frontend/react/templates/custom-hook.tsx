import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom Hook Templates
 *
 * Collection of reusable custom hooks following React best practices.
 * All hooks start with 'use' prefix per convention.
 */

// ============================================================================
// useFetch: Generic data fetching hook
// ============================================================================

interface UseFetchOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
}

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useFetch<T>(
  url: string,
  options?: UseFetchOptions
): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [refetchToggle, setRefetchToggle] = useState(false);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    async function fetchData() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(url, {
          method: options?.method || 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
          },
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (isMounted) {
          setData(result);
        }
      } catch (err) {
        if (isMounted && err instanceof Error && err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [url, options?.method, refetchToggle]);

  const refetch = useCallback(() => {
    setRefetchToggle(prev => !prev);
  }, []);

  return { data, loading, error, refetch };
}

// Usage:
// const { data, loading, error, refetch } = useFetch<User>('/api/user/123');

// ============================================================================
// useLocalStorage: Persist state in localStorage
// ============================================================================

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  // Get from localStorage or use initial value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error loading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Update localStorage and state
  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  // Remove from localStorage
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue];
}

// Usage:
// const [name, setName, removeName] = useLocalStorage('userName', 'Guest');

// ============================================================================
// useDebounce: Debounce a value
// ============================================================================

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage:
// const [searchTerm, setSearchTerm] = useState('');
// const debouncedSearch = useDebounce(searchTerm, 300);
// useEffect(() => { api.search(debouncedSearch) }, [debouncedSearch]);

// ============================================================================
// usePrevious: Get previous value
// ============================================================================

export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage:
// const [count, setCount] = useState(0);
// const prevCount = usePrevious(count);

// ============================================================================
// useToggle: Boolean state toggle
// ============================================================================

export function useToggle(
  initialValue: boolean = false
): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(prev => !prev);
  }, []);

  const set = useCallback((newValue: boolean) => {
    setValue(newValue);
  }, []);

  return [value, toggle, set];
}

// Usage:
// const [isOpen, toggleOpen, setOpen] = useToggle(false);

// ============================================================================
// useOnClickOutside: Detect clicks outside an element
// ============================================================================

export function useOnClickOutside<T extends HTMLElement>(
  handler: () => void
): React.RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      handler();
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [handler]);

  return ref;
}

// Usage:
// const ref = useOnClickOutside<HTMLDivElement>(() => setIsOpen(false));
// <div ref={ref}>...</div>

// ============================================================================
// useMediaQuery: Responsive design hook
// ============================================================================

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);

    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);

    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

// Usage:
// const isMobile = useMediaQuery('(max-width: 768px)');

// ============================================================================
// useInterval: setInterval with hooks
// ============================================================================

export function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef<() => void>();

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const tick = () => savedCallback.current?.();
    const id = setInterval(tick, delay);

    return () => clearInterval(id);
  }, [delay]);
}

// Usage:
// useInterval(() => setCount(count + 1), 1000);

// ============================================================================
// useAsync: Generic async operation handler
// ============================================================================

interface UseAsyncResult<T> {
  loading: boolean;
  error: Error | null;
  value: T | null;
  execute: (...args: unknown[]) => Promise<void>;
}

export function useAsync<T>(
  asyncFunction: (...args: unknown[]) => Promise<T>,
  immediate: boolean = false
): UseAsyncResult<T> {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [value, setValue] = useState<T | null>(null);

  const execute = useCallback(async (...args: unknown[]) => {
    setLoading(true);
    setError(null);
    setValue(null);

    try {
      const result = await asyncFunction(...args);
      setValue(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }, [asyncFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { loading, error, value, execute };
}

// Usage:
// const { loading, error, value, execute } = useAsync(fetchUser, true);

/**
 * Custom Hook Best Practices:
 *
 * 1. Always prefix with 'use'
 * 2. Return arrays for position-based destructuring [value, setter]
 * 3. Return objects for name-based destructuring { value, setValue }
 * 4. Clean up side effects (timers, listeners, fetch abort)
 * 5. Use useCallback for returned functions
 * 6. Use useRef for values that shouldn't trigger re-renders
 * 7. Handle edge cases (unmounted components, null values)
 * 8. Add TypeScript types for all parameters and return values
 * 9. Document expected usage with examples
 * 10. Keep hooks focused on a single responsibility
 */
