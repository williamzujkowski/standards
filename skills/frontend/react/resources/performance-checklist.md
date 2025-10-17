# React Performance Optimization Checklist

Comprehensive guide for optimizing React application performance.

## Rendering Optimization

### Component Memoization

- [ ] **Wrap expensive components in React.memo()**
  ```tsx
  const ExpensiveList = React.memo(({ items }) => {
    return items.map(item => <ListItem key={item.id} {...item} />);
  });
  ```

- [ ] **Use custom comparison for complex props**
  ```tsx
  const MyComponent = React.memo(
    Component,
    (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
  );
  ```

### Hook Optimization

- [ ] **Use useMemo for expensive calculations**
  ```tsx
  const sortedItems = useMemo(
    () => items.sort((a, b) => b.price - a.price),
    [items]
  );
  ```

- [ ] **Use useCallback for functions passed to children**
  ```tsx
  const handleClick = useCallback(() => {
    doSomething(id);
  }, [id]);
  ```

- [ ] **Avoid creating objects/arrays in render**
  ```tsx
  // Bad
  <Child config={{ option: true }} />

  // Good
  const config = useMemo(() => ({ option: true }), []);
  <Child config={config} />
  ```

### Virtual DOM Optimization

- [ ] **Provide stable keys for lists**
  ```tsx
  // Bad: index as key
  {items.map((item, i) => <Item key={i} {...item} />)}

  // Good: stable unique ID
  {items.map(item => <Item key={item.id} {...item} />)}
  ```

- [ ] **Avoid inline styles (creates new object every render)**
  ```tsx
  // Bad
  <div style={{ margin: 10 }} />

  // Good
  <div className="my-class" />
  ```

## Code Splitting

### Route-Based Splitting

- [ ] **Split routes with React.lazy()**
  ```tsx
  const Home = lazy(() => import('./pages/Home'));
  const Dashboard = lazy(() => import('./pages/Dashboard'));

  <Suspense fallback={<Loading />}>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Suspense>
  ```

### Component-Based Splitting

- [ ] **Lazy load heavy components**
  ```tsx
  const HeavyChart = lazy(() => import('./HeavyChart'));

  {showChart && (
    <Suspense fallback={<Skeleton />}>
      <HeavyChart data={data} />
    </Suspense>
  )}
  ```

### Dynamic Imports

- [ ] **Load modules on demand**
  ```tsx
  const loadEditor = async () => {
    const { Editor } = await import('./Editor');
    return Editor;
  };
  ```

## Bundle Optimization

### Analyze Bundle Size

- [ ] **Install webpack-bundle-analyzer**
  ```bash
  npm install --save-dev webpack-bundle-analyzer
  ```

- [ ] **Run analysis after build**
  ```bash
  npx webpack-bundle-analyzer build/bundle-stats.json
  ```

### Tree Shaking

- [ ] **Use ES6 imports (not CommonJS)**
  ```tsx
  // Good (tree-shakeable)
  import { Button } from './components';

  // Bad (imports entire module)
  const components = require('./components');
  ```

- [ ] **Import only what you need from libraries**
  ```tsx
  // Bad
  import _ from 'lodash';

  // Good
  import debounce from 'lodash/debounce';
  ```

### Production Build

- [ ] **Always deploy production builds**
  ```bash
  npm run build  # Not npm start!
  ```

- [ ] **Enable compression (gzip/brotli)**
  ```javascript
  // In server config or CDN
  compress: true
  ```

- [ ] **Set NODE_ENV=production**
  ```bash
  NODE_ENV=production npm run build
  ```

## Image Optimization

### Loading Strategies

- [ ] **Use lazy loading for images**
  ```tsx
  <img src="image.jpg" loading="lazy" alt="Description" />
  ```

- [ ] **Implement progressive image loading**
  ```tsx
  <img
    src="low-res.jpg"
    data-src="high-res.jpg"
    className="progressive"
  />
  ```

### Format Optimization

- [ ] **Use modern formats (WebP, AVIF)**
  ```tsx
  <picture>
    <source srcset="image.avif" type="image/avif" />
    <source srcset="image.webp" type="image/webp" />
    <img src="image.jpg" alt="Fallback" />
  </picture>
  ```

- [ ] **Serve responsive images**
  ```tsx
  <img
    srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
    sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
    src="medium.jpg"
    alt="Responsive"
  />
  ```

