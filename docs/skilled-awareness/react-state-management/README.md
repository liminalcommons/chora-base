# SAP-023: React State Management Patterns

**SAP ID**: SAP-023
**Version**: 1.0.0
**TanStack Query Version**: 5.x
**Zustand Version**: 4.x
**React Hook Form Version**: 7.x
**Research Foundation**: RT-019-SYNTHESIS (Q4 2024 - Q1 2025)

---

## Quick Start (5 minutes)

```bash
# Install state management libraries
pnpm add @tanstack/react-query@5
pnpm add @tanstack/react-query-devtools -D
pnpm add zustand@4
pnpm add react-hook-form@7 @hookform/resolvers zod

# Create Query Provider
cat > src/app/providers/query-provider.tsx <<'EOF'
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: { staleTime: 60 * 1000, retry: 3 },
    },
  }))

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools />}
    </QueryClientProvider>
  )
}
EOF

# Wrap app with provider
echo "// app/layout.tsx
import { QueryProvider } from './providers/query-provider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}"

# Use in components
echo "// Server State (TanStack Query)
const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then(r => r.json()),
})

// Client State (Zustand)
const { theme, setTheme } = useThemeStore()

// Form State (React Hook Form)
const { register, handleSubmit } = useForm()"
```

**Expected outcome**: Three-pillar state management setup complete in 5 minutes.

---

## What Is It?

SAP-023 provides **production-ready state management** for React 19 using the **three-pillar architecture**: TanStack Query for server state, Zustand for client state, and React Hook Form for form state.

### Purpose

- **Three-Pillar Architecture**: Separate server, client, and form state (70% reduction in state bugs)
- **Server State (TanStack Query)**: API data, caching, background refetching, optimistic updates
- **Client State (Zustand)**: UI state, theme, preferences, minimal boilerplate
- **Form State (React Hook Form)**: Validation with Zod, performance, dynamic fields
- **Research-Backed**: RT-019 analysis (85-90% time reduction vs Redux/Context)

### How It Works

1. **Install** TanStack Query, Zustand, React Hook Form
2. **Setup** QueryProvider in root layout
3. **Classify** state type (server, client, or form)
4. **Use** appropriate tool for each state type
5. **Integrate** with Next.js 15 Server Components and Actions

---

## When to Use

### ✅ Use React State Management (SAP-023) When

- **Server Data**: Fetching from APIs, need caching and refetching (use TanStack Query)
- **UI State**: Theme, sidebar, modals, preferences (use Zustand)
- **Forms**: User input, validation, error handling (use React Hook Form)
- **Global State Needed**: Share state across components (TanStack Query or Zustand)
- **Performance Critical**: Minimize re-renders, optimize network calls
- **Complex State**: Multi-source data, dependencies, derived values

### ❌ Don't Use When

- **Local State Only**: Single component state (use `useState`)
- **Props Sufficient**: Parent-child communication (use props)
- **Static Data**: Constants, configuration (use module exports)
- **Server Components Only**: No client state needed (Next.js 15 RSC)

---

## Key Features

### Three-Pillar Architecture

**Pillar 1: Server State (TanStack Query)**
- API data fetching and caching
- Background refetching (stale-while-revalidate)
- Optimistic updates for mutations
- Automatic retry logic (exponential backoff)
- Devtools for debugging

**Pillar 2: Client State (Zustand)**
- UI state (theme, sidebar, modals)
- Minimal boilerplate (3-5 lines per store)
- Middleware (persist to localStorage, devtools)
- TypeScript support out-of-box
- No Provider wrapper required

**Pillar 3: Form State (React Hook Form)**
- Uncontrolled inputs (better performance)
- Validation with Zod schemas
- Error handling per field
- Dynamic fields (add/remove)
- Multi-step wizards

**RT-019 Finding**: This separation reduces state-related bugs by 70%.

### TanStack Query v5 Features

**Data Fetching**:
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
  staleTime: 60 * 1000,  // Fresh for 1 minute
})
```

**Mutations**:
```tsx
const mutation = useMutation({
  mutationFn: (newUser) => fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(newUser),
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] })
  },
})
```

**Optimistic Updates**:
```tsx
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newUser) => {
    await queryClient.cancelQueries({ queryKey: ['users', userId] })
    const previousUser = queryClient.getQueryData(['users', userId])

    queryClient.setQueryData(['users', userId], newUser)

    return { previousUser }
  },
  onError: (err, newUser, context) => {
    queryClient.setQueryData(['users', userId], context.previousUser)
  },
})
```

**Infinite Queries** (pagination):
```tsx
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: ({ pageParam = 0 }) => fetchProjects(pageParam),
  getNextPageParam: (lastPage) => lastPage.nextCursor,
})
```

### Zustand v4 Features

**Basic Store**:
```tsx
import { create } from 'zustand'

interface ThemeStore {
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
}

export const useThemeStore = create<ThemeStore>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}))

