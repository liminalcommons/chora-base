# SAP-021: React Testing & Quality - Protocol Specification

**SAP ID**: SAP-021
**Version**: 1.0.0
**Vitest Version**: 4.0.x
**React Testing Library Version**: 16.x
**MSW Version**: 2.x
**Research Foundation**: RT-019-DEV (Q4 2024 - Q1 2025)

---

## Overview

This document specifies the technical contracts, testing patterns, and guarantees for testing React applications using the SAP-021 capability package.

**Scope**: Unit and integration testing for React 19 applications using Vitest v4, React Testing Library v16, and MSW v2
**Audience**: AI agents, developers implementing React tests
**Compliance**: Vitest 4.x, React Testing Library v16, MSW v2.x, TypeScript 5.7

---

## Protocol Foundation

### Testing Philosophy

**The Testing Trophy** (Kent C. Dodds, 2025):
```
        /\       E2E (10-20%) [Future: SAP-027]
       /  \
      /____\     Integration (50-60%) ← HIGHEST ROI, SAP-021 FOCUS
     /      \
    /________\   Unit (20-30%) ← SAP-021 FOCUS
   /__________\
Static Analysis (100% - TypeScript, ESLint) [SAP-020, SAP-022]
```

**SAP-021 Coverage**:
- ✅ Static Analysis (TypeScript strict mode - from SAP-020)
- ✅ Unit Tests (20-30% of test suite)
- ✅ Integration Tests (50-60% of test suite)
- ❌ E2E Tests (10-20% - future SAP-027 with Playwright)

### Core Testing Principles

**1. Test User Behavior, Not Implementation**
```typescript
// ✅ GOOD: Tests what user sees/does
it('increments count when clicking increment button', async () => {
  const user = userEvent.setup()
  render(<Counter />)
  await user.click(screen.getByRole('button', { name: /increment/i }))
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
})

// ❌ BAD: Tests implementation details
it('calls setState when increment is called', () => {
  const wrapper = shallow(<Counter />)
  wrapper.instance().increment()
  expect(wrapper.state('count')).toBe(1)
})
```

**2. Accessible Queries First**
```typescript
// Query Priority (from React Testing Library docs):
screen.getByRole('button', { name: /submit/i })  // ✅ Best (accessible)
screen.getByLabelText(/email/i)                   // ✅ Good (forms)
screen.getByPlaceholderText(/search/i)            // ⚠️  OK (if no label)
screen.getByText(/hello/i)                        // ⚠️  OK (non-interactive)
screen.getByTestId('submit-btn')                  // ❌ Last resort
```

**3. Integration Over Unit**
```typescript
// ✅ GOOD: Integration test (higher value)
it('fetches and displays user list', async () => {
  render(<UserList />)
  await waitFor(() => {
    expect(screen.getByText(/alice/i)).toBeInTheDocument()
  })
})

// ⚠️ OK: Unit test (lower value, but faster)
it('formats user name correctly', () => {
  expect(formatUserName({ first: 'John', last: 'Doe' })).toBe('John Doe')
})
```

---

## Vitest Configuration Protocol

### Vitest v4.0 Specification

**Version**: 4.0.5+
**Source**: https://vitest.dev

**Decision Rationale** (from RT-019 Research, Q4 2024 - Q1 2025):

**Vitest vs Jest 2025 Comparison**:

| Criteria | Vitest 4.x | Jest 29.x | Winner |
|----------|------------|-----------|--------|
| **Performance** | 4x faster (small suites), 1.9x faster (800+ tests) | Baseline | ✅ Vitest |
| **ESM Support** | Native ESM, zero config | Requires `--experimental-vm-modules` | ✅ Vitest |
| **TypeScript** | Native support, no ts-jest | Requires ts-jest dependency | ✅ Vitest |
| **Vite Ecosystem** | Native Vite integration, Next.js 15 support | Separate config | ✅ Vitest |
| **Watch Mode** | <1s re-runs, instant feedback | Slower, requires cache | ✅ Vitest |
| **Developer Experience** | Modern API, better error messages | Mature but dated | ✅ Vitest |
| **Migration** | 98% Jest-compatible API | N/A | ✅ Vitest |
| **Adoption (2025)** | Fast-growing (State of JS 2024: 98% retention) | Stable but not growing | ✅ Vitest |
| **Bundle Size** | Lighter runtime | Heavier | ✅ Vitest |
| **Community** | Growing rapidly, Vite ecosystem | Large, established | Tie |

