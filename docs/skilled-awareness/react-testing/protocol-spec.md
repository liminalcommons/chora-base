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

**Decision Rationale** (from RT-019-DEV):
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

## Test Patterns and Examples

### Pattern 1: Component Test

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

### Pattern 4: Integration Test

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

**End of Protocol Specification**
