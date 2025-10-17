---
name: vue-frontend
category: frontend
difficulty: intermediate
wcag_level: AA
version: 1.0.0
last_updated: 2025-10-17
related_skills:
  - typescript
  - testing
  - accessibility
  - security
---

# Vue.js Frontend Development Skill

## Level 1: Quick Reference (~700-900 tokens)

### Core Concepts

**Composition API vs Options API**

```typescript
// Composition API (recommended for new projects)
import { ref, computed } from 'vue';

const count = ref(0);
const doubled = computed(() => count.value * 2);

// Options API (traditional)
export default {
  data() { return { count: 0 }; },
  computed: { doubled() { return this.count * 2; } }
};
```

**Reactivity Fundamentals**

```typescript
// ref - for primitives and single values
const count = ref(0);
count.value++; // access with .value

// reactive - for objects
const state = reactive({ count: 0, name: 'Vue' });
state.count++; // direct access

// computed - derived state
const doubled = computed(() => count.value * 2);

// watch - side effects
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`);
});
```

**Component Communication**

```typescript
// Props (parent → child)
defineProps<{ message: string }>();

// Emits (child → parent)
const emit = defineEmits<{ submit: [data: FormData] }>();
emit('submit', formData);

// Provide/Inject (ancestor → descendant)
// Parent
provide('theme', ref('dark'));
// Child
const theme = inject<Ref<string>>('theme');
```

### Essential Checklist

**Setup & Configuration**

- [ ] Vue 3 with Vite or Vue CLI
- [ ] TypeScript integration
- [ ] ESLint + Prettier configured
- [ ] Vue Router installed
- [ ] Pinia for state management
- [ ] Vitest + Vue Test Utils for testing

**Component Development**

- [ ] Use Composition API with `<script setup>`
- [ ] Define props with TypeScript types
- [ ] Emit typed events
- [ ] Implement proper lifecycle hooks
- [ ] Use composables for reusable logic

**Routing & Navigation**

- [ ] Define routes with lazy loading
- [ ] Implement route guards (auth, permissions)
- [ ] Handle 404 and error pages
- [ ] Use typed router with generics

**State Management**

- [ ] Define Pinia stores with TypeScript
- [ ] Use composition stores for complex logic
- [ ] Implement persistence for user preferences
- [ ] Handle async actions properly

**Performance**

- [ ] Use `v-once` for static content
- [ ] Implement virtual scrolling for large lists
- [ ] Lazy load routes and components
- [ ] Use `v-memo` for expensive renders
- [ ] Configure proper build optimization

**Accessibility (WCAG 2.1 AA)**

- [ ] Semantic HTML elements
- [ ] ARIA labels and roles
- [ ] Keyboard navigation support
- [ ] Focus management
- [ ] Screen reader testing

**Security**

- [ ] Sanitize user input (DOMPurify)
- [ ] Configure CSP headers
- [ ] Avoid `v-html` with untrusted content
- [ ] Implement proper authentication
- [ ] Secure API communication

---

## Level 2: Implementation Guide (~4000-5000 tokens)

### 1. Vue 3 Composition API

#### Setup Function & Script Setup

The Composition API provides better TypeScript support and code organization:

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';

// Reactive state
const count = ref(0);
const user = reactive({ name: 'Vue', age: 3 });

// Computed values
const doubled = computed(() => count.value * 2);

// Watchers
watch(count, (newVal) => {
  console.log('Count changed:', newVal);
});

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted');
});

// Methods
function increment() {
  count.value++;
}
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

#### Reactive Primitives

**ref vs reactive**:

- `ref`: Primitives, single values, needs `.value` in script
- `reactive`: Objects, arrays, no `.value` needed

```typescript
// ref - wrap primitives
const count = ref(0);
const message = ref('Hello');

// Access in script
count.value++; // needs .value
// Access in template
<p>{{ count }}</p> // no .value needed

// reactive - for objects
const state = reactive({
  user: { name: 'Vue', email: 'vue@example.com' },
  items: [] as Item[]
});

// Direct access
state.user.name = 'Vue 3';
state.items.push(newItem);

// Destructuring loses reactivity
const { user } = state; // ❌ Not reactive
const user = toRef(state, 'user'); // ✅ Keeps reactivity
```

#### Computed Properties

```typescript
// Basic computed
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});

// Writable computed
const fullName = computed({
  get() {
    return `${firstName.value} ${lastName.value}`;
  },
  set(newValue) {
    [firstName.value, lastName.value] = newValue.split(' ');
  }
});

