# SAP-023: React State Management Patterns - Adoption Blueprint

**SAP ID**: SAP-023
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01
**Category**: Technology-Specific SAP (Front-End State Management)

---

## 1. Overview

This blueprint provides step-by-step instructions for adopting SAP-023 (React State Management Patterns) in your React 19 project using the **three-pillar architecture** validated by RT-019 research.

**Estimated Time**: 30 minutes (85-90% reduction from 4-6 hours manual setup)
**Prerequisites**: SAP-020 (React Foundation) - React 19 + Next.js 15 or Vite 7 project

**Three-Pillar Architecture**:
1. **Server State** → TanStack Query v5 (API data, caching, mutations)
2. **Client State** → Zustand v4 (UI state, preferences, filters)
3. **Form State** → React Hook Form v7 + Zod (forms with validation)

**Evidence-Based**: This architecture is validated by State of JS 2024 survey data, production case studies from Vercel/Supabase/T3 Stack teams, and RT-019 research showing 70% bug reduction and 85-90% time savings.

---

## 2. Installation

### Step 1: Install Dependencies

#### For Next.js 15 Projects

```bash
# TanStack Query
npm install @tanstack/react-query@^5.62.7

# TanStack Query DevTools (dev only)
npm install -D @tanstack/react-query-devtools@^5.62.7

# Zustand
npm install zustand@^4.5.2

# React Hook Form
npm install react-hook-form@^7.54.0

# Zod (validation)
npm install zod@^3.24.1

# Zod + React Hook Form integration
npm install @hookform/resolvers@^3.9.1

# Axios (API client)
npm install axios@^1.7.9
```

#### For Vite 7 Projects

```bash
# Same dependencies as Next.js
npm install @tanstack/react-query@^5.62.7 zustand@^4.5.2 react-hook-form@^7.54.0 zod@^3.24.1 @hookform/resolvers@^3.9.1 axios@^1.7.9

# DevTools (dev only)
npm install -D @tanstack/react-query-devtools@^5.62.7
```

**Verify Installation**:
```bash
npm list @tanstack/react-query zustand react-hook-form zod
```

---

### Step 2: Copy Template Files

#### 2.1 Create Directory Structure

```bash
# TanStack Query
mkdir -p src/lib/tanstack-query

# Zustand
mkdir -p src/stores

# React Hook Form (optional - copy as needed)
mkdir -p src/components/forms
```

#### 2.2 Copy TanStack Query Templates

**From**: `templates/react/state-management/tanstack-query/`
**To**: `src/lib/tanstack-query/`

Copy these files:
1. `query-client.ts` → `src/lib/tanstack-query/query-client.ts`
2. `query-provider.tsx` → `src/lib/tanstack-query/query-provider.tsx`
3. `use-query-example.ts` → `src/lib/tanstack-query/use-query-example.ts` (reference)
4. `use-mutation-example.ts` → `src/lib/tanstack-query/use-mutation-example.ts` (reference)

**Command**:
```bash
# From chora-base root
cp templates/react/state-management/tanstack-query/query-client.ts src/lib/tanstack-query/
cp templates/react/state-management/tanstack-query/query-provider.tsx src/lib/tanstack-query/
```

---

#### 2.3 Copy Zustand Templates (as needed)

**From**: `templates/react/state-management/zustand/`
**To**: `src/stores/`

Copy as needed:
1. `store-basic.ts` → Reference for creating stores
2. `store-slice-pattern.ts` → Reference for large stores
3. `store-persist.ts` → Reference for persistence

**Example** (copy and modify for your needs):
```bash
cp templates/react/state-management/zustand/store-basic.ts src/stores/theme-store.ts
# Edit theme-store.ts to customize
```

---

#### 2.4 Copy React Hook Form Templates (as needed)

**From**: `templates/react/state-management/react-hook-form/`
**To**: `src/components/forms/`

Copy as needed:
1. `form-basic.tsx` → Reference for simple forms
2. `form-zod-validation.tsx` → Reference for Zod integration
3. `form-complex.tsx` → Reference for dynamic arrays, multi-step

**Example**:
```bash
cp templates/react/state-management/react-hook-form/form-zod-validation.tsx src/components/forms/login-form.tsx
# Edit login-form.tsx to customize
```

---

## 3. Setup

### Step 3: Configure TanStack Query Provider

