# SAP-025: React Performance Optimization - Awareness Guide

**SAP ID**: SAP-025
**Version**: 1.0.0
**Status**: Active
**Category**: Technology-Specific SAP (React/Performance)
**Created**: 2025-11-01
**Last Updated**: 2025-11-01

---

## Purpose

This guide helps developers make informed decisions about performance optimization using SAP-025 templates. It includes:

- Decision trees for choosing optimization strategies
- Performance budget guidelines
- Common pitfalls and how to avoid them
- Troubleshooting guide for Core Web Vitals issues

---

## Decision Tree: When to Use SAP-025

```
START: Do you have a React application?
│
├─ NO → SAP-025 not applicable
│
└─ YES → Is performance a concern?
    │
    ├─ NO → Consider SAP-025 proactively (prevent issues)
    │
    └─ YES → What's your primary concern?
        │
        ├─ Slow initial load (LCP >2.5s)
        │   └─ Use: Image optimization + Code splitting
        │
        ├─ Slow interactions (INP >200ms)
        │   └─ Use: Code splitting + Event optimization
        │
        ├─ Layout shifts (CLS >0.1)
        │   └─ Use: Image dimensions + Font optimization
        │
        └─ Large bundle size (>750KB)
            └─ Use: Code splitting + Bundle analysis
```

---

## Decision Tree: Code Splitting Strategy

```
START: What are you trying to optimize?
│
├─ Entire page/route
│   └─ Use: Route-based code splitting (lazy-route.tsx)
│       Example: Dashboard, Settings, Profile pages
│
├─ Heavy component (>50KB)
│   ├─ Visible above fold?
│   │   ├─ YES → Load immediately (no lazy loading)
│   │   └─ NO → Use viewport-based lazy loading (lazy-component.tsx)
│   │
│   └─ Examples: Charts, Maps, Rich Text Editors
│
├─ User interaction required
│   └─ Use: Interaction-based lazy loading (lazy-component.tsx)
│       Example: Modals, Tooltips, Dropdowns
│
└─ Third-party library
    └─ Use: Dynamic imports with retry (dynamic-import.ts)
        Example: Analytics, Chat widgets
```

---

## Decision Tree: Image Optimization

```
START: What type of image?
│
├─ Hero image (above fold)
│   └─ Use: priority={true} + AVIF format
│       Target: LCP <2.5s
│
├─ Product images (e-commerce)
│   └─ Use: Responsive srcset + lazy loading
│       Formats: AVIF → WebP → JPEG fallback
│
├─ Avatars/thumbnails (<100KB)
│   └─ Use: Lazy loading + fixed dimensions
│       Consider: Inline as base64 if <4KB
│
├─ Background images
│   └─ Use: CSS background-image with image-set()
│       Formats: AVIF, WebP, JPEG
│
└─ Icons
    └─ Use: SVG sprites or icon font
        Avoid: Individual image files
```

---

## Decision Tree: Font Optimization

```
START: How many fonts do you need?
│
├─ 1-2 fonts
│   └─ Use: Variable fonts (single file for all weights)
│       Example: Inter Variable (100-900 weights in 1 file)
│
├─ 3+ fonts
│   ├─ Are they all above fold?
│   │   ├─ YES → Preload all (increase TTFB risk)
│   │   └─ NO → Preload only above-fold fonts
│   │
│   └─ Consider: Reducing number of fonts
│
└─ Custom font vs Google Fonts?
    ├─ Google Fonts → Use next/font (self-hosted)
    │   Benefit: Eliminates external request
    │
    └─ Custom font → Use localFont with WOFF2
        Benefit: Full control over subsetting
```

---

## Performance Budgets

### Core Web Vitals Budgets

| Metric | Good | Needs Improvement | Poor | Your Target |
|--------|------|-------------------|------|-------------|
| **LCP** | ≤2.5s | 2.5-4.0s | >4.0s | **≤2.5s** |
| **INP** | ≤200ms | 200-500ms | >500ms | **≤200ms** |
| **CLS** | ≤0.1 | 0.1-0.25 | >0.25 | **≤0.1** |

### Bundle Size Budgets

| Resource | Budget | Tolerance | Rationale |
|----------|--------|-----------|-----------|
| **script** (JS) | 200 KB | 50 KB | HTTP Archive P50 for React apps |
| **stylesheet** (CSS) | 50 KB | 20 KB | Tailwind CSS production average |
| **image** | 300 KB | 100 KB | 2-3 hero images (AVIF compressed) |
| **font** | 100 KB | 30 KB | 2 variable fonts (WOFF2) |
| **total** | 750 KB | 150 KB | Google "good" threshold |