// Computed with type
interface User {
  firstName: string;
  lastName: string;
}

const fullName = computed<string>(() => {
  return `${user.value.firstName} ${user.value.lastName}`;
});
```

#### Watchers

```typescript
// Watch single ref
watch(count, (newVal, oldVal) => {
  console.log(`Count: ${oldVal} → ${newVal}`);
});

// Watch multiple sources
watch([firstName, lastName], ([newFirst, newLast]) => {
  console.log(`Name: ${newFirst} ${newLast}`);
});

// Watch reactive object property
watch(
  () => state.user.name,
  (newName) => console.log('Name changed:', newName)
);

// Immediate execution
watch(count, (val) => {
  console.log('Count:', val);
}, { immediate: true });

// Deep watching
watch(state, (newVal) => {
  console.log('State changed:', newVal);
}, { deep: true });

// watchEffect - auto-tracks dependencies
watchEffect(() => {
  console.log(`Count is ${count.value}`);
  // Automatically re-runs when count changes
});
```

### 2. Component Architecture

#### Props & Emits

```vue
<script setup lang="ts">
// Define props with TypeScript
interface Props {
  title: string;
  count?: number; // optional
  items: string[]; // required
  onUpdate?: (value: number) => void; // callback
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
});

// Define emits with TypeScript
interface Emits {
  submit: [data: FormData]; // event with payload
  cancel: []; // event without payload
  'update:modelValue': [value: string]; // v-model support
}

const emit = defineEmits<Emits>();

// Emit events
function handleSubmit() {
  const formData = new FormData();
  emit('submit', formData);
}

// v-model support
const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});
</script>

<template>
  <div>
    <h2>{{ title }}</h2>
    <input v-model="modelValue" />
    <button @click="handleSubmit">Submit</button>
  </div>
</template>
```

#### Slots

```vue
<script setup lang="ts">
// Named slots with scoped data
interface SlotProps {
  item: Item;
  index: number;
}
</script>

<template>
  <div class="card">
    <!-- Default slot -->
    <slot />

    <!-- Named slots -->
    <header>
      <slot name="header" />
    </header>

    <!-- Scoped slots -->
    <div v-for="(item, index) in items" :key="item.id">
      <slot name="item" :item="item" :index="index" />
    </div>

    <!-- Fallback content -->
    <footer>
      <slot name="footer">
        <p>Default footer content</p>
      </slot>
    </footer>
  </div>
</template>

<!-- Usage -->
<Card>
  <template #header>
    <h1>Custom Header</h1>
  </template>

  <template #item="{ item, index }">
    <p>{{ index }}: {{ item.name }}</p>
  </template>

  Default content
</Card>
```

#### Provide/Inject

```typescript
// Parent component
import { provide, ref } from 'vue';

const theme = ref('dark');
const updateTheme = (newTheme: string) => {
  theme.value = newTheme;
};

provide('theme', theme);
provide('updateTheme', updateTheme);

// Child component (any depth)
import { inject } from 'vue';

const theme = inject<Ref<string>>('theme');
const updateTheme = inject<(theme: string) => void>('updateTheme');

// With default value
const theme = inject('theme', ref('light'));

// Typed injection key (recommended)
// keys.ts
export const ThemeKey: InjectionKey<Ref<string>> = Symbol('theme');

// Parent
provide(ThemeKey, ref('dark'));

// Child
const theme = inject(ThemeKey); // Fully typed
```

### 3. Vue Router

#### Route Configuration

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: () => import('@/views/UserDetail.vue'),
    props: true, // pass route params as props
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  }
});

export default router;
```

#### Navigation Guards

```typescript
// Global guards
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();

  // Redirect to login if not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } };
  }

  // Check permissions
  if (to.meta.roles && !authStore.hasRole(to.meta.roles)) {
    return { name: 'Forbidden' };
  }
});

// Per-route guards
const routes = [
  {
    path: '/admin',
    component: AdminView,
    beforeEnter: (to, from) => {
      // Check admin access
      if (!hasAdminAccess()) {
        return false; // cancel navigation
      }
    }
  }
];

// Component guards
<script setup lang="ts">
import { onBeforeRouteLeave } from 'vue-router';

const hasUnsavedChanges = ref(false);

onBeforeRouteLeave((to, from) => {
  if (hasUnsavedChanges.value) {
    return window.confirm('You have unsaved changes. Leave anyway?');
  }
});
</script>
```

#### Typed Routes

