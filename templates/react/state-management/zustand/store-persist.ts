/**
 * Zustand - Persistent Store with localStorage
 *
 * SAP-023: React State Management Patterns
 * Template: store-persist.ts
 *
 * Purpose:
 * - Persist Zustand state to localStorage
 * - Survive page refreshes (user preferences, auth, cart)
 * - Handle SSR hydration (Next.js 15)
 * - Migrate state between versions
 *
 * Use persist middleware for:
 * - User preferences (theme, language, settings)
 * - Auth tokens (user, accessToken)
 * - Shopping cart
 * - Form drafts
 *
 * DO NOT persist:
 * - UI state (modals, sidebar) - should reset on refresh
 * - Temporary filters
 * - Server data (use TanStack Query)
 *
 * @see https://docs.pmnd.rs/zustand/integrations/persisting-store-data
 */

import { create } from 'zustand'
import { persist, createJSONStorage, PersistOptions } from 'zustand/middleware'

/**
 * Example 1: Basic Persist (Theme)
 *
 * Persist theme preference to localStorage
 */

interface ThemeStore {
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
  toggleTheme: () => void
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
    }),
    {
      name: 'theme-store', // localStorage key
    },
  ),
)

/**
 * Usage:
 *
 * function ThemeToggle() {
 *   const { theme, toggleTheme } = useThemeStore()
 *   return <button onClick={toggleTheme}>{theme}</button>
 * }
 *
 * localStorage:
 * Key: 'theme-store'
 * Value: {"state":{"theme":"dark"},"version":0}
 *
 * On page refresh → theme restored from localStorage
 */

/**
 * Example 2: Partial Persist (Auth + UI)
 *
 * Only persist auth, not UI state
 */

interface AppStore {
  // Auth (persist)
  user: { id: string; name: string } | null
  token: string | null
  login: (user: AppStore['user'], token: string) => void
  logout: () => void

  // UI (don't persist)
  sidebarOpen: boolean
  toggleSidebar: () => void
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      // Auth
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),

      // UI
      sidebarOpen: false,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    {
      name: 'app-store',

      // partialize: Only persist specific state
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        // DON'T persist sidebarOpen (should reset on refresh)
      }),
    },
  ),
)

/**
 * Usage:
 *
 * function App() {
 *   const { user, logout } = useAppStore()
 *   // user restored from localStorage on mount
 *
 *   return user ? <button onClick={logout}>Logout</button> : <LoginForm />
 * }
 *
 * localStorage:
 * Only { user, token } stored, NOT sidebarOpen
 */

/**
 * Example 3: SSR Hydration (Next.js 15)
 *
 * Handle client-only state in Server Components
 * - Prevent hydration mismatch errors
 * - Use useEffect to check if hydrated
 */

interface PreferencesStore {
  preferences: {
    notifications: boolean
    language: string
  }
  setPreferences: (prefs: Partial<PreferencesStore['preferences']>) => void
  _hasHydrated: boolean
  setHasHydrated: (hasHydrated: boolean) => void
}

export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      preferences: {
        notifications: true,
        language: 'en',
      },
      setPreferences: (prefs) =>
        set((state) => ({
          preferences: { ...state.preferences, ...prefs },
        })),

      // Hydration tracking
      _hasHydrated: false,
      setHasHydrated: (hasHydrated) => set({ _hasHydrated: hasHydrated }),
    }),
    {
      name: 'preferences-store',

      // onRehydrateStorage: Called after rehydration
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    },
  ),
)

/**
 * Usage (Next.js 15 Client Component):
 *
 * 'use client'
 *
 * import { useEffect, useState } from 'react'
 *
 * function PreferencesPanel() {
 *   const { preferences, setPreferences, _hasHydrated } = usePreferencesStore()
 *   const [mounted, setMounted] = useState(false)
 *
 *   useEffect(() => {
 *     setMounted(true)
 *   }, [])
 *
 *   // Prevent hydration mismatch (SSR vs client state differ)
 *   if (!mounted || !_hasHydrated) {
 *     return <div>Loading preferences...</div>
 *   }
 *
 *   return (
 *     <div>
 *       <label>
 *         <input
 *           type="checkbox"
 *           checked={preferences.notifications}
 *           onChange={(e) => setPreferences({ notifications: e.target.checked })}
 *         />
 *         Notifications
 *       </label>
 *     </div>
 *   )
 * }
 *
 * Pattern Explained:
 * 1. SSR renders with default state (notifications: true)
 * 2. Client hydrates, reads localStorage, updates state
 * 3. Without mounted check → hydration mismatch error
 * 4. With mounted check → render loading until hydrated
 *
 * Alternative: Use skipHydration option (see below)
 */

/**
 * Example 4: Custom Storage (sessionStorage, IndexedDB)
 *
 * Use sessionStorage instead of localStorage
 * - Data cleared when tab closes
 * - Good for temporary preferences
 */

