/**
 * TanStack Query - useMutation Hook Examples
 *
 * SAP-023: React State Management Patterns
 * Template: use-mutation-example.ts
 *
 * Purpose:
 * - Demonstrate useMutation patterns for WRITE operations (POST/PUT/DELETE)
 * - Cover optimistic updates, error handling, query invalidation
 * - Production-ready patterns for creating, updating, deleting data
 *
 * useMutation is for WRITE operations (POST/PUT/DELETE)
 * - Does NOT auto-cache like useQuery
 * - Manually trigger with mutate() or mutateAsync()
 * - Invalidate queries after success to refetch fresh data
 * - Support optimistic updates for instant UX
 *
 * For READ operations (GET), see use-query-example.ts
 *
 * @see https://tanstack.com/query/v5/docs/react/reference/useMutation
 */

'use client' // Required for Next.js 15 Client Components

import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api-client' // See SAP-023 api-client.ts template

/**
 * Type Definitions
 */
interface Product {
  id: string
  name: string
  price: number
  category: string
  inStock: boolean
}

interface CreateProductInput {
  name: string
  price: number
  category: string
}

interface UpdateProductInput {
  name?: string
  price?: number
  category?: string
  inStock?: boolean
}

interface Todo {
  id: string
  title: string
  completed: boolean
}

/**
 * API Functions
 */
async function createProduct(input: CreateProductInput): Promise<Product> {
  const response = await api.post<Product>('/products', input)
  return response.data
}

async function updateProduct(id: string, input: UpdateProductInput): Promise<Product> {
  const response = await api.put<Product>(`/products/${id}`, input)
  return response.data
}

async function deleteProduct(id: string): Promise<void> {
  await api.delete(`/products/${id}`)
}

async function updateTodo(todo: Todo): Promise<Todo> {
  const response = await api.put<Todo>(`/todos/${todo.id}`, todo)
  return response.data
}

/**
 * Example 1: Basic Mutation (Create)
 *
 * Create a new product
 * - Invalidate products query after success (refetch list)
 * - Show error message on failure
 */
export function useCreateProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createProduct,

    onSuccess: () => {
      // Invalidate and refetch products query
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },

    onError: (error) => {
      console.error('Failed to create product:', error)
      // Show toast notification
      // toast.error('Failed to create product')
    },
  })
}

/**
 * Usage in Component:
 *
 * function CreateProductForm() {
 *   const createProduct = useCreateProduct()
 *
 *   const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
 *     e.preventDefault()
 *     const formData = new FormData(e.currentTarget)
 *
 *     createProduct.mutate({
 *       name: formData.get('name') as string,
 *       price: Number(formData.get('price')),
 *       category: formData.get('category') as string,
 *     })
 *   }
 *
 *   return (
 *     <form onSubmit={handleSubmit}>
 *       <input name="name" required />
 *       <input name="price" type="number" required />
 *       <input name="category" required />
 *       <button disabled={createProduct.isPending}>
 *         {createProduct.isPending ? 'Creating...' : 'Create Product'}
 *       </button>
 *       {createProduct.isError && (
 *         <p>Error: {createProduct.error.message}</p>
 *       )}
 *     </form>
 *   )
 * }
 *
 * Lifecycle:
 * 1. User submits form → createProduct.mutate() called
 * 2. isPending: true → button disabled
 * 3. API request sent
 * 4. Success → onSuccess runs → queries invalidated → products refetch
 * 5. isPending: false, isSuccess: true
 * 6. Product list automatically updates (query refetched)
 *
 * Alternative: mutateAsync (for await)
 * const handleSubmit = async () => {
 *   try {
 *     const product = await createProduct.mutateAsync({ ... })
 *     console.log('Created:', product)
 *     router.push(`/products/${product.id}`)
 *   } catch (error) {
 *     console.error('Failed:', error)
 *   }
 * }
 */

/**
 * Example 2: Update Mutation
 *
 * Update existing product
 * - Invalidate specific product query
 * - Invalidate products list query
 */
export function useUpdateProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, input }: { id: string; input: UpdateProductInput }) =>
      updateProduct(id, input),

    onSuccess: (updatedProduct) => {
      // Invalidate specific product query
      queryClient.invalidateQueries({ queryKey: ['products', updatedProduct.id] })

      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}

