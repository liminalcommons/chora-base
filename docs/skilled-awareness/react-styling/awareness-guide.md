# SAP-024: React Styling Architecture - Awareness Guide

**SAP ID**: SAP-024
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01

---

## Overview

This awareness guide helps developers make informed decisions about React styling approaches, avoid common pitfalls, and troubleshoot issues when using SAP-024 (Tailwind CSS v4 + shadcn/ui + CVA).

---

## Decision Trees

### 1. Which Styling Approach Should I Use?

```
Start: Need to style React components
│
├─ Do you need dynamic runtime styles (CSS variables from JS)?
│  ├─ YES → CSS-in-JS (Emotion, Styled Components)
│  └─ NO → Continue
│
├─ Is bundle size a primary concern (<10KB CSS)?
│  ├─ YES → Tailwind CSS (SAP-024) ✅
│  └─ NO → Continue
│
├─ Do you need component library (pre-built components)?
│  ├─ YES → Tailwind + shadcn/ui (SAP-024) ✅
│  └─ NO → Continue
│
├─ Do you prefer traditional CSS (separate files)?
│  ├─ YES → CSS Modules
│  └─ NO → Tailwind CSS (SAP-024) ✅
│
└─ Default: Tailwind CSS (SAP-024) ✅
```

**Recommendation**: Use SAP-024 (Tailwind + shadcn/ui) for 90% of projects. Use CSS Modules for 5% edge cases (complex animations). Avoid CSS-in-JS unless you have specific runtime requirements.

---

### 2. Tailwind CSS vs CSS Modules vs CSS-in-JS

| Factor | Tailwind CSS v4 (SAP-024) | CSS Modules | CSS-in-JS |
|--------|------------------------|-------------|-----------|
| **Bundle Size** | 6-15KB | 20-50KB | 60-100KB |
| **Runtime** | Zero (pure CSS) | Zero (pure CSS) | 5-15KB + parsing |
| **RSC Compatibility** | Perfect (zero-JS) | Perfect | **Poor (incompatible)** |
| **Build Speed** | **5x faster than v3** | Fast | Slower (runtime) |
| **Learning Curve** | Moderate (utility classes) | Low (traditional CSS) | Steep (CSS-in-JS API) |
| **Maintenance** | Single source (Tailwind) | Multiple CSS files | JavaScript files |
| **Performance** | Fastest | Fast | Slower (runtime) |
| **Dark Mode** | Built-in (`dark:`) | Manual | Manual/runtime |
| **Responsive** | Built-in (`sm:`, `md:`) | Manual (`@media`) | Manual/runtime |
| **Community** | **Growing (80% adoption)** | Medium (20%) | **Declining (10-15%)** |
| **React 19 Support** | Full support | Full support | **Limited (RSC issues)** |

**Use Tailwind CSS (SAP-024) when**:
- ✅ Building new React 19 app (Next.js 15 or Vite 7)
- ✅ Need small bundle size (<10KB CSS)
- ✅ Want pre-built accessible components (shadcn/ui)
- ✅ Need dark mode + responsive design out-of-box
- ✅ Prefer utility-first approach (fast iteration)

**Use CSS Modules when**:
- ✅ Complex keyframe animations (10+ steps)
- ✅ Team prefers traditional CSS workflow
- ✅ Migrating legacy project gradually
- ✅ Need CSS Grid with named areas

**Use CSS-in-JS when**:
- ⚠️ **CAUTION**: CSS-in-JS is declining due to React Server Components incompatibility
- ⚠️ **Emotion, Styled Components**: Deprecation trend (State of CSS 2024)
- ⚠️ **RSC Issues**: Runtime CSS generation doesn't work with Server Components
- ✅ **Only if**: Legacy project migration or very specific runtime styling needs
- 🔄 **Recommended**: Migrate to Tailwind v4 or CSS Modules

**CSS-in-JS Deprecation Context** (RT-019 Research):
- React Server Components (RSC) incompatible with runtime CSS generation
- styled-components, Emotion declining in adoption (State of CSS 2024)
- Zero-runtime solutions preferred: Tailwind v4, CSS Modules, vanilla-extract
- **Migration path**: CSS-in-JS → Tailwind v4 typically 2-4 days for medium apps (see Migration Guides below)

