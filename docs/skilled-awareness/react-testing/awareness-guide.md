# SAP-021: React Testing & Quality - Awareness Guide

**SAP ID**: SAP-021
**Version**: 1.0.0
**Last Updated**: 2025-11-01
**Status**: Active

---

## Overview

This guide provides comprehensive awareness for AI agents and developers working with the React Testing & Quality capability package (SAP-021). It covers workflows, decision trees, common pitfalls, and testing strategies for React applications.

**Audience**: AI agents (Claude Code, GPT-4, etc.), developers testing React applications
**Prerequisite SAPs**: SAP-000 (SAP Framework), SAP-020 (React Foundation)
**Complementary SAPs**: SAP-022 (Linting), SAP-005 (CI/CD), SAP-026 (Accessibility Testing)

---

## When to Use SAP-021

### Use Case 1: Testing React Applications with External APIs

**Scenario**: You're building a React app that fetches data from REST APIs, displays it in components, and allows users to create/update/delete records. You need to test these flows without hitting real APIs.

**Why SAP-021**:
- ✅ MSW v2 intercepts HTTP requests at network level (realistic mocking)
- ✅ Same mocks work in tests AND development (no duplicate code)
- ✅ Type-safe handlers with TypeScript
- ✅ Test TanStack Query integration (loading, success, error states)
- ✅ Integration tests catch real bugs (60-80% more than unit tests alone)

**Example**:
```typescript
// Component that fetches users
function UserList() {
  const { data: users, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users')
      return response.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}

// Integration test (MSW intercepts fetch automatically)
test('fetches and displays users', async () => {
  renderWithProviders(<UserList />)

  // MSW handler returns mock data
  await waitFor(() => {
    expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
  })
})
```

