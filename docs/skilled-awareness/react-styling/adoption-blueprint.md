# SAP-024: React Styling Architecture - Adoption Blueprint

**SAP ID**: SAP-024
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01

---

## Overview

This adoption blueprint provides a step-by-step guide to adopt SAP-024 (Tailwind CSS v4 + shadcn/ui + CVA) in your React 19 project.

**Estimated setup time**: **30 minutes**

**Why SAP-024**:
- **5x faster builds**: Tailwind v4 (~100ms vs ~500ms v3)
- **100k+ stars**: shadcn/ui is the most popular React component library (2024)
- **Zero-runtime**: Perfect React Server Components compatibility
- **60-80% smaller bundles**: vs CSS-in-JS solutions

---

## Prerequisites

### Required
- ✅ Node.js 20+ and npm 10+
- ✅ React 19 project (Next.js 15 or Vite 7)
- ✅ TypeScript 5.3+

### Recommended
- ✅ VS Code with Tailwind CSS IntelliSense extension
- ✅ SAP-020 (React Foundation) for project templates

---

## Quick Start (30 Minutes)

### Phase 1: Install Dependencies (5 minutes)

**Step 1.1**: Install Tailwind CSS v4

```bash
# For Next.js 15
npm install tailwindcss@^4.0.0 @tailwindcss/postcss@^4.0.0

# For Vite 7
npm install -D tailwindcss@^4.0.0 postcss@^8.4.47 autoprefixer@^10.4.20
```

**Step 1.2**: Install Component Dependencies

```bash
npm install class-variance-authority@^0.7.1 clsx@^2.1.1 tailwind-merge@^2.5.5
npm install next-themes@^0.4.4
npm install @radix-ui/react-slot@^1.0.2 @radix-ui/react-label@^2.0.2
npm install @radix-ui/react-dialog@^1.0.5 @radix-ui/react-dropdown-menu@^2.0.6
npm install lucide-react@^0.468.0
```

**Verification**:

```bash
npm list | grep -E "tailwindcss|class-variance|next-themes|radix-ui"
```

Expected output: All packages installed successfully.

---

### Phase 2: Configure Tailwind (10 minutes)

**Step 2.1**: Copy PostCSS Configuration

**For Next.js 15**:

```bash
cp templates/react/styling/nextjs/postcss.config.mjs postcss.config.mjs
```

**For Vite 7**:

```bash
cp templates/react/styling/vite/postcss.config.js postcss.config.js
```

**Step 2.2**: Copy Global CSS

**For Next.js 15**:

```bash
cp templates/react/styling/nextjs/globals.css app/globals.css
```

**For Vite 7**:

```bash
cp templates/react/styling/vite/globals.css src/index.css
```

**Step 2.3**: Set Up Path Aliases

**File**: `tsconfig.json` (add to `compilerOptions`)

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

**File**: `vite.config.ts` (Vite only)

```typescript
import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

**Verification**:

```bash
# Start dev server
npm run dev

# Check browser console - no errors related to Tailwind
```

---

### Phase 3: Install Core Components (10 minutes)

**Step 3.1**: Create Directory Structure

```bash
mkdir -p src/lib src/providers src/components/ui
```

**Step 3.2**: Copy Utility Files

```bash
cp templates/react/styling/shared/lib/utils.ts src/lib/utils.ts
cp templates/react/styling/shared/lib/cva-utils.ts src/lib/cva-utils.ts
cp templates/react/styling/shared/providers/theme-provider.tsx src/providers/theme-provider.tsx
```

**Step 3.3**: Copy Core Components

```bash
# Core components (8 total)
cp templates/react/styling/shared/components/ui/button.tsx src/components/ui/button.tsx
cp templates/react/styling/shared/components/ui/card.tsx src/components/ui/card.tsx
cp templates/react/styling/shared/components/ui/input.tsx src/components/ui/input.tsx
cp templates/react/styling/shared/components/ui/label.tsx src/components/ui/label.tsx
cp templates/react/styling/shared/components/ui/dialog.tsx src/components/ui/dialog.tsx
cp templates/react/styling/shared/components/ui/dropdown-menu.tsx src/components/ui/dropdown-menu.tsx
cp templates/react/styling/shared/components/ui/theme-toggle.tsx src/components/ui/theme-toggle.tsx
cp templates/react/styling/shared/components/ui/responsive-example.tsx src/components/ui/responsive-example.tsx
```

**Step 3.4**: Set Up Theme Provider

**For Next.js 15** (`app/layout.tsx`):

```typescript
import { ThemeProvider } from "@/providers/theme-provider"
import "./globals.css"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