---

### 3. Which shadcn/ui Component Should I Use?

```
Need a component?
│
├─ Interactive controls?
│  ├─ Button → button.tsx
│  ├─ Link → button.tsx (asChild with Link)
│  ├─ Icon button → button.tsx (variant="ghost" size="icon")
│  └─ Toggle → Future (install with shadcn CLI)
│
├─ Form inputs?
│  ├─ Text input → input.tsx
│  ├─ Label → label.tsx
│  ├─ Select → Future (install with shadcn CLI)
│  ├─ Checkbox → Future (install with shadcn CLI)
│  └─ Radio → Future (install with shadcn CLI)
│
├─ Layout containers?
│  ├─ Card → card.tsx
│  ├─ Container → div with Tailwind classes
│  └─ Grid → div with Tailwind grid classes
│
├─ Overlays?
│  ├─ Modal → dialog.tsx
│  ├─ Dropdown → dropdown-menu.tsx
│  ├─ Tooltip → Future (install with shadcn CLI)
│  └─ Popover → Future (install with shadcn CLI)
│
└─ Theme?
   └─ Dark mode toggle → theme-toggle.tsx
```

**Note**: SAP-024 includes 8 core components. Install additional components with:

```bash
npx shadcn@latest add [component-name]
```

---

### 4. When to Use CVA vs Inline Tailwind?

```
Styling a component?
│
├─ Does it have 3+ visual variants (primary, secondary, destructive)?
│  ├─ YES → Use CVA (class-variance-authority) ✅
│  └─ NO → Continue
│
├─ Does it have 3+ size variants (sm, md, lg)?
│  ├─ YES → Use CVA ✅
│  └─ NO → Continue
│
├─ Is it reused in 5+ places?
│  ├─ YES → Use CVA (easier to maintain) ✅
│  └─ NO → Inline Tailwind ✅
│
└─ Default: Inline Tailwind ✅
```

**Example - Use CVA**:
```typescript
// Good: Button has many variants + sizes, reused everywhere
export const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: { default: "...", destructive: "...", outline: "..." },
      size: { default: "...", sm: "...", lg: "..." },
    },
  }
)
```

**Example - Use Inline Tailwind**:
```typescript
// Good: One-off component, no variants, not reused
<div className="flex items-center gap-2 p-4 rounded-lg bg-muted">
  Simple component
</div>
```

---

### 5. How to Handle Dark Mode?

```
Need dark mode?
│
├─ Entire app?
│  ├─ YES → Use next-themes (ThemeProvider) ✅
│  └─ NO → Use Tailwind dark: prefix directly
│
├─ Specific sections only?
│  ├─ YES → Use dark: prefix on container ✅
│  └─ NO → Full app dark mode
│
└─ User toggle or system preference?
   ├─ User toggle → theme-toggle.tsx ✅
   ├─ System only → ThemeProvider (defaultTheme="system")
   └─ Both → ThemeProvider + theme-toggle.tsx ✅
```

**Pattern - Full App Dark Mode**:
```typescript
// layout.tsx
<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
  <ThemeToggle />
  {children}
</ThemeProvider>
```

**Pattern - Section-Only Dark Mode**:
```typescript
// Force dark mode for specific section
<div className="dark">
  <div className="bg-background text-foreground">
    This section is always dark
  </div>
</div>
```

---

## Common Pitfalls

### 1. Forgetting to Merge Tailwind Classes

**Problem**: Conflicting Tailwind classes aren't resolved automatically.

❌ **Bad**:
```typescript
function Button({ className }) {
  return <button className={`px-4 py-2 ${className}`} />  // px-4 + px-8 both apply
}

<Button className="px-8" />  // Has BOTH px-4 (from component) + px-8 (from prop)
```

