# SAP-024: React Styling Architecture

**SAP ID**: SAP-024
**Version**: 1.0.0
**Tailwind CSS Version**: 4.x
**shadcn/ui Version**: Latest
**CVA Version**: 1.x
**Research Foundation**: RT-019-SYNTHESIS (Q4 2024 - Q1 2025)

---

## 🚀 Quick Start (4 minutes)

```bash
# Install Tailwind CSS v4
pnpm add -D @tailwindcss/postcss@next tailwindcss@next autoprefixer

# Install shadcn/ui
npx shadcn-ui@latest init

# Install CVA for component variants
pnpm add class-variance-authority clsx tailwind-merge

# Create PostCSS config
cat > postcss.config.mjs <<'EOF'
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
EOF

# Create Tailwind globals
cat > app/globals.css <<'EOF'
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.5 0.2 250);
  --font-sans: system-ui, sans-serif;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
}
EOF

# Import in layout
echo "import './globals.css'" >> app/layout.tsx
```

**Expected outcome**: Tailwind CSS v4 + shadcn/ui setup complete in 4 minutes.

---

## What Is It?

SAP-024 provides **production-ready styling architecture** for React 19 using Tailwind CSS v4 (5x faster), shadcn/ui components, CVA for variants, and OKLCH color space.

### Purpose

- **Tailwind CSS v4**: 5x faster builds (100ms vs 500ms), CSS-first config with `@theme`
- **shadcn/ui**: Copy-paste component library (no npm install, full customization)
- **CVA**: Type-safe component variants with TypeScript inference
- **OKLCH Colors**: Perceptual uniformity for better contrast and dark mode
- **Dark Mode**: Class-based dark mode with next-themes
- **Container Queries**: Modern responsive design beyond media queries

### How It Works

1. **Install** Tailwind CSS v4, shadcn/ui CLI, CVA
2. **Configure** `@theme` directive in `globals.css` for design tokens
3. **Add** shadcn/ui components with `npx shadcn-ui add button`
4. **Create** variant components with CVA
5. **Implement** dark mode with next-themes
6. **Optimize** with automatic content detection (no manual purge)

---

## When to Use

### ✅ Use React Styling (SAP-024) When

- **Utility-First CSS**: Tailwind's approach fits your team
- **Component Library**: Need accessible, customizable components (shadcn/ui)
- **Type Safety**: Want TypeScript inference for component variants (CVA)
- **Dark Mode**: App requires light/dark theme support
- **Performance**: Need fast builds (5x faster with Tailwind v4)
- **RSC Compatible**: Server Components require zero-runtime CSS

### ❌ Don't Use When

- **CSS-in-JS Required**: Need runtime theming (use styled-components, Emotion)
- **Tailwind Aversion**: Team prefers semantic CSS or BEM methodology
- **Minimal CSS**: Simple app doesn't justify Tailwind overhead

---

## Key Features

### Tailwind CSS v4 Performance

**5x Faster Builds**:
- Tailwind v3: ~500ms incremental builds
- Tailwind v4: ~100ms incremental builds
- **Impact**: Near-instant feedback in development

**CSS-First Configuration**:
```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.5 0.2 250);
  --font-sans: system-ui, sans-serif;
  --breakpoint-md: 768px;
}
```

**No JavaScript Config**:
- ❌ REMOVED: `tailwind.config.js` (JavaScript config file)
- ✅ NEW: `@theme` directive (CSS-native config)
- **Benefit**: Zero runtime, perfect for RSC

**Automatic Content Detection**:
- No manual `content: []` configuration
- Automatically scans `.tsx`, `.jsx`, `.ts`, `.js` files
- Eliminates purge configuration errors

### shadcn/ui Component Library

**Copy-Paste Philosophy**:
```bash
# Add button component (copies source code to your project)
npx shadcn-ui add button

# Result: src/components/ui/button.tsx created
```

**Benefits**:
- Full source code control (not npm package)
- Complete customization (edit generated code)
- Zero dependency bloat (only what you use)
- Accessible by default (ARIA attributes, keyboard navigation)