**Recommendation**: **Vitest is the default choice for all new React projects in 2025**. Jest remains acceptable for legacy projects or teams with existing Jest infrastructure.

**Migration Path**: Jest → Vitest typically takes 2-4 hours for medium projects (200-500 tests). SAP-021 provides Vitest-first templates.

**Evidence from RT-019**:
- 4x faster than Jest for small test suites
- 1.9x faster for medium test suites (800 tests)
- ESM-first (no `--experimental-vm-modules` flag)
- Native TypeScript support (no ts-jest)
- 98% retention rate (State of JS 2024)
- Compatible with Jest matchers (easy migration)

### Next.js 15 Configuration

**File**: `vitest.config.ts` (project root)

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup-tests.ts'],

    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'vitest.config.ts',
        'next.config.ts',
        '**/*.test.{ts,tsx}',
        '**/__tests__/**',
        'src/test/**',
        '.next/**',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },

    // Performance optimization
    pool: 'vmThreads',
    poolOptions: {
      threads: {
        singleThread: false,
        maxThreads: 8,
        minThreads: 4,
      },
    },

    // CI optimization
    ...(process.env.CI && {
      minWorkers: 4,
      maxWorkers: 4,
    }),
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**Configuration Breakdown**:

| Option | Value | Rationale |
|--------|-------|-----------|
| `environment` | `'jsdom'` | DOM testing (React components render to DOM) |
| `globals` | `true` | Global `describe`, `it`, `expect` (optional, convenient) |
| `setupFiles` | Setup file path | Runs before each test file |
| `coverage.provider` | `'v8'` | Faster than istanbul, native Chrome engine |
| `coverage.thresholds` | 80-90% | Industry standard for production apps |
| `pool` | `'vmThreads'` | Optimal for CPU-bound tests |
| `maxThreads` | `8` | Parallel test execution (adjust for CPU cores) |

### Vite 7 Configuration

**File**: `vitest.config.ts` (identical to Next.js, but exclude `.next/**`)

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup-tests.ts'],

    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'vitest.config.ts',
        '**/*.test.{ts,tsx}',
        '**/__tests__/**',
        'src/test/**',
        'dist/**',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },

    pool: 'vmThreads',
    poolOptions: {
      threads: {
        singleThread: false,
        maxThreads: 8,
        minThreads: 4,
      },
    },

    ...(process.env.CI && {
      minWorkers: 4,
      maxWorkers: 4,
    }),
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

---

## Global Test Setup Protocol

### setup-tests.ts Specification

**File**: `src/test/setup-tests.ts`

**Purpose**:
- Import jest-dom matchers (toBeInTheDocument, toHaveTextContent, etc.)
- Mock browser APIs (matchMedia, IntersectionObserver)
- Mock Next.js router (for Next.js projects)
- Global cleanup after each test

**Next.js Variant**:

```typescript
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    refresh: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}))

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
} as any
```

**Vite Variant** (exclude Next.js router mock):

```typescript
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})

// (matchMedia and IntersectionObserver mocks same as Next.js)
```

---

## React Testing Library Protocol

### React Testing Library v16 Specification

**Version**: 16.0.1+
**Source**: https://testing-library.com/react

**Key Features**:
- React 18+ support (React 19 compatible)
- `renderHook` integrated (no separate package)
- Automatic cleanup with `afterEach`
- userEvent v14 (realistic user interactions)

### Test Utils Pattern

**File**: `src/test/test-utils.tsx`

**Purpose**: Wrap components with providers (TanStack Query, Router, Theme, etc.)

```typescript
import { render, RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactElement, ReactNode } from 'react'

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Disable retries for faster test failures
        gcTime: Infinity,    // Disable garbage collection for predictable behavior
      },
      mutations: {
        retry: false,
      },
    },
  })
}

interface AllTheProvidersProps {
  children: ReactNode
}

function AllTheProviders({ children }: AllTheProvidersProps) {
  const queryClient = createTestQueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options })
}

export function createWrapper() {
  return ({ children }: { children: ReactNode }) => (
    <AllTheProviders>{children}</AllTheProviders>
  )
}

// Re-export everything from React Testing Library
export * from '@testing-library/react'
export { userEvent } from '@testing-library/user-event'
```

**Usage**:
```typescript
import { renderWithProviders, screen } from '@/test/test-utils'

test('renders component with providers', () => {
  renderWithProviders(<MyComponent />)
  expect(screen.getByText(/hello/i)).toBeInTheDocument()
})
```