## List Optimization

### Virtual Scrolling

- [ ] **Use react-window for long lists**
  ```tsx
  import { FixedSizeList } from 'react-window';

  <FixedSizeList
    height={600}
    itemCount={10000}
    itemSize={35}
    width="100%"
  >
    {Row}
  </FixedSizeList>
  ```

### Pagination

- [ ] **Implement pagination or infinite scroll**
  ```tsx
  const [page, setPage] = useState(1);
  const { data } = useQuery(['items', page], () => fetchItems(page));
  ```

## State Management Optimization

### Context Optimization

- [ ] **Split contexts to avoid unnecessary re-renders**
  ```tsx
  // Bad: one large context
  <AppContext.Provider value={{ user, theme, locale, notifications }}>

  // Good: multiple focused contexts
  <UserContext.Provider value={user}>
    <ThemeContext.Provider value={theme}>
      <App />
    </ThemeContext.Provider>
  </UserContext.Provider>
  ```

### Server State vs Client State

- [ ] **Use React Query for server data**
  ```tsx
  // Handles caching, refetching, loading states
  const { data } = useQuery(['users'], fetchUsers);
  ```

- [ ] **Keep client state local when possible**
  ```tsx
  // Don't lift state unnecessarily
  const [filter, setFilter] = useState('');  // Keep local to component
  ```

## Network Optimization

### API Calls

- [ ] **Debounce search inputs**
  ```tsx
  const debouncedSearch = useDebounce(searchTerm, 300);
  useEffect(() => { api.search(debouncedSearch) }, [debouncedSearch]);
  ```

- [ ] **Cancel requests on unmount**
  ```tsx
  useEffect(() => {
    const controller = new AbortController();
    fetch(url, { signal: controller.signal });
    return () => controller.abort();
  }, []);
  ```

- [ ] **Batch API requests**
  ```tsx
  const results = await Promise.all([
    fetch('/api/users'),
    fetch('/api/posts'),
    fetch('/api/comments')
  ]);
  ```

### Caching

- [ ] **Enable HTTP caching headers**
  ```
  Cache-Control: public, max-age=31536000, immutable
  ```

- [ ] **Use service workers for offline support**

## Third-Party Libraries

### Audit Dependencies

- [ ] **Check bundle impact before adding libraries**
  ```bash
  npm install --save-dev bundle-analyzer
  ```

- [ ] **Use lighter alternatives when possible**
  - Moment.js (heavy) → date-fns or Day.js (light)
  - Lodash (full) → lodash-es (tree-shakeable)

### Dynamic Loading

- [ ] **Load third-party scripts asynchronously**
  ```tsx
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://third-party.com/widget.js';
    script.async = true;
    document.body.appendChild(script);
  }, []);
  ```

## Development Tools

### Profiling

- [ ] **Use React DevTools Profiler**
  1. Open React DevTools
  2. Go to Profiler tab
  3. Click record
  4. Interact with app
  5. Stop recording and analyze

- [ ] **Use Chrome Performance tab**
  - Record performance
  - Look for long tasks (>50ms)
  - Identify rendering bottlenecks

### Monitoring

- [ ] **Track Core Web Vitals**
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1

- [ ] **Use performance monitoring (Lighthouse, WebPageTest)**
  ```bash
  npm install -g lighthouse
  lighthouse https://yoursite.com
  ```

## Checklist Summary

Run through this checklist for each performance review:

1. ✅ React.memo on expensive components
2. ✅ useMemo/useCallback for optimization
3. ✅ Code splitting with lazy/Suspense
4. ✅ Bundle size analyzed and optimized
5. ✅ Images lazy loaded and optimized
6. ✅ Virtual scrolling for long lists
7. ✅ Context split to prevent re-renders
8. ✅ Production build deployed with compression
9. ✅ API calls debounced and canceled properly
10. ✅ Third-party libraries audited

## Performance Targets

- **Initial Load**: < 3 seconds
- **Time to Interactive**: < 5 seconds
- **Bundle Size**: < 200KB (gzipped)
- **Lighthouse Score**: > 90
- **Re-render Time**: < 16ms (60fps)

## Resources

- [React DevTools Profiler](https://react.dev/learn/react-developer-tools)
- [web.dev Performance](https://web.dev/performance/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [React Window](https://github.com/bvaughn/react-window)
