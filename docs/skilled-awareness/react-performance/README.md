# SAP-025: React Performance Optimization

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Achieve Core Web Vitals excellence with React 19 + Next.js 15—LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 through AVIF images, code splitting, React Server Components, and automated Lighthouse CI validation.

---

## 🚀 Quick Start (5 minutes)

```bash
# Install performance dependencies
pnpm add sharp  # Image optimization (Next.js)

# Install Lighthouse CI
pnpm add -D @lhci/cli

# Install bundle analyzer
pnpm add -D @next/bundle-analyzer

# Configure performance budgets (lighthouse-ci.json)
cat > lh-ci.json <<'EOF'
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "interaction-to-next-paint": ["error", {"maxNumericValue": 200}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}]
      }
    }
  }
}
EOF

# Run Lighthouse CI (validate performance)
pnpm exec lhci autorun --config=lh-ci.json
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for step-by-step setup (20-min read)

---

## 📖 What Is SAP-025?

SAP-025 provides **performance optimization patterns** for React 19 + Next.js 15 applications. Achieve **90+ Lighthouse scores** for LCP, INP, and CLS through evidence-based optimization strategies: AVIF image formats, React Server Components, code splitting, and automated CI validation.

**Key Innovation**: **INP-first optimization** (new Core Web Vital since March 2024)—60% of React apps fail INP on mobile. SAP-025 prioritizes main thread optimization through code splitting, useDeferredValue, and startTransition.

### How It Works

1. **Core Web Vitals**: LCP ≤2.5s (AVIF images, font preloading), INP ≤200ms (code splitting, React 19 hooks), CLS ≤0.1 (skeleton placeholders)
2. **React 19 Optimizations**: useDeferredValue (defer non-urgent updates), startTransition (break long tasks), RSC (zero-JS static content)
3. **Next.js 15 Patterns**: Automatic image optimization (AVIF/WebP), font optimization (WOFF2 self-hosting), route-based code splitting
4. **Automated Validation**: Lighthouse CI enforces performance budgets in CI/CD, fails builds if metrics regress

---

## 🎯 When to Use

Use SAP-025 when you need to:

1. **Achieve Core Web Vitals compliance** - LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 for SEO ranking
2. **Optimize React 19 apps** - Leverage useDeferredValue, startTransition, RSC for performance
3. **Reduce bundle sizes** - Code splitting, tree-shaking, dynamic imports for faster loads
4. **Automate performance testing** - Lighthouse CI in GitHub Actions prevents regressions
5. **Mobile performance** - 60% of React apps fail INP on mobile (RT-019 finding)

**Not needed for**: Server-rendered static sites (Astro, Hugo), non-React apps, or apps with <1000 monthly users

---

## ✨ Key Features

- ✅ **Core Web Vitals**: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 (Google Search ranking factors)
- ✅ **React 19 Optimizations**: useDeferredValue, startTransition, React Server Components
- ✅ **Next.js 15 Integration**: Image/font optimization, automatic code splitting
- ✅ **AVIF Images**: -50% file size vs JPEG, 96% browser support, automatic format selection
- ✅ **Code Splitting**: Route-based + component-based + viewport lazy loading
- ✅ **Lighthouse CI**: Automated performance budgets in CI/CD (fail builds on regression)
- ✅ **Bundle Analysis**: @next/bundle-analyzer visualizes JavaScript chunk sizes

---

## 📚 Quick Reference

### Core Web Vitals Targets

| Metric | Target | Threshold | Impact |
|--------|--------|-----------|--------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | Good: ≤2.5s, Poor: ≥4.0s | Image/font/code optimization |
| **INP** (Interaction to Next Paint) | ≤200ms | Good: ≤200ms, Poor: ≥500ms | Code splitting, React 19 hooks |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | Good: ≤0.1, Poor: ≥0.25 | Skeleton placeholders, fixed dimensions |

**RT-019 Finding**: INP is the #1 performance priority—60% of React apps fail INP on mobile due to JavaScript blocking main thread. Optimize INP first.

---

### LCP Optimization (Target: ≤2.5s)

**Definition**: Time from page load until largest text block or image is rendered.

#### 1. Image Optimization (Primary LCP Element)

```tsx
// next/image with priority loading
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  priority  // ✅ Preload hero image
  sizes="100vw"