```typescript
// Extend route meta type
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    roles?: string[];
    title?: string;
  }
}

// Type-safe navigation
import { useRouter } from 'vue-router';

const router = useRouter();

// Type-safe params
router.push({
  name: 'UserDetail',
  params: { id: userId }
});

// Query parameters
router.push({
  name: 'Search',
  query: { q: searchTerm, page: '1' }
});
```

### 4. State Management with Pinia

#### Store Definition

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// Composition style (recommended)
export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters (computed)
  const isAuthenticated = computed(() => user.value !== null);
  const fullName = computed(() =>
    user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
  );

  // Actions
  async function login(email: string, password: string) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await api.login(email, password);
      user.value = response.data.user;
      localStorage.setItem('token', response.data.token);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  function logout() {
    user.value = null;
    localStorage.removeItem('token');
  }

  return {
    // State
    user,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    fullName,
    // Actions
    login,
    logout
  };
});

// Options style
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isLoading: false
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null
  },

  actions: {
    async login(email: string, password: string) {
      // Same implementation
    }
  }
});
```

#### Store Composition

```typescript
// Compose multiple stores
export const useCartStore = defineStore('cart', () => {
  const userStore = useUserStore();

  const items = ref<CartItem[]>([]);

  const total = computed(() => {
    if (!userStore.isAuthenticated) return 0;
    return items.value.reduce((sum, item) => sum + item.price, 0);
  });

  async function checkout() {
    if (!userStore.isAuthenticated) {
      throw new Error('Must be logged in');
    }
    // Checkout logic
  }

  return { items, total, checkout };
});
```

#### Store Persistence

```typescript
import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const usePreferencesStore = defineStore('preferences', () => {
  // Auto-persist to localStorage
  const theme = useStorage('theme', 'light');
  const language = useStorage('language', 'en');

  function setTheme(newTheme: string) {
    theme.value = newTheme;
    // Automatically saved to localStorage
  }

  return { theme, language, setTheme };
});

// Or use pinia-plugin-persistedstate
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export const useStore = defineStore('main', {
  state: () => ({ count: 0 }),
  persist: true // Automatically persist to localStorage
});
```

### 5. Performance Optimization

#### Virtual Scrolling

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { useVirtualList } from '@vueuse/core';

const allItems = ref(Array.from({ length: 100000 }, (_, i) => ({
  id: i,
  text: `Item ${i}`
})));

const { list, containerProps, wrapperProps } = useVirtualList(
  allItems,
  {
    itemHeight: 50, // Fixed height for each item
    overscan: 10 // Render extra items for smooth scrolling
  }
);
</script>

<template>
  <div v-bind="containerProps" style="height: 600px; overflow: auto;">
    <div v-bind="wrapperProps">
      <div
        v-for="{ data, index } in list"
        :key="data.id"
        style="height: 50px;"
      >
        {{ data.text }}
      </div>
    </div>
  </div>
</template>
```

#### Lazy Loading

```typescript
// Route-based lazy loading
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue')
  }
];

// Component lazy loading
<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const HeavyComponent = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorMessage,
  delay: 200,
  timeout: 10000
});
</script>

// Conditional lazy loading
<script setup lang="ts">
import { ref, defineAsyncComponent } from 'vue';

const showChart = ref(false);
const ChartComponent = defineAsyncComponent(
  () => import('./Chart.vue')
);

function loadChart() {
  showChart.value = true;
}
</script>

<template>
  <button @click="loadChart">Load Chart</button>
  <Suspense v-if="showChart">
    <ChartComponent />
    <template #fallback>
      <div>Loading chart...</div>
    </template>
  </Suspense>
</template>
```

#### Memoization

```vue
<script setup lang="ts">
import { ref, computed, useMemoize } from 'vue';

// Use v-memo for expensive list rendering
const items = ref([/* large array */]);

// Memoize expensive computations
const expensiveCalculation = useMemoize((input: number) => {
  // Heavy computation
  return result;
});

// Computed with caching
const processedItems = computed(() => {
  return items.value.map(item => expensiveCalculation(item.id));
});
</script>

<template>
  <!-- v-memo: only re-render if dependencies change -->
  <div
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item.updated]"
  >
    {{ expensiveCalculation(item.id) }}
  </div>

  <!-- v-once: render once, never update -->
  <div v-once>
    Static content that never changes
  </div>
</template>
```

#### Build Optimization

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'ui': ['@/components/ui']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia']
  }
});
```

### 6. Testing with Vitest

#### Component Testing

```typescript
// UserProfile.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import UserProfile from '@/components/UserProfile.vue';