✅ **Good**:
```typescript
import { cn } from "@/lib/utils"

function Button({ className }) {
  return <button className={cn("px-4 py-2", className)} />  // px-8 wins
}

<Button className="px-8" />  // Only px-8 applies (conflict resolved)
```

**Solution**: Always use `cn()` helper to merge Tailwind classes.

---

### 2. Not Using Selectors with CVA

**Problem**: Destructuring full variant object causes unnecessary re-renders.

❌ **Bad**:
```typescript
function Button(props: ButtonProps) {
  return <button className={buttonVariants(props)} />  // Re-renders on ANY prop change
}
```

✅ **Good**:
```typescript
function Button({ variant, size, className, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
```

**Solution**: Destructure only needed variant props (variant, size), pass rest with `...props`.

---

### 3. SSR Hydration Mismatch with Dark Mode

**Problem**: Server renders light mode, client renders dark mode (localStorage).

❌ **Bad**:
```typescript
// Server: renders "Light Mode" (default)
// Client: reads localStorage, renders "Dark Mode"
// Result: Hydration error
function Theme() {
  const { theme } = useTheme()
  return <div>{theme} Mode</div>
}
```

✅ **Good**:
```typescript
function Theme() {
  const { theme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])

  if (!mounted) return null  // Skip render on server + first client render

  return <div>{theme} Mode</div>
}
```

**Solution**: Use `mounted` flag to skip render until hydration complete. Add `suppressHydrationWarning` to `<html>` tag.

---

### 4. Hardcoding Colors Instead of CSS Variables

**Problem**: Dark mode doesn't work for hardcoded colors.

❌ **Bad**:
```typescript
<div className="bg-white text-black">
  {/* Doesn't adapt to dark mode */}
</div>
```

✅ **Good**:
```typescript
<div className="bg-background text-foreground">
  {/* Uses CSS variables, adapts to dark mode */}
</div>
```

**Solution**: Use semantic color names (`bg-background`, `text-foreground`, `bg-primary`) instead of literal colors (`bg-white`, `text-black`).

---

### 5. Overusing `!important` with Tailwind

**Problem**: `!important` breaks Tailwind's cascade and responsive design.

❌ **Bad**:
```typescript
<div className="!p-4 sm:!p-8">
  {/* !important on both makes responsive design fragile */}
</div>
```

✅ **Good**:
```typescript
<div className="p-4 sm:p-8">
  {/* Tailwind's cascade handles specificity */}
</div>
```

**Solution**: Avoid `!important` (marked by `!` prefix). If needed, use `!` only on the override, not base class.

---

### 6. Not Extracting Repeated Patterns

**Problem**: Copy-pasting same Tailwind classes in 20 places.

❌ **Bad**:
```typescript
// Repeated in 20 components
<div className="flex items-center gap-2 p-4 rounded-lg bg-card text-card-foreground shadow-sm">
  Card content
</div>
```

✅ **Good**:
```typescript
// Create component
export function Card({ className, ...props }) {
  return (
    <div
      className={cn(
        "flex items-center gap-2 p-4 rounded-lg bg-card text-card-foreground shadow-sm",
        className
      )}
      {...props}
    />
  )
}

// Use everywhere
<Card>Card content</Card>
```

**Solution**: Extract repeated patterns into components or CVA variants.

---

### 7. Mixing Tailwind v3 and v4 Syntax

**Problem**: Tailwind v4 uses CSS-first configuration, not JavaScript config.

