# Vue.js Accessibility Checklist (WCAG 2.1 AA)

## Overview

This checklist ensures your Vue.js application meets WCAG 2.1 Level AA accessibility standards.

## Perceivable

### Text Alternatives (1.1)

- [ ] All images have meaningful `alt` attributes
- [ ] Decorative images use `alt=""` or CSS backgrounds
- [ ] Icons have accessible labels via `aria-label` or visually hidden text
- [ ] SVGs include `<title>` and `<desc>` elements
- [ ] Complex images have extended descriptions

```vue
<template>
  <!-- Meaningful image -->
  <img src="user.jpg" alt="User profile photo" />

  <!-- Decorative image -->
  <img src="decoration.png" alt="" role="presentation" />

  <!-- Icon with label -->
  <button aria-label="Close dialog">
    <svg aria-hidden="true"><use href="#close-icon" /></svg>
  </button>
</template>
```

### Time-Based Media (1.2)

- [ ] Videos have captions/subtitles
- [ ] Audio content has transcripts
- [ ] Media players are keyboard accessible
- [ ] Media controls are clearly labeled

### Adaptable (1.3)

- [ ] Semantic HTML elements used (`<nav>`, `<main>`, `<article>`)
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Lists use `<ul>`, `<ol>`, `<dl>` appropriately
- [ ] Tables have proper structure (`<th>`, `scope`)
- [ ] Form inputs have associated `<label>` elements
- [ ] Related content is grouped with `<fieldset>` and `<legend>`

```vue
<template>
  <main id="main-content">
    <h1>Page Title</h1>

    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>

    <article>
      <h2>Article Title</h2>
      <p>Content...</p>
    </article>
  </main>
</template>
```

### Distinguishable (1.4)

- [ ] Color contrast ratio ≥ 4.5:1 for normal text
- [ ] Color contrast ratio ≥ 3:1 for large text (18pt+)
- [ ] Information not conveyed by color alone
- [ ] Text can be resized up to 200%
- [ ] No horizontal scrolling at 320px width
- [ ] Line spacing is at least 1.5x font size
- [ ] Paragraph spacing is at least 2x font size

```css
/* Good contrast examples */
.text-normal {
  color: #212121; /* Black text */
  background: #ffffff; /* White background - 16.1:1 ratio */
}

.text-large {
  font-size: 18pt;
  color: #595959; /* Gray text */
  background: #ffffff; /* White background - 4.6:1 ratio */
}
```

## Operable

### Keyboard Accessible (2.1)

- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Focus order is logical
- [ ] Skip links provided for navigation
- [ ] Keyboard shortcuts documented
- [ ] Custom components support Tab, Enter, Space, Arrow keys

```vue
<script setup lang="ts">
function handleKeydown(event: KeyboardEvent) {
  switch (event.key) {
    case 'Enter':
    case ' ':
      event.preventDefault();
      handleClick();
      break;
    case 'Escape':
      closeDialog();
      break;
    case 'ArrowDown':
      focusNext();
      break;
  }
}
</script>

<template>
  <div
    role="button"
    tabindex="0"
    @click="handleClick"
    @keydown="handleKeydown"
  >
    Accessible Button
  </div>
</template>
```

### Enough Time (2.2)

- [ ] Users can disable or extend time limits
- [ ] Auto-updating content can be paused
- [ ] No time-outs under 20 hours (or adjustable)
- [ ] Warnings before session timeout

### Seizures and Physical Reactions (2.3)

- [ ] No content flashes more than 3 times per second
- [ ] Animations can be paused or disabled
- [ ] Respect `prefers-reduced-motion`

```vue
<script setup lang="ts">
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;
</script>

<template>
  <div :class="{ 'animate': !prefersReducedMotion }">
    Content
  </div>
</template>

<style>
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
```

### Navigable (2.4)

- [ ] Skip to main content link provided
- [ ] Page titles are descriptive
- [ ] Focus order matches visual order
- [ ] Link text is descriptive (avoid "click here")
- [ ] Multiple ways to find pages (search, sitemap)
- [ ] Headings and labels are descriptive
- [ ] Focus indicator is visible

```vue
<template>
  <!-- Skip link -->
  <a href="#main-content" class="skip-link">
    Skip to main content
  </a>

  <nav aria-label="Main navigation">
    <!-- Navigation -->
  </nav>

  <main id="main-content">
    <!-- Content -->
  </main>
</template>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}

/* Visible focus indicator */
*:focus {
  outline: 2px solid #2196f3;
  outline-offset: 2px;
}
</style>
```

### Input Modalities (2.5)

