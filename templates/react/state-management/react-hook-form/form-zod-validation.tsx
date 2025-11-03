/**
 * React Hook Form + Zod Validation
 *
 * SAP-023: React State Management Patterns
 * Template: form-zod-validation.tsx
 *
 * Purpose:
 * - Type-safe validation with Zod schemas
 * - Automatic TypeScript inference
 * - Reusable schemas (client + server)
 * - Complex validation rules
 *
 * Zod Benefits:
 * - TypeScript-first (perfect type inference)
 * - Reuse schema on server (tRPC, API routes)
 * - Better error messages
 * - Composable schemas
 *
 * @see https://react-hook-form.com/get-started#SchemaValidation
 * @see https://zod.dev
 */

'use client'

import { useForm, SubmitHandler } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

/**
 * Example 1: Registration Form with Zod
 *
 * - Email, password, confirm password
 * - Password strength validation
 * - Password match validation
 * - TypeScript type inference
 */

// 1. Define Zod schema
const registrationSchema = z
  .object({
    email: z
      .string()
      .min(1, 'Email is required')
      .email('Invalid email address'),

    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number'),

    confirmPassword: z.string(),

    username: z
      .string()
      .min(3, 'Username must be at least 3 characters')
      .max(20, 'Username must be at most 20 characters')
      .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),

    age: z
      .number({ invalid_type_error: 'Age must be a number' })
      .min(18, 'You must be at least 18 years old')
      .max(120, 'Invalid age'),

    terms: z.boolean().refine((val) => val === true, {
      message: 'You must accept the terms and conditions',
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'], // Show error on confirmPassword field
  })

// 2. Infer TypeScript type from schema
type RegistrationFormData = z.infer<typeof registrationSchema>

export function RegistrationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
  })

  const onSubmit: SubmitHandler<RegistrationFormData> = async (data) => {
    console.log('Valid data:', data)
    // data is fully type-safe here!

    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Call API
    // const response = await fetch('/api/auth/register', {
    //   method: 'POST',
    //   body: JSON.stringify(data),
    // })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email */}
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="w-full rounded border p-2"
        />
        {errors.email && <p className="text-red-600">{errors.email.message}</p>}
      </div>

      {/* Username */}
      <div>
        <label htmlFor="username">Username</label>
        <input id="username" {...register('username')} className="w-full rounded border p-2" />
        {errors.username && <p className="text-red-600">{errors.username.message}</p>}
      </div>

      {/* Age */}
      <div>
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          {...register('age', { valueAsNumber: true })} // Convert to number
          className="w-full rounded border p-2"
        />
        {errors.age && <p className="text-red-600">{errors.age.message}</p>}
      </div>

      {/* Password */}
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="w-full rounded border p-2"
        />
        {errors.password && <p className="text-red-600">{errors.password.message}</p>}
      </div>

      {/* Confirm Password */}
      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          className="w-full rounded border p-2"
        />
        {errors.confirmPassword && (
          <p className="text-red-600">{errors.confirmPassword.message}</p>
        )}
      </div>

      {/* Terms Checkbox */}
      <div className="flex items-center">
        <input id="terms" type="checkbox" {...register('terms')} className="mr-2" />
        <label htmlFor="terms">I accept the terms and conditions</label>
      </div>
      {errors.terms && <p className="text-red-600">{errors.terms.message}</p>}

      {/* Submit */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {isSubmitting ? 'Creating account...' : 'Register'}
      </button>
    </form>
  )
}

/**
 * Key Concepts:
 *
 * 1. zodResolver: Connects Zod schema to React Hook Form
 *    - Validates data using Zod schema
 *    - Converts Zod errors to RHF format
 *
 * 2. z.infer: Extract TypeScript type from schema
 *    - type FormData = z.infer<typeof schema>
 *    - Perfect type safety (schema = source of truth)
 *
 * 3. .refine(): Custom validation
 *    - Validate multiple fields together (password match)
 *    - path: Which field to show error on
 *
 * 4. valueAsNumber: Convert string to number
 *    - register('age', { valueAsNumber: true })
 *    - Without this, age would be string
 */

/**
 * Example 2: Product Form with Optional Fields
 *
 * - Optional fields
 * - Default values
 * - Nested objects
 */

