# React Testing Templates

This directory contains testing configuration templates and examples for React projects using SAP-021 (React Testing & Quality).

## Quick Start

```bash
# From your React project root (created with SAP-020)

# 1. Install dependencies
pnpm add -D vitest @vitejs/plugin-react jsdom @vitest/coverage-v8 @vitest/ui
pnpm add -D @testing-library/react @testing-library/user-event @testing-library/jest-dom
pnpm add -D msw

# 2. Copy configuration for your framework
# For Next.js:
cp templates/react/testing/nextjs/vitest.config.ts .
cp templates/react/testing/nextjs/src/test/setup-tests.ts src/test/

# For Vite:
cp templates/react/testing/vite/vitest.config.ts .
cp templates/react/testing/vite/src/test/setup-tests.ts src/test/

# 3. Copy shared utilities
cp templates/react/testing/shared/test-utils.tsx src/test/
cp -r templates/react/testing/shared/mocks src/test/

# 4. Add test scripts to package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}

# 5. Run tests
pnpm test
```

## Directory Structure

```
templates/react/testing/
├── README.md                    # This file
├── nextjs/                      # Next.js-specific configs
│   ├── vitest.config.ts         # Vitest config for Next.js 15
│   └── src/test/
│       └── setup-tests.ts       # Global setup (includes Next.js router mocks)
├── vite/                        # Vite-specific configs
│   ├── vitest.config.ts         # Vitest config for Vite 7
│   └── src/test/
│       └── setup-tests.ts       # Global setup (no Next.js mocks)
├── shared/                      # Framework-agnostic utilities
│   ├── test-utils.tsx           # Custom render with providers
│   └── mocks/
│       ├── handlers.ts          # MSW request handlers
│       ├── server.ts            # MSW server for Node.js (tests)
│       └── browser.ts           # MSW worker for browser (dev)
└── examples/                    # Example tests
    ├── component.test.tsx       # Component testing patterns
    ├── hook.test.tsx            # Hook testing patterns (TanStack Query + Zustand)
    └── integration.test.tsx     # Integration testing patterns
```

## Template Files

### Next.js Configuration

