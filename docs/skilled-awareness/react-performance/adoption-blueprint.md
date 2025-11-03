# SAP-025: React Performance Optimization - Adoption Blueprint

**SAP ID**: SAP-025
**Version**: 1.0.0
**Status**: Active
**Category**: Technology-Specific SAP (React/Performance)
**Created**: 2025-11-01
**Last Updated**: 2025-11-01

---

## Overview

This blueprint provides a **60-minute setup guide** for adopting SAP-025 in your React project.

**Time Breakdown**:
- Prerequisites & Planning: 10 minutes
- Configuration Setup: 10 minutes
- Template Integration: 25 minutes
- Lighthouse CI Setup: 10 minutes
- Validation & Testing: 5 minutes

---

## Prerequisites (10 minutes)

### Required Tools

- [ ] **Node.js 22+** (`node --version`)
- [ ] **npm 10+** or **pnpm 9+** (`npm --version`)
- [ ] **Git** (`git --version`)
- [ ] **Code editor** (VS Code recommended)

### Required Knowledge

- [ ] React fundamentals (hooks, components)
- [ ] Next.js or Vite basics (routing, config)
- [ ] Basic performance concepts (LCP, bundle size)

### Project Requirements

- [ ] **React 19+** (or React 18.2+)
- [ ] **Next.js 15+** OR **Vite 7+**
- [ ] **TypeScript** (recommended but optional)

### Pre-Adoption Checklist

- [ ] Run baseline Lighthouse audit (record scores)
- [ ] Measure current bundle size (`npm run build`)
- [ ] Identify performance bottlenecks (LCP >2.5s, INP >200ms, CLS >0.1)
- [ ] Back up project (`git commit -am "Pre-SAP-025 baseline"`)

---

## Setup Guide: Next.js 15 (30 minutes)

### Step 1: Copy Configuration Files (5 minutes)

```bash
# Navigate to SAP-025 templates
cd path/to/chora-base/templates/react/performance

# Copy Next.js configurations
cp nextjs/next.config.performance.ts $YOUR_PROJECT/next.config.ts
cp nextjs/middleware.performance.ts $YOUR_PROJECT/middleware.ts
cp nextjs/instrumentation.ts $YOUR_PROJECT/instrumentation.ts
```

**Verification**:
```bash
# Verify files exist
ls -la next.config.ts middleware.ts instrumentation.ts
```

---

### Step 2: Install Dependencies (3 minutes)

```bash
cd $YOUR_PROJECT

# Core dependencies
npm install web-vitals

# Dev dependencies for bundle analysis
npm install -D webpack-bundle-analyzer
```

**Verification**:
```bash
# Verify installation
npm list web-vitals webpack-bundle-analyzer
```

---

### Step 3: Copy Code Splitting Patterns (5 minutes)

```bash
# Create patterns directory
mkdir -p src/lib/patterns

# Copy patterns
cp path/to/templates/shared/patterns/*.tsx src/lib/patterns/
cp path/to/templates/shared/patterns/*.ts src/lib/patterns/
```

**Files copied**:
- `lazy-route.tsx` - Route-based code splitting
- `lazy-component.tsx` - Component-based lazy loading
- `dynamic-import.ts` - Dynamic imports with retry
- `suspense-boundary.tsx` - Suspense boundaries

---

### Step 4: Set Up Image Optimization (5 minutes)

```bash
# Create components directory
mkdir -p src/components

# Copy image components
cp path/to/templates/shared/components/optimized-image.tsx src/components/
cp path/to/templates/shared/lib/image-loader.ts src/lib/
```

**Update next.config.ts** (if using CDN):
```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    loader: 'custom',
    loaderFile: './src/lib/image-loader.ts',  // ✅ Add this
  },
}
```

---

### Step 5: Set Up Font Optimization (5 minutes)

```bash
# Copy font configuration
cp path/to/templates/shared/fonts/font-config.ts src/lib/fonts.ts
```

**Update app/layout.tsx**:
```typescript
// app/layout.tsx
import { inter, robotoMono } from '@/lib/fonts'
import './globals.css'

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${robotoMono.variable}`}
    >
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

---

### Step 6: Set Up Web Vitals Monitoring (5 minutes)