describe('UserProfile', () => {
  it('renders user information', () => {
    const wrapper = mount(UserProfile, {
      props: {
        user: {
          name: 'John Doe',
          email: 'john@example.com'
        }
      }
    });

    expect(wrapper.text()).toContain('John Doe');
    expect(wrapper.text()).toContain('john@example.com');
  });

  it('emits update event on edit', async () => {
    const wrapper = mount(UserProfile, {
      props: { user: { name: 'John', email: 'john@example.com' } }
    });

    await wrapper.find('button.edit').trigger('click');

    expect(wrapper.emitted()).toHaveProperty('update');
    expect(wrapper.emitted('update')?.[0]).toEqual([{
      name: 'John',
      email: 'john@example.com'
    }]);
  });
});
```

#### Store Testing

```typescript
// stores/user.test.ts
import { setActivePinia, createPinia } from 'pinia';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useUserStore } from '@/stores/user';

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('initializes with null user', () => {
    const store = useUserStore();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it('logs in user successfully', async () => {
    const store = useUserStore();

    // Mock API
    vi.mock('@/api', () => ({
      login: vi.fn().mockResolvedValue({
        data: {
          user: { id: 1, name: 'John' },
          token: 'abc123'
        }
      })
    }));

    await store.login('john@example.com', 'password');

    expect(store.user).toEqual({ id: 1, name: 'John' });
    expect(store.isAuthenticated).toBe(true);
  });
});
```

#### Composable Testing

```typescript
// composables/useCounter.test.ts
import { describe, it, expect } from 'vitest';
import { useCounter } from '@/composables/useCounter';

describe('useCounter', () => {
  it('increments count', () => {
    const { count, increment } = useCounter();

    expect(count.value).toBe(0);
    increment();
    expect(count.value).toBe(1);
  });

  it('accepts initial value', () => {
    const { count } = useCounter(10);
    expect(count.value).toBe(10);
  });
});
```

### 7. Accessibility (WCAG 2.1 AA)

#### Semantic HTML

```vue
<template>
  <!-- Use semantic elements -->
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>

  <main id="main-content">
    <article>
      <h1>Page Title</h1>
      <p>Content...</p>
    </article>
  </main>

  <!-- Form accessibility -->
  <form @submit.prevent="handleSubmit">
    <label for="email">Email:</label>
    <input
      id="email"
      v-model="email"
      type="email"
      required
      aria-describedby="email-error"
      :aria-invalid="emailError ? 'true' : 'false'"
    />
    <span id="email-error" role="alert" v-if="emailError">
      {{ emailError }}
    </span>
  </form>
</template>
```

#### ARIA Attributes

```vue
<script setup lang="ts">
const isOpen = ref(false);
const menuId = useId(); // Generate unique ID
</script>

<template>
  <!-- Button with ARIA -->
  <button
    @click="isOpen = !isOpen"
    :aria-expanded="isOpen"
    :aria-controls="menuId"
    aria-haspopup="true"
  >
    Menu
  </button>

  <!-- Menu with ARIA -->
  <ul
    :id="menuId"
    role="menu"
    :aria-hidden="!isOpen"
    v-show="isOpen"
  >
    <li role="menuitem">
      <a href="/profile">Profile</a>
    </li>
    <li role="menuitem">
      <a href="/settings">Settings</a>
    </li>
  </ul>

  <!-- Loading state -->
  <div v-if="isLoading" role="status" aria-live="polite">
    Loading...
  </div>
</template>
```

#### Keyboard Navigation

```vue
<script setup lang="ts">
const selectedIndex = ref(0);
const items = ref(['Item 1', 'Item 2', 'Item 3']);

function handleKeydown(event: KeyboardEvent) {
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault();
      selectedIndex.value = Math.min(
        selectedIndex.value + 1,
        items.value.length - 1
      );
      break;
    case 'ArrowUp':
      event.preventDefault();
      selectedIndex.value = Math.max(selectedIndex.value - 1, 0);
      break;
    case 'Enter':
      event.preventDefault();
      selectItem(selectedIndex.value);
      break;
  }
}
</script>

<template>
  <ul
    role="listbox"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <li
      v-for="(item, index) in items"
      :key="index"
      role="option"
      :aria-selected="index === selectedIndex"
      :tabindex="index === selectedIndex ? 0 : -1"
    >
      {{ item }}
    </li>
  </ul>
</template>
```

#### Focus Management

```vue
<script setup lang="ts">
import { ref, nextTick } from 'vue';

