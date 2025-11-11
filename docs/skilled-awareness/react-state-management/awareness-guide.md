# SAP-023: React State Management Patterns - Awareness Guide

**SAP ID**: SAP-023
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01
**Category**: Technology-Specific SAP (Front-End State Management)

---

## 1. Purpose

This guide helps developers:
- **Choose the right tool** for each type of state (server/client/form)
- **Avoid common mistakes** that cause bugs and performance issues
- **Understand when NOT to use** each tool
- **Learn real-world use cases** with examples

**Core Philosophy**: Different state types require different tools. Mixing server and client state causes 30-40% of state-related bugs.

---

## 2. Quick Decision Trees

### Decision Tree 1: Which Tool Should I Use?

```
START: I need to manage state
│
├─ Is it data from an API/server?
│  ├─ YES → Use TanStack Query (Server State - Pillar 1)
│  └─ NO
│     │
│     ├─ Is it form data (user input)?
│     │  ├─ YES → Use React Hook Form + Zod (Form State - Pillar 3)
│     │  └─ NO
│     │     │
│     │     ├─ Should it be in the URL (shareable, bookmarkable)?
│     │     │  ├─ YES → Use URL State (useSearchParams + router.push)
│     │     │  └─ NO
│     │     │     │
│     │     │     ├─ Is it UI state (theme, sidebar, filters)?
│     │     │     │  ├─ YES
│     │     │     │  │  └─ Multiple components need it?
│     │     │     │  │     ├─ YES → Use Zustand (Client State - Pillar 2)
│     │     │     │  │     └─ NO → Use useState (Local Component State)
│     │     │     │  └─ NO → Use useState
```

**RT-019 Enhancement**: Added URL state layer for filters, pagination, and sort order (from RT-019-SYNTHESIS three-pillar architecture + URL state pattern).

### Decision Tree 2: TanStack Query vs Zustand vs Context

```
I have state that multiple components need
│
├─ Where does the data come from?
│  ├─ API/Server → TanStack Query (Server State)
│  ├─ User Input (forms) → React Hook Form
│  └─ Local/Browser → Continue
│
├─ Does the data become stale (can change on server)?
│  ├─ YES (needs refetching) → TanStack Query
│  └─ NO (always current) → Continue
│
├─ Do I need caching/background refetching?
│  ├─ YES (reduce network calls) → TanStack Query
│  └─ NO (UI state) → Continue
│
├─ How many components need this state?
│  ├─ 1-2 components (same subtree) → React Context
│  ├─ 3+ components (different subtrees) → Zustand
│  └─ 1 component only → useState
│
├─ Does state need to persist (localStorage)?
│  ├─ YES (user preferences, auth) → Zustand with persist middleware
│  └─ NO (temporary UI state) → Zustand or Context
```

**RT-019 Enhancement**: Clear separation between server state (TanStack Query) and client state (Zustand/Context), with Context as lightweight alternative for localized state sharing (from RT-019-APP patterns).

### Decision Tree 3: Form Library vs useState

```
I need to handle user input
│
├─ Is it a form (1+ fields with validation)?
│  ├─ YES → React Hook Form
│  └─ NO
│     │
│     ├─ Is it a single search input?
│     │  ├─ YES → useState + TanStack Query for search
│     │  └─ NO → useState
```

---

## 3. TanStack Query Awareness

### 3.1 When to Use TanStack Query

✅ **Use TanStack Query for**:

1. **API Data** (GET requests)
   ```typescript
   // ✅ Good: Fetching products from API
   const { data: products } = useQuery({
     queryKey: ['products'],
     queryFn: fetchProducts,
   })
   ```

2. **Data that becomes stale**
   ```typescript
   // ✅ Good: User profile (can change on server)
   const { data: user } = useQuery({
     queryKey: ['users', userId],
     queryFn: () => fetchUser(userId),
     staleTime: 60 * 1000, // Fresh for 1 minute
   })
   ```

