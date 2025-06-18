# Web Design and UX Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** WD

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Design Principles and Philosophy](#1-design-principles-and-philosophy)
2. [Visual Design Standards](#2-visual-design-standards)
3. [Typography and Content Layout](#3-typography-and-content-layout)
4. [Color Systems and Theming](#4-color-systems-and-theming)
5. [Component Design Systems](#5-component-design-systems)
6. [Interaction and Animation](#6-interaction-and-animation)
7. [Responsive and Adaptive Design](#7-responsive-and-adaptive-design)
8. [User Experience Patterns](#8-user-experience-patterns)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Design Principles and Philosophy

### 1.1 Core Design Principles

#### User-Centered Design **[REQUIRED]**
```yaml
# Core UX principles
user_centered_design:
  principles:
    clarity:
      description: "Interface should be self-explanatory"
      guidelines:
        - Use clear, concise language
        - Provide visual hierarchy
        - Minimize cognitive load
        - Show system status clearly

    consistency:
      description: "Predictable patterns and behaviors"
      guidelines:
        - Maintain pattern consistency
        - Use standard UI conventions
        - Keep terminology uniform
        - Align with platform guidelines

    efficiency:
      description: "Enable users to accomplish tasks quickly"
      guidelines:
        - Minimize steps to completion
        - Provide keyboard shortcuts
        - Remember user preferences
        - Offer smart defaults

    feedback:
      description: "Communicate system state and actions"
      guidelines:
        - Immediate response to actions
        - Clear error messages
        - Progress indicators
        - Success confirmations

    accessibility:
      description: "Usable by everyone"
      guidelines:
        - WCAG 2.1 AA compliance minimum
        - Keyboard navigation support
        - Screen reader compatibility
        - Color contrast requirements
```

#### Design Process Standards **[REQUIRED]**
```yaml
# Design workflow standards
design_process:
  phases:
    research:
      activities:
        - User interviews
        - Competitive analysis
        - Analytics review
        - Stakeholder input
      deliverables:
        - User personas
        - Journey maps
        - Problem statements
        - Success metrics

    ideation:
      activities:
        - Sketching sessions
        - Design workshops
        - Concept exploration
        - Information architecture
      deliverables:
        - Concept sketches
        - User flows
        - Site maps
        - Wireframes

    design:
      activities:
        - Visual design
        - Interaction design
        - Prototyping
        - Design system creation
      deliverables:
        - High-fidelity mockups
        - Interactive prototypes
        - Design specifications
        - Component library

    validation:
      activities:
        - Usability testing
        - A/B testing
        - Accessibility audit
        - Performance testing
      deliverables:
        - Test results
        - Improvement recommendations
        - Final designs
        - Handoff documentation
```

### 1.2 Design System Governance

#### System Architecture **[REQUIRED]**
```typescript
// design-system/core/types.ts
export interface DesignToken {
  name: string;
  value: string | number;
  type: 'color' | 'spacing' | 'typography' | 'shadow' | 'radius';
  category: string;
  description?: string;
  deprecated?: boolean;
}

export interface ComponentSpec {
  name: string;
  version: string;
  status: 'draft' | 'beta' | 'stable' | 'deprecated';
  props: PropDefinition[];
  variants: VariantDefinition[];
  examples: ExampleDefinition[];
  accessibility: AccessibilitySpec;
  guidelines: UsageGuidelines;
}

export interface DesignSystem {
  version: string;
  tokens: Map<string, DesignToken>;
  components: Map<string, ComponentSpec>;
  patterns: Map<string, PatternDefinition>;
  guidelines: DesignGuidelines;
}
```

#### Version Control **[RECOMMENDED]**
```json
// design-system/package.json
{
  "name": "@company/design-system",
  "version": "2.0.0",
  "exports": {
    "./tokens": "./dist/tokens/index.js",
    "./components": "./dist/components/index.js",
    "./styles": "./dist/styles/index.css"
  },
  "peerDependencies": {
    "react": ">=16.8.0",
    "styled-components": ">=5.0.0"
  },
  "designSystem": {
    "tokensVersion": "2.0.0",
    "componentsVersion": "2.0.0",
    "documentationUrl": "https://design.company.com",
    "migrationGuide": "./MIGRATION.md"
  }
}
```

---

## 2. Visual Design Standards

### 2.1 Grid Systems

#### Layout Grid **[REQUIRED]**
```scss
// styles/grid.scss
// 12-column grid system with responsive breakpoints
$grid-columns: 12;
$grid-gutter-width: 24px;
$grid-outer-margin: 24px;

// Breakpoint definitions
$breakpoints: (
  xs: 0,      // Mobile portrait
  sm: 576px,  // Mobile landscape
  md: 768px,  // Tablet portrait
  lg: 992px,  // Tablet landscape / Desktop
  xl: 1200px, // Desktop
  xxl: 1400px // Large desktop
);

// Container max-widths
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1140px,
  xxl: 1320px
);

// Grid mixin
@mixin make-grid($columns: $grid-columns, $gutter: $grid-gutter-width) {
  display: grid;
  grid-template-columns: repeat($columns, 1fr);
  gap: $gutter;

  @each $breakpoint, $value in $breakpoints {
    @media (min-width: $value) {
      &.grid-#{$breakpoint} {
        grid-template-columns: repeat(var(--grid-cols-#{$breakpoint}, $columns), 1fr);
      }
    }
  }
}

// Layout regions
.layout {
  &__header {
    grid-column: 1 / -1;
    min-height: 64px;
  }

  &__sidebar {
    grid-column: span 3;

    @media (max-width: map-get($breakpoints, md)) {
      grid-column: 1 / -1;
    }
  }

  &__main {
    grid-column: span 9;

    @media (max-width: map-get($breakpoints, md)) {
      grid-column: 1 / -1;
    }
  }
}
```

#### Spacing System **[REQUIRED]**
```scss
// styles/spacing.scss
// Base unit: 8px for consistent spatial rhythm
$spacing-unit: 8px;

// Spacing scale
$spacing: (
  0: 0,
  1: $spacing-unit * 0.5,   // 4px
  2: $spacing-unit,         // 8px
  3: $spacing-unit * 1.5,   // 12px
  4: $spacing-unit * 2,     // 16px
  5: $spacing-unit * 3,     // 24px
  6: $spacing-unit * 4,     // 32px
  7: $spacing-unit * 5,     // 40px
  8: $spacing-unit * 6,     // 48px
  9: $spacing-unit * 8,     // 64px
  10: $spacing-unit * 10,   // 80px
  11: $spacing-unit * 12,   // 96px
  12: $spacing-unit * 16    // 128px
);

// Spacing utilities
@each $name, $value in $spacing {
  // Margin utilities
  .m-#{$name} { margin: $value; }
  .mt-#{$name} { margin-top: $value; }
  .mr-#{$name} { margin-right: $value; }
  .mb-#{$name} { margin-bottom: $value; }
  .ml-#{$name} { margin-left: $value; }
  .mx-#{$name} { margin-left: $value; margin-right: $value; }
  .my-#{$name} { margin-top: $value; margin-bottom: $value; }

  // Padding utilities
  .p-#{$name} { padding: $value; }
  .pt-#{$name} { padding-top: $value; }
  .pr-#{$name} { padding-right: $value; }
  .pb-#{$name} { padding-bottom: $value; }
  .pl-#{$name} { padding-left: $value; }
  .px-#{$name} { padding-left: $value; padding-right: $value; }
  .py-#{$name} { padding-top: $value; padding-bottom: $value; }

  // Gap utilities
  .gap-#{$name} { gap: $value; }
}
```

### 2.2 Visual Hierarchy

#### Depth and Elevation **[REQUIRED]**
```scss
// styles/elevation.scss
// Material Design inspired elevation system
$shadows: (
  0: none,
  1: (0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)),
  2: (0 3px 6px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12)),
  3: (0 10px 20px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.10)),
  4: (0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22)),
  5: (0 19px 38px rgba(0, 0, 0, 0.30), 0 15px 12px rgba(0, 0, 0, 0.22))
);

// Elevation mixins
@mixin elevation($level) {
  @if map-has-key($shadows, $level) {
    box-shadow: map-get($shadows, $level);
  } @else {
    @warn "Invalid elevation level: #{$level}";
  }
}

// Component elevation standards
.card {
  @include elevation(1);
  transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    @include elevation(3);
  }
}

.modal {
  @include elevation(5);
}

.dropdown {
  @include elevation(2);
}

.tooltip {
  @include elevation(2);
}
```

#### Z-Index Management **[REQUIRED]**
```scss
// styles/z-index.scss
// Centralized z-index management
$z-layers: (
  base: 0,
  dropdown: 1000,
  sticky: 1100,
  fixed: 1200,
  modal-backdrop: 1300,
  modal: 1400,
  popover: 1500,
  tooltip: 1600,
  notification: 1700,
  debug: 9999
);

// Z-index function
@function z($layer) {
  @if map-has-key($z-layers, $layer) {
    @return map-get($z-layers, $layer);
  } @else {
    @warn "Invalid z-index layer: #{$layer}";
    @return 0;
  }
}

// Usage examples
.header--sticky {
  position: sticky;
  z-index: z(sticky);
}

.modal {
  z-index: z(modal);

  &__backdrop {
    z-index: z(modal-backdrop);
  }
}
```

---

## 3. Typography and Content Layout

### 3.1 Typography System

#### Type Scale **[REQUIRED]**
```scss
// styles/typography.scss
// Modular type scale (1.250 - Major Third)
$type-scale-ratio: 1.250;
$type-base-size: 16px;

// Font families
$font-families: (
  sans: (-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif),
  serif: (Georgia, Cambria, "Times New Roman", Times, serif),
  mono: (SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace)
);

// Type scale
$type-scale: (
  xs: $type-base-size / pow($type-scale-ratio, 2),    // 10.24px
  sm: $type-base-size / $type-scale-ratio,            // 12.8px
  base: $type-base-size,                              // 16px
  md: $type-base-size * $type-scale-ratio,            // 20px
  lg: $type-base-size * pow($type-scale-ratio, 2),    // 25px
  xl: $type-base-size * pow($type-scale-ratio, 3),    // 31.25px
  2xl: $type-base-size * pow($type-scale-ratio, 4),   // 39.06px
  3xl: $type-base-size * pow($type-scale-ratio, 5),   // 48.83px
  4xl: $type-base-size * pow($type-scale-ratio, 6)    // 61.04px
);

// Line heights
$line-heights: (
  tight: 1.2,
  snug: 1.375,
  normal: 1.5,
  relaxed: 1.625,
  loose: 2
);

// Font weights
$font-weights: (
  thin: 100,
  light: 300,
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
  black: 900
);

// Typography mixins
@mixin text-style($size: base, $weight: normal, $line-height: normal) {
  font-size: map-get($type-scale, $size);
  font-weight: map-get($font-weights, $weight);
  line-height: map-get($line-heights, $line-height);
}

// Heading styles
h1, .h1 {
  @include text-style(3xl, bold, tight);
  margin-bottom: map-get($spacing, 4);
}

h2, .h2 {
  @include text-style(2xl, semibold, tight);
  margin-bottom: map-get($spacing, 3);
}

h3, .h3 {
  @include text-style(xl, semibold, snug);
  margin-bottom: map-get($spacing, 3);
}

h4, .h4 {
  @include text-style(lg, medium, snug);
  margin-bottom: map-get($spacing, 2);
}

h5, .h5 {
  @include text-style(md, medium, normal);
  margin-bottom: map-get($spacing, 2);
}

h6, .h6 {
  @include text-style(base, medium, normal);
  margin-bottom: map-get($spacing, 2);
}

// Body text
p {
  @include text-style(base, normal, relaxed);
  margin-bottom: map-get($spacing, 4);
}

// Text utilities
.text-xs { font-size: map-get($type-scale, xs); }
.text-sm { font-size: map-get($type-scale, sm); }
.text-base { font-size: map-get($type-scale, base); }
.text-lg { font-size: map-get($type-scale, lg); }
.text-xl { font-size: map-get($type-scale, xl); }
```

#### Readable Content **[REQUIRED]**
```scss
// styles/content.scss
// Optimal reading experience standards

// Maximum line length for readability
$max-line-length: 65ch;
$comfortable-line-length: 45-75ch;

// Content container
.content {
  max-width: $max-line-length;
  margin-left: auto;
  margin-right: auto;

  // Responsive font sizing
  font-size: clamp(
    map-get($type-scale, base),
    2.5vw,
    map-get($type-scale, md)
  );

  // Paragraph spacing
  p + p {
    margin-top: map-get($spacing, 4);
  }

  // List styling
  ul, ol {
    margin-bottom: map-get($spacing, 4);
    padding-left: map-get($spacing, 5);

    li {
      margin-bottom: map-get($spacing, 2);
    }
  }

  // Blockquote styling
  blockquote {
    margin: map-get($spacing, 6) 0;
    padding-left: map-get($spacing, 4);
    border-left: 4px solid var(--color-primary);
    font-style: italic;
  }

  // Code blocks
  pre {
    margin: map-get($spacing, 4) 0;
    padding: map-get($spacing, 4);
    background-color: var(--color-code-bg);
    border-radius: var(--radius-md);
    overflow-x: auto;
  }

  // Inline code
  code {
    padding: 2px 4px;
    background-color: var(--color-code-bg);
    border-radius: var(--radius-sm);
    font-family: map-get($font-families, mono);
    font-size: 0.875em;
  }
}

// Responsive typography
@media (max-width: map-get($breakpoints, sm)) {
  .content {
    font-size: map-get($type-scale, base);
  }

  h1, .h1 { @include text-style(2xl, bold, tight); }
  h2, .h2 { @include text-style(xl, semibold, tight); }
  h3, .h3 { @include text-style(lg, semibold, snug); }
}
```

### 3.2 Content Patterns

#### Card Layouts **[REQUIRED]**
```scss
// components/card.scss
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  @include elevation(1);
  overflow: hidden;
  transition: all 0.3s ease;

  &__media {
    position: relative;
    padding-bottom: 56.25%; // 16:9 aspect ratio
    overflow: hidden;

    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: map-get($spacing, 5);
  }

  &__title {
    @include text-style(lg, semibold, snug);
    margin-bottom: map-get($spacing, 2);
  }

  &__description {
    @include text-style(base, normal, normal);
    color: var(--color-text-secondary);
    margin-bottom: map-get($spacing, 4);
  }

  &__actions {
    display: flex;
    gap: map-get($spacing, 3);
    margin-top: auto;
  }

  // Interactive states
  &--interactive {
    cursor: pointer;

    &:hover {
      @include elevation(3);
      transform: translateY(-2px);
    }

    &:active {
      @include elevation(1);
      transform: translateY(0);
    }
  }
}
```

#### Data Tables **[REQUIRED]**
```scss
// components/table.scss
.table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);

  &__header {
    background: var(--color-surface-variant);
    border-bottom: 2px solid var(--color-border);
  }

  &__row {
    border-bottom: 1px solid var(--color-border-light);

    &:hover {
      background: var(--color-surface-hover);
    }

    &--selected {
      background: var(--color-surface-selected);
    }
  }

  &__cell {
    padding: map-get($spacing, 3) map-get($spacing, 4);
    text-align: left;

    &--numeric {
      text-align: right;
      font-feature-settings: "tnum" 1; // Tabular numbers
    }

    &--actions {
      text-align: right;
      white-space: nowrap;
    }
  }

  &__header-cell {
    @extend .table__cell;
    @include text-style(sm, semibold, normal);
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  // Responsive table
  @media (max-width: map-get($breakpoints, md)) {
    &--responsive {
      display: block;

      .table__header {
        display: none;
      }

      .table__row {
        display: block;
        margin-bottom: map-get($spacing, 4);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
      }

      .table__cell {
        display: flex;
        justify-content: space-between;

        &::before {
          content: attr(data-label);
          font-weight: map-get($font-weights, semibold);
        }
      }
    }
  }
}
```

---

## 4. Color Systems and Theming

### 4.1 Color Architecture

#### Color Tokens **[REQUIRED]**
```scss
// styles/colors.scss
// Semantic color system with light/dark theme support

// Brand colors
$brand-colors: (
  primary: #1976d2,
  primary-light: #42a5f5,
  primary-dark: #1565c0,
  secondary: #dc004e,
  secondary-light: #e33371,
  secondary-dark: #9a0036
);

// Neutral palette
$neutral-colors: (
  0: #ffffff,
  50: #fafafa,
  100: #f5f5f5,
  200: #eeeeee,
  300: #e0e0e0,
  400: #bdbdbd,
  500: #9e9e9e,
  600: #757575,
  700: #616161,
  800: #424242,
  900: #212121,
  1000: #000000
);

// Semantic colors
$semantic-colors: (
  success: #4caf50,
  success-light: #80e27e,
  success-dark: #087f23,
  warning: #ff9800,
  warning-light: #ffcc80,
  warning-dark: #c66900,
  error: #f44336,
  error-light: #ff7961,
  error-dark: #ba000d,
  info: #2196f3,
  info-light: #6ec6ff,
  info-dark: #0069c0
);

// Theme definitions
:root {
  // Light theme (default)
  --color-primary: #{map-get($brand-colors, primary)};
  --color-primary-light: #{map-get($brand-colors, primary-light)};
  --color-primary-dark: #{map-get($brand-colors, primary-dark)};
  --color-secondary: #{map-get($brand-colors, secondary)};

  --color-background: #{map-get($neutral-colors, 50)};
  --color-surface: #{map-get($neutral-colors, 0)};
  --color-surface-variant: #{map-get($neutral-colors, 100)};

  --color-text-primary: #{map-get($neutral-colors, 900)};
  --color-text-secondary: #{map-get($neutral-colors, 600)};
  --color-text-disabled: #{map-get($neutral-colors, 400)};

  --color-border: #{map-get($neutral-colors, 300)};
  --color-border-light: #{map-get($neutral-colors, 200)};

  --color-success: #{map-get($semantic-colors, success)};
  --color-warning: #{map-get($semantic-colors, warning)};
  --color-error: #{map-get($semantic-colors, error)};
  --color-info: #{map-get($semantic-colors, info)};
}

// Dark theme
[data-theme="dark"] {
  --color-background: #{map-get($neutral-colors, 900)};
  --color-surface: #{map-get($neutral-colors, 800)};
  --color-surface-variant: #{map-get($neutral-colors, 700)};

  --color-text-primary: #{map-get($neutral-colors, 50)};
  --color-text-secondary: #{map-get($neutral-colors, 300)};
  --color-text-disabled: #{map-get($neutral-colors, 600)};

  --color-border: #{map-get($neutral-colors, 700)};
  --color-border-light: #{map-get($neutral-colors, 800)};

  --color-success: #{map-get($semantic-colors, success-light)};
  --color-warning: #{map-get($semantic-colors, warning-light)};
  --color-error: #{map-get($semantic-colors, error-light)};
  --color-info: #{map-get($semantic-colors, info-light)};
}
```

#### Color Contrast **[REQUIRED]**
```typescript
// utils/color-contrast.ts
// WCAG 2.1 contrast ratio calculations

interface ColorContrastResult {
  ratio: number;
  level: 'AAA' | 'AA' | 'FAIL';
  largeTextLevel: 'AAA' | 'AA' | 'FAIL';
}

export function calculateContrast(
  foreground: string,
  background: string
): ColorContrastResult {
  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);

  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

  // WCAG 2.1 Level AA: 4.5:1 for normal text, 3:1 for large text
  // WCAG 2.1 Level AAA: 7:1 for normal text, 4.5:1 for large text
  const level = ratio >= 7 ? 'AAA' : ratio >= 4.5 ? 'AA' : 'FAIL';
  const largeTextLevel = ratio >= 4.5 ? 'AAA' : ratio >= 3 ? 'AA' : 'FAIL';

  return { ratio, level, largeTextLevel };
}

function getLuminance(color: string): number {
  const rgb = hexToRgb(color);
  const [r, g, b] = rgb.map(val => {
    val = val / 255;
    return val <= 0.03928
      ? val / 12.92
      : Math.pow((val + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Color validation utilities
export const colorValidation = {
  checkTextContrast(text: string, background: string): boolean {
    const result = calculateContrast(text, background);
    return result.level !== 'FAIL';
  },

  checkLargeTextContrast(text: string, background: string): boolean {
    const result = calculateContrast(text, background);
    return result.largeTextLevel !== 'FAIL';
  },

  suggestAccessibleColor(
    baseColor: string,
    background: string,
    targetRatio: number = 4.5
  ): string {
    // Implementation to adjust color until target ratio is met
    // ...
  }
};
```

### 4.2 Theme Management

#### Theme Provider **[REQUIRED]**
```typescript
// theme/ThemeProvider.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface Theme {
  name: 'light' | 'dark' | 'auto';
  colors: ThemeColors;
  typography: ThemeTypography;
  spacing: ThemeSpacing;
  breakpoints: ThemeBreakpoints;
}

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme['name']) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  const [theme, setThemeState] = useState<Theme['name']>('auto');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme['name'];
    if (savedTheme) {
      setThemeState(savedTheme);
    }

    // Handle system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      if (theme === 'auto') {
        document.documentElement.setAttribute(
          'data-theme',
          e.matches ? 'dark' : 'light'
        );
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const setTheme = (newTheme: Theme['name']) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);

    if (newTheme === 'auto') {
      const prefersDark = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches;
      document.documentElement.setAttribute(
        'data-theme',
        prefersDark ? 'dark' : 'light'
      );
    } else {
      document.documentElement.setAttribute('data-theme', newTheme);
    }
  };

  const toggleTheme = () => {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(nextTheme);
  };

  return (
    <ThemeContext.Provider
      value={{
        theme: getThemeObject(theme),
        setTheme,
        toggleTheme,
      }}
    >
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

## 5. Component Design Systems

### 5.1 Component Architecture

#### Component Structure **[REQUIRED]**
```typescript
// components/Button/Button.tsx
import React, { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './Button.module.scss';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'medium',
      fullWidth = false,
      loading = false,
      icon,
      iconPosition = 'left',
      children,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={clsx(
          styles.button,
          styles[`button--${variant}`],
          styles[`button--${size}`],
          {
            [styles['button--full-width']]: fullWidth,
            [styles['button--loading']]: loading,
            [styles['button--disabled']]: disabled || loading,
            [styles['button--icon-only']]: icon && !children,
          },
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <span className={styles.button__spinner} aria-hidden="true">
            <Spinner size={size} />
          </span>
        )}
        {icon && iconPosition === 'left' && (
          <span className={styles.button__icon} aria-hidden="true">
            {icon}
          </span>
        )}
        {children && <span className={styles.button__text}>{children}</span>}
        {icon && iconPosition === 'right' && (
          <span className={styles.button__icon} aria-hidden="true">
            {icon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

#### Component Documentation **[REQUIRED]**
```typescript
// components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { IconSave, IconDelete } from '../Icons';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    docs: {
      description: {
        component: `
A button triggers an action or event when activated.

## When to use
- **Primary actions**: Use primary buttons for the main action on a page
- **Secondary actions**: Use secondary buttons for less important actions
- **Dangerous actions**: Use danger buttons for destructive actions
- **Ghost buttons**: Use ghost buttons for tertiary actions

## Accessibility
- All buttons must have accessible labels
- Use aria-label for icon-only buttons
- Ensure sufficient color contrast
- Support keyboard navigation
        `,
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost', 'danger'],
      description: 'Visual style variant',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Button size',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const WithIcon: Story = {
  args: {
    children: 'Save',
    icon: <IconSave />,
    variant: 'primary',
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading',
    loading: true,
    variant: 'primary',
  },
};

export const IconOnly: Story = {
  args: {
    icon: <IconDelete />,
    variant: 'danger',
    'aria-label': 'Delete item',
  },
};

export const ButtonGroup: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px' }}>
      <Button variant="secondary">Cancel</Button>
      <Button variant="primary">Save</Button>
    </div>
  ),
};
```

### 5.2 Component Patterns

#### Form Components **[REQUIRED]**
```scss
// components/forms.scss
// Consistent form component styling

.form-field {
  margin-bottom: map-get($spacing, 5);

  &__label {
    display: block;
    margin-bottom: map-get($spacing, 2);
    @include text-style(sm, medium, normal);
    color: var(--color-text-primary);

    &--required::after {
      content: " *";
      color: var(--color-error);
    }
  }

  &__input {
    width: 100%;
    padding: map-get($spacing, 3) map-get($spacing, 4);
    font-size: map-get($type-scale, base);
    line-height: map-get($line-heights, normal);
    color: var(--color-text-primary);
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    transition: all 0.2s ease;

    &:hover:not(:disabled) {
      border-color: var(--color-border-hover);
    }

    &:focus {
      outline: none;
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
    }

    &:disabled {
      background-color: var(--color-surface-disabled);
      color: var(--color-text-disabled);
      cursor: not-allowed;
    }

    &--error {
      border-color: var(--color-error);

      &:focus {
        box-shadow: 0 0 0 3px rgba(var(--color-error-rgb), 0.2);
      }
    }
  }

  &__help {
    margin-top: map-get($spacing, 2);
    @include text-style(sm, normal, normal);
    color: var(--color-text-secondary);
  }

  &__error {
    margin-top: map-get($spacing, 2);
    @include text-style(sm, normal, normal);
    color: var(--color-error);
  }
}

// Checkbox and Radio patterns
.form-check {
  display: flex;
  align-items: flex-start;
  margin-bottom: map-get($spacing, 3);

  &__input {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    margin-top: 2px;
    margin-right: map-get($spacing, 3);
    cursor: pointer;

    &:disabled {
      cursor: not-allowed;
    }
  }

  &__label {
    @include text-style(base, normal, normal);
    cursor: pointer;

    .form-check__input:disabled + & {
      color: var(--color-text-disabled);
      cursor: not-allowed;
    }
  }
}
```

#### Navigation Components **[REQUIRED]**
```typescript
// components/Navigation/NavigationMenu.tsx
interface NavigationItem {
  id: string;
  label: string;
  href?: string;
  icon?: React.ReactNode;
  children?: NavigationItem[];
  badge?: string | number;
}

interface NavigationMenuProps {
  items: NavigationItem[];
  orientation?: 'horizontal' | 'vertical';
  activeItem?: string;
  onItemClick?: (item: NavigationItem) => void;
}

export const NavigationMenu: React.FC<NavigationMenuProps> = ({
  items,
  orientation = 'horizontal',
  activeItem,
  onItemClick,
}) => {
  return (
    <nav
      className={clsx('nav-menu', `nav-menu--${orientation}`)}
      role="navigation"
    >
      <ul className="nav-menu__list" role="list">
        {items.map((item) => (
          <NavigationMenuItem
            key={item.id}
            item={item}
            isActive={activeItem === item.id}
            orientation={orientation}
            onItemClick={onItemClick}
          />
        ))}
      </ul>
    </nav>
  );
};

const NavigationMenuItem: React.FC<{
  item: NavigationItem;
  isActive: boolean;
  orientation: 'horizontal' | 'vertical';
  onItemClick?: (item: NavigationItem) => void;
}> = ({ item, isActive, orientation, onItemClick }) => {
  const [isOpen, setIsOpen] = useState(false);
  const hasChildren = item.children && item.children.length > 0;

  return (
    <li className="nav-menu__item" role="none">
      <a
        href={item.href || '#'}
        className={clsx('nav-menu__link', {
          'nav-menu__link--active': isActive,
          'nav-menu__link--has-children': hasChildren,
        })}
        onClick={(e) => {
          if (!item.href || hasChildren) {
            e.preventDefault();
            setIsOpen(!isOpen);
          }
          onItemClick?.(item);
        }}
        aria-current={isActive ? 'page' : undefined}
        aria-expanded={hasChildren ? isOpen : undefined}
      >
        {item.icon && (
          <span className="nav-menu__icon" aria-hidden="true">
            {item.icon}
          </span>
        )}
        <span className="nav-menu__label">{item.label}</span>
        {item.badge && (
          <span className="nav-menu__badge" aria-label={`${item.badge} new`}>
            {item.badge}
          </span>
        )}
        {hasChildren && (
          <span className="nav-menu__chevron" aria-hidden="true">
            <ChevronIcon direction={isOpen ? 'up' : 'down'} />
          </span>
        )}
      </a>
      {hasChildren && isOpen && (
        <ul className="nav-menu__submenu" role="list">
          {item.children.map((child) => (
            <NavigationMenuItem
              key={child.id}
              item={child}
              isActive={activeItem === child.id}
              orientation={orientation}
              onItemClick={onItemClick}
            />
          ))}
        </ul>
      )}
    </li>
  );
};
```

---

## 6. Interaction and Animation

### 6.1 Animation Principles

#### Motion Design System **[REQUIRED]**
```scss
// styles/motion.scss
// Consistent animation system based on Material Design

// Duration scale
$duration: (
  instant: 0ms,
  faster: 100ms,
  fast: 200ms,
  normal: 300ms,
  slow: 400ms,
  slower: 600ms,
  slowest: 800ms
);

// Easing functions
$easing: (
  // Accelerate (enter)
  enter: cubic-bezier(0.0, 0.0, 0.2, 1),
  // Decelerate (exit)
  exit: cubic-bezier(0.4, 0.0, 1, 1),
  // Standard (move)
  standard: cubic-bezier(0.4, 0.0, 0.2, 1),
  // Emphasized
  emphasized: cubic-bezier(0.0, 0.0, 0.2, 1),
  // Spring
  spring: cubic-bezier(0.175, 0.885, 0.32, 1.275)
);

// Animation mixins
@mixin transition($properties, $duration: normal, $easing: standard, $delay: 0ms) {
  $duration-value: map-get($duration, $duration);
  $easing-value: map-get($easing, $easing);

  transition-property: $properties;
  transition-duration: $duration-value;
  transition-timing-function: $easing-value;
  transition-delay: $delay;
}

// Micro-interactions
@mixin hover-lift() {
  @include transition(transform box-shadow, fast);

  &:hover {
    transform: translateY(-2px);
    box-shadow: map-get($shadows, 3);
  }
}

@mixin press-scale() {
  @include transition(transform, faster);

  &:active {
    transform: scale(0.96);
  }
}

// Page transitions
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

// Stagger animations
@mixin stagger-children($delay: 50ms, $count: 10) {
  @for $i from 1 through $count {
    &:nth-child(#{$i}) {
      animation-delay: $delay * $i;
    }
  }
}

// Loading states
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes skeleton {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-skeleton-base) 25%,
    var(--color-skeleton-shine) 50%,
    var(--color-skeleton-base) 75%
  );
  background-size: 200% 100%;
  animation: skeleton 1.5s ease-in-out infinite;
}
```

#### Gesture Feedback **[REQUIRED]**
```typescript
// utils/gesture-feedback.ts
interface RippleOptions {
  color?: string;
  duration?: number;
  size?: number;
}

export class RippleEffect {
  private container: HTMLElement;
  private options: Required<RippleOptions>;

  constructor(element: HTMLElement, options: RippleOptions = {}) {
    this.container = element;
    this.options = {
      color: options.color || 'currentColor',
      duration: options.duration || 600,
      size: options.size || 0,
    };

    this.container.style.position = 'relative';
    this.container.style.overflow = 'hidden';

    this.bindEvents();
  }

  private bindEvents() {
    this.container.addEventListener('pointerdown', this.createRipple);
  }

  private createRipple = (event: PointerEvent) => {
    const ripple = document.createElement('span');
    const rect = this.container.getBoundingClientRect();

    const size = this.options.size || Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background-color: ${this.options.color};
      opacity: 0.3;
      transform: scale(0);
      animation: ripple-effect ${this.options.duration}ms ease-out;
    `;

    this.container.appendChild(ripple);

    ripple.addEventListener('animationend', () => {
      ripple.remove();
    });
  };

  destroy() {
    this.container.removeEventListener('pointerdown', this.createRipple);
  }
}

// Usage
const button = document.querySelector('.button');
new RippleEffect(button, { color: 'rgba(255, 255, 255, 0.5)' });
```

### 6.2 Interactive Patterns

#### Drag and Drop **[RECOMMENDED]**
```typescript
// components/DragDrop/useDragDrop.ts
interface DragDropOptions {
  onDragStart?: (item: any) => void;
  onDragEnd?: (item: any) => void;
  onDrop?: (item: any, target: any) => void;
  canDrop?: (item: any, target: any) => boolean;
}

export function useDragDrop(options: DragDropOptions) {
  const [isDragging, setIsDragging] = useState(false);
  const [draggedItem, setDraggedItem] = useState<any>(null);

  const dragHandlers = {
    draggable: true,
    onDragStart: (e: React.DragEvent, item: any) => {
      setIsDragging(true);
      setDraggedItem(item);
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', JSON.stringify(item));
      options.onDragStart?.(item);
    },
    onDragEnd: (e: React.DragEvent) => {
      setIsDragging(false);
      setDraggedItem(null);
      options.onDragEnd?.(draggedItem);
    },
  };

  const dropHandlers = {
    onDragOver: (e: React.DragEvent) => {
      e.preventDefault();
      if (options.canDrop?.(draggedItem, e.currentTarget) ?? true) {
        e.dataTransfer.dropEffect = 'move';
      } else {
        e.dataTransfer.dropEffect = 'none';
      }
    },
    onDrop: (e: React.DragEvent, target: any) => {
      e.preventDefault();
      const item = JSON.parse(e.dataTransfer.getData('text/plain'));
      options.onDrop?.(item, target);
    },
  };

  return {
    isDragging,
    draggedItem,
    dragHandlers,
    dropHandlers,
  };
}

// Visual feedback during drag
.draggable {
  cursor: move;
  transition: opacity 0.2s ease;

  &--dragging {
    opacity: 0.5;
    cursor: grabbing;
  }
}

.drop-zone {
  transition: all 0.2s ease;

  &--active {
    background-color: var(--color-drop-zone-active);
    border: 2px dashed var(--color-primary);
  }

  &--hover {
    background-color: var(--color-drop-zone-hover);
    transform: scale(1.02);
  }
}
```

#### Scroll Interactions **[RECOMMENDED]**
```typescript
// hooks/useScrollProgress.ts
export function useScrollProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const updateProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight;
      const winHeight = window.innerHeight;
      const scrollPercent = scrollTop / (docHeight - winHeight);

      setProgress(Math.min(Math.max(scrollPercent, 0), 1));
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();

    return () => window.removeEventListener('scroll', updateProgress);
  }, []);

  return progress;
}

// Parallax scrolling
export function useParallax(speed: number = 0.5) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const handleScroll = () => {
      const scrolled = window.scrollY;
      const yPos = -(scrolled * speed);
      element.style.transform = `translateY(${yPos}px)`;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [speed]);

  return ref;
}
```

---

## 7. Responsive and Adaptive Design

### 7.1 Responsive Patterns

#### Breakpoint System **[REQUIRED]**
```scss
// styles/responsive.scss
// Mobile-first responsive design system

// Breakpoint definitions (same as in section 2.1)
$breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 992px,
  xl: 1200px,
  xxl: 1400px
);

// Breakpoint mixins
@mixin media-up($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Invalid breakpoint: #{$breakpoint}";
  }
}

@mixin media-down($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (max-width: map-get($breakpoints, $breakpoint) - 1px) {
      @content;
    }
  } @else {
    @warn "Invalid breakpoint: #{$breakpoint}";
  }
}

@mixin media-between($lower, $upper) {
  @if map-has-key($breakpoints, $lower) and map-has-key($breakpoints, $upper) {
    @media (min-width: map-get($breakpoints, $lower)) and (max-width: map-get($breakpoints, $upper) - 1px) {
      @content;
    }
  } @else {
    @warn "Invalid breakpoints: #{$lower}, #{$upper}";
  }
}

// Container system
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: map-get($spacing, 4);
  padding-right: map-get($spacing, 4);

  @each $breakpoint, $container-width in $container-max-widths {
    @include media-up($breakpoint) {
      max-width: $container-width;
    }
  }

  &--fluid {
    max-width: none;
  }
}

// Responsive utilities
@each $breakpoint in map-keys($breakpoints) {
  @include media-up($breakpoint) {
    .hide-#{$breakpoint} { display: none !important; }
    .show-#{$breakpoint} { display: block !important; }
  }
}
```

#### Responsive Components **[REQUIRED]**
```typescript
// hooks/useMediaQuery.ts
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);

    const updateMatch = () => setMatches(media.matches);
    updateMatch();

    media.addEventListener('change', updateMatch);
    return () => media.removeEventListener('change', updateMatch);
  }, [query]);

  return matches;
}