**Example Component**:
```tsx
import { Button } from '@/components/ui/button'

export function Example() {
  return (
    <Button variant="outline" size="lg">
      Click me
    </Button>
  )
}
```

**Available Components** (40+):
- **Forms**: Button, Input, Select, Checkbox, Radio, Switch
- **Feedback**: Alert, Toast, Dialog, Popover, Tooltip
- **Data**: Table, Card, Badge, Avatar, Progress
- **Navigation**: Tabs, Accordion, Dropdown, Command

### CVA (Class Variance Authority)

**Type-Safe Variants**:
```tsx
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  'rounded-md font-medium transition-colors',  // Base styles
  {
    variants: {
      variant: {
        default: 'bg-primary text-white hover:bg-primary/90',
        outline: 'border border-gray-300 hover:bg-gray-100',
        ghost: 'hover:bg-gray-100',
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
)

type ButtonProps = VariantProps<typeof buttonVariants> & {
  children: React.ReactNode
}

export function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={buttonVariants({ variant, size })}>
      {children}
    </button>
  )
}

// Usage with TypeScript inference
<Button variant="outline" size="lg">Click me</Button>
```

**Compound Variants** (conditional classes):
```tsx
const buttonVariants = cva('base', {
  variants: {
    variant: { primary: 'bg-blue', secondary: 'bg-gray' },
    size: { sm: 'text-sm', lg: 'text-lg' },
  },
  compoundVariants: [
    {
      variant: 'primary',
      size: 'lg',
      className: 'font-bold',  // Only when both primary AND lg
    },
  ],
})
```

### OKLCH Color Space

**Perceptual Uniformity**:
```css
@theme {
  /* Primary (Blue) - perceptually consistent */
  --color-primary-50: oklch(0.95 0.05 250);
  --color-primary-100: oklch(0.90 0.10 250);
  --color-primary-500: oklch(0.50 0.20 250);  /* Base */
  --color-primary-900: oklch(0.20 0.15 250);

  /* Semantic colors */
  --color-success: oklch(0.60 0.18 145);  /* Green */
  --color-warning: oklch(0.75 0.15 85);   /* Yellow */
  --color-error: oklch(0.55 0.22 25);     /* Red */
}
```

**Why OKLCH?**:
- Equal numeric changes = equal perceived changes
- Easier WCAG contrast compliance
- Better dark mode (just increase lightness)
- Wide gamut for modern displays

**Dark Mode Pattern**:
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

### Dark Mode Implementation

**Next.js Setup with next-themes**:
```bash
pnpm add next-themes
```

**Theme Provider**:
```tsx
'use client'
import { ThemeProvider as NextThemesProvider } from 'next-themes'

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </NextThemesProvider>
  )
}
```

**Layout Integration**:
```tsx
// app/layout.tsx
import { ThemeProvider } from './providers/theme-provider'

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

**Theme Toggle Component**:
```tsx
'use client'
import { useTheme } from 'next-themes'
import { Button } from '@/components/ui/button'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="outline"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      {theme === 'dark' ? '☀️' : '🌙'}
    </Button>
  )
}
```

**CSS Dark Mode Classes**:
```css
/* globals.css */
@theme {
  --color-background: white;
  --color-text: black;
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: black;
    --color-text: white;
  }
}

/* Or use .dark class for manual control */
.dark {
  --color-background: black;
  --color-text: white;
}
```

### Container Queries

**Modern Responsive Design**:
```tsx
<div className="@container">
  <div className="@md:grid-cols-2 @lg:grid-cols-3 grid">
    {/* Layout changes based on CONTAINER size, not viewport */}
  </div>
</div>
```

**Benefits**:
- Component-scoped responsiveness (not global viewport)
- Reusable components across different contexts
- Better than media queries for component libraries

---

## Quick Reference

### Tailwind v4 Config

**globals.css**:
```css
@import "tailwindcss";