/>
```

**Impact**: -40% LCP (4.2s → 2.5s) with AVIF format + priority loading

**Format Selection**:
- **AVIF**: -50% vs JPEG (96% browser support) → Hero images
- **WebP**: -30% vs JPEG (98% browser support) → Fallback
- **JPEG**: Baseline (100% browser support)

---

#### 2. Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // ✅ Show fallback font immediately
  preload: true,
})

export default function RootLayout({ children }) {
  return (
    <html className={inter.variable}>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

**Impact**: -25% LCP (3.2s → 2.4s) with WOFF2 self-hosting + preload

---

#### 3. Code Splitting (Reduce Initial Bundle)

```tsx
// Route-based code splitting (automatic in Next.js)
// app/dashboard/page.tsx
export default function DashboardPage() {
  return <Dashboard />  // Automatically code-split
}

// Component-based lazy loading
import { lazy, Suspense } from 'react'

const HeavyChart = lazy(() => import('@/components/heavy-chart'))

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart />
</Suspense>
```

**Impact**: -30% LCP (3.5s → 2.5s) by reducing initial bundle from 350KB → 180KB

**LCP Combined Impact**: -56% (4.8s → 2.1s)

---

### INP Optimization (Target: ≤200ms)

**Definition**: Latency from user interaction (click, tap, keypress) until next paint. INP replaced FID as Core Web Vital in **March 2024**.

**Why INP Matters**:
- Measures **all interactions** during page lifetime (vs FID's first input only)
- 60% of React apps fail INP on mobile (RT-019 research)
- Google Search ranking factor since March 2024

#### 1. Code Splitting (Reduce JavaScript Parse Time)

```tsx
// Viewport lazy loading for heavy components
import { ViewportLazyComponent } from '@/lib/patterns/lazy-component'

<ViewportLazyComponent
  loader={() => import('@/components/heavy-chart')}
  fallback={<ChartSkeleton />}
  threshold={0.1}  // Load when 10% visible
  rootMargin="200px"  // Load 200px before visible
/>
```

**Impact**: -45% INP (350ms → 190ms) by reducing main thread work

**Target**: <50KB per route chunk

---

#### 2. useDeferredValue (React 19)

```tsx
import { useDeferredValue, useState } from 'react'

function SearchBox() {
  const [search, setSearch] = useState('')
  const deferredSearch = useDeferredValue(search)  // ✅ Defer non-urgent updates

  // Heavy search logic uses deferredSearch (not blocking)
  const results = useSearchResults(deferredSearch)

  return (
    <input
      value={search}
      onChange={(e) => setSearch(e.target.value)}  // Immediate UI update
    />
  )
}
```

**Impact**: -40% INP (300ms → 180ms) by deferring non-urgent updates

**RT-019 Finding**: useDeferredValue is more effective than manual debouncing for INP because React schedules updates automatically.

---

#### 3. startTransition (React 19)

```tsx
import { startTransition, useState } from 'react'