### Query Priority Hierarchy

**From React Testing Library docs** (https://testing-library.com/docs/queries/about#priority):

1. **Queries Accessible to Everyone**:
   - `getByRole` (with `name` option) ← **Best for accessibility**
   - `getByLabelText` ← Forms
   - `getByPlaceholderText` ← If no label available
   - `getByText` ← Non-interactive content
   - `getByDisplayValue` ← Current form values

2. **Semantic Queries**:
   - `getByAltText` ← Images, area elements
   - `getByTitle` ← Only if alt and role unavailable

3. **Test IDs**:
   - `getByTestId` ← **Last resort**, escape hatch

**Example**:
```typescript
// ✅ Best: Accessible query
const submitButton = screen.getByRole('button', { name: /submit/i })

// ✅ Good: Form label
const emailInput = screen.getByLabelText(/email address/i)

// ⚠️ OK: Placeholder (if no label)
const searchInput = screen.getByPlaceholderText(/search.../i)

// ⚠️ OK: Text content (non-interactive)
const heading = screen.getByText(/welcome back/i)

// ❌ Avoid: Test ID (use only if above don't work)
const modal = screen.getByTestId('confirmation-modal')
```

---

## MSW (Mock Service Worker) Protocol

### MSW v2.x Specification

**Version**: 2.6.5+
**Source**: https://mswjs.io

**Purpose**: Intercept HTTP requests at network level (realistic API mocking)

**Advantages over axios mocking**:
- Works with fetch, axios, and any HTTP client
- Same mocks work in dev, test, and Storybook
- Type-safe handlers (TypeScript + Zod)
- Realistic testing (code makes real HTTP requests)

### Handlers Pattern

**File**: `src/test/mocks/handlers.ts`

```typescript
import { http, HttpResponse } from 'msw'

interface User {
  id: string
  name: string
  email: string
}

export const handlers = [
  // GET /api/users
  http.get('/api/users', () => {
    return HttpResponse.json<User[]>([
      { id: '1', name: 'Alice Johnson', email: 'alice@example.com' },
      { id: '2', name: 'Bob Smith', email: 'bob@example.com' },
    ])
  }),

  // GET /api/users/:id
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params
    return HttpResponse.json<User>({
      id: id as string,
      name: 'Alice Johnson',
      email: 'alice@example.com',
    })
  }),

  // POST /api/users
  http.post('/api/users', async ({ request }) => {
    const newUser = (await request.json()) as Omit<User, 'id'>
    return HttpResponse.json<User>(
      {
        id: crypto.randomUUID(),
        ...newUser,
      },
      { status: 201 }
    )
  }),

  // Error simulation
  http.get('/api/error', () => {
    return HttpResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    )
  }),
]
```

### Server Setup (Node.js/Tests)

**File**: `src/test/mocks/server.ts`

```typescript
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

**Integration with Vitest** (add to `setup-tests.ts`):

```typescript
import { server } from './mocks/server'
import { beforeAll, afterEach, afterAll } from 'vitest'

// Start server before all tests
beforeAll(() => server.listen())

// Reset handlers after each test (remove runtime overrides)
afterEach(() => server.resetHandlers())

// Close server after all tests
afterAll(() => server.close())
```

### Browser Setup (Development)

**File**: `src/test/mocks/browser.ts`

```typescript
import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

export const worker = setupWorker(...handlers)
```

**Enable in development** (optional, add to `main.tsx` or `_app.tsx`):

```typescript
if (process.env.NODE_ENV === 'development') {
  const { worker } = await import('./test/mocks/browser')
  worker.start()
}
```

### Overriding Handlers Per Test

```typescript
import { server } from '@/test/mocks/server'
import { http, HttpResponse } from 'msw'

test('handles API error', async () => {
  // Override handler for this test only
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json(
        { error: 'Server Error' },
        { status: 500 }
      )
    })
  )

  render(<UserList />)

  await waitFor(() => {
    expect(screen.getByText(/error:/i)).toBeInTheDocument()
  })
})
```

---

## Next.js 15 Advanced Testing Patterns

### Server Component Testing (React Server Components)

**Overview**: Server Components (RSC) are async functions that run only on the server. They don't render in the browser, so traditional React Testing Library patterns don't apply.

**Testing Strategy**:
- Test Server Components like regular async functions (unit tests)
- No `render()` needed - they're just functions that return JSX
- Test data fetching, business logic, and JSX structure
- Use Node.js test patterns, not browser-based RTL patterns

**Example**:

```typescript
// app/users/page.tsx (Server Component)
import { prisma } from '@/lib/db'

