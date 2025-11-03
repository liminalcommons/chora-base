/**
 * Zustand - Basic Store Example
 *
 * SAP-023: React State Management Patterns
 * Template: store-basic.ts
 *
 * Purpose:
 * - Demonstrate simple Zustand store for client-side UI state
 * - Zero boilerplate: No providers, context, or reducers
 * - TypeScript-first with automatic type inference
 * - Automatic re-render optimization (only re-render what changed)
 *
 * Use Zustand for CLIENT STATE (UI state, preferences, filters)
 * - Theme (light/dark)
 * - Sidebar open/closed
 * - Selected filters
 * - User preferences
 *
 * DO NOT use Zustand for SERVER STATE (API data)
 * - Use TanStack Query for server state (caching, refetching, etc.)
 * - See use-query-example.ts
 *
 * Bundle Size: 1-3KB (vs Redux 30KB+)
 * Downloads: 12.1M/week (surpassed Redux 6.9M/week)
 *
 * @see https://docs.pmnd.rs/zustand/getting-started/introduction
 */

import { create } from 'zustand'

/**
 * Example 1: Theme Store (Simplest)
 *
 * Toggle between light/dark theme
 * - 2 state properties (theme, setTheme)
 * - 1 derived action (toggleTheme)
 * - Total: 10 lines of code
 */

interface ThemeStore {
  // State
  theme: 'light' | 'dark'

  // Actions
  setTheme: (theme: 'light' | 'dark') => void
  toggleTheme: () => void
}

export const useThemeStore = create<ThemeStore>((set) => ({
  // Initial state
  theme: 'light',

  // Actions (update state)
  setTheme: (theme) => set({ theme }),

  toggleTheme: () =>
    set((state) => ({
      theme: state.theme === 'light' ? 'dark' : 'light',
    })),
}))

/**
 * Usage in Component:
 *
 * function ThemeToggle() {
 *   const theme = useThemeStore((state) => state.theme)
 *   const toggleTheme = useThemeStore((state) => state.toggleTheme)
 *
 *   return (
 *     <button onClick={toggleTheme}>
 *       Current theme: {theme}
 *     </button>
 *   )
 * }
 *
 * Key Benefits:
 * 1. NO PROVIDER: Works out of the box (unlike Context)
 * 2. AUTOMATIC OPTIMIZATION: Component only re-renders when theme changes
 * 3. SIMPLE: No actions, reducers, dispatch, or boilerplate
 *
 * Selector Pattern:
 * - useThemeStore((state) => state.theme) subscribes to theme only
 * - If other state changes (e.g., user), component doesn't re-render
 * - This is why Zustand is fast (automatic optimization)
 */

/**
 * Example 2: Counter Store (Actions)
 *
 * Simple counter with increment/decrement
 * - Demonstrates multiple actions
 * - Shows how to access current state in actions
 */

interface CounterStore {
  count: number
  increment: () => void
  decrement: () => void
  incrementBy: (amount: number) => void
  reset: () => void
}

export const useCounterStore = create<CounterStore>((set) => ({
  count: 0,

  increment: () => set((state) => ({ count: state.count + 1 })),

  decrement: () => set((state) => ({ count: state.count - 1 })),

  incrementBy: (amount) => set((state) => ({ count: state.count + amount })),

  reset: () => set({ count: 0 }),
}))

/**
 * Usage:
 *
 * function Counter() {
 *   const count = useCounterStore((state) => state.count)
 *   const increment = useCounterStore((state) => state.increment)
 *   const decrement = useCounterStore((state) => state.decrement)
 *   const reset = useCounterStore((state) => state.reset)
 *
 *   return (
 *     <div>
 *       <h1>Count: {count}</h1>
 *       <button onClick={increment}>+</button>
 *       <button onClick={decrement}>-</button>
 *       <button onClick={reset}>Reset</button>
 *     </div>
 *   )
 * }
 *
 * Alternative: Destructure multiple values
 * function Counter() {
 *   const { count, increment, decrement } = useCounterStore()
 *   // ⚠️ WARNING: This subscribes to ALL state changes (less optimal)
 *   // Better to use selectors for large stores
 * }
 */

