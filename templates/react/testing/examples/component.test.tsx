import { describe, it, expect } from 'vitest'
import { renderWithProviders, screen, userEvent } from '@/test/test-utils'

/**
 * Example Component Test
 *
 * This demonstrates testing patterns for React components:
 * - Rendering with providers
 * - User interactions
 * - Accessibility-focused queries
 * - Async behavior
 */

// Example component (replace with your actual component)
interface CounterProps {
  initialCount?: number
  label?: string
}

function Counter({ initialCount = 0, label = 'Count' }: CounterProps) {
  const [count, setCount] = React.useState(initialCount)

  return (
    <div>
      <p>
        {label}: <span data-testid="count">{count}</span>
      </p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
      <button onClick={() => setCount((c) => c - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  )
}

describe('Counter Component', () => {
  it('renders with initial count', () => {
    renderWithProviders(<Counter initialCount={5} />)

    // Use accessible queries (getByText) when possible
    expect(screen.getByText(/count: 5/i)).toBeInTheDocument()
  })

  it('increments count when increment button is clicked', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter />)

    const incrementButton = screen.getByRole('button', { name: /increment/i })
    await user.click(incrementButton)

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })

  it('decrements count when decrement button is clicked', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter initialCount={5} />)

    const decrementButton = screen.getByRole('button', { name: /decrement/i })
    await user.click(decrementButton)

    expect(screen.getByText(/count: 4/i)).toBeInTheDocument()
  })

  it('resets count to 0 when reset button is clicked', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter initialCount={10} />)

    const resetButton = screen.getByRole('button', { name: /reset/i })
    await user.click(resetButton)

    expect(screen.getByText(/count: 0/i)).toBeInTheDocument()
  })

  it('renders with custom label', () => {
    renderWithProviders(<Counter label="Total" />)

    expect(screen.getByText(/total:/i)).toBeInTheDocument()
  })

  it('supports multiple clicks', async () => {
    const user = userEvent.setup()
    renderWithProviders(<Counter />)

    const incrementButton = screen.getByRole('button', { name: /increment/i })

    await user.click(incrementButton)
    await user.click(incrementButton)
    await user.click(incrementButton)

    expect(screen.getByText(/count: 3/i)).toBeInTheDocument()
  })
})

/**
 * Testing Tips:
 *
 * 1. Query Priority (from React Testing Library docs):
 *    - getByRole (best for accessibility)
 *    - getByLabelText (forms)
 *    - getByPlaceholderText
 *    - getByText
 *    - getByTestId (last resort)
 *
 * 2. User Interactions:
 *    - Always use userEvent.setup() before render
 *    - Await all userEvent actions
 *    - Use async/await for async behavior
 *
 * 3. Assertions:
 *    - Use @testing-library/jest-dom matchers
 *    - toBeInTheDocument(), toHaveTextContent(), etc.
 *
 * 4. Avoid:
 *    - Testing implementation details
 *    - Using container.querySelector()
 *    - Accessing component state directly
 */