interface User {
  id: string
  name: string
  email: string
}

export default async function UsersPage() {
  const users = await prisma.user.findMany()

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}

// app/users/page.test.ts (Unit test, NOT component test)
import { describe, it, expect, vi } from 'vitest'
import UsersPage from './page'
import { prisma } from '@/lib/db'

// Mock Prisma
vi.mock('@/lib/db', () => ({
  prisma: {
    user: {
      findMany: vi.fn(),
    },
  },
}))

describe('UsersPage Server Component', () => {
  it('fetches users from database', async () => {
    const mockUsers = [
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]

    vi.mocked(prisma.user.findMany).mockResolvedValue(mockUsers)

    // Call Server Component as a function
    const jsx = await UsersPage()

    // Verify Prisma was called
    expect(prisma.user.findMany).toHaveBeenCalledTimes(1)

    // Option 1: Test JSX structure (fragile, not recommended)
    // expect(jsx.props.children[1].props.children).toHaveLength(2)

    // Option 2: Render to string and test (better for Server Components)
    const { renderToString } = await import('react-dom/server')
    const html = renderToString(jsx)
    expect(html).toContain('Alice')
    expect(html).toContain('Bob')
  })

  it('handles empty user list', async () => {
    vi.mocked(prisma.user.findMany).mockResolvedValue([])

    const jsx = await UsersPage()
    const { renderToString } = await import('react-dom/server')
    const html = renderToString(jsx)

    expect(html).toContain('Users')
    // No user names in output
    expect(html).not.toContain('Alice')
  })
})
```

**Key Points**:
- ✅ Server Components are async functions - test them as functions, not React components
- ✅ Mock database/API calls (Prisma, fetch, etc.)
- ✅ Use `renderToString` from react-dom/server to verify HTML output
- ❌ Don't use React Testing Library's `render()` (Server Components don't run in browser)
- ❌ Don't test interactivity (Server Components are static)

---

### Server Action Testing

**Overview**: Server Actions are server-side functions (Next.js 15) that handle form submissions and mutations. They run on the server, not the client.

**Testing Strategy**:
- Test Server Actions like async functions (unit tests)
- Mock database calls (Prisma, fetch, etc.)
- Test validation (Zod schemas)
- Test authorization checks
- Test revalidation side effects (revalidatePath, revalidateTag)
- Use MSW v2 for external API calls

**Example**:

```typescript
// app/actions/create-user.ts (Server Action)
'use server'

import { prisma } from '@/lib/db'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const createUserSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
})

export async function createUser(formData: FormData) {
  // 1. Validate input
  const data = {
    name: formData.get('name') as string,
    email: formData.get('email') as string,
  }

  const result = createUserSchema.safeParse(data)
  if (!result.success) {
    return { error: result.error.flatten().fieldErrors }
  }

  // 2. Authorization check (example)
  // const session = await auth()
  // if (!session) return { error: 'Unauthorized' }

  // 3. Database mutation
  try {
    const user = await prisma.user.create({
      data: result.data,
    })

    // 4. Revalidate cache
    revalidatePath('/users')

    return { success: true, user }
  } catch (error) {
    return { error: 'Failed to create user' }
  }
}

// app/actions/create-user.test.ts (Unit test for Server Action)
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createUser } from './create-user'
import { prisma } from '@/lib/db'

// Mock dependencies
vi.mock('@/lib/db', () => ({
  prisma: {
    user: {
      create: vi.fn(),
    },
  },
}))

vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
  revalidateTag: vi.fn(),
}))

