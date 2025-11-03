/**
 * Component-Based Code Splitting Pattern
 *
 * SAP-025: React Performance Optimization
 *
 * This pattern demonstrates component-based code splitting for heavy components.
 * Components are loaded on-demand, often combined with viewport-based loading.
 *
 * Use cases:
 * - Heavy charting libraries (e.g., Chart.js, Recharts)
 * - Rich text editors (e.g., TipTap, Quill)
 * - Maps (e.g., Mapbox, Google Maps)
 * - Code editors (e.g., Monaco, CodeMirror)
 * - Video players (e.g., Video.js, Plyr)
 *
 * Benefits:
 * - Smaller initial bundle (faster FCP and LCP)
 * - Components loaded only when needed
 * - Improved INP (less JavaScript to parse)
 *
 * @see https://react.dev/reference/react/lazy
 */

import { lazy, Suspense, useEffect, useRef, useState } from 'react'

// ============================================
// LAZY COMPONENT IMPORTS
// ============================================

/**
 * Lazy load heavy components
 *
 * These components are only loaded when rendered.
 */
const HeavyChart = lazy(() => import('@/components/heavy-chart'))
const RichTextEditor = lazy(() => import('@/components/rich-text-editor'))
const MapView = lazy(() => import('@/components/map-view'))
const CodeEditor = lazy(() => import('@/components/code-editor'))
const VideoPlayer = lazy(() => import('@/components/video-player'))

// ============================================
// SIMPLE LAZY COMPONENT
// ============================================

/**
 * Simple lazy component wrapper
 *
 * This is the most basic pattern - lazy load a component with Suspense.
 *
 * @example
 * <ChartSection />
 */
export function ChartSection() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart data={[1, 2, 3, 4, 5]} />
    </Suspense>
  )
}

/**
 * Skeleton loading component for charts
 */
function ChartSkeleton() {
  return (
    <div className="h-64 w-full animate-pulse rounded-lg bg-gray-200">
      <div className="flex h-full items-center justify-center">
        <p className="text-sm text-gray-500">Loading chart...</p>
      </div>
    </div>
  )
}

// ============================================
// VIEWPORT-BASED LAZY LOADING
// ============================================

/**
 * Lazy load component when it enters the viewport
 *
 * This pattern uses IntersectionObserver to load the component
 * only when it's about to become visible.
 *
 * Benefits:
 * - Component not loaded if user never scrolls to it
 * - Reduces initial bundle size
 * - Improves LCP for above-the-fold content
 *
 * @example
 * <ViewportLazyComponent
 *   loader={() => import('@/components/heavy-chart')}
 *   fallback={<ChartSkeleton />}
 *   threshold={0.1}
 * />
 */
interface ViewportLazyComponentProps {
  loader: () => Promise<{ default: React.ComponentType<any> }>
  fallback?: React.ReactNode
  threshold?: number
  rootMargin?: string
  componentProps?: any
}

export function ViewportLazyComponent({
  loader,
  fallback = <div>Loading...</div>,
  threshold = 0.1,
  rootMargin = '200px',
  componentProps = {},
}: ViewportLazyComponentProps) {
  const [isVisible, setIsVisible] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const LazyComponent = lazy(loader)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          // Disconnect after first intersection (component loaded once)
          observer.disconnect()
        }
      },
      {
        threshold,
        rootMargin,
      }
    )

    if (containerRef.current) {
      observer.observe(containerRef.current)
    }

    return () => observer.disconnect()
  }, [threshold, rootMargin])

  return (
    <div ref={containerRef}>
      {isVisible ? (
        <Suspense fallback={fallback}>
          <LazyComponent {...componentProps} />
        </Suspense>
      ) : (
        fallback
      )}
    </div>
  )
}

// ============================================
// INTERACTION-BASED LAZY LOADING
// ============================================

/**
 * Lazy load component on user interaction (click, hover)
 *
 * This pattern loads the component only when the user interacts with a trigger.
 * Common for modals, tooltips, and popovers.
 *
 * @example
 * <InteractionLazyComponent
 *   trigger="click"
 *   loader={() => import('@/components/modal')}
 *   triggerElement={<button>Open Modal</button>}
 * />
 */
interface InteractionLazyComponentProps {
  loader: () => Promise<{ default: React.ComponentType<any> }>
  trigger: 'click' | 'hover'
  triggerElement: React.ReactNode
  fallback?: React.ReactNode
  componentProps?: any
}