### Timing Budgets

| Metric | Budget | Tolerance | Impact |
|--------|--------|-----------|--------|
| **TTFB** | 800ms | 200ms | Server response time |
| **FCP** | 1500ms | 200ms | First visible content |
| **LCP** | 2500ms | 300ms | Main content visible |
| **TBT** | 300ms | 100ms | Main thread blocking |
| **TTI** | 3000ms | 500ms | Page interactive |

---

## Common Pitfalls

### Pitfall 1: Over-Optimization

**Symptom**: Spending hours optimizing non-critical paths

**Example**:
```typescript
// ❌ Bad: Lazy loading small components
const Button = lazy(() => import('./Button'))  // Button is 2KB!

// ✅ Good: Only lazy load heavy components (>50KB)
const HeavyChart = lazy(() => import('./HeavyChart'))  // 85KB
```

**Rule of Thumb**: Only lazy load components >50KB

---

### Pitfall 2: Missing Image Dimensions

**Symptom**: CLS >0.1 despite using next/image

**Example**:
```typescript
// ❌ Bad: Missing dimensions causes layout shift
<Image src="/hero.jpg" alt="Hero" fill />

// ✅ Good: Explicit dimensions prevent layout shift
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080} />
```

**Impact**: -70% CLS (0.18 → 0.05)

---

### Pitfall 3: Too Many Dynamic Imports

**Symptom**: Dozens of network requests on page load

**Example**:
```typescript
// ❌ Bad: Every utility function dynamically imported
const formatDate = (await import('./formatDate')).default
const formatCurrency = (await import('./formatCurrency')).default

// ✅ Good: Group utilities in one module
import { formatDate, formatCurrency } from './utils'
```

**Rule**: <10 dynamic imports per route

---

### Pitfall 4: Preloading Too Many Fonts

**Symptom**: TTFB >1s, LCP >3s

**Example**:
```html
<!-- ❌ Bad: Preloading 5 fonts blocks rendering -->
<link rel="preload" href="/font1.woff2" as="font" />
<link rel="preload" href="/font2.woff2" as="font" />
<link rel="preload" href="/font3.woff2" as="font" />
<link rel="preload" href="/font4.woff2" as="font" />
<link rel="preload" href="/font5.woff2" as="font" />

<!-- ✅ Good: Preload only above-fold fonts (1-2 max) -->
<link rel="preload" href="/inter-variable.woff2" as="font" />
```

**Rule**: Preload ≤2 fonts

---

## Troubleshooting Guide

### Issue: LCP >2.5s

#### Diagnosis

1. **Identify LCP element**:
   ```javascript
   new PerformanceObserver((list) => {
     const entries = list.getEntries()
     const lastEntry = entries[entries.length - 1]
     console.log('LCP element:', lastEntry.element)
   }).observe({ type: 'largest-contentful-paint', buffered: true })
   ```

2. **Common LCP elements**:
   - Hero image (60% of cases)
   - Heading text with web font (30%)
   - Video thumbnail (10%)

#### Solutions

**If LCP element is image**:
```typescript
// ✅ Add priority loading
<OptimizedImage
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  priority  // Preload this image
  sizes="100vw"
/>
```

**If LCP element is text**:
```typescript
// ✅ Preload font
export const inter = Inter({
  preload: true,  // Add <link rel="preload">
  display: 'optional',  // Prevent font swap shift
})
```

**If LCP is caused by JavaScript**:
```typescript
// ✅ Code split heavy bundles
const HeavyComponent = lazy(() => import('./HeavyComponent'))
```

---

### Issue: INP >200ms

#### Diagnosis

1. **Measure interaction latency**:
   ```javascript
   import { onINP } from 'web-vitals'

   onINP((metric) => {
     console.log('INP:', metric.value, 'ms')
     console.log('Attribution:', metric.attribution)
   })
   ```

2. **Common causes**:
   - Heavy JavaScript on main thread (50%)
   - Unoptimized event handlers (30%)
   - Large DOM size (20%)

#### Solutions

**If main thread is blocked**:
```typescript
// ✅ Code split heavy components
const Dashboard = lazy(() => import('./Dashboard'))

<Suspense fallback={<Skeleton />}>
  <Dashboard />
</Suspense>
```

**If event handlers are slow**:
```typescript
// ✅ Debounce expensive operations
import { useDeferredValue } from 'react'

const deferredSearch = useDeferredValue(search)
```

**If DOM is large** (>1500 nodes):
```typescript
// ✅ Virtualize long lists
import { useVirtualizer } from '@tanstack/react-virtual'

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
})
```