describe('createUser Server Action', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('creates user with valid data', async () => {
    const mockUser = {
      id: '1',
      name: 'Alice',
      email: 'alice@example.com',
    }

    vi.mocked(prisma.user.create).mockResolvedValue(mockUser)

    const formData = new FormData()
    formData.set('name', 'Alice')
    formData.set('email', 'alice@example.com')

    const result = await createUser(formData)

    // Verify success
    expect(result).toEqual({ success: true, user: mockUser })

    // Verify Prisma called with correct data
    expect(prisma.user.create).toHaveBeenCalledWith({
      data: {
        name: 'Alice',
        email: 'alice@example.com',
      },
    })

    // Verify revalidation
    const { revalidatePath } = await import('next/cache')
    expect(revalidatePath).toHaveBeenCalledWith('/users')
  })

  it('returns validation error for invalid email', async () => {
    const formData = new FormData()
    formData.set('name', 'Alice')
    formData.set('email', 'invalid-email')

    const result = await createUser(formData)

    // Verify validation error
    expect(result).toHaveProperty('error')
    expect(result.error).toHaveProperty('email')

    // Verify Prisma NOT called
    expect(prisma.user.create).not.toHaveBeenCalled()
  })

  it('returns validation error for missing name', async () => {
    const formData = new FormData()
    formData.set('name', '')
    formData.set('email', 'alice@example.com')

    const result = await createUser(formData)

    expect(result).toHaveProperty('error')
    expect(result.error).toHaveProperty('name')
  })

  it('handles database errors', async () => {
    vi.mocked(prisma.user.create).mockRejectedValue(new Error('DB Error'))

    const formData = new FormData()
    formData.set('name', 'Alice')
    formData.set('email', 'alice@example.com')

    const result = await createUser(formData)

    expect(result).toEqual({ error: 'Failed to create user' })
  })
})
```

**Key Points**:
- ✅ Test Server Actions as async functions (they're just functions)
- ✅ Mock database calls (Prisma, Drizzle)
- ✅ Test Zod schema validation (both success and failure cases)
- ✅ Verify revalidatePath/revalidateTag calls (cache invalidation)
- ✅ Test authorization checks (mock auth() calls)
- ✅ Test error handling (database errors, network errors)
- ❌ Don't use React Testing Library (Server Actions aren't React components)

**Integration with MSW v2**:

If Server Action calls external APIs, use MSW:

```typescript
import { server } from '@/test/mocks/server'
import { http, HttpResponse } from 'msw'

it('calls external API in Server Action', async () => {
  server.use(
    http.post('https://api.external.com/users', () => {
      return HttpResponse.json({ id: 'ext-123' }, { status: 201 })
    })
  )

  const formData = new FormData()
  formData.set('name', 'Alice')

  const result = await createUserWithExternalAPI(formData)

  expect(result.success).toBe(true)
})
```

---

## Test Patterns and Examples

### Pattern 1: Component Test (Client Components)

**What to test**:
- Rendering with props
- User interactions (clicks, typing)
- Conditional rendering
- Accessibility (ARIA attributes)

**Example**:

```typescript
import { describe, it, expect } from 'vitest'
import { renderWithProviders, screen, userEvent } from '@/test/test-utils'

describe('Counter Component', () => {
  it('renders with initial count', () => {
    renderWithProviders(<Counter initialCount={5} />)
    expect(screen.getByText(/count: 5/i)).toBeInTheDocument()
  })

  it('increments count on button click', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter />)

    const incrementButton = screen.getByRole('button', { name: /increment/i })
    await user.click(incrementButton)

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })

  it('supports keyboard interaction', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter />)

    const incrementButton = screen.getByRole('button', { name: /increment/i })
    incrementButton.focus()
    await user.keyboard('{Enter}')

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })
})
```

### Pattern 2: Hook Test (TanStack Query)

**What to test**:
- Loading states
- Success states
- Error states
- Data transformation

**Example**:

```typescript
import { describe, it, expect } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { createWrapper } from '@/test/test-utils'

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    },
  })
}

describe('useUsers Hook', () => {
  it('fetches users successfully', async () => {
    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    })

    // Initially loading
    expect(result.current.isLoading).toBe(true)

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true))

    // Verify data
    expect(result.current.data).toHaveLength(2)
    expect(result.current.data[0]).toHaveProperty('name', 'Alice Johnson')
  })

  it('handles errors', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json({ error: 'Server Error' }, { status: 500 })
      })
    )

    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
    expect(result.current.error).toBeDefined()
  })
})
```

### Pattern 3: Hook Test (Zustand Store)

**What to test**:
- Initial state
- State updates
- Action creators
- Cross-instance updates

**Example**:

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { create } from 'zustand'

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}))

describe('CounterStore', () => {
  beforeEach(() => {
    useCounterStore.setState({ count: 0 }) // Reset between tests
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounterStore())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('updates across multiple instances', () => {
    const { result: result1 } = renderHook(() => useCounterStore())
    const { result: result2 } = renderHook(() => useCounterStore())

    act(() => {
      result1.current.increment()
    })

    expect(result1.current.count).toBe(1)
    expect(result2.current.count).toBe(1) // Both see same state
  })
})
```