❌ **Bad (v3 syntax)**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
      },
    },
  },
}
```

✅ **Good (v4 syntax)**:
```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.55 0.22 250);
}
```

**Solution**: Use @theme directive in CSS for Tailwind v4 (Next.js 15). Use JavaScript config only for Vite 7 with Tailwind v3.

---

## Troubleshooting Guide

### Issue 1: Tailwind Classes Not Applying

**Symptoms**:
- Tailwind classes in code, but no styles in browser
- "Unknown at rule @tailwind" warning in CSS

**Diagnosis**:

1. **Check PostCSS configuration**:
   ```javascript
   // postcss.config.mjs (Next.js 15)
   export default {
     plugins: {
       '@tailwindcss/postcss': {},  // ✅ Correct
       // 'tailwindcss': {},        // ❌ Wrong (v3 syntax)
     },
   }
   ```

2. **Check CSS import**:
   ```css
   /* globals.css */
   @import "tailwindcss";  /* ✅ Correct (v4) */
   /* @tailwind base; */   /* ❌ Wrong (v3) */
   ```

3. **Check content configuration** (Vite only):
   ```typescript
   // tailwind.config.ts
   export default {
     content: [
       './index.html',
       './src/**/*.{js,ts,jsx,tsx}',  // ✅ Includes all files
     ],
   }
   ```

**Solution**: Ensure PostCSS config uses `@tailwindcss/postcss` (v4) and globals.css uses `@import "tailwindcss"`.

---

### Issue 2: Dark Mode Not Working

**Symptoms**:
- Dark mode toggle doesn't change theme
- `dark:` classes not applying

**Diagnosis**:

1. **Check ThemeProvider attribute**:
   ```typescript
   <ThemeProvider
     attribute="class"  // ✅ Must be "class"
     // attribute="data-theme"  // ❌ Wrong
   >
   ```

2. **Check Tailwind dark mode configuration**:
   ```typescript
   // tailwind.config.ts (Vite)
   export default {
     darkMode: ['class'],  // ✅ Correct
     // darkMode: 'media',  // ❌ Uses only system preference
   }
   ```

3. **Check suppressHydrationWarning**:
   ```typescript
   <html lang="en" suppressHydrationWarning>  {/* ✅ Required */}
   ```

4. **Check dark: prefix usage**:
   ```typescript
   <div className="bg-white dark:bg-slate-900">  {/* ✅ Correct */}
   ```

**Solution**: Set `attribute="class"` in ThemeProvider, `darkMode: ['class']` in Tailwind config, and `suppressHydrationWarning` on `<html>`.

---

### Issue 3: Hydration Mismatch Errors

**Symptoms**:
- Warning: "Text content did not match. Server: ... Client: ..."
- Flash of unstyled content (FOUC) on page load

**Diagnosis**:

1. **Check if using theme on first render**:
   ```typescript
   // ❌ Bad: Reads theme immediately (server = default, client = localStorage)
   function Component() {
     const { theme } = useTheme()
     return <div>{theme}</div>  // Hydration mismatch
   }
   ```

2. **Add mounted check**:
   ```typescript
   // ✅ Good: Skip render until mounted
   function Component() {
     const { theme } = useTheme()
     const [mounted, setMounted] = useState(false)

     useEffect(() => setMounted(true), [])

     if (!mounted) return null

     return <div>{theme}</div>
   }
   ```

**Solution**: Use `mounted` flag for components that read `useTheme()`. Add `suppressHydrationWarning` to `<html>` tag.

---

### Issue 4: CVA Variants Not Applying

**Symptoms**:
- Variant prop passed, but styles not changing
- TypeScript error: "Type '...' is not assignable to type '...'"

**Diagnosis**:

1. **Check variant is passed to cva()**:
   ```typescript
   // ❌ Bad: Variant not passed to buttonVariants()
   function Button({ variant, className }) {
     return <button className={cn(buttonVariants(), className)} />
   }

   // ✅ Good: Variant passed
   function Button({ variant, className }) {
     return <button className={cn(buttonVariants({ variant }), className)} />
   }
   ```

2. **Check variant spelling**:
   ```typescript
   // ❌ Bad: "destruct" (typo)
   <Button variant="destruct" />

   // ✅ Good: "destructive" (matches CVA definition)
   <Button variant="destructive" />
   ```

3. **Check TypeScript type extraction**:
   ```typescript
   // ✅ Must extract VariantProps for TypeScript
   export type ButtonVariants = VariantProps<typeof buttonVariants>

   interface ButtonProps extends ButtonVariants {
     // ...
   }
   ```

**Solution**: Pass variant to `buttonVariants({ variant, size })` and ensure TypeScript types are extracted with `VariantProps`.

---

### Issue 5: Responsive Classes Not Working

**Symptoms**:
- `sm:`, `md:`, `lg:` classes not applying at correct breakpoints
- Mobile design shows desktop layout

**Diagnosis**:

1. **Check mobile-first approach**:
   ```typescript
   // ❌ Bad: Largest to smallest (not mobile-first)
   <div className="lg:grid-cols-4 md:grid-cols-2 grid-cols-1">

   // ✅ Good: Smallest to largest (mobile-first)
   <div className="grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
   ```

2. **Check viewport meta tag**:
   ```html
   <!-- ✅ Required in <head> -->
   <meta name="viewport" content="width=device-width, initial-scale=1" />
   ```

3. **Check breakpoint values** (Vite only):
   ```typescript
   // tailwind.config.ts
   export default {
     theme: {
       screens: {
         sm: '640px',   // ✅ Default
         md: '768px',
         lg: '1024px',
         xl: '1280px',
         '2xl': '1536px',
       },
     },
   }
   ```

**Solution**: Use mobile-first approach (base = mobile, add `sm:`/`md:`/`lg:` for larger screens). Ensure viewport meta tag exists.

---

### Issue 6: shadcn/ui Component Import Errors

**Symptoms**:
- "Module not found: @/components/ui/button"
- "Cannot find module '@/lib/utils'"

**Diagnosis**:

1. **Check path aliases** (TypeScript):
   ```json
   // tsconfig.json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["./src/*"]  // ✅ Maps @/ to ./src/
       }
     }
   }
   ```

2. **Check path aliases** (Vite):
   ```typescript
   // vite.config.ts
   import path from 'path'

   export default defineConfig({
     resolve: {
       alias: {
         "@": path.resolve(__dirname, "./src"),  // ✅ Maps @/ to ./src/
       },
     },
   })
   ```

3. **Check file exists**:
   ```bash
   ls src/components/ui/button.tsx  # ✅ Should exist
   ls src/lib/utils.ts              # ✅ Should exist
   ```

**Solution**: Configure `@/*` path alias in `tsconfig.json` and `vite.config.ts` (Vite only). Ensure component files copied from SAP-024 templates.

---

## Migration Guides

### Migrating from CSS-in-JS to Tailwind

**Step 1**: Install Tailwind v4 (follow adoption-blueprint.md)

**Step 2**: Convert styled components to Tailwind

```typescript
// Before (Emotion)
import styled from '@emotion/styled'

const Button = styled.button`
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: blue;
  color: white;
  border-radius: 0.375rem;

  &:hover {
    background-color: darkblue;
  }
`

// After (Tailwind)
function Button({ children, ...props }) {
  return (
    <button
      className="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
      {...props}
    >
      {children}
    </button>
  )
}
```

**Step 3**: Convert theme to @theme directive

```typescript
// Before (Emotion theme)
const theme = {
  colors: {
    primary: '#3B82F6',
    secondary: '#6B7280',
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
  },
}

// After (Tailwind @theme)
@theme {
  --color-primary: oklch(0.55 0.22 250);
  --color-secondary: oklch(0.5 0.05 250);

  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
}
```

**Step 4**: Remove CSS-in-JS dependencies

```bash
npm uninstall @emotion/react @emotion/styled styled-components
```

**Estimated Time**: 2-4 hours for small project (10-20 components)

---

### Migrating from Tailwind v3 to v4

**Why Migrate**: Tailwind v4 provides **5x faster builds** (~100ms vs ~500ms), CSS-first configuration, and zero-runtime output for better React Server Components compatibility.

**Step 1**: Update dependencies

```bash
npm install tailwindcss@^4.0.0 @tailwindcss/postcss@^4.0.0
```

**Step 2**: Update PostCSS config

```javascript
// Before (v3)
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

// After (v4) - postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

**Step 3**: Update globals.css

```css
/* Before (v3) */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* After (v4) */
@import "tailwindcss";

