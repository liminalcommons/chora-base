# SAP-021: React Testing & Quality - Implementation Plan

**Created**: 2025-10-31
**Target Completion**: 2025-11-15 (2 weeks)
**Dependencies**: SAP-000, SAP-004, SAP-020
**Priority**: P1 (High - enables quality assurance)

---

## Overview

SAP-021 provides comprehensive testing infrastructure for React applications using Vitest v4, React Testing Library v16, and MSW v2. Based on RT-019-DEV research showing Vitest 4x faster than Jest with 85% weighted score vs 71%.

**Time Savings Target**: 3-5 hours → 30 minutes (85% reduction)

---

## Scope Definition

### In Scope

**Testing Stack**:
- ✅ Vitest v4 configuration (Next.js + Vite)
- ✅ React Testing Library v16 + user-event v14
- ✅ MSW v2 (Mock Service Worker) for API mocking
- ✅ @testing-library/jest-dom matchers
- ✅ Coverage configuration (v8 provider, 80-90% targets)
- ✅ Integration test patterns

**Templates**:
1. `vitest.config.ts` (Next.js variant)
2. `vitest.config.ts` (Vite variant)
3. `test-utils.tsx` (custom render with providers)
4. `component.test.template.tsx` (component test pattern)
5. `hook.test.template.tsx` (custom hook test pattern)
6. `integration.test.template.tsx` (integration test pattern)
7. `msw/handlers.ts` (MSW setup)
8. `msw/server.ts` (MSW server config)
9. `setup-tests.ts` (global test setup)

**Documentation**:
1. capability-charter.md (business case, ROI)
2. protocol-spec.md (testing architecture, patterns)
3. awareness-guide.md (when to test what, common pitfalls)
4. adoption-blueprint.md (step-by-step installation)
5. ledger.md (adoption tracking)

### Out of Scope

**Not Included in SAP-021**:
- ❌ E2E testing (Playwright, Cypress) - future SAP-027
- ❌ Visual regression testing (Percy, Chromatic) - future SAP-028
- ❌ Performance testing (Lighthouse CI) - covered in SAP-025
- ❌ Accessibility testing (jest-axe) - covered in SAP-026
- ❌ Load testing / stress testing

---

## Key Decisions from RT-019-DEV Research

### Why Vitest v4 Over Jest

**Performance** (RT-019-DEV lines 280-310):
- 4x faster for small test suites
- 1.9x faster for medium suites
- ESM-first (no CJS issues)
- Native TypeScript support (no ts-jest)

**Developer Experience**:
- 98% retention rate (State of JS 2024)
- Watch mode 10x faster
- Better error messages
- Compatible with Jest matchers

**Weighted Score**: Vitest 85%, Jest 71%

### Why React Testing Library

**Philosophy** (RT-019-DEV lines 315-350):
- Test user behavior, not implementation
- Accessible by default (queries by role, label)
- Avoid testing internals (state, props)
- Encourages accessible component design

**Industry Standard**:
- De facto React testing library
- 14M+ weekly downloads
- Kent C. Dodds patterns (testing-library.com)

### Why MSW v2

**API Mocking** (RT-019-DEV lines 355-390):
- Intercepts network requests (fetch, axios)
- Works in tests AND browser (dev mode)
- Type-safe handlers (TypeScript + Zod)
- Realistic API simulation

**Alternative**: Nock (lower-level, less realistic)

---

## Testing Pyramid Strategy

Based on RT-019-DEV Testing Pyramid (lines 395-425):

```
        E2E (10-20%)
       ████████████
      Integration (50-60%)
     ████████████████████████
   Unit Tests (20-30%)
  ████████████████
```

**SAP-021 Focus**: Unit + Integration (80-90% of test suite)

**Rationale**:
- Integration tests catch most bugs (realistic scenarios)
- Unit tests for complex logic (algorithms, utilities)
- E2E tests for critical paths only (expensive, flaky)

---

## Template Specifications

### 1. vitest.config.ts (Next.js)

**Purpose**: Vitest configuration for Next.js projects

