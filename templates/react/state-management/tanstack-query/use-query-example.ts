/**
 * TanStack Query - useQuery Hook Examples
 *
 * SAP-023: React State Management Patterns
 * Template: use-query-example.ts
 *
 * Purpose:
 * - Demonstrate useQuery patterns for fetching data (GET requests)
 * - Cover common use cases: basic query, params, dependent queries, polling
 * - Production-ready error handling and TypeScript typing
 *
 * useQuery is for READ operations (GET)
 * - Automatically caches data
 * - Handles loading, error, success states
 * - Refetches based on config (staleTime, refetchOnWindowFocus, etc.)
 * - Deduplicates requests (multiple components using same query = 1 request)
 *
 * For WRITE operations (POST/PUT/DELETE), see use-mutation-example.ts
 *
 * @see https://tanstack.com/query/v5/docs/react/reference/useQuery
 */

'use client' // Required for Next.js 15 Client Components

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api-client' // See SAP-023 api-client.ts template

/**
 * Type Definitions
 *
 * Define types for your data
 * Ensures type safety throughout query lifecycle
 */
interface Product {
  id: string
  name: string
  price: number
  category: string
  inStock: boolean
}

interface User {
  id: string
  name: string
  email: string
}

interface UserProfile {
  userId: string
  bio: string
  avatarUrl: string
}

/**
 * API Functions
 *
 * Extract API calls into separate functions
 * - Easier to test
 * - Reusable across queries
 * - Clear separation of concerns
 */
async function fetchProducts(): Promise<Product[]> {
  const response = await api.get<Product[]>('/products')
  return response.data
}

async function fetchProductById(id: string): Promise<Product> {
  const response = await api.get<Product>(`/products/${id}`)
  return response.data
}

async function fetchUser(userId: string): Promise<User> {
  const response = await api.get<User>(`/users/${userId}`)
  return response.data
}

async function fetchUserProfile(userId: string): Promise<UserProfile> {
  const response = await api.get<UserProfile>(`/users/${userId}/profile`)
  return response.data
}

async function searchProducts(query: string): Promise<Product[]> {
  const response = await api.get<Product[]>('/products/search', {
    params: { q: query },
  })
  return response.data
}

/**
 * Example 1: Basic Query
 *
 * Fetch a list of products
 * - Simplest use case
 * - No parameters needed
 * - Automatically caches with queryKey ['products']
 */
export function useProducts() {
  return useQuery({
    queryKey: ['products'], // Unique key for this query (used for caching)
    queryFn: fetchProducts, // Function that returns a Promise
  })
}

/**
 * Usage in Component:
 *
 * function ProductList() {
 *   const { data, isLoading, error } = useProducts()
 *
 *   if (isLoading) return <div>Loading...</div>
 *   if (error) return <div>Error: {error.message}</div>
 *
 *   return (
 *     <ul>
 *       {data.map((product) => (
 *         <li key={product.id}>{product.name}</li>
 *       ))}
 *     </ul>
 *   )
 * }
 *
 * Data Lifecycle:
 * 1. Component mounts → isLoading: true
 * 2. fetchProducts() called → network request
 * 3. Success → data populated, isLoading: false
 * 4. Data cached with key ['products']
 * 5. Component unmounts → data stays in cache (gcTime)
 * 6. Component re-mounts → if data fresh (staleTime), use cache, else refetch
 */

/**
 * Example 2: Query with Parameters
 *
 * Fetch a single product by ID
 * - Include params in queryKey (cache per ID)
 * - Use arrow function for queryFn (closure over id)
 */
export function useProduct(id: string) {
  return useQuery({
    queryKey: ['products', id], // Different cache entry per ID
    queryFn: () => fetchProductById(id), // Arrow function to pass id
    enabled: !!id, // Only run query if id exists (conditional execution)
  })
}