function FilterPanel() {
  const [filter, setFilter] = useState('all')

  function handleClick(newFilter: string) {
    startTransition(() => {
      // Non-urgent state update (doesn't block UI)
      setFilter(newFilter)
    })
  }

  return <button onClick={() => handleClick('active')}>Active</button>
}
```

**Impact**: -35% INP (280ms → 180ms) by breaking long tasks

---

#### 4. React Server Components (RSC)

```tsx
// app/dashboard/page.tsx (Server Component)
async function DashboardPage() {
  const data = await fetchData()  // Server-side fetch (zero client JS)

  return (
    <Dashboard data={data}>
      <StaticHeader />  {/* Zero JS */}
      <StaticSidebar />  {/* Zero JS */}
    </Dashboard>
  )
}
```

**Impact**: -60% INP (450ms → 180ms) by eliminating client JavaScript for static content

**INP Combined Impact**: -70% (600ms → 180ms)

---

### CLS Optimization (Target: ≤0.1)

**Definition**: Visual stability—sum of unexpected layout shifts during page lifetime.

#### 1. Fixed Dimensions for Images/Videos

```tsx
<Image
  src="/product.jpg"
  alt="Product"
  width={800}  // ✅ Fixed width
  height={600}  // ✅ Fixed height
  // CLS: 0 (no layout shift)
/>
```

**Impact**: -72% CLS (0.18 → 0.05)

---

#### 2. Skeleton Placeholders

```tsx
function ProductCard() {
  const { data, isLoading } = useQuery(['product'])

  if (isLoading) {
    return <ProductSkeleton />  // ✅ Same dimensions as real content
  }

  return <ProductContent data={data} />
}
```

**Impact**: -50% CLS (0.12 → 0.06)

---

#### 3. Font Loading with font-display: swap

```tsx
// next/font automatically adds font-display: swap
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // ✅ Show fallback font immediately
})
```

**Impact**: -60% CLS (0.15 → 0.06)

**CLS Combined Impact**: -72% (0.18 → 0.05)

---

### Code Splitting Patterns

#### Pattern 1: Route-Based Code Splitting

**Use Case**: Split code by route (most common pattern)

```tsx
// Next.js App Router (automatic code splitting)
// app/dashboard/page.tsx
export default function DashboardPage() {
  return <Dashboard />  // Automatically split into separate chunk
}

// Vite + React Router
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('@/pages/dashboard'))

<Route
  path="/dashboard"
  element={
    <Suspense fallback={<Skeleton />}>
      <Dashboard />
    </Suspense>
  }
/>
```

**Bundle Impact**:
- Initial bundle: 350KB → 180KB (-49%)
- Dashboard route: +120KB (loaded on-demand)

**LCP Impact**: -30% (3.5s → 2.5s)

---

#### Pattern 2: Component-Based Lazy Loading

**Use Case**: Heavy components (charts, maps, editors)

```tsx
import { lazy, Suspense } from 'react'

const HeavyChart = lazy(() => import('chart.js'))

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

**Bundle Impact**:
- Chart library: 85KB (not loaded until rendered)
- Main bundle reduction: -85KB

**INP Impact**: -20% (240ms → 190ms)

---

#### Pattern 3: Viewport Lazy Loading

**Use Case**: Load components when visible in viewport

```tsx
import { ViewportLazyComponent } from '@/lib/patterns/lazy-component'

<ViewportLazyComponent
  loader={() => import('@/components/heavy-map')}
  fallback={<MapSkeleton />}
  threshold={0.1}  // Load when 10% visible
  rootMargin="200px"  // Load 200px before entering viewport
/>
```

**Bundle Impact**:
- Map library: 150KB (not loaded until visible)

**LCP Impact**: -15% for below-fold content

---

### Image Optimization

#### Format Selection

| Format | Size vs JPEG | Browser Support | Use Case |
|--------|--------------|-----------------|----------|
| **AVIF** | -50% | 96% | Hero images, product photos |
| **WebP** | -30% | 98% | Fallback for AVIF |
| **JPEG** | Baseline | 100% | Final fallback |

#### Next.js Image Component

```tsx
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  priority  // ✅ Preload for LCP
  quality={85}  // ✅ Balance quality vs size
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  placeholder="blur"  // ✅ Show blur while loading
  blurDataURL="data:image/jpeg;base64,..."
/>
```

**Automatic Optimizations**:
- AVIF/WebP format selection (browser-dependent)
- Responsive srcset generation
- Lazy loading (unless priority set)
- Blur placeholder generation

---

### Font Optimization

