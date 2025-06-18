# Frontend and Mobile Development Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** FE

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Frontend Architecture Standards](#1-frontend-architecture-standards)
2. [React/Vue/Angular Standards](#2-reactvueangular-standards)
3. [State Management](#3-state-management)
4. [Performance and Optimization](#4-performance-and-optimization)
5. [Progressive Web Apps (PWA)](#5-progressive-web-apps-pwa)
6. [Mobile Development Standards](#6-mobile-development-standards)
7. [UI/UX Standards](#7-uiux-standards)
8. [Testing and Quality Assurance](#8-testing-and-quality-assurance)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Frontend Architecture Standards

### 1.1 Project Structure

#### Modern Frontend Structure **[REQUIRED]**
```
frontend-app/
├── public/                     # Static assets
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/            # Reusable UI components
│   │   ├── common/           # Generic components
│   │   ├── forms/            # Form components
│   │   └── layout/           # Layout components
│   ├── pages/                # Page-level components
│   │   ├── Home/
│   │   ├── Profile/
│   │   └── Settings/
│   ├── hooks/                # Custom React hooks
│   ├── services/             # API and external services
│   ├── store/                # State management
│   ├── utils/                # Utility functions
│   ├── types/                # TypeScript type definitions
│   ├── styles/               # Global styles and themes
│   ├── assets/               # Images, fonts, icons
│   ├── constants/            # App constants
│   └── __tests__/            # Test files
├── docs/                     # Documentation
├── scripts/                  # Build and utility scripts
├── .env.example             # Environment variables template
├── .eslintrc.js             # ESLint configuration
├── .prettierrc              # Prettier configuration
├── tsconfig.json            # TypeScript configuration
├── package.json
└── webpack.config.js        # Build configuration
```

#### Component Organization **[REQUIRED]**
```typescript
// components/Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button.types';

// components/Button/Button.types.ts
export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  'data-testid'?: string;
}

// components/Button/Button.tsx
import React from 'react';
import { ButtonProps } from './Button.types';
import { StyledButton, LoadingSpinner } from './Button.styles';

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  onClick,
  'data-testid': testId,
  ...props
}) => {
  return (
    <StyledButton
      variant={variant}
      size={size}
      disabled={disabled || loading}
      onClick={onClick}
      data-testid={testId}
      {...props}
    >
      {loading && <LoadingSpinner />}
      {children}
    </StyledButton>
  );
};

// components/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
});
```

### 1.2 TypeScript Configuration

#### Strict TypeScript Setup **[REQUIRED]**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src",
    "paths": {
      "@components/*": ["components/*"],
      "@pages/*": ["pages/*"],
      "@utils/*": ["utils/*"],
      "@types/*": ["types/*"],
      "@services/*": ["services/*"],
      "@store/*": ["store/*"]
    }
  },
  "include": [
    "src/**/*",
    "src/**/*.json"
  ],
  "exclude": [
    "node_modules",
    "build",
    "dist"
  ]
}
```

#### Type Safety Patterns **[REQUIRED]**
```typescript
// types/api.types.ts
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: UserRole;
  createdAt: string;
  updatedAt: string;
}

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator'
}

// services/api.service.ts
import { ApiResponse, User } from '@types/api.types';

class ApiService {
  private baseURL = process.env.REACT_APP_API_URL || '';

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse<T> = await response.json();
      return data;
    } catch (error) {
      throw new Error(`API request failed: ${error}`);
    }
  }

  async getUser(id: string): Promise<User> {
    const response = await this.request<User>(`/users/${id}`);
    if (!response.success) {
      throw new Error(response.message || 'Failed to fetch user');
    }
    return response.data;
  }

  async updateUser(id: string, updates: Partial<User>): Promise<User> {
    const response = await this.request<User>(`/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });

    if (!response.success) {
      throw new Error(response.message || 'Failed to update user');
    }

    return response.data;
  }
}

export const apiService = new ApiService();
```

### 1.3 Build and Bundling

#### Webpack Configuration **[REQUIRED]**
```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  mode: isProduction ? 'production' : 'development',
  entry: './src/index.tsx',

  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: isProduction
      ? '[name].[contenthash].js'
      : '[name].js',
    chunkFilename: isProduction
      ? '[name].[contenthash].chunk.js'
      : '[name].chunk.js',
    clean: true,
    publicPath: '/',
  },

  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.jsx'],
    alias: {
      '@components': path.resolve(__dirname, 'src/components'),
      '@pages': path.resolve(__dirname, 'src/pages'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@types': path.resolve(__dirname, 'src/types'),
      '@services': path.resolve(__dirname, 'src/services'),
      '@store': path.resolve(__dirname, 'src/store'),
    },
  },

  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [
          isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
          'css-loader',
          'postcss-loader',
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name].[hash][ext]',
        },
      },
    ],
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      minify: isProduction,
    }),
    ...(isProduction
      ? [
          new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
          }),
        ]
      : []
    ),
    ...(process.env.ANALYZE === 'true'
      ? [new BundleAnalyzerPlugin()]
      : []
    ),
  ],

  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },

  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    compress: true,
    port: 3000,
    historyApiFallback: true,
    hot: true,
  },
};
```

---

## 2. React/Vue/Angular Standards

### 2.1 React Standards

#### Component Patterns **[REQUIRED]**
```typescript
// Custom Hooks Pattern
import { useState, useEffect, useCallback } from 'react';
import { apiService } from '@services/api.service';
import { User } from '@types/api.types';

interface UseUserResult {
  user: User | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export const useUser = (userId: string): UseUserResult => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUser = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const userData = await apiService.getUser(userId);
      setUser(userData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch user');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return {
    user,
    loading,
    error,
    refetch: fetchUser,
  };
};

// Higher-Order Component for Error Boundary
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-fallback">
          <h2>Something went wrong.</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Compound Component Pattern
interface TabsProps {
  children: ReactNode;
  defaultTab?: string;
  onTabChange?: (tabId: string) => void;
}

interface TabListProps {
  children: ReactNode;
}

interface TabProps {
  id: string;
  children: ReactNode;
}

interface TabPanelsProps {
  children: ReactNode;
}

interface TabPanelProps {
  id: string;
  children: ReactNode;
}

const TabsContext = React.createContext<{
  activeTab: string;
  setActiveTab: (id: string) => void;
} | null>(null);

export const Tabs: React.FC<TabsProps> & {
  List: React.FC<TabListProps>;
  Tab: React.FC<TabProps>;
  Panels: React.FC<TabPanelsProps>;
  Panel: React.FC<TabPanelProps>;
} = ({ children, defaultTab, onTabChange }) => {
  const [activeTab, setActiveTab] = useState(defaultTab || '');

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    onTabChange?.(tabId);
  };

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleTabChange }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
};

Tabs.List = ({ children }) => (
  <div className="tab-list" role="tablist">{children}</div>
);

Tabs.Tab = ({ id, children }) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  const { activeTab, setActiveTab } = context;

  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={`tab ${activeTab === id ? 'active' : ''}`}
    >
      {children}
    </button>
  );
};

Tabs.Panels = ({ children }) => (
  <div className="tab-panels">{children}</div>
);

Tabs.Panel = ({ id, children }) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  const { activeTab } = context;

  if (activeTab !== id) return null;

  return (
    <div role="tabpanel" className="tab-panel">
      {children}
    </div>
  );
};
```

#### Performance Optimization **[REQUIRED]**
```typescript
// Memoization and optimization patterns
import React, { memo, useMemo, useCallback } from 'react';

interface ExpensiveListProps {
  items: Array<{ id: string; name: string; value: number }>;
  filter: string;
  onItemClick: (id: string) => void;
}

export const ExpensiveList = memo<ExpensiveListProps>(({
  items,
  filter,
  onItemClick
}) => {
  // Memoize expensive computations
  const filteredItems = useMemo(() => {
    return items.filter(item =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  const sortedItems = useMemo(() => {
    return [...filteredItems].sort((a, b) => b.value - a.value);
  }, [filteredItems]);

  // Memoize callbacks to prevent unnecessary re-renders
  const handleItemClick = useCallback((id: string) => {
    onItemClick(id);
  }, [onItemClick]);

  return (
    <div className="expensive-list">
      {sortedItems.map(item => (
        <ExpensiveListItem
          key={item.id}
          item={item}
          onClick={handleItemClick}
        />
      ))}
    </div>
  );
});

// Separate component for individual items
interface ExpensiveListItemProps {
  item: { id: string; name: string; value: number };
  onClick: (id: string) => void;
}

const ExpensiveListItem = memo<ExpensiveListItemProps>(({ item, onClick }) => {
  const handleClick = useCallback(() => {
    onClick(item.id);
  }, [item.id, onClick]);

  return (
    <div className="list-item" onClick={handleClick}>
      <span>{item.name}</span>
      <span>{item.value}</span>
    </div>
  );
});

// Code splitting with React.lazy
import { lazy, Suspense } from 'react';

const LazyDashboard = lazy(() => import('@pages/Dashboard'));
const LazyProfile = lazy(() => import('@pages/Profile'));
const LazySettings = lazy(() => import('@pages/Settings'));

export const AppRouter: React.FC = () => {
  return (
    <Router>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route
            path="/dashboard"
            element={<LazyDashboard />}
          />
          <Route
            path="/profile"
            element={<LazyProfile />}
          />
          <Route
            path="/settings"
            element={<LazySettings />}
          />
        </Routes>
      </Suspense>
    </Router>
  );
};
```

### 2.2 Vue.js Standards

#### Composition API Patterns **[REQUIRED]**
```vue
<!-- UserProfile.vue -->
<template>
  <div class="user-profile">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="user" class="user-content">
      <h1>{{ user.name }}</h1>
      <p>{{ user.email }}</p>
      <button @click="updateProfile" :disabled="updating">
        {{ updating ? 'Updating...' : 'Update Profile' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useUser } from '@/composables/useUser';
import type { User } from '@/types/user';

interface Props {
  userId: string;
}

const props = defineProps<Props>();

// Use composable for user management
const {
  user,
  loading,
  error,
  fetchUser,
  updateUser
} = useUser();

const updating = ref(false);

// Computed properties
const displayName = computed(() => {
  return user.value ? `${user.value.firstName} ${user.value.lastName}` : '';
});

// Watch for prop changes
watch(() => props.userId, (newId) => {
  if (newId) {
    fetchUser(newId);
  }
}, { immediate: true });

// Methods
const updateProfile = async () => {
  if (!user.value) return;

  updating.value = true;
  try {
    await updateUser(user.value.id, {
      lastActive: new Date().toISOString()
    });
  } catch (err) {
    console.error('Failed to update profile:', err);
  } finally {
    updating.value = false;
  }
};

// Lifecycle
onMounted(() => {
  console.log('UserProfile component mounted');
});
</script>

<style scoped>
.user-profile {
  padding: 1rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: var(--color-error);
}

.user-content {
  max-width: 600px;
  margin: 0 auto;
}
</style>
```

```typescript
// composables/useUser.ts
import { ref, reactive } from 'vue';
import type { Ref } from 'vue';
import { apiService } from '@/services/api';
import type { User } from '@/types/user';

interface UseUserReturn {
  user: Ref<User | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  fetchUser: (id: string) => Promise<void>;
  updateUser: (id: string, data: Partial<User>) => Promise<void>;
}

export function useUser(): UseUserReturn {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchUser = async (id: string) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await apiService.getUser(id);
      user.value = response.data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch user';
    } finally {
      loading.value = false;
    }
  };

  const updateUser = async (id: string, data: Partial<User>) => {
    try {
      const response = await apiService.updateUser(id, data);
      user.value = response.data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update user';
      throw err;
    }
  };

  return {
    user,
    loading,
    error,
    fetchUser,
    updateUser
  };
}
```

### 2.3 Angular Standards

#### Component and Service Patterns **[REQUIRED]**
```typescript
// user-profile.component.ts
import { Component, Input, OnInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { Observable, Subject, BehaviorSubject, combineLatest } from 'rxjs';
import { takeUntil, map, catchError, startWith } from 'rxjs/operators';
import { UserService } from '@services/user.service';
import { User } from '@models/user.model';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserProfileComponent implements OnInit, OnDestroy {
  @Input() userId!: string;

  private destroy$ = new Subject<void>();
  private userId$ = new BehaviorSubject<string>('');

  user$: Observable<User | null>;
  loading$: Observable<boolean>;
  error$: Observable<string | null>;

  constructor(private userService: UserService) {
    // Reactive data streams
    this.user$ = this.userId$.pipe(
      switchMap(id =>
        id ? this.userService.getUser(id) : of(null)
      ),
      catchError(error => {
        console.error('Error fetching user:', error);
        return of(null);
      }),
      takeUntil(this.destroy$)
    );

    this.loading$ = this.userService.loading$;
    this.error$ = this.userService.error$;
  }

  ngOnInit(): void {
    this.userId$.next(this.userId);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onUpdateProfile(userData: Partial<User>): void {
    if (this.userId) {
      this.userService.updateUser(this.userId, userData);
    }
  }

  trackByFn(index: number, item: any): any {
    return item.id || index;
  }
}

// user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map, catchError, finalize } from 'rxjs/operators';
import { environment } from '@environments/environment';
import { User } from '@models/user.model';
import { ApiResponse } from '@models/api.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly baseUrl = `${environment.apiUrl}/users`;

  private loadingSubject = new BehaviorSubject<boolean>(false);
  private errorSubject = new BehaviorSubject<string | null>(null);

  public loading$ = this.loadingSubject.asObservable();
  public error$ = this.errorSubject.asObservable();

  constructor(private http: HttpClient) {}

  getUser(id: string): Observable<User> {
    this.setLoading(true);
    this.setError(null);

    return this.http.get<ApiResponse<User>>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data),
      catchError(this.handleError.bind(this)),
      finalize(() => this.setLoading(false))
    );
  }

  updateUser(id: string, userData: Partial<User>): Observable<User> {
    this.setLoading(true);
    this.setError(null);

    return this.http.patch<ApiResponse<User>>(`${this.baseUrl}/${id}`, userData).pipe(
      map(response => response.data),
      catchError(this.handleError.bind(this)),
      finalize(() => this.setLoading(false))
    );
  }

  private setLoading(loading: boolean): void {
    this.loadingSubject.next(loading);
  }

  private setError(error: string | null): void {
    this.errorSubject.next(error);
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      errorMessage = `Server Error: ${error.status} - ${error.message}`;
    }

    this.setError(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
```

---

## 3. State Management

### 3.1 Redux Toolkit Standards

#### Store Configuration **[REQUIRED]**
```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { authSlice } from './slices/authSlice';
import { userSlice } from './slices/userSlice';
import { uiSlice } from './slices/uiSlice';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth'], // Only persist auth state
};

const persistedAuthReducer = persistReducer(persistConfig, authSlice.reducer);

export const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
    user: userSlice.reducer,
    ui: uiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiService } from '@services/api.service';
import { User } from '@types/api.types';

interface UserState {
  currentUser: User | null;
  users: User[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  currentUser: null,
  users: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string, { rejectWithValue }) => {
    try {
      const user = await apiService.getUser(userId);
      return user;
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Failed to fetch user'
      );
    }
  }
);

export const updateUser = createAsyncThunk(
  'user/updateUser',
  async (
    { userId, updates }: { userId: string; updates: Partial<User> },
    { rejectWithValue }
  ) => {
    try {
      const user = await apiService.updateUser(userId, updates);
      return user;
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Failed to update user'
      );
    }
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentUser: (state, action: PayloadAction<User | null>) => {
      state.currentUser = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch user
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.currentUser = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Update user
      .addCase(updateUser.fulfilled, (state, action) => {
        state.currentUser = action.payload;
        // Update in users array if it exists
        const index = state.users.findIndex(u => u.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        }
      });
  },
});

export const { clearError, setCurrentUser } = userSlice.actions;
export { userSlice };

// hooks/useAppSelector.ts
import { useSelector, TypedUseSelectorHook } from 'react-redux';
import type { RootState } from '@store/index';

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// hooks/useAppDispatch.ts
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '@store/index';

export const useAppDispatch = () => useDispatch<AppDispatch>();
```

### 3.2 Zustand Standards

#### Simple State Management **[RECOMMENDED]**
```typescript
// store/userStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { apiService } from '@services/api.service';
import { User } from '@types/api.types';

interface UserState {
  // State
  currentUser: User | null;
  users: User[];
  loading: boolean;
  error: string | null;

  // Actions
  setCurrentUser: (user: User | null) => void;
  fetchUser: (userId: string) => Promise<void>;
  updateUser: (userId: string, updates: Partial<User>) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  currentUser: null,
  users: [],
  loading: false,
  error: null,
};

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        setCurrentUser: (user) =>
          set({ currentUser: user }, false, 'setCurrentUser'),

        fetchUser: async (userId) => {
          set({ loading: true, error: null }, false, 'fetchUser/pending');

          try {
            const user = await apiService.getUser(userId);
            set(
              { currentUser: user, loading: false },
              false,
              'fetchUser/fulfilled'
            );
          } catch (error) {
            set(
              {
                error: error instanceof Error ? error.message : 'Failed to fetch user',
                loading: false,
              },
              false,
              'fetchUser/rejected'
            );
          }
        },

        updateUser: async (userId, updates) => {
          set({ loading: true, error: null }, false, 'updateUser/pending');

          try {
            const user = await apiService.updateUser(userId, updates);
            set(
              {
                currentUser: user,
                loading: false,
                users: get().users.map(u => u.id === userId ? user : u),
              },
              false,
              'updateUser/fulfilled'
            );
          } catch (error) {
            set(
              {
                error: error instanceof Error ? error.message : 'Failed to update user',
                loading: false,
              },
              false,
              'updateUser/rejected'
            );
          }
        },

        clearError: () => set({ error: null }, false, 'clearError'),

        reset: () => set(initialState, false, 'reset'),
      }),
      {
        name: 'user-store',
        partialize: (state) => ({
          currentUser: state.currentUser,
        }),
      }
    ),
    {
      name: 'user-store',
    }
  )
);

// Selectors
export const useCurrentUser = () => useUserStore(state => state.currentUser);
export const useUserLoading = () => useUserStore(state => state.loading);
export const useUserError = () => useUserStore(state => state.error);
```

### 3.3 Context API Patterns

#### Provider Pattern **[REQUIRED]**
```typescript
// contexts/ThemeContext.tsx
import React, { createContext, useContext, useReducer, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeState {
  theme: Theme;
  systemTheme: 'light' | 'dark';
  effectiveTheme: 'light' | 'dark';
}

type ThemeAction =
  | { type: 'SET_THEME'; payload: Theme }
  | { type: 'SET_SYSTEM_THEME'; payload: 'light' | 'dark' };

interface ThemeContextType {
  state: ThemeState;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

function themeReducer(state: ThemeState, action: ThemeAction): ThemeState {
  switch (action.type) {
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload,
        effectiveTheme:
          action.payload === 'system' ? state.systemTheme : action.payload,
      };
    case 'SET_SYSTEM_THEME':
      return {
        ...state,
        systemTheme: action.payload,
        effectiveTheme:
          state.theme === 'system' ? action.payload : state.effectiveTheme,
      };
    default:
      return state;
  }
}

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(themeReducer, {
    theme: 'system',
    systemTheme: 'light',
    effectiveTheme: 'light',
  });

  // Monitor system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleChange = (e: MediaQueryListEvent) => {
      dispatch({
        type: 'SET_SYSTEM_THEME',
        payload: e.matches ? 'dark' : 'light',
      });
    };

    // Set initial system theme
    dispatch({
      type: 'SET_SYSTEM_THEME',
      payload: mediaQuery.matches ? 'dark' : 'light',
    });

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const setTheme = (theme: Theme) => {
    dispatch({ type: 'SET_THEME', payload: theme });
    localStorage.setItem('theme', theme);
  };

  const value = {
    state,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
```

---

## 4. Performance and Optimization

### 4.1 Core Web Vitals

#### Performance Monitoring **[REQUIRED]**
```typescript
// utils/performance.ts
interface PerformanceMetrics {
  fcp: number; // First Contentful Paint
  lcp: number; // Largest Contentful Paint
  fid: number; // First Input Delay
  cls: number; // Cumulative Layout Shift
  ttfb: number; // Time to First Byte
}

class PerformanceMonitor {
  private metrics: Partial<PerformanceMetrics> = {};

  constructor() {
    this.observePerformance();
  }

  private observePerformance() {
    // Observe FCP and LCP
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
          this.metrics.fcp = entry.startTime;
        }
        if (entry.entryType === 'largest-contentful-paint') {
          this.metrics.lcp = entry.startTime;
        }
      }
    }).observe({ entryTypes: ['paint', 'largest-contentful-paint'] });

    // Observe FID
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        this.metrics.fid = entry.processingStart - entry.startTime;
      }
    }).observe({ entryTypes: ['first-input'] });

    // Observe CLS
    new PerformanceObserver((list) => {
      let clsValue = 0;
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      }
      this.metrics.cls = clsValue;
    }).observe({ entryTypes: ['layout-shift'] });

    // Calculate TTFB
    window.addEventListener('load', () => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      this.metrics.ttfb = navigation.responseStart - navigation.requestStart;
    });
  }

  getMetrics(): Partial<PerformanceMetrics> {
    return { ...this.metrics };
  }

  reportMetrics() {
    // Report to analytics service
    if (window.gtag) {
      Object.entries(this.metrics).forEach(([metric, value]) => {
        window.gtag('event', metric, {
          custom_parameter_value: value,
        });
      });
    }
  }
}

export const performanceMonitor = new PerformanceMonitor();

// Performance budget checker
export const checkPerformanceBudget = () => {
  const metrics = performanceMonitor.getMetrics();

  const budget = {
    fcp: 1800, // 1.8s
    lcp: 2500, // 2.5s
    fid: 100,  // 100ms
    cls: 0.1,  // 0.1
    ttfb: 600, // 600ms
  };

  const violations = Object.entries(budget)
    .filter(([metric, threshold]) => {
      const value = metrics[metric as keyof PerformanceMetrics];
      return value !== undefined && value > threshold;
    })
    .map(([metric, threshold]) => ({
      metric,
      actual: metrics[metric as keyof PerformanceMetrics],
      threshold,
    }));

  if (violations.length > 0) {
    console.warn('Performance budget violations:', violations);
  }

  return violations;
};
```

#### Image Optimization **[REQUIRED]**
```typescript
// components/OptimizedImage.tsx
import React, { useState, useRef, useEffect } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  lazy?: boolean;
  placeholder?: string;
  sizes?: string;
  priority?: boolean;
}

export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width,
  height,
  className,
  lazy = true,
  placeholder,
  sizes,
  priority = false,
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(!lazy || priority);
  const imgRef = useRef<HTMLImageElement>(null);

  // Intersection Observer for lazy loading
  useEffect(() => {
    if (!lazy || priority || isInView) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [lazy, priority, isInView]);

  // Generate responsive image URLs
  const generateSrcSet = (baseSrc: string) => {
    const widths = [320, 640, 768, 1024, 1280, 1536];
    return widths
      .map(w => `${baseSrc}?w=${w} ${w}w`)
      .join(', ');
  };

  // Generate WebP alternative
  const getWebPSrc = (src: string) => {
    return src.replace(/\.(jpg|jpeg|png)$/i, '.webp');
  };

  return (
    <div className={`optimized-image ${className || ''}`}>
      {placeholder && !isLoaded && (
        <div className="image-placeholder">
          <img src={placeholder} alt="" aria-hidden="true" />
        </div>
      )}

      {isInView && (
        <picture>
          <source
            srcSet={generateSrcSet(getWebPSrc(src))}
            sizes={sizes}
            type="image/webp"
          />
          <img
            ref={imgRef}
            src={src}
            srcSet={generateSrcSet(src)}
            sizes={sizes}
            alt={alt}
            width={width}
            height={height}
            loading={lazy && !priority ? 'lazy' : 'eager'}
            onLoad={() => setIsLoaded(true)}
            style={{
              opacity: isLoaded ? 1 : 0,
              transition: 'opacity 0.3s ease',
            }}
          />
        </picture>
      )}
    </div>
  );
};
```

### 4.2 Bundle Optimization

#### Code Splitting Strategies **[REQUIRED]**
```typescript
// utils/loadable.tsx
import React, { Suspense, ComponentType } from 'react';

interface LoadableOptions {
  fallback?: React.ComponentType;
  delay?: number;
}

export function loadable<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>,
  options: LoadableOptions = {}
) {
  const LazyComponent = React.lazy(importFunc);

  return function LoadableComponent(props: React.ComponentProps<T>) {
    return (
      <Suspense fallback={options.fallback ? <options.fallback /> : <div>Loading...</div>}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };
}

// Route-based code splitting
const Dashboard = loadable(() => import('@pages/Dashboard'), {
  fallback: () => <PageSkeleton />,
});

const UserProfile = loadable(() => import('@pages/UserProfile'), {
  fallback: () => <PageSkeleton />,
});

// Feature-based code splitting
const ChartComponent = loadable(() => import('@components/Chart'), {
  fallback: () => <ChartSkeleton />,
});

// Preload critical routes
export const preloadRoutes = () => {
  // Preload likely next routes
  const routes = [
    () => import('@pages/Dashboard'),
    () => import('@pages/UserProfile'),
  ];

  routes.forEach(route => {
    route().catch(() => {
      // Silently handle preload failures
    });
  });
};

// webpack.config.js optimization
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor chunk for stable dependencies
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
          priority: 10,
          reuseExistingChunk: true,
        },
        // Common chunk for shared code
        common: {
          name: 'common',
          minChunks: 2,
          chunks: 'all',
          priority: 5,
          reuseExistingChunk: true,
        },
        // React chunk
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          chunks: 'all',
          priority: 20,
        },
      },
    },
    runtimeChunk: 'single',
  },
};
```

---

## 5. Progressive Web Apps (PWA)

### 5.1 Service Worker Implementation

#### Service Worker Strategy **[REQUIRED]**
```typescript
// service-worker.ts
const CACHE_NAME = 'app-v1.0.0';
const STATIC_CACHE = 'static-v1.0.0';
const DYNAMIC_CACHE = 'dynamic-v1.0.0';

const STATIC_ASSETS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/offline.html',
];

const API_CACHE_STRATEGY = {
  '/api/users': 'networkFirst',
  '/api/settings': 'cacheFirst',
  '/api/notifications': 'networkOnly',
};

// Install event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName =>
              cacheName !== STATIC_CACHE &&
              cacheName !== DYNAMIC_CACHE
            )
            .map(cacheName => caches.delete(cacheName))
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event with different strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    const strategy = getApiCacheStrategy(url.pathname);
    event.respondWith(handleApiRequest(request, strategy));
    return;
  }

  // Handle static assets
  if (STATIC_ASSETS.includes(url.pathname)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // Handle navigation requests
  if (request.mode === 'navigate') {
    event.respondWith(networkFirst(request));
    return;
  }

  // Default: network first with dynamic cache
  event.respondWith(networkFirst(request, DYNAMIC_CACHE));
});

// Cache strategies
async function cacheFirst(request, cacheName = DYNAMIC_CACHE) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);
    const cache = await caches.open(cacheName);
    cache.put(request, networkResponse.clone());
    return networkResponse;
  } catch (error) {
    if (request.mode === 'navigate') {
      return caches.match('/offline.html');
    }
    throw error;
  }
}

async function networkFirst(request, cacheName = DYNAMIC_CACHE) {
  try {
    const networkResponse = await fetch(request);
    const cache = await caches.open(cacheName);
    cache.put(request, networkResponse.clone());
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    if (request.mode === 'navigate') {
      return caches.match('/offline.html');
    }
    throw error;
  }
}

function getApiCacheStrategy(pathname) {
  for (const [pattern, strategy] of Object.entries(API_CACHE_STRATEGY)) {
    if (pathname.startsWith(pattern)) {
      return strategy;
    }
  }
  return 'networkFirst';
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // Process offline actions queue
  const offlineActions = await getOfflineActions();

  for (const action of offlineActions) {
    try {
      await processOfflineAction(action);
      await removeOfflineAction(action.id);
    } catch (error) {
      console.error('Failed to sync offline action:', error);
    }
  }
}
```

#### PWA Manifest Configuration **[REQUIRED]**
```json
{
  "name": "Modern Web Application",
  "short_name": "ModernApp",
  "description": "A modern progressive web application",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#000000",
  "background_color": "#ffffff",
  "scope": "/",
  "lang": "en",
  "categories": ["productivity", "business"],
  "screenshots": [
    {
      "src": "/images/screenshot-mobile.png",
      "sizes": "640x1136",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/images/screenshot-desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ],
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ],
  "shortcuts": [
    {
      "name": "Dashboard",
      "short_name": "Dashboard",
      "description": "Open the dashboard",
      "url": "/dashboard",
      "icons": [
        {
          "src": "/icons/dashboard-96x96.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Profile",
      "short_name": "Profile",
      "description": "View profile",
      "url": "/profile",
      "icons": [
        {
          "src": "/icons/profile-96x96.png",
          "sizes": "96x96"
        }
      ]
    }
  ]
}
```

### 5.2 Offline Functionality

#### Offline Data Management **[REQUIRED]**
```typescript
// utils/offlineStorage.ts
interface OfflineAction {
  id: string;
  type: string;
  payload: any;
  timestamp: number;
  retryCount: number;
}

class OfflineManager {
  private dbName = 'app-offline-db';
  private version = 1;
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Create object stores
        if (!db.objectStoreNames.contains('actions')) {
          const actionStore = db.createObjectStore('actions', { keyPath: 'id' });
          actionStore.createIndex('timestamp', 'timestamp');
        }

        if (!db.objectStoreNames.contains('cache')) {
          const cacheStore = db.createObjectStore('cache', { keyPath: 'key' });
          cacheStore.createIndex('expiry', 'expiry');
        }
      };
    });
  }

  async addOfflineAction(action: Omit<OfflineAction, 'id' | 'timestamp' | 'retryCount'>): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const offlineAction: OfflineAction = {
      ...action,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      retryCount: 0,
    };

    const transaction = this.db.transaction(['actions'], 'readwrite');
    const store = transaction.objectStore('actions');
    await store.add(offlineAction);
  }

  async getOfflineActions(): Promise<OfflineAction[]> {
    if (!this.db) throw new Error('Database not initialized');

    const transaction = this.db.transaction(['actions'], 'readonly');
    const store = transaction.objectStore('actions');
    const request = store.getAll();

    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async removeOfflineAction(id: string): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const transaction = this.db.transaction(['actions'], 'readwrite');
    const store = transaction.objectStore('actions');
    await store.delete(id);
  }

  async cacheData(key: string, data: any, ttl: number = 3600000): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const cacheItem = {
      key,
      data,
      expiry: Date.now() + ttl,
    };

    const transaction = this.db.transaction(['cache'], 'readwrite');
    const store = transaction.objectStore('cache');
    await store.put(cacheItem);
  }

  async getCachedData(key: string): Promise<any | null> {
    if (!this.db) throw new Error('Database not initialized');

    const transaction = this.db.transaction(['cache'], 'readonly');
    const store = transaction.objectStore('cache');
    const request = store.get(key);

    return new Promise((resolve, reject) => {
      request.onsuccess = () => {
        const result = request.result;
        if (!result || result.expiry < Date.now()) {
          resolve(null);
        } else {
          resolve(result.data);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }
}

export const offlineManager = new OfflineManager();

// React hook for offline functionality
export function useOffline() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [hasOfflineActions, setHasOfflineActions] = useState(false);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    if (isOnline) {
      // Sync offline actions when coming back online
      syncOfflineActions();
    }
  }, [isOnline]);

  const syncOfflineActions = async () => {
    try {
      const actions = await offlineManager.getOfflineActions();
      setHasOfflineActions(actions.length > 0);

      for (const action of actions) {
        try {
          await processOfflineAction(action);
          await offlineManager.removeOfflineAction(action.id);
        } catch (error) {
          console.error('Failed to sync action:', error);
        }
      }

      setHasOfflineActions(false);
    } catch (error) {
      console.error('Failed to sync offline actions:', error);
    }
  };

  const addOfflineAction = async (type: string, payload: any) => {
    await offlineManager.addOfflineAction({ type, payload });
    setHasOfflineActions(true);
  };

  return {
    isOnline,
    hasOfflineActions,
    addOfflineAction,
    syncOfflineActions,
  };
}
```

---

## 6. Mobile Development Standards

### 6.1 React Native Standards

#### Project Structure **[REQUIRED]**
```
mobile-app/
├── src/
│   ├── components/            # Reusable components
│   │   ├── common/
│   │   ├── forms/
│   │   └── navigation/
│   ├── screens/              # Screen components
│   │   ├── Auth/
│   │   ├── Home/
│   │   └── Profile/
│   ├── navigation/           # Navigation configuration
│   ├── services/             # API and services
│   ├── store/                # State management
│   ├── hooks/                # Custom hooks
│   ├── utils/                # Utility functions
│   ├── types/                # TypeScript types
│   ├── styles/               # Styling
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   └── spacing.ts
│   └── assets/               # Images, fonts
├── android/                  # Android-specific code
├── ios/                      # iOS-specific code
├── __tests__/                # Test files
├── metro.config.js           # Metro bundler config
├── babel.config.js           # Babel configuration
├── react-native.config.js    # RN configuration
└── package.json
```

#### Component Development **[REQUIRED]**
```typescript
// components/Button/Button.tsx
import React from 'react';
import {
  TouchableOpacity,
  Text,
  ActivityIndicator,
  StyleSheet,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { colors, typography, spacing } from '@styles/index';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  testID?: string;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  style,
  textStyle,
  testID,
}) => {
  const buttonStyle = [
    styles.base,
    styles[variant],
    styles[size],
    disabled && styles.disabled,
    style,
  ];

  const titleStyle = [
    styles.text,
    styles[`${variant}Text`],
    styles[`${size}Text`],
    disabled && styles.disabledText,
    textStyle,
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
      testID={testID}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={variant === 'primary' ? colors.white : colors.primary}
        />
      ) : (
        <Text style={titleStyle}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
  },

  // Variants
  primary: {
    backgroundColor: colors.primary,
  },
  secondary: {
    backgroundColor: colors.secondary,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  danger: {
    backgroundColor: colors.danger,
  },

  // Sizes
  small: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    minHeight: 32,
  },
  medium: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    minHeight: 44,
  },
  large: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    minHeight: 56,
  },

  // States
  disabled: {
    opacity: 0.5,
  },

  // Text styles
  text: {
    fontFamily: typography.semiBold,
    textAlign: 'center',
  },
  primaryText: {
    color: colors.white,
  },
  secondaryText: {
    color: colors.primary,
  },
  dangerText: {
    color: colors.white,
  },
  smallText: {
    fontSize: 14,
  },
  mediumText: {
    fontSize: 16,
  },
  largeText: {
    fontSize: 18,
  },
  disabledText: {
    opacity: 0.7,
  },
});
```

#### Navigation Setup **[REQUIRED]**
```typescript
// navigation/AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useAuthStore } from '@store/authStore';

// Type definitions for navigation
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Profile: { userId: string };
  Settings: undefined;
};

export type TabParamList = {
  Home: undefined;
  Search: undefined;
  Profile: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Icon name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Icon name="search" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Icon name="user" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

export const AppNavigator = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <>
            <Stack.Screen name="Main" component={TabNavigator} />
            <Stack.Screen
              name="Profile"
              component={ProfileScreen}
              options={{ presentation: 'modal' }}
            />
            <Stack.Screen name="Settings" component={SettingsScreen} />
          </>
        ) : (
          <Stack.Screen name="Auth" component={AuthScreen} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
```

### 6.2 Platform-Specific Optimizations

#### iOS Guidelines **[REQUIRED]**
```typescript
// utils/platform.ts
import { Platform, Dimensions } from 'react-native';

export const isIOS = Platform.OS === 'ios';
export const isAndroid = Platform.OS === 'android';

export const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// Safe area handling for iOS
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export const SafeAreaView: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={{
        flex: 1,
        paddingTop: insets.top,
        paddingBottom: insets.bottom,
        paddingLeft: insets.left,
        paddingRight: insets.right,
      }}
    >
      {children}
    </View>
  );
};

// Platform-specific styling
export const createPlatformStyles = (iosStyle: any, androidStyle: any) => {
  return Platform.select({
    ios: iosStyle,
    android: androidStyle,
  });
};

// Performance optimizations
export const useKeyboardHeight = () => {
  const [keyboardHeight, setKeyboardHeight] = useState(0);

  useEffect(() => {
    const showEvent = isIOS ? 'keyboardWillShow' : 'keyboardDidShow';
    const hideEvent = isIOS ? 'keyboardWillHide' : 'keyboardDidHide';

    const showListener = Keyboard.addListener(showEvent, (e) => {
      setKeyboardHeight(e.endCoordinates.height);
    });

    const hideListener = Keyboard.addListener(hideEvent, () => {
      setKeyboardHeight(0);
    });

    return () => {
      showListener.remove();
      hideListener.remove();
    };
  }, []);

  return keyboardHeight;
};
```

#### Android Guidelines **[REQUIRED]**
```xml
<!-- android/app/src/main/res/values/styles.xml -->
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="android:editTextBackground">@drawable/rn_edit_text_material</item>
        <item name="android:statusBarColor">@android:color/transparent</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:navigationBarColor">@android:color/transparent</item>
        <item name="android:windowLightNavigationBar">true</item>
    </style>
</resources>
```

```typescript
// Android-specific optimizations
import { BackHandler } from 'react-native';

export const useBackHandler = (handler: () => boolean) => {
  useEffect(() => {
    if (isAndroid) {
      const backHandler = BackHandler.addEventListener('hardwareBackPress', handler);
      return () => backHandler.remove();
    }
  }, [handler]);
};

// Permission handling
import { PermissionsAndroid } from 'react-native';

export const requestPermissions = async () => {
  if (isAndroid) {
    try {
      const granted = await PermissionsAndroid.requestMultiple([
        PermissionsAndroid.PERMISSIONS.CAMERA,
        PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      ]);

      return Object.values(granted).every(
        permission => permission === PermissionsAndroid.RESULTS.GRANTED
      );
    } catch (err) {
      console.warn(err);
      return false;
    }
  }
  return true;
};
```

---

## Implementation Checklist

### Frontend Architecture
- [ ] Project structure follows standards
- [ ] TypeScript configured with strict settings
- [ ] Build system optimized
- [ ] Component architecture defined
- [ ] Error boundaries implemented

### Framework Implementation
- [ ] Framework-specific patterns applied
- [ ] Performance optimizations implemented
- [ ] Code splitting configured
- [ ] State management setup
- [ ] Testing framework integrated

### Performance Optimization
- [ ] Core Web Vitals monitored
- [ ] Images optimized
- [ ] Bundle size optimized
- [ ] Lazy loading implemented
- [ ] Caching strategies applied

### PWA Features
- [ ] Service worker implemented
- [ ] Manifest configured
- [ ] Offline functionality working
- [ ] Background sync setup
- [ ] Installation prompts added

### Mobile Development
- [ ] Platform-specific optimizations
- [ ] Navigation configured
- [ ] Performance optimized
- [ ] Native features integrated
- [ ] Testing on real devices

### Testing and Quality
- [ ] Unit tests comprehensive
- [ ] Integration tests working
- [ ] E2E tests automated
- [ ] Performance tests defined
- [ ] Accessibility tests included

---

**End of Frontend and Mobile Development Standards**