export function InteractionLazyComponent({
  loader,
  trigger,
  triggerElement,
  fallback = <div>Loading...</div>,
  componentProps = {},
}: InteractionLazyComponentProps) {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isPreloaded, setIsPreloaded] = useState(false)
  const LazyComponent = lazy(loader)

  const handleTrigger = () => {
    setIsLoaded(true)
  }

  const handlePreload = () => {
    if (!isPreloaded) {
      // Preload component on hover (before click)
      loader()
      setIsPreloaded(true)
    }
  }

  return (
    <>
      <div
        onClick={trigger === 'click' ? handleTrigger : undefined}
        onMouseEnter={trigger === 'hover' ? handlePreload : undefined}
      >
        {triggerElement}
      </div>

      {isLoaded && (
        <Suspense fallback={fallback}>
          <LazyComponent {...componentProps} />
        </Suspense>
      )}
    </>
  )
}

// ============================================
// USAGE EXAMPLES
// ============================================

/**
 * Example 1: Heavy chart with viewport loading
 */
export function DashboardCharts() {
  return (
    <div className="space-y-8">
      {/* First chart (above fold) - load immediately */}
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={[1, 2, 3]} />
      </Suspense>

      {/* Second chart (below fold) - load when visible */}
      <ViewportLazyComponent
        loader={() => import('@/components/heavy-chart')}
        fallback={<ChartSkeleton />}
        threshold={0.1}
        rootMargin="200px"
        componentProps={{ data: [4, 5, 6] }}
      />
    </div>
  )
}

/**
 * Example 2: Rich text editor with interaction loading
 */
export function BlogPostEditor() {
  return (
    <InteractionLazyComponent
      loader={() => import('@/components/rich-text-editor')}
      trigger="click"
      triggerElement={
        <button className="rounded bg-blue-600 px-4 py-2 text-white">
          Open Editor
        </button>
      }
      fallback={<div>Loading editor...</div>}
      componentProps={{ placeholder: 'Start writing...' }}
    />
  )
}

/**
 * Example 3: Map with viewport loading
 */
export function LocationSection() {
  return (
    <ViewportLazyComponent
      loader={() => import('@/components/map-view')}
      fallback={
        <div className="h-96 w-full animate-pulse rounded-lg bg-gray-200">
          <div className="flex h-full items-center justify-center">
            <p className="text-sm text-gray-500">Loading map...</p>
          </div>
        </div>
      }
      threshold={0.1}
      rootMargin="400px"
      componentProps={{
        center: { lat: 37.7749, lng: -122.4194 },
        zoom: 12,
      }}
    />
  )
}

// ============================================
// ADVANCED: RETRY ON ERROR
// ============================================

/**
 * Lazy component with retry on error
 *
 * If the component fails to load (e.g., network error),
 * this provides a retry button.
 */
interface LazyComponentWithRetryProps {
  loader: () => Promise<{ default: React.ComponentType<any> }>
  fallback?: React.ReactNode
  componentProps?: any
}

export function LazyComponentWithRetry({
  loader,
  fallback = <div>Loading...</div>,
  componentProps = {},
}: LazyComponentWithRetryProps) {
  const [hasError, setHasError] = useState(false)
  const [retryKey, setRetryKey] = useState(0)

  const LazyComponent = lazy(loader)

  const handleRetry = () => {
    setHasError(false)
    setRetryKey((prev) => prev + 1)
  }

  if (hasError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4">
        <p className="mb-2 text-sm text-red-700">Failed to load component</p>
        <button
          onClick={handleRetry}
          className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <Suspense fallback={fallback} key={retryKey}>
      <LazyComponent {...componentProps} />
    </Suspense>
  )
}

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Load critical components immediately (above-the-fold)
 * 2. Use viewport loading for below-the-fold heavy components
 * 3. Use interaction loading for modals, tooltips, popovers
 * 4. Preload components on hover (before click) for better UX
 * 5. Set rootMargin="200px" to load before component enters viewport
 * 6. Use lightweight fallback components (avoid heavy skeletons)
 * 7. Consider component size before lazy loading (>50KB = good candidate)
 * 8. Test on slow 3G network to verify loading experience
 *
 * CORE WEB VITALS IMPACT:
 * - LCP: Reduces initial bundle → faster LCP for hero content
 * - INP: Less JavaScript to parse → faster interactions
 * - CLS: Use fixed-size skeleton fallbacks → prevent layout shift
 */
