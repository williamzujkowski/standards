---
name: react-frontend
description: React frontend standards covering hooks (useState, useEffect, useContext, custom hooks), state management (Context API, Redux, Zustand), performance optimization (memoization, lazy loading, code splitting), testing with React Testing Library, and accessibility (WCAG 2.1, ARIA) for modern SPAs
tags: [frontend, react, hooks, state-management, performance, accessibility, testing]
category: frontend
difficulty: intermediate
estimated_time: 45 minutes
prerequisites: [javascript-coding-standards, html-css-standards]
related_skills: [typescript-coding-standards, testing-standards, web-accessibility]
wcag_level: AA
---

# React Frontend Development Standards

## Level 1: Quick Reference (5-10 minutes)

### Hook Patterns Quick Reference

```tsx
// State Hook
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Effect Hook
useEffect(() => {
  // Side effect
  return () => {/* cleanup */};
}, [dependencies]);

// Context Hook
const theme = useContext(ThemeContext);

// Ref Hook
const inputRef = useRef<HTMLInputElement>(null);

// Memo Hooks
const value = useMemo(() => expensiveCalc(a, b), [a, b]);
const callback = useCallback(() => doSomething(a), [a]);
```

### State Management Decision Tree

```
Start
  ↓
Is state needed in >2 components?
  NO → Use local state (useState)
  YES ↓
Is it global UI state (theme, auth)?
  YES → Use Context API
  NO ↓
Is it server data (API responses)?
  YES → Use React Query/TanStack Query
  NO ↓
Complex state with many actions?
  YES → Use Redux Toolkit or Zustand
  NO → Use Context API + useReducer
```

### Component Checklist

- [ ] Use functional components with hooks
- [ ] Destructure props with TypeScript types
- [ ] Use semantic HTML elements
- [ ] Add proper ARIA labels where needed
- [ ] Implement keyboard navigation support
- [ ] Memoize expensive computations with useMemo
- [ ] Memoize callbacks passed to children with useCallback
- [ ] Add loading and error states
- [ ] Handle edge cases (empty states, no data)
- [ ] Write tests with React Testing Library
- [ ] Ensure 4.5:1 color contrast ratio
- [ ] Add alt text to images
- [ ] Use proper form validation
- [ ] Clean up effects with return function
- [ ] Keep components under 300 lines

### Performance Optimization Checklist

- [ ] Use React.lazy() for code splitting
- [ ] Wrap expensive components in React.memo()
- [ ] Use useMemo for expensive calculations
- [ ] Use useCallback for functions passed to children
- [ ] Implement virtual scrolling for long lists
- [ ] Lazy load images with loading="lazy"
- [ ] Analyze bundle size (webpack-bundle-analyzer)
- [ ] Avoid inline object/array creation in JSX
- [ ] Use production build for deployment
- [ ] Enable compression (gzip/brotli)

### Accessibility Quick Wins

```tsx
// Semantic HTML
<nav><header><main><article><footer>

// ARIA labels
<button aria-label="Close dialog">×</button>

// Keyboard navigation
onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}

// Focus management
useEffect(() => inputRef.current?.focus(), []);

// Form labels
<label htmlFor="email">Email</label>
<input id="email" />

// Error announcements
<div role="alert">{error}</div>
```

### Quick Start Guide

```bash
# Create React app with TypeScript
npx create-react-app my-app --template typescript

# Install testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Install React Query for server state
npm install @tanstack/react-query

# Install state management (choose one)
npm install zustand  # Lightweight
npm install @reduxjs/toolkit react-redux  # Enterprise
```

---

## Level 2: Comprehensive Standards (30-45 minutes)

### React Hooks

#### useState: Simple State Management

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
```

#### useEffect: Side Effects and Lifecycle

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

// Common patterns
useEffect(() => {
  let isMounted = true;

  async function fetchData() {
    const result = await api.getData();
    if (isMounted) setData(result);
  }

  fetchData();
  return () => { isMounted = false; };
}, []);
```

#### useContext: Global State Access

```tsx
// Create context
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider component
export const ThemeProvider: FC<PropsWithChildren> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook for consuming context
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

#### useReducer: Complex State Management

```tsx
interface State {
  count: number;
  history: number[];
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return {
        count: state.count + 1,
        history: [...state.history, state.count + 1]
      };
    case 'decrement':
      return {
        count: state.count - 1,
        history: [...state.history, state.count - 1]
      };
    case 'reset':
      return { count: 0, history: [] };
    default:
      return state;
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0, history: [] });
```

#### useMemo and useCallback: Performance Optimization

```tsx
// useMemo: Memoize expensive computations
const expensiveValue = useMemo(() => {
  return items.filter(item => item.price > 100)
              .sort((a, b) => b.price - a.price);
}, [items]);

// useCallback: Memoize function identity
const handleSubmit = useCallback((values: FormValues) => {
  api.submitForm(userId, values);
}, [userId]);