/**
 * Usage:
 *
 * function EditProductForm({ product }: { product: Product }) {
 *   const updateProduct = useUpdateProduct()
 *
 *   const handleSubmit = (input: UpdateProductInput) => {
 *     updateProduct.mutate({ id: product.id, input })
 *   }
 *
 *   return (
 *     <form onSubmit={(e) => {
 *       e.preventDefault()
 *       handleSubmit({ name: 'New Name' })
 *     }}>
 *       <input defaultValue={product.name} />
 *       <button disabled={updateProduct.isPending}>Update</button>
 *     </form>
 *   )
 * }
 */

/**
 * Example 3: Delete Mutation
 *
 * Delete product
 * - Invalidate queries
 * - Navigate away after success
 */
export function useDeleteProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteProduct,

    onSuccess: (_, deletedId) => {
      // Remove product from cache
      queryClient.setQueryData<Product[]>(['products'], (old) =>
        old?.filter((p) => p.id !== deletedId),
      )

      // Or invalidate to refetch
      // queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}

/**
 * Usage:
 *
 * function ProductActions({ productId }: { productId: string }) {
 *   const deleteProduct = useDeleteProduct()
 *   const router = useRouter()
 *
 *   const handleDelete = async () => {
 *     if (confirm('Delete this product?')) {
 *       await deleteProduct.mutateAsync(productId)
 *       router.push('/products')
 *     }
 *   }
 *
 *   return (
 *     <button onClick={handleDelete} disabled={deleteProduct.isPending}>
 *       {deleteProduct.isPending ? 'Deleting...' : 'Delete'}
 *     </button>
 *   )
 * }
 *
 * Note: Using mutateAsync for sequential operations (delete → navigate)
 */

/**
 * Example 4: Optimistic Updates
 *
 * Update UI immediately before server responds
 * - Best UX: feels instant
 * - Rollback if server fails
 * - Pattern: onMutate (optimistic) → onError (rollback) → onSettled (refetch)
 */
export function useUpdateTodoOptimistic() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateTodo,

    /**
     * onMutate: Called before mutationFn
     *
     * 1. Cancel outgoing refetches (don't overwrite optimistic update)
     * 2. Snapshot current data (for rollback)
     * 3. Optimistically update cache
     * 4. Return context (snapshot for rollback)
     */
    onMutate: async (updatedTodo) => {
      // Cancel any outgoing refetches (so they don't overwrite our optimistic update)
      await queryClient.cancelQueries({ queryKey: ['todos'] })

      // Snapshot the previous value
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos'])

      // Optimistically update cache
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.map((todo) => (todo.id === updatedTodo.id ? updatedTodo : todo)),
      )

      // Return context with snapshot
      return { previousTodos }
    },

    /**
     * onError: Called if mutation fails
     *
     * Rollback to previous state using snapshot from context
     */
    onError: (error, updatedTodo, context) => {
      console.error('Update failed, rolling back:', error)

      // Rollback to previous state
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos)
      }

      // Show error toast
      // toast.error('Failed to update todo')
    },

    /**
     * onSettled: Called after success or error
     *
     * Refetch to sync with server (regardless of success/error)
     */
    onSettled: () => {
      // Always refetch after mutation (sync with server)
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}

/**
 * Usage (Toggle Todo):
 *
 * function TodoItem({ todo }: { todo: Todo }) {
 *   const updateTodo = useUpdateTodoOptimistic()
 *
 *   const handleToggle = () => {
 *     updateTodo.mutate({
 *       ...todo,
 *       completed: !todo.completed,
 *     })
 *   }
 *
 *   return (
 *     <div>
 *       <input
 *         type="checkbox"
 *         checked={todo.completed}
 *         onChange={handleToggle}
 *       />
 *       <span>{todo.title}</span>
 *     </div>
 *   )
 * }
 *
 * UX Flow:
 * 1. User clicks checkbox
 * 2. onMutate: UI updates immediately (checkbox checked)
 * 3. mutationFn: API request sent
 * 4. Success: onSettled refetches to confirm
 * 5. Error: onError rolls back (checkbox unchecked)
 *
 * User sees instant feedback, but if server fails, change is reverted
 */

/**
 * Example 5: Mutation with Callbacks
 *
 * Execute custom logic on success/error
 * - Show toast notifications
 * - Navigate to new page
 * - Reset form
 */