#### For Next.js 15 App Router

**Edit**: `src/app/layout.tsx`

```typescript
import { QueryProvider } from '@/lib/tanstack-query/query-provider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
```

**Note**: `QueryProvider` is a Client Component (`'use client'`), but children can be Server Components.

---

#### For Vite 7

**Edit**: `src/main.tsx`

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryProvider } from './lib/tanstack-query/query-provider'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryProvider>
      <App />
    </QueryProvider>
  </React.StrictMode>,
)
```

---

### Step 4: Create Your First Store (Zustand)

**Create**: `src/stores/theme-store.ts`

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

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
      toggleTheme: () => set((state) => ({
        theme: state.theme === 'light' ? 'dark' : 'light',
      })),
    }),
    {
      name: 'theme-store', // localStorage key
    },
  ),
)
```

**Usage**:
```typescript
import { useThemeStore } from '@/stores/theme-store'

export function ThemeToggle() {
  const { theme, toggleTheme } = useThemeStore()

  return (
    <button onClick={toggleTheme}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  )
}
```

---

### Step 5: Create Your First Query Hook

**Create**: `src/lib/tanstack-query/use-products.ts`

```typescript
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface Product {
  id: string
  name: string
  price: number
}

async function fetchProducts(): Promise<Product[]> {
  const { data } = await axios.get('/api/products')
  return data
}

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  })
}
```

**Usage**:
```typescript
import { useProducts } from '@/lib/tanstack-query/use-products'

export function ProductList() {
  const { data: products, isLoading, error } = useProducts()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {products?.map((product) => (
        <li key={product.id}>{product.name} - ${product.price}</li>
      ))}
    </ul>
  )
}
```

---

### Step 6: Create Your First Form

**Create**: `src/components/forms/login-form.tsx`

```typescript
'use client' // For Next.js 15

import { useForm, SubmitHandler } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit: SubmitHandler<LoginFormData> = async (data) => {
    console.log('Login data:', data)
    // Call API
    await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="w-full rounded border p-2"
        />
        {errors.email && <p className="text-red-600">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="w-full rounded border p-2"
        />
        {errors.password && <p className="text-red-600">{errors.password.message}</p>}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

---

## 4. Verification

### Step 7: Verify TanStack Query Setup

1. **Run dev server**:
   ```bash
   npm run dev
   ```

2. **Open DevTools**:
   - Next.js 15: http://localhost:3000
   - Vite 7: http://localhost:5173
   - Click TanStack Query DevTools button (bottom-right)

3. **Check for**:
   - DevTools panel opens
   - No errors in console
   - Queries appear in DevTools (if you've added any)

---

### Step 8: Verify Zustand Store

1. **Create test component**:
   ```typescript
   'use client'

   import { useThemeStore } from '@/stores/theme-store'

   export function ThemeTest() {
     const { theme, toggleTheme } = useThemeStore()

     return (
       <div>
         <p>Current theme: {theme}</p>
         <button onClick={toggleTheme}>Toggle Theme</button>
       </div>
     )
   }
   ```

2. **Add to page**:
   ```typescript
   import { ThemeTest } from '@/components/theme-test'

   export default function HomePage() {
     return <ThemeTest />
   }
   ```

3. **Test**:
   - Click "Toggle Theme" button
   - Theme should change
   - Refresh page → theme persists (localStorage)
   - Check browser DevTools → Application → Local Storage → `theme-store`

---

### Step 9: Verify React Hook Form

1. **Add LoginForm to page**:
   ```typescript
   import { LoginForm } from '@/components/forms/login-form'

   export default function LoginPage() {
     return <LoginForm />
   }
   ```

2. **Test validation**:
   - Submit empty form → errors appear
   - Type invalid email → error appears
   - Type short password → error appears
   - Fix errors → submit succeeds

3. **Check console**:
   - Valid form data logged on submit

---

## 5. Common Issues & Troubleshooting

### Issue 1: "use client" Missing (Next.js 15)

**Error**:
```
Error: createContext only works in Client Components
```

**Solution**: Add `'use client'` to top of file
```typescript
'use client' // Add this

