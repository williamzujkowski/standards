import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderHook, act } from '@testing-library/react';
import '@testing-library/jest-dom';

/**
 * React Testing Library Template
 *
 * Demonstrates user-centric testing patterns following RTL best practices.
 * Focus on testing behavior, not implementation details.
 */

// ============================================================================
// Example Component to Test
// ============================================================================

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  onForgotPassword: () => void;
}

function LoginForm({ onSubmit, onForgotPassword }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onSubmit(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Login form">
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      {error && <div role="alert">{error}</div>}

      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Log in'}
      </button>

      <button type="button" onClick={onForgotPassword}>
        Forgot password?
      </button>
    </form>
  );
}

// ============================================================================
// Basic Component Tests
// ============================================================================

describe('LoginForm', () => {
  it('renders login form with all fields', () => {
    const mockSubmit = jest.fn();
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    // Query by accessible roles and labels
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /forgot password/i })).toBeInTheDocument();
  });

  it('allows user to type in email and password fields', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn();
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    // Simulate user typing
    await user.type(emailInput, 'user@example.com');
    await user.type(passwordInput, 'password123');

    expect(emailInput).toHaveValue('user@example.com');
    expect(passwordInput).toHaveValue('password123');
  });

  it('calls onSubmit with email and password when form is submitted', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn().mockResolvedValue(undefined);
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    // Fill form
    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Submit form
    await user.click(screen.getByRole('button', { name: /log in/i }));

    // Assert callback was called with correct values
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith('user@example.com', 'password123');
      expect(mockSubmit).toHaveBeenCalledTimes(1);
    });
  });

  it('displays error message when login fails', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn().mockRejectedValue(new Error('Invalid credentials'));
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /log in/i }));

    // Error message should appear
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Invalid credentials');
  });

  it('shows loading state during submission', async () => {
    const user = userEvent.setup();
    let resolveSubmit: () => void;
    const mockSubmit = jest.fn(() => new Promise<void>(resolve => {
      resolveSubmit = resolve;
    }));
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    const submitButton = screen.getByRole('button', { name: /log in/i });
    await user.click(submitButton);

    // Button should show loading state
    expect(screen.getByRole('button', { name: /logging in/i })).toBeDisabled();
    expect(screen.getByLabelText(/email/i)).toBeDisabled();

    // Resolve promise
    act(() => {
      resolveSubmit!();
    });

    // Loading state should be gone
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /log in/i })).not.toBeDisabled();
    });
  });

  it('calls onForgotPassword when forgot password button is clicked', async () => {
    const user = userEvent.setup();
    const mockSubmit = jest.fn();
    const mockForgotPassword = jest.fn();

    render(<LoginForm onSubmit={mockSubmit} onForgotPassword={mockForgotPassword} />);

    await user.click(screen.getByRole('button', { name: /forgot password/i }));

    expect(mockForgotPassword).toHaveBeenCalledTimes(1);
  });
});

// ============================================================================
// Testing Async Components
// ============================================================================

interface UserListProps {
  userId: string;
}

function UserList({ userId }: UserListProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/users?id=${userId}`)
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div role="alert">Error: {error}</div>;
  if (users.length === 0) return <div>No users found</div>;

  return (
    <ul aria-label="User list">
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

describe('UserList - Async', () => {
  beforeEach(() => {
    // Mock fetch
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('shows loading state initially', () => {
    (global.fetch as jest.Mock).mockImplementation(() => new Promise(() => {}));

    render(<UserList userId="123" />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays users after successful fetch', async () => {
    const mockUsers = [
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ];

    (global.fetch as jest.Mock).mockResolvedValue({
      json: async () => mockUsers,
    });

    render(<UserList userId="123" />);

    // Wait for users to appear
    const alice = await screen.findByText('Alice');
    const bob = await screen.findByText('Bob');

    expect(alice).toBeInTheDocument();
    expect(bob).toBeInTheDocument();
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('displays error when fetch fails', async () => {
    (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(<UserList userId="123" />);

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Error: Network error');
  });

  it('displays empty state when no users', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      json: async () => [],
    });

    render(<UserList userId="123" />);

    const emptyMessage = await screen.findByText(/no users found/i);
    expect(emptyMessage).toBeInTheDocument();
  });
});

// ============================================================================
// Testing Custom Hooks
// ============================================================================

function useCounter(initialValue: number = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);

  return { count, increment, decrement, reset };
}

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
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
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});

// ============================================================================
// Testing with Context
// ============================================================================

const ThemeContext = createContext<{ theme: string; toggleTheme: () => void } | undefined>(undefined);

function ThemeToggle() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('Must be used within ThemeProvider');

  return (
    <div>
      <p>Current theme: {context.theme}</p>
      <button onClick={context.toggleTheme}>Toggle theme</button>
    </div>
  );
}

describe('ThemeToggle - With Context', () => {
  it('displays current theme and allows toggling', async () => {
    const user = userEvent.setup();
    const mockToggle = jest.fn();

    render(
      <ThemeContext.Provider value={{ theme: 'light', toggleTheme: mockToggle }}>
        <ThemeToggle />
      </ThemeContext.Provider>
    );

    expect(screen.getByText(/current theme: light/i)).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /toggle theme/i }));

    expect(mockToggle).toHaveBeenCalledTimes(1);
  });
});

/**
 * React Testing Library Best Practices:
 *
 * 1. Query by accessibility (role, label, text) not test IDs
 * 2. Use userEvent for realistic interactions
 * 3. Test user behavior, not implementation
 * 4. Wait for async updates with waitFor/findBy
 * 5. Mock external dependencies (API calls, timers)
 * 6. Use act() for state updates in hooks
 * 7. Clean up after each test (afterEach)
 * 8. Test loading, error, and success states
 * 9. Prefer integration tests over unit tests
 * 10. Aim for 80%+ coverage on components
 *
 * Query Priority (from RTL docs):
 * 1. getByRole (most accessible)
 * 2. getByLabelText (forms)
 * 3. getByPlaceholderText (forms)
 * 4. getByText (non-interactive)
 * 5. getByDisplayValue (current value)
 * 6. getByAltText (images)
 * 7. getByTitle (last resort)
 * 8. getByTestId (avoid if possible)
 */