@theme {
  /* Colors (OKLCH) */
  --color-primary: oklch(0.5 0.2 250);
  --color-background: white;
  --color-foreground: black;

  /* Typography */
  --font-sans: system-ui, sans-serif;
  --font-mono: 'SF Mono', Consolas, monospace;

  /* Spacing */
  --spacing-unit: 0.25rem;  /* 4px base */

  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}
```

### shadcn/ui Commands

```bash
# Initialize shadcn/ui
npx shadcn-ui init

# Add components
npx shadcn-ui add button
npx shadcn-ui add input
npx shadcn-ui add card
npx shadcn-ui add dialog

# Add all components
npx shadcn-ui add --all
```

### CVA Patterns

**Basic Variant**:
```tsx
const button = cva('base-classes', {
  variants: {
    color: { blue: 'bg-blue', red: 'bg-red' },
  },
})
```

**Compound Variant**:
```tsx
const button = cva('base', {
  variants: { /* ... */ },
  compoundVariants: [{
    variant: 'primary',
    size: 'lg',
    className: 'font-bold',
  }],
})
```

**Default Variants**:
```tsx
const button = cva('base', {
  variants: { /* ... */ },
  defaultVariants: {
    variant: 'default',
    size: 'md',
  },
})
```

### Utility Functions

**cn() Helper** (merge Tailwind classes):
```tsx
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
<div className={cn('px-4 py-2', isActive && 'bg-blue-500')} />
```

---

## Integration with Other SAPs

### SAP-020 (React Foundation)
- **Link**: TypeScript strict mode for type-safe variants
- **How**: CVA uses TypeScript generics for variant props
- **Benefit**: Compile-time errors for invalid variants

### SAP-022 (React Linting)
- **Link**: ESLint plugin for Tailwind class sorting
- **How**: Add `eslint-plugin-tailwindcss` for consistent class order
- **Benefit**: Automatic class sorting (px-4 py-2 → py-2 px-4)

### SAP-023 (React State Management)
- **Link**: Zustand for theme state persistence
- **How**: Store theme in Zustand with persist middleware
- **Benefit**: Theme persists across sessions

### SAP-026 (React Accessibility)
- **Link**: shadcn/ui components are accessible by default
- **How**: ARIA attributes, keyboard navigation, focus management
- **Benefit**: WCAG 2.2 Level AA compliance out-of-box

### SAP-025 (React Performance)
- **Link**: Tailwind v4 optimization (5x faster builds)
- **How**: CSS-first config, automatic content detection
- **Benefit**: Minimal bundle size, zero runtime overhead

---

## Success Metrics

### Initial Setup (<4 minutes)
- ✅ **Dependencies Installed**: Tailwind v4, shadcn/ui, CVA
- ✅ **Config Created**: `@theme` in globals.css
- ✅ **First Component**: shadcn/ui button works
- ✅ **Dark Mode**: Theme toggle functional

### Code Quality
- ✅ **Type Safety**: CVA variants with TypeScript inference
- ✅ **Accessibility**: shadcn/ui components pass jsx-a11y linting
- ✅ **Consistency**: Tailwind classes sorted with prettier-plugin-tailwindcss
- ✅ **Color System**: OKLCH colors for perceptual uniformity

### Performance Targets
- ✅ **Build Time**: <100ms incremental (vs 500ms Tailwind v3)
- ✅ **Bundle Size**: <50 KB CSS (vs 200 KB+ with full framework)
- ✅ **First Paint**: <1.5s (optimized critical CSS)
- ✅ **CLS**: <0.1 (no layout shifts from CSS loading)

### Adoption Indicators
- ✅ **Utility-First**: 90%+ styling via Tailwind classes
- ✅ **Component Reuse**: 80%+ components use shadcn/ui or CVA
- ✅ **Dark Mode**: Theme toggle in all layouts
- ✅ **No Custom CSS**: <5% custom CSS (use Tailwind or CSS Modules escape hatch)

---

## Troubleshooting

### Problem: Tailwind classes not applying

**Symptom**: Tailwind classes have no effect on components

**Cause**: Missing `@import "tailwindcss"` in globals.css

**Fix**: Add import at top of globals.css
```css
@import "tailwindcss";