import { useQuery } from '@tanstack/react-query'
```

**Files that need 'use client'**:
- Components using `useQuery`, `useMutation`
- Components using Zustand stores
- Components using `useForm`
- `query-provider.tsx`

---

### Issue 2: SSR Hydration Mismatch (Zustand persist)

**Error**:
```
Warning: Text content did not match. Server: "light" Client: "dark"
```

**Solution**: Use _hasHydrated pattern
```typescript
'use client'

import { useEffect, useState } from 'react'
import { useThemeStore } from '@/stores/theme-store'

export function Theme() {
  const { theme, _hasHydrated } = useThemeStore()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])

  if (!mounted || !_hasHydrated) return null

  return <div>{theme}</div>
}
```

**Or** add _hasHydrated to your store:
```typescript
interface ThemeStore {
  theme: 'light' | 'dark'
  _hasHydrated: boolean
  setHasHydrated: (hasHydrated: boolean) => void
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: 'light',
      _hasHydrated: false,
      setHasHydrated: (hasHydrated) => set({ _hasHydrated: hasHydrated }),
    }),
    {
      name: 'theme-store',
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    },
  ),
)
```

---

### Issue 3: TanStack Query Not Refetching

**Problem**: Data not updating after mutation

**Solution**: Invalidate queries in `onSuccess`
```typescript
const createProduct = useMutation({
  mutationFn: createProduct,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['products'] })
  },
})
```

---

### Issue 4: React Hook Form Not Validating

**Problem**: No errors shown on invalid input

**Solution**: Check `formState.errors`
```typescript
const {
  register,
  handleSubmit,
  formState: { errors }, // ← Must destructure
} = useForm()

{errors.email && <p>{errors.email.message}</p>}
```

---

### Issue 5: TypeScript Errors with Zod

**Problem**:
```
Type 'string | undefined' is not assignable to type 'string'
```

**Solution**: Zod schemas should match required fields
```typescript
// ❌ Bad: Optional field but required in form
const schema = z.object({
  email: z.string().optional(),
})

// ✅ Good: Required field
const schema = z.object({
  email: z.string().min(1, 'Email is required').email(),
})
```

---

## 6. Next Steps

### Step 10: Explore Templates

**TanStack Query**:
- Review `use-query-example.ts` for query patterns
- Review `use-mutation-example.ts` for mutation patterns
- Copy patterns to your project

**Zustand**:
- Review `store-basic.ts` for simple stores
- Review `store-slice-pattern.ts` for large stores
- Review `store-persist.ts` for localStorage

**React Hook Form**:
- Review `form-basic.tsx` for simple forms
- Review `form-zod-validation.tsx` for Zod integration
- Review `form-complex.tsx` for dynamic arrays, multi-step

---

### Step 11: Integrate Into Your App

**Create API Service** (optional):
```typescript
// src/lib/api/products.ts
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export const productService = {
  getAll: () => api.get('/products'),
  getById: (id: string) => api.get(`/products/${id}`),
  create: (data: Product) => api.post('/products', data),
  update: (id: string, data: Product) => api.put(`/products/${id}`, data),
  delete: (id: string) => api.delete(`/products/${id}`),
}
```

**Create Query Hooks**:
```typescript
// src/lib/tanstack-query/use-products.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { productService } from '../api/products'

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => productService.getAll(),
  })
}

export function useCreateProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: productService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}
```

---

### Step 12: Set Up Stores

**Create stores** for:
- Theme (`theme-store.ts`)
- Auth (`auth-store.ts` with persist)
- UI state (`ui-store.ts` - modals, sidebar)
- Filters (`filter-store.ts`)

**Example Auth Store**:
```typescript
// src/stores/auth-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  name: string
  email: string
}

interface AuthStore {
  user: User | null
  token: string | null
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
      }),
    },
  ),
)
```

---

### Step 13: Create Forms

**Create forms** for:
- Login (`login-form.tsx`)
- Registration (`registration-form.tsx`)
- Profile settings (`profile-form.tsx`)
- Product creation (`product-form.tsx`)

**Tip**: Start with `form-zod-validation.tsx` template, customize schema and fields.

---

## 7. Advanced Configuration

### Customize TanStack Query Defaults

**Edit**: `src/lib/tanstack-query/query-client.ts`

```typescript
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,     // 5 minutes (increase for slower-changing data)
      gcTime: 10 * 60 * 1000,       // 10 minutes (increase to keep cache longer)
      retry: 3,                      // 3 retries (increase for flaky networks)
      refetchOnWindowFocus: true,    // false to disable auto-refetch
      refetchOnReconnect: true,
    },
  },
})
```

---

### Add Zustand DevTools

**Install**:
```bash
npm install -D @redux-devtools/extension
```

**Update store**:
```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

