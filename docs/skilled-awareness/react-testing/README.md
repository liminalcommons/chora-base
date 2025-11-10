# SAP-021: React Testing & Quality

**SAP ID**: SAP-021
**Version**: 1.0.0
**Vitest Version**: 4.0.x
**React Testing Library Version**: 16.x
**MSW Version**: 2.x
**Research Foundation**: RT-019-DEV (Q4 2024 - Q1 2025)

---

## 🚀 Quick Start (3 minutes)

```bash
# Install testing dependencies
pnpm add -D vitest@4 @vitejs/plugin-react jsdom
pnpm add -D @testing-library/react@16 @testing-library/jest-dom@6 @testing-library/user-event@14
pnpm add -D msw@2

# Create Vitest config
cat > vitest.config.ts <<'EOF'
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
      thresholds: { lines: 80, functions: 80, branches: 75 },
    },
  },
})
EOF

# Create setup file
mkdir -p src/test
cat > src/test/setup-tests.ts <<'EOF'
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
EOF

# Run tests
pnpm vitest
```

**Expected output**:
```
 ✓ src/components/Counter.test.tsx (2)
   ✓ increments count when clicking increment button
   ✓ decrements count when clicking decrement button

 Test Files  1 passed (1)
      Tests  2 passed (2)
   Duration  0.45s
```

---

## What Is It?

SAP-021 provides **production-grade React testing infrastructure** using Vitest 4.0 (4x faster than Jest), React Testing Library v16, and MSW v2 for API mocking.

### Purpose

- **Fast Testing**: Vitest 4.0 runs 4x faster than Jest for small suites, 1.9x faster for 800+ tests
- **User-Centric Tests**: React Testing Library focuses on testing user behavior, not implementation
- **Integration Focus**: Testing Trophy philosophy (50-60% integration, 20-30% unit)
- **API Mocking**: MSW v2 intercepts network requests at the network level
- **Type-Safe**: Native TypeScript support, no ts-jest required
- **Coverage Enforcement**: 80%+ lines/functions, 75%+ branches with automatic thresholds

### How It Works

1. **Install** Vitest, React Testing Library, MSW
2. **Configure** vitest.config.ts with jsdom environment and coverage thresholds
3. **Setup** global test utilities (jest-dom matchers, router mocks, browser API mocks)
4. **Write** tests using `render()`, `screen`, `userEvent`, and accessible queries
5. **Mock** APIs with MSW handlers
6. **Run** tests in parallel with `vitest` (watch mode) or `vitest run` (CI)

---

## When to Use

### ✅ Use React Testing (SAP-021) When

- **New React Project**: Testing infrastructure for React 19 + Next.js 15
- **Unit Tests**: Test individual components, hooks, utilities
- **Integration Tests**: Test component interactions, data flow, user journeys
- **API Mocking**: Intercept fetch/axios requests with MSW
- **Migration from Jest**: Vitest is 98% Jest-compatible (2-4 hour migration)
- **Coverage Requirements**: Enforce 80%+ test coverage
- **CI/CD Integration**: Fast, parallel test execution for GitHub Actions

### ❌ Don't Use When

- **E2E Testing**: Use Playwright/Cypress (SAP-039) for full browser automation
- **Non-React Projects**: Use framework-specific testing tools
- **Visual Regression**: Use Chromatic, Percy, or Playwright screenshots
- **Performance Testing**: Use Lighthouse CI, WebPageTest

---

## Key Features

### Vitest 4.0 Performance

**4x Faster Than Jest**:
- Small test suites: 0.5s (Vitest) vs 2.1s (Jest)
- Medium suites (800 tests): 4.2s (Vitest) vs 8.1s (Jest)
- Watch mode: <1s re-runs with instant feedback

**Native ESM + TypeScript**:
- Zero configuration for ESM modules
- No `ts-jest` dependency required
- Direct `.tsx` file imports

**Better Developer Experience**:
- Clear error messages with source maps
- Inline snapshots
- UI mode for debugging (`vitest --ui`)

### React Testing Library v16

**Accessible Queries First**:
```tsx
// ✅ Best: Role-based (accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })

// ✅ Good: Label-based (forms)
screen.getByLabelText(/password/i)

// ⚠️ OK: Text content (non-interactive)
screen.getByText(/welcome/i)

// ❌ Last resort: Test IDs
screen.getByTestId('submit-btn')
```

