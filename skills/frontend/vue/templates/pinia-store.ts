/**
 * Pinia Store Template with TypeScript
 * Demonstrates: Composition API style, async actions, error handling, persistence
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Ref, ComputedRef } from 'vue';

// ============================================================================
// Types & Interfaces
// ============================================================================

export interface User {
  id: number;
  email: string;
  name: string;
  role: 'admin' | 'user';
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  language: string;
  notifications: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface ApiError {
  message: string;
  code: string;
  details?: unknown;
}

// ============================================================================
// Store Definition (Composition API style)
// ============================================================================

export const useUserStore = defineStore('user', () => {
  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const lastLoginTime = ref<Date | null>(null);

  // ---------------------------------------------------------------------------
  // Getters (computed properties)
  // ---------------------------------------------------------------------------

  const isAuthenticated = computed(() => user.value !== null);

  const isAdmin = computed(() => user.value?.role === 'admin');

  const fullName = computed(() => {
    if (!user.value) return '';
    return user.value.name;
  });

  const initials = computed(() => {
    if (!user.value) return '';
    return user.value.name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
  });

  // ---------------------------------------------------------------------------
  // Actions
  // ---------------------------------------------------------------------------

  /**
   * Login user with email and password
   */
  async function login(credentials: LoginCredentials): Promise<void> {
    isLoading.value = true;
    error.value = null;

    try {
      // Call API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      // Update state
      user.value = data.user;
      lastLoginTime.value = new Date();

      // Store token
      localStorage.setItem('auth_token', data.token);

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Logout user and clear session
   */
  async function logout(): Promise<void> {
    isLoading.value = true;

    try {
      // Call logout API
      const token = localStorage.getItem('auth_token');
      await fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      // Clear state regardless of API result
      user.value = null;
      lastLoginTime.value = null;
      localStorage.removeItem('auth_token');
      isLoading.value = false;
    }
  }

  /**
   * Restore session from stored token
   */
  async function restoreSession(): Promise<boolean> {
    const token = localStorage.getItem('auth_token');

    if (!token) {
      return false;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Session expired');
      }

      const data = await response.json();
      user.value = data.user;

      return true;
    } catch (err) {
      // Clear invalid session
      localStorage.removeItem('auth_token');
      error.value = err instanceof Error ? err.message : 'Session restore failed';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Update user preferences
   */
  async function updatePreferences(
    preferences: Partial<UserPreferences>
  ): Promise<void> {
    if (!user.value) {
      throw new Error('User not authenticated');
    }

    isLoading.value = true;
    error.value = null;

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch('/api/user/preferences', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(preferences)
      });

      if (!response.ok) {
        throw new Error('Failed to update preferences');
      }

      // Optimistic update
      user.value.preferences = {
        ...user.value.preferences,
        ...preferences
      };

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Update failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Update user profile
   */
  async function updateProfile(updates: Partial<User>): Promise<void> {
    if (!user.value) {
      throw new Error('User not authenticated');
    }

    isLoading.value = true;
    error.value = null;

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch('/api/user/profile', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updates)
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const data = await response.json();
      user.value = data.user;

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Update failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Check if user has specific role
   */
  function hasRole(role: string): boolean {
    return user.value?.role === role;
  }

  /**
   * Clear error state
   */
  function clearError(): void {
    error.value = null;
  }

  // ---------------------------------------------------------------------------
  // Return (public API)
  // ---------------------------------------------------------------------------

  return {
    // State
    user,
    isLoading,
    error,
    lastLoginTime,

    // Getters
    isAuthenticated,
    isAdmin,
    fullName,
    initials,

    // Actions
    login,
    logout,
    restoreSession,
    updatePreferences,
    updateProfile,
    hasRole,
    clearError
  };
});

// ============================================================================
// Store Definition (Options API style - alternative)
// ============================================================================

export const useUserStoreOptions = defineStore('user-options', {
  state: () => ({
    user: null as User | null,
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
    isAdmin: (state) => state.user?.role === 'admin',
    fullName: (state) => state.user?.name || ''
  },

  actions: {
    async login(credentials: LoginCredentials) {
      // Same implementation as composition style
    },

    async logout() {
      // Same implementation
    }
  }
});

// ============================================================================
// Composable for using the store with additional utilities
// ============================================================================

export function useAuth() {
  const userStore = useUserStore();
  const router = useRouter();

  async function loginAndRedirect(credentials: LoginCredentials, redirectTo = '/') {
    await userStore.login(credentials);
    router.push(redirectTo);
  }

  async function logoutAndRedirect(redirectTo = '/login') {
    await userStore.logout();
    router.push(redirectTo);
  }

  return {
    ...userStore,
    loginAndRedirect,
    logoutAndRedirect
  };
}
