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

### RT-019 Principle: "Measure First!"

**NEVER optimize without measurement.** RT-019 research shows that 40% of performance optimization efforts are wasted on the wrong problems. Always start with data.

```
START: Do you have a React application?
│
├─ NO → SAP-025 not applicable
│
└─ YES → Have you measured performance?
    │
    ├─ NO → **STOP! Measure first:**
    │   │   1. Run Lighthouse: npx lighthouse http://localhost:3000 --view
    │   │   2. Check Core Web Vitals (LCP, INP, CLS)
    │   │   3. Analyze bundle size: ANALYZE=true npm run build
    │   │   4. Install Real User Monitoring (Vercel Analytics or web-vitals)
    │   │   └─ Return to this tree after measurement
    │
    └─ YES → What does your data show? (Priority order)
        │
        ├─ **Priority 1: INP >200ms** (Most common issue - 60% of React apps)
        │   ├─ Diagnosis: Heavy JavaScript blocks main thread
        │   ├─ Root cause:
        │   │   - Large initial bundle (>100KB JS)
        │   │   - Heavy event handlers without debouncing
        │   │   - Long synchronous tasks
        │   │   - Too much client-side JavaScript (use RSC)
        │   └─ Solutions (in priority order):
        │       1. React Server Components (40-60% bundle reduction)
        │       2. Code splitting (route-based + component-based)
        │       3. useDeferredValue for search/filters
        │       4. startTransition for non-urgent updates
        │       5. Reduce bundle to <100KB initial
        │
        ├─ **Priority 2: LCP >2.5s** (Second most common - 45% of apps)
        │   ├─ Diagnosis: Slow content rendering
        │   ├─ Root cause:
        │   │   - Large hero images without optimization
        │   │   - Fonts not preloaded
        │   │   - Heavy JavaScript blocking render
        │   │   - No priority loading
        │   └─ Solutions:
        │       1. Image optimization (AVIF + priority={true})
        │       2. Font optimization (self-host, preload)
        │       3. Code splitting (reduce blocking JS)
        │       4. Preconnect to third-party domains
        │
        ├─ **Priority 3: CLS >0.1** (30% of apps)
        │   ├─ Diagnosis: Layout shifts during load
        │   ├─ Root cause:
        │   │   - Images without width/height
        │   │   - Fonts causing FOUT/FOIT
        │   │   - Dynamic content insertion
        │   └─ Solutions:
        │       1. Explicit image dimensions
        │       2. font-display: optional
        │       3. Skeleton placeholders
        │
        ├─ **Priority 4: Large bundle (>300KB initial)**
        │   └─ Solutions:
        │       1. React Server Components
        │       2. Code splitting
        │       3. Tree-shaking (Next.js 15 optimizePackageImports)
        │       4. Bundle analysis to find heavy dependencies
        │
        └─ **All metrics good?** → Set up monitoring to prevent regressions
            ├─ Lighthouse CI for automated testing
            ├─ Real User Monitoring (Vercel Analytics or web-vitals)
            └─ Performance budgets in CI/CD
```

**RT-019 Finding**: 60% of React apps fail **INP** on mobile, making it the #1 priority for optimization in 2025.

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

### RT-019 Updated Core Web Vitals Budgets (2025)

| Metric | Good | Needs Improvement | Poor | RT-019 Target | Changed? |
|--------|------|-------------------|------|---------------|----------|
| **LCP** | ≤2.5s | 2.5-4.0s | >4.0s | **≤2.5s** | No change |
| **INP** | ≤200ms | 200-500ms | >500ms | **≤200ms** | **NEW** (replaced FID) |
| **CLS** | ≤0.1 | 0.1-0.25 | >0.25 | **≤0.1** | No change |
| ~~**FID**~~ | ~~≤100ms~~ | ~~100-300ms~~ | ~~>300ms~~ | **DEPRECATED** | Replaced by INP (March 2024) |

**RT-019 Key Change**: **INP (Interaction to Next Paint)** replaced FID (First Input Delay) as a Core Web Vital in **March 2024**. INP measures ALL interactions during page lifetime, not just the first input.

**Why INP Matters More**:
- FID only measured first interaction (incomplete picture)
- INP measures 75th percentile of all interactions (full user experience)
- 60% of React apps fail INP on mobile (RT-019 finding)
- Correlates with -35% bounce rate improvement

### RT-019 Updated Bundle Size Budgets (2025)

| Resource | RT-019 Budget | Previous | Tolerance | Rationale |
|----------|---------------|----------|-----------|-----------|
| **script (initial)** | **100 KB** | 200 KB | 20 KB | Interactive in <2s on 3G |
| **script (total)** | **200 KB** | N/A | 50 KB | All routes combined |
| **stylesheet** (CSS) | **50 KB** | 50 KB | 10 KB | Tailwind v4 production |
| **image (per page)** | **300 KB** | 300 KB | 50 KB | AVIF-compressed hero images |
| **font (total)** | **100 KB** | 100 KB | 20 KB | 2 variable fonts (WOFF2) |
| **total (initial)** | **300 KB** | 750 KB | 50 KB | **BREAKING CHANGE** |

