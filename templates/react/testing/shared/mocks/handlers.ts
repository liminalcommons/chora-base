import { http, HttpResponse } from 'msw'

/**
 * MSW Request Handlers
 * Define your API mocks here
 *
 * @see https://mswjs.io/docs/
 */

// Example User type
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

  // PUT /api/users/:id
  http.put('/api/users/:id', async ({ params, request }) => {
    const { id } = params
    const updates = (await request.json()) as Partial<User>
    return HttpResponse.json<User>({
      id: id as string,
      name: 'Alice Johnson',
      email: 'alice@example.com',
      ...updates,
    })
  }),

  // DELETE /api/users/:id
  http.delete('/api/users/:id', () => {
    return new HttpResponse(null, { status: 204 })
  }),

  // Error simulation example
  http.get('/api/error', () => {
    return HttpResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    )
  }),

  // Delayed response example (useful for testing loading states)
  http.get('/api/slow', async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000))
    return HttpResponse.json({ message: 'Slow response' })
  }),
]