// When to use:
// - useMemo: Expensive calculations, object/array creation in render
// - useCallback: Functions passed to memoized children, effect dependencies
```

#### useRef: DOM Access and Mutable Values

```tsx
// DOM reference
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => inputRef.current?.focus(), []);

// Store previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => { ref.current = value; });
  return ref.current;
}

// Store mutable value that doesn't trigger re-renders
const countRef = useRef(0);
countRef.current += 1; // No re-render
```

#### Custom Hooks: Reusable Logic

```tsx
// Always prefix with 'use'
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (isMounted) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (isMounted) {
          setError(err);
          setLoading(false);
        }
      });

    return () => { isMounted = false; };
  }, [url]);

  return { data, loading, error };
}

// Usage
const { data, loading, error } = useFetch<User>('/api/user');
```

### State Management

#### When to Use Context API

```tsx
// Good for: Theme, auth, localization, UI preferences
// Avoid for: Frequently changing data (causes many re-renders)

interface AppContextType {
  user: User | null;
  theme: 'light' | 'dark';
  locale: string;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Optimize with multiple contexts to reduce re-renders
<AuthProvider>
  <ThemeProvider>
    <LocaleProvider>
      <App />
    </LocaleProvider>
  </ThemeProvider>
</AuthProvider>
```

#### Redux Toolkit: Modern Redux

```tsx
// Create slice
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async () => {
    const response = await api.getUsers();
    return response.data;
  }
);

const usersSlice = createSlice({
  name: 'users',
  initialState: { list: [], loading: false, error: null },
  reducers: {
    addUser: (state, action) => {
      state.list.push(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});
```

#### Zustand: Lightweight Alternative

```tsx
import create from 'zustand';

interface BearState {
  bears: number;
  increase: () => void;
  reset: () => void;
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  reset: () => set({ bears: 0 }),
}));

// Usage (no Provider needed!)
const bears = useBearStore((state) => state.bears);
```

#### Server State vs Client State

```tsx
// Server state: Use React Query/TanStack Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  // React Query handles: caching, refetching, loading states, errors
}

// Client state: Use useState/Context/Zustand
// Examples: Form inputs, UI toggles, filters, modals
```

### Performance Optimization

#### React.memo: Component Memoization

```tsx
// Only re-render when props change
const ExpensiveComponent = React.memo(({ data }: Props) => {
  return <div>{/* Expensive render */}</div>;
});

// Custom comparison
const MyComponent = React.memo(
  ({ user }: { user: User }) => <div>{user.name}</div>,
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
);
```

#### Code Splitting and Lazy Loading

```tsx
// Route-based code splitting
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Suspense>
  );
}

// Component-based lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'));

<Suspense fallback={<Skeleton />}>
  {showChart && <HeavyChart data={data} />}
</Suspense>
```

#### Virtual Scrolling for Long Lists

```tsx
// Use react-window or react-virtualized
import { FixedSizeList } from 'react-window';

const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
  <div style={style}>Row {index}</div>
);

<FixedSizeList
  height={600}
  itemCount={10000}
  itemSize={35}
  width="100%"
>
  {Row}
</FixedSizeList>
```

#### Bundle Size Analysis

```bash
# Install analyzer
npm install --save-dev webpack-bundle-analyzer

# Analyze build
npm run build
npx webpack-bundle-analyzer build/bundle-stats.json
```

### Component Patterns

#### Functional Components Best Practices

```tsx
// Use named exports for better tree-shaking
export function UserCard({ name, email }: UserCardProps) {
  return (
    <article className="user-card">
      <h2>{name}</h2>
      <p>{email}</p>
    </article>
  );
}

// Props with defaults
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children
}: ButtonProps) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}
```

#### Children Pattern

```tsx
interface CardProps {
  children: React.ReactNode;
  title?: string;
}

export function Card({ children, title }: CardProps) {
  return (
    <div className="card">
      {title && <h2>{title}</h2>}
      <div className="card-content">{children}</div>
    </div>
  );
}
```

#### Compound Components

```tsx
// Parent manages state, children consume via context
const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (tab: string) => void;
} | undefined>(undefined);

export function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState('tab1');
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: React.ReactNode }) {
  return <div className="tabs-list">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  return (
    <button
      onClick={() => context?.setActiveTab(id)}
      className={context?.activeTab === id ? 'active' : ''}
    >
      {children}
    </button>
  );
};

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab id="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab id="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
</Tabs>
```

### Testing with React Testing Library

#### User-Centric Testing Philosophy

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Test user interactions, not implementation details
test('user can submit form', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();

  render(<ContactForm onSubmit={onSubmit} />);

  // Query by role (accessible)
  const nameInput = screen.getByRole('textbox', { name: /name/i });
  const submitButton = screen.getByRole('button', { name: /submit/i });

  // Simulate user actions
  await user.type(nameInput, 'John Doe');
  await user.click(submitButton);

  // Assert results
  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({ name: 'John Doe' });
  });
});
```

#### Testing Async Components

