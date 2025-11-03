import { render, RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactElement, ReactNode } from 'react'

/**
 * Create a new QueryClient instance for testing
 * Each test gets a fresh client to avoid cross-test pollution
 */
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // Disable retries in tests for faster failures
        retry: false,
        // Disable garbage collection for predictable behavior
        gcTime: Infinity,
      },
      mutations: {
        retry: false,
      },
    },
  })
}

/**
 * All test providers wrapper
 * Add your app's providers here (QueryClient, Router, Theme, etc.)
 */
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

/**
 * Custom render function that wraps components with all providers
 * Use this instead of RTL's render in your tests
 *
 * @example
 * import { renderWithProviders, screen } from '@/test/test-utils'
 *
 * test('renders component', () => {
 *   renderWithProviders(<MyComponent />)
 *   expect(screen.getByText('Hello')).toBeInTheDocument()
 * })
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options })
}

/**
 * Create a wrapper function for renderHook
 * Use this with renderHook from @testing-library/react
 *
 * @example
 * import { renderHook } from '@testing-library/react'
 * import { createWrapper } from '@/test/test-utils'
 *
 * test('custom hook', () => {
 *   const { result } = renderHook(() => useMyHook(), {
 *     wrapper: createWrapper(),
 *   })
 *   expect(result.current.data).toBeDefined()
 * })
 */
export function createWrapper() {
  return ({ children }: { children: ReactNode }) => (
    <AllTheProviders>{children}</AllTheProviders>
  )
}

// Re-export everything from React Testing Library
export * from '@testing-library/react'

// Export userEvent separately for convenience
export { userEvent } from '@testing-library/user-event'
