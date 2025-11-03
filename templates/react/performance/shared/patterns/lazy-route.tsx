/**
 * Route-Based Code Splitting Pattern
 *
 * SAP-025: React Performance Optimization
 *
 * This pattern demonstrates route-based code splitting using React.lazy and Suspense.
 * Each route is loaded on-demand, reducing the initial bundle size.
 *
 * Benefits:
 * - Smaller initial bundle (faster FCP and LCP)
 * - Routes loaded only when needed
 * - Automatic code splitting by Vite/Next.js
 *
 * @see https://react.dev/reference/react/lazy
 */

import { lazy, Suspense } from 'react'

// ============================================
// LAZY ROUTE IMPORTS
// ============================================

/**
 * Lazy load route components
 *
 * React.lazy takes a function that returns a dynamic import.
 * The component is only loaded when first rendered.
 */
const HomePage = lazy(() => import('@/pages/home'))
const DashboardPage = lazy(() => import('@/pages/dashboard'))
const ProfilePage = lazy(() => import('@/pages/profile'))
const SettingsPage = lazy(() => import('@/pages/settings'))
const NotFoundPage = lazy(() => import('@/pages/not-found'))

// ============================================
// LOADING FALLBACK
// ============================================

/**
 * Loading fallback component
 *
 * Shown while the route component is loading.
 * Keep it lightweight to avoid delaying render.
 */
function RouteLoadingFallback() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        {/* Spinner */}
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
        {/* Loading text */}
        <p className="text-sm text-gray-600">Loading page...</p>
      </div>
    </div>
  )
}

// ============================================
// ROUTE WRAPPER COMPONENT
// ============================================

/**
 * Route wrapper with Suspense boundary
 *
 * This component wraps each lazy route with a Suspense boundary.
 * The fallback is shown while the route component loads.
 *
 * @param Component - The lazy-loaded route component
 * @returns Wrapped component with Suspense boundary
 */
function LazyRoute({ Component }: { Component: React.LazyExoticComponent<any> }) {
  return (
    <Suspense fallback={<RouteLoadingFallback />}>
      <Component />
    </Suspense>
  )
}

// ============================================
// ROUTE EXPORTS
// ============================================

/**
 * Export wrapped route components
 *
 * Use these in your router configuration (React Router, TanStack Router, etc.)
 */
export function HomeRoute() {
  return <LazyRoute Component={HomePage} />
}

export function DashboardRoute() {
  return <LazyRoute Component={DashboardPage} />
}

export function ProfileRoute() {
  return <LazyRoute Component={ProfilePage} />
}

export function SettingsRoute() {
  return <LazyRoute Component={SettingsPage} />
}

export function NotFoundRoute() {
  return <LazyRoute Component={NotFoundPage} />
}

// ============================================
// USAGE WITH REACT ROUTER
// ============================================

/**
 * Example: React Router configuration
 *
 * @example
 * import { createBrowserRouter, RouterProvider } from 'react-router-dom'
 * import { HomeRoute, DashboardRoute, ProfileRoute } from './patterns/lazy-route'
 *
 * const router = createBrowserRouter([
 *   {
 *     path: '/',
 *     element: <HomeRoute />,
 *   },
 *   {
 *     path: '/dashboard',
 *     element: <DashboardRoute />,
 *   },
 *   {
 *     path: '/profile',
 *     element: <ProfileRoute />,
 *   },
 * ])
 *
 * function App() {
 *   return <RouterProvider router={router} />
 * }
 */

// ============================================
// USAGE WITH TANSTACK ROUTER
// ============================================

/**
 * Example: TanStack Router configuration
 *
 * @example
 * import { createRoute, createRouter } from '@tanstack/react-router'
 * import { lazy } from 'react'
 *
 * const HomeRoute = createRoute({
 *   getParentRoute: () => rootRoute,
 *   path: '/',
 *   component: lazy(() => import('@/pages/home')),
 * })
 *
 * const router = createRouter({
 *   routeTree: rootRoute.addChildren([HomeRoute]),
 * })
 */

// ============================================
// USAGE WITH NEXT.JS APP ROUTER
// ============================================

/**
 * Example: Next.js App Router
 *
 * Next.js automatically code-splits routes in the app directory.
 * No need for React.lazy - just create page.tsx files.
 *
 * @example
 * // app/page.tsx (home page)
 * export default function HomePage() {
 *   return <div>Home</div>
 * }
 *
 * // app/dashboard/page.tsx (dashboard page)
 * export default function DashboardPage() {
 *   return <div>Dashboard</div>
 * }
 */

// ============================================
// ADVANCED: PRELOADING ROUTES
// ============================================

/**
 * Preload a route before navigation
 *
 * This improves perceived performance by loading routes
 * before the user clicks a link.
 *
 * @example
 * import { preloadRoute } from './patterns/lazy-route'
 *
 * // Preload dashboard route on hover
 * <Link
 *   to="/dashboard"
 *   onMouseEnter={() => preloadRoute(() => import('@/pages/dashboard'))}
 * >
 *   Dashboard
 * </Link>
 */
export function preloadRoute(
  importFunc: () => Promise<{ default: React.ComponentType<any> }>
) {
  importFunc()
}

// ============================================
// ADVANCED: ERROR BOUNDARY FOR ROUTES
// ============================================

/**
 * Error boundary for lazy routes
 *
 * Catches errors during route loading (e.g., network failures).
 *
 * @example
 * import { RouteErrorBoundary } from './patterns/lazy-route'
 *
 * function App() {
 *   return (
 *     <RouteErrorBoundary>
 *       <RouterProvider router={router} />
 *     </RouteErrorBoundary>
 *   )
 * }
 */
import { Component, ErrorInfo, ReactNode } from 'react'

interface RouteErrorBoundaryProps {
  children: ReactNode
}

interface RouteErrorBoundaryState {
  hasError: boolean
  error?: Error
}

export class RouteErrorBoundary extends Component<
  RouteErrorBoundaryProps,
  RouteErrorBoundaryState
> {
  constructor(props: RouteErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): RouteErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Route loading error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center">
          <div className="max-w-md rounded-lg border border-red-200 bg-red-50 p-6">
            <h2 className="mb-2 text-lg font-semibold text-red-900">
              Failed to load page
            </h2>
            <p className="mb-4 text-sm text-red-700">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="rounded bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
            >
              Reload page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