@theme {
  /* Move theme config from tailwind.config.js to here */
}
```

**Step 4**: Move theme config to @theme directive

```javascript
// Before (v3 - tailwind.config.js)
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
      },
    },
  },
}

// After (v4 - globals.css)
@theme {
  --color-primary: oklch(0.55 0.22 250);
}
```

**Step 5**: Remove old config files

```bash
# Tailwind v4 uses CSS-first config, so remove:
rm tailwind.config.js  # or .ts, .mjs
# Keep only postcss.config.mjs
```

**Breaking Changes**:
- `@tailwind` directives replaced with `@import "tailwindcss"`
- JavaScript theme config replaced with CSS @theme directive
- Automatic content detection (no `content: []` config needed in most cases)
- OKLCH color space recommended (better perceptual uniformity than HSL)
- Container queries native (no plugin needed)

**Performance Improvement**:
- **5x faster builds**: ~100ms (v4) vs ~500ms (v3) for typical projects
- **Smaller bundle**: Better tree-shaking with CSS-first approach
- **Zero-JS config**: Faster parsing, better caching

**Estimated Time**: 1-2 hours for medium projects (10-20 components)

**Validation Checklist**:
- [ ] Dev server starts without errors
- [ ] All Tailwind classes still apply
- [ ] Dark mode still works (test toggle)
- [ ] Responsive breakpoints work (resize window)
- [ ] Production build succeeds
- [ ] Bundle size reduced or similar

---

## Best Practices

### 1. Component Organization

**Pattern**: Separate layout, primitive, and feature components

```
src/
├── components/
│   ├── ui/           # Primitive components (shadcn/ui)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── input.tsx
│   ├── layout/       # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── sidebar.tsx
│   └── features/     # Feature-specific components
│       ├── auth/
│       │   └── login-form.tsx
│       └── dashboard/
│           └── metrics-card.tsx
```

### 2. CVA Variant Organization

**Pattern**: Co-locate variants with components

```typescript
// components/ui/button.tsx
const buttonVariants = cva(/* ... */)  // ✅ Co-located