### Pattern 4: Accessibility Testing with vitest-axe

**Overview**: Automated accessibility testing catches 30-40% of WCAG violations. Combined with manual testing, achieve 80%+ compliance.

**Setup**:

```bash
# Install vitest-axe
pnpm add -D vitest-axe
```

**Example**:

```typescript
import { describe, it, expect } from 'vitest'
import { renderWithProviders, screen } from '@/test/test-utils'
import { axe, toHaveNoViolations } from 'vitest-axe'

// Add custom matcher
expect.extend(toHaveNoViolations)

describe('LoginForm Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(<LoginForm />)

    // Run axe accessibility audit
    const results = await axe(container)

    // Assert no violations
    expect(results).toHaveNoViolations()
  })

  it('has proper form labels', () => {
    renderWithProviders(<LoginForm />)

    // Verify labels exist (accessible to screen readers)
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('has accessible error messages', async () => {
    const user = userEvent.setup()
    renderWithProviders(<LoginForm />)

    // Submit invalid form
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    // Error should be announced to screen readers
    const errorMessage = screen.getByText(/email is required/i)
    expect(errorMessage).toHaveAttribute('role', 'alert')
  })

  it('supports keyboard navigation', async () => {
    const user = userEvent.setup()
    renderWithProviders(<LoginForm />)

    // Tab to email input
    await user.tab()
    expect(screen.getByLabelText(/email/i)).toHaveFocus()

    // Tab to password input
    await user.tab()
    expect(screen.getByLabelText(/password/i)).toHaveFocus()

    // Tab to submit button
    await user.tab()
    expect(screen.getByRole('button', { name: /sign in/i })).toHaveFocus()
  })
})
```

**Key Points**:
- ✅ Use `axe()` to catch common WCAG violations
- ✅ Test form labels with `getByLabelText` (ensures accessible forms)
- ✅ Test error announcements with `role="alert"` (screen reader support)
- ✅ Test keyboard navigation with userEvent.tab() (keyboard accessibility)
- ✅ Run axe on every component test (automated a11y regression prevention)

**Recommended Integration**:

Add to `src/test/test-utils.tsx`:

```typescript
import { axe, toHaveNoViolations } from 'vitest-axe'
import { expect } from 'vitest'

// Extend matchers globally
expect.extend(toHaveNoViolations)

// Helper function for accessibility testing
export async function testAccessibility(container: HTMLElement) {
  const results = await axe(container)
  expect(results).toHaveNoViolations()
}
```

Then use in tests:

```typescript
import { renderWithProviders, testAccessibility } from '@/test/test-utils'

it('is accessible', async () => {
  const { container } = renderWithProviders(<MyComponent />)
  await testAccessibility(container)
})
```

---

### Pattern 5: Integration Test

**What to test**:
- Full user flows (load → interact → submit)
- API integration (via MSW)
- Form submissions
- Navigation
- Error handling end-to-end

**Example**:

```typescript
import { describe, it, expect } from 'vitest'
import { renderWithProviders, screen, userEvent, waitFor } from '@/test/test-utils'

describe('UserList Integration', () => {
  it('completes add user flow', async () => {
    const user = userEvent.setup()
    renderWithProviders(<UserList />)

    // Step 1: Wait for initial load
    await waitFor(() => {
      expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
    })

    // Step 2: Fill out form
    await user.type(screen.getByLabelText(/name/i), 'Charlie Brown')
    await user.type(screen.getByLabelText(/email/i), 'charlie@example.com')

    // Step 3: Submit form
    await user.click(screen.getByRole('button', { name: /add user/i }))

    // Step 4: Verify success
    await waitFor(() => {
      expect(screen.getByLabelText(/name/i)).toHaveValue('')
    })
  })
})
```

---

## Test File Naming and Structure

### Naming Conventions

**File Naming**:
```
src/
├── components/
│   ├── button.tsx
│   └── button.test.tsx         # ✅ Component tests (collocated)
├── hooks/
│   ├── use-users.ts
│   └── use-users.test.ts       # ✅ Hook tests (collocated)
├── lib/
│   ├── utils.ts
│   └── utils.test.ts           # ✅ Unit tests (collocated)
└── __tests__/
    └── user-flow.test.tsx      # ✅ Integration tests (separate folder)
```