/**
 * Usage:
 *
 * function ProductDetail({ id }: { id: string }) {
 *   const { data: product, isLoading } = useProduct(id)
 *
 *   if (isLoading) return <div>Loading...</div>
 *
 *   return <div>{product.name} - ${product.price}</div>
 * }
 *
 * Cache Behavior:
 * - useProduct('1') and useProduct('2') cache separately
 * - queryKey ['products', '1'] vs ['products', '2']
 * - Navigating back to product '1' → instant load (cache hit)
 *
 * enabled Pattern:
 * - enabled: !!id prevents query from running if id is null/undefined
 * - Useful for dependent data (wait for user to select product)
 */

/**
 * Example 3: Dependent Queries
 *
 * Fetch user profile AFTER fetching user
 * - Wait for user query to succeed before fetching profile
 * - Use enabled to control execution order
 */
export function useUserWithProfile(userId: string) {
  // First query: Fetch user
  const userQuery = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
    enabled: !!userId,
  })

  // Second query: Fetch user profile (depends on user query success)
  const profileQuery = useQuery({
    queryKey: ['users', userId, 'profile'],
    queryFn: () => fetchUserProfile(userId),
    enabled: !!userQuery.data, // Only run if user data exists
  })

  return {
    user: userQuery.data,
    profile: profileQuery.data,
    isLoading: userQuery.isLoading || profileQuery.isLoading,
    error: userQuery.error || profileQuery.error,
  }
}

/**
 * Usage:
 *
 * function UserProfile({ userId }: { userId: string }) {
 *   const { user, profile, isLoading } = useUserWithProfile(userId)
 *
 *   if (isLoading) return <div>Loading...</div>
 *
 *   return (
 *     <div>
 *       <h1>{user.name}</h1>
 *       <p>{profile.bio}</p>
 *     </div>
 *   )
 * }
 *
 * Execution Order:
 * 1. userQuery runs (enabled: !!userId)
 * 2. userQuery succeeds → userQuery.data populated
 * 3. profileQuery runs (enabled: !!userQuery.data)
 * 4. profileQuery succeeds → profile.data populated
 *
 * Why Dependent Queries?
 * - Avoid 404 errors (profile needs userId from user)
 * - Sequential data fetching (can't fetch profile without user)
 * - Better error handling (if user fails, don't try profile)
 */

/**
 * Example 4: Search Query with Debouncing
 *
 * Search products as user types
 * - Debounce user input (avoid request on every keystroke)
 * - Keep previous data while fetching new results (better UX)
 */
export function useProductSearch(query: string) {
  return useQuery({
    queryKey: ['products', 'search', query],
    queryFn: () => searchProducts(query),
    enabled: query.length >= 3, // Only search if query is 3+ characters
    staleTime: 30 * 1000, // 30 seconds (search results don't change often)
    placeholderData: (previousData) => previousData, // Keep previous results while loading
  })
}

/**
 * Usage (with debounced input):
 *
 * import { useState } from 'react'
 * import { useDebounce } from '@/hooks/use-debounce' // Custom hook
 *
 * function ProductSearch() {
 *   const [input, setInput] = useState('')
 *   const debouncedQuery = useDebounce(input, 300) // 300ms debounce
 *
 *   const { data: results, isLoading } = useProductSearch(debouncedQuery)
 *
 *   return (
 *     <div>
 *       <input
 *         value={input}
 *         onChange={(e) => setInput(e.target.value)}
 *         placeholder="Search products..."
 *       />
 *       {isLoading && <span>Searching...</span>}
 *       <ul>
 *         {results?.map((product) => (
 *           <li key={product.id}>{product.name}</li>
 *         ))}
 *       </ul>
 *     </div>
 *   )
 * }
 *
 * Debounce Hook (useDebounce):
 * export function useDebounce<T>(value: T, delay: number): T {
 *   const [debouncedValue, setDebouncedValue] = useState(value)
 *
 *   useEffect(() => {
 *     const timer = setTimeout(() => setDebouncedValue(value), delay)
 *     return () => clearTimeout(timer)
 *   }, [value, delay])
 *
 *   return debouncedValue
 * }
 *
 * Behavior:
 * - User types "laptop" → debounce waits 300ms after last keystroke
 * - After 300ms → debouncedQuery updates → query runs
 * - While loading new results, previous results still shown (placeholderData)
 * - No search if query <3 chars (enabled: query.length >= 3)
 */

