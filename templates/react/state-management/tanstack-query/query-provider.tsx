/**
 * TanStack Query Provider Component
 *
 * SAP-023: React State Management Patterns
 * Template: query-provider.tsx
 *
 * Purpose:
 * - Wrap app with QueryClientProvider
 * - Enable React Query DevTools (dev only)
 * - Provide error boundary for query errors
 *
 * Usage (Next.js 15 App Router):
 * // app/layout.tsx
 * import { QueryProvider } from '@/lib/query-provider'
 *
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         <QueryProvider>{children}</QueryProvider>
 *       </body>
 *     </html>
 *   )
 * }
 *
 * Usage (Vite 7):
 * // src/main.tsx
 * import { QueryProvider } from './lib/query-provider'
 *
 * ReactDOM.createRoot(document.getElementById('root')!).render(
 *   <QueryProvider>
 *     <App />
 *   </QueryProvider>
 * )
 *
 * @see https://tanstack.com/query/v5/docs/react/reference/QueryClientProvider
 */

'use client' // Required for Next.js 15 App Router (Client Component)

import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { queryClient } from './query-client'
import type { ReactNode } from 'react'

interface QueryProviderProps {
  children: ReactNode
}

/**
 * Query Provider Component
 *
 * Wraps app with QueryClientProvider and DevTools
 *
 * Note: This is a Client Component ('use client')
 * - TanStack Query uses hooks (client-side only)
 * - In Next.js 15, wrap children (which can be Server Components)
 */
export function QueryProvider({ children }: QueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}

      {/* React Query DevTools - Development only */}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools
          initialIsOpen={false}
          buttonPosition="bottom-right"
          position="bottom"
        />
      )}
    </QueryClientProvider>
  )
}

/**
 * React Query DevTools Features
 *
 * - View all queries and their states (loading, success, error)
 * - Inspect query data and cache
 * - Manually refetch, invalidate, or reset queries
 * - Monitor network requests
 * - Debug stale/fresh data
 *
 * Keyboard Shortcut: Click floating button (bottom-right)
 *
 * Advanced DevTools Config:
 * <ReactQueryDevtools
 *   initialIsOpen={false}          // Start closed (default)
 *   buttonPosition="bottom-right"  // Button position
 *   position="bottom"              // Panel position (bottom, top, left, right)
 *   panelPosition="bottom"         // Deprecated, use position
 *   toggleButtonProps={{ ... }}    // Customize button
 *   closeButtonProps={{ ... }}     // Customize close button
 *   errorTypes={[...]}             // Filter error types
 * />
 */

/**
 * Next.js 15 App Router Pattern
 *
 * app/layout.tsx:
 * import { QueryProvider } from '@/lib/query-provider'
 *
 * export default function RootLayout({ children }: { children: ReactNode }) {
 *   return (
 *     <html lang="en">
 *       <body>
 *         <QueryProvider>
 *           {children}  {/* Can be Server Components */}
 *         </QueryProvider>
 *       </body>
 *     </html>
 *   )
 * }
 *
 * app/page.tsx (Server Component):
 * export default async function HomePage() {
 *   // This is a Server Component (no 'use client')
 *   // Can fetch data server-side, pass to Client Components
 *   return <ProductList />
 * }
 *
 * app/components/product-list.tsx (Client Component):
 * 'use client'
 * import { useQuery } from '@tanstack/react-query'
 *
 * export function ProductList() {
 *   const { data } = useQuery({ ... })  // Uses QueryProvider from layout
 *   return <div>{data.map(...)}</div>
 * }
 */

/**
 * Vite 7 Pattern
 *
 * src/main.tsx:
 * import { StrictMode } from 'react'
 * import { createRoot } from 'react-dom/client'
 * import { QueryProvider } from './lib/query-provider'
 * import App from './App'
 * import './index.css'
 *
 * createRoot(document.getElementById('root')!).render(
 *   <StrictMode>
 *     <QueryProvider>
 *       <App />
 *     </QueryProvider>
 *   </StrictMode>
 * )
 *
 * src/App.tsx:
 * import { useQuery } from '@tanstack/react-query'
 *
 * export default function App() {
 *   const { data } = useQuery({ ... })  // Uses QueryProvider from main.tsx
 *   return <div>{data.map(...)}</div>
 * }
 */

/**
 * Error Boundary Pattern (Optional)
 *
 * Wrap QueryProvider with ErrorBoundary for global error handling
 *
 * import { ErrorBoundary } from 'react-error-boundary'
 *
 * export function Providers({ children }: { children: ReactNode }) {
 *   return (
 *     <ErrorBoundary
 *       fallback={<ErrorFallback />}
 *       onError={(error) => console.error('Query error:', error)}
 *     >
 *       <QueryProvider>{children}</QueryProvider>
 *     </ErrorBoundary>
 *   )
 * }
 *
 * Note: TanStack Query has built-in error handling per query
 * Global ErrorBoundary is optional, useful for unhandled errors
 */

/**
 * Hydration Pattern (Next.js SSR)
 *
 * For Server-Side Rendering with prefetched data:
 *
 * app/layout.tsx:
 * import { HydrationBoundary, dehydrate } from '@tanstack/react-query'
 * import { queryClient } from '@/lib/query-client'
 *
 * export default async function Layout({ children }) {
 *   // Prefetch data server-side
 *   await queryClient.prefetchQuery({
 *     queryKey: ['products'],
 *     queryFn: fetchProducts,
 *   })
 *
 *   return (
 *     <QueryProvider>
 *       <HydrationBoundary state={dehydrate(queryClient)}>
 *         {children}
 *       </HydrationBoundary>
 *     </QueryProvider>
 *   )
 * }
 *
 * Note: This is advanced - most apps don't need SSR prefetching
 * Use for critical above-the-fold data only
 */

/**
 * Multiple Providers Pattern
 *
 * Combine QueryProvider with other providers (Theme, Auth, etc.)
 *
 * export function Providers({ children }: { children: ReactNode }) {
 *   return (
 *     <QueryProvider>
 *       <ThemeProvider>
 *         <AuthProvider>
 *           {children}
 *         </AuthProvider>
 *       </ThemeProvider>
 *     </QueryProvider>
 *   )
 * }
 *
 * Recommendation: Keep providers in separate file (lib/providers.tsx)
 * Makes it easy to add/remove providers
 */