**RT-019 Breaking Change**: Total budget reduced from **750KB → 300KB** for initial page load.

**Rationale**: Apps exceeding 300KB initial load show:
- +40% bounce rate on mobile
- -25% conversion rate
- 60% fail INP on mobile (<100KB is ideal)

### RT-019 Timing Budgets

| Metric | RT-019 Budget | Previous | Tolerance | Impact |
|--------|---------------|----------|-----------|--------|
| **TTFB** | **800ms** | N/A | 200ms | Server response time |
| **FCP** | **1500ms** | 1500ms | 200ms | First visible content |
| **LCP** | **2500ms** | 2500ms | 300ms | Main content visible |
| **INP** | **200ms** | N/A (FID) | 50ms | **NEW** interaction latency |
| **TBT** | **200ms** | 300ms | 50ms | Proxy for INP (lab) |
| **TTI** | **3000ms** | 3000ms | 500ms | Page interactive |

**RT-019 Addition**: **INP** is now the primary interaction metric (replacing FID). Target: <200ms for 75th percentile.

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

### Issue: INP >200ms (RT-019: #1 Performance Issue)

**RT-019 Finding**: INP is the **most common performance issue** in React apps (60% failure rate on mobile).

#### Diagnosis

1. **Measure interaction latency with web-vitals v4+**:
   ```javascript
   import { onINP } from 'web-vitals'

   onINP((metric) => {
     console.log('INP:', metric.value, 'ms')
     console.log('Rating:', metric.rating)  // 'good', 'needs-improvement', 'poor'
     console.log('Attribution:', metric.attribution)

     // Log slow interactions
     if (metric.value > 200) {
       console.warn('❌ INP exceeds 200ms threshold')
       console.log('Interaction type:', metric.attribution.interactionType)  // 'click', 'keyboard', etc.
       console.log('Interaction target:', metric.attribution.interactionTarget)
       console.log('Input delay:', metric.attribution.inputDelay)
       console.log('Processing time:', metric.attribution.processingTime)
       console.log('Presentation delay:', metric.attribution.presentationDelay)
     }
   })
   ```

2. **RT-019 Common causes** (priority order):
   - **60%**: Large JavaScript bundle (>100KB initial) blocking main thread
   - **25%**: Unoptimized event handlers (synchronous state updates)
   - **10%**: Large DOM size (>1500 nodes)
   - **5%**: Heavy third-party scripts

#### RT-019 Solutions (Apply in Priority Order)

**Priority 1: Reduce Bundle Size with React Server Components**
```typescript
// ❌ BAD: Everything on client (150KB bundle)
'use client'
import { useState } from 'react'
import { fetchData } from './api'

export default function Page() {
  const [data, setData] = useState([])
  useEffect(() => {
    fetchData().then(setData)
  }, [])
  return <Dashboard data={data} />
}

// ✅ GOOD: Server Component (80KB bundle, -47% JS)
async function Page() {
  const data = await fetchData()  // Server-side, zero client JS
  return <Dashboard data={data} />  // Only Dashboard is client JS
}
```

**Impact**: 40-60% bundle reduction, -45% INP improvement (RT-019 evidence)

---

**Priority 2: Code Split Heavy Components**
```typescript
// ✅ Lazy load dashboard chart (85KB)
import { lazy, Suspense } from 'react'

const HeavyChart = lazy(() => import('@/components/heavy-chart'))

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

**Impact**: -45% INP (350ms → 190ms) by reducing parse time

---

**Priority 3: Use useDeferredValue for Non-Urgent Updates**
```typescript
// ❌ BAD: Synchronous state update blocks interaction
function SearchBox() {
  const [search, setSearch] = useState('')
  const results = expensiveSearch(search)  // Blocks main thread

  return <input value={search} onChange={(e) => setSearch(e.target.value)} />
}

// ✅ GOOD: Defer non-urgent updates (React 19)
import { useDeferredValue } from 'react'

function SearchBox() {
  const [search, setSearch] = useState('')
  const deferredSearch = useDeferredValue(search)  // React schedules update
  const results = expensiveSearch(deferredSearch)

  return <input value={search} onChange={(e) => setSearch(e.target.value)} />
}
```

**Impact**: -40% INP (300ms → 180ms) by deferring updates (RT-019 React 19 benchmarks)

---

**Priority 4: Use startTransition for Long Tasks**
```typescript
// ✅ Mark non-urgent state updates
import { startTransition } from 'react'

function handleClick() {
  startTransition(() => {
    // Non-urgent updates (React yields to main thread)
    setLargeDataset(processData())
  })
}
```

**Impact**: -35% INP (280ms → 180ms) by yielding to browser

---

**Priority 5: Virtualize Large Lists** (>1500 DOM nodes)
```typescript
// ❌ BAD: Render 10,000 items (INP >500ms)
{items.map(item => <Card key={item.id} data={item} />)}