/**
 * Example 3: Filter Store (Complex State)
 *
 * Product filters for e-commerce app
 * - Multiple state properties
 * - Complex actions (update specific filter)
 * - Demonstrates real-world use case
 */

interface ProductFilters {
  category: string | null
  priceRange: [number, number]
  inStockOnly: boolean
  searchQuery: string
  sortBy: 'name' | 'price' | 'date'
}

interface FilterStore extends ProductFilters {
  setCategory: (category: string | null) => void
  setPriceRange: (range: [number, number]) => void
  setInStockOnly: (value: boolean) => void
  setSearchQuery: (query: string) => void
  setSortBy: (sortBy: ProductFilters['sortBy']) => void
  resetFilters: () => void
}

const initialFilters: ProductFilters = {
  category: null,
  priceRange: [0, 1000],
  inStockOnly: false,
  searchQuery: '',
  sortBy: 'name',
}

export const useFilterStore = create<FilterStore>((set) => ({
  // Initial state
  ...initialFilters,

  // Actions
  setCategory: (category) => set({ category }),

  setPriceRange: (priceRange) => set({ priceRange }),

  setInStockOnly: (inStockOnly) => set({ inStockOnly }),

  setSearchQuery: (searchQuery) => set({ searchQuery }),

  setSortBy: (sortBy) => set({ sortBy }),

  resetFilters: () => set(initialFilters),
}))

/**
 * Usage:
 *
 * function ProductFilters() {
 *   const category = useFilterStore((state) => state.category)
 *   const setCategory = useFilterStore((state) => state.setCategory)
 *   const inStockOnly = useFilterStore((state) => state.inStockOnly)
 *   const setInStockOnly = useFilterStore((state) => state.setInStockOnly)
 *   const resetFilters = useFilterStore((state) => state.resetFilters)
 *
 *   return (
 *     <div>
 *       <select value={category || ''} onChange={(e) => setCategory(e.target.value)}>
 *         <option value="">All Categories</option>
 *         <option value="electronics">Electronics</option>
 *         <option value="clothing">Clothing</option>
 *       </select>
 *
 *       <label>
 *         <input
 *           type="checkbox"
 *           checked={inStockOnly}
 *           onChange={(e) => setInStockOnly(e.target.checked)}
 *         />
 *         In Stock Only
 *       </label>
 *
 *       <button onClick={resetFilters}>Reset Filters</button>
 *     </div>
 *   )
 * }
 *
 * Integration with TanStack Query:
 *
 * function ProductList() {
 *   // Server state (TanStack Query)
 *   const { data: products } = useQuery({
 *     queryKey: ['products'],
 *     queryFn: fetchProducts,
 *   })
 *
 *   // Client state (Zustand)
 *   const filters = useFilterStore()
 *
 *   // Filter products client-side
 *   const filteredProducts = useMemo(() => {
 *     if (!products) return []
 *
 *     return products
 *       .filter((p) => !filters.category || p.category === filters.category)
 *       .filter((p) => !filters.inStockOnly || p.inStock)
 *       .filter((p) => p.name.toLowerCase().includes(filters.searchQuery.toLowerCase()))
 *       .sort((a, b) => {
 *         if (filters.sortBy === 'name') return a.name.localeCompare(b.name)
 *         if (filters.sortBy === 'price') return a.price - b.price
 *         return 0
 *       })
 *   }, [products, filters])
 *
 *   return (
 *     <div>
 *       {filteredProducts.map((product) => (
 *         <div key={product.id}>{product.name}</div>
 *       ))}
 *     </div>
 *   )
 * }
 */

/**
 * Example 4: Auth Store (Async Actions)
 *
 * User authentication state
 * - Demonstrates async actions (login, logout)
 * - Shows how to handle loading states
 * - Integration with API
 */

interface User {
  id: string
  name: string
  email: string
}

interface AuthStore {
  user: User | null
  isLoading: boolean
  error: string | null