```bash
# Copy Web Vitals library
cp path/to/templates/shared/lib/web-vitals.ts src/lib/
```

**Create API route**:
```typescript
// app/api/web-vitals/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const data = await request.json()

  console.log('[Web Vitals]', data)

  // TODO: Send to analytics service
  // await sendToAnalytics(data)

  return NextResponse.json({ success: true })
}
```

**Update app/layout.tsx**:
```typescript
// app/layout.tsx
'use client'
import { useEffect } from 'react'
import { reportWebVitals } from '@/lib/web-vitals'

export default function RootLayout({ children }) {
  useEffect(() => {
    reportWebVitals()  // ✅ Start monitoring
  }, [])

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

---

### Step 7: Set Up Lighthouse CI (10 minutes)

```bash
# Copy Lighthouse CI files
mkdir -p ci
cp path/to/templates/ci/lighthouserc.json ./
cp path/to/templates/ci/lighthouse-budget.json ./ci/

# Copy GitHub Actions workflow
mkdir -p .github/workflows
cp path/to/templates/ci/lighthouse-ci.yml .github/workflows/
```

**Update lighthouserc.json URLs**:
```json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000/",
        "http://localhost:3000/dashboard"  // ✅ Update with your routes
      ]
    }
  }
}
```

**Install Lighthouse CI locally**:
```bash
npm install -g @lhci/cli
```

---

### Step 8: Copy Bundle Analysis Script (2 minutes)

```bash
# Copy script
mkdir -p scripts
cp path/to/templates/shared/scripts/analyze-bundle.js scripts/
chmod +x scripts/analyze-bundle.js
```

---

### Step 9: Validation & Testing (5 minutes)

```bash
# 1. Build project
npm run build

# 2. Run bundle analysis
node scripts/analyze-bundle.js --framework=nextjs

# 3. Run Lighthouse CI
lhci autorun

# 4. Start dev server and test
npm run dev
```

**Expected Results**:
- ✅ Build succeeds
- ✅ Bundle size within budgets (script <200KB, total <750KB)
- ✅ Lighthouse Performance score ≥90
- ✅ Core Web Vitals: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1

---

## Setup Guide: Vite 7 (30 minutes)

### Step 1: Copy Configuration Files (5 minutes)

```bash
# Copy Vite configurations
cp path/to/templates/vite/vite.config.performance.ts $YOUR_PROJECT/vite.config.ts
cp path/to/templates/vite/vite-env.d.ts $YOUR_PROJECT/src/vite-env.d.ts
cp path/to/templates/vite/.env.example $YOUR_PROJECT/.env.example
```

---

### Step 2: Install Dependencies (3 minutes)

```bash
cd $YOUR_PROJECT

# Core dependencies
npm install web-vitals