**Alternatives**:
- Axios mocking (less realistic, doesn't test fetch calls)
- Real API calls (slow, flaky, requires test database)

**Decision Criteria**: Use SAP-021 when you have any external API dependencies.

---

### Use Case 2: Test-Driven Development (TDD) Workflows

**Scenario**: You want to write tests before implementation (Red → Green → Refactor) to ensure code meets requirements and prevent regression.

**Why SAP-021**:
- ✅ Vitest watch mode provides instant feedback (<1s re-runs)
- ✅ React Testing Library enforces testing user behavior (not implementation)
- ✅ Clear test examples make it easy to start with TDD
- ✅ Integration tests serve as living documentation

**Example TDD Workflow**:
```typescript
// Step 1: Write failing test (RED)
test('increments counter on button click', async () => {
  const user = userEvent.setup()
  render(<Counter />)

  await user.click(screen.getByRole('button', { name: /increment/i }))
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
})
// Test fails: Counter component doesn't exist yet

// Step 2: Write minimal code to pass (GREEN)
function Counter() {
  const [count, setCount] = useState(0)
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
// Test passes

// Step 3: Refactor (REFACTOR)
function Counter() {
  const [count, setCount] = useState(0)
  const increment = useCallback(() => setCount(c => c + 1), [])
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  )
}
// Test still passes (behavior unchanged)
```

**Alternatives**:
- No tests (faster initially, slower long-term due to bugs)
- Manual testing (not repeatable, misses edge cases)

**Decision Criteria**: Use TDD when building features with clear requirements.

---

### Use Case 3: Ensuring Accessibility Compliance

**Scenario**: You need to verify that components are keyboard-navigable, screen-reader friendly, and WCAG compliant.

**Why SAP-021**:
- ✅ React Testing Library queries (getByRole, getByLabelText) enforce accessibility
- ✅ userEvent simulates real keyboard/mouse interactions
- ✅ Forces you to add ARIA labels (tests fail without them)
- ✅ Complements future SAP-026 (jest-axe integration)

**Example**:
```typescript
test('form is keyboard accessible', async () => {
  const user = userEvent.setup()
  render(<LoginForm />)

  // Tab to email input
  await user.tab()
  expect(screen.getByLabelText(/email/i)).toHaveFocus()

  // Type email
  await user.keyboard('user@example.com')

  // Tab to password input
  await user.tab()
  expect(screen.getByLabelText(/password/i)).toHaveFocus()

  // Submit with Enter
  await user.keyboard('{Enter}')

  // Verify submission
  await waitFor(() => {
    expect(screen.getByText(/welcome/i)).toBeInTheDocument()
  })
})
```

**Pitfalls if NOT using SAP-021**:
- Missing ARIA labels (screen readers can't navigate)
- Keyboard traps (can't tab to elements)
- Invisible focus indicators

**Decision Criteria**: Use SAP-021 for all user-facing components.

---

### Use Case 4: Preventing Production Regressions

**Scenario**: You're refactoring code or adding features and want confidence that existing functionality still works.

**Why SAP-021**:
- ✅ Comprehensive test suite catches 80% of regressions pre-commit
- ✅ Integration tests verify entire user flows (not just units)
- ✅ Fast feedback (5s for 50 tests) enables continuous refactoring
- ✅ Coverage reports identify untested code paths

**Example**:
```typescript
// Integration test covering full checkout flow
test('user can complete checkout', async () => {
  const user = userEvent.setup()
  render(<CheckoutPage />)

  // Step 1: Add items to cart
  await user.click(screen.getByRole('button', { name: /add to cart/i }))
  expect(screen.getByText(/1 item in cart/i)).toBeInTheDocument()

  // Step 2: Go to checkout
  await user.click(screen.getByRole('button', { name: /checkout/i }))
  expect(screen.getByText(/checkout/i)).toBeInTheDocument()

  // Step 3: Fill shipping info
  await user.type(screen.getByLabelText(/name/i), 'John Doe')
  await user.type(screen.getByLabelText(/address/i), '123 Main St')

  // Step 4: Submit order
  await user.click(screen.getByRole('button', { name: /place order/i }))

  // Step 5: Verify success
  await waitFor(() => {
    expect(screen.getByText(/order confirmed/i)).toBeInTheDocument()
  })
})

// This single test exercises:
// - Cart state management
// - Navigation
// - Form validation
// - API calls (mocked with MSW)
// - Success/error states
```

**Alternatives**:
- Manual QA testing (slow, expensive, misses edge cases)
- E2E tests only (slow, flaky, hard to debug)

**Decision Criteria**: Write integration tests for all critical user flows.

---

### Use Case 5: Testing Complex State Management

**Scenario**: You're using TanStack Query for server state and Zustand for client UI state, and need to verify they interact correctly.

**Why SAP-021**:
- ✅ test-utils.tsx provides QueryClient wrapper automatically
- ✅ Zustand stores can be reset between tests
- ✅ renderHook tests hooks in isolation
- ✅ MSW simulates realistic API responses

**Example (TanStack Query + Zustand)**:
```typescript
// Zustand store
const useUIStore = create((set) => ({
  isModalOpen: false,
  openModal: () => set({ isModalOpen: true }),
  closeModal: () => set({ isModalOpen: false }),
}))

// Component using both stores
function UserModal() {
  const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers })
  const { isModalOpen, closeModal } = useUIStore()

  if (!isModalOpen) return null

  return (
    <div role="dialog">
      <h2>Users</h2>
      <ul>{users?.map(u => <li key={u.id}>{u.name}</li>)}</ul>
      <button onClick={closeModal}>Close</button>
    </div>
  )
}

// Integration test
test('modal displays fetched users', async () => {
  const user = userEvent.setup()

  // Setup: Open modal
  useUIStore.getState().openModal()

  render(<UserModal />)

  // Verify modal renders
  expect(screen.getByRole('dialog')).toBeInTheDocument()

  // Wait for users to load (MSW mocks API)
  await waitFor(() => {
    expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
  })

  // Close modal
  await user.click(screen.getByRole('button', { name: /close/i }))

  // Verify modal closes
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
})
```

**Decision Criteria**: Test state integration whenever multiple stores interact.

---

## Anti-Patterns (What NOT to Do)

### Anti-Pattern 1: Testing Implementation Details

**Problem**: Tests break when refactoring, even though user behavior is unchanged.

**Example (BAD)**:
```typescript
// ❌ Tests internal state
test('updates count state', () => {
  const wrapper = shallow(<Counter />)
  wrapper.instance().setState({ count: 5 })
  expect(wrapper.state('count')).toBe(5)
})

// ❌ Tests component methods
test('calls increment method', () => {
  const wrapper = shallow(<Counter />)
  const spy = jest.spyOn(wrapper.instance(), 'increment')
  wrapper.instance().increment()
  expect(spy).toHaveBeenCalled()
})
```

**Why It's Bad**:
- Tests break when switching from class to functional components
- Tests break when renaming methods
- Tests pass even if UI is broken

**Solution (GOOD)**:
```typescript
// ✅ Tests user-visible behavior
test('increments count when clicking button', async () => {
  const user = userEvent.setup()
  render(<Counter />)

  await user.click(screen.getByRole('button', { name: /increment/i }))
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
})
```

**Principle**: If the user can't see it, don't test it.

---

### Anti-Pattern 2: Using getByTestId as Primary Query

**Problem**: Test IDs couple tests to implementation, obscure accessibility issues.

**Example (BAD)**:
```typescript
// ❌ Relies on test IDs
test('renders submit button', () => {
  render(<Form />)
  expect(screen.getByTestId('submit-button')).toBeInTheDocument()
})
```

**Why It's Bad**:
- Doesn't verify button is accessible
- Doesn't test actual text
- Encourages adding non-production attributes

**Solution (GOOD)**:
```typescript
// ✅ Uses accessible query
test('renders submit button', () => {
  render(<Form />)
  expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument()
})
```

**Principle**: Prefer getByRole → getByLabelText → getByText → getByTestId (last resort).

---

### Anti-Pattern 3: Not Waiting for Async Updates

**Problem**: Tests fail intermittently or pass incorrectly due to async timing.

**Example (BAD)**:
```typescript
// ❌ No waiting for async state
test('displays users', () => {
  render(<UserList />)
  expect(screen.getByText(/alice/i)).toBeInTheDocument()  // Fails - data not loaded yet
})

// ❌ Using setTimeout
test('displays users', async () => {
  render(<UserList />)
  await new Promise(resolve => setTimeout(resolve, 1000))  // Brittle
  expect(screen.getByText(/alice/i)).toBeInTheDocument()
})
```

**Why It's Bad**:
- Flaky tests (sometimes pass, sometimes fail)
- Hardcoded timeouts are brittle

**Solution (GOOD)**:
```typescript
// ✅ Use findBy (combines getBy + waitFor)
test('displays users', async () => {
  render(<UserList />)
  expect(await screen.findByText(/alice/i)).toBeInTheDocument()
})

// ✅ Or use waitFor explicitly
test('displays users', async () => {
  render(<UserList />)
  await waitFor(() => {
    expect(screen.getByText(/alice/i)).toBeInTheDocument()
  })
})
```

**Principle**: Always await async operations (findBy, waitFor, userEvent).

---

### Anti-Pattern 4: Mocking Too Much

**Problem**: Over-mocking makes tests unrealistic and misses integration bugs.

**Example (BAD)**:
```typescript
// ❌ Mocking fetch directly
vi.mock('fetch', () => ({
  fetch: vi.fn().mockResolvedValue({
    json: () => Promise.resolve([{ id: '1', name: 'Alice' }]),
  }),
}))

test('fetches users', async () => {
  render(<UserList />)
  expect(await screen.findByText(/alice/i)).toBeInTheDocument()
})
```

**Why It's Bad**:
- Doesn't test actual fetch calls
- Doesn't test error handling
- Doesn't test response parsing

**Solution (GOOD)**:
```typescript
// ✅ Use MSW for network-level mocking
// MSW handler in setup-tests.ts
http.get('/api/users', () => {
  return HttpResponse.json([{ id: '1', name: 'Alice' }])
})

test('fetches users', async () => {
  render(<UserList />)
  expect(await screen.findByText(/alice/i)).toBeInTheDocument()
})
```

**Principle**: Mock at the network boundary (MSW), not internal functions.

---

### Anti-Pattern 5: Writing Only Unit Tests

**Problem**: High unit test coverage doesn't prevent integration failures.

**Example (BAD)**:
```typescript
// ❌ Only testing individual functions
test('formatUserName formats correctly', () => {
  expect(formatUserName('John', 'Doe')).toBe('John Doe')
})

test('fetchUsers calls API', () => {
  const spy = vi.spyOn(api, 'fetchUsers')
  fetchUsers()
  expect(spy).toHaveBeenCalled()
})

test('UserListItem renders user', () => {
  render(<UserListItem user={{ id: '1', name: 'Alice' }} />)
  expect(screen.getByText(/alice/i)).toBeInTheDocument()
})
```

**Why It's Bad**:
- Units work individually but fail when integrated
- Doesn't test user flows
- Misses API contract mismatches

**Solution (GOOD)**:
```typescript
// ✅ Integration test covering full flow
test('user list loads and displays users', async () => {
  render(<UserList />)

  // Loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument()

  // Success state (MSW returns data)
  await waitFor(() => {
    expect(screen.getByText(/alice/i)).toBeInTheDocument()
    expect(screen.getByText(/bob/i)).toBeInTheDocument()
  })

  // Tests:
  // - API call
  // - Response parsing
  // - State management
  // - Component rendering
  // - All in one realistic flow
})
```

**Principle**: Follow the testing trophy (50-60% integration, 20-30% unit).

---

## Decision Trees

### Decision Tree 1: What Type of Test to Write?

```
START: I need to test...
│
├─ A single utility function (no React, no state)
│  → UNIT TEST
│  → Example: formatDate, parseJSON, validateEmail
│  → File: lib/utils.test.ts
│
├─ A custom React hook
│  ├─ Hook uses TanStack Query or external data?
│  │  → INTEGRATION TEST with renderHook + createWrapper()
│  │  → Example: useUsers, useAuth, usePosts
│  │  → File: hooks/use-users.test.ts
│  │
│  └─ Hook is pure (no external deps)?
│     → UNIT TEST with renderHook
│     → Example: useToggle, useLocalStorage
│     → File: hooks/use-toggle.test.ts
│
├─ A React component
│  ├─ Component makes API calls or uses TanStack Query?
│  │  → INTEGRATION TEST with renderWithProviders + MSW
│  │  → Example: UserList, PostDetail
│  │  → File: components/user-list.test.tsx
│  │
│  ├─ Component is complex with multiple child components?
│  │  → INTEGRATION TEST covering full component tree
│  │  → Example: CheckoutForm, Dashboard
│  │  → File: components/checkout-form.test.tsx
│  │
│  └─ Component is simple presentational (just props → UI)?
│     → UNIT TEST with render
│     → Example: Button, Avatar, Badge
│     → File: components/button.test.tsx
│
└─ A complete user flow (login → dashboard → action)
   → INTEGRATION TEST in __tests__ directory
   → Example: User authentication flow, checkout flow
   → File: __tests__/checkout-flow.test.tsx
```

---

### Decision Tree 2: Which React Testing Library Query to Use?

```
START: I need to query for an element
│
├─ Is it an interactive element (button, link, input)?
│  → screen.getByRole('button', { name: /submit/i })
│  → Most accessible, tests ARIA compliance
│
├─ Is it a form input with a label?
│  → screen.getByLabelText(/email address/i)
│  → Ensures accessible form
│
├─ Is it a form input WITHOUT a label? (edge case)
│  ├─ Can you add a label?
│  │  → YES: Add label, use getByLabelText
│  └─ No label possible? (design limitation)
│     → screen.getByPlaceholderText(/search.../i)
│
├─ Is it non-interactive text content (heading, paragraph)?
│  → screen.getByText(/welcome back/i)
│  → Use for headings, paragraphs, static text
│
├─ Is it an image?
│  → screen.getByAltText(/profile picture/i)
│  → Ensures alt text for accessibility
│
├─ None of the above work? (complex case)
│  └─ Add data-testid ONLY as last resort
│     → screen.getByTestId('complex-widget')
│     → Document why other queries don't work
```

---

### Decision Tree 3: How to Handle Async Behavior?

```
START: My test involves async behavior
│
├─ Waiting for element to APPEAR?
│  ├─ Simple case (one element)?
│  │  → const element = await screen.findByText(/loaded/i)
│  │  → findBy = getBy + waitFor (convenient)
│  │
│  └─ Multiple assertions?
│     → await waitFor(() => {
│        expect(screen.getByText(/loaded/i)).toBeInTheDocument()
│        expect(screen.getByText(/success/i)).toBeInTheDocument()
│      })
│
├─ Waiting for element to DISAPPEAR?
│  → await waitFor(() => {
│     expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
│   })
│  → Use queryBy (returns null if not found)
│
├─ Waiting for user interaction to complete?
│  → const user = userEvent.setup()
│    await user.click(button)
│    await waitFor(() => {
│      expect(screen.getByText(/clicked/i)).toBeInTheDocument()
│    })
│
├─ Testing loading → success → error flow?
│  → test('handles error after loading', async () => {
│      render(<Component />)
│
│      // Loading state
│      expect(screen.getByText(/loading/i)).toBeInTheDocument()
│
│      // Override MSW to return error
│      server.use(
│        http.get('/api/data', () => HttpResponse.json({}, { status: 500 }))
│      )
│
│      // Wait for error
│      await waitFor(() => {
│        expect(screen.getByText(/error/i)).toBeInTheDocument()
│      })
│    })
│
└─ TanStack Query refetch or mutation?
   → const { result } = renderHook(() => useUsers(), {
       wrapper: createWrapper(),
     })
     await waitFor(() => expect(result.current.isSuccess).toBe(true))
     act(() => result.current.refetch())
     await waitFor(() => expect(result.current.isFetching).toBe(false))
```

---

## Common Pitfalls and Solutions

### Pitfall 1: "Warning: An update to Component inside a test was not wrapped in act(...)"

**Cause**: React state update occurred after test completed, or async update not awaited.

**Example**:
```typescript
// ❌ Causes act() warning
test('updates state', () => {
  render(<Counter />)
  fireEvent.click(screen.getByRole('button'))
  // State update happens after test ends
})
```

**Solution**:
```typescript
// ✅ Await user interactions
test('updates state', async () => {
  const user = userEvent.setup()
  render(<Counter />)
  await user.click(screen.getByRole('button'))
  // Wait for state update to complete
})

// ✅ Or use waitFor
test('updates state', async () => {
  const user = userEvent.setup()
  render(<Counter />)
  await user.click(screen.getByRole('button'))
  await waitFor(() => {
    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })
})
```

**Prevention**: Always use `await` with userEvent and async queries.

---

### Pitfall 2: "Unable to find an element with the role..."

**Cause**: Element doesn't exist, or doesn't have expected role/accessible name.

**Example**:
```typescript
// ❌ Fails if button doesn't have accessible name
screen.getByRole('button', { name: /submit/i })
```

**Debugging**:
```typescript
// Step 1: Print DOM to console
screen.debug()

// Step 2: Check all available roles
screen.logTestingPlaygroundURL()  // Opens browser tool

// Step 3: Verify element exists with broader query
screen.getByRole('button')  // Find ANY button

// Step 4: Check aria-label or text content
<button>Submit</button>              // ✅ name = "Submit"
<button aria-label="Submit form">    // ✅ name = "Submit form"
<button><Icon /></button>            // ❌ no accessible name
```

**Solution**:
```typescript
// ✅ Add accessible name to button
<button>Submit</button>
// Or
<button aria-label="Submit form"><Icon /></button>

// ✅ Test passes
screen.getByRole('button', { name: /submit/i })
```

---

### Pitfall 3: "Cannot read property 'getState' of undefined" (Zustand)

**Cause**: Zustand store not reset between tests, causing state pollution.

**Example**:
```typescript
// ❌ Tests interfere with each other
test('test 1', () => {
  const { result } = renderHook(() => useCounterStore())
  act(() => result.current.increment())
  expect(result.current.count).toBe(1)
})

test('test 2', () => {
  const { result } = renderHook(() => useCounterStore())
  expect(result.current.count).toBe(0)  // ❌ Fails - count is still 1
})
```

**Solution**:
```typescript
// ✅ Reset store in beforeEach
describe('CounterStore', () => {
  beforeEach(() => {
    useCounterStore.setState({ count: 0 })
  })

  test('test 1', () => {
    const { result } = renderHook(() => useCounterStore())
    act(() => result.current.increment())
    expect(result.current.count).toBe(1)
  })

  test('test 2', () => {
    const { result } = renderHook(() => useCounterStore())
    expect(result.current.count).toBe(0)  // ✅ Passes
  })
})
```

---

### Pitfall 4: "Request to /api/users failed with 404" (MSW not intercepting)

**Cause**: MSW server not started, or handler URL doesn't match request.

**Example**:
```typescript
// ❌ MSW server not started
test('fetches users', async () => {
  render(<UserList />)
  // Fails - real fetch() call goes to network
})
```

**Solution**:
```typescript
// ✅ Add MSW server to setup-tests.ts
import { server } from './mocks/server'
import { beforeAll, afterEach, afterAll } from 'vitest'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

// ✅ Verify handler URL matches
// Handler
http.get('/api/users', () => { ... })

// Component (must match exactly)
fetch('/api/users')  // ✅ Matches
fetch('http://localhost:3000/api/users')  // ❌ Doesn't match (includes origin)
```

**Debugging**:
```typescript
// Enable MSW request logging
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))

// Console will show:
// [MSW] Warning: captured a request without a matching request handler
// GET /api/users
```

---

### Pitfall 5: "QueryClientProvider not found in component tree" (TanStack Query)

**Cause**: Component using useQuery not wrapped with QueryClientProvider.

**Example**:
```typescript
// ❌ Missing provider
test('fetches data', async () => {
  render(<MyComponent />)  // Component uses useQuery
  // Error: QueryClientProvider not found
})
```

**Solution**:
```typescript
// ✅ Use renderWithProviders from test-utils.tsx
import { renderWithProviders } from '@/test/test-utils'

test('fetches data', async () => {
  renderWithProviders(<MyComponent />)
  // QueryClientProvider added automatically
})

// ✅ Or for hooks
import { renderHook } from '@testing-library/react'
import { createWrapper } from '@/test/test-utils'

test('hook fetches data', async () => {
  const { result } = renderHook(() => useMyQuery(), {
    wrapper: createWrapper(),
  })
  await waitFor(() => expect(result.current.isSuccess).toBe(true))
})
```

---

## Integration with Other SAPs

### SAP-020 (React Foundation)

**Integration**: SAP-021 templates are designed for SAP-020 projects.

**Workflow**:
1. Create project with SAP-020 (Next.js or Vite template)
2. Install SAP-021 testing infrastructure
3. Add tests as you build features

**File Structure**:
```
my-nextjs-app/  (from SAP-020)
├── src/
│   ├── app/              # Next.js routes
│   ├── components/       # React components
│   │   ├── button.tsx
│   │   └── button.test.tsx  # ← Tests added with SAP-021
│   └── test/             # ← SAP-021 infrastructure
│       ├── setup-tests.ts
│       ├── test-utils.tsx
│       └── mocks/
│           ├── handlers.ts
│           └── server.ts
└── vitest.config.ts      # ← SAP-021 config
```

---

### SAP-022 (Linting - Future)

**Integration**: ESLint rules for testing best practices.

**Rules SAP-022 will add**:
- `testing-library/prefer-screen-queries` (enforce screen.getBy vs getBy)
- `testing-library/no-await-sync-queries` (prevent await with getBy)
- `testing-library/no-debugging-utils` (no screen.debug in production)

---

### SAP-005 (CI/CD - Future Integration)

**Integration**: Run tests in GitHub Actions, fail PR if coverage drops.

**Example GitHub Actions** (to be added in SAP-005):
```yaml
- name: Run tests
  run: pnpm test --coverage --run

- name: Check coverage thresholds
  run: |
    if [ $(jq -r '.total.lines.pct' coverage/coverage-summary.json) -lt 80 ]; then
      echo "Coverage below 80%"
      exit 1
    fi
```

---

## Workflows

### Workflow 1: Adding Tests to Existing SAP-020 Project

**Steps**:
1. Install SAP-021 dependencies
   ```bash
   pnpm add -D vitest @vitejs/plugin-react jsdom
   pnpm add -D @vitest/coverage-v8 @vitest/ui
   pnpm add -D @testing-library/react @testing-library/user-event
   pnpm add -D @testing-library/jest-dom msw
   ```

2. Copy configuration files from SAP-021 templates
   ```bash
   cp templates/react/testing/nextjs/vitest.config.ts .
   cp templates/react/testing/nextjs/src/test/setup-tests.ts src/test/
   cp templates/react/testing/shared/test-utils.tsx src/test/
   cp -r templates/react/testing/shared/mocks src/test/
   ```

3. Add test scripts to package.json
   ```json
   {
     "scripts": {
       "test": "vitest",
       "test:ui": "vitest --ui",
       "test:coverage": "vitest --coverage"
     }
   }
   ```

4. Write first test using examples
   ```bash
   cp templates/react/testing/examples/component.test.tsx src/components/
   ```

5. Run tests
   ```bash
   pnpm test
   ```

---

### Workflow 2: Test-Driven Development (TDD)

**Red → Green → Refactor Cycle**:

1. **Write Failing Test (RED)**
   ```typescript
   test('fetches and displays users', async () => {
     renderWithProviders(<UserList />)
     await screen.findByText(/alice/i)  // Fails - component doesn't exist
   })
   ```

2. **Write Minimal Code (GREEN)**
   ```typescript
   function UserList() {
     const { data: users } = useQuery({
       queryKey: ['users'],
       queryFn: async () => (await fetch('/api/users')).json(),
     })
     return <ul>{users?.map(u => <li key={u.id}>{u.name}</li>)}</ul>
   }
   // Test passes
   ```

3. **Refactor (REFACTOR)**
   ```typescript
   function UserList() {
     const { data: users, isLoading, error } = useQuery({
       queryKey: ['users'],
       queryFn: fetchUsers,  // Extract to service
     })

     if (isLoading) return <Spinner />
     if (error) return <ErrorMessage error={error} />
     return <ul>{users?.map(u => <UserListItem key={u.id} user={u} />)}</ul>
   }
   // Test still passes (behavior unchanged)
   ```

---

### Workflow 3: Debugging Failing Tests

**Systematic Debugging Process**:

1. **Run single test in watch mode**
   ```bash
   pnpm test user-list.test.tsx
   ```

2. **Print DOM to console**
   ```typescript
   test('debug test', () => {
     render(<MyComponent />)
     screen.debug()  // Prints entire DOM
     screen.debug(screen.getByRole('button'))  // Prints specific element
   })
   ```

3. **Use Testing Playground**
   ```typescript
   test('find query', () => {
     render(<MyComponent />)
     screen.logTestingPlaygroundURL()
     // Opens browser tool to find correct query
   })
   ```

4. **Check MSW logs**
   ```typescript
   beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
   // Console shows which requests MSW is/isn't handling
   ```

5. **Verify async operations complete**
   ```typescript
   test('async debug', async () => {
     render(<MyComponent />)
     await waitFor(() => {
       screen.debug()  // Print DOM after async update
     })
   })
   ```

---

## Best Practices Summary

### Testing Mindset
1. ✅ Test user behavior, not implementation details
2. ✅ Focus on integration tests (50-60% of suite)
3. ✅ Use accessible queries (getByRole, getByLabelText)
4. ✅ Always await async operations
5. ✅ Mock at network boundary (MSW), not functions

### Test Organization
1. ✅ Collocate tests with code (`button.tsx` → `button.test.tsx`)
2. ✅ Use `__tests__/` for integration tests
3. ✅ Group related tests with `describe`
4. ✅ Write descriptive test names ("it does X when Y")
5. ✅ One assertion per test (when possible)

### Performance
1. ✅ Run tests in watch mode during development
2. ✅ Use `test.only` to focus on single test
3. ✅ Reset state between tests (Zustand, MSW handlers)
4. ✅ Avoid hardcoded timeouts (use waitFor)
5. ✅ Parallel test execution (Vitest default)

### Maintenance
1. ✅ Update tests when requirements change
2. ✅ Remove tests for deleted features
3. ✅ Refactor tests when they become brittle
4. ✅ Keep tests simple (avoid complex logic)
5. ✅ Document edge cases in test names

---

**End of Awareness Guide**