```tsx
test('displays user data after loading', async () => {
  const mockUser = { id: 1, name: 'Jane' };
  jest.spyOn(api, 'getUser').mockResolvedValue(mockUser);

  render(<UserProfile userId={1} />);

  // Loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data
  const userName = await screen.findByText('Jane');
  expect(userName).toBeInTheDocument();

  // Loading state gone
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});
```

#### Testing Hooks

```tsx
import { renderHook, act } from '@testing-library/react';

test('useCounter increments', () => {
  const { result } = renderHook(() => useCounter());

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

#### Coverage Targets

- **Components**: 80%+ (focus on user interactions)
- **Hooks**: 90%+ (reusable logic needs thorough testing)
- **Utils**: 95%+ (pure functions are easy to test)

### Accessibility (WCAG 2.1 AA)

#### Semantic HTML

```tsx
// Use semantic elements, not divs everywhere
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <section>
      <h2>Section Heading</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

<footer>
  <p>&copy; 2024 Company</p>
</footer>
```

#### ARIA Labels and Roles

```tsx
// Use ARIA when semantic HTML isn't enough
<button aria-label="Close dialog" onClick={onClose}>
  ×
</button>

// Dialog pattern
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Action</h2>
  <button onClick={onConfirm}>Confirm</button>
</div>

// Live regions for dynamic updates
<div role="alert" aria-live="assertive">
  {error && <p>{error}</p>}
</div>

// Don't add ARIA when semantic HTML works
<button>Submit</button> {/* Already accessible */}
```

#### Keyboard Navigation

```tsx
function Menu() {
  const [open, setOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      setOpen(false);
      buttonRef.current?.focus(); // Return focus
    }
  };

  return (
    <>
      <button
        ref={buttonRef}
        aria-expanded={open}
        aria-haspopup="true"
        onClick={() => setOpen(!open)}
      >
        Menu
      </button>
      {open && (
        <ul role="menu" onKeyDown={handleKeyDown}>
          <li role="menuitem" tabIndex={0}>Item 1</li>
          <li role="menuitem" tabIndex={0}>Item 2</li>
        </ul>
      )}
    </>
  );
}
```

#### Color Contrast

```tsx
// WCAG AA requires 4.5:1 for normal text, 3:1 for large text

// Good (7:1 contrast)
<p style={{ color: '#000', backgroundColor: '#fff' }}>Text</p>

// Bad (2.1:1 contrast)
<p style={{ color: '#999', backgroundColor: '#fff' }}>Text</p>

// Check with browser DevTools or https://webaim.org/resources/contrastchecker/
```

#### Form Accessibility

```tsx
function AccessibleForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          required
        />
        {errors.email && (
          <span id="email-error" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Security Best Practices

#### XSS Prevention

```tsx
// React escapes by default - safe
<div>{userInput}</div>

// Dangerous - avoid unless necessary
<div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />

// If needed, use DOMPurify
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirtyHTML);
```

#### Content Security Policy

```html
<!-- In index.html or server headers -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

#### Secure Token Storage

```tsx
// Store JWT in httpOnly cookie (backend sets it)
// Avoid localStorage (vulnerable to XSS)

// If you must use localStorage:
// - Implement short token expiry
// - Use refresh tokens
// - Clear on logout

function useAuth() {
  const logout = () => {
    localStorage.removeItem('token');
    // Also call API to invalidate server-side
    api.logout();
  };

  return { logout };
}
```

---

## Level 3: Resources

See bundled resources in `skills/frontend/react/`:

- `templates/functional-component.tsx` - Complete component template
- `templates/custom-hook.tsx` - Custom hook pattern
- `templates/component.test.tsx` - Testing template
- `resources/performance-checklist.md` - Performance optimization guide
- `resources/accessibility-checklist.md` - WCAG 2.1 AA compliance
- `config/jest.config.js` - Jest configuration for React + TypeScript

## Examples

### Basic Usage

```javascript
// TODO: Add basic example for react
// This example demonstrates core functionality
```

### Advanced Usage

```javascript
// TODO: Add advanced example for react
// This example shows production-ready patterns
```

### Integration Example

```javascript
// TODO: Add integration example showing how react
// works with other systems and services
```

See `examples/react/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: React, Redux, React Router, Jest
- **Prerequisites**: Basic understanding of frontend concepts

### Downstream Consumers

- **Applications**: Production systems requiring react functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- [Typescript](../../typescript/SKILL.md)
- [Unit Testing](../../unit-testing/SKILL.md)
- [E2E Testing](../../e2e-testing/SKILL.md)

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for react
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

---

## Summary

React development focuses on:

1. **Hooks mastery** for state and side effects
2. **Appropriate state management** (local → Context → external library)
3. **Performance optimization** with memoization and code splitting
4. **User-centric testing** with React Testing Library
5. **Accessibility** (WCAG 2.1 AA) with semantic HTML and ARIA
6. **Security** through XSS prevention and secure auth patterns

For detailed examples, see the bundled resources above.