# Dev dependencies
npm install -D rollup-plugin-visualizer vite-plugin-compression2
```

---

### Step 3: Copy Code Splitting Patterns (5 minutes)

```bash
# Same as Next.js (framework-agnostic patterns)
mkdir -p src/lib/patterns
cp path/to/templates/shared/patterns/*.tsx src/lib/patterns/
cp path/to/templates/shared/patterns/*.ts src/lib/patterns/
```

---

### Step 4: Set Up Image Optimization (5 minutes)

```bash
# Copy Vite image component
mkdir -p src/components
cp path/to/templates/shared/components/vite-image.tsx src/components/
```

---

### Step 5: Set Up Font Optimization (5 minutes)

```bash
# Copy font CSS
mkdir -p src/styles
cp path/to/templates/shared/fonts/font-face.css src/styles/fonts.css
```

**Import in main.tsx**:
```typescript
// src/main.tsx
import './styles/fonts.css'  // ✅ Add this
import './index.css'
```

---

### Step 6: Set Up Web Vitals Monitoring (5 minutes)

```bash
# Copy Web Vitals library
cp path/to/templates/shared/lib/web-vitals.ts src/lib/
```

**Update main.tsx**:
```typescript
// src/main.tsx
import { reportWebVitals } from './lib/web-vitals'

// Start monitoring
reportWebVitals()  // ✅ Add this
```

---

### Step 7: Set Up Lighthouse CI (Same as Next.js, 10 minutes)

```bash
# Copy Lighthouse CI files
mkdir -p ci
cp path/to/templates/ci/lighthouserc.json ./
cp path/to/templates/ci/lighthouse-budget.json ./ci/
cp path/to/templates/ci/lighthouse-ci.yml .github/workflows/
```

**Update lighthouserc.json for Vite**:
```json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run preview",  // ✅ Vite preview
      "url": ["http://localhost:4173/"]  // ✅ Vite preview port
    }
  }
}
```

---

### Step 8: Validation & Testing (5 minutes)

```bash
# 1. Build project
npm run build

# 2. Run bundle analysis
node scripts/analyze-bundle.js --framework=vite

# 3. Preview build
npm run preview

# 4. Run Lighthouse CI
lhci autorun
```

---

## Post-Adoption Tasks

### Immediate (First Day)

- [ ] Update README with performance targets
- [ ] Document custom optimizations (if any)
- [ ] Share results with team (before/after metrics)
- [ ] Update ledger.md with adoption details

### First Week

- [ ] Monitor Web Vitals via analytics dashboard
- [ ] Review Lighthouse CI results on PRs
- [ ] Identify slow routes and optimize further
- [ ] Train team on SAP-025 patterns

### First Month

- [ ] Review performance trends (weekly reports)
- [ ] Adjust performance budgets if needed
- [ ] Document lessons learned in ledger.md
- [ ] Share success story (if applicable)

---

## Troubleshooting

### Issue: Build Fails After Copying Templates

**Cause**: TypeScript errors due to missing types

**Solution**:
```bash
# Install missing types
npm install -D @types/react @types/node
```

---

### Issue: Lighthouse CI Fails to Start Server

**Cause**: Incorrect `startServerCommand` or port

**Solution**:
```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",  // Next.js
      // OR
      "startServerCommand": "npm run preview",  // Vite
      "startServerReadyPattern": "ready on|Local:",
      "startServerReadyTimeout": 60000
    }
  }
}
```

---

### Issue: Web Vitals Not Sending

**Cause**: API route not created

**Solution**:
```bash
# Next.js: Create app/api/web-vitals/route.ts
# Vite: Set up Express endpoint at /api/web-vitals
```

---

## Validation Checklist

### Configuration
- [ ] next.config.ts or vite.config.ts copied and customized
- [ ] Environment variables configured (.env.local)
- [ ] TypeScript types resolved (no build errors)

### Templates
- [ ] Code splitting patterns copied to src/lib/patterns
- [ ] Image optimization component copied
- [ ] Font configuration set up
- [ ] Web Vitals monitoring configured

### Lighthouse CI
- [ ] lighthouserc.json configured with correct URLs
- [ ] lighthouse-budget.json adjusted for project
- [ ] GitHub Actions workflow added
- [ ] Lighthouse CI passes locally

### Performance
- [ ] Bundle size within budgets (run analyze-bundle.js)
- [ ] Core Web Vitals meet targets (run Lighthouse)
- [ ] No performance regressions (compare with baseline)

---

## Success Criteria

### Quantitative
- [ ] Setup completed in ≤60 minutes
- [ ] Lighthouse Performance score ≥90
- [ ] LCP ≤2.5s (75th percentile)
- [ ] INP ≤200ms (75th percentile)
- [ ] CLS ≤0.1 (75th percentile)
- [ ] Bundle size <750KB

### Qualitative
- [ ] Team can explain Core Web Vitals targets
- [ ] Developers understand when to use code splitting
- [ ] Performance monitoring dashboard set up
- [ ] Lighthouse CI integrated into PR workflow

---

## Next Steps

1. **Document Custom Optimizations**: Record any project-specific patterns in ledger.md
2. **Set Up Monitoring Alerts**: Configure alerts for LCP/INP/CLS thresholds
3. **Train Team**: Conduct 1-hour workshop on SAP-025 patterns
4. **Review Quarterly**: Update dependencies, adjust budgets

---

## Support

### Getting Help

- **Documentation**: [templates/react/performance/README.md](../../../templates/react/performance/README.md)
- **Examples**: See template files for code examples
- **Troubleshooting**: [awareness-guide.md](./awareness-guide.md)

### Feedback

- **Report Issues**: Create issue in chora-base repo
- **Suggest Improvements**: Submit PR with enhancements
- **Share Success**: Add adoption story to ledger.md

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-01