const productSchema = z.object({
  name: z.string().min(1, 'Product name is required'),

  price: z
    .number({ invalid_type_error: 'Price must be a number' })
    .positive('Price must be positive'),

  description: z.string().optional(), // Optional field

  category: z.enum(['electronics', 'clothing', 'food'], {
    errorMap: () => ({ message: 'Please select a category' }),
  }),

  inStock: z.boolean().default(true),

  // Nested object
  dimensions: z
    .object({
      width: z.number().positive().optional(),
      height: z.number().positive().optional(),
      depth: z.number().positive().optional(),
    })
    .optional(),

  tags: z.array(z.string()).min(1, 'At least one tag is required'),
})

type ProductFormData = z.infer<typeof productSchema>

export function ProductForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      inStock: true,
      tags: [],
    },
  })

  const onSubmit: SubmitHandler<ProductFormData> = (data) => {
    console.log('Product:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name">Product Name</label>
        <input id="name" {...register('name')} className="w-full rounded border p-2" />
        {errors.name && <p className="text-red-600">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="price">Price</label>
        <input
          id="price"
          type="number"
          step="0.01"
          {...register('price', { valueAsNumber: true })}
          className="w-full rounded border p-2"
        />
        {errors.price && <p className="text-red-600">{errors.price.message}</p>}
      </div>

      <div>
        <label htmlFor="description">Description (Optional)</label>
        <textarea id="description" {...register('description')} className="w-full rounded border p-2" rows={3} />
      </div>

      <div>
        <label htmlFor="category">Category</label>
        <select id="category" {...register('category')} className="w-full rounded border p-2">
          <option value="">Select category</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
          <option value="food">Food</option>
        </select>
        {errors.category && <p className="text-red-600">{errors.category.message}</p>}
      </div>

      <div className="flex items-center">
        <input id="inStock" type="checkbox" {...register('inStock')} className="mr-2" />
        <label htmlFor="inStock">In Stock</label>
      </div>

      <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white">
        Create Product
      </button>
    </form>
  )
}

/**
 * Zod Schema Patterns
 *
 * // String
 * z.string()
 *   .min(3, 'Too short')
 *   .max(100, 'Too long')
 *   .email('Invalid email')
 *   .url('Invalid URL')
 *   .regex(/pattern/, 'Invalid format')
 *   .trim() // Auto-trim whitespace
 *   .toLowerCase() // Auto-lowercase
 *
 * // Number
 * z.number()
 *   .min(0, 'Must be positive')
 *   .max(100, 'Too large')
 *   .int('Must be integer')
 *   .positive('Must be positive')
 *   .nonnegative('Must be non-negative')
 *
 * // Boolean
 * z.boolean()
 *   .default(false)
 *
 * // Enum
 * z.enum(['option1', 'option2'])
 *
 * // Array
 * z.array(z.string())
 *   .min(1, 'At least one item')
 *   .max(10, 'Too many items')
 *
 * // Object
 * z.object({
 *   key: z.string(),
 * })
 *
 * // Optional
 * z.string().optional()
 *
 * // Nullable
 * z.string().nullable()
 *
 * // Default
 * z.string().default('default value')
 *
 * // Transform
 * z.string().transform((val) => val.toUpperCase())
 *
 * // Union (OR)
 * z.union([z.string(), z.number()])
 * // Or use z.string().or(z.number())
 *
 * // Discriminated Union
 * z.discriminatedUnion('type', [
 *   z.object({ type: z.literal('a'), a: z.string() }),
 *   z.object({ type: z.literal('b'), b: z.number() }),
 * ])
 *
 * // Custom Validation
 * z.string().refine((val) => val !== 'admin', {
 *   message: 'Reserved word',
 * })
 */

/**
 * Reusing Schemas (Client + Server)
 *
 * // schemas/user.ts
 * export const userSchema = z.object({
 *   email: z.string().email(),
 *   password: z.string().min(8),
 * })
 *
 * // Client (React Hook Form)
 * import { userSchema } from '@/schemas/user'
 * const { register } = useForm({
 *   resolver: zodResolver(userSchema),
 * })
 *
 * // Server (Next.js API Route)
 * import { userSchema } from '@/schemas/user'
 * export async function POST(req: Request) {
 *   const body = await req.json()
 *   const validated = userSchema.parse(body) // Throws if invalid
 *   // ... use validated data
 * }
 *
 * Benefits:
 * - Single source of truth
 * - Client + server validation match
 * - TypeScript types match
 */