// Responsive component example
export const ResponsiveNavigation: React.FC = () => {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)');
  const isDesktop = useMediaQuery('(min-width: 1025px)');

  if (isMobile) {
    return <MobileNavigation />;
  }

  if (isTablet) {
    return <TabletNavigation />;
  }

  return <DesktopNavigation />;
};
```

### 7.2 Adaptive Patterns

#### Progressive Enhancement **[REQUIRED]**
```typescript
// utils/feature-detection.ts
export const features = {
  touch: 'ontouchstart' in window,
  webp: supportsWebP(),
  grid: CSS.supports('display', 'grid'),
  sticky: CSS.supports('position', 'sticky'),
  blur: CSS.supports('backdrop-filter', 'blur(10px)'),
  customProperties: CSS.supports('--custom', 'property'),
  prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  prefersColorScheme: window.matchMedia('(prefers-color-scheme: dark)').matches,
};

// Progressive image loading
export const ProgressiveImage: React.FC<{
  src: string;
  alt: string;
  placeholder?: string;
}> = ({ src, alt, placeholder }) => {
  const [imageSrc, setImageSrc] = useState(placeholder || '');
  const [imageRef, setImageRef] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = new Image();
            img.src = src;
            img.onload = () => setImageSrc(src);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    if (imageRef) {
      observer.observe(imageRef);
    }

    return () => observer.disconnect();
  }, [imageRef, src]);

  return (
    <img
      ref={setImageRef}
      src={imageSrc}
      alt={alt}
      loading="lazy"
      className={clsx('progressive-image', {
        'progressive-image--loaded': imageSrc === src,
      })}
    />
  );
};
```

#### Device Optimization **[RECOMMENDED]**
```scss
// styles/device-optimization.scss
// Touch-optimized styles
@media (hover: none) and (pointer: coarse) {
  // Touch devices
  .button {
    min-height: 44px; // Apple HIG minimum
    min-width: 44px;
  }

  .link {
    padding: map-get($spacing, 2) map-get($spacing, 3);
    margin: -#{map-get($spacing, 2)} -#{map-get($spacing, 3)};
  }

  // Disable hover effects on touch
  .card:hover {
    transform: none;
    box-shadow: map-get($shadows, 1);
  }
}