**User Event Simulation**:
```tsx
import { userEvent } from '@testing-library/user-event'

const user = userEvent.setup()
await user.click(screen.getByRole('button'))
await user.type(screen.getByRole('textbox'), 'Hello')
await user.keyboard('{Enter}')
```

**Async Testing**:
```tsx
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument()
})

const element = await screen.findByText(/loaded/i) // Combines waitFor + getBy
```

### MSW v2 API Mocking

**Network-Level Mocking**:
```tsx
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' },
    ])
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

**Dynamic Responses**:
```tsx
http.post('/api/login', async ({ request }) => {
  const { email, password } = await request.json()

  if (password === 'correct') {
    return HttpResponse.json({ token: 'abc123' })
  }

  return HttpResponse.json(
    { error: 'Invalid credentials' },
    { status: 401 }
  )
})
```

### Coverage Thresholds

**Automatic Enforcement**:
```typescript
coverage: {
  provider: 'v8',  // Faster than istanbul
  thresholds: {
    lines: 80,      // 80% line coverage
    functions: 80,   // 80% function coverage
    branches: 75,    // 75% branch coverage
    statements: 80,  // 80% statement coverage
  },
}
```

**Coverage Reports**:
- Terminal: Text summary
- HTML: Interactive report (`coverage/index.html`)
- LCOV: CI/CD integration (Codecov, Coveralls)
- JSON: Machine-readable data

---

## Quick Reference

### Testing Patterns

**Component Test** (integration):
```tsx
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import { Counter } from './Counter'

describe('Counter', () => {
  it('increments count when clicking increment button', async () => {
    const user = userEvent.setup()
    render(<Counter />)

    await user.click(screen.getByRole('button', { name: /increment/i }))

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })
})
```

**Server Component Test** (Next.js):
```tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { UserList } from './UserList'

// Mock async function
vi.mock('./api', () => ({
  getUsers: vi.fn(() => Promise.resolve([
    { id: 1, name: 'Alice' },
  ])),
}))

describe('UserList (Server Component)', () => {
  it('displays user list', async () => {
    const UserListWithData = await UserList()
    render(UserListWithData)

    expect(screen.getByText(/alice/i)).toBeInTheDocument()
  })
})
```

**Custom Hook Test**:
```tsx
import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments count', async () => {
    const { result } = renderHook(() => useCounter())

    act(() => {
      result.current.increment()
    })

    await waitFor(() => {
      expect(result.current.count).toBe(1)
    })
  })
})
```

**API Mocking with MSW**:
```tsx
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { render, screen, waitFor } from '@testing-library/react'
import { beforeAll, afterAll, afterEach, describe, it, expect } from 'vitest'
import { UserProfile } from './UserProfile'

const server = setupServer(
  http.get('/api/user/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Alice',
      email: 'alice@example.com',
    })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('UserProfile', () => {
  it('fetches and displays user data', async () => {
    render(<UserProfile userId={1} />)

    await waitFor(() => {
      expect(screen.getByText(/alice/i)).toBeInTheDocument()
    })
  })
})
```

### Test Commands

```bash
# Run tests in watch mode (dev)
pnpm vitest

# Run tests once (CI)
pnpm vitest run

# Run with coverage
pnpm vitest --coverage

# Run specific file
pnpm vitest src/components/Counter.test.tsx

# Run in UI mode (debugging)
pnpm vitest --ui

