# React Accessibility Checklist (WCAG 2.1 AA)

Comprehensive accessibility checklist for React applications to meet WCAG 2.1 Level AA standards.

## Semantic HTML

### Structure

- [ ] **Use semantic HTML5 elements**

  ```tsx
  <header>
    <nav>
      <ul><li><a href="/">Home</a></li></ul>
    </nav>
  </header>

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

- [ ] **Avoid div soup - use meaningful elements**

  ```tsx
  // Bad
  <div className="header">
    <div className="nav">...</div>
  </div>

  // Good
  <header>
    <nav>...</nav>
  </header>
  ```

### Headings

- [ ] **Use heading hierarchy (h1 → h2 → h3)**

  ```tsx
  <h1>Page Title</h1>
    <h2>Section</h2>
      <h3>Subsection</h3>
  ```

- [ ] **Don't skip heading levels**

  ```tsx
  // Bad: h1 → h3 (skips h2)
  <h1>Title</h1>
  <h3>Subsection</h3>

  // Good
  <h1>Title</h1>
  <h2>Section</h2>
  <h3>Subsection</h3>
  ```

## Keyboard Navigation

### Focus Management

- [ ] **All interactive elements must be keyboard accessible**

  ```tsx
  // Buttons are naturally keyboard accessible
  <button onClick={handleClick}>Click me</button>

  // Divs are not - add role and keyboard handlers
  <div
    role="button"
    tabIndex={0}
    onClick={handleClick}
    onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  >
    Click me
  </div>
  ```

- [ ] **Manage focus for dynamic content**

  ```tsx
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.focus();
    }
  }, [isOpen]);

  return (
    <div
      ref={dialogRef}
      role="dialog"
      tabIndex={-1}
      aria-labelledby="dialog-title"
    >
      <h2 id="dialog-title">Confirm Action</h2>
      <button onClick={onClose}>Close</button>
    </div>
  );
  ```

### Tab Order

- [ ] **Ensure logical tab order**

  ```tsx
  // Use natural DOM order (preferred)
  <form>
    <input name="name" />
    <input name="email" />
    <button type="submit">Submit</button>
  </form>

  // Only use tabIndex if absolutely necessary
  <div tabIndex={0}>Focusable div</div>
  <div tabIndex={-1}>Programmatically focusable</div>
  ```

- [ ] **Skip links for main content**

  ```tsx
  <a href="#main-content" className="skip-link">
    Skip to main content
  </a>

  <main id="main-content">
    {/* Content */}
  </main>
  ```

### Keyboard Shortcuts

- [ ] **Implement common keyboard patterns**

  ```tsx
  // Escape to close modals
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Arrow keys for menus/tabs
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowRight') selectNextTab();
    if (e.key === 'ArrowLeft') selectPrevTab();
  };
  ```

## ARIA (Accessible Rich Internet Applications)

### When to Use ARIA

- [ ] **First Rule of ARIA: Don't use ARIA**

  ```tsx
  // Bad: unnecessary ARIA
  <button role="button">Click me</button>

  // Good: semantic HTML
  <button>Click me</button>
  ```

- [ ] **Use ARIA only when semantic HTML isn't enough**

  ```tsx
  // Dialog pattern (no native element)
  <div
    role="dialog"
    aria-labelledby="dialog-title"
    aria-describedby="dialog-desc"
    aria-modal="true"
  >
    <h2 id="dialog-title">Title</h2>
    <p id="dialog-desc">Description</p>
  </div>
  ```

### Common ARIA Attributes

- [ ] **aria-label for icon buttons**

  ```tsx
  <button aria-label="Close dialog">
    <XIcon />
  </button>
  ```

- [ ] **aria-labelledby for associating labels**

  ```tsx
  <div role="region" aria-labelledby="section-heading">
    <h2 id="section-heading">Section Title</h2>
  </div>
  ```

- [ ] **aria-describedby for additional context**

  ```tsx
  <input
    id="email"
    aria-describedby="email-hint"
  />
  <span id="email-hint">We'll never share your email</span>
  ```

- [ ] **aria-expanded for collapsible content**

  ```tsx
  <button
    aria-expanded={isOpen}
    aria-controls="menu"
    onClick={toggleMenu}
  >
    Menu
  </button>
  <div id="menu" hidden={!isOpen}>
    {/* Menu items */}
  </div>
  ```

- [ ] **aria-live for dynamic updates**

  ```tsx
  // Announcements
  <div role="alert" aria-live="assertive">
    {error && <p>{error}</p>}
  </div>

  // Status updates
  <div role="status" aria-live="polite">
    {message && <p>{message}</p>}
  </div>
  ```

### ARIA States

- [ ] **aria-invalid for form validation**

  ```tsx
  <input
    id="email"
    type="email"
    aria-invalid={!!errors.email}
    aria-describedby={errors.email ? 'email-error' : undefined}
  />
  {errors.email && (
    <span id="email-error" role="alert">{errors.email}</span>
  )}
  ```

- [ ] **aria-disabled vs disabled**

  ```tsx
  // Use disabled for interactive elements
  <button disabled={isLoading}>Submit</button>

  // Use aria-disabled if you need custom behavior
  <div
    role="button"
    aria-disabled={isLoading}
    onClick={isLoading ? undefined : handleClick}
  >
    Submit
  </div>
  ```

## Forms

### Labels

- [ ] **Every input must have a label**

  ```tsx
  // Explicit association (preferred)
  <label htmlFor="name">Name</label>
  <input id="name" type="text" />

  // Implicit association
  <label>
    Name
    <input type="text" />
  </label>
  ```

- [ ] **Use aria-label for inputs without visible labels**

  ```tsx
  <input
    type="search"
    aria-label="Search articles"
    placeholder="Search..."
  />
  ```

### Validation

- [ ] **Clear error messages**

  ```tsx
  function FormField({ id, label, error }: Props) {
    return (
      <div>
        <label htmlFor={id}>{label}</label>
        <input
          id={id}
          aria-invalid={!!error}
          aria-describedby={error ? `${id}-error` : undefined}
        />
        {error && (
          <span id={`${id}-error`} role="alert" className="error">
            {error}
          </span>
        )}
      </div>
    );
  }
  ```

- [ ] **Required field indicators**

  ```tsx
  <label htmlFor="email">
    Email <span aria-label="required">*</span>
  </label>
  <input id="email" type="email" required />
  ```

### Fieldsets

- [ ] **Group related inputs with fieldset**

  ```tsx
  <fieldset>
    <legend>Shipping Address</legend>
    <label htmlFor="street">Street</label>
    <input id="street" type="text" />
    <label htmlFor="city">City</label>
    <input id="city" type="text" />
  </fieldset>
  ```

## Color and Contrast

### Contrast Ratios (WCAG AA)

- [ ] **Text contrast: 4.5:1 minimum (normal text)**

  ```tsx
  // Good (7:1 contrast)
  <p style={{ color: '#000', backgroundColor: '#fff' }}>Text</p>

  // Bad (2.1:1 contrast)
  <p style={{ color: '#999', backgroundColor: '#fff' }}>Text</p>
  ```

- [ ] **Large text contrast: 3:1 minimum (18pt+ or 14pt+ bold)**

- [ ] **UI component contrast: 3:1 minimum (buttons, form borders)**

### Tools for Checking

- [ ] **Use browser DevTools contrast checker**
- [ ] **Use online tools: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)**
- [ ] **Run automated tests (axe-core, Lighthouse)**

### Don't Rely on Color Alone

- [ ] **Use multiple indicators**

  ```tsx
  // Bad: color only
  <span style={{ color: 'red' }}>Error</span>

  // Good: icon + color + text
  <span className="error">
    <ErrorIcon aria-hidden="true" />
    <span>Error: Invalid input</span>
  </span>
  ```

## Images and Media

### Alternative Text

- [ ] **Provide alt text for all images**

  ```tsx
  // Informative image
  <img src="chart.png" alt="Sales increased 25% in Q4" />

  // Decorative image
  <img src="decoration.png" alt="" />

  // Functional image (button)
  <button>
    <img src="save.png" alt="Save document" />
  </button>
  ```

- [ ] **Use empty alt for decorative images**

  ```tsx
  <img src="divider.png" alt="" role="presentation" />
  ```

### Video and Audio

- [ ] **Provide captions for videos**

  ```tsx
  <video controls>
    <source src="video.mp4" type="video/mp4" />
    <track kind="captions" src="captions.vtt" srcLang="en" label="English" />
  </video>
  ```

- [ ] **Provide transcripts for audio**

- [ ] **Don't autoplay media**

  ```tsx
  // Bad
  <video autoPlay />

  // Good
  <video controls />
  ```

## Screen Readers

### Testing

- [ ] **Test with screen readers**
  - NVDA (Windows, free)
  - JAWS (Windows, paid)
  - VoiceOver (Mac/iOS, built-in)
  - TalkBack (Android, built-in)

### Best Practices

- [ ] **Hide decorative elements from screen readers**

  ```tsx
  <span aria-hidden="true">→</span>
  <img src="decoration.png" alt="" aria-hidden="true" />
  ```

- [ ] **Provide screen reader-only text when needed**

  ```tsx
  <button>
    <span aria-hidden="true">×</span>
    <span className="sr-only">Close dialog</span>
  </button>
  ```

- [ ] **Use visually-hidden class for important info**

  ```tsx
  // CSS
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  ```

## Responsive and Mobile

### Touch Targets

- [ ] **Minimum touch target size: 44x44 pixels**

  ```css
  button {
    min-width: 44px;
    min-height: 44px;
  }
  ```

### Viewport

- [ ] **Set proper viewport meta tag**

  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  ```