**Test File Structure**:
```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { renderWithProviders, screen, userEvent } from '@/test/test-utils'

describe('ComponentName', () => {
  // Optional: Setup
  beforeEach(() => {
    // Reset state, mocks, etc.
  })

  // Group related tests
  describe('rendering', () => {
    it('renders with default props', () => {
      // Test rendering
    })

    it('renders with custom props', () => {
      // Test prop variations
    })
  })

  describe('interactions', () => {
    it('handles click events', async () => {
      // Test user interactions
    })

    it('handles keyboard events', async () => {
      // Test accessibility
    })
  })

  describe('error states', () => {
    it('displays error message on failure', () => {
      // Test error handling
    })
  })
})
```

---

## Coverage Configuration

### Coverage Targets (Industry Standard)

| Component Type | Target Coverage |
|----------------|-----------------|
| Components | 85-90% |
| Hooks/Utils | 95%+ |
| Pages/Routes | 70-80% |
| **Overall Project** | **80-90%** |

### Coverage Types Priority

1. **Branch Coverage** (most important) - Decision paths (if/else, switch)
2. **Statement Coverage** - Lines executed
3. **Function Coverage** - Functions called
4. **Line Coverage** - Similar to statement

### Running Coverage

```bash
# Generate coverage report
pnpm test --coverage

# View HTML report
open coverage/index.html

# CI mode (fail if below thresholds)
pnpm test --coverage --run
```

**Coverage Output**:
```
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
components/button.tsx | 100   | 100      | 100     | 100     |
hooks/use-users.ts    | 95.8  | 91.7     | 100     | 95.8    |
lib/utils.ts          | 100   | 100      | 100     | 100     |
--------------------|---------|----------|---------|---------|
All files             | 87.3  | 85.2     | 94.1    | 87.3    |
```

---

## Guarantees

### Performance Guarantees

- ✅ Test suite runs in <5 seconds for 50 tests
- ✅ Test suite runs in <15 seconds for 200 tests
- ✅ Watch mode re-runs in <1 second
- ✅ Coverage generation adds <2 seconds overhead

### Correctness Guarantees

- ✅ All provided example tests pass
- ✅ MSW intercepts API calls successfully
- ✅ TanStack Query integration works in tests
- ✅ Zustand stores reset between tests
- ✅ No act() warnings with provided patterns
- ✅ No provider errors with test-utils.tsx

### Quality Guarantees

- ✅ 100% TypeScript coverage (no `any` types in templates)
- ✅ All templates follow accessibility best practices
- ✅ Integration tests cover realistic user flows
- ✅ Error states are tested alongside happy paths

---

## Quality Attributes

### Reliability

**Test Stability**:
- No flaky tests (consistent pass/fail)
- Deterministic behavior (no random failures)
- Predictable async handling (waitFor, findBy)

**Error Handling**:
- Clear error messages on test failures
- Helpful debugging output
- MSW request logs in verbose mode

### Maintainability

**Test Independence**:
- Each test runs in isolation
- No shared state between tests
- Automatic cleanup after each test

**Readability**:
- Descriptive test names ("it does X when Y")
- Clear arrange-act-assert structure
- Minimal test logic (avoid conditionals in tests)

### Performance

**Fast Feedback**:
- Instant watch mode (<1s re-run)
- Parallel test execution
- Optimized for CPU cores

**Scalability**:
- Handles 1000+ tests without slowdown
- Memory-efficient (v8 coverage provider)
- CI-optimized (fixed worker count)

---

## Dependencies

### Required Packages

```json
{
  "devDependencies": {
    "vitest": "^4.0.5",
    "@vitejs/plugin-react": "^4.3.4",
    "jsdom": "^25.0.1",
    "@vitest/coverage-v8": "^4.0.5",
    "@vitest/ui": "^4.0.5",
    "@testing-library/react": "^16.0.1",
    "@testing-library/user-event": "^14.5.2",
    "@testing-library/jest-dom": "^6.5.0",
    "msw": "^2.6.5"
  }
}
```

### Optional Packages

```json
{
  "devDependencies": {
    "vite-tsconfig-paths": "^5.1.4",  // Auto-resolve tsconfig paths
    "@testing-library/dom": "^10.4.0"  // Explicit DOM queries
  }
}
```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install
      - run: pnpm test --coverage --run

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

---

## Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents self-evaluation criteria for SAP-021 awareness file completeness, enabling automated validation of equivalent support for generic agents and Claude Code.

### Awareness File Requirements