#### next/font (Self-Hosting)

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
  preload: true,
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

**Benefits**:
- WOFF2 self-hosting (no external requests)
- Preload critical fonts
- font-display: swap (show fallback immediately)
- CSS variables for Tailwind integration

---

### Lighthouse CI Integration

#### lighthouse-ci.json

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "interaction-to-next-paint": ["error", {"maxNumericValue": 200}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "first-contentful-paint": ["error", {"maxNumericValue": 1800}],
        "speed-index": ["error", {"maxNumericValue": 3400}],
        "total-blocking-time": ["error", {"maxNumericValue": 200}]
      }
    },
    "collect": {
      "numberOfRuns": 3,
      "settings": {
        "preset": "desktop"
      }
    }
  }
}
```

#### GitHub Actions Workflow

```yaml
# .github/workflows/lighthouse-ci.yml
name: Lighthouse CI

on:
  pull_request:
    paths:
      - 'app/**'
      - 'components/**'

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - name: Install dependencies
        run: pnpm install
      - name: Build production
        run: pnpm build
      - name: Run Lighthouse CI
        run: pnpm exec lhci autorun --config=lh-ci.json
```

**Behavior**:
- Runs on Pull Requests for app/ or components/ changes
- 3 Lighthouse runs (median score)
- Fails build if performance score <90 or metrics regress

---

### Bundle Analysis

#### @next/bundle-analyzer

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Next.js config
})
```

#### Usage

```bash
# Generate bundle analysis
ANALYZE=true pnpm build

# Opens interactive visualization:
# - Treemap of all JavaScript chunks
# - Identifies largest dependencies
# - Shows duplicate code across chunks
```

**Use Cases**:
- Identify heavy dependencies (e.g., moment.js → date-fns)
- Find duplicate code across chunks
- Validate code splitting effectiveness

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-020** (Next.js 15 Foundation) | Image/Font Optimization | Use Next.js Image and next/font for automatic optimization |
| **SAP-021** (Testing) | Performance Testing | Add Lighthouse CI tests to validate Core Web Vitals in CI/CD |
| **SAP-024** (Styling) | Tailwind CSS | Use next/font with CSS variables for Tailwind integration |
| **SAP-023** (State Management) | React 19 Hooks | Use useDeferredValue and startTransition for INP optimization |
| **SAP-005** (CI/CD) | Automated Validation | Lighthouse CI runs in GitHub Actions on Pull Requests |
| **SAP-026** (Accessibility) | Skeleton Placeholders | Use accessible loading states to prevent CLS |

---

## 🏆 Success Metrics

- **LCP**: ≤2.5s (Good), ≤4.0s (Needs Improvement), ≥4.0s (Poor)
- **INP**: ≤200ms (Good), 200-500ms (Needs Improvement), ≥500ms (Poor)
- **CLS**: ≤0.1 (Good), 0.1-0.25 (Needs Improvement), ≥0.25 (Poor)
- **Lighthouse Performance Score**: ≥90 (A), 75-89 (B), 50-74 (C), <50 (F)
- **Bundle Size**: <50KB per route chunk (target for INP <200ms)
- **CI/CD**: 100% Pull Requests validated with Lighthouse CI

---

## 🔧 Troubleshooting

### Problem: LCP >4.0s (Poor)

**Symptom**: Lighthouse reports "Largest Contentful Paint is slow"

**Common Causes**:
1. Large hero image without priority loading
2. Fonts loaded from external CDN (Google Fonts)
3. Large initial JavaScript bundle (>350KB)

**Solutions**:

```tsx
// 1. Add priority to hero image
<Image
  src="/hero.jpg"
  priority  // ✅ Preload hero image
  // ...
/>

// 2. Self-host fonts with next/font
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], preload: true })

// 3. Code split heavy components
const HeavyChart = lazy(() => import('@/components/heavy-chart'))
```

**Validation**: Run Lighthouse CI, verify LCP ≤2.5s