3. **Data shared across components**
   ```typescript
   // ✅ Good: Multiple components need same product
   function ProductCard({ id }) {
     const { data } = useQuery({ queryKey: ['products', id], ... })
   }

   function ProductDetails({ id }) {
     const { data } = useQuery({ queryKey: ['products', id], ... })
     // Same query key → shared cache (1 request)
   }
   ```

4. **Real-time data** (polling, live updates)
   ```typescript
   // ✅ Good: Dashboard with live metrics
   const { data } = useQuery({
     queryKey: ['metrics'],
     queryFn: fetchMetrics,
     refetchInterval: 5000, // Poll every 5 seconds
   })
   ```

5. **Mutations** (POST/PUT/DELETE)
   ```typescript
   // ✅ Good: Create/update/delete operations
   const createProduct = useMutation({
     mutationFn: createProduct,
     onSuccess: () => {
       queryClient.invalidateQueries({ queryKey: ['products'] })
     },
   })
   ```

---

### 3.2 When NOT to Use TanStack Query

❌ **Don't use TanStack Query for**:

1. **UI State** (theme, sidebar, modals)
   ```typescript
   // ❌ Bad: Using TanStack Query for UI state
   const { data: theme } = useQuery({
     queryKey: ['theme'],
     queryFn: () => localStorage.getItem('theme'),
   })

   // ✅ Good: Use Zustand
   const theme = useThemeStore((state) => state.theme)
   ```

2. **Form State**
   ```typescript
   // ❌ Bad: Managing form with TanStack Query
   const { data: formData } = useQuery({ queryKey: ['form'], ... })

   // ✅ Good: Use React Hook Form
   const { register, handleSubmit } = useForm()
   ```

3. **Synchronous Local State**
   ```typescript
   // ❌ Bad: Overkill for simple counter
   const { data: count } = useQuery({
     queryKey: ['count'],
     queryFn: () => 0,
   })

   // ✅ Good: Use useState
   const [count, setCount] = useState(0)
   ```