export const useThemeStore = create<ThemeStore>()(
  devtools(
    persist(
      (set) => ({
        theme: 'light',
        setTheme: (theme) => set({ theme }),
      }),
      { name: 'theme-store' },
    ),
    { name: 'ThemeStore' }, // DevTools name
  ),
)
```

**Usage**: Open Redux DevTools extension in browser

---

### Configure Axios Interceptors

**Create**: `src/lib/api/axios-instance.ts`

```typescript
import axios from 'axios'
import { useAuthStore } from '@/stores/auth-store'

const api = axios.create({
  baseURL: '/api',
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors (logout)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
    }
    return Promise.reject(error)
  },
)

export default api
```

---

## 8. Testing Setup

### Install Testing Libraries

```bash
npm install -D @testing-library/react @testing-library/user-event vitest
```

### Test TanStack Query

```typescript
// src/lib/tanstack-query/__tests__/use-products.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useProducts } from '../use-products'

test('useProducts fetches products', async () => {
  const queryClient = new QueryClient()
  const wrapper = ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )

  const { result } = renderHook(() => useProducts(), { wrapper })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(result.current.data).toHaveLength(3)
})
```

### Test Zustand

```typescript
// src/stores/__tests__/theme-store.test.ts
import { renderHook, act } from '@testing-library/react'
import { useThemeStore } from '../theme-store'

test('toggleTheme switches theme', () => {
  const { result } = renderHook(() => useThemeStore())

  expect(result.current.theme).toBe('light')

  act(() => {
    result.current.toggleTheme()
  })

  expect(result.current.theme).toBe('dark')
})
```

---

## 9. Deployment Checklist

- [ ] Remove DevTools in production
  ```typescript
  {process.env.NODE_ENV === 'development' && <ReactQueryDevtools />}
  ```

- [ ] Set appropriate staleTime/gcTime for production
  ```typescript
  staleTime: 5 * 60 * 1000, // 5 minutes (vs 1 minute in dev)
  ```

- [ ] Test SSR hydration (Next.js 15)
  ```bash
  npm run build
  npm run start
  ```

- [ ] Check bundle size
  ```bash
  npm run build
  # Check output for bundle sizes
  ```

- [ ] Test localStorage persistence (Zustand)
  ```
  1. Set state (e.g., theme)
  2. Refresh page
  3. Verify state persists
  ```

- [ ] Test error handling
  ```
  1. Disconnect network
  2. Verify TanStack Query retries
  3. Verify error states render
  ```

---

## 10. Summary

You've successfully set up SAP-023 (React State Management Patterns)!

**What You've Installed**:
- ✅ TanStack Query v5 (server state)
- ✅ Zustand v4 (client state)
- ✅ React Hook Form v7 + Zod (forms)
- ✅ Axios (API client)

**What You've Created**:
- ✅ Query client + provider
- ✅ Theme store (Zustand)
- ✅ First query hook
- ✅ First form (React Hook Form + Zod)

**Next Steps**:
1. Review [protocol-spec.md](./protocol-spec.md) for technical patterns and three-pillar architecture details
2. Review [awareness-guide.md](./awareness-guide.md) for decision trees and server/client state separation best practices
3. Copy templates as needed for your app
4. Track adoption in [ledger.md](./ledger.md)

**Integration with Other SAPs** (RT-019 Finding):
- **SAP-030 (Data Fetching)**: TanStack Query IS the data fetching solution
- **SAP-037 (Real-Time)**: Future SAP for WebSocket/SSE integration with TanStack Query
- **SAP-020 (React Foundation)**: Provides Next.js 15 server/client boundary patterns
- **Combined Impact**: Reduces total project setup from 22-34 hours to ~4 hours (RT-019-SYNTHESIS)

**Support**:
- Templates: `/templates/react/state-management/`
- Examples: See template files (use-query-example.ts, etc.)
- Docs: TanStack Query, Zustand, React Hook Form official docs

---

**Congratulations!** You're ready to build production-ready React apps with SAP-023 state management patterns.