- [ ] **Don't disable zoom**

  ```html
  <!-- Bad -->
  <meta name="viewport" content="user-scalable=no" />

  <!-- Good -->
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  ```

## Testing and Validation

### Automated Testing

- [ ] **Run axe-core in tests**

  ```tsx
  import { axe, toHaveNoViolations } from 'jest-axe';
  expect.extend(toHaveNoViolations);

  test('should have no accessibility violations', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  ```

- [ ] **Run Lighthouse accessibility audit**

  ```bash
  lighthouse https://yoursite.com --only-categories=accessibility
  ```

### Manual Testing

- [ ] **Keyboard-only navigation**
  - Unplug mouse and navigate with keyboard only
  - Check all interactive elements are reachable

- [ ] **Screen reader testing**
  - Test with at least one screen reader
  - Ensure all content is announced properly

- [ ] **Browser extensions**
  - [axe DevTools](https://www.deque.com/axe/devtools/)
  - [WAVE](https://wave.webaim.org/extension/)
  - [Lighthouse](https://developers.google.com/web/tools/lighthouse)

## Common Patterns

### Modal Dialog

```tsx
function AccessibleModal({ isOpen, onClose, title, children }: Props) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      modalRef.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 id="modal-title">{title}</h2>
        <div>{children}</div>
        <button onClick={onClose} aria-label="Close dialog">
          ×
        </button>
      </div>
    </div>
  );
}
```

### Dropdown Menu

```tsx
function AccessibleDropdown({ label, items }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      setIsOpen(false);
      buttonRef.current?.focus();
    }
  };

  return (
    <div>
      <button
        ref={buttonRef}
        aria-haspopup="true"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
      >
        {label}
      </button>
      {isOpen && (
        <ul role="menu" onKeyDown={handleKeyDown}>
          {items.map(item => (
            <li key={item.id} role="menuitem" tabIndex={0}>
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [React Accessibility Docs](https://react.dev/learn/accessibility)