// Use in components
const { theme, setTheme } = useThemeStore()
```

**Persist Middleware** (localStorage):
```tsx
import { persist } from 'zustand/middleware'

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'theme-storage' }
  )
)
```

**Immer Middleware** (immutable updates):
```tsx
import { immer } from 'zustand/middleware/immer'

export const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],
    addTodo: (text) => set((state) => {
      state.todos.push({ id: Date.now(), text, done: false })
    }),
  }))
)
```

**Selectors** (optimize re-renders):
```tsx
// ❌ BAD: Re-renders on any theme store change
const store = useThemeStore()

// ✅ GOOD: Re-renders only when theme changes
const theme = useThemeStore((state) => state.theme)
```

### React Hook Form v7 Features

**Basic Form**:
```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Must be 8+ characters'),
})

type FormData = z.infer<typeof schema>

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = (data: FormData) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  )
}
```

**Server Actions Integration** (Next.js 15):
```tsx
'use client'
import { useForm } from 'react-hook-form'
import { createUser } from './actions'

export function SignupForm() {
  const { register, handleSubmit } = useForm()

  const onSubmit = async (data) => {
    const result = await createUser(data)
    if (result.success) {
      // Handle success
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* form fields */}
    </form>
  )
}
```

**Dynamic Fields**:
```tsx
import { useFieldArray } from 'react-hook-form'

export function TodoListForm() {
  const { control, register } = useForm({
    defaultValues: { todos: [{ text: '' }] },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'todos',
  })

  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`todos.${index}.text`)} />
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ text: '' })}>Add Todo</button>
    </form>
  )
}
```

---

## Quick Reference

### State Classification Decision Tree

```
Is the data from an API/server?
  ✅ YES → Use TanStack Query (server state)
  ❌ NO → Continue

Is it form data (user input)?
  ✅ YES → Use React Hook Form (form state)
  ❌ NO → Continue

Is it UI state (theme, sidebar, modal)?
  ✅ YES → Use Zustand (client state)
  ❌ NO → Use useState (local component state)
```

### TanStack Query Patterns

**Basic Query**:
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['resource', id],
  queryFn: () => fetchResource(id),
})
```

**Mutation**:
```tsx
const mutation = useMutation({
  mutationFn: createResource,
  onSuccess: () => queryClient.invalidateQueries(['resources']),
})
```

**Prefetch**:
```tsx
await queryClient.prefetchQuery({
  queryKey: ['resource', id],
  queryFn: () => fetchResource(id),
})
```

### Zustand Patterns

**Basic Store**:
```tsx
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))
```

**Persist**:
```tsx
const useStore = create(
  persist((set) => ({ /* store */ }), { name: 'storage-key' })
)
```

**Selector**:
```tsx
const count = useStore((state) => state.count)  // Only re-render when count changes
```

### React Hook Form Patterns

**Basic Form**:
```tsx
const { register, handleSubmit, formState: { errors } } = useForm()
```

**With Zod**:
```tsx
const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema),
})
```

**Dynamic Fields**:
```tsx
const { fields, append, remove } = useFieldArray({ control, name: 'items' })
```

---

## Integration with Other SAPs

### SAP-020 (React Foundation)
- **Link**: TypeScript strict mode for type-safe state
- **How**: TanStack Query, Zustand, RHF use TypeScript generics
- **Benefit**: Compile-time errors for state misuse

### SAP-021 (React Testing)
- **Link**: Test state management with MSW + testing patterns
- **How**: Mock API responses, test optimistic updates, form validation
- **Benefit**: Integration tests for state workflows

### SAP-024 (React Styling)
- **Link**: Zustand for theme state (light/dark mode)
- **How**: Store theme in Zustand, persist to localStorage
- **Benefit**: Consistent theme across app reload

### SAP-033 (React Authentication)
- **Link**: TanStack Query for user session, Zustand for auth state
- **How**: Query current user, cache in TanStack Query, store tokens in Zustand
- **Benefit**: Automatic refetch on window focus, logout across tabs

### SAP-034 (React Database Integration)
- **Link**: TanStack Query for database queries (Prisma, Drizzle)
- **How**: Server Actions as mutationFn, invalidate queries on success
- **Benefit**: Optimistic updates, automatic cache invalidation

---

## Success Metrics

### Initial Setup (<5 minutes)
- ✅ **Dependencies Installed**: TanStack Query, Zustand, React Hook Form
- ✅ **Provider Setup**: QueryProvider in root layout
- ✅ **First Query Works**: Data fetching with useQuery
- ✅ **Devtools Installed**: React Query Devtools in development

### Code Quality
- ✅ **State Separation**: Server (TanStack Query), Client (Zustand), Form (RHF)
- ✅ **Type Safety**: TypeScript generics for all state
- ✅ **No Global Redux**: Zero Redux boilerplate (85-90% time savings)
- ✅ **No Context Hell**: Zero nested Context providers

### Performance Targets
- ✅ **Caching**: <100ms for cached data (vs 500ms+ network)
- ✅ **Optimistic Updates**: <50ms perceived latency for mutations
- ✅ **Form Re-renders**: <10 re-renders for 20-field form (vs 200+ controlled)
- ✅ **Bundle Size**: <50 KB combined (TanStack Query + Zustand + RHF)