# Update snapshots
pnpm vitest -u
```

### Query Priority

**Always use the most accessible query**:

1. **getByRole** (best for interactive elements)
   - `getByRole('button', { name: /submit/i })`
   - `getByRole('textbox', { name: /email/i })`
   - `getByRole('heading', { name: /title/i })`

2. **getByLabelText** (forms)
   - `getByLabelText(/email address/i)`
   - `getByLabelText(/password/i)`

3. **getByPlaceholderText** (if no label)
   - `getByPlaceholderText(/search/i)`

4. **getByText** (non-interactive)
   - `getByText(/welcome back/i)`

5. **getByTestId** (last resort)
   - `getByTestId('complex-widget')`

### jest-dom Matchers

**Common assertions**:
```tsx
expect(element).toBeInTheDocument()
expect(element).toHaveTextContent(/hello/i)
expect(element).toHaveAttribute('href', '/about')
expect(element).toHaveClass('active')
expect(element).toBeVisible()
expect(element).toBeDisabled()
expect(element).toHaveValue('test@example.com')
expect(element).toBeChecked()
```

---

## Integration with Other SAPs

### SAP-020 (React Foundation)
- **Link**: TypeScript strict mode + React 19 baseline
- **How**: Tests validate React 19 features (RSC, Actions, use() hook)
- **Benefit**: Type-safe tests with full React 19 support

### SAP-022 (React Linting)
- **Link**: ESLint rules for tests (testing-library plugin)
- **How**: Enforce accessible queries, async best practices
- **Benefit**: Catch common testing mistakes at compile time

### SAP-023 (React State Management)
- **Link**: Test TanStack Query and Zustand
- **How**: Mock API responses with MSW, test cache updates
- **Benefit**: Integration tests for data fetching and global state

### SAP-005 (CI/CD Workflows)
- **Link**: GitHub Actions test automation
- **How**: Run `vitest run --coverage` in CI
- **Benefit**: Automated coverage enforcement, PR checks

### SAP-039 (E2E Testing)
- **Link**: Playwright for full browser automation
- **How**: Unit/integration (SAP-021) + E2E (SAP-039) = full coverage
- **Benefit**: Testing Trophy completion (static → unit → integration → E2E)

---

## Success Metrics

### Initial Setup (<3 minutes)
- ✅ **Dependencies Installed**: vitest, @testing-library/react, msw
- ✅ **Config Created**: vitest.config.ts with jsdom environment
- ✅ **Setup File**: src/test/setup-tests.ts with jest-dom
- ✅ **First Test Passes**: Sample component test runs successfully

### Test Quality
- ✅ **Coverage Thresholds**: 80%+ lines, 80%+ functions, 75%+ branches
- ✅ **Accessible Queries**: 90%+ tests use `getByRole` or `getByLabelText`
- ✅ **No Implementation Details**: Zero tests checking state/props directly
- ✅ **Async Handling**: All async tests use `waitFor` or `findBy*`

### Performance Targets
- ✅ **Watch Mode**: <1s re-runs after code changes
- ✅ **Full Suite**: <5s for 50 tests, <30s for 500 tests
- ✅ **CI Build**: <2 minutes for test + coverage report

### Adoption Indicators
- ✅ **Testing Trophy**: 50-60% integration tests, 20-30% unit tests
- ✅ **User-Centric**: Tests describe user behavior, not implementation
- ✅ **MSW Integration**: API tests use MSW handlers, not mocked fetch

---

## Troubleshooting

### Problem: "document is not defined" error

**Symptom**: Tests fail with `ReferenceError: document is not defined`

**Cause**: Vitest not using jsdom environment

**Fix**: Verify `vitest.config.ts` has `environment: 'jsdom'`
```typescript
export default defineConfig({
  test: {
    environment: 'jsdom',  // Required for React Testing Library
  },
})
```

**Alternative**: Per-file environment
```typescript
// @vitest-environment jsdom
import { render } from '@testing-library/react'
```

---

### Problem: jest-dom matchers not available (toBeInTheDocument, etc.)

**Symptom**: `TypeError: expect(...).toBeInTheDocument is not a function`

**Cause**: jest-dom not imported in setup file

**Fix**: Add to `src/test/setup-tests.ts`:
```typescript
import '@testing-library/jest-dom/vitest'
```

**Verify**: Check `vitest.config.ts` has setupFiles:
```typescript
export default defineConfig({
  test: {
    setupFiles: ['./src/test/setup-tests.ts'],
  },
})
```

---

### Problem: "Unable to find role" errors

**Symptom**: `TestingLibraryElementError: Unable to find an accessible element with the role "button"`

**Cause**: Element doesn't have expected role or is missing accessible name

**Fix**: Use `screen.logTestingPlaygroundURL()` to debug:
```tsx
render(<MyComponent />)
screen.logTestingPlaygroundURL()  // Opens testing playground in browser
```

**Common fixes**:
```tsx
// ❌ BAD: Missing accessible name
<button>Submit</button>
screen.getByRole('button', { name: /login/i })  // Fails

// ✅ GOOD: Text content provides name
<button>Login</button>
screen.getByRole('button', { name: /login/i })  // Works