**For Vite 7** (`src/main.tsx`):

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider } from './providers/theme-provider'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
```

**Verification**:

```bash
# Start dev server
npm run dev

# Create test page to verify components work
```

---

### Phase 4: Test Installation (5 minutes)

**Step 4.1**: Create Test Page

**For Next.js 15** (`app/test-styling/page.tsx`):

```typescript
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ThemeToggle } from "@/components/ui/theme-toggle"

export default function TestStylingPage() {
  return (
    <div className="container mx-auto p-8 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-4xl font-bold">SAP-024 Test Page</h1>
        <ThemeToggle />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Component Test</CardTitle>
          <CardDescription>Testing SAP-024 components</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="you@example.com" />
          </div>

          <div className="flex gap-2">
            <Button>Default</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </div>

          <div className="flex gap-2">
            <Button size="sm">Small</Button>
            <Button size="default">Default</Button>
            <Button size="lg">Large</Button>
            <Button size="icon">🚀</Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Card 1</CardTitle>
          </CardHeader>
          <CardContent>Responsive grid test</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Card 2</CardTitle>
          </CardHeader>
          <CardContent>Responsive grid test</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Card 3</CardTitle>
          </CardHeader>
          <CardContent>Responsive grid test</CardContent>
        </Card>
      </div>
    </div>
  )
}
```

**For Vite 7** (`src/pages/TestStyling.tsx`):

```typescript
// Same code as Next.js example above
```

**Step 4.2**: Verify in Browser

1. Navigate to `/test-styling` (Next.js) or add route (Vite)
2. Check button variants (default, destructive, outline, secondary, ghost, link)
3. Check button sizes (small, default, large, icon)
4. Check dark mode toggle (click theme toggle, verify colors change)
5. Check responsive grid (resize window, verify 1→2→3 columns)

**Expected Results**:
- ✅ All buttons render with correct styles
- ✅ Dark mode toggle switches theme (sun/moon icon)
- ✅ Grid adapts to screen size (1 column mobile, 2 tablet, 3 desktop)
- ✅ No console errors

---

## Integration with SAP-020

SAP-024 integrates seamlessly with SAP-020 (React Foundation) project templates.

### Option 1: New Project (SAP-020 + SAP-024)

```bash
# Step 1: Create project from SAP-020 template
cp -r templates/react/nextjs-15 my-project
cd my-project
npm install

# Step 2: Add SAP-024 styling (follow Phase 1-3 above)
npm install tailwindcss@^4.0.0 @tailwindcss/postcss@^4.0.0
# ... continue with Phase 1-3
```

### Option 2: Existing SAP-020 Project

```bash
# You already have a Next.js 15 or Vite 7 project from SAP-020
# Just follow Phase 1-3 above to add SAP-024 styling
```

---

## Customization Guide

### Customize Colors

**File**: `app/globals.css` or `src/index.css`

```css
@theme {
  /* Change primary color (default: neutral) */
  --color-primary: oklch(0.55 0.22 250);  /* Blue */
  --color-primary-foreground: oklch(0.98 0 0);

  /* Add brand colors */
  --color-brand: oklch(0.60 0.20 330);  /* Pink */
  --color-brand-foreground: oklch(0.98 0 0);
}

/* Usage */
<Button className="bg-brand text-brand-foreground">Brand Button</Button>
```

### Customize Border Radius

```css
@theme {
  --radius-sm: 0.125rem;   /* 2px - sharp corners */
  --radius-md: 0.375rem;   /* 6px - slightly rounded */
  --radius-lg: 0.5rem;     /* 8px - default */
  --radius-xl: 1rem;       /* 16px - very rounded */
}
```

### Add Custom Breakpoints

```css
@theme {
  --breakpoint-3xl: 1920px;  /* 4K monitors */
  --breakpoint-4xl: 2560px;  /* Ultra-wide */
}

/* Usage */
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 3xl:grid-cols-4">
```

### Add Custom Component Variants

**File**: `lib/cva-utils.ts`

```typescript
export const buttonVariants = cva(
  "inline-flex items-center justify-center...",
  {
    variants: {
      variant: {
        default: "...",
        // Add custom variant
        gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
      },
    },
  }
)