const modalOpen = ref(false);
const modalRef = ref<HTMLElement>();
const triggerRef = ref<HTMLElement>();

async function openModal() {
  modalOpen.value = true;
  await nextTick();
  modalRef.value?.focus();
}

function closeModal() {
  modalOpen.value = false;
  nextTick(() => {
    triggerRef.value?.focus(); // Return focus to trigger
  });
}

// Trap focus in modal
function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    closeModal();
  }

  if (event.key === 'Tab') {
    // Implement focus trap logic
    const focusableElements = modalRef.value?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    // Handle tab navigation within modal
  }
}
</script>

<template>
  <button ref="triggerRef" @click="openModal">
    Open Modal
  </button>

  <div
    v-if="modalOpen"
    ref="modalRef"
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    @keydown="handleKeydown"
  >
    <!-- Modal content -->
    <button @click="closeModal">Close</button>
  </div>
</template>
```

### 8. Security Best Practices

#### XSS Prevention

```vue
<script setup lang="ts">
import DOMPurify from 'dompurify';

const userInput = ref('');
const sanitizedHTML = computed(() => {
  return DOMPurify.sanitize(userInput.value, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
});
</script>

<template>
  <!-- NEVER use v-html with unsanitized user input -->
  <!-- ❌ Dangerous -->
  <div v-html="userInput"></div>

  <!-- ✅ Safe - sanitized -->
  <div v-html="sanitizedHTML"></div>

  <!-- ✅ Best - no v-html needed -->
  <div>{{ userInput }}</div>
</template>
```

#### Content Security Policy

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    headers: {
      'Content-Security-Policy': [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "font-src 'self'",
        "connect-src 'self' https://api.example.com"
      ].join('; ')
    }
  }
});
```

#### Secure API Communication

```typescript
// api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor - add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### Input Validation

```typescript
// composables/useForm.ts
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  age: z.number().min(18, 'Must be 18 or older')
});

export function useForm() {
  const errors = ref<Record<string, string>>({});

  function validate(data: unknown) {
    try {
      schema.parse(data);
      errors.value = {};
      return true;
    } catch (err) {
      if (err instanceof z.ZodError) {
        errors.value = err.errors.reduce((acc, error) => {
          acc[error.path[0]] = error.message;
          return acc;
        }, {} as Record<string, string>);
      }
      return false;
    }
  }

  return { errors, validate };
}
```

---

## Level 3: Deep Dive Resources

### Official Documentation

- [Vue 3 Documentation](https://vuejs.org/guide/introduction.html) - Official Vue 3 guide
- [Vue Router Documentation](https://router.vuejs.org/) - Official routing library
- [Pinia Documentation](https://pinia.vuejs.org/) - Official state management
- [Vitest Documentation](https://vitest.dev/) - Testing framework
- [Vue Test Utils](https://test-utils.vuejs.org/) - Component testing utilities

### Advanced Topics

- [Vue 3 Composition API RFC](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0013-composition-api.md) - Design rationale
- [VueUse](https://vueuse.org/) - Collection of composition utilities
- [Vue Macros](https://vue-macros.sxzz.moe/) - Experimental features
- [Nuxt 3](https://nuxt.com/) - Full-stack Vue framework
- [Vite](https://vitejs.dev/) - Next-generation build tool

### Performance & Optimization

- [Vue Performance Guide](https://vuejs.org/guide/best-practices/performance.html) - Official performance tips
- [Virtual Scrolling](https://github.com/tangbc/vue-virtual-scroll-list) - Large list optimization
- [Vue DevTools](https://devtools.vuejs.org/) - Performance profiling

### Accessibility

- [Vue A11y](https://vue-a11y.com/) - Vue accessibility resources
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) - W3C patterns
- [axe DevTools](https://www.deque.com/axe/devtools/) - Accessibility testing

### Security

- [OWASP Vue Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Vue_Security_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify) - XSS sanitization
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) - MDN guide

### Bundled Resources

- See `templates/composition-component.vue` - Complete component template
- See `templates/pinia-store.ts` - Pinia store template
- See `templates/component.test.ts` - Vitest test template
- See `config/vitest.config.ts` - Vitest configuration
- See `resources/accessibility-checklist.md` - WCAG 2.1 AA checklist
- See `resources/performance-checklist.md` - Performance optimization guide

---

**Note**: This skill focuses on Vue 3 Composition API, modern tooling (Vite, Vitest), and production-ready patterns. For options API or Vue 2, refer to the official migration guides.