@theme {
  /* ... */
}
```

**Verify**: Check browser devtools for Tailwind CSS in <style> tags

---

### Problem: Dark mode not working

**Symptom**: Theme toggle doesn't change colors

**Cause**: Missing `suppressHydrationWarning` on <html> tag

**Fix**: Add to layout.tsx
```tsx
<html lang="en" suppressHydrationWarning>
```

**Reason**: Prevents React hydration mismatch when theme class changes

---

### Problem: shadcn/ui components not found

**Symptom**: Import error when using `@/components/ui/button`

**Cause**: Path alias not configured in tsconfig.json

**Fix**: Add to tsconfig.json
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

### Problem: CVA TypeScript errors

**Symptom**: Type errors when using component variants

**Cause**: Not using `VariantProps` type helper

**Fix**: Extract variant props type
```tsx
import { type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(/* ... */)

type ButtonProps = VariantProps<typeof buttonVariants> & {
  children: React.ReactNode
}
```

---

### Problem: Tailwind build slow despite v4

**Symptom**: Builds still take >500ms

**Cause**: Using old `@tailwindcss/postcss` version

**Fix**: Update to Tailwind v4
```bash
pnpm remove tailwindcss @tailwindcss/postcss
pnpm add -D tailwindcss@next @tailwindcss/postcss@next
```

**Verify**: Check package.json for `@next` versions

---

## Learn More

### Documentation

- **[Capability Charter](capability-charter.md)**: Problem statement, solution design, success criteria
- **[Protocol Spec](protocol-spec.md)**: Complete technical specification (Tailwind v4, shadcn/ui, CVA)
- **[Awareness Guide](awareness-guide.md)**: Detailed workflows, styling patterns, examples
- **[Adoption Blueprint](adoption-blueprint.md)**: Step-by-step installation and setup
- **[Ledger](ledger.md)**: Adoption tracking, version history, active deployments

### Official Resources

- **[Tailwind CSS Documentation](https://tailwindcss.com)**: Complete Tailwind v4 guide
- **[shadcn/ui Documentation](https://ui.shadcn.com)**: Component library and examples
- **[CVA Documentation](https://cva.style)**: Class Variance Authority patterns
- **[OKLCH Color Picker](https://oklch.com)**: Visual color picker for OKLCH

### Related SAPs

- **[SAP-020 (react-foundation)](../react-foundation/)**: TypeScript strict mode baseline
- **[SAP-022 (react-linting)](../react-linting/)**: Tailwind class sorting
- **[SAP-023 (react-state-management)](../react-state-management/)**: Theme state with Zustand
- **[SAP-025 (react-performance)](../react-performance/)**: CSS optimization
- **[SAP-026 (react-accessibility)](../react-accessibility/)**: WCAG compliance

### Research Foundation

- **RT-019-SYNTHESIS**: Styling architecture analysis (Tailwind v4 benchmarks, shadcn/ui adoption, OKLCH perceptual uniformity)

---

## Version History

- **1.0.0** (2025-11-09): Initial SAP-024 release
  - Tailwind CSS v4 baseline (5x faster builds, CSS-first @theme config)
  - shadcn/ui integration (copy-paste components, full customization)
  - CVA for type-safe variants (TypeScript inference, compound variants)
  - OKLCH color space (perceptual uniformity, better dark mode)
  - Dark mode implementation (next-themes, class-based)
  - Container queries (component-scoped responsiveness)
  - Integration with 5 SAPs (Foundation, Linting, State, Performance, Accessibility)
  - Research-backed patterns from RT-019-SYNTHESIS

---

**Next Steps**:
1. Read [adoption-blueprint.md](adoption-blueprint.md) for installation instructions
2. Install dependencies: `pnpm add -D @tailwindcss/postcss@next tailwindcss@next`
3. Initialize shadcn/ui: `npx shadcn-ui init`
4. Add first component: `npx shadcn-ui add button`
5. Implement dark mode with next-themes