- [ ] Pointer gestures have keyboard alternatives
- [ ] Touch targets are at least 44x44 CSS pixels
- [ ] Labels match visible text
- [ ] Motion actuation has alternative controls

## Understandable

### Readable (3.1)

- [ ] Page language set via `lang` attribute
- [ ] Language changes marked with `lang`
- [ ] Unusual words have definitions
- [ ] Abbreviations explained

```vue
<template>
  <html lang="en">
    <body>
      <p>The <abbr title="World Wide Web">WWW</abbr> was invented...</p>
      <p lang="fr">Bonjour le monde</p>
    </body>
  </html>
</template>
```

### Predictable (3.2)

- [ ] Navigation is consistent across pages
- [ ] Components behave consistently
- [ ] Focus doesn't trigger unexpected changes
- [ ] Input doesn't cause unexpected changes
- [ ] Help is available in consistent location

### Input Assistance (3.3)

- [ ] Form errors identified clearly
- [ ] Labels and instructions provided
- [ ] Error suggestions provided
- [ ] Error prevention for critical actions
- [ ] Confirmation for data submission

```vue
<script setup lang="ts">
const email = ref('');
const emailError = ref('');

function validateEmail() {
  if (!email.value.includes('@')) {
    emailError.value = 'Please enter a valid email address';
  } else {
    emailError.value = '';
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <label for="email">Email:</label>
    <input
      id="email"
      v-model="email"
      type="email"
      required
      aria-describedby="email-error"
      :aria-invalid="!!emailError"
      @blur="validateEmail"
    />

    <span id="email-error" role="alert" v-if="emailError">
      {{ emailError }}
    </span>

    <button type="submit">Submit</button>
  </form>
</template>
```

## Robust

### Compatible (4.1)

- [ ] Valid HTML (no duplicate IDs, proper nesting)
- [ ] Name, role, value provided for custom components
- [ ] Status messages identifiable by screen readers
- [ ] ARIA roles used correctly
- [ ] ARIA states and properties valid

```vue
<template>
  <!-- Custom dropdown -->
  <div>
    <button
      :aria-expanded="isOpen"
      aria-haspopup="listbox"
      aria-controls="dropdown-list"
      @click="toggle"
    >
      Select option
    </button>

    <ul
      id="dropdown-list"
      role="listbox"
      :aria-hidden="!isOpen"
      v-show="isOpen"
    >
      <li role="option" :aria-selected="selected === 1">
        Option 1
      </li>
    </ul>
  </div>

  <!-- Status message -->
  <div role="status" aria-live="polite">
    {{ statusMessage }}
  </div>
</template>
```

## Testing Tools

### Automated Testing

- [ ] axe DevTools browser extension
- [ ] WAVE accessibility checker
- [ ] Lighthouse accessibility audit
- [ ] Pa11y or axe-core in CI/CD

```typescript
// vitest test with axe-core
import { axe } from 'vitest-axe';

it('has no accessibility violations', async () => {
  const wrapper = mount(MyComponent);
  const results = await axe(wrapper.element);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing

- [ ] Keyboard-only navigation test
- [ ] Screen reader test (NVDA, JAWS, VoiceOver)
- [ ] Zoom to 200% test
- [ ] Color contrast check
- [ ] Focus indicator visibility
- [ ] Form error handling
- [ ] Mobile touch target size

### Screen Reader Testing Commands

**NVDA (Windows)**
- `Insert + Down Arrow` - Read next line
- `Insert + Space` - Switch mode
- `H` - Next heading
- `Tab` - Next focusable element

**VoiceOver (Mac)**
- `VO + A` - Read all
- `VO + Right/Left Arrow` - Navigate
- `VO + H` - Next heading
- `Tab` - Next focusable element

**JAWS (Windows)**
- `Insert + Down Arrow` - Say all
- `H` - Next heading
- `T` - Next table
- `Tab` - Next link/button

## Common Issues & Solutions

### Issue: Focus not visible
**Solution**: Add clear focus styles
```css
*:focus {
  outline: 2px solid #2196f3;
  outline-offset: 2px;
}
```

### Issue: Screen reader can't read dynamic content
**Solution**: Use `aria-live` regions
```vue
<div aria-live="polite" role="status">
  {{ dynamicMessage }}
</div>
```

### Issue: Custom controls not keyboard accessible
**Solution**: Add keyboard event handlers
```vue
<div
  role="button"
  tabindex="0"
  @click="handleClick"
  @keydown.enter="handleClick"
  @keydown.space.prevent="handleClick"
>
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Vue A11y](https://vue-a11y.com/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM](https://webaim.org/)