### Adoption Indicators
- ✅ **Server State**: 100% API data uses TanStack Query (not useState)
- ✅ **Client State**: 100% UI state uses Zustand (not Context)
- ✅ **Form State**: 100% forms use React Hook Form (not controlled inputs)
- ✅ **No Mixing**: Zero cases of API data in Zustand

---

## Troubleshooting

### Problem 1: "QueryClient is not defined" error

**Symptom**: Error when using useQuery in components

**Cause**: Missing QueryProvider wrapper

**Fix**: Wrap app with QueryProvider in root layout
```tsx
// app/layout.tsx
import { QueryProvider } from './providers/query-provider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
```

---

### Problem 2: Zustand store not persisting to localStorage

**Symptom**: State resets on page reload despite persist middleware

**Cause**: Not using persist middleware correctly

**Fix**: Wrap store creator with persist
```tsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useStore = create<Store>()(  // Note the extra ()
  persist(
    (set) => ({ /* store */ }),
    { name: 'storage-key' }
  )
)
```

---

### Problem 3: Form validation not working

**Symptom**: Form submits even with invalid data

**Cause**: Not using zodResolver or schema errors

**Fix**: Add zodResolver to useForm
```tsx
import { zodResolver } from '@hookform/resolvers/zod'

const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema),  // Connect Zod schema
})
```

**Verify**: Check errors object
```tsx
const { formState: { errors } } = useForm()
console.log(errors)  // Should show validation errors
```

---

### Problem 4: useQuery infinite re-renders

**Symptom**: Component re-renders continuously with useQuery

**Cause**: Query key dependency changes on every render

**Fix**: Memoize dependencies
```tsx
// ❌ BAD: Object created on every render
const { data } = useQuery({
  queryKey: ['users', { filter: 'active' }],  // New object each time
})

// ✅ GOOD: Stable primitive dependencies
const filter = 'active'
const { data } = useQuery({
  queryKey: ['users', filter],
})

// ✅ GOOD: Memoized object
const filters = useMemo(() => ({ status: 'active' }), [])
const { data } = useQuery({
  queryKey: ['users', filters],
})
```

---

### Problem 5: Zustand store not updating in other components

**Symptom**: Store changes in one component don't reflect in others

**Cause**: Creating multiple store instances

**Fix**: Export single store instance
```tsx
// ❌ BAD: Creating new store each import
export const useStore = () => create(/* store */)

// ✅ GOOD: Single instance
export const useStore = create(/* store */)
```

---

## Learn More

### Documentation

- **[Capability Charter](capability-charter.md)**: Problem statement, solution design, success criteria
- **[Protocol Spec](protocol-spec.md)**: Complete technical specification (TanStack Query, Zustand, RHF)
- **[Awareness Guide](awareness-guide.md)**: Detailed workflows, state patterns, examples
- **[Adoption Blueprint](adoption-blueprint.md)**: Step-by-step installation and setup
- **[Ledger](ledger.md)**: Adoption tracking, version history, active deployments

### Official Resources

- **[TanStack Query Documentation](https://tanstack.com/query)**: Complete guide and API reference
- **[Zustand Documentation](https://zustand-demo.pmnd.rs)**: Examples and patterns
- **[React Hook Form Documentation](https://react-hook-form.com)**: Form patterns and validation
- **[Zod Documentation](https://zod.dev)**: Schema validation library

### Related SAPs

- **[SAP-020 (react-foundation)](../react-foundation/)**: TypeScript strict mode baseline
- **[SAP-021 (react-testing)](../react-testing/)**: Test state management
- **[SAP-024 (react-styling)](../react-styling/)**: Theme state with Zustand
- **[SAP-033 (react-authentication)](../react-authentication/)**: User session state
- **[SAP-034 (react-database-integration)](../react-database-integration/)**: Database queries

### Research Foundation

- **RT-019-SYNTHESIS**: State management patterns analysis (85-90% time reduction vs Redux, 70% bug reduction)

---

## Version History

- **1.0.0** (2025-11-09): Initial SAP-023 release
  - Three-pillar architecture (Server, Client, Form state)
  - TanStack Query v5 for server state (caching, refetching, optimistic updates)
  - Zustand v4 for client state (minimal boilerplate, middleware)
  - React Hook Form v7 + Zod for form state (validation, performance)
  - RT-019 research foundation (85-90% time reduction, 70% bug reduction)
  - Integration with 5 SAPs (Foundation, Testing, Styling, Auth, Database)
  - Next.js 15 Server Components and Actions integration
  - Research-backed patterns from RT-019-SYNTHESIS

---

**Next Steps**:
1. Read [adoption-blueprint.md](adoption-blueprint.md) for installation instructions
2. Install dependencies: `pnpm add @tanstack/react-query zustand react-hook-form @hookform/resolvers zod`
3. Create QueryProvider and wrap root layout
4. Start with server state (TanStack Query) for API data
5. Add client state (Zustand) for UI state
6. Use React Hook Form for forms with Zod validation