  login: (email: string, password: string) => Promise<void>
  logout: () => void
  clearError: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null })

    try {
      // Call API (replace with actual API call)
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const user = await response.json()

      set({ user, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      })
    }
  },

  logout: () => {
    // Call API to logout (optional)
    // await fetch('/api/auth/logout', { method: 'POST' })

    set({ user: null })
  },

  clearError: () => set({ error: null }),
}))

/**
 * Usage:
 *
 * function LoginForm() {
 *   const { user, isLoading, error, login, clearError } = useAuthStore()
 *
 *   const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
 *     e.preventDefault()
 *     const formData = new FormData(e.currentTarget)
 *     await login(
 *       formData.get('email') as string,
 *       formData.get('password') as string
 *     )
 *   }
 *
 *   if (user) {
 *     return <div>Welcome, {user.name}!</div>
 *   }
 *
 *   return (
 *     <form onSubmit={handleSubmit}>
 *       {error && (
 *         <div role="alert">
 *           {error}
 *           <button onClick={clearError}>×</button>
 *         </div>
 *       )}
 *       <input name="email" type="email" required />
 *       <input name="password" type="password" required />
 *       <button disabled={isLoading}>
 *         {isLoading ? 'Logging in...' : 'Login'}
 *       </button>
 *     </form>
 *   )
 * }
 *
 * Note: For more robust auth, consider using TanStack Query mutations
 * Zustand is best for storing auth STATE (user, token)
 * TanStack Query is best for auth ACTIONS (login, logout API calls)
 */

/**
 * Advanced: Computed Values (Selectors)
 *
 * Derive values from state without storing duplicates
 *
 * interface CartStore {
 *   items: CartItem[]
 *   addItem: (item: CartItem) => void
 *   removeItem: (id: string) => void
 *
 *   // Computed values (NOT stored in state)
 *   get total(): number
 *   get itemCount(): number
 * }
 *
 * export const useCartStore = create<CartStore>((set, get) => ({
 *   items: [],
 *
 *   addItem: (item) => set((state) => ({ items: [...state.items, item] })),
 *
 *   removeItem: (id) =>
 *     set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
 *
 *   // Computed values use get()
 *   get total() {
 *     return get().items.reduce((sum, item) => sum + item.price, 0)
 *   },
 *
 *   get itemCount() {
 *     return get().items.length
 *   },
 * }))
 *
 * Usage:
 * const total = useCartStore((state) => state.total)
 * const itemCount = useCartStore((state) => state.itemCount)
 *
 * Note: Computed values recalculated on every access
 * For expensive calculations, consider useMemo in component
 */

/**
 * Performance Tips
 *
 * 1. Use Selectors (subscribe to specific state only):
 *    ✅ const theme = useThemeStore((state) => state.theme)
 *    ❌ const { theme } = useThemeStore() // Re-renders on ANY state change
 *
 * 2. Memoize Selectors (for complex logic):
 *    const filteredProducts = useFilterStore(
 *      useCallback((state) => state.products.filter(...), [])
 *    )
 *
 * 3. Batch Updates (multiple set calls):
 *    set((state) => ({
 *      count: state.count + 1,
 *      lastUpdated: Date.now(),
 *    }))
 *    // Better than two separate set() calls
 *
 * 4. Shallow Equality (for objects):
 *    import { shallow } from 'zustand/shallow'
 *    const { theme, user } = useThemeStore(
 *      (state) => ({ theme: state.theme, user: state.user }),
 *      shallow
 *    )
 */

/**
 * TypeScript Tips
 *
 * 1. Infer types from interface:
 *    interface Store { count: number; increment: () => void }
 *    const useStore = create<Store>(...)
 *    // Types automatically inferred in components
 *
 * 2. Derive types from store:
 *    const useStore = create<Store>(...)
 *    type StoreState = ReturnType<typeof useStore.getState>
 *
 * 3. Action types:
 *    type StoreActions = Pick<Store, 'increment' | 'decrement'>
 */