// High-DPI displays
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  // Use higher resolution images
  .logo {
    background-image: url('/images/logo@2x.png');
  }

  // Thinner borders
  .divider {
    border-width: 0.5px;
  }
}

// Reduced motion
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .parallax {
    transform: none !important;
  }
}

// Print styles
@media print {
  .no-print {
    display: none !important;
  }

  body {
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
    background: #fff;
  }

  a {
    text-decoration: underline;

    &[href^="http"]:after {
      content: " (" attr(href) ")";
    }
  }
}
```

---

## 8. User Experience Patterns

### 8.1 Navigation Patterns

#### Information Architecture **[REQUIRED]**
```yaml
# ux/information-architecture.yaml
navigation_patterns:
  primary_navigation:
    max_items: 7  # Miller's Law
    patterns:
      - horizontal_bar
      - hamburger_menu
      - tab_bar
      - side_drawer

  secondary_navigation:
    patterns:
      - breadcrumbs
      - section_tabs
      - sidebar_menu
      - contextual_actions

  mobile_navigation:
    patterns:
      - bottom_tab_bar  # Max 5 items
      - hamburger_drawer
      - gesture_navigation
      - floating_action_button

information_hierarchy:
  levels:
    1: "Global navigation"
    2: "Section navigation"
    3: "Page navigation"
    4: "Content navigation"

  principles:
    - Progressive disclosure
    - Consistent positioning
    - Clear labeling
    - Visual hierarchy