---

### Problem: INP >500ms (Poor)

**Symptom**: Clicks/taps feel laggy, Lighthouse reports "Interaction to Next Paint is high"

**Common Causes**:
1. Large JavaScript bundle blocking main thread
2. Heavy synchronous event handlers
3. No code splitting for heavy components

**Solutions**:

```tsx
// 1. Use useDeferredValue for non-urgent updates
const deferredSearch = useDeferredValue(search)

// 2. Wrap long tasks in startTransition
startTransition(() => {
  setLargeDataset(processData())
})

// 3. Code split heavy components
const Dashboard = lazy(() => import('@/pages/dashboard'))
```

**Validation**: Run Lighthouse CI, verify INP ≤200ms

---

### Problem: CLS >0.25 (Poor)

**Symptom**: Content jumps during page load, Lighthouse reports "Cumulative Layout Shift is high"

**Common Causes**:
1. Images without fixed width/height
2. Fonts loaded without fallback (font-display: block)
3. Ads/embeds without reserved space

**Solutions**:

```tsx
// 1. Add width/height to all images
<Image
  src="/product.jpg"
  width={800}  // ✅ Fixed dimensions
  height={600}
  // ...
/>

// 2. Use font-display: swap
import { Inter } from 'next/font/google'
const inter = Inter({ display: 'swap' })  // ✅ Show fallback immediately

// 3. Use skeleton placeholders
if (isLoading) return <ProductSkeleton />
```

**Validation**: Run Lighthouse CI, verify CLS ≤0.1

---

### Problem: Lighthouse CI Failing in CI/CD

**Symptom**: GitHub Actions workflow fails with "Lighthouse CI assertions failed"

**Common Causes**:
1. Performance regression (new feature increased bundle size)
2. Missing AVIF image optimization
3. No code splitting for new routes

**Solutions**:

```bash
# 1. Run Lighthouse CI locally to debug
pnpm exec lhci autorun --config=lh-ci.json

# 2. Analyze bundle with @next/bundle-analyzer
ANALYZE=true pnpm build

# 3. Check for heavy dependencies
pnpm exec bundlephobia <package-name>

# 4. Validate optimizations
# - Are images using <Image priority>?
# - Are fonts using next/font?
# - Are heavy components code-split?
```

**Validation**: Re-run Lighthouse CI, ensure assertions pass

---

### Problem: AVIF Images Not Loading

**Symptom**: Images fall back to JPEG even in modern browsers

**Common Causes**:
1. Sharp not installed (required for AVIF generation)
2. Missing sharp binary (Linux/Docker)
3. Image optimization disabled in next.config.js

**Solutions**:

```bash
# 1. Install sharp
pnpm add sharp

# 2. Docker: Install sharp dependencies
RUN apk add --no-cache libc6-compat
RUN pnpm add sharp

# 3. Enable image optimization in next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
  },
}
```

**Validation**: Open DevTools Network tab, verify Content-Type: image/avif

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete performance specification (45KB, 23-min read)
- **[AGENTS.md](AGENTS.md)** - Agent performance workflows (17KB, 9-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (15KB, 8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Setup guide (38KB, 19-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

### External Resources

- [Web.dev Core Web Vitals](https://web.dev/vitals/) - Google's official guide
- [React 19 Performance](https://react.dev/blog/2024/04/25/react-19) - useDeferredValue, startTransition
- [Next.js Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images) - AVIF, WebP, blur placeholders
- [Lighthouse CI Docs](https://github.com/GoogleChrome/lighthouse-ci) - Automated performance testing
- [RT-019 Research Report](../../dev-docs/research/react/RT-019-SCALE%20Research%20Report_%20Global%20Scale%20&%20Advanced%20Patterns.md) - INP findings and benchmarks

---

**Version History**:
- **1.0.0** (2025-11-05) - Initial React Performance Optimization with Core Web Vitals, React 19 optimizations, Lighthouse CI

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