4. **Static Data** (doesn't change)
   ```typescript
   // ❌ Bad: Constants don't need caching
   const { data: COUNTRIES } = useQuery({
     queryKey: ['countries'],
     queryFn: () => COUNTRY_LIST,
   })

   // ✅ Good: Import directly
   import { COUNTRY_LIST } from './constants'
   ```

---

### 3.2.5 Optimistic Updates for Instant UX

✅ **Use Optimistic Updates for**:

1. **Like/Unlike Actions** (instant feedback)
   ```typescript
   const likeMutation = useMutation({
     mutationFn: likePost,
     onMutate: async (postId) => {
       await queryClient.cancelQueries({ queryKey: ['posts', postId] })
       const previousPost = queryClient.getQueryData(['posts', postId])

       queryClient.setQueryData(['posts', postId], (old) => ({
         ...old,
         liked: true,
         likeCount: (old?.likeCount || 0) + 1
       }))

       return { previousPost }
     },
     onError: (err, postId, context) => {
       queryClient.setQueryData(['posts', postId], context.previousPost)
     }
   })
   ```

2. **Cart Updates** (instant UX critical for e-commerce)
3. **Todo Toggle** (simple boolean state)
4. **Follow/Unfollow** (social interactions)

**RT-019 Finding**: Optimistic updates improve perceived performance by 40% and reduce user frustration in poor network conditions (from RT-019-DATA research).

**When NOT to Use**:
- Financial transactions (wait for server confirmation)
- Irreversible actions (account deletion)
- Complex server-side validation

---

### 3.3 Common TanStack Query Pitfalls

#### Pitfall 1: Wrong Query Key

❌ **Bad**: Same key for different data
```typescript
// Both queries use same key → cache collision
const { data: product1 } = useQuery({
  queryKey: ['products'], // Same key!
  queryFn: () => fetchProduct(1),
})

const { data: product2 } = useQuery({
  queryKey: ['products'], // Same key!
  queryFn: () => fetchProduct(2),
})
```

✅ **Good**: Include parameters in query key
```typescript
const { data: product1 } = useQuery({
  queryKey: ['products', 1], // Different key
  queryFn: () => fetchProduct(1),
})

const { data: product2 } = useQuery({
  queryKey: ['products', 2], // Different key
  queryFn: () => fetchProduct(2),
})
```

---

#### Pitfall 2: Not Using Query Keys as Dependency Array

❌ **Bad**: Query key doesn't match dependencies
```typescript
const { data } = useQuery({
  queryKey: ['products'], // Missing filters in key
  queryFn: () => fetchProducts({ category, priceRange }), // Uses filters
})
// Bug: Changing filters doesn't trigger new query
```

✅ **Good**: Include all dependencies in query key
```typescript
const { data } = useQuery({
  queryKey: ['products', { category, priceRange }], // All dependencies
  queryFn: () => fetchProducts({ category, priceRange }),
})
// Changing filters → new query key → refetch
```

---

#### Pitfall 3: Forgetting to Invalidate After Mutation

❌ **Bad**: Create product but list doesn't update
```typescript
const createProduct = useMutation({
  mutationFn: createProduct,
  // Missing onSuccess → list stays stale
})
```

✅ **Good**: Invalidate queries to refetch
```typescript
const createProduct = useMutation({
  mutationFn: createProduct,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['products'] })
  },
})
```

---

#### Pitfall 4: Over-Fetching in Loops

❌ **Bad**: Query inside map (N queries for N items)
```typescript
function ProductList({ productIds }) {
  return productIds.map(id => (
    <ProductCard key={id} id={id} />
  ))
}

function ProductCard({ id }) {
  const { data } = useQuery({ queryKey: ['products', id], ... })
  // 100 products → 100 requests
}
```

✅ **Good**: Fetch all at once
```typescript
function ProductList({ productIds }) {
  const { data: products } = useQuery({
    queryKey: ['products', productIds],
    queryFn: () => fetchProductsByIds(productIds),
  })
  // 1 request for all products
}
```

---

## 4. Zustand Awareness

### 4.1 When to Use Zustand

✅ **Use Zustand for**:

1. **Theme/Appearance**
   ```typescript
   const useThemeStore = create((set) => ({
     theme: 'light',
     toggleTheme: () => set((state) => ({
       theme: state.theme === 'light' ? 'dark' : 'light'
     })),
   }))
   ```

2. **UI State** (modals, sidebars, tooltips)
   ```typescript
   const useUiStore = create((set) => ({
     sidebarOpen: false,
     modalOpen: false,
     toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
   }))
   ```

3. **Filters/Pagination** (client-side)
   ```typescript
   const useFilterStore = create((set) => ({
     category: null,
     priceRange: [0, 1000],
     page: 1,
     setCategory: (category) => set({ category }),
     resetFilters: () => set({ category: null, priceRange: [0, 1000], page: 1 }),
   }))
   ```

4. **User Preferences** (language, timezone, layout)
   ```typescript
   const usePreferencesStore = create(persist(
     (set) => ({
       language: 'en',
       timezone: 'UTC',
       setLanguage: (language) => set({ language }),
     }),
     { name: 'preferences' },
   ))
   ```

5. **Auth State** (user, token - with persist)
   ```typescript
   const useAuthStore = create(persist(
     (set) => ({
       user: null,
       token: null,
       login: (user, token) => set({ user, token }),
       logout: () => set({ user: null, token: null }),
     }),
     { name: 'auth-store' },
   ))
   ```

---

### 4.2 When NOT to Use Zustand

❌ **Don't use Zustand for**:

1. **API Data**
   ```typescript
   // ❌ Bad: Fetching API data into Zustand
   const useStore = create((set) => ({
     products: [],
     fetchProducts: async () => {
       const data = await fetch('/api/products')
       set({ products: data })
     },
   }))

   // ✅ Good: Use TanStack Query
   const { data: products } = useQuery({
     queryKey: ['products'],
     queryFn: fetchProducts,
   })
   ```

2. **Form State**
   ```typescript
   // ❌ Bad: Managing form with Zustand
   const useFormStore = create((set) => ({
     email: '',
     password: '',
     setEmail: (email) => set({ email }),
   }))

   // ✅ Good: Use React Hook Form
   const { register, handleSubmit } = useForm()
   ```

3. **Single-Component State**
   ```typescript
   // ❌ Bad: Global store for local state
   const useCounterStore = create((set) => ({
     count: 0,
     increment: () => set((state) => ({ count: state.count + 1 })),
   }))

   // Only used in one component
   function Counter() {
     const { count, increment } = useCounterStore()
   }

   // ✅ Good: Use useState
   function Counter() {
     const [count, setCount] = useState(0)
   }
   ```

---

### 4.3 Common Zustand Pitfalls

#### Pitfall 1: Not Using Selectors

❌ **Bad**: Re-renders on ANY state change
```typescript
const useStore = create((set) => ({
  theme: 'light',
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

function ThemeDisplay() {
  const store = useStore() // Re-renders when count changes!
  return <div>{store.theme}</div>
}
```

✅ **Good**: Use selector (only re-render when theme changes)
```typescript
function ThemeDisplay() {
  const theme = useStore((state) => state.theme) // Only re-renders when theme changes
  return <div>{theme}</div>
}
```

---

#### Pitfall 2: Persisting Everything

❌ **Bad**: Persist UI state (should reset on refresh)
```typescript
const useStore = create(persist(
  (set) => ({
    user: null,
    sidebarOpen: false, // Don't persist!
    modalOpen: false,   // Don't persist!
  }),
  { name: 'app-store' },
))
```

✅ **Good**: Only persist user data
```typescript
const useStore = create(persist(
  (set) => ({
    user: null,
    sidebarOpen: false,
    modalOpen: false,
  }),
  {
    name: 'app-store',
    partialize: (state) => ({ user: state.user }), // Only persist user
  },
))
```

---

#### Pitfall 3: SSR Hydration Mismatch

❌ **Bad**: Render persisted state immediately
```typescript
function Theme() {
  const theme = useThemeStore((state) => state.theme)
  return <div>{theme}</div> // SSR: 'light', Client: 'dark' → MISMATCH
}
```

✅ **Good**: Use _hasHydrated flag
```typescript
function Theme() {
  const { theme, _hasHydrated } = useThemeStore()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])

  if (!mounted || !_hasHydrated) return null

  return <div>{theme}</div>
}
```

---

## 5. React Hook Form Awareness

### 5.1 When to Use React Hook Form

✅ **Use React Hook Form for**:

1. **All Forms** (login, registration, checkout, etc.)
   ```typescript
   const { register, handleSubmit } = useForm()

   <form onSubmit={handleSubmit(onSubmit)}>
     <input {...register('email')} />
   </form>
   ```

2. **Forms with Validation**
   ```typescript
   const { register, handleSubmit, formState: { errors } } = useForm({
     resolver: zodResolver(schema),
   })
   ```

3. **Dynamic Forms** (add/remove fields)
   ```typescript
   const { fields, append, remove } = useFieldArray({
     control,
     name: 'emails',
   })
   ```

4. **Multi-Step Forms**
   ```typescript
   const { trigger } = useForm({ mode: 'onBlur' })

   const nextStep = async () => {
     const isValid = await trigger(['email', 'password'])
     if (isValid) setStep(step + 1)
   }
   ```

---

### 5.2 When NOT to Use React Hook Form

❌ **Don't use React Hook Form for**:

1. **Single Search Input** (use useState + TanStack Query)
   ```typescript
   // ❌ Bad: Overkill for single input
   const { register } = useForm()
   <input {...register('search')} />

   // ✅ Good: useState
   const [query, setQuery] = useState('')
   <input value={query} onChange={(e) => setQuery(e.target.value)} />
   ```

2. **Non-Form Inputs** (toggles, sliders outside forms)
   ```typescript
   // ❌ Bad: Not a form
   const { register } = useForm()
   <input type="checkbox" {...register('darkMode')} />

   // ✅ Good: Zustand
   const { darkMode, toggleDarkMode } = useStore()
   <input type="checkbox" checked={darkMode} onChange={toggleDarkMode} />
   ```

---

### 5.3 Common React Hook Form Pitfalls

#### Pitfall 1: Using Controlled Inputs

❌ **Bad**: Controlled inputs (50-70% slower)
```typescript
const [email, setEmail] = useState('')

<input value={email} onChange={(e) => setEmail(e.target.value)} />
```

✅ **Good**: Uncontrolled inputs (React Hook Form)
```typescript
const { register } = useForm()

<input {...register('email')} />
```

---

#### Pitfall 2: Validation Without Zod

❌ **Bad**: Manual validation (verbose, not type-safe)
```typescript
const { register } = useForm()

<input
  {...register('email', {
    required: 'Required',
    pattern: { value: /^[A-Z0-9._%+-]+@.../, message: 'Invalid' },
    minLength: { value: 3, message: 'Too short' },
  })}
/>
```

✅ **Good**: Zod schema (reusable, type-safe)
```typescript
const schema = z.object({
  email: z.string().email('Invalid email'),
})

const { register } = useForm({ resolver: zodResolver(schema) })

<input {...register('email')} />
```

---

#### Pitfall 3: Not Using valueAsNumber

❌ **Bad**: Age is string (should be number)
```typescript
const { register, handleSubmit } = useForm()

const onSubmit = (data) => {
  console.log(data.age) // "25" (string)
}

<input type="number" {...register('age')} />
```

✅ **Good**: Convert to number
```typescript
<input type="number" {...register('age', { valueAsNumber: true })} />

const onSubmit = (data) => {
  console.log(data.age) // 25 (number)
}
```

---

## 6. Real-World Use Cases

### Use Case 1: E-Commerce Product Page

**Requirements**:
- Fetch products from API
- Filter by category/price (client-side)
- Add to cart (mutation)
- Theme toggle

**Solution**:
```typescript
// Server state: Products
const { data: products } = useQuery({
  queryKey: ['products', { category, priceRange }],
  queryFn: () => fetchProducts({ category, priceRange }),
})

// Client state: Filters
const { category, priceRange, setCategory } = useFilterStore()

// Client state: Theme
const { theme, toggleTheme } = useThemeStore()

// Mutation: Add to cart
const addToCart = useMutation({
  mutationFn: (productId) => postAddToCart(productId),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['cart'] })
  },
})
```

**State Breakdown**:
- **TanStack Query**: Products (server data), cart (server data)
- **Zustand**: Filters (client state), theme (client state)

---

### Use Case 2: User Registration Flow

**Requirements**:
- Multi-step form (3 steps)
- Email, password, personal info, address
- Validate each step before proceeding

**Solution**:
```typescript
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  firstName: z.string().min(1),
  address: z.string().min(1),
})

const { register, trigger, handleSubmit } = useForm({
  resolver: zodResolver(schema),
  mode: 'onBlur',
})

const [step, setStep] = useState(1)

const nextStep = async () => {
  const fields = step === 1 ? ['email', 'password'] : ['firstName']
  const isValid = await trigger(fields)
  if (isValid) setStep(step + 1)
}

const onSubmit = (data) => {
  registerMutation.mutate(data)
}
```

**State Breakdown**:
- **React Hook Form + Zod**: Form validation (all steps)
- **TanStack Query (mutation)**: Submit registration

---

### Use Case 3: Dashboard with Live Data

**Requirements**:
- Fetch metrics from API (polling every 10 seconds)
- Toggle between views (client state)
- Save user preferences (persist)

**Solution**:
```typescript
// Server state: Metrics (polling)
const { data: metrics } = useQuery({
  queryKey: ['metrics'],
  queryFn: fetchMetrics,
  refetchInterval: 10000, // Poll every 10 seconds
})

// Client state: View + Preferences (persist)
const useDashboardStore = create(persist(
  (set) => ({
    view: 'grid',
    setView: (view) => set({ view }),
  }),
  { name: 'dashboard-preferences' },
))

const { view, setView } = useDashboardStore()
```

**State Breakdown**:
- **TanStack Query**: Metrics (server data, polling)
- **Zustand (persist)**: View preference (saved to localStorage)

---

### Use Case 4: Search with Autocomplete

**Requirements**:
- Search products as user types
- Debounce to avoid excessive requests
- Show previous results during search

**Solution**:
```typescript
const [query, setQuery] = useState('')

const { data: results } = useQuery({
  queryKey: ['products', 'search', query],
  queryFn: () => searchProducts(query),
  enabled: query.length >= 3, // Only search if 3+ chars
  placeholderData: (previousData) => previousData, // Keep old results
})

<input
  value={query}
  onChange={(e) => setQuery(e.target.value)}
  placeholder="Search products..."
/>
```

**State Breakdown**:
- **useState**: Search query (single input, controlled)
- **TanStack Query**: Search results (server data, debounced by query key change)

---

## 7. Anti-Patterns to Avoid

### Anti-Pattern 1: Global State for Everything

❌ **Bad**: Everything in one global store
```typescript
const useStore = create((set) => ({
  // Server data (should be TanStack Query)
  products: [],
  user: null,

  // Form data (should be React Hook Form)
  email: '',
  password: '',

  // UI state (OK for Zustand)
  theme: 'light',
}))
```

✅ **Good**: Separate by type
```typescript
// TanStack Query: Server data
const { data: products } = useQuery({ queryKey: ['products'], ... })
const { data: user } = useQuery({ queryKey: ['user'], ... })

// React Hook Form: Form data
const { register } = useForm()

// Zustand: UI state
const { theme } = useThemeStore()
```

---

### Anti-Pattern 2: Prop Drilling Instead of Global State

❌ **Bad**: Pass theme through 5 levels
```typescript
<App theme={theme}>
  <Layout theme={theme}>
    <Sidebar theme={theme}>
      <Menu theme={theme}>
        <MenuItem theme={theme} />
      </Menu>
    </Sidebar>
  </Layout>
</App>
```

✅ **Good**: Use Zustand
```typescript
const useThemeStore = create((set) => ({
  theme: 'light',
}))

function MenuItem() {
  const theme = useThemeStore((state) => state.theme)
}
```

---

### Anti-Pattern 3: Mixing Server and Client State

❌ **Bad**: Store API data in Zustand
```typescript
const useStore = create((set) => ({
  products: [],
  fetchProducts: async () => {
    const data = await fetch('/api/products')
    set({ products: data })
  },
}))
```

**Problems**:
- No caching
- No retry logic
- No loading/error states
- Manual refetching

✅ **Good**: Use TanStack Query for server data
```typescript
const { data: products, isLoading, error } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
})
```

---

## 8. Performance Best Practices

### 8.1 TanStack Query Performance

1. **Set appropriate staleTime**
   ```typescript
   // Products change rarely → longer staleTime
   useQuery({
     queryKey: ['products'],
     queryFn: fetchProducts,
     staleTime: 5 * 60 * 1000, // 5 minutes
   })

   // User profile changes often → shorter staleTime
   useQuery({
     queryKey: ['user'],
     queryFn: fetchUser,
     staleTime: 30 * 1000, // 30 seconds
   })
   ```

2. **Use placeholderData for instant UX**
   ```typescript
   useQuery({
     queryKey: ['products', filters],
     queryFn: () => fetchProducts(filters),
     placeholderData: (previousData) => previousData, // Keep old data
   })
   ```

3. **Prefetch for faster navigation**
   ```typescript
   const prefetchProduct = (id: string) => {
     queryClient.prefetchQuery({
       queryKey: ['products', id],
       queryFn: () => fetchProduct(id),
     })
   }

   <Link to={`/products/${id}`} onMouseEnter={() => prefetchProduct(id)}>
     View Product
   </Link>
   ```

---

### 8.2 Zustand Performance

1. **Use selectors to prevent unnecessary re-renders**
   ```typescript
   // ❌ Bad: Re-renders on ANY state change
   const store = useStore()

   // ✅ Good: Only re-renders when theme changes
   const theme = useStore((state) => state.theme)
   ```

2. **Combine related state updates**
   ```typescript
   // ❌ Bad: Two updates (two re-renders)
   setCategory('electronics')
   setPriceRange([0, 500])

   // ✅ Good: One update (one re-render)
   set({ category: 'electronics', priceRange: [0, 500] })
   ```

---

### 8.3 React Hook Form Performance

1. **Use uncontrolled inputs (default)**
   ```typescript
   // ✅ Good: Uncontrolled (fast)
   const { register } = useForm()
   <input {...register('email')} />
   ```

2. **Set validation mode wisely**
   ```typescript
   // Fewer validations (faster)
   const { register } = useForm({
     mode: 'onSubmit', // Validate only on submit
   })

   // More validations (better UX, slower)
   const { register } = useForm({
     mode: 'onChange', // Validate on every change
   })
   ```

---

## 9. Migration Checklist

### Migrating from Redux to Zustand

- [ ] Remove Redux DevTools (use Zustand devtools middleware)
- [ ] Remove actions/reducers (use set() directly)
- [ ] Remove Provider (Zustand has no provider)
- [ ] Remove useSelector/useDispatch (use store hook)
- [ ] Remove combineReducers (use slice pattern)

**Before**:
```typescript
// Redux: 5 files
// actions.ts, reducer.ts, store.ts, types.ts, provider.tsx
```

**After**:
```typescript
// Zustand: 1 file
// store.ts
const useStore = create((set) => ({ ... }))
```

---

### Migrating from useState to React Hook Form

- [ ] Remove useState for form fields
- [ ] Remove onChange handlers
- [ ] Remove manual validation
- [ ] Add useForm hook
- [ ] Add Zod schema (optional but recommended)

**Before**:
```typescript
// useState: 20+ lines
const [email, setEmail] = useState('')
const [errors, setErrors] = useState({})
const handleSubmit = (e) => { /* validation */ }
```

**After**:
```typescript
// React Hook Form: 5 lines
const { register, handleSubmit } = useForm({ resolver: zodResolver(schema) })
```

---

## 10. Server/Client State Separation Best Practices

### Rule 1: Server is Source of Truth for Server State

✅ **Good**: TanStack Query manages server data
```typescript
// Server state: Products from API
const { data: products } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts
})
```

❌ **Bad**: Storing server data in client state
```typescript
// Don't store API data in Zustand!
const useStore = create((set) => ({
  products: [],
  fetchProducts: async () => {
    const data = await fetchProducts()
    set({ products: data })
  }
}))
```

**Why**: TanStack Query provides caching, background refetching, retry logic, and stale-while-revalidate. Client state (Zustand) loses all these benefits.

---

### Rule 2: Client is Source of Truth for UI State

✅ **Good**: Zustand for UI state
```typescript
const useUIStore = create((set) => ({
  theme: 'light',
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen }))
}))
```

❌ **Bad**: Using TanStack Query for UI state
```typescript
// Don't use TanStack Query for non-server state!
const { data: theme } = useQuery({
  queryKey: ['theme'],
  queryFn: () => localStorage.getItem('theme')
})
```

**Why**: UI state is synchronous, always current, and doesn't need caching/refetching. TanStack Query adds unnecessary complexity.

---

### Rule 3: Never Mix Server and Client State

✅ **Good**: Separate concerns
```typescript
// Server state
const { data: products } = useQuery({
  queryKey: ['products', { category, priceRange }],
  queryFn: () => fetchProducts({ category, priceRange })
})

// Client state (filters)
const { category, priceRange } = useFilterStore()
```

❌ **Bad**: Mixing in one store
```typescript
const useStore = create((set) => ({
  // Server state (wrong!)
  products: [],
  // Client state (ok)
  category: null,
  priceRange: [0, 1000]
}))
```

**Why**: Mixing concerns causes 30-40% of state-related bugs (RT-019 research).

---

### Rule 4: URL State for Shareable/Bookmarkable State

✅ **Good**: Filters in URL
```typescript
const searchParams = useSearchParams()
const category = searchParams.get('category')
const page = parseInt(searchParams.get('page') || '1')

// TanStack Query uses URL params in query key (automatic refetch on URL change)
const { data: products } = useQuery({
  queryKey: ['products', { category, page }],
  queryFn: () => fetchProducts({ category, page })
})
```

**Why**: URL state is shareable (copy link), bookmarkable (save filter), and SEO-friendly.

---

### Rule 5: Form State is Temporary

✅ **Good**: React Hook Form for forms
```typescript
const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema)
})

const onSubmit = (data) => {
  // Mutation to server
  createMutation.mutate(data)
  // Form cleared after submit
}
```

❌ **Bad**: Storing form state globally
```typescript
const useFormStore = create((set) => ({
  email: '',
  password: '',
  setEmail: (email) => set({ email })
}))
// Form state persists after submit (wrong!)
```

**Why**: Form state should be cleared after submission. Global state persists unnecessarily.

---

### Rule 6: Optimistic Updates for Server Mutations

✅ **Good**: Instant UI feedback
```typescript
const likeMutation = useMutation({
  mutationFn: likePost,
  onMutate: async (postId) => {
    // Instant UI update (optimistic)
    queryClient.setQueryData(['posts', postId], (old) => ({
      ...old,
      liked: true
    }))
  },
  onError: (err, postId, context) => {
    // Rollback on error
    queryClient.setQueryData(['posts', postId], context.previousPost)
  }
})
```

**Why**: Users see instant feedback (40% better perceived performance - RT-019).

---

### Decision Matrix: State Separation Summary

| State Type | Tool | Example | Persist? | Shareable? |
|------------|------|---------|----------|------------|
| **Server State** | TanStack Query | Products, users, posts | Cache (5min-10min) | No |
| **Client State** | Zustand | Theme, sidebar, modals | localStorage (optional) | No |
| **URL State** | useSearchParams | Filters, pagination, sort | URL | Yes (copy link) |
| **Form State** | React Hook Form | Login, registration | No (cleared on submit) | No |
| **Local State** | useState | Component-specific toggles | No | No |

**RT-019 Finding**: Proper state separation reduces bugs by 70% and setup time from 4-6 hours to 30 minutes (85-90% reduction).

---

## 11. Quick Reference

### When to Use Each Tool

| State Type | Tool | Example |
|-----------|------|---------|
| API data | TanStack Query | Products, users, posts |
| UI state | Zustand | Theme, sidebar, modals |
| User preferences | Zustand + persist | Language, timezone |
| Forms | React Hook Form + Zod | Login, registration, checkout |
| Auth | Zustand + persist | User, token |
| Filters | Zustand | Category, price range, pagination |
| Search | useState + TanStack Query | Single input + results |
| Cart | TanStack Query + mutations | Fetch cart, add/remove items |

---

### Bundle Size Reference

| Library | Size (gzipped) | Use Case |
|---------|---------------|----------|
| TanStack Query | 11.8KB | Server state |
| Zustand | 2.9KB | Client state |
| React Hook Form | 29.4KB | Forms |
| Zod | 13.7KB | Validation |
| **Total** | **~58KB** | Full state management |

---

## Summary

**Key Takeaways**:

1. **Separate state by type**: Server (TanStack Query) vs Client (Zustand) vs Form (RHF)
2. **Don't mix server and client state**: Causes 30-40% of bugs
3. **Use selectors**: Prevent unnecessary re-renders
4. **Persist wisely**: Only user data, not UI state
5. **Handle SSR**: Use _hasHydrated flag for Next.js 15

**Decision Framework**:
- API data → TanStack Query
- UI state (multi-component) → Zustand
- Forms → React Hook Form + Zod
- Single input → useState

**Next Steps**: See [adoption-blueprint.md](./adoption-blueprint.md) for installation, [protocol-spec.md](./protocol-spec.md) for technical details.