// Usage
<Button variant="gradient">Gradient Button</Button>
```

---

## Validation Checklist

Use this checklist to verify SAP-024 is correctly installed:

### Dependencies
- [ ] Tailwind CSS v4.0+ installed
- [ ] class-variance-authority v0.7.1+ installed
- [ ] next-themes v0.4.4+ installed
- [ ] Radix UI packages installed
- [ ] lucide-react v0.468+ installed

### Configuration
- [ ] PostCSS config created (`postcss.config.mjs` or `postcss.config.js`)
- [ ] Global CSS created (`app/globals.css` or `src/index.css`)
- [ ] Path aliases configured (`@/*` maps to `src/*`)
- [ ] Theme provider added to layout/main

### Components
- [ ] `src/lib/utils.ts` (cn helper)
- [ ] `src/lib/cva-utils.ts` (CVA patterns)
- [ ] `src/providers/theme-provider.tsx` (dark mode provider)
- [ ] 8 UI components in `src/components/ui/`

### Functionality
- [ ] Dev server starts without errors
- [ ] Tailwind classes apply (check in browser DevTools)
- [ ] Dark mode toggle works (theme changes)
- [ ] Responsive design works (grid adapts to screen size)
- [ ] No hydration errors in console

### Performance
- [ ] Production build succeeds (`npm run build`)
- [ ] CSS bundle size <10KB (check build output, typical: 6-8KB gzipped)
- [ ] Build time ≤200ms (Tailwind v4 target: ~100ms, vs ~500ms v3)
- [ ] Lighthouse Performance score ≥90
- [ ] Lighthouse Accessibility score ≥90 (WCAG 2.2 Level AA)
- [ ] Zero runtime JavaScript from Tailwind (check bundle analysis)

---

## Troubleshooting

### Issue: "Cannot find module '@/lib/utils'"

**Solution**: Configure path aliases in `tsconfig.json` and `vite.config.ts` (Vite only).

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Issue: "Unknown at rule @tailwind"

**Solution**: Use `@import "tailwindcss"` (v4) instead of `@tailwind base` (v3).

```css
/* ✅ Correct (v4) */
@import "tailwindcss";

/* ❌ Wrong (v3) */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Issue: Dark mode not working

**Solution**: Ensure `attribute="class"` in ThemeProvider and `suppressHydrationWarning` on `<html>`.

```typescript
// layout.tsx
<html lang="en" suppressHydrationWarning>
  <body>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
```

### Issue: Hydration mismatch errors

**Solution**: Use `mounted` flag for components that read `useTheme()`.

```typescript
import { useEffect, useState } from "react"
import { useTheme } from "next-themes"

function Component() {
  const { theme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])

  if (!mounted) return null

  return <div>{theme}</div>
}
```

