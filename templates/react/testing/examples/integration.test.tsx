import { describe, it, expect } from 'vitest'
import { renderWithProviders, screen, userEvent, waitFor } from '@/test/test-utils'
import { http, HttpResponse } from 'msw'
import { server } from '@/test/mocks/server'

/**
 * Example Integration Test
 *
 * Integration tests combine multiple units (components, hooks, API calls)
 * to test realistic user flows. They provide the highest ROI for testing.
 *
 * This demonstrates:
 * - Full user flows (data fetching → display → interaction)
 * - MSW API mocking
 * - Loading and error states
 * - Form submissions
 */

// =============================================================================
// Example: User List with Add/Delete functionality
// =============================================================================

interface User {
  id: string
  name: string
  email: string
}

function UserList() {
  const { data: users, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: async (): Promise<User[]> => {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch users')
      return response.json()
    },
  })

  const addUserMutation = useMutation({
    mutationFn: async (newUser: Omit<User, 'id'>) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser),
      })
      if (!response.ok) throw new Error('Failed to add user')
      return response.json()
    },
  })

  const [name, setName] = React.useState('')
  const [email, setEmail] = React.useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    addUserMutation.mutate(
      { name, email },
      {
        onSuccess: () => {
          setName('')
          setEmail('')
        },
      }
    )
  }

  if (isLoading) return <div>Loading users...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h1>User Management</h1>

      {/* User List */}
      <ul role="list">
        {users?.map((user) => (
          <li key={user.id}>
            {user.name} ({user.email})
          </li>
        ))}
      </ul>

      {/* Add User Form */}
      <form onSubmit={handleSubmit}>
        <h2>Add New User</h2>
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={addUserMutation.isPending}>
          {addUserMutation.isPending ? 'Adding...' : 'Add User'}
        </button>
        {addUserMutation.isError && (
          <p role="alert">Error: {addUserMutation.error.message}</p>
        )}
      </form>
    </div>
  )
}

describe('UserList Integration', () => {
  it('displays loading state initially', () => {
    renderWithProviders(<UserList />)
    expect(screen.getByText(/loading users/i)).toBeInTheDocument()
  })

  it('fetches and displays users', async () => {
    renderWithProviders(<UserList />)

    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByText(/loading users/i)).not.toBeInTheDocument()
    })

    // Verify users are displayed
    expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
    expect(screen.getByText(/bob smith/i)).toBeInTheDocument()
  })

  it('handles fetch error gracefully', async () => {
    // Override handler to return error
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { error: 'Internal Server Error' },
          { status: 500 }
        )
      })
    )

    renderWithProviders(<UserList />)

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/error:/i)).toBeInTheDocument()
    })
  })

  it('adds a new user via form submission', async () => {
    const user = userEvent.setup()
    renderWithProviders(<UserList />)

    // Wait for initial load
    await waitFor(() => {
      expect(screen.queryByText(/loading users/i)).not.toBeInTheDocument()
    })

    // Fill out form
    const nameInput = screen.getByLabelText(/name/i)
    const emailInput = screen.getByLabelText(/email/i)

    await user.type(nameInput, 'Charlie Brown')
    await user.type(emailInput, 'charlie@example.com')

    // Submit form
    const submitButton = screen.getByRole('button', { name: /add user/i })
    await user.click(submitButton)

    // Verify loading state
    expect(screen.getByText(/adding.../i)).toBeInTheDocument()

    // Wait for success
    await waitFor(() => {
      expect(screen.queryByText(/adding.../i)).not.toBeInTheDocument()
    })

    // Form should be cleared
    expect(nameInput).toHaveValue('')
    expect(emailInput).toHaveValue('')
  })

  it('displays error when add user fails', async () => {
    const user = userEvent.setup()

    // Override handler to return error
    server.use(
      http.post('/api/users', () => {
        return HttpResponse.json(
          { error: 'Validation Error' },
          { status: 400 }
        )
      })
    )

    renderWithProviders(<UserList />)

    // Wait for initial load
    await waitFor(() => {
      expect(screen.queryByText(/loading users/i)).not.toBeInTheDocument()
    })

    // Fill and submit form
    await user.type(screen.getByLabelText(/name/i), 'Invalid User')
    await user.type(screen.getByLabelText(/email/i), 'invalid@example.com')
    await user.click(screen.getByRole('button', { name: /add user/i }))

    // Wait for error
    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/error:/i)
    })
  })

  it('completes full user journey: load → add → verify', async () => {
    const user = userEvent.setup()
    renderWithProviders(<UserList />)

    // Step 1: Wait for users to load
    await waitFor(() => {
      expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
    })

    // Step 2: Add new user
    await user.type(screen.getByLabelText(/name/i), 'Diana Prince')
    await user.type(screen.getByLabelText(/email/i), 'diana@example.com')
    await user.click(screen.getByRole('button', { name: /add user/i }))

    // Step 3: Verify form cleared
    await waitFor(() => {
      expect(screen.getByLabelText(/name/i)).toHaveValue('')
    })

    // This is an integration test - we verify the interaction flow
    // In a real app, you'd refetch or optimistically update the list
  })
})

/**
 * Integration Testing Tips:
 *
 * 1. Test user flows, not implementation:
 *    - Simulate what a real user would do
 *    - Click buttons, fill forms, navigate
 *
 * 2. Use MSW for realistic API mocking:
 *    - Mock at network level, not fetch directly
 *    - Override handlers per test with server.use()
 *
 * 3. Test all states:
 *    - Loading states
 *    - Success states
 *    - Error states
 *    - Empty states
 *
 * 4. Use waitFor for async:
 *    - Don't assume instant rendering
 *    - Wait for loading states to disappear
 *    - Wait for success/error messages
 *
 * 5. Test accessibility:
 *    - Use role-based queries
 *    - Verify ARIA attributes
 *    - Test keyboard navigation
 *
 * 6. Focus on business value:
 *    - Can users complete their tasks?
 *    - Do errors show helpful messages?
 *    - Does the happy path work end-to-end?
 */