```

#### Search Patterns **[REQUIRED]**
```typescript
// components/Search/SearchExperience.tsx
interface SearchConfig {
  placeholder?: string;
  debounceMs?: number;
  minChars?: number;
  maxResults?: number;
  showRecent?: boolean;
  showSuggestions?: boolean;
  categories?: string[];
}

export const SearchExperience: React.FC<SearchConfig> = ({
  placeholder = "Search...",
  debounceMs = 300,
  minChars = 2,
  maxResults = 10,
  showRecent = true,
  showSuggestions = true,
  categories = [],
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const debouncedSearch = useMemo(
    () => debounce(async (searchQuery: string) => {
      if (searchQuery.length < minChars) {
        setResults([]);
        return;
      }

      setIsSearching(true);
      try {
        const searchResults = await performSearch(searchQuery, {
          maxResults,
          categories,
        });
        setResults(searchResults);
      } finally {
        setIsSearching(false);
      }
    }, debounceMs),
    [debounceMs, minChars, maxResults, categories]
  );

  useEffect(() => {
    debouncedSearch(query);
  }, [query, debouncedSearch]);

  return (
    <div className={clsx('search', { 'search--active': isFocused })}>
      <div className="search__input-wrapper">
        <SearchIcon className="search__icon" />
        <input
          type="search"
          className="search__input"
          placeholder={placeholder}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 200)}
          aria-label="Search"
          aria-autocomplete="list"
          aria-controls="search-results"
          aria-expanded={isFocused && (results.length > 0 || showRecent)}
        />
        {isSearching && <Spinner className="search__spinner" />}
        {query && (
          <button
            className="search__clear"
            onClick={() => setQuery('')}
            aria-label="Clear search"
          >
            <ClearIcon />
          </button>
        )}
      </div>

      {isFocused && (
        <div
          id="search-results"
          className="search__results"
          role="listbox"
        >
          {query.length < minChars && showRecent && (
            <RecentSearches onSelect={setQuery} />
          )}

          {query.length >= minChars && (
            <>
              {showSuggestions && (
                <SearchSuggestions
                  query={query}
                  onSelect={setQuery}
                />
              )}

              <SearchResults
                results={results}
                query={query}
                isSearching={isSearching}
              />
            </>
          )}
        </div>
      )}
    </div>
  );
};
```

### 8.2 Feedback Patterns

#### Loading States **[REQUIRED]**
```typescript
// components/Loading/LoadingPatterns.tsx
export const SkeletonLoader: React.FC<{
  lines?: number;
  showAvatar?: boolean;
  showImage?: boolean;
}> = ({ lines = 3, showAvatar = false, showImage = false }) => {
  return (
    <div className="skeleton-loader">
      {showImage && (
        <div className="skeleton skeleton--image" />
      )}
      <div className="skeleton-loader__content">
        {showAvatar && (
          <div className="skeleton skeleton--avatar" />
        )}
        <div className="skeleton-loader__text">
          <div className="skeleton skeleton--title" />
          {Array.from({ length: lines }).map((_, i) => (
            <div
              key={i}
              className="skeleton skeleton--line"
              style={{ width: `${Math.random() * 40 + 60}%` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export const ProgressIndicator: React.FC<{
  value: number;
  max?: number;
  label?: string;
  showPercentage?: boolean;
}> = ({ value, max = 100, label, showPercentage = true }) => {
  const percentage = Math.round((value / max) * 100);

  return (
    <div className="progress" role="progressbar" aria-valuenow={value} aria-valuemax={max}>
      {label && <div className="progress__label">{label}</div>}
      <div className="progress__track">
        <div
          className="progress__fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      {showPercentage && (
        <div className="progress__percentage">{percentage}%</div>
      )}
    </div>
  );
};
```

#### Error Handling **[REQUIRED]**
```typescript
// components/Error/ErrorBoundary.tsx
interface ErrorFallbackProps {
  error: Error;
  resetError: () => void;
  level?: 'page' | 'section' | 'component';
}

export const ErrorFallback: React.FC<ErrorFallbackProps> = ({
  error,
  resetError,
  level = 'component',
}) => {
  const errorId = useId();

  useEffect(() => {
    console.error('Error boundary caught:', error);
    // Log to error tracking service
    trackError(error, { level, errorId });
  }, [error, level, errorId]);

  if (level === 'page') {
    return (
      <div className="error-page">
        <div className="error-page__content">
          <h1>Something went wrong</h1>
          <p>We're sorry, but something unexpected happened.</p>
          <details className="error-page__details">
            <summary>Error details</summary>
            <pre>{error.message}</pre>
          </details>
          <div className="error-page__actions">
            <Button onClick={resetError} variant="primary">
              Try again
            </Button>
            <Button onClick={() => window.location.href = '/'} variant="ghost">
              Go to homepage
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={clsx('error-fallback', `error-fallback--${level}`)}>
      <div className="error-fallback__icon">
        <ErrorIcon />
      </div>
      <div className="error-fallback__message">
        <p>Unable to load this {level}</p>
        <button
          className="error-fallback__retry"
          onClick={resetError}
        >
          Try again
        </button>
      </div>
    </div>
  );
};

// Form validation feedback
export const FormFieldError: React.FC<{
  error?: string;
  touched?: boolean;
}> = ({ error, touched }) => {
  if (!error || !touched) return null;

  return (
    <div className="form-field__error" role="alert">
      <ErrorIcon className="form-field__error-icon" />
      <span>{error}</span>
    </div>
  );
};
```

### 8.3 Accessibility Patterns

#### Keyboard Navigation **[REQUIRED]**
```typescript
// hooks/useKeyboardNavigation.ts
export function useKeyboardNavigation(
  items: any[],
  options: {
    orientation?: 'horizontal' | 'vertical';
    loop?: boolean;
    onSelect?: (item: any, index: number) => void;
  } = {}
) {
  const {
    orientation = 'vertical',
    loop = true,
    onSelect,
  } = options;

  const [focusedIndex, setFocusedIndex] = useState(-1);

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    const key = event.key;
    const itemCount = items.length;

    const navigationKeys = {
      vertical: {
        next: 'ArrowDown',
        prev: 'ArrowUp',
      },
      horizontal: {
        next: 'ArrowRight',
        prev: 'ArrowLeft',
      },
    };

    const { next, prev } = navigationKeys[orientation];

    switch (key) {
      case next:
        event.preventDefault();
        setFocusedIndex(current => {
          const nextIndex = current + 1;
          if (nextIndex >= itemCount) {
            return loop ? 0 : current;
          }
          return nextIndex;
        });
        break;

      case prev:
        event.preventDefault();
        setFocusedIndex(current => {
          const prevIndex = current - 1;
          if (prevIndex < 0) {
            return loop ? itemCount - 1 : current;
          }
          return prevIndex;
        });
        break;

      case 'Enter':
      case ' ':
        event.preventDefault();
        if (focusedIndex >= 0 && focusedIndex < itemCount) {
          onSelect?.(items[focusedIndex], focusedIndex);
        }
        break;

      case 'Home':
        event.preventDefault();
        setFocusedIndex(0);
        break;

      case 'End':
        event.preventDefault();
        setFocusedIndex(itemCount - 1);
        break;

      case 'Escape':
        event.preventDefault();
        setFocusedIndex(-1);
        break;
    }
  }, [items, orientation, loop, onSelect, focusedIndex]);

  return {
    focusedIndex,
    setFocusedIndex,
    handleKeyDown,
    keyboardProps: {
      onKeyDown: handleKeyDown,
      tabIndex: 0,
      role: 'list',
    },
  };
}
```

#### Screen Reader Support **[REQUIRED]**
```typescript
// components/Accessibility/LiveRegion.tsx
export const LiveRegion: React.FC<{
  message: string;
  politeness?: 'polite' | 'assertive' | 'off';
  atomic?: boolean;
  relevant?: 'additions' | 'removals' | 'text' | 'all';
}> = ({
  message,
  politeness = 'polite',
  atomic = true,
  relevant = 'additions',
}) => {
  return (
    <div
      role="status"
      aria-live={politeness}
      aria-atomic={atomic}
      aria-relevant={relevant}
      className="sr-only"
    >
      {message}
    </div>
  );
};

// Accessible tooltips
export const Tooltip: React.FC<{
  content: React.ReactNode;
  children: React.ReactElement;
}> = ({ content, children }) => {
  const [isVisible, setIsVisible] = useState(false);
  const tooltipId = useId();

  return (
    <>
      {React.cloneElement(children, {
        'aria-describedby': isVisible ? tooltipId : undefined,
        onMouseEnter: () => setIsVisible(true),
        onMouseLeave: () => setIsVisible(false),
        onFocus: () => setIsVisible(true),
        onBlur: () => setIsVisible(false),
      })}
      {isVisible && (
        <div
          id={tooltipId}
          role="tooltip"
          className="tooltip"
        >
          {content}
        </div>
      )}
    </>
  );
};
```

---

## Implementation Guidelines

### Design System Adoption
1. **Audit Phase**: Review existing designs and identify patterns
2. **Foundation Phase**: Establish color, typography, and spacing systems
3. **Component Phase**: Build core component library
4. **Pattern Phase**: Document common UI patterns
5. **Optimization Phase**: Refine based on usage and feedback

### Design Tools Integration
- **Figma**: Use shared libraries and design tokens
- **Sketch**: Maintain symbol libraries
- **Adobe XD**: Create component states and interactions
- **Storybook**: Document component variations
- **Design Tokens**: Sync between design and code

### Quality Assurance
- **Visual Testing**: Screenshot comparison tests
- **Accessibility Testing**: Automated and manual audits
- **Performance Testing**: Lighthouse scores
- **Cross-browser Testing**: Ensure consistency
- **Device Testing**: Real device validation

### Success Metrics
- **Consistency Score**: Design system adoption rate
- **Accessibility Score**: WCAG compliance level
- **Performance Score**: Core Web Vitals metrics
- **Efficiency Gain**: Time saved in design/development
- **User Satisfaction**: Usability testing results

---

**End of Web Design and UX Standards**