export function Button({ variant, size, ...props }) {
  return <button className={cn(buttonVariants({ variant, size }))} {...props} />
}

// ❌ Don't: Separate file for just variants
// lib/button-variants.ts
```

### 3. Responsive Design Strategy

**Pattern**: Mobile-first, then add breakpoints

```typescript
// ✅ Good: Mobile base, tablet (md), desktop (lg)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// ❌ Bad: Desktop base, then shrink
<div className="grid grid-cols-3 lg:grid-cols-2 md:grid-cols-1 gap-4">
```

### 4. Color Naming

**Pattern**: Semantic names, not literal colors

```typescript
// ✅ Good: Semantic (adapts to dark mode)
<div className="bg-background text-foreground border-border">

// ❌ Bad: Literal (breaks in dark mode)
<div className="bg-white text-black border-gray-200">
```

### 5. Spacing Consistency

**Pattern**: Use Tailwind's spacing scale (4px base)

```typescript
// ✅ Good: Uses spacing scale (4, 8, 12, 16, 24, 32)
<div className="p-4 space-y-4">
  <div className="mb-6">Item 1</div>
  <div className="mb-8">Item 2</div>
</div>

// ❌ Bad: Arbitrary values (inconsistent)
<div className="p-[13px] space-y-[17px]">
```

---

## Conclusion

This awareness guide provides decision trees, troubleshooting steps, and best practices for SAP-024 (React Styling Architecture). Use these patterns to make informed decisions and avoid common pitfalls.

**Key Takeaways**:
1. ✅ Use Tailwind for 90% of projects, CSS Modules for 5% edge cases
2. ✅ Always use `cn()` helper to merge Tailwind classes
3. ✅ Use CVA for components with 3+ variants or sizes
4. ✅ Use semantic color names (`bg-background`) not literal (`bg-white`)
5. ✅ Use mobile-first responsive design (base = mobile, add `sm:`/`md:`/`lg:`)
6. ✅ Use `mounted` flag to prevent dark mode hydration mismatch
7. ✅ Extract repeated patterns into components or CVA variants

**Next Steps**: See [adoption-blueprint.md](adoption-blueprint.md) for 30-minute setup guide.

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-01