// ✅ GOOD: Virtualize with @tanstack/react-virtual
import { useVirtualizer } from '@tanstack/react-virtual'

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
  overscan: 5,  // Render 5 extra items for smooth scrolling
})

{virtualizer.getVirtualItems().map(virtualItem => (
  <Card key={items[virtualItem.index].id} data={items[virtualItem.index]} />
))}
```

**Impact**: -60% INP for large lists (500ms → 200ms)

---

### RT-019 INP Optimization Checklist

- [ ] **Measure first**: Install web-vitals v4.2.4+, track INP
- [ ] **Bundle <100KB**: Use React Server Components, code splitting
- [ ] **Defer updates**: Use useDeferredValue for search/filters
- [ ] **Break long tasks**: Use startTransition for non-urgent updates
- [ ] **Virtualize**: Use @tanstack/react-virtual for lists >100 items
- [ ] **Monitor**: Set up Real User Monitoring (Vercel Analytics or custom)
- [ ] **Alert**: Slack/email alert if 75th percentile INP >200ms

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

### RT-019 Recommendation: Real User Monitoring (RUM)

**Lab data vs. Real User Monitoring**:
- **Lab data** (Lighthouse): Synthetic testing on simulated networks
- **RUM**: Real user data from actual devices/networks
- **RT-019 Finding**: RUM data is 30% more accurate for detecting regressions

### Option 1: Vercel Analytics (Recommended)

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />  {/* Core Web Vitals */}
        <SpeedInsights />  {/* Real-time insights */}
      </body>
    </html>
  )
}
```

**Features**:
- Automatic INP tracking (web-vitals v4+)
- Geographic breakdown
- Device type segmentation
- Free tier: 100k events/month

---

### Option 2: Custom web-vitals Integration

```typescript
// lib/web-vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals'

function sendToAnalytics(metric) {
  // Send to your analytics endpoint
  fetch('/api/web-vitals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: metric.name,
      value: metric.value,
      rating: metric.rating,  // 'good', 'needs-improvement', 'poor'
      navigationType: metric.navigationType,
      url: window.location.href,
      userAgent: navigator.userAgent,
    }),
  })
}

// Track all Core Web Vitals
onCLS(sendToAnalytics)
onINP(sendToAnalytics)  // RT-019: INP tracking
onLCP(sendToAnalytics)
onFCP(sendToAnalytics)
onTTFB(sendToAnalytics)
```

**RT-019 Requirement**: Use `web-vitals` v4.2.4+ for INP support (INP added in v4.0.0).

---

### RT-019 Updated Alert Thresholds

| Metric | Warning (P75) | Critical (P90) | RT-019 Target | Business Impact |
|--------|---------------|----------------|---------------|-----------------|
| **INP** | >200ms | >500ms | ≤200ms | -35% bounce rate (Good) |
| **LCP** | >2.5s | >4.0s | ≤2.5s | +25% conversion (Good) |
| **CLS** | >0.1 | >0.25 | ≤0.1 | +30% revenue (Good) |
| **Bundle Size** | >300KB | >500KB | ≤300KB | +15% mobile engagement |

**RT-019 Change**: Bundle size threshold reduced from 750KB → 300KB (initial load).

---

### Example Alert Logic (RT-019 INP Priority)

```typescript
// app/api/web-vitals/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const metric = await request.json()

  // Store in database
  await db.webVitals.create({ data: metric })

  // RT-019: Alert on INP threshold (highest priority)
  if (metric.name === 'INP' && metric.value > 200) {
    await sendSlackAlert({
      text: `⚠️ INP threshold exceeded`,
      fields: [
        { title: 'INP', value: `${metric.value}ms (target: ≤200ms)` },
        { title: 'URL', value: metric.url },
        { title: 'Rating', value: metric.rating },
        { title: 'Interaction', value: metric.attribution?.interactionType },
      ],
    })
  }

  // Alert on LCP threshold (secondary priority)
  if (metric.name === 'LCP' && metric.value > 2500) {
    await sendSlackAlert({ text: `⚠️ LCP threshold exceeded: ${metric.value}ms` })
  }

  // Alert on bundle size (tertiary priority)
  if (metric.name === 'bundle-size' && metric.value > 307200) {  // 300KB
    await sendSlackAlert({ text: `⚠️ Bundle exceeds 300KB: ${metric.value} bytes` })
  }

  return NextResponse.json({ success: true })
}
```

**RT-019 Priority Order**: INP → LCP → CLS → Bundle Size

---

### Performance Monitoring Dashboard

```sql
-- Query 75th percentile INP (RT-019 target metric)
SELECT
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) AS p75_inp,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY value) AS p90_inp,
  COUNT(*) AS sample_size
FROM web_vitals
WHERE name = 'INP'
  AND timestamp > NOW() - INTERVAL '7 days'
```

**RT-019 Recommendation**: Track 75th percentile (not average) for all Core Web Vitals.

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