**More Troubleshooting**: See [awareness-guide.md](awareness-guide.md#troubleshooting-guide)

---

## Next Steps

### Immediate (First Hour)
1. ✅ Complete 30-minute setup (Phase 1-4)
2. ✅ Create test page, verify components work
3. ✅ Customize colors/radius to match brand
4. ✅ Build first feature with SAP-024 components

### Short-term (First Week)
1. Install additional shadcn/ui components as needed:
   ```bash
   npx shadcn@latest add select checkbox radio switch tabs
   ```
2. Create custom CVA variants for project-specific components
3. Set up responsive design patterns for main layout
4. Test dark mode across all pages

### Long-term (First Month)
1. Migrate existing components to Tailwind (if applicable)
2. Measure bundle size, optimize if needed
3. Run Lighthouse audit, ensure ≥90 scores
4. Document project-specific styling patterns
5. Share feedback with chora-base (open issue/PR)

---

## Advanced Patterns

### Pattern 1: Custom Design System

**File**: `app/globals.css`

```css
@import "tailwindcss";

@theme {
  /* Brand Colors */
  --color-brand-primary: oklch(0.55 0.22 250);
  --color-brand-secondary: oklch(0.60 0.18 330);
  --color-brand-accent: oklch(0.70 0.15 145);

  /* Typography Scale (1.25 ratio) */
  --font-size-xs: 0.64rem;   /* 10px */
  --font-size-sm: 0.8rem;    /* 13px */
  --font-size-base: 1rem;    /* 16px */
  --font-size-lg: 1.25rem;   /* 20px */
  --font-size-xl: 1.563rem;  /* 25px */
  --font-size-2xl: 1.953rem; /* 31px */
  --font-size-3xl: 2.441rem; /* 39px */

  /* Spacing (8px base, Fibonacci sequence) */
  --spacing-1: 0.5rem;   /* 8px */
  --spacing-2: 0.75rem;  /* 12px */
  --spacing-3: 1.25rem;  /* 20px */
  --spacing-4: 2rem;     /* 32px */
  --spacing-5: 3.25rem;  /* 52px */
  --spacing-6: 5.25rem;  /* 84px */
}
```

### Pattern 2: Animation System

**File**: `app/globals.css`

```css
@theme {
  --animate-duration-instant: 100ms;
  --animate-duration-fast: 150ms;
  --animate-duration-base: 200ms;
  --animate-duration-slow: 300ms;
  --animate-duration-slower: 500ms;

  --animate-timing-linear: linear;
  --animate-timing-ease: ease;
  --animate-timing-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --animate-timing-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --animate-timing-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --animate-timing-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@layer utilities {
  .animate-fade-in {
    animation: fade-in var(--animate-duration-base) var(--animate-timing-ease-out);
  }

  .animate-slide-up {
    animation: slide-up var(--animate-duration-base) var(--animate-timing-ease-out);
  }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Usage**:

```tsx
<div className="animate-fade-in">Fades in on mount</div>
<div className="animate-slide-up">Slides up on mount</div>
```

### Pattern 3: Container Queries

**File**: `tailwind.config.ts` (Vite only)

```typescript
export default {
  theme: {
    extend: {
      containers: {
        '2xs': '16rem',
        'xs': '20rem',
        'sm': '24rem',
        'md': '28rem',
        'lg': '32rem',
        'xl': '36rem',
        '2xl': '42rem',
      },
    },
  },
}
```

**Usage**:

```tsx
<div className="@container">
  <Card className="@sm:flex-row flex flex-col">
    <div className="@sm:w-1/3 w-full">Image</div>
    <div className="@sm:w-2/3 w-full">Content</div>
  </Card>
</div>
```

---

## Success Metrics

Track these metrics after adopting SAP-024:

### Setup Metrics
- [ ] Setup time ≤30 minutes
- [ ] Zero errors during installation
- [ ] Test page renders correctly
- [ ] Dark mode toggle works

### Performance Metrics
- [ ] Production CSS bundle ≤10KB (gzipped)
- [ ] Lighthouse Performance ≥90
- [ ] First Contentful Paint ≤1.5s
- [ ] Time to Interactive ≤3s

### Quality Metrics
- [ ] Lighthouse Accessibility ≥90 (WCAG 2.2 Level AA)
- [ ] Zero hydration errors
- [ ] Responsive design works across devices
- [ ] Dark mode works without flash

### Developer Experience Metrics
- [ ] Time to create new component ≤5 minutes
- [ ] TypeScript autocomplete works for variants
- [ ] VS Code IntelliSense suggests Tailwind classes
- [ ] Team satisfaction ≥8/10

---

## Support & Resources

### Documentation
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Business case, ROI, scope
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Technical patterns, code examples
- **Awareness Guide**: [awareness-guide.md](awareness-guide.md) - Decision trees, troubleshooting
- **Ledger**: [ledger.md](ledger.md) - Adoption tracking, lessons learned

### External Resources
- **Tailwind CSS v4**: https://tailwindcss.com/docs
- **shadcn/ui**: https://ui.shadcn.com/
- **CVA**: https://cva.style/docs
- **next-themes**: https://github.com/pacocoursey/next-themes
- **Radix UI**: https://www.radix-ui.com/

### Community
- **Issues**: Open issue in chora-base repository
- **Discussions**: GitHub Discussions for Q&A
- **Contributions**: Submit PR with improvements to templates

---

## Conclusion

This adoption blueprint provides a 30-minute setup guide for SAP-024 (React Styling Architecture). Follow Phase 1-4 for quick setup, then customize colors/radius to match your brand.

**Total Time**: 30 minutes (5min dependencies + 10min config + 10min components + 5min testing)

**Next Steps**: Build your first feature with SAP-024 components, then share feedback with chora-base community.

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-01
