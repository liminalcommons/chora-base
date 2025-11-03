/**
 * Suspense Boundary Pattern
 *
 * SAP-025: React Performance Optimization
 *
 * This pattern provides reusable Suspense boundaries with:
 * - Customizable fallback components
 * - Error boundaries
 * - Loading states
 * - Retry logic
 *
 * Benefits:
 * - Consistent loading UX across the app
 * - Graceful error handling
 * - Reduced boilerplate (DRY principle)
 *
 * @see https://react.dev/reference/react/Suspense
 */

import { Suspense, Component, ErrorInfo, ReactNode } from 'react'

// ============================================
// BASIC SUSPENSE BOUNDARY
// ============================================

/**
 * Basic Suspense boundary with custom fallback
 *
 * @param children - Child components
 * @param fallback - Loading fallback
 *
 * @example
 * <SuspenseBoundary fallback={<Spinner />}>
 *   <HeavyComponent />
 * </SuspenseBoundary>
 */
interface SuspenseBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

export function SuspenseBoundary({
  children,
  fallback = <DefaultFallback />,
}: SuspenseBoundaryProps) {
  return <Suspense fallback={fallback}>{children}</Suspense>
}

/**
 * Default fallback component (spinner + text)
 */
function DefaultFallback() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="flex flex-col items-center gap-4">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
        <p className="text-sm text-gray-600">Loading...</p>
      </div>
    </div>
  )
}

// ============================================
// SUSPENSE BOUNDARY WITH ERROR BOUNDARY
// ============================================

/**
 * Suspense boundary with error boundary
 *
 * This combines Suspense (for loading) and Error Boundary (for errors).
 * Provides a complete loading + error handling solution.
 *
 * @example
 * <SuspenseWithErrorBoundary
 *   fallback={<Spinner />}
 *   errorFallback={<ErrorMessage />}
 * >
 *   <HeavyComponent />
 * </SuspenseWithErrorBoundary>
 */
interface SuspenseWithErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
  errorFallback?: (error: Error, retry: () => void) => ReactNode
}

export function SuspenseWithErrorBoundary({
  children,
  fallback = <DefaultFallback />,
  errorFallback,
}: SuspenseWithErrorBoundaryProps) {
  return (
    <ErrorBoundary errorFallback={errorFallback}>
      <Suspense fallback={fallback}>{children}</Suspense>
    </ErrorBoundary>
  )
}

// ============================================
// ERROR BOUNDARY
// ============================================

/**
 * Error boundary component
 *
 * Catches errors in child components and displays a fallback UI.
 */
interface ErrorBoundaryProps {
  children: ReactNode
  errorFallback?: (error: Error, retry: () => void) => ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error boundary caught error:', error, errorInfo)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined })
  }

  render() {
    if (this.state.hasError && this.state.error) {
      // Custom error fallback
      if (this.props.errorFallback) {
        return this.props.errorFallback(this.state.error, this.handleRetry)
      }

      // Default error fallback
      return <DefaultErrorFallback error={this.state.error} retry={this.handleRetry} />
    }

    return this.props.children
  }
}

/**
 * Default error fallback component
 */
function DefaultErrorFallback({ error, retry }: { error: Error; retry: () => void }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-6">
      <h2 className="mb-2 text-lg font-semibold text-red-900">Something went wrong</h2>
      <p className="mb-4 text-sm text-red-700">{error.message}</p>
      <button
        onClick={retry}
        className="rounded bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
      >
        Try again
      </button>
    </div>
  )
}

// ============================================
// NESTED SUSPENSE BOUNDARIES
// ============================================

/**
 * Nested Suspense boundaries for progressive loading
 *
 * This pattern loads content progressively (e.g., shell → sidebar → content).
 * Improves perceived performance by showing content as it loads.
 *
 * @example
 * <NestedSuspenseBoundaries
 *   shell={<AppShell />}
 *   sidebar={<Sidebar />}
 *   content={<MainContent />}
 * />
 */
interface NestedSuspenseBoundariesProps {
  shell: ReactNode
  sidebar: ReactNode
  content: ReactNode
}

export function NestedSuspenseBoundaries({
  shell,
  sidebar,
  content,
}: NestedSuspenseBoundariesProps) {
  return (
    <Suspense fallback={<AppShellSkeleton />}>
      {shell}
      <div className="flex">
        <Suspense fallback={<SidebarSkeleton />}>
          {sidebar}
        </Suspense>
        <Suspense fallback={<ContentSkeleton />}>
          {content}
        </Suspense>
      </div>
    </Suspense>
  )
}

function AppShellSkeleton() {
  return <div className="h-16 w-full animate-pulse bg-gray-200" />
}

function SidebarSkeleton() {
  return <div className="h-screen w-64 animate-pulse bg-gray-200" />
}

function ContentSkeleton() {
  return <div className="flex-1 animate-pulse bg-gray-100" />
}