---

### Issue: CLS >0.1

#### Diagnosis

1. **Identify shifting elements**:
   ```javascript
   new PerformanceObserver((list) => {
     for (const entry of list.getEntries()) {
       console.log('Layout shift:', entry.value, entry.sources)
     }
   }).observe({ type: 'layout-shift', buffered: true })
   ```

2. **Common causes**:
   - Images without dimensions (50%)
   - Fonts causing layout shift (30%)
   - Dynamic content insertion (20%)

#### Solutions

**If images cause shift**:
```typescript
// ✅ Always set width/height
<Image
  src="/product.jpg"
  alt="Product"
  width={600}  // Explicit dimensions
  height={600}
  />
```

**If fonts cause shift**:
```typescript
// ✅ Use font-display: optional
export const inter = Inter({
  display: 'optional',  // Skip font if not loaded quickly
  adjustFontFallback: true,  // Match fallback metrics
})
```

**If dynamic content causes shift**:
```typescript
// ✅ Reserve space with skeleton
<div className="h-64 w-full">  {/* Fixed height */}
  <Suspense fallback={<Skeleton className="h-64" />}>
    <DynamicContent />
  </Suspense>
</div>
```

---

## Monitoring & Alerts

### Real User Monitoring (RUM)

```typescript
// app/layout.tsx
import { reportWebVitals } from '@/lib/web-vitals'

useEffect(() => {
  reportWebVitals()  // Send metrics to analytics
}, [])
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| **LCP** | >2.5s | >4.0s |
| **INP** | >200ms | >500ms |
| **CLS** | >0.1 | >0.25 |
| **Bundle Size** | >750KB | >1MB |

### Example Alert Logic

```typescript
function sendAlert(metric) {
  if (metric.value > CRITICAL_THRESHOLD) {
    notify('🚨 Critical performance issue', metric)
  } else if (metric.value > WARNING_THRESHOLD) {
    notify('⚠️ Performance warning', metric)
  }
}
```

---

## Best Practices Checklist

### Images
- [ ] Use AVIF format with WebP/JPEG fallbacks
- [ ] Set explicit width/height on all images
- [ ] Use `priority` for hero images
- [ ] Use lazy loading for below-fold images
- [ ] Use responsive srcset for different screen sizes
- [ ] Optimize images to <300KB total per page

### Fonts
- [ ] Use variable fonts (single file for all weights)
- [ ] Self-host fonts (no external requests)
- [ ] Use WOFF2 format (smallest size)
- [ ] Preload only above-fold fonts (1-2 max)
- [ ] Use `font-display: swap` or `optional`
- [ ] Subset fonts to needed characters

### Code Splitting
- [ ] Split code by route
- [ ] Lazy load heavy components (>50KB)
- [ ] Use viewport-based loading for below-fold components
- [ ] Limit dynamic imports to <10 per route
- [ ] Add retry logic for network-resilient imports

### Monitoring
- [ ] Set up Lighthouse CI with performance budgets
- [ ] Monitor Core Web Vitals with Real User Monitoring
- [ ] Set up alerts for LCP/INP/CLS thresholds
- [ ] Review performance metrics weekly
- [ ] Run bundle analysis on every build

---

## Performance Testing Checklist

### Before Deployment

- [ ] Run Lighthouse CI locally (`lhci autorun`)
- [ ] Verify Core Web Vitals meet targets (LCP ≤2.5s, INP ≤200ms, CLS ≤0.1)
- [ ] Run bundle analysis (`node scripts/analyze-bundle.js`)
- [ ] Test on slow 3G network (Chrome DevTools)
- [ ] Test on mobile device (real device, not simulator)

### After Deployment

- [ ] Monitor RUM data for first 24 hours
- [ ] Check for performance regressions
- [ ] Verify Lighthouse CI passes on all PRs
- [ ] Review alert notifications

---

## Quick Reference

### Core Web Vitals Targets

| Metric | Target |
|--------|--------|
| **LCP** | ≤2.5s |
| **INP** | ≤200ms |
| **CLS** | ≤0.1 |

### Bundle Size Budgets

| Resource | Budget |
|----------|--------|
| **script** | 200 KB |
| **stylesheet** | 50 KB |
| **image** | 300 KB |
| **font** | 100 KB |
| **total** | 750 KB |

### Key Commands

```bash
# Build and analyze
npm run build
node scripts/analyze-bundle.js --framework=nextjs

# Run Lighthouse CI
npm install -g @lhci/cli
lhci autorun

# Monitor Web Vitals
# (Automatic with reportWebVitals() in app)
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-01