interface SessionStore {
  tempFilters: { category: string | null }
  setTempFilters: (filters: SessionStore['tempFilters']) => void
}

export const useSessionStore = create<SessionStore>()(
  persist(
    (set) => ({
      tempFilters: { category: null },
      setTempFilters: (tempFilters) => set({ tempFilters }),
    }),
    {
      name: 'session-store',
      storage: createJSONStorage(() => sessionStorage), // Use sessionStorage
    },
  ),
)

/**
 * Other Storage Options:
 *
 * // IndexedDB (for large data)
 * import { get, set, del } from 'idb-keyval'
 * storage: createJSONStorage(() => ({
 *   getItem: async (name) => (await get(name)) ?? null,
 *   setItem: async (name, value) => await set(name, value),
 *   removeItem: async (name) => await del(name),
 * }))
 *
 * // AsyncStorage (React Native)
 * import AsyncStorage from '@react-native-async-storage/async-storage'
 * storage: createJSONStorage(() => AsyncStorage)
 */

/**
 * Example 5: Migration (State Version Management)
 *
 * Migrate state when structure changes
 * - Prevent breaking changes on user's localStorage
 * - Transform old state to new format
 */

interface CartStore {
  items: { id: string; quantity: number }[]
  addItem: (item: CartStore['items'][0]) => void
}

export const useCartStore = create<CartStore>()(
  persist(
    (set) => ({
      items: [],
      addItem: (item) => set((state) => ({ items: [...state.items, item] })),
    }),
    {
      name: 'cart-store',
      version: 1, // Increment on breaking changes

      // migrate: Transform old state to new structure
      migrate: (persistedState: any, version: number) => {
        // Version 0 → 1: items was array of IDs, now objects
        if (version === 0) {
          return {
            items: persistedState.items.map((id: string) => ({
              id,
              quantity: 1, // Add default quantity
            })),
          }
        }

        return persistedState
      },
    },
  ),
)

/**
 * Migration Flow:
 * 1. User has old state (version: 0)
 * 2. Code updated to version: 1
 * 3. migrate() runs automatically
 * 4. Old state transformed to new format
 * 5. New state saved to localStorage
 *
 * When to migrate:
 * - Adding required fields (e.g., quantity)
 * - Changing structure (array → object)
 * - Renaming fields
 *
 * When NOT to migrate:
 * - Adding optional fields (just use defaults)
 * - Minor changes (backwards compatible)
 */

/**
 * Advanced: skipHydration (Next.js 15 SSR)
 *
 * Skip hydration check, load from localStorage only client-side
 */

export const useThemeStoreSSR = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
    }),
    {
      name: 'theme-store',
      skipHydration: true, // Don't auto-hydrate (manual control)
    },
  ),
)

/**
 * Usage (manual hydration):
 *
 * 'use client'
 *
 * import { useEffect } from 'react'
 *
 * function App({ children }) {
 *   useEffect(() => {
 *     useThemeStoreSSR.persist.rehydrate() // Manual hydration
 *   }, [])
 *
 *   return <div>{children}</div>
 * }
 */

/**
 * Persist Options Reference
 *
 * persist(storeCreator, {
 *   name: string,                      // localStorage key (required)
 *   storage: Storage,                  // localStorage, sessionStorage, custom
 *   partialize: (state) => Partial<T>, // Only persist specific state
 *   version: number,                   // State version (for migrations)
 *   migrate: (state, version) => T,    // Migration function
 *   skipHydration: boolean,            // Don't auto-hydrate (manual control)
 *   onRehydrateStorage: () => (state) => void, // Callback after hydration
 * })
 */

/**
 * Common Pitfalls
 *
 * 1. Persisting UI state
 *    ❌ persist({ sidebarOpen: true })
 *    ✅ persist({ user, token }) only
 *
 * 2. Large localStorage (>5MB)
 *    ❌ persist({ products: 10000 items })
 *    ✅ Use IndexedDB or server state (TanStack Query)
 *
 * 3. SSR hydration mismatch
 *    ❌ Render persisted state immediately (SSR != client)
 *    ✅ Use _hasHydrated or skipHydration + manual
 *
 * 4. Security: Storing sensitive data
 *    ❌ persist({ creditCard: '...' })
 *    ✅ Only store non-sensitive data, encrypt if needed
 *
 * 5. Breaking changes without migration
 *    ❌ Change structure, old users get errors
 *    ✅ Increment version, provide migrate function
 */

/**
 * Performance Considerations
 *
 * - localStorage is SYNCHRONOUS (blocks main thread)
 * - Writes on every set() call
 * - For frequent updates, consider debouncing:
 *
 * import { debounce } from 'lodash'
 *
 * const debouncedPersist = debounce(() => {
 *   useCartStore.persist.rehydrate()
 * }, 1000)
 *
 * Note: Built-in persist already optimized (JSON.stringify once per update)
 */
