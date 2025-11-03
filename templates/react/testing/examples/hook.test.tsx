import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { createWrapper } from '@/test/test-utils'

/**
 * Example Hook Tests
 *
 * This demonstrates testing patterns for React hooks:
 * - Custom hooks with state
 * - TanStack Query hooks
 * - Zustand stores
 * - Async behavior
 */

// =============================================================================
// Example 1: Testing a simple custom hook
// =============================================================================

function useCounter(initialValue = 0) {
  const [count, setCount] = React.useState(initialValue)

  const increment = () => setCount((c) => c + 1)
  const decrement = () => setCount((c) => c - 1)
  const reset = () => setCount(initialValue)

  return { count, increment, decrement, reset }
}

describe('useCounter Hook', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10))
    expect(result.current.count).toBe(10)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounter())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })
})

// =============================================================================
// Example 2: Testing TanStack Query hook
// =============================================================================

interface User {
  id: string
  name: string
  email: string
}

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async (): Promise<User[]> => {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch users')
      return response.json()
    },
  })
}

describe('useUsers Hook (TanStack Query)', () => {
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
    expect(result.current.data?.[0]).toHaveProperty('name', 'Alice Johnson')
  })

  it('handles errors', async () => {
    // Override handler to return error
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { error: 'Server Error' },
          { status: 500 }
        )
      })
    )

    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
    expect(result.current.error).toBeDefined()
  })
})

// =============================================================================
// Example 3: Testing Zustand store
// =============================================================================

interface CounterStore {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))

describe('CounterStore (Zustand)', () => {
  beforeEach(() => {
    // Reset store between tests
    useCounterStore.setState({ count: 0 })
  })

  it('has initial state', () => {
    const { result } = renderHook(() => useCounterStore())
    expect(result.current.count).toBe(0)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounterStore())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements count', () => {
    const { result } = renderHook(() => useCounterStore())

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.decrement()
    })

    expect(result.current.count).toBe(1)
  })

  it('resets count', () => {
    const { result } = renderHook(() => useCounterStore())

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(0)
  })

  it('updates across multiple hook instances', () => {
    const { result: result1 } = renderHook(() => useCounterStore())
    const { result: result2 } = renderHook(() => useCounterStore())

    act(() => {
      result1.current.increment()
    })

    // Both instances see the same state
    expect(result1.current.count).toBe(1)
    expect(result2.current.count).toBe(1)
  })
})

/**
 * Hook Testing Tips:
 *
 * 1. Always wrap state updates in act():
 *    act(() => { result.current.doSomething() })
 *
 * 2. Use waitFor for async operations:
 *    await waitFor(() => expect(result.current.isSuccess).toBe(true))
 *
 * 3. For TanStack Query hooks:
 *    - Use createWrapper() to provide QueryClient
 *    - Check isLoading, isSuccess, isError states
 *    - Use MSW to mock API responses
 *
 * 4. For Zustand stores:
 *    - Reset state in beforeEach
 *    - Test that state updates propagate to all consumers
 *
 * 5. Avoid:
 *    - Testing React internals
 *    - Not wrapping updates in act()
 *    - Forgetting to await async operations
 */
