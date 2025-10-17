# Vue.js Performance Optimization Checklist

## Overview

This checklist provides actionable performance optimization techniques for Vue 3 applications.

## Build & Bundle Optimization

### Code Splitting

- [ ] Route-based lazy loading implemented
- [ ] Large components lazy loaded
- [ ] Third-party libraries code-split
- [ ] Dynamic imports used for heavy features

```typescript
// Route-based code splitting
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue')
  }
];

// Component lazy loading
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: LoadingSpinner,
  delay: 200,
  timeout: 10000
});
```

### Bundle Analysis

- [ ] Bundle size analyzed with `rollup-plugin-visualizer`
- [ ] Dependencies reviewed for size
- [ ] Tree-shaking verified
- [ ] Unused code eliminated

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    vue(),
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true
    })
  ]
});
```

### Manual Chunks

- [ ] Vendor code separated
- [ ] Common components bundled
- [ ] Large libraries isolated

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'ui-framework': ['element-plus'],
          'charts': ['chart.js', 'vue-chartjs'],
          'utils': ['lodash-es', 'dayjs']
        }
      }
    }
  }
});
```

## Rendering Optimization

### Virtual Scrolling

- [ ] Virtual scrolling for lists > 100 items
- [ ] Windowing library used (vue-virtual-scroller)
- [ ] Fixed item heights where possible

```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core';

const items = ref(Array.from({ length: 100000 }, (_, i) => `Item ${i}`));

const { list, containerProps, wrapperProps } = useVirtualList(
  items,
  { itemHeight: 50 }
);
</script>

<template>
  <div v-bind="containerProps" style="height: 600px;">
    <div v-bind="wrapperProps">
      <div v-for="{ data, index } in list" :key="index">
        {{ data }}
      </div>
    </div>
  </div>
</template>
```

### Memoization

- [ ] `v-memo` used for expensive list items
- [ ] `v-once` used for static content
- [ ] Computed properties cached properly
- [ ] Expensive functions memoized

```vue
<script setup lang="ts">
const items = ref([/* large array */]);

const expensiveComputation = (id: number) => {
  // Heavy calculation
  return result;
};
</script>

<template>
  <!-- v-memo: only update if dependencies change -->
  <div
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item.lastUpdated]"
  >
    {{ expensiveComputation(item.id) }}
  </div>
  
  <!-- v-once: render once, never update -->
  <footer v-once>
    <p>© 2025 Company Name</p>
  </footer>
</template>
```

### Deferred Content

- [ ] Below-fold content lazy loaded
- [ ] Images lazy loaded
- [ ] `<Suspense>` used for async components
- [ ] Critical CSS inlined

```vue
<script setup lang="ts">
import { useIntersectionObserver } from '@vueuse/core';

const target = ref(null);
const isVisible = ref(false);

useIntersectionObserver(
  target,
  ([{ isIntersecting }]) => {
    if (isIntersecting) {
      isVisible.value = true;
    }
  }
);
</script>

<template>
  <div ref="target">
    <HeavyComponent v-if="isVisible" />
  </div>
</template>
```

## Reactivity Optimization

### Shallow Reactivity

- [ ] `shallowRef` used for large objects
- [ ] `shallowReactive` used when deep reactivity not needed
- [ ] `readonly` used for immutable data

```typescript
// Large object - only track top level
const state = shallowReactive({
  user: { /* large nested object */ },
  settings: { /* large nested object */ }
});

// Array of objects - don't track each item
const items = shallowRef<Item[]>([]);

// Immutable data
const config = readonly({
  apiUrl: 'https://api.example.com',
  timeout: 10000
});
```

### Computed Caching

- [ ] Computeds used instead of methods for derived state
- [ ] Dependencies minimized
- [ ] Expensive computations cached

```typescript
// ❌ Bad: recalculates on every render
const displayName = () => {
  return firstName.value + ' ' + lastName.value;
};

// ✅ Good: cached until dependencies change
const displayName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});
```

### Watch Optimization

- [ ] `watchEffect` used instead of `watch` when appropriate
- [ ] Deep watches avoided when possible
- [ ] Flush timing optimized (`pre`, `post`, `sync`)

```typescript
// Avoid deep watching
// ❌ Bad
watch(state, () => { /* ... */ }, { deep: true });

// ✅ Good: watch specific properties
watch(() => state.user.name, () => { /* ... */ });

// Flush timing
watch(
  source,
  callback,
  { flush: 'post' } // Run after component updates
);
```

## Network Optimization

### API Calls

- [ ] Requests debounced/throttled
- [ ] Data cached when appropriate
- [ ] Request deduplication implemented
- [ ] Pagination used for large datasets

```typescript
import { useDebounceFn } from '@vueuse/core';

// Debounce search
const debouncedSearch = useDebounceFn(async (query: string) => {
  const results = await api.search(query);
  searchResults.value = results;
}, 300);

// Cache requests
const cache = new Map<string, any>();

async function fetchUser(id: string) {
  if (cache.has(id)) {
    return cache.get(id);
  }
  
  const user = await api.getUser(id);
  cache.set(id, user);
  return user;
}
```

### Prefetching

- [ ] Critical data prefetched
- [ ] Route data preloaded on hover
- [ ] Next page data prefetched

```typescript
// Prefetch on route enter
router.beforeEach(async (to) => {
  if (to.meta.prefetch) {
    await to.meta.prefetch();
  }
});

// Prefetch on hover
<template>
  <RouterLink
    to="/dashboard"
    @mouseenter="prefetchDashboard"
  >
    Dashboard
  </RouterLink>
</template>

<script setup lang="ts">
function prefetchDashboard() {
  // Preload component and data
  import('@/views/Dashboard.vue');
  dashboardStore.prefetchData();
}
</script>
```

