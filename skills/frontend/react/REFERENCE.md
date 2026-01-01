# React Frontend Reference

This document contains detailed examples, advanced patterns, and production-ready templates for React development. For core concepts and quick reference, see [SKILL.md](./SKILL.md).

## Table of Contents

- [Advanced Hooks Patterns](#advanced-hooks-patterns)
- [Complete State Management Examples](#complete-state-management-examples)
- [Performance Optimization Deep Dive](#performance-optimization-deep-dive)
- [Component Pattern Templates](#component-pattern-templates)
- [Comprehensive Testing Patterns](#comprehensive-testing-patterns)
- [Full Accessibility Checklist](#full-accessibility-checklist)
- [Security Best Practices](#security-best-practices)
- [Production Configuration](#production-configuration)

---

## Advanced Hooks Patterns

### useState: Complete Patterns

```tsx
// Basic usage
const [count, setCount] = useState(0);
const increment = () => setCount(count + 1);

// Multiple state variables
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [errors, setErrors] = useState<Record<string, string>>({});

// Lazy initialization (expensive initial state)
const [data, setData] = useState(() => {
  return computeExpensiveValue();
});

// Functional updates (when new state depends on old)
setCount(prevCount => prevCount + 1);

// Object state updates (always spread to avoid mutation)
const [user, setUser] = useState<User>({ name: '', email: '' });
setUser(prev => ({ ...prev, name: 'John' }));
```

### useEffect: Complete Patterns

```tsx
// Component mount (runs once)
useEffect(() => {
  console.log('Component mounted');
}, []);

// Dependency tracking (runs when deps change)
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// Cleanup function (unmount or before re-run)
useEffect(() => {
  const subscription = api.subscribe(userId);
  return () => subscription.unsubscribe();
}, [userId]);

// Async operations with cleanup
useEffect(() => {
  let isMounted = true;
  const controller = new AbortController();

  async function fetchData() {
    try {
      const result = await api.getData({ signal: controller.signal });
      if (isMounted) setData(result);
    } catch (error) {
      if (isMounted && error.name !== 'AbortError') {
        setError(error);
      }
    }
  }

  fetchData();
  return () => {
    isMounted = false;
    controller.abort();
  };
}, []);

// Event listener cleanup
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

// Timer cleanup
useEffect(() => {
  const intervalId = setInterval(() => {
    setCount(c => c + 1);
  }, 1000);
  return () => clearInterval(intervalId);
}, []);
```

### useContext: Full Provider Pattern

```tsx
// Create context with TypeScript
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  colors: {
    primary: string;
    secondary: string;
    background: string;
    text: string;
  };
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider component with full implementation
export const ThemeProvider: FC<PropsWithChildren> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('theme');
    return (saved as 'light' | 'dark') || 'light';
  });

  const toggleTheme = useCallback(() => {
    setTheme(prev => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      return next;
    });
  }, []);

  const colors = useMemo(() => {
    if (theme === 'dark') {
      return {
        primary: '#90caf9',
        secondary: '#f48fb1',
        background: '#121212',
        text: '#ffffff',
      };
    }
    return {
      primary: '#1976d2',
      secondary: '#dc004e',
      background: '#ffffff',
      text: '#000000',
    };
  }, [theme]);

  const value = useMemo(
    () => ({ theme, toggleTheme, colors }),
    [theme, toggleTheme, colors]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook for consuming context
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

// Usage in component
function ThemedButton() {
  const { theme, toggleTheme, colors } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{ backgroundColor: colors.primary, color: colors.text }}
    >
      Current theme: {theme}
    </button>
  );
}
```

### useReducer: Complex State Management

```tsx
// Complete state and action types
interface State {
  count: number;
  history: number[];
  lastAction: string | null;
  error: string | null;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'incrementBy'; payload: number }
  | { type: 'reset' }
  | { type: 'setError'; payload: string };

// Reducer with comprehensive handling
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return {
        ...state,
        count: state.count + 1,
        history: [...state.history, state.count + 1],
        lastAction: 'increment',
        error: null,
      };
    case 'decrement':
      if (state.count <= 0) {
        return { ...state, error: 'Cannot go below zero' };
      }
      return {
        ...state,
        count: state.count - 1,
        history: [...state.history, state.count - 1],
        lastAction: 'decrement',
        error: null,
      };
    case 'incrementBy':
      return {
        ...state,
        count: state.count + action.payload,
        history: [...state.history, state.count + action.payload],
        lastAction: `incrementBy(${action.payload})`,
        error: null,
      };
    case 'reset':
      return { count: 0, history: [], lastAction: 'reset', error: null };
    case 'setError':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

// Initial state with lazy initialization
const initialState: State = { count: 0, history: [], lastAction: null, error: null };

function init(initial: State): State {
  const saved = localStorage.getItem('counterState');
  return saved ? JSON.parse(saved) : initial;
}

// Usage in component
function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState, init);

  useEffect(() => {
    localStorage.setItem('counterState', JSON.stringify(state));
  }, [state]);

  return (
    <div>
      <p>Count: {state.count}</p>
      <p>Last action: {state.lastAction}</p>
      {state.error && <p className="error">{state.error}</p>}
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'incrementBy', payload: 5 })}>+5</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

### useMemo and useCallback: When to Use

```tsx
// useMemo: Memoize expensive computations
const expensiveValue = useMemo(() => {
  return items.filter(item => item.price > 100)
              .sort((a, b) => b.price - a.price)
              .slice(0, 10);
}, [items]);

// useMemo: Memoize object/array to prevent child re-renders
const memoizedOptions = useMemo(() => ({
  sortBy: 'price',
  order: 'desc',
  limit: 10,
}), []); // Empty deps = never changes

// useCallback: Memoize function identity
const handleSubmit = useCallback((values: FormValues) => {
  api.submitForm(userId, values);
}, [userId]);

// useCallback: For event handlers passed to memoized children
const MemoizedChild = React.memo(({ onClick }: { onClick: () => void }) => {
  console.log('Child rendered');
  return <button onClick={onClick}>Click</button>;
});

function Parent() {
  // Without useCallback, MemoizedChild re-renders every time
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <MemoizedChild onClick={handleClick} />;
}

// When NOT to use useMemo/useCallback:
// - Simple calculations (overhead > benefit)
// - Values/functions not passed to children
// - Components that always re-render anyway
```

### useRef: Complete Patterns

```tsx
// DOM reference
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => inputRef.current?.focus(), []);

// Store previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}

// Store mutable value that doesn't trigger re-renders
function useRenderCount() {
  const countRef = useRef(0);
  countRef.current += 1;
  return countRef.current;
}

// Store interval/timeout ID
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}

// Store abort controller
function useFetchWithAbort(url: string) {
  const abortControllerRef = useRef<AbortController>();

  useEffect(() => {
    abortControllerRef.current?.abort();
    abortControllerRef.current = new AbortController();

    fetch(url, { signal: abortControllerRef.current.signal })
      .then(res => res.json())
      .then(setData)
      .catch(err => {
        if (err.name !== 'AbortError') setError(err);
      });

    return () => abortControllerRef.current?.abort();
  }, [url]);
}
```

### Custom Hooks Library

```tsx
// useLocalStorage: Persist state to localStorage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('useLocalStorage error:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// useDebounce: Debounce a value
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// useMediaQuery: Responsive design hook
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(
    () => window.matchMedia(query).matches
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// useOnClickOutside: Detect clicks outside element
function useOnClickOutside<T extends HTMLElement>(
  ref: RefObject<T>,
  handler: (event: MouseEvent | TouchEvent) => void
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}

// useAsync: Handle async operations
function useAsync<T>(asyncFunction: () => Promise<T>, dependencies: any[] = []) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let isMounted = true;
    setState({ data: null, loading: true, error: null });

    asyncFunction()
      .then(data => {
        if (isMounted) setState({ data, loading: false, error: null });
      })
      .catch(error => {
        if (isMounted) setState({ data: null, loading: false, error });
      });

    return () => { isMounted = false; };
  }, dependencies);

  return state;
}
```

---

## Complete State Management Examples

### Redux Toolkit Full Implementation

```tsx
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import usersReducer from './usersSlice';
import cartReducer from './cartSlice';

export const store = configureStore({
  reducer: {
    users: usersReducer,
    cart: cartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// store/hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './index';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// store/usersSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UsersState {
  list: User[];
  loading: boolean;
  error: string | null;
  selectedUserId: string | null;
}

const initialState: UsersState = {
  list: [],
  loading: false,
  error: null,
  selectedUserId: null,
};

export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.getUsers();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createUser = createAsyncThunk(
  'users/createUser',
  async (userData: Omit<User, 'id'>, { rejectWithValue }) => {
    try {
      const response = await api.createUser(userData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const usersSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    selectUser: (state, action: PayloadAction<string>) => {
      state.selectedUserId = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createUser.fulfilled, (state, action) => {
        state.list.push(action.payload);
      });
  },
});

export const { selectUser, clearError } = usersSlice.actions;
export default usersSlice.reducer;

// Usage in component
function UsersList() {
  const dispatch = useAppDispatch();
  const { list, loading, error } = useAppSelector((state) => state.users);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading) return <Loading />;
  if (error) return <Error message={error} />;

  return (
    <ul>
      {list.map((user) => (
        <li key={user.id} onClick={() => dispatch(selectUser(user.id))}>
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

### Zustand Advanced Usage

```tsx
import create from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
}

const useCartStore = create<CartState>()(
  devtools(
    persist(
      immer((set, get) => ({
        items: [],
        total: 0,

        addItem: (item) =>
          set((state) => {
            const existing = state.items.find((i) => i.id === item.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              state.items.push({ ...item, quantity: 1 });
            }
            state.total = state.items.reduce(
              (sum, i) => sum + i.price * i.quantity,
              0
            );
          }),

        removeItem: (id) =>
          set((state) => {
            state.items = state.items.filter((i) => i.id !== id);
            state.total = state.items.reduce(
              (sum, i) => sum + i.price * i.quantity,
              0
            );
          }),

        updateQuantity: (id, quantity) =>
          set((state) => {
            const item = state.items.find((i) => i.id === id);
            if (item) {
              item.quantity = quantity;
              state.total = state.items.reduce(
                (sum, i) => sum + i.price * i.quantity,
                0
              );
            }
          }),

        clearCart: () =>
          set((state) => {
            state.items = [];
            state.total = 0;
          }),
      })),
      { name: 'cart-storage' }
    ),
    { name: 'CartStore' }
  )
);

// Selector for specific item
const selectItemQuantity = (id: string) => (state: CartState) =>
  state.items.find((i) => i.id === id)?.quantity ?? 0;

// Usage
function CartButton({ productId }: { productId: string }) {
  const quantity = useCartStore(selectItemQuantity(productId));
  const addItem = useCartStore((state) => state.addItem);

  return (
    <button onClick={() => addItem({ id: productId, name: 'Product', price: 10 })}>
      Add to Cart {quantity > 0 && `(${quantity})`}
    </button>
  );
}
```

### React Query Advanced Patterns

```tsx
import {
  useQuery,
  useMutation,
  useQueryClient,
  useInfiniteQuery,
} from '@tanstack/react-query';

// Query with refetch options
function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
    refetchOnWindowFocus: false,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

// Dependent queries
function useUserPosts(userId: string) {
  const { data: user } = useUser(userId);

  return useQuery({
    queryKey: ['posts', userId],
    queryFn: () => fetchUserPosts(userId),
    enabled: !!user, // Only run when user is loaded
  });
}

// Optimistic updates
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      await queryClient.cancelQueries({ queryKey: ['user', newUser.id] });
      const previousUser = queryClient.getQueryData(['user', newUser.id]);
      queryClient.setQueryData(['user', newUser.id], newUser);
      return { previousUser };
    },
    onError: (err, newUser, context) => {
      queryClient.setQueryData(['user', newUser.id], context?.previousUser);
    },
    onSettled: (data, error, newUser) => {
      queryClient.invalidateQueries({ queryKey: ['user', newUser.id] });
    },
  });
}

// Infinite scroll
function useInfinitePosts() {
  return useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam = 0 }) => fetchPosts({ page: pageParam, limit: 20 }),
    getNextPageParam: (lastPage, pages) => {
      return lastPage.hasMore ? pages.length : undefined;
    },
    initialPageParam: 0,
  });
}

// Usage with infinite scroll
function PostsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfinitePosts();

  return (
    <>
      {data?.pages.map((page, i) => (
        <React.Fragment key={i}>
          {page.posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </React.Fragment>
      ))}
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more'}
      </button>
    </>
  );
}
```

---

## Performance Optimization Deep Dive

### React.memo with Custom Comparison

```tsx
interface UserCardProps {
  user: User;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

// Default shallow comparison
const UserCard = React.memo(({ user, onSelect, isSelected }: UserCardProps) => {
  return (
    <div className={isSelected ? 'selected' : ''} onClick={() => onSelect(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// Custom comparison for deep equality or selective comparison
const DeepUserCard = React.memo(
  ({ user, onSelect, isSelected }: UserCardProps) => {
    return (
      <div className={isSelected ? 'selected' : ''} onClick={() => onSelect(user.id)}>
        <h3>{user.name}</h3>
        <p>{user.email}</p>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if these specific fields change
    return (
      prevProps.user.id === nextProps.user.id &&
      prevProps.user.name === nextProps.user.name &&
      prevProps.isSelected === nextProps.isSelected
    );
  }
);
```

### Bundle Analysis and Optimization

```bash
# Install analyzer
npm install --save-dev webpack-bundle-analyzer source-map-explorer

# For Create React App
npm run build
npx source-map-explorer 'build/static/js/*.js'

# For Next.js
ANALYZE=true npm run build

# Webpack config for bundle analyzer
// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: false,
    }),
  ],
};
```

### Dynamic Imports for Heavy Libraries

```tsx
// Lazy load heavy charting library
const Chart = lazy(() => import('recharts').then(mod => ({ default: mod.LineChart })));

// Lazy load moment.js with specific locale
const moment = lazy(() => import('moment').then(async (mod) => {
  await import('moment/locale/fr');
  return mod;
}));

// Preload on hover for better UX
function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const preload = () => {
    const componentMap: Record<string, () => Promise<any>> = {
      '/dashboard': () => import('./pages/Dashboard'),
      '/settings': () => import('./pages/Settings'),
    };
    componentMap[to]?.();
  };

  return (
    <Link to={to} onMouseEnter={preload} onFocus={preload}>
      {children}
    </Link>
  );
}
```

### Avoiding Re-renders

```tsx
// Problem: Inline objects cause re-renders
function Bad() {
  return <Child style={{ color: 'red' }} />; // New object every render
}

// Solution: Move outside component or useMemo
const style = { color: 'red' };
function Good() {
  return <Child style={style} />;
}

// Problem: Inline functions cause re-renders
function Bad() {
  return <Child onClick={() => console.log('clicked')} />;
}

// Solution: useCallback
function Good() {
  const handleClick = useCallback(() => console.log('clicked'), []);
  return <Child onClick={handleClick} />;
}

// Problem: Context causes all consumers to re-render
function Bad() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  return (
    <AppContext.Provider value={{ count, setCount, name, setName }}>
      {children}
    </AppContext.Provider>
  );
}

// Solution: Split contexts and memoize values
function Good() {
  const [count, setCount] = useState(0);
  const countValue = useMemo(() => ({ count, setCount }), [count]);

  const [name, setName] = useState('');
  const nameValue = useMemo(() => ({ name, setName }), [name]);

  return (
    <CountContext.Provider value={countValue}>
      <NameContext.Provider value={nameValue}>
        {children}
      </NameContext.Provider>
    </CountContext.Provider>
  );
}
```

---

## Component Pattern Templates

### Complete Functional Component Template

```tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';

// Types
interface UserCardProps {
  /** User data to display */
  user: User;
  /** Called when user is selected */
  onSelect?: (userId: string) => void;
  /** Whether the card is in selected state */
  isSelected?: boolean;
  /** Optional CSS class name */
  className?: string;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
}

interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

// Constants
const SIZE_CLASSES = {
  sm: 'p-2 text-sm',
  md: 'p-4 text-base',
  lg: 'p-6 text-lg',
} as const;

/**
 * UserCard displays user information in a card format.
 * Supports selection state and multiple size variants.
 *
 * @example
 * <UserCard
 *   user={{ id: '1', name: 'John', email: 'john@example.com' }}
 *   onSelect={(id) => console.log('Selected:', id)}
 *   size="md"
 * />
 */
export function UserCard({
  user,
  onSelect,
  isSelected = false,
  className = '',
  size = 'md',
}: UserCardProps) {
  // Memoized computed values
  const initials = useMemo(() => {
    return user.name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  }, [user.name]);

  // Event handlers
  const handleClick = useCallback(() => {
    onSelect?.(user.id);
  }, [onSelect, user.id]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onSelect?.(user.id);
      }
    },
    [onSelect, user.id]
  );

  // Derived classes
  const cardClasses = useMemo(() => {
    return [
      'user-card',
      SIZE_CLASSES[size],
      isSelected && 'user-card--selected',
      className,
    ]
      .filter(Boolean)
      .join(' ');
  }, [size, isSelected, className]);

  return (
    <article
      className={cardClasses}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      tabIndex={onSelect ? 0 : undefined}
      role={onSelect ? 'button' : undefined}
      aria-pressed={onSelect ? isSelected : undefined}
    >
      <div className="user-card__avatar">
        {user.avatar ? (
          <img src={user.avatar} alt="" aria-hidden="true" />
        ) : (
          <span aria-hidden="true">{initials}</span>
        )}
      </div>
      <div className="user-card__info">
        <h3 className="user-card__name">{user.name}</h3>
        <p className="user-card__email">{user.email}</p>
      </div>
    </article>
  );
}

// Display name for debugging
UserCard.displayName = 'UserCard';

// Default export for lazy loading
export default UserCard;
```

### Complete Compound Component Pattern

```tsx
import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  ReactNode,
} from 'react';

// Types
interface AccordionContextValue {
  expandedItems: Set<string>;
  toggleItem: (itemId: string) => void;
  allowMultiple: boolean;
}

interface AccordionProps {
  children: ReactNode;
  /** Allow multiple items to be expanded simultaneously */
  allowMultiple?: boolean;
  /** Initially expanded item IDs */
  defaultExpanded?: string[];
  /** Controlled expanded items */
  expanded?: string[];
  /** Called when expansion state changes */
  onExpandedChange?: (expanded: string[]) => void;
  className?: string;
}

interface AccordionItemProps {
  children: ReactNode;
  /** Unique identifier for this item */
  itemId: string;
  /** Disable this item */
  disabled?: boolean;
  className?: string;
}

interface AccordionTriggerProps {
  children: ReactNode;
  className?: string;
}

interface AccordionContentProps {
  children: ReactNode;
  className?: string;
}

// Context
const AccordionContext = createContext<AccordionContextValue | undefined>(undefined);
const AccordionItemContext = createContext<{ itemId: string; disabled: boolean } | undefined>(undefined);

// Hooks
function useAccordion() {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error('Accordion components must be used within an Accordion');
  }
  return context;
}

function useAccordionItem() {
  const context = useContext(AccordionItemContext);
  if (!context) {
    throw new Error('AccordionItem components must be used within an AccordionItem');
  }
  return context;
}

// Components
export function Accordion({
  children,
  allowMultiple = false,
  defaultExpanded = [],
  expanded: controlledExpanded,
  onExpandedChange,
  className = '',
}: AccordionProps) {
  const [internalExpanded, setInternalExpanded] = useState<Set<string>>(
    () => new Set(defaultExpanded)
  );

  const isControlled = controlledExpanded !== undefined;
  const expandedItems = isControlled
    ? new Set(controlledExpanded)
    : internalExpanded;

  const toggleItem = useCallback(
    (itemId: string) => {
      const newExpanded = new Set(expandedItems);

      if (newExpanded.has(itemId)) {
        newExpanded.delete(itemId);
      } else {
        if (!allowMultiple) {
          newExpanded.clear();
        }
        newExpanded.add(itemId);
      }

      if (!isControlled) {
        setInternalExpanded(newExpanded);
      }
      onExpandedChange?.(Array.from(newExpanded));
    },
    [expandedItems, allowMultiple, isControlled, onExpandedChange]
  );

  const value = useMemo(
    () => ({ expandedItems, toggleItem, allowMultiple }),
    [expandedItems, toggleItem, allowMultiple]
  );

  return (
    <AccordionContext.Provider value={value}>
      <div className={`accordion ${className}`} role="presentation">
        {children}
      </div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({
  children,
  itemId,
  disabled = false,
  className = '',
}: AccordionItemProps) {
  const { expandedItems } = useAccordion();
  const isExpanded = expandedItems.has(itemId);

  const value = useMemo(() => ({ itemId, disabled }), [itemId, disabled]);

  return (
    <AccordionItemContext.Provider value={value}>
      <div
        className={`accordion-item ${isExpanded ? 'accordion-item--expanded' : ''} ${className}`}
        data-state={isExpanded ? 'open' : 'closed'}
      >
        {children}
      </div>
    </AccordionItemContext.Provider>
  );
};

Accordion.Trigger = function AccordionTrigger({
  children,
  className = '',
}: AccordionTriggerProps) {
  const { toggleItem, expandedItems } = useAccordion();
  const { itemId, disabled } = useAccordionItem();
  const isExpanded = expandedItems.has(itemId);

  const handleClick = useCallback(() => {
    if (!disabled) {
      toggleItem(itemId);
    }
  }, [disabled, toggleItem, itemId]);

  return (
    <button
      type="button"
      className={`accordion-trigger ${className}`}
      onClick={handleClick}
      disabled={disabled}
      aria-expanded={isExpanded}
      aria-controls={`accordion-content-${itemId}`}
      id={`accordion-trigger-${itemId}`}
    >
      {children}
      <span className="accordion-icon" aria-hidden="true">
        {isExpanded ? '-' : '+'}
      </span>
    </button>
  );
};

Accordion.Content = function AccordionContent({
  children,
  className = '',
}: AccordionContentProps) {
  const { expandedItems } = useAccordion();
  const { itemId } = useAccordionItem();
  const isExpanded = expandedItems.has(itemId);

  return (
    <div
      id={`accordion-content-${itemId}`}
      className={`accordion-content ${className}`}
      role="region"
      aria-labelledby={`accordion-trigger-${itemId}`}
      hidden={!isExpanded}
    >
      {isExpanded && children}
    </div>
  );
};

// Usage example:
// <Accordion allowMultiple defaultExpanded={['item-1']}>
//   <Accordion.Item itemId="item-1">
//     <Accordion.Trigger>Section 1</Accordion.Trigger>
//     <Accordion.Content>Content 1</Accordion.Content>
//   </Accordion.Item>
//   <Accordion.Item itemId="item-2">
//     <Accordion.Trigger>Section 2</Accordion.Trigger>
//     <Accordion.Content>Content 2</Accordion.Content>
//   </Accordion.Item>
// </Accordion>
```

---

## Comprehensive Testing Patterns

### Component Testing Template

```tsx
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

// Test utilities
const mockUser = {
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
};

const renderUserCard = (props = {}) => {
  const defaultProps = {
    user: mockUser,
    onSelect: jest.fn(),
  };
  return {
    ...render(<UserCard {...defaultProps} {...props} />),
    user: userEvent.setup(),
  };
};

describe('UserCard', () => {
  describe('rendering', () => {
    it('displays user name and email', () => {
      renderUserCard();

      expect(screen.getByRole('heading', { name: 'John Doe' })).toBeInTheDocument();
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });

    it('shows initials when no avatar is provided', () => {
      renderUserCard();

      expect(screen.getByText('JD')).toBeInTheDocument();
    });

    it('shows avatar image when provided', () => {
      renderUserCard({
        user: { ...mockUser, avatar: 'https://example.com/avatar.jpg' },
      });

      expect(screen.getByRole('img')).toHaveAttribute('src', 'https://example.com/avatar.jpg');
    });

    it('applies size class correctly', () => {
      const { container } = renderUserCard({ size: 'lg' });

      expect(container.firstChild).toHaveClass('p-6', 'text-lg');
    });
  });

  describe('interaction', () => {
    it('calls onSelect when clicked', async () => {
      const onSelect = jest.fn();
      const { user } = renderUserCard({ onSelect });

      await user.click(screen.getByRole('button'));

      expect(onSelect).toHaveBeenCalledWith('1');
      expect(onSelect).toHaveBeenCalledTimes(1);
    });

    it('calls onSelect when Enter is pressed', async () => {
      const onSelect = jest.fn();
      const { user } = renderUserCard({ onSelect });

      await user.tab();
      await user.keyboard('{Enter}');

      expect(onSelect).toHaveBeenCalledWith('1');
    });

    it('calls onSelect when Space is pressed', async () => {
      const onSelect = jest.fn();
      const { user } = renderUserCard({ onSelect });

      await user.tab();
      await user.keyboard(' ');

      expect(onSelect).toHaveBeenCalledWith('1');
    });
  });

  describe('accessibility', () => {
    it('has correct ARIA attributes when selectable', () => {
      renderUserCard({ isSelected: true });

      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-pressed', 'true');
    });

    it('is focusable when selectable', async () => {
      const { user } = renderUserCard();

      await user.tab();

      expect(screen.getByRole('button')).toHaveFocus();
    });

    it('is not focusable when not selectable', () => {
      renderUserCard({ onSelect: undefined });

      expect(screen.queryByRole('button')).not.toBeInTheDocument();
    });
  });
});
```

### Async Testing Patterns

```tsx
import { render, screen, waitFor, waitForElementToBeRemoved } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';
import * as api from '../api';

// Mock API module
jest.mock('../api');
const mockedApi = api as jest.Mocked<typeof api>;

describe('UserProfile', () => {
  const mockUser = { id: '1', name: 'Jane Doe', email: 'jane@example.com' };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('displays loading state initially', () => {
    mockedApi.getUser.mockReturnValue(new Promise(() => {})); // Never resolves

    render(<UserProfile userId="1" />);

    expect(screen.getByRole('status')).toHaveTextContent(/loading/i);
  });

  it('displays user data after loading', async () => {
    mockedApi.getUser.mockResolvedValue(mockUser);

    render(<UserProfile userId="1" />);

    // Wait for loading to disappear
    await waitForElementToBeRemoved(() => screen.queryByRole('status'));

    // Assert user data is displayed
    expect(screen.getByText('Jane Doe')).toBeInTheDocument();
    expect(screen.getByText('jane@example.com')).toBeInTheDocument();
  });

  it('displays error state on API failure', async () => {
    mockedApi.getUser.mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId="1" />);

    const errorAlert = await screen.findByRole('alert');
    expect(errorAlert).toHaveTextContent(/network error/i);
  });

  it('refetches when userId changes', async () => {
    mockedApi.getUser.mockResolvedValue(mockUser);

    const { rerender } = render(<UserProfile userId="1" />);
    await waitFor(() => expect(mockedApi.getUser).toHaveBeenCalledWith('1'));

    rerender(<UserProfile userId="2" />);
    await waitFor(() => expect(mockedApi.getUser).toHaveBeenCalledWith('2'));

    expect(mockedApi.getUser).toHaveBeenCalledTimes(2);
  });

  it('handles form submission correctly', async () => {
    const user = userEvent.setup();
    mockedApi.updateUser.mockResolvedValue({ ...mockUser, name: 'Updated Name' });
    mockedApi.getUser.mockResolvedValue(mockUser);

    render(<UserProfile userId="1" />);
    await screen.findByText('Jane Doe');

    // Open edit mode
    await user.click(screen.getByRole('button', { name: /edit/i }));

    // Change name
    const nameInput = screen.getByLabelText(/name/i);
    await user.clear(nameInput);
    await user.type(nameInput, 'Updated Name');

    // Submit
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Assert API called with correct data
    await waitFor(() => {
      expect(mockedApi.updateUser).toHaveBeenCalledWith('1', {
        name: 'Updated Name',
        email: 'jane@example.com',
      });
    });
  });
});
```

### Testing Custom Hooks

```tsx
import { renderHook, act, waitFor } from '@testing-library/react';
import { useCounter } from './useCounter';
import { useFetch } from './useFetch';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(5);
  });
});

describe('useFetch', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('returns loading state initially', () => {
    (global.fetch as jest.Mock).mockReturnValue(new Promise(() => {}));

    const { result } = renderHook(() => useFetch('/api/data'));

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeNull();
    expect(result.current.error).toBeNull();
  });

  it('returns data on successful fetch', async () => {
    const mockData = { id: 1, name: 'Test' };
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    });

    const { result } = renderHook(() => useFetch('/api/data'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual(mockData);
    expect(result.current.error).toBeNull();
  });

  it('returns error on failed fetch', async () => {
    (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useFetch('/api/data'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBeNull();
    expect(result.current.error).toEqual(new Error('Network error'));
  });

  it('refetches when URL changes', async () => {
    const mockData1 = { id: 1 };
    const mockData2 = { id: 2 };
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockData1) })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockData2) });

    const { result, rerender } = renderHook(
      ({ url }) => useFetch(url),
      { initialProps: { url: '/api/data/1' } }
    );

    await waitFor(() => expect(result.current.data).toEqual(mockData1));

    rerender({ url: '/api/data/2' });

    await waitFor(() => expect(result.current.data).toEqual(mockData2));
    expect(global.fetch).toHaveBeenCalledTimes(2);
  });
});
```

### Integration Testing with MSW

```tsx
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserDashboard } from './UserDashboard';

// Setup MSW server
const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: '1', name: 'John', email: 'john@example.com' },
        { id: '2', name: 'Jane', email: 'jane@example.com' },
      ])
    );
  }),
  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json();
    return res(
      ctx.json({ id: '3', ...body })
    );
  }),
  rest.delete('/api/users/:id', (req, res, ctx) => {
    return res(ctx.status(204));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Test wrapper with providers
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('UserDashboard Integration', () => {
  it('displays list of users', async () => {
    render(<UserDashboard />, { wrapper: createWrapper() });

    expect(await screen.findByText('John')).toBeInTheDocument();
    expect(screen.getByText('Jane')).toBeInTheDocument();
  });

  it('creates a new user', async () => {
    const user = userEvent.setup();
    render(<UserDashboard />, { wrapper: createWrapper() });

    await screen.findByText('John');

    await user.click(screen.getByRole('button', { name: /add user/i }));
    await user.type(screen.getByLabelText(/name/i), 'New User');
    await user.type(screen.getByLabelText(/email/i), 'new@example.com');
    await user.click(screen.getByRole('button', { name: /save/i }));

    expect(await screen.findByText('New User')).toBeInTheDocument();
  });

  it('handles server error gracefully', async () => {
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ message: 'Server error' }));
      })
    );

    render(<UserDashboard />, { wrapper: createWrapper() });

    expect(await screen.findByRole('alert')).toHaveTextContent(/error/i);
  });
});
```

---

## Full Accessibility Checklist

### WCAG 2.1 AA Requirements

#### Perceivable

- [ ] **1.1.1 Non-text Content**: All images have alt text
- [ ] **1.3.1 Info and Relationships**: Use semantic HTML (header, nav, main, footer)
- [ ] **1.3.2 Meaningful Sequence**: DOM order matches visual order
- [ ] **1.3.4 Orientation**: Content works in both portrait and landscape
- [ ] **1.4.1 Use of Color**: Color is not the only visual means of conveying information
- [ ] **1.4.3 Contrast (Minimum)**: Text has 4.5:1 contrast ratio (3:1 for large text)
- [ ] **1.4.4 Resize Text**: Text can be resized up to 200% without loss of functionality
- [ ] **1.4.10 Reflow**: Content reflows without horizontal scrolling at 320px width
- [ ] **1.4.11 Non-text Contrast**: UI components have 3:1 contrast ratio
- [ ] **1.4.12 Text Spacing**: No loss of content when adjusting text spacing

#### Operable

- [ ] **2.1.1 Keyboard**: All functionality is keyboard accessible
- [ ] **2.1.2 No Keyboard Trap**: Focus can be moved away from any component
- [ ] **2.4.1 Bypass Blocks**: Skip link to main content
- [ ] **2.4.2 Page Titled**: Pages have descriptive titles
- [ ] **2.4.3 Focus Order**: Focus order is logical and intuitive
- [ ] **2.4.4 Link Purpose**: Link text is descriptive (avoid "click here")
- [ ] **2.4.6 Headings and Labels**: Headings and labels are descriptive
- [ ] **2.4.7 Focus Visible**: Focus indicator is visible
- [ ] **2.5.3 Label in Name**: Visible labels match accessible names

#### Understandable

- [ ] **3.1.1 Language of Page**: HTML lang attribute is set
- [ ] **3.2.1 On Focus**: No unexpected changes on focus
- [ ] **3.2.2 On Input**: No unexpected changes on input
- [ ] **3.3.1 Error Identification**: Errors are identified and described
- [ ] **3.3.2 Labels or Instructions**: Form inputs have labels
- [ ] **3.3.3 Error Suggestion**: Error messages suggest corrections
- [ ] **3.3.4 Error Prevention**: Confirm destructive actions

#### Robust

- [ ] **4.1.1 Parsing**: Valid HTML
- [ ] **4.1.2 Name, Role, Value**: Custom controls have accessible names and roles
- [ ] **4.1.3 Status Messages**: Status messages are announced by screen readers

### Accessibility Testing Tools

```bash
# Browser extensions
- axe DevTools (Chrome/Firefox)
- WAVE Evaluation Tool
- Accessibility Insights for Web

# Automated testing
npm install --save-dev @axe-core/react jest-axe

# In tests
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('component has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

# CI integration
npm install --save-dev @axe-core/cli
npx axe https://example.com --tags wcag2a,wcag2aa
```

---

## Security Best Practices

### XSS Prevention

```tsx
// React automatically escapes - safe by default
<div>{userInput}</div>

// Dangerous - only use with sanitized content
<div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />

// Always sanitize if dangerouslySetInnerHTML is needed
import DOMPurify from 'dompurify';

function SafeHTML({ html }: { html: string }) {
  const sanitized = useMemo(() => DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target', 'rel'],
  }), [html]);

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// URL validation
function SafeLink({ href, children }: { href: string; children: React.ReactNode }) {
  const isSafe = useMemo(() => {
    try {
      const url = new URL(href);
      return ['http:', 'https:'].includes(url.protocol);
    } catch {
      return false;
    }
  }, [href]);

  if (!isSafe) {
    return <span>{children}</span>;
  }

  return (
    <a href={href} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  );
}
```

### Secure Authentication

```tsx
// Auth context with secure patterns
interface AuthContextValue {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (credentials: Credentials) => {
    // Never log credentials
    const response = await api.login(credentials);

    // Token should be in httpOnly cookie (set by server)
    // Only store non-sensitive user data in state
    setUser(response.user);
  }, []);

  const logout = useCallback(async () => {
    await api.logout(); // Server clears httpOnly cookie
    setUser(null);
    // Clear any sensitive data from memory
    window.sessionStorage.clear();
  }, []);

  // Auto-logout on token expiry
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.checkAuth();
        setUser(response.user);
      } catch {
        setUser(null);
      }
    };

    checkAuth();
    const interval = setInterval(checkAuth, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const value = useMemo(
    () => ({
      user,
      login,
      logout,
      isAuthenticated: !!user,
    }),
    [user, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Protected route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
```

---

## Production Configuration

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
    '!src/reportWebVitals.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testMatch: ['**/__tests__/**/*.test.{ts,tsx}', '**/*.test.{ts,tsx}'],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },
};

// jest.setup.js
import '@testing-library/jest-dom';
import { server } from './src/mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'prettier',
  ],
  plugins: ['@typescript-eslint', 'react', 'react-hooks', 'jsx-a11y'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'jsx-a11y/anchor-is-valid': [
      'error',
      {
        components: ['Link'],
        specialLink: ['to'],
      },
    ],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src",
    "paths": {
      "@/*": ["*"],
      "@components/*": ["components/*"],
      "@hooks/*": ["hooks/*"],
      "@utils/*": ["utils/*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

---

## Related Resources

- [Main SKILL.md](./SKILL.md) - Core concepts and quick reference
- [React Documentation](https://react.dev/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://github.com/pmndrs/zustand)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
