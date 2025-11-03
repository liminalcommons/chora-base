/**
 * Zustand - Slice Pattern for Large Stores
 *
 * SAP-023: React State Management Patterns
 * Template: store-slice-pattern.ts
 *
 * Purpose:
 * - Organize large stores into modular slices
 * - Each slice handles one domain (auth, ui, cart, settings)
 * - Combine slices into single store
 * - Scale to 50+ state properties without chaos
 *
 * Use this pattern when:
 * - Store has 5+ actions
 * - Multiple domains in one app (auth + cart + ui)
 * - Team needs separation of concerns
 *
 * @see https://docs.pmnd.rs/zustand/guides/typescript#slices-pattern
 */

import { create, StateCreator } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

/**
 * Type Definitions
 */
interface User {
  id: string
  name: string
  email: string
}

/**
 * Slice 1: Auth Slice
 *
 * Handles authentication state and actions
 */
interface AuthSlice {
  user: User | null
  token: string | null
  login: (user: User, token: string) => void
  logout: () => void
}

const createAuthSlice: StateCreator<AppStore, [], [], AuthSlice> = (set) => ({
  user: null,
  token: null,

  login: (user, token) => set({ user, token }, false, 'auth/login'),

  logout: () => set({ user: null, token: null }, false, 'auth/logout'),
})

/**
 * Slice 2: UI Slice
 *
 * Handles UI state (sidebar, modals, theme)
 */
interface UiSlice {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  modalOpen: boolean

  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
  openModal: () => void
  closeModal: () => void
}

const createUiSlice: StateCreator<AppStore, [], [], UiSlice> = (set) => ({
  theme: 'light',
  sidebarOpen: false,
  modalOpen: false,

  setTheme: (theme) => set({ theme }, false, 'ui/setTheme'),

  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen }), false, 'ui/toggleSidebar'),

  openModal: () => set({ modalOpen: true }, false, 'ui/openModal'),

  closeModal: () => set({ modalOpen: false }, false, 'ui/closeModal'),
})

/**
 * Slice 3: Cart Slice
 *
 * Handles shopping cart state
 */
interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartSlice {
  items: CartItem[]

  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  updateQuantity: (id: string, quantity: number) => void
  clearCart: () => void

  // Computed values
  get total(): number
  get itemCount(): number
}

const createCartSlice: StateCreator<AppStore, [], [], CartSlice> = (set, get) => ({
  items: [],

  addItem: (item) =>
    set(
      (state) => {
        const existing = state.items.find((i) => i.id === item.id)
        if (existing) {
          return {
            items: state.items.map((i) =>
              i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i,
            ),
          }
        }
        return { items: [...state.items, item] }
      },
      false,
      'cart/addItem',
    ),

  removeItem: (id) =>
    set(
      (state) => ({ items: state.items.filter((i) => i.id !== id) }),
      false,
      'cart/removeItem',
    ),

  updateQuantity: (id, quantity) =>
    set(
      (state) => ({
        items: state.items.map((i) => (i.id === id ? { ...i, quantity } : i)),
      }),
      false,
      'cart/updateQuantity',
    ),

  clearCart: () => set({ items: [] }, false, 'cart/clearCart'),

  get total() {
    return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  },

  get itemCount() {
    return get().items.reduce((sum, item) => sum + item.quantity, 0)
  },
})

/**
 * Slice 4: Settings Slice
 *
 * Handles user preferences/settings
 */
interface SettingsSlice {
  notifications: boolean
  language: 'en' | 'es' | 'fr'
  currency: 'USD' | 'EUR' | 'GBP'

  setNotifications: (enabled: boolean) => void
  setLanguage: (language: SettingsSlice['language']) => void
  setCurrency: (currency: SettingsSlice['currency']) => void
  resetSettings: () => void
}

const defaultSettings = {
  notifications: true,
  language: 'en' as const,
  currency: 'USD' as const,
}