// ✅ GOOD: aria-label provides name
<button aria-label="Login">→</button>
screen.getByRole('button', { name: /login/i })  // Works
```

---

### Problem: Tests timeout with async components

**Symptom**: Tests fail with `Timeout - Async callback was not invoked within the 5000 ms timeout`

**Cause**: Not using `waitFor` or `findBy*` for async operations

**Fix**: Use async queries
```tsx
// ❌ BAD: Synchronous query for async data
render(<UserProfile userId={1} />)
expect(screen.getByText(/alice/i)).toBeInTheDocument()  // Fails immediately

// ✅ GOOD: Wait for async data
render(<UserProfile userId={1} />)
await waitFor(() => {
  expect(screen.getByText(/alice/i)).toBeInTheDocument()
})

// ✅ BETTER: findBy* combines waitFor + getBy
render(<UserProfile userId={1} />)
const name = await screen.findByText(/alice/i)  // Waits up to 1s
expect(name).toBeInTheDocument()
```

---

### Problem: Coverage not reaching 80% threshold

**Symptom**: `vitest --coverage` fails with `Coverage thresholds not met`

**Cause**: Untested code paths or excluded files

**Fix**: Generate HTML coverage report to find gaps:
```bash
pnpm vitest --coverage
open coverage/index.html  # macOS
start coverage/index.html  # Windows
```

**Common gaps**:
- Error boundaries (test error states)
- Edge cases (empty states, loading states)
- Utility functions (move to separate files and test)

**Exclude non-testable files**:
```typescript
coverage: {
  exclude: [
    'node_modules/',
    '**/*.config.ts',
    '**/__tests__/**',
    'src/test/**',
  ],
}
```

---

## Learn More

### Documentation

- **[Capability Charter](capability-charter.md)**: Problem statement, solution design, success criteria
- **[Protocol Spec](protocol-spec.md)**: Complete technical specification (Vitest, RTL, MSW)
- **[Awareness Guide](awareness-guide.md)**: Detailed workflows, testing patterns, examples
- **[Adoption Blueprint](adoption-blueprint.md)**: Step-by-step installation and setup
- **[Ledger](ledger.md)**: Adoption tracking, version history, active deployments

### Official Resources

- **[Vitest Documentation](https://vitest.dev)**: Official Vitest guide and API reference
- **[React Testing Library](https://testing-library.com/react)**: Guiding principles and API
- **[MSW Documentation](https://mswjs.io)**: API mocking with Mock Service Worker
- **[jest-dom Matchers](https://github.com/testing-library/jest-dom)**: Custom matchers

### Related SAPs

- **[SAP-020 (react-foundation)](../react-foundation/)**: React 19 + Next.js 15 baseline
- **[SAP-022 (react-linting)](../react-linting/)**: ESLint rules for tests
- **[SAP-023 (react-state-management)](../react-state-management/)**: Test TanStack Query + Zustand
- **[SAP-005 (ci-cd-workflows)](../ci-cd-workflows/)**: GitHub Actions automation
- **[SAP-039 (react-e2e-testing)](../react-e2e-testing/)**: Playwright E2E tests

### Research Foundation

- **RT-019-DEV**: Developer experience research (Vitest vs Jest benchmarks, Testing Trophy validation)

---

## Version History

- **1.0.0** (2025-11-09): Initial SAP-021 release
  - Vitest 4.0 baseline (4x faster than Jest, native ESM/TypeScript)
  - React Testing Library v16 (accessible queries, user-centric testing)
  - MSW v2 for network-level API mocking
  - Testing Trophy philosophy (50-60% integration, 20-30% unit)
  - Coverage thresholds (80% lines/functions, 75% branches)
  - Next.js 15 router mocking
  - Browser API mocking (matchMedia, IntersectionObserver)
  - Integration with 5 SAPs (Foundation, Linting, State, CI/CD, E2E)
  - Research-backed patterns from RT-019-DEV

---

**Next Steps**:
1. Read [adoption-blueprint.md](adoption-blueprint.md) for installation instructions
2. Install dependencies: `pnpm add -D vitest @testing-library/react @testing-library/jest-dom msw`
3. Create vitest.config.ts and setup-tests.ts
4. Write first test: `src/components/Counter.test.tsx`
5. Run tests: `pnpm vitest`