export function useCreateProductWithCallbacks() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createProduct,

    onMutate: () => {
      console.log('Creating product...')
      // Show loading toast
      // const toastId = toast.loading('Creating product...')
      // return { toastId }
    },

    onSuccess: (newProduct, variables, context) => {
      console.log('Product created:', newProduct)
      console.log('Input variables:', variables)

      // Update loading toast to success
      // if (context?.toastId) {
      //   toast.success('Product created!', { id: context.toastId })
      // }

      // Invalidate queries
      queryClient.invalidateQueries({ queryKey: ['products'] })

      // Navigate to product page
      // router.push(`/products/${newProduct.id}`)
    },

    onError: (error, variables, context) => {
      console.error('Failed to create product:', error)
      console.log('Variables:', variables)

      // Update loading toast to error
      // if (context?.toastId) {
      //   toast.error('Failed to create product', { id: context.toastId })
      // }
    },

    onSettled: (data, error, variables, context) => {
      console.log('Mutation settled (success or error)')
      // Cleanup logic here
    },
  })
}

/**
 * Callback Parameters:
 *
 * onMutate(variables):
 * - variables: Input passed to mutate()
 * - Return: Context object (available in other callbacks)
 *
 * onSuccess(data, variables, context):
 * - data: Response from mutationFn
 * - variables: Input passed to mutate()
 * - context: Return value from onMutate
 *
 * onError(error, variables, context):
 * - error: Error object
 * - variables: Input passed to mutate()
 * - context: Return value from onMutate
 *
 * onSettled(data, error, variables, context):
 * - data: Response (if success) or undefined
 * - error: Error (if failure) or null
 * - variables: Input passed to mutate()
 * - context: Return value from onMutate
 */

/**
 * Advanced: Global Mutation Defaults
 *
 * Set default callbacks for ALL mutations
 *
 * In query-client.ts:
 * export const queryClient = new QueryClient({
 *   defaultOptions: {
 *     mutations: {
 *       onError: (error) => {
 *         console.error('Mutation error:', error)
 *         toast.error('Something went wrong')
 *       },
 *       onSuccess: () => {
 *         console.log('Mutation succeeded')
 *       },
 *       retry: 0, // Don't retry mutations (avoid duplicates)
 *     },
 *   },
 * })
 *
 * Individual mutations can override these defaults
 */

/**
 * Advanced: Multiple Mutations in Parallel
 *
 * Run multiple mutations simultaneously
 *
 * const createProduct1 = useCreateProduct()
 * const createProduct2 = useCreateProduct()
 *
 * const handleCreateMultiple = async () => {
 *   await Promise.all([
 *     createProduct1.mutateAsync({ ... }),
 *     createProduct2.mutateAsync({ ... }),
 *   ])
 *   console.log('Both products created!')
 * }
 *
 * Warning: Only use parallel mutations if they're independent
 * If one depends on another, use sequential (await first, then second)
 */

/**
 * Advanced: Invalidate vs Set Query Data
 *
 * Two ways to update cache after mutation:
 *
 * 1. Invalidate (refetch from server):
 *    queryClient.invalidateQueries({ queryKey: ['products'] })
 *    - Triggers refetch
 *    - Always accurate (server is source of truth)
 *    - Extra network request
 *
 * 2. Set Query Data (manual update):
 *    queryClient.setQueryData(['products'], (old) => [...old, newProduct])
 *    - No network request
 *    - Faster UX
 *    - Risk of stale data if server changes
 *
 * Recommendation: Invalidate for simplicity, setQueryData for performance
 */

/**
 * TypeScript Tips
 *
 * 1. Type mutation function:
 *    const mutation = useMutation<Product, Error, CreateProductInput>({
 *      mutationFn: createProduct,
 *    })
 *    // Product: return type
 *    // Error: error type
 *    // CreateProductInput: variables type
 *
 * 2. Type context:
 *    interface MutationContext {
 *      previousTodos: Todo[]
 *      toastId: string
 *    }
 *
 *    const mutation = useMutation<Todo, Error, Todo, MutationContext>({
 *      onMutate: () => ({ previousTodos: [], toastId: '' }),
 *      onError: (err, vars, context) => {
 *        // context is typed as MutationContext
 *      },
 *    })
 *
 * 3. Infer types from mutationFn:
 *    const mutation = useMutation({ mutationFn: createProduct })
 *    // Types inferred from createProduct signature
 */