## Image Optimization

### Lazy Loading

- [ ] Native lazy loading used (`loading="lazy"`)
- [ ] Intersection Observer for custom lazy loading
- [ ] Placeholder images shown during load

```vue
<template>
  <!-- Native lazy loading -->
  <img
    src="large-image.jpg"
    loading="lazy"
    alt="Description"
  />
  
  <!-- Custom lazy loading with placeholder -->
  <img
    :src="isLoaded ? actualSrc : placeholderSrc"
    @load="isLoaded = true"
  />
</template>
```

### Responsive Images

- [ ] `srcset` used for different screen sizes
- [ ] Modern formats (WebP, AVIF) provided
- [ ] Image dimensions specified

```vue
<template>
  <picture>
    <source
      type="image/avif"
      srcset="image-400.avif 400w, image-800.avif 800w"
    />
    <source
      type="image/webp"
      srcset="image-400.webp 400w, image-800.webp 800w"
    />
    <img
      src="image-800.jpg"
      srcset="image-400.jpg 400w, image-800.jpg 800w"
      sizes="(max-width: 600px) 400px, 800px"
      width="800"
      height="600"
      alt="Description"
    />
  </picture>
</template>
```

## State Management Optimization

### Pinia Optimization

- [ ] Stores split by feature
- [ ] Getters used for derived state
- [ ] Actions batch updates
- [ ] Unnecessary reactivity avoided

```typescript
export const useUserStore = defineStore('user', () => {
  // Split large stores
  const profile = ref<Profile | null>(null);
  const settings = ref<Settings>({});
  
  // Use getters for derived state
  const fullName = computed(() => {
    return profile.value
      ? `${profile.value.firstName} ${profile.value.lastName}`
      : '';
  });
  
  // Batch updates
  function updateProfile(updates: Partial<Profile>) {
    if (!profile.value) return;
    
    // Single update
    profile.value = {
      ...profile.value,
      ...updates
    };
  }
  
  return { profile, settings, fullName, updateProfile };
});
```

## Memory Management

### Cleanup

- [ ] Event listeners removed on unmount
- [ ] Timers cleared on unmount
- [ ] Observers disconnected on unmount
- [ ] Large data structures cleared when done

```typescript
onMounted(() => {
  const timer = setInterval(() => {
    // Do something
  }, 1000);
  
  const observer = new IntersectionObserver(() => {
    // Observe
  });
  
  onUnmounted(() => {
    clearInterval(timer);
    observer.disconnect();
  });
});
```

### Weak References

- [ ] WeakMap/WeakSet used for caches
- [ ] Large objects stored with weak references

```typescript
// Cache that allows garbage collection
const cache = new WeakMap<object, any>();

function getData(key: object) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const data = expensiveOperation(key);
  cache.set(key, data);
  return data;
}
```

## Testing Performance

### Profiling

- [ ] Vue DevTools performance tab used
- [ ] Chrome DevTools profiler used
- [ ] Lighthouse performance audit run
- [ ] Core Web Vitals monitored

```typescript
// Performance mark
performance.mark('component-mount-start');
// ... component logic
performance.mark('component-mount-end');

performance.measure(
  'component-mount',
  'component-mount-start',
  'component-mount-end'
);
```

### Benchmarking

- [ ] Critical paths benchmarked
- [ ] Performance regression tests
- [ ] Bundle size tracked in CI

```typescript
// vitest benchmark
import { bench, describe } from 'vitest';

describe('performance', () => {
  bench('expensive operation', () => {
    expensiveOperation();
  });
});
```

## Production Optimization

### Build Configuration

- [ ] Production mode enabled
- [ ] Source maps disabled or external
- [ ] Minification enabled
- [ ] Tree-shaking working

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: { /* ... */ }
      }
    }
  }
});
```

### CDN & Caching

- [ ] Static assets served from CDN
- [ ] Aggressive cache headers set
- [ ] Service worker for offline caching

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name].[hash][extname]',
        chunkFileNames: 'js/[name].[hash].js',
        entryFileNames: 'js/[name].[hash].js'
      }
    }
  }
});
```

## Monitoring

### Real User Monitoring

- [ ] Core Web Vitals tracked
- [ ] Error rates monitored
- [ ] Performance metrics logged

```typescript
// Track Core Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## Performance Budgets

### Targets (Mobile)

- [ ] First Contentful Paint < 1.8s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Time to Interactive < 3.8s
- [ ] Cumulative Layout Shift < 0.1
- [ ] First Input Delay < 100ms
- [ ] Bundle size < 200KB gzipped

### Tracking

```json
{
  "budgets": [
    {
      "path": "/*",
      "timings": [
        { "metric": "interactive", "budget": 3800 },
        { "metric": "first-contentful-paint", "budget": 1800 }
      ],
      "resourceSizes": [
        { "resourceType": "script", "budget": 200 },
        { "resourceType": "total", "budget": 500 }
      ]
    }
  ]
}
```

## Quick Wins

1. **Enable compression**: Gzip/Brotli on server
2. **Add loading states**: Skeleton screens, spinners
3. **Optimize fonts**: Font-display: swap, subset fonts
4. **Remove unused CSS**: PurgeCSS or similar
5. **Use CDN**: For static assets
6. **Enable HTTP/2**: Multiple requests in parallel
7. **Preload critical resources**: `<link rel="preload">`
8. **Defer non-critical JS**: `defer` or `async` attributes

## Resources

- [Vue Performance Guide](https://vuejs.org/guide/best-practices/performance.html)
- [Web.dev Performance](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Vite Performance](https://vitejs.dev/guide/performance.html)