// ============================================
// SUSPENSE LIST (EXPERIMENTAL)
// ============================================

/**
 * Suspense list pattern (coordinate loading order)
 *
 * This pattern coordinates the loading order of multiple Suspense boundaries.
 * Useful for lists, grids, or feeds.
 *
 * Note: SuspenseList is experimental and may change in future React versions.
 *
 * @example
 * <SuspenseList revealOrder="forwards">
 *   <Suspense fallback={<Skeleton />}>
 *     <Item1 />
 *   </Suspense>
 *   <Suspense fallback={<Skeleton />}>
 *     <Item2 />
 *   </Suspense>
 * </SuspenseList>
 */
// Note: SuspenseList is not yet stable in React 19
// Uncomment when stable:
// import { SuspenseList } from 'react'
//
// export { SuspenseList }

// ============================================
// SKELETON FALLBACK COMPONENTS
// ============================================

/**
 * Card skeleton fallback
 */
export function CardSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <div className="space-y-4">
        <div className="h-6 w-3/4 animate-pulse rounded bg-gray-200" />
        <div className="h-4 w-full animate-pulse rounded bg-gray-200" />
        <div className="h-4 w-5/6 animate-pulse rounded bg-gray-200" />
      </div>
    </div>
  )
}

/**
 * Table skeleton fallback
 */
export function TableSkeleton() {
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200">
      <div className="border-b border-gray-200 bg-gray-50 p-4">
        <div className="h-4 w-32 animate-pulse rounded bg-gray-300" />
      </div>
      {[...Array(5)].map((_, i) => (
        <div key={i} className="border-b border-gray-200 p-4 last:border-b-0">
          <div className="h-4 w-full animate-pulse rounded bg-gray-200" />
        </div>
      ))}
    </div>
  )
}

/**
 * Avatar skeleton fallback
 */
export function AvatarSkeleton() {
  return (
    <div className="flex items-center gap-3">
      <div className="h-10 w-10 animate-pulse rounded-full bg-gray-200" />
      <div className="space-y-2">
        <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
        <div className="h-3 w-32 animate-pulse rounded bg-gray-200" />
      </div>
    </div>
  )
}

/**
 * Grid skeleton fallback
 */
export function GridSkeleton({ items = 6 }: { items?: number }) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {[...Array(items)].map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  )
}

// ============================================
// USAGE EXAMPLES
// ============================================

/**
 * Example 1: Basic usage with custom fallback
 */
export function DashboardExample() {
  return (
    <SuspenseBoundary fallback={<GridSkeleton items={6} />}>
      <DashboardContent />
    </SuspenseBoundary>
  )
}

function DashboardContent() {
  return <div>Dashboard content</div>
}

/**
 * Example 2: With error boundary and custom error UI
 */
export function ProfileExample() {
  return (
    <SuspenseWithErrorBoundary
      fallback={<CardSkeleton />}
      errorFallback={(error, retry) => (
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <h2 className="mb-2 text-lg font-semibold text-red-900">
            Failed to load profile
          </h2>
          <p className="mb-4 text-sm text-red-700">{error.message}</p>
          <button
            onClick={retry}
            className="rounded bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700"
          >
            Try again
          </button>
        </div>
      )}
    >
      <ProfileContent />
    </SuspenseWithErrorBoundary>
  )
}

function ProfileContent() {
  return <div>Profile content</div>
}

/**
 * Example 3: Nested boundaries for progressive loading
 */
export function AppExample() {
  return (
    <Suspense fallback={<AppShellSkeleton />}>
      <AppShell>
        <div className="flex">
          <Suspense fallback={<SidebarSkeleton />}>
            <Sidebar />
          </Suspense>
          <main className="flex-1">
            <Suspense fallback={<ContentSkeleton />}>
              <MainContent />
            </Suspense>
          </main>
        </div>
      </AppShell>
    </Suspense>
  )
}

function AppShell({ children }: { children: ReactNode }) {
  return <div>{children}</div>
}

function Sidebar() {
  return <aside className="w-64">Sidebar</aside>
}

function MainContent() {
  return <div>Main content</div>
}

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Use nested Suspense boundaries for progressive loading
 * 2. Place Suspense boundaries close to the lazy component
 * 3. Use lightweight skeleton fallbacks (avoid heavy animations)
 * 4. Match skeleton size to actual content (prevent CLS)
 * 5. Combine Suspense with Error Boundary (complete loading solution)
 * 6. Use SuspenseList for coordinated loading (when stable)
 * 7. Avoid wrapping entire app in one Suspense (bad UX)
 * 8. Test loading states on slow 3G network
 *
 * CORE WEB VITALS IMPACT:
 * - LCP: Progressive loading → faster perceived performance
 * - CLS: Fixed-size skeletons → prevent layout shift
 * - INP: Error boundaries with retry → better error UX
 */