**vitest.config.ts**:
- Configured for Next.js 15
- Path aliases match `tsconfig.json` (@/*)
- Excludes `.next/**` from coverage
- Optimized for parallel execution

**setup-tests.ts**:
- Mocks Next.js router (`next/navigation`)
- Mocks `window.matchMedia`
- Mocks `IntersectionObserver`
- Integrates MSW server

### Vite Configuration

**vitest.config.ts**:
- Configured for Vite 7
- Path aliases match `tsconfig.json` (@/*)
- Excludes `dist/**` from coverage
- Same performance optimizations as Next.js

**setup-tests.ts**:
- No Next.js router mocks (not needed for Vite)
- Same browser API mocks as Next.js variant

### Shared Utilities

**test-utils.tsx**:
- `renderWithProviders()` - Wraps components with TanStack Query provider
- `createWrapper()` - For use with `renderHook`
- Re-exports all React Testing Library utilities
- Exports `userEvent` for user interactions

**mocks/handlers.ts**:
- Example MSW handlers for REST API
- Type-safe request/response handling
- Includes GET, POST, PUT, DELETE examples
- Error simulation examples

**mocks/server.ts**:
- MSW server setup for Node.js (test environment)
- Integrates with Vitest via `setup-tests.ts`

**mocks/browser.ts**:
- MSW worker setup for browser (development)
- Optional: enables API mocking in dev mode

### Example Tests

**component.test.tsx**:
- Testing component rendering
- User interactions with `userEvent`
- Accessibility-focused queries (`getByRole`, `getByLabelText`)
- Multiple test scenarios

**hook.test.tsx**:
- Testing custom hooks with `renderHook`
- TanStack Query hook testing (loading, success, error states)
- Zustand store testing (state updates, cross-instance behavior)
- Async behavior with `waitFor`

**integration.test.tsx**:
- Full user flow testing (load → interact → submit)
- MSW integration (mocking API calls)
- Form submissions and validations
- Error handling end-to-end

## Usage Instructions

### For Next.js Projects

1. Copy Next.js-specific files:
   ```bash
   cp templates/react/testing/nextjs/vitest.config.ts .
   cp templates/react/testing/nextjs/src/test/setup-tests.ts src/test/
   ```

2. Copy shared utilities:
   ```bash
   cp templates/react/testing/shared/test-utils.tsx src/test/
   cp -r templates/react/testing/shared/mocks src/test/
   ```

3. Copy example tests (optional):
   ```bash
   cp templates/react/testing/examples/* src/components/
   ```

### For Vite Projects

1. Copy Vite-specific files:
   ```bash
   cp templates/react/testing/vite/vitest.config.ts .
   cp templates/react/testing/vite/src/test/setup-tests.ts src/test/
   ```

2. Copy shared utilities (same as Next.js):
   ```bash
   cp templates/react/testing/shared/test-utils.tsx src/test/
   cp -r templates/react/testing/shared/mocks src/test/
   ```

3. Copy example tests (optional):
   ```bash
   cp templates/react/testing/examples/* src/components/
   ```

## Customization

### Adding More Providers

If your app uses additional providers (theme, router, i18n), update `test-utils.tsx`:

```typescript
function AllTheProviders({ children }: AllTheProvidersProps) {
  const queryClient = createTestQueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={lightTheme}>
        <I18nProvider locale="en">
          {children}
        </I18nProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}
```

### Customizing MSW Handlers

Add your API endpoints to `mocks/handlers.ts`:

```typescript
export const handlers = [
  // ... existing handlers ...

  // Add your endpoints
  http.get('/api/posts', () => {
    return HttpResponse.json([
      { id: '1', title: 'My Post', content: '...' },
    ])
  }),
]
```

### Adjusting Coverage Thresholds

Edit `vitest.config.ts` to change coverage requirements:

```typescript
coverage: {
  thresholds: {
    lines: 85,      // Increase from 80%
    functions: 85,  // Increase from 80%
    branches: 80,   // Increase from 75%
    statements: 85, // Increase from 80%
  },
}
```

## Testing Patterns

### Component Tests

Test user-visible behavior, not implementation:

```typescript
// ✅ Good
test('increments count on button click', async () => {
  const user = userEvent.setup()
  render(<Counter />)
  await user.click(screen.getByRole('button', { name: /increment/i }))
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
})

// ❌ Bad
test('calls setState', () => {
  const wrapper = shallow(<Counter />)
  wrapper.instance().increment()
  expect(wrapper.state('count')).toBe(1)
})
```

### Hook Tests

Use `renderHook` with providers:

```typescript
test('fetches users', async () => {
  const { result } = renderHook(() => useUsers(), {
    wrapper: createWrapper(),
  })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(result.current.data).toHaveLength(2)
})
```

### Integration Tests

Test complete user flows:

```typescript
test('user can add item to cart', async () => {
  const user = userEvent.setup()
  render(<ProductPage />)

  await user.click(screen.getByRole('button', { name: /add to cart/i }))

  await waitFor(() => {
    expect(screen.getByText(/1 item in cart/i)).toBeInTheDocument()
  })
})
```

## Performance

### Test Execution Speed

Expected performance (from SAP-021):
- <5s for 50 tests
- <15s for 200 tests
- <1s watch mode re-runs

### Optimizations

All configs include:
- ✅ Parallel execution (`pool: 'vmThreads'`)
- ✅ v8 coverage provider (faster than istanbul)
- ✅ Optimized for CI (fixed worker count)
- ✅ No retry on failures (fast feedback)

## Troubleshooting

### Common Issues

**"Cannot find module '@/test/test-utils'"**
- Verify `resolve.alias` in `vitest.config.ts` points to `./src`

**"QueryClientProvider not found"**
- Use `renderWithProviders` instead of `render`

**"Warning: An update to X inside a test was not wrapped in act(...)"**
- Always `await` userEvent interactions: `await user.click(button)`

**"Request to /api/users was not handled"**
- Verify MSW server started in `setup-tests.ts`
- Check handler URL matches exactly

## Documentation

For comprehensive documentation, see:
- [SAP-021 Capability Charter](../../../docs/skilled-awareness/react-testing/capability-charter.md)
- [SAP-021 Protocol Spec](../../../docs/skilled-awareness/react-testing/protocol-spec.md)
- [SAP-021 Awareness Guide](../../../docs/skilled-awareness/react-testing/awareness-guide.md)
- [SAP-021 Adoption Blueprint](../../../docs/skilled-awareness/react-testing/adoption-blueprint.md)

## Support

- [Vitest Docs](https://vitest.dev)
- [React Testing Library Docs](https://testing-library.com/react)
- [MSW Docs](https://mswjs.io)
- [chora-base GitHub Discussions](https://github.com/liminalcommons/chora-base/discussions)

## License

MIT - Same as chora-base repository