**Key Features**:
- React environment (@vitejs/plugin-react)
- Path aliases matching tsconfig.json (@/*)
- Coverage with v8 provider (80-90% thresholds)
- jsdom environment for DOM testing
- Setup files (setup-tests.ts)

**Example**:
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup-tests.ts'],
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### 2. test-utils.tsx

**Purpose**: Custom render function with providers (TanStack Query, etc.)

**Pattern**:
```typescript
import { render, RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactElement } from 'react'

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
}

export function renderWithProviders(
  ui: ReactElement,
  options?: RenderOptions
) {
  const queryClient = createTestQueryClient()

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    )
  }

  return render(ui, { wrapper: Wrapper, ...options })
}

// Re-export everything
export * from '@testing-library/react'
export { userEvent } from '@testing-library/user-event'
```

### 3. Component Test Template

**Pattern**:
```typescript
import { renderWithProviders, screen } from '@/test/test-utils'
import { userEvent } from '@testing-library/user-event'
import { Counter } from './counter'

describe('Counter', () => {
  it('renders initial count', () => {
    renderWithProviders(<Counter initialCount={5} />)
    expect(screen.getByRole('button')).toHaveTextContent('5')
  })

  it('increments count on click', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter initialCount={0} />)

    const button = screen.getByRole('button', { name: /increment/i })
    await user.click(button)

    expect(button).toHaveTextContent('1')
  })
})
```

### 4. Hook Test Template

**Pattern**:
```typescript
import { renderHook, waitFor } from '@testing-library/react'
import { useUsers } from './use-users'
import { createWrapper } from '@/test/test-utils'

describe('useUsers', () => {
  it('fetches users successfully', async () => {
    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toHaveLength(2)
  })
})
```

### 5. MSW Handlers

**Pattern**:
```typescript
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ])
  }),

  http.post('/api/users', async ({ request }) => {
    const newUser = await request.json()
    return HttpResponse.json({ id: '3', ...newUser }, { status: 201 })
  }),
]
```

---

## Documentation Outline

### capability-charter.md

**Sections**:
1. What This Is - Testing infrastructure for React
2. Why This Exists - Problem: Manual testing unreliable, time-consuming
3. Who Should Use This - All React developers, teams
4. Business Value - Catch 60-80% more bugs pre-commit
5. Scope - What's included, what's not
6. Outcomes - 80-90% coverage, <5s test runs
7. Stakeholders - React developers, QA teams
8. Dependencies - SAP-020, SAP-004
9. Constraints - Vitest only (no Jest), integration-focused
10. Risks - Learning curve, false positives

**ROI**:
- Manual testing: 3-5 hours/project
- SAP-021 setup: 30 minutes
- Savings: 85% time reduction
- Quality: 60-80% more bugs caught pre-commit

### protocol-spec.md

**Sections**:
1. Overview - Testing stack (Vitest, RTL, MSW)
2. Protocol Foundation - Testing principles, pyramid
3. Inputs - Prerequisites (Node.js, React project)
4. Architecture - Testing patterns (unit, integration)
5. Outputs - Test suites, coverage reports
6. Behavior Specification - What to test, how to test
7. Interface Contracts - Test file naming, structure
8. Guarantees - Coverage thresholds, speed targets
9. Test Patterns - Component, hook, integration examples
10. Quality Attributes - Reliability, maintainability

### awareness-guide.md

**Sections**:
1. When to Use SAP-021 - All React projects with >10 components
2. Use Cases - Component testing, API mocking, integration tests
3. Anti-Patterns - Don't test implementation, don't mock too much
4. Decision Trees - What to test (component vs integration)
5. Common Pitfalls - Act warnings, async state, query invalidation
6. Integration with SAPs - SAP-020 (foundation), SAP-022 (linting)
7. Workflows - Adding tests to existing project, TDD workflow

### adoption-blueprint.md

**Sections**:
1. Prerequisites - Node.js 22.x, React project from SAP-020
2. Installing SAP-021 - Step-by-step (15 steps)
3. Validation - Run tests, check coverage
4. Creating First Test - Component test example
5. Next Steps - Add tests to all features, integrate with CI

---

## Implementation Timeline

### Week 1 (2025-11-01 to 2025-11-08)

**Day 1-2**: Research Validation
- Re-read RT-019-DEV testing sections
- Validate Vitest v4 compatibility with Next.js 15
- Test MSW v2 with TanStack Query
- Document any breaking changes

**Day 3-4**: Template Creation
- Create vitest.config.ts (Next.js + Vite variants)
- Create test-utils.tsx
- Create component/hook/integration test templates
- Create MSW handlers

**Day 5**: Documentation (Part 1)
- Write capability-charter.md
- Write protocol-spec.md (first half)

### Week 2 (2025-11-08 to 2025-11-15)

**Day 6-7**: Documentation (Part 2)
- Complete protocol-spec.md
- Write awareness-guide.md
- Write adoption-blueprint.md
- Write ledger.md

**Day 8-9**: Validation
- Install SAP-021 in test project
- Write 10+ tests (component, hook, integration)
- Measure setup time (target: ≤30 min)
- Run coverage, ensure 80%+ achievable

**Day 10**: Finalization
- Update INDEX.md
- Update sap-catalog.json
- Create GitHub issue for SAP-021
- Publish to chora-base

---

## Success Criteria

### Required Validations

- [ ] Vitest config works with Next.js 15 (zero errors)
- [ ] Vitest config works with Vite 7 (zero errors)
- [ ] test-utils.tsx renders with TanStack Query provider
- [ ] MSW handlers intercept API calls successfully
- [ ] Component tests pass (10+ examples)
- [ ] Hook tests pass (5+ examples)
- [ ] Integration tests pass (3+ examples)
- [ ] Coverage reports generate correctly
- [ ] Setup time ≤30 minutes (measured)

### Quality Metrics

- [ ] TypeScript coverage: 100% (no any types)
- [ ] Documentation completeness: 5/5 artifacts
- [ ] Template count: 9 templates minimum
- [ ] Test speed: <5 seconds for 50 tests
- [ ] Coverage threshold: 80-90% achievable

---

## Risk Mitigation

### Risk 1: Vitest + Next.js Compatibility Issues

**Likelihood**: Medium (Next.js has custom webpack config)
**Impact**: High (blocks SAP-021)
**Mitigation**:
- Test with fresh Next.js 15 project from SAP-020
- Check vitest-nextjs plugin if needed
- Document workarounds in adoption-blueprint

### Risk 2: MSW v2 Breaking Changes

**Likelihood**: Low (MSW v2 stable since 2023)
**Impact**: Medium (API mocking breaks)
**Mitigation**:
- Follow MSW v2 migration guide
- Test with TanStack Query integration
- Provide clear handler examples

### Risk 3: Learning Curve Too Steep

**Likelihood**: Medium (testing has learning curve)
**Impact**: Low (adoption slower, not blocked)
**Mitigation**:
- Provide 10+ working test examples
- Clear patterns in awareness-guide
- Video tutorials (future)

---

## Dependencies on Other Work

### Requires Completion

- [x] SAP-020 (React Foundation) - ✅ Complete
- [x] Templates (Next.js + Vite) - ✅ Complete

### Integrates With

- [ ] SAP-022 (Linting) - Will add testing rules to ESLint
- [ ] SAP-005 (CI/CD) - Will integrate test runs in GitHub Actions

---

## Post-Launch Activities

### Month 1 (2025-11-15 to 2025-12-15)

- Monitor adoption (track in ledger.md)
- Gather feedback via GitHub Discussions
- Fix bugs, iterate templates
- Create video tutorials (optional)

### Quarterly (2025-12, 2026-03, 2026-06)

- Update dependencies (Vitest, RTL, MSW)
- Review test patterns, add new examples
- Measure ROI (time savings, bugs caught)

---

## Next SAPs After SAP-021

**Priority Order**:
1. **SAP-022** (Linting) - Complements testing, team standardization
2. **SAP-024** (Styling) - Visual development, high developer value
3. **SAP-023** (State) - Advanced patterns, medium priority
4. **SAP-025** (Performance) - Production readiness
5. **SAP-026** (Accessibility) - Production readiness

**Recommended**: SAP-022 next (linting + testing = complete quality gates)

---

## Appendix: Key Research Citations

### RT-019-DEV: Testing Section (Lines 280-425)

**Vitest vs Jest Comparison**:
- Lines 280-310: Performance benchmarks (4x faster small suites)
- Lines 311-340: Feature comparison (ESM, TypeScript, watch mode)
- Lines 341-370: Migration guide (Jest → Vitest)

**React Testing Library**:
- Lines 315-350: Philosophy (test behavior, not implementation)
- Lines 351-380: Query priorities (getByRole > getByLabelText > getByTestId)
- Lines 381-410: Common patterns (userEvent, async state, waitFor)

**MSW (Mock Service Worker)**:
- Lines 355-390: Setup guide (handlers, server, browser)
- Lines 391-420: Integration with TanStack Query
- Lines 421-450: Debugging tips

---

**End of SAP-021 Implementation Plan**
