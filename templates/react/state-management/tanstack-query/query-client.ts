/**
 * TanStack Query Client Configuration
 *
 * SAP-023: React State Management Patterns
 * Template: query-client.ts
 *
 * Purpose:
 * - Configure QueryClient with production-ready defaults
 * - Optimize for Next.js 15 / Vite 7 + React 19
 * - Balance between fresh data and network efficiency
 *
 * Usage:
 * Import this singleton client in app.tsx or layout.tsx
 *
 * @see https://tanstack.com/query/v5/docs/react/reference/QueryClient
 */

import { QueryClient } from '@tanstack/react-query'

/**
 * Create QueryClient singleton
 *
 * Best Practice: Create ONE client for entire app
 * Re-using the same client ensures cache consistency
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      /**
       * staleTime: How long data is considered "fresh"
       *
       * - During this time, no refetch occurs (even on mount)
       * - Balances freshness vs network efficiency
       * - Default: 0 (always stale, refetch every time)
       *
       * Recommendation: 60 seconds (1 minute)
       * - Most data doesn't change every second
       * - Reduces unnecessary network requests
       * - Users won't notice 1-minute staleness
       *
       * Adjust per query if needed:
       * - Real-time data: 0-10 seconds
       * - Static data: 5-10 minutes (300000-600000)
       */
      staleTime: 60 * 1000, // 1 minute

      /**
       * gcTime (garbage collection time): How long inactive data stays in cache
       *
       * - After this time, unused data is removed from memory
       * - Applies to queries with NO active observers
       * - Default: 5 minutes (300000)
       *
       * Recommendation: 5 minutes (keep default)
       * - Good balance between memory usage and cache hits
       * - User navigates back within 5 min → instant load
       */
      gcTime: 5 * 60 * 1000, // 5 minutes

      /**
       * retry: Number of retry attempts for failed requests
       *
       * - Exponential backoff by default (1s, 2s, 4s delays)
       * - Useful for transient network errors
       * - Default: 3
       *
       * Recommendation: 3 retries
       * - Handles temporary network issues
       * - Doesn't retry forever (UX)
       *
       * Set to false for mutations (don't retry POST/PUT/DELETE)
       */
      retry: 3,

      /**
       * retryDelay: Custom retry delay function
       *
       * Default: exponentialBackoff (attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000))
       * - Attempt 1: 1s delay
       * - Attempt 2: 2s delay
       * - Attempt 3: 4s delay
       *
       * Keep default for most cases
       */
      // retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),

      /**
       * refetchOnWindowFocus: Refetch when window regains focus
       *
       * - User switches back to tab → refetch to ensure fresh data
       * - Good for dashboards, admin panels
       * - Default: true
       *
       * Recommendation: true (keep default)
       * - Ensures users see latest data when they return
       * - Respects staleTime (won't refetch if still fresh)
       *
       * Set to false for apps where data rarely changes
       */
      refetchOnWindowFocus: true,

      /**
       * refetchOnReconnect: Refetch when network reconnects
       *
       * - User loses internet → reconnects → refetch
       * - Default: true
       *
       * Recommendation: true (keep default)
       * - Critical for mobile apps (spotty connections)
       */
      refetchOnReconnect: true,

      /**
       * refetchOnMount: Refetch when component mounts
       *
       * - Default: true
       * - Respects staleTime (won't refetch if fresh)
       *
       * Recommendation: true (keep default)
       * - Ensures data is fresh on first mount
       * - staleTime prevents excessive refetching
       */
      refetchOnMount: true,

      /**
       * refetchInterval: Auto-refetch at interval (polling)
       *
       * - Default: false (no polling)
       *
       * Recommendation: false (don't poll by default)
       * - Enable per-query for real-time data (e.g., stock prices)
       * - Example: refetchInterval: 5000 (5 seconds)
       */
      refetchInterval: false,

      /**
       * enabled: Whether query should auto-run
       *
       * - Default: true
       *
       * Recommendation: Control per-query
       * - Useful for dependent queries (wait for user ID)
       * - Example: enabled: !!userId
       */
      // enabled: true,
    },

    mutations: {
      /**
       * retry: Don't retry mutations by default
       *
       * - Mutations change server state (POST/PUT/DELETE)
       * - Retrying could duplicate actions (e.g., charge card twice)
       * - Default: 0 (don't retry)
       *
       * Recommendation: 0 (keep default)
       * - Only retry if mutation is idempotent
       * - Better to show error and let user retry manually
       */
      retry: 0,

      /**
       * onError: Global mutation error handler
       *
       * - Log errors, show toast, etc.
       * - Can be overridden per-mutation
       */
      // onError: (error) => {
      //   console.error('Mutation error:', error)
      //   toast.error('Something went wrong. Please try again.')
      // },
    },
  },
})

/**
 * Advanced: Network Mode
 *
 * Controls how queries behave when offline
 * - 'online': Only fetch when online (default)
 * - 'always': Fetch even when offline (will fail, good for testing)
 * - 'offlineFirst': Use cache first, fetch if online
 *
 * Recommendation: 'online' (keep default)
 *
 * Set in defaultOptions.queries.networkMode if needed
 */

/**
 * Advanced: Query Cache Listeners
 *
 * Listen to cache updates globally (analytics, debugging)
 *
 * Example:
 * queryClient.getQueryCache().subscribe((event) => {
 *   console.log('Cache event:', event)
 * })
 */

/**
 * Advanced: Prefetching
 *
 * Prefetch data before component mounts (faster UX)
 *
 * Example (in route loader or parent component):
 * await queryClient.prefetchQuery({
 *   queryKey: ['products'],
 *   queryFn: fetchProducts,
 * })
 */

/**
 * Development vs Production Configuration
 *
 * Adjust settings based on environment
 */
if (import.meta.env.DEV) {
  // Development: Faster refetching for better DX
  queryClient.setDefaultOptions({
    queries: {
      staleTime: 0, // Always refetch in dev (see latest data)
      gcTime: 1 * 60 * 1000, // 1 minute (less memory usage)
    },
  })
}

/**
 * Type-Safe Query Keys Pattern
 *
 * Define query keys as constants to avoid typos
 *
 * Example:
 * export const queryKeys = {
 *   products: ['products'] as const,
 *   productById: (id: string) => ['products', id] as const,
 *   productsByCategory: (category: string) => ['products', { category }] as const,
 * }
 *
 * Usage:
 * useQuery({ queryKey: queryKeys.products, queryFn: fetchProducts })
 */
