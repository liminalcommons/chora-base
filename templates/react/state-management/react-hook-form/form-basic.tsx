/**
 * React Hook Form - Basic Form Example
 *
 * SAP-023: React State Management Patterns
 * Template: form-basic.tsx
 *
 * Purpose:
 * - Demonstrate basic React Hook Form setup
 * - Uncontrolled inputs (better performance)
 * - Simple validation, error handling, submission
 *
 * React Hook Form Benefits:
 * - 50-70% better performance vs controlled forms
 * - Minimal re-renders (only on blur/submit)
 * - Built-in validation
 * - 30KB bundle (vs Formik 50KB)
 *
 * Use React Hook Form for:
 * - All forms (login, registration, checkout, etc.)
 * - Dynamic forms (add/remove fields)
 * - Multi-step forms
 * - Forms with validation
 *
 * @see https://react-hook-form.com/get-started
 */

'use client'

import { useForm, SubmitHandler } from 'react-hook-form'

/**
 * Form Data Type
 */
interface LoginFormData {
  email: string
  password: string
  rememberMe: boolean
}

/**
 * Example 1: Basic Login Form
 *
 * - Email + password fields
 * - Basic validation (required, email, minLength)
 * - Error display
 * - Submit handling
 */
export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
  })

  const onSubmit: SubmitHandler<LoginFormData> = async (data) => {
    console.log('Form data:', data)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Handle login (call API, redirect, etc.)
    // const response = await fetch('/api/auth/login', {
    //   method: 'POST',
    //   body: JSON.stringify(data),
    // })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email Field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
          className="mt-1 block w-full rounded-md border p-2"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      {/* Password Field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: {
              value: 8,
              message: 'Password must be at least 8 characters',
            },
          })}
          className="mt-1 block w-full rounded-md border p-2"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      {/* Remember Me Checkbox */}
      <div className="flex items-center">
        <input
          id="rememberMe"
          type="checkbox"
          {...register('rememberMe')}
          className="h-4 w-4 rounded border-gray-300"
        />
        <label htmlFor="rememberMe" className="ml-2 block text-sm">
          Remember me
        </label>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}

/**
 * Key Concepts:
 *
 * 1. register(): Connects input to form
 *    - Returns: { name, ref, onChange, onBlur }
 *    - Spread on input: {...register('fieldName')}
 *    - Second arg: Validation rules
 *
 * 2. handleSubmit(): Validates + calls onSubmit
 *    - Prevents default form submission
 *    - Validates all fields
 *    - Only calls onSubmit if valid
 *
 * 3. errors: Validation errors
 *    - errors.email.message, errors.password.message
 *    - Automatically cleared when field becomes valid
 *
 * 4. isSubmitting: Loading state
 *    - true during async onSubmit
 *    - Use to disable button, show spinner
 */

/**
 * Example 2: Contact Form
 *
 * - Text, email, textarea
 * - Custom validation
 * - Success message
 */
interface ContactFormData {
  name: string
  email: string
  subject: string
  message: string
}

export function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitSuccessful },
    reset,
  } = useForm<ContactFormData>()

  const onSubmit: SubmitHandler<ContactFormData> = async (data) => {
    console.log('Contact form:', data)
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Reset form after successful submission
    reset()
  }

  if (isSubmitSuccessful) {
    return (
      <div className="rounded-md bg-green-50 p-4">
        <p className="text-green-800">Message sent successfully!</p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          {...register('name', {
            required: 'Name is required',
            minLength: { value: 2, message: 'Name must be at least 2 characters' },
          })}
          className="w-full rounded border p-2"
        />
        {errors.name && <p className="text-red-600">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: 'Invalid email',
            },
          })}
          className="w-full rounded border p-2"
        />
        {errors.email && <p className="text-red-600">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="subject">Subject</label>
        <input
          id="subject"
          {...register('subject', { required: 'Subject is required' })}
          className="w-full rounded border p-2"
        />
        {errors.subject && <p className="text-red-600">{errors.subject.message}</p>}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          rows={4}
          {...register('message', {
            required: 'Message is required',
            minLength: { value: 10, message: 'Message must be at least 10 characters' },
          })}
          className="w-full rounded border p-2"
        />
        {errors.message && <p className="text-red-600">{errors.message.message}</p>}
      </div>

      <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white">
        Send Message
      </button>
    </form>
  )
}

/**
 * Additional Concepts:
 *
 * - reset(): Clear form after submission
 * - isSubmitSuccessful: True after successful submit
 * - Textarea: Works same as input
 */

/**
 * Validation Rules Reference
 *
 * register('fieldName', {
 *   required: 'Error message' | true,
 *   minLength: { value: 8, message: 'Too short' },
 *   maxLength: { value: 100, message: 'Too long' },
 *   min: { value: 0, message: 'Must be positive' },
 *   max: { value: 100, message: 'Too large' },
 *   pattern: { value: /regex/, message: 'Invalid format' },
 *   validate: (value) => value !== 'admin' || 'Reserved word',
 *   validate: {
 *     positive: (v) => v > 0 || 'Must be positive',
 *     lessThan100: (v) => v < 100 || 'Too large',
 *   },
 * })
 */

/**
 * Performance Tips
 *
 * 1. Uncontrolled inputs (default):
 *    - Fast (no re-render on every keystroke)
 *    - Use register()
 *
 * 2. Controlled inputs (when needed):
 *    - Use Controller component
 *    - Or watch() for specific fields
 *
 * 3. Validation mode:
 *    - Default: 'onSubmit' (validate on submit)
 *    - 'onBlur': Validate when field loses focus
 *    - 'onChange': Validate on every change (slower)
 *    - 'all': All of the above
 */