const createSettingsSlice: StateCreator<AppStore, [], [], SettingsSlice> = (set) => ({
  ...defaultSettings,

  setNotifications: (notifications) => set({ notifications }, false, 'settings/setNotifications'),

  setLanguage: (language) => set({ language }, false, 'settings/setLanguage'),

  setCurrency: (currency) => set({ currency }, false, 'settings/setCurrency'),

  resetSettings: () => set(defaultSettings, false, 'settings/reset'),
})

/**
 * Combine All Slices into App Store
 */
type AppStore = AuthSlice & UiSlice & CartSlice & SettingsSlice

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (...args) => ({
        ...createAuthSlice(...args),
        ...createUiSlice(...args),
        ...createCartSlice(...args),
        ...createSettingsSlice(...args),
      }),
      {
        name: 'app-store',
        partialize: (state) => ({
          // Only persist specific slices
          user: state.user,
          token: state.token,
          theme: state.theme,
          settings: {
            notifications: state.notifications,
            language: state.language,
            currency: state.currency,
          },
        }),
      },
    ),
  ),
)

/**
 * Usage in Components:
 *
 * // Auth
 * function Header() {
 *   const user = useAppStore((state) => state.user)
 *   const logout = useAppStore((state) => state.logout)
 *
 *   return user ? <button onClick={logout}>Logout</button> : <LoginButton />
 * }
 *
 * // UI
 * function Sidebar() {
 *   const isOpen = useAppStore((state) => state.sidebarOpen)
 *   const toggle = useAppStore((state) => state.toggleSidebar)
 *
 *   return <aside className={isOpen ? 'open' : 'closed'}>...</aside>
 * }
 *
 * // Cart
 * function CartSummary() {
 *   const total = useAppStore((state) => state.total)
 *   const itemCount = useAppStore((state) => state.itemCount)
 *
 *   return <div>Total: ${total} ({itemCount} items)</div>
 * }
 *
 * // Settings
 * function LanguageSelector() {
 *   const language = useAppStore((state) => state.language)
 *   const setLanguage = useAppStore((state) => state.setLanguage)
 *
 *   return (
 *     <select value={language} onChange={(e) => setLanguage(e.target.value)}>
 *       <option value="en">English</option>
 *       <option value="es">Español</option>
 *     </select>
 *   )
 * }
 */

/**
 * Middleware Explained
 *
 * 1. devtools: Redux DevTools integration
 *    - View state, actions, time-travel debugging
 *    - Second param in set() is action name: set({ ... }, false, 'auth/login')
 *    - false = don't replace state, merge it
 *
 * 2. persist: localStorage persistence
 *    - name: localStorage key
 *    - partialize: Only persist specific state (avoid persisting UI state)
 *    - By default, persists entire store (can be large)
 *
 * Order matters:
 * devtools(persist(...)) = DevTools shows persisted actions
 * persist(devtools(...)) = DevTools doesn't see persist actions
 */

/**
 * Benefits of Slice Pattern
 *
 * 1. Separation of Concerns
 *    - Each slice is independent (easier to test, modify)
 *    - Clear boundaries between domains
 *
 * 2. Scalability
 *    - Add new slices without touching existing code
 *    - Easy to split into separate files
 *
 * 3. Team Collaboration
 *    - Different devs work on different slices (fewer conflicts)
 *    - Each slice has clear ownership
 *
 * 4. Type Safety
 *    - TypeScript infers all types correctly
 *    - Autocomplete for all actions and state
 *
 * 5. Testability
 *    - Test each slice independently
 *    - Mock specific slices in tests
 */

/**
 * File Structure (for large apps)
 *
 * stores/
 *   slices/
 *     auth-slice.ts    - createAuthSlice
 *     ui-slice.ts      - createUiSlice
 *     cart-slice.ts    - createCartSlice
 *     settings-slice.ts - createSettingsSlice
 *   app-store.ts      - Combine all slices
 */

/**
 * Advanced: Slice Dependencies
 *
 * If one slice needs to access another:
 *
 * const createAuthSlice: StateCreator<AppStore> = (set, get) => ({
 *   login: (user, token) => {
 *     set({ user, token })
 *
 *     // Access cart slice
 *     get().clearCart() // Clear cart after login
 *   },
 * })
 *
 * Note: Be careful with circular dependencies
 * Keep slices as independent as possible
 */