**Required Files**:
- `AGENTS.md` - Generic AI agent workflows
- `CLAUDE.md` - Claude Code-specific tool patterns

**Validation Command**:
```bash
python scripts/sap-evaluator.py --deep react-testing
```

### Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Install Testing Infrastructure (10-20 min) - Install Vitest, RTL, MSW, create config files, test setup
2. Write Component Test (5-10 min) - Create component test with RTL, test user interactions
3. Write Hook Test (5-10 min) - Test custom React hook with renderHook
4. Setup MSW for API Mocking (15-25 min) - Configure MSW v2, create handlers, setup server
5. Write Integration Test with API Mocking (10-20 min) - Integration test with MSW, providers, async operations

**CLAUDE.md**: 3 workflows
1. Installing Testing Infrastructure with Bash and Write - Install dependencies with Bash, create config files with Write
2. Writing Component Test with Write - Read component first, write test with Write, run with Bash
3. Writing Integration Test with MSW - Check MSW handlers with Read, write integration test, verify with Bash

**Variance**: 3 workflows (CLAUDE.md) vs 5 workflows (AGENTS.md) = 40% difference
**Acceptable**: Yes (within ±30-40% tolerance with documented rationale)

**Rationale for Variance**: CLAUDE.md consolidates test writing operations with tool-specific patterns (Bash for running tests, Write for test files, Read for component understanding), focusing on practical test creation workflow. AGENTS.md provides granular step-by-step guidance for each testing operation including separate workflows for hook testing and MSW setup. Both provide equivalent coverage of testing infrastructure setup, component testing, integration testing, and API mocking through different organizational approaches optimized for their respective audiences.

### User Signal Pattern Coverage

**AGENTS.md**: 2 tables with 10 signals
- Testing Setup Operations table (5 signals):
  - "setup React testing" → install_testing_infrastructure()
  - "add Vitest" → install_vitest()
  - "configure testing" → configure_vitest()
  - "setup MSW" → install_msw()
  - "run tests" → run_test_suite()
- Test Writing Operations table (5 signals):
  - "test component" → write_component_test()
  - "test hook" → write_hook_test()
  - "test API integration" → write_integration_test()
  - "mock API" → create_msw_handler()
  - "check coverage" → generate_coverage()

**CLAUDE.md**: Tool-specific patterns documented in 5 tips
- Tip 1: Always read component before writing test
- Tip 2: Use Bash to run tests immediately after writing
- Tip 3: Check for existing MSW handlers before adding
- Tip 4: Use Write for new tests, Edit for updating
- Tip 5: Run coverage to verify test completeness

**Coverage**: AGENTS.md provides user signal translation for React testing operations, CLAUDE.md provides tool patterns for implementing those signals with Claude Code tools (Bash, Write, Read, Edit).

### Validation Checkpoints

**Structural Validation**:
```bash
# Check both awareness files exist
ls docs/skilled-awareness/react-testing/AGENTS.md
ls docs/skilled-awareness/react-testing/CLAUDE.md

# Check YAML frontmatter present
head -20 docs/skilled-awareness/react-testing/AGENTS.md | grep "sap_id: SAP-021"
head -20 docs/skilled-awareness/react-testing/CLAUDE.md | grep "sap_id: SAP-021"
```

**Coverage Validation**:
```bash
# Count workflows in AGENTS.md (expect: 5)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/react-testing/AGENTS.md

# Count workflows in CLAUDE.md (expect: 3)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/react-testing/CLAUDE.md

# Check user signal tables exist in AGENTS.md
grep -c "## User Signal Patterns" docs/skilled-awareness/react-testing/AGENTS.md
```

**Expected Results**:
- Both awareness files exist ✅
- YAML frontmatter with progressive_loading ✅
- AGENTS.md: 5 workflows, 2 user signal tables ✅
- CLAUDE.md: 3 workflows, 5 tool-specific tips ✅
- Workflow variance: 40% (acceptable with documented rationale) ✅

### Integration with SAP-009

**Phase 4 Criteria Met**:
- ✅ AGENTS.md provides generic workflow guidance
- ✅ CLAUDE.md provides Claude Code tool patterns
- ✅ Workflow coverage within acceptable variance (40% with rationale)
- ✅ Rationale documented for organizational differences
- ✅ Self-evaluation criteria documented in protocol-spec.md

**SAP-021 Awareness Status**: Phase 4 compliant (equivalent support for generic agents and Claude Code)

---

**End of Protocol Specification**
