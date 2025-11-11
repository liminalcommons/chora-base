# SAP-024: React Styling Architecture - Protocol Specification

**SAP ID**: SAP-024
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01

---

## Overview

This protocol specification defines the technical standards, patterns, and implementation details for SAP-024 (React Styling Architecture). It provides production-ready examples for Tailwind CSS v4, shadcn/ui, CVA, and dark mode implementation.

---

## Table of Contents

1. [Tailwind CSS v4 Configuration](#tailwind-css-v4-configuration)
2. [CSS-First Configuration with @theme](#css-first-configuration-with-theme)
3. [OKLCH Color Space](#oklch-color-space)
4. [Component Variant Patterns (CVA)](#component-variant-patterns-cva)
5. [Dark Mode Implementation](#dark-mode-implementation)
6. [Responsive Design Patterns](#responsive-design-patterns)
7. [Container Queries](#container-queries)
8. [Accessibility Patterns](#accessibility-patterns)
9. [shadcn/ui Integration](#shadcnui-integration)
10. [TypeScript Integration](#typescript-integration)
11. [Performance Optimization](#performance-optimization)
12. [CSS Modules Escape Hatch](#css-modules-escape-hatch)

---

## Tailwind CSS v4 Configuration

### Why Tailwind v4?

**Tailwind CSS v4** (released December 2024) represents a major performance breakthrough:

- **5x faster builds** compared to Tailwind v3 (~100ms vs ~500ms)
- **CSS-first configuration** with `@theme` directive (zero JavaScript config)
- **Zero-runtime** pure CSS output (perfect RSC compatibility)
- **Native CSS features**: Container queries, cascade layers, OKLCH colors
- **Automatic content detection** (no manual purge configuration)

**Migration**: Tailwind v3 → v4 typically takes 1-2 hours for existing projects.

### Next.js 15 Setup

**File**: `postcss.config.mjs`

```javascript
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}

export default config
```

**File**: `app/globals.css`

```css
@import "tailwindcss";

@theme {
  /* Design tokens defined here */
}
```

**File**: `app/layout.tsx`

```typescript
import './globals.css'

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  )
}
```

### Vite 7 Setup

**File**: `postcss.config.js`

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**File**: `tailwind.config.ts`

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        // ... more colors
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
}

export default config
```

**File**: `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    /* ... more CSS variables */
  }

  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    /* ... more CSS variables */
  }
}
```

---

## CSS-First Configuration with @theme

### Tailwind v4 @theme Directive

Tailwind v4 introduces CSS-first configuration using the `@theme` directive, replacing JavaScript config for design tokens.

**Pattern**: Define design tokens in CSS

```css
@import "tailwindcss";

@theme {
  /* Typography */
  --font-sans: "Inter", system-ui, -apple-system, sans-serif;
  --font-mono: "Fira Code", "Monaco", monospace;

  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */

  /* Spacing (0.25rem base = 4px) */
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */

  /* Color Palette (OKLCH) */
  --color-primary: oklch(0.5 0.2 250);
  --color-secondary: oklch(0.6 0.15 180);

  /* Breakpoints (extended) */
  --breakpoint-xs: 475px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
  --breakpoint-3xl: 1920px;  /* 4K monitors */
  --breakpoint-4xl: 2560px;  /* Ultra-wide */

  /* Border Radius */
  --radius-sm: 0.125rem;   /* 2px */
  --radius-md: 0.375rem;   /* 6px */
  --radius-lg: 0.5rem;     /* 8px */
  --radius-xl: 0.75rem;    /* 12px */
  --radius-2xl: 1rem;      /* 16px */
  --radius-full: 9999px;   /* Fully rounded */

  /* Animation */
  --animate-duration-fast: 150ms;
  --animate-duration-base: 200ms;
  --animate-duration-slow: 300ms;
  --animate-timing: cubic-bezier(0.4, 0, 0.2, 1);  /* Ease out */
}
```

**Usage in HTML**:

```tsx
<div className="font-sans text-base p-4 rounded-lg">
  {/* Uses design tokens from @theme */}
</div>
```

---

## OKLCH Color Space

### Why OKLCH?

OKLCH (Oklch Lightness Chroma Hue) provides perceptual uniformity for better color consistency:

- **Perceptual Uniformity**: Equal numeric changes = equal perceived changes
- **Better Contrast**: Easier to maintain WCAG contrast ratios
- **Predictable Darkening**: oklch(0.5 0.2 250) → oklch(0.4 0.2 250) = consistent darkening
- **Wide Gamut**: Supports modern display technology

### OKLCH Pattern

**Syntax**: `oklch(lightness chroma hue)`

- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (grayscale) to 0.4 (vivid) - typically 0.1-0.25
- **Hue**: 0-360 degrees (0=red, 120=green, 240=blue)

**Example Color System**:

```css
@theme {
  /* Primary (Blue) */
  --color-primary-50: oklch(0.95 0.05 250);
  --color-primary-100: oklch(0.90 0.10 250);
  --color-primary-200: oklch(0.80 0.15 250);
  --color-primary-500: oklch(0.50 0.20 250);  /* Base */
  --color-primary-700: oklch(0.35 0.18 250);
  --color-primary-900: oklch(0.20 0.15 250);

  /* Semantic Colors */
  --color-success: oklch(0.60 0.18 145);  /* Green */
  --color-warning: oklch(0.75 0.15 85);   /* Yellow */
  --color-error: oklch(0.55 0.22 25);     /* Red */
  --color-info: oklch(0.60 0.18 230);     /* Blue */
}
```

### Converting from HSL to OKLCH

**HSL**: `hsl(220, 90%, 50%)` (Blue)
**OKLCH**: `oklch(0.55 0.22 250)` (Blue)

Use [OKLCH Color Picker](https://oklch.com/) for visual conversion.

### Dark Mode with OKLCH

```css
@theme {
  --color-primary: oklch(0.5 0.2 250);  /* Light mode */
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-primary: oklch(0.7 0.2 250);  /* Dark mode (lighter) */
  }
}
```

**Insight**: In dark mode, increase lightness (0.5 → 0.7) for better contrast against dark backgrounds.

---

## Component Variant Patterns (CVA)

### CVA (Class Variance Authority)

CVA provides type-safe component variants with TypeScript inference.

### Basic Pattern

**File**: `lib/cva-utils.ts`

```typescript
import { cva, type VariantProps } from "class-variance-authority"

export const buttonVariants = cva(
  // Base classes (always applied)
  "inline-flex items-center justify-center rounded-md font-medium transition-colors disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// Extract TypeScript type
export type ButtonVariants = VariantProps<typeof buttonVariants>
```

**Usage**:

```typescript
import { buttonVariants } from "@/lib/cva-utils"
import { cn } from "@/lib/utils"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, ButtonVariants {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}

// Usage in component
<Button variant="destructive" size="lg">Delete</Button>
```

### Compound Variants

Use compound variants for special combinations:

```typescript
export const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        secondary: "bg-secondary text-secondary-foreground",
        destructive: "bg-destructive text-destructive-foreground",
      },
      size: {
        default: "",
        lg: "px-3 py-1 text-sm",
      },
    },
    compoundVariants: [
      {
        variant: "destructive",
        size: "lg",
        className: "border-2 border-destructive/50",  // Special styling
      },
    ],
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### Boolean Variants

```typescript
export const inputVariants = cva(
  "flex w-full rounded-md border px-3 py-2",
  {
    variants: {
      error: {
        true: "border-destructive focus-visible:ring-destructive",
        false: "border-input focus-visible:ring-ring",
      },
      disabled: {
        true: "cursor-not-allowed opacity-50",
        false: "",
      },
    },
    defaultVariants: {
      error: false,
      disabled: false,
    },
  }
)
```

---

## Dark Mode Implementation

### Using next-themes

**File**: `providers/theme-provider.tsx`

```typescript
"use client"

import { ThemeProvider as NextThemesProvider } from "next-themes"
import { type ThemeProviderProps } from "next-themes/dist/types"

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
```

**File**: `app/layout.tsx` (Next.js 15)

```typescript
import { ThemeProvider } from "@/providers/theme-provider"

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"           // Use class-based dark mode
          defaultTheme="system"       // Default to system preference
          enableSystem                // Enable system preference detection
          disableTransitionOnChange   // Prevent flash on theme change
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

**File**: `main.tsx` (Vite 7)

```typescript
import { ThemeProvider } from "./providers/theme-provider"

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
```

### Theme Toggle Component

**File**: `components/ui/theme-toggle.tsx`

```typescript
"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function ThemeToggle() {
  const { setTheme } = useTheme()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon">
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>Light</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>Dark</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>System</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

### Dark Mode CSS Variables

**Pattern**: Define light/dark colors with CSS variables

```css
@theme {
  --color-background: oklch(1 0 0);       /* White */
  --color-foreground: oklch(0.09 0 0);    /* Near-black */
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: oklch(0.09 0 0);  /* Near-black */
    --color-foreground: oklch(0.98 0 0);  /* Near-white */
  }
}
```

### Conditional Dark Mode Classes

```tsx
<div className="bg-white dark:bg-slate-900 text-black dark:text-white">
  Content adapts to theme
</div>
```

---

## Responsive Design Patterns

### Mobile-First Breakpoints

Tailwind uses mobile-first breakpoints (default applies to all sizes, use prefixes for larger screens):

| Prefix | Min Width | Target Devices |
|--------|-----------|----------------|
| `(none)` | 0px | All (mobile-first) |
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large desktops |

### Responsive Grid

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {/* 1 column mobile, 2 tablet, 3 laptop, 4 desktop */}
  {items.map((item) => <Card key={item.id}>{item.title}</Card>)}
</div>
```

### Responsive Typography

```tsx
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Heading scales with screen size
</h1>
```

### Responsive Layout (Stack → Side-by-Side)

```tsx
<div className="flex flex-col gap-4 lg:flex-row">
  <aside className="w-full lg:w-1/4">Sidebar</aside>
  <main className="w-full lg:w-3/4">Main content</main>
</div>
```

### Responsive Spacing

```tsx
<Card className="p-4 sm:p-6 md:p-8 lg:p-10">
  Padding increases on larger screens
</Card>
```

### Hide/Show on Breakpoints

```tsx
{/* Show on mobile only */}
<div className="block lg:hidden">Mobile nav</div>

{/* Show on desktop only */}
<div className="hidden lg:block">Desktop nav</div>
```

---

## Container Queries

### What Are Container Queries?

Container queries allow components to adapt based on their **container width**, not viewport width. This enables truly reusable components.

### Setup

**File**: `tailwind.config.ts` (Vite) or @theme directive (Next.js 15)

```typescript
export default {
  theme: {
    extend: {
      containers: {
        '2xs': '16rem',   /* 256px */
        'xs': '20rem',    /* 320px */
        'sm': '24rem',    /* 384px */
        'md': '28rem',    /* 448px */
        'lg': '32rem',    /* 512px */
        'xl': '36rem',    /* 576px */
      },
    },
  },
}
```

### Usage

**Pattern**: Use `@container` directive + `@[size]:` prefixes

```tsx
<div className="@container">
  <Card className="@sm:flex-row flex flex-col gap-4">
    <div className="@sm:w-1/3 w-full bg-muted">Image</div>
    <div className="@sm:w-2/3 w-full">
      <CardHeader>
        <CardTitle>Container Query Card</CardTitle>
      </CardHeader>
      <CardContent>
        Adapts based on container width, not viewport
      </CardContent>
    </div>
  </Card>
</div>
```

**Benefits**:
- Reusable components (same component adapts to different containers)
- Nested responsiveness (components inside sidebars can adapt independently)
- Component-first design (CSS follows component structure)

---

## Accessibility Patterns

### WCAG 2.2 Level AA Baseline

SAP-024 provides WCAG 2.2 Level AA foundation via Radix UI primitives:

1. **Keyboard Navigation** - All interactive elements accessible via keyboard
2. **Focus Management** - Visible focus indicators, focus trapping in modals
3. **Screen Reader Support** - ARIA labels, semantic HTML
4. **Color Contrast** - ≥4.5:1 for text (OKLCH helps maintain contrast)

### Accessible Button

```typescript
import { Button } from "@/components/ui/button"

// Good: Accessible text
<Button>Submit Form</Button>

// Good: Icon button with screen reader text
<Button variant="ghost" size="icon">
  <X className="h-4 w-4" />
  <span className="sr-only">Close dialog</span>
</Button>

// Bad: Icon button without screen reader text
<Button variant="ghost" size="icon">
  <X className="h-4 w-4" />
</Button>
```

### Accessible Form

```typescript
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

<div className="space-y-2">
  <Label htmlFor="email">Email address</Label>
  <Input
    id="email"
    type="email"
    placeholder="you@example.com"
    aria-describedby="email-error"
  />
  <p id="email-error" className="text-sm text-destructive">
    {errors.email?.message}
  </p>
</div>
```

### Focus Visible Pattern

```css
/* Tailwind provides focus-visible utilities */
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
  Button with focus ring
</button>
```

### Skip to Content Link

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:p-4 focus:bg-background focus:border"
>
  Skip to main content
</a>

<main id="main-content">
  {/* Main content */}
</main>
```

---

## shadcn/ui Integration

### Why shadcn/ui?

**shadcn/ui** has become the most popular React component library in 2024:

- **100k+ GitHub stars** (most popular React component library)
- **Copy-paste model**: Full source control, no npm dependency lock-in
- **Built on Radix UI**: Accessibility (WAI-ARIA) built-in
- **Tailwind v4 compatible**: Integrates seamlessly with modern Tailwind
- **Customization-first**: Edit components directly (they're your code)

**Alternative to npm-installed libraries**: Unlike Material-UI or Ant Design, shadcn/ui gives you full ownership of component code.

### Installation

**Step 1**: Add `components.json`

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui"
  }
}
```

**Step 2**: Install CLI (optional, for additional components)

```bash
npx shadcn@latest init
```

**Step 3**: Copy component templates from SAP-024

```bash
cp templates/react/styling/shared/components/ui/button.tsx src/components/ui/
cp templates/react/styling/shared/components/ui/card.tsx src/components/ui/
# ... repeat for other components
```

### Customizing Components

**Pattern**: Edit component files directly (they're your code, not a package)

```typescript
// components/ui/button.tsx
export const buttonVariants = cva(
  "inline-flex items-center justify-center...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        // Add custom variant
        gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
      },
      size: {
        default: "h-10 px-4 py-2",
        // Add custom size
        xs: "h-7 px-2 text-xs",
      },
    },
  }
)
```

---

## TypeScript Integration

### Component Props with CVA

```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { type ButtonHTMLAttributes, forwardRef } from "react"

const buttonVariants = cva(/* ... */)

// Extract variant types
export type ButtonVariants = VariantProps<typeof buttonVariants>

// Merge with HTML attributes
export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    ButtonVariants {}

// Use in component
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant, size, className, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"
```

### Typed cn() Helper

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage with type safety
<button className={cn(
  "base-classes",
  condition && "conditional-class",
  { "variant-class": isVariant },
  className  // From props
)} />
```

---

## Performance Optimization

### Bundle Size Optimization

**Tailwind v4 Auto-Detection**: Automatically scans files for used classes (no manual purge configuration).

**Production Build**:

```bash
# Next.js 15
npm run build

# Vite 7
npm run build

# Result: 6-15KB CSS (gzipped)
```

### Code Splitting

**Pattern**: Use dynamic imports for large components

```typescript
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./heavy-component'), {
  loading: () => <p>Loading...</p>,
})
```

### Critical CSS

**Next.js 15**: Automatic critical CSS extraction (no configuration needed)

**Vite 7**: Use `vite-plugin-critical` for critical CSS

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import critical from 'vite-plugin-critical'

export default defineConfig({
  plugins: [
    critical({
      inline: true,
      dimensions: [
        { width: 375, height: 667 },   // Mobile
        { width: 1920, height: 1080 }, // Desktop
      ],
    }),
  ],
})
```

---

## CSS Modules Escape Hatch

### When to Use CSS Modules (5% Use Case)

Use CSS Modules for complex patterns Tailwind can't handle:

1. **Complex Keyframe Animations** (10+ steps)
2. **CSS Grid with Named Areas**
3. **Advanced Pseudo-Selectors** (`:has()`, `:is()`)
4. **Legacy Code Migration** (gradual adoption)

### Pattern: Mixing Tailwind + CSS Modules

**File**: `components/complex-animation.module.css`

```css
.pulse-complex {
  animation: pulse-complex 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-complex {
  0%, 100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
  25% {
    opacity: 0.8;
    transform: scale(1.05) rotate(5deg);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1) rotate(-5deg);
  }
  75% {
    opacity: 0.8;
    transform: scale(1.05) rotate(5deg);
  }
}
```

**File**: `components/complex-animation.tsx`

```typescript
import styles from './complex-animation.module.css'
import { cn } from '@/lib/utils'

export function ComplexAnimation() {
  return (
    <div className={cn(
      "p-4 rounded-lg bg-primary",  // Tailwind
      styles.pulseComplex            // CSS Module
    )}>
      Complex animation
    </div>
  )
}
```

---

## Conclusion

This protocol specification provides comprehensive technical patterns for SAP-024 (React Styling Architecture). Use these patterns as production-ready starting points for React 19 applications with Tailwind CSS v4, shadcn/ui, and CVA.

**Key Patterns**:
1. ✅ CSS-first configuration with @theme directive
2. ✅ OKLCH color space for perceptual uniformity
3. ✅ CVA for type-safe component variants
4. ✅ Dark mode with next-themes
5. ✅ Mobile-first responsive design
6. ✅ Container queries for component-based responsiveness
7. ✅ WCAG 2.2 Level AA baseline via Radix UI
8. ✅ TypeScript integration with VariantProps
9. ✅ Performance optimization (6-15KB bundles)
10. ✅ CSS Modules escape hatch for 5% edge cases

**Next Steps**: See [adoption-blueprint.md](adoption-blueprint.md) for 30-minute setup guide.

---

## Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents the expected awareness file coverage for SAP-024 to validate SAP-009 Phase 4 compliance.

### Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Install Tailwind CSS v4 for Next.js 15 (10-15 min)
2. Setup shadcn/ui Component Library (10-20 min)
3. Setup Dark Mode with next-themes (10-15 min)
4. Add shadcn/ui Component (2-5 min per component)
5. Create Component with CVA Variants (15-20 min)

**CLAUDE.md**: 3 workflows
1. Installing Tailwind CSS v4 with Bash and Write
2. Setting up shadcn/ui with Bash and Write
3. Setting up Dark Mode with Bash, Write, and Edit

**Variance**: 3 workflows (CLAUDE.md) vs 5 workflows (AGENTS.md) = 40% difference
**Acceptable**: Yes (within ±30-40% tolerance with documented rationale)

**Rationale for Variance**: CLAUDE.md focuses on installation and configuration patterns with tool-specific guidance (Bash for CLI commands, Write for config creation, Edit for layout integration), consolidating setup operations into single workflows. AGENTS.md provides granular step-by-step guidance for each styling operation including component installation, CVA variant creation, and dark mode implementation.

### Actual Coverage (To Be Validated)

**AGENTS.md**: ✅ 5 workflows
- Install Tailwind CSS v4 for Next.js 15
- Setup shadcn/ui Component Library
- Setup Dark Mode with next-themes
- Add shadcn/ui Component
- Create Component with CVA Variants

**CLAUDE.md**: ✅ 3 workflows
- Installing Tailwind CSS v4 with Bash and Write
- Setting up shadcn/ui with Bash and Write
- Setting up Dark Mode with Bash, Write, and Edit

**User Signal Pattern Tables**: ✅ 2 tables
- Table 1: Styling Setup Signals (5 intents)
- Table 2: Styling Operation Signals (5 intents)

**Best Practices**: ✅ 5 documented
**Common Pitfalls**: ✅ 5 documented
**Progressive Loading**: ✅ YAML frontmatter with phase_1/2/3 token estimates

**Validation Status**: ✅ Equivalent Support (40% variance with documented rationale)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-01