/**
 * Example 5: Polling (Auto-Refetch)
 *
 * Poll server every 5 seconds for real-time data
 * - Useful for dashboards, stock prices, notifications
 * - Automatically stops when component unmounts
 */
export function useLiveProducts() {
  return useQuery({
    queryKey: ['products', 'live'],
    queryFn: fetchProducts,
    refetchInterval: 5000, // Refetch every 5 seconds
    refetchIntervalInBackground: false, // Pause polling when tab not visible (save bandwidth)
  })
}

/**
 * Usage:
 *
 * function LiveProductDashboard() {
 *   const { data: products, dataUpdatedAt } = useLiveProducts()
 *
 *   return (
 *     <div>
 *       <p>Last updated: {new Date(dataUpdatedAt).toLocaleTimeString()}</p>
 *       <ul>
 *         {products?.map((product) => (
 *           <li key={product.id}>
 *             {product.name} - {product.inStock ? 'In Stock' : 'Out of Stock'}
 *           </li>
 *         ))}
 *       </ul>
 *     </div>
 *   )
 * }
 *
 * Behavior:
 * - Initial fetch on mount
 * - Refetch every 5 seconds while component mounted
 * - If user switches tabs → pause polling (refetchIntervalInBackground: false)
 * - If user returns → resume polling
 * - Component unmounts → stop polling
 *
 * Advanced Polling:
 * - Dynamic interval: refetchInterval: (data) => data.hasNewData ? 1000 : 5000
 * - Conditional polling: refetchInterval: isLive ? 5000 : false
 */

/**
 * Advanced: Query Options
 *
 * All available useQuery options:
 *
 * useQuery({
 *   queryKey: ['key'],
 *   queryFn: fetchData,
 *
 *   // Caching
 *   staleTime: 60000,
 *   gcTime: 300000,
 *
 *   // Refetching
 *   refetchOnMount: true,
 *   refetchOnWindowFocus: true,
 *   refetchOnReconnect: true,
 *   refetchInterval: false,
 *   refetchIntervalInBackground: false,
 *
 *   // Retry
 *   retry: 3,
 *   retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
 *
 *   // Conditional Execution
 *   enabled: true,
 *
 *   // UX
 *   placeholderData: (previousData) => previousData,
 *   initialData: () => localStorage.getItem('cachedData'),
 *
 *   // Callbacks
 *   onSuccess: (data) => console.log('Success:', data),
 *   onError: (error) => console.error('Error:', error),
 *   onSettled: (data, error) => console.log('Settled'),
 *
 *   // Advanced
 *   select: (data) => data.filter(item => item.active), // Transform data
 *   keepPreviousData: true, // Deprecated in v5, use placeholderData
 *   structuralSharing: true, // Deep compare (default)
 *   notifyOnChangeProps: ['data', 'error'], // Only re-render on these changes
 * })
 */

/**
 * TypeScript Tips
 *
 * 1. Infer types from queryFn:
 *    const { data } = useQuery({ queryKey: ['key'], queryFn: fetchData })
 *    // data is inferred from fetchData return type
 *
 * 2. Override types:
 *    const { data } = useQuery<Product[], Error>({ ... })
 *
 * 3. Handle undefined (data is undefined during loading):
 *    const { data } = useQuery({ ... })
 *    const products = data ?? [] // Fallback to empty array
 *
 * 4. Type query result:
 *    const query: UseQueryResult<Product[], Error> = useQuery({ ... })
 */
