/**
 * Accessible Form Component
 *
 * WCAG 2.2 Level AA compliant form with:
 * - Labels associated with inputs (for/id or aria-labelledby)
 * - Error messages linked via aria-describedby
 * - aria-invalid on invalid fields
 * - aria-live announcements for validation errors
 * - Required field indicators
 * - Keyboard navigation support
 *
 * Based on WCAG 2.2 criteria:
 * - 1.3.1 Info and Relationships
 * - 3.3.1 Error Identification
 * - 3.3.2 Labels or Instructions
 * - 3.3.3 Error Suggestion
 * - 3.3.7 Redundant Entry (auto-fill support)
 *
 * Usage:
 * ```tsx
 * <AccessibleForm
 *   onSubmit={handleSubmit}
 *   ariaLabel="Contact form"
 * >
 *   <FormField
 *     id="email"
 *     label="Email"
 *     type="email"
 *     required
 *     error={errors.email}
 *   />
 *   <FormField
 *     id="message"
 *     label="Message"
 *     as="textarea"
 *     required
 *   />
 *   <button type="submit">Send</button>
 * </AccessibleForm>
 * ```
 */

import { type FormEvent, type ReactNode } from 'react'

interface AccessibleFormProps {
  /** Form submission handler */
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
  /** Form aria-label */
  ariaLabel?: string
  /** Form aria-labelledby (alternative to ariaLabel) */
  ariaLabelledBy?: string
  /** Form children */
  children: ReactNode
  /** Optional className */
  className?: string
  /** Optional noValidate (use for custom validation) */
  noValidate?: boolean
}

export function AccessibleForm({
  onSubmit,
  ariaLabel,
  ariaLabelledBy,
  children,
  className = '',
  noValidate = true,
}: AccessibleFormProps) {
  return (
    <form
      onSubmit={onSubmit}
      aria-label={ariaLabel}
      aria-labelledby={ariaLabelledBy}
      noValidate={noValidate}
      className={className}
    >
      {/* Live region for form-level error announcements */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
        id="form-status"
      />
      {children}
    </form>
  )
}

interface FormFieldProps {
  /** Unique field ID (required for label association) */
  id: string
  /** Field label text */
  label: string
  /** Input type (default: 'text') */
  type?: 'text' | 'email' | 'password' | 'tel' | 'url' | 'number' | 'search'
  /** Render as textarea instead of input */
  as?: 'input' | 'textarea'
  /** Required field */
  required?: boolean
  /** Error message (shows below field when present) */
  error?: string
  /** Help text (shows below field) */
  helpText?: string
  /** Placeholder text (use sparingly, prefer helpText) */
  placeholder?: string
  /** Current value */
  value?: string
  /** Change handler */
  onChange?: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  /** Blur handler */
  onBlur?: (event: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  /** Autocomplete attribute (improves accessibility and UX) */
  autoComplete?: string
  /** Optional className for input */
  className?: string
  /** Disabled state */
  disabled?: boolean
}

export function FormField({
  id,
  label,
  type = 'text',
  as = 'input',
  required = false,
  error,
  helpText,
  placeholder,
  value,
  onChange,
  onBlur,
  autoComplete,
  className = '',
  disabled = false,
}: FormFieldProps) {
  const hasError = Boolean(error)
  const helpId = `${id}-help`
  const errorId = `${id}-error`

  // Build aria-describedby (combines help text and error)
  const describedBy = [
    helpText && helpId,
    hasError && errorId,
  ].filter(Boolean).join(' ') || undefined

  const inputProps = {
    id,
    name: id, // Use same name as id for form data
    required,
    disabled,
    value,
    onChange,
    onBlur,
    autoComplete,
    placeholder,
    'aria-invalid': hasError || undefined,
    'aria-describedby': describedBy,
    className: `block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 ${
      hasError
        ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
    } ${disabled ? 'cursor-not-allowed bg-gray-100' : ''} ${className}`,
  }

  return (
    <div className="mb-4">
      {/* Label with required indicator */}
      <label
        htmlFor={id}
        className="mb-1 block text-sm font-medium text-gray-700"
      >
        {label}
        {required && (
          <span className="ml-1 text-red-500" aria-label="required">
            *
          </span>
        )}
      </label>

      {/* Help text (before input for screen readers) */}
      {helpText && (
        <p id={helpId} className="mb-1 text-sm text-gray-600">
          {helpText}
        </p>
      )}

      {/* Input or Textarea */}
      {as === 'textarea' ? (
        <textarea
          {...inputProps}
          rows={4}
        />
      ) : (
        <input
          type={type}
          {...inputProps}
        />
      )}

      {/* Error message with aria-live for screen reader announcements */}
      {hasError && (
        <p
          id={errorId}
          role="alert"
          aria-live="assertive"
          className="mt-1 text-sm text-red-600"
        >
          {error}
        </p>
      )}
    </div>
  )
}

/**
 * Example: Form with React Hook Form + Zod
 *
 * ```tsx
 * import { useForm } from 'react-hook-form'
 * import { zodResolver } from '@hookform/resolvers/zod'
 * import { z } from 'zod'
 * import { AccessibleForm, FormField } from './accessible-form'
 *
 * const contactSchema = z.object({
 *   name: z.string().min(2, 'Name must be at least 2 characters'),
 *   email: z.string().email('Invalid email address'),
 *   message: z.string().min(10, 'Message must be at least 10 characters'),
 * })
 *
 * type ContactFormData = z.infer<typeof contactSchema>
 *
 * function ContactForm() {
 *   const {
 *     register,
 *     handleSubmit,
 *     formState: { errors },
 *   } = useForm<ContactFormData>({
 *     resolver: zodResolver(contactSchema),
 *   })
 *
 *   const onSubmit = (data: ContactFormData) => {
 *     console.log('Form data:', data)
 *   }
 *
 *   return (
 *     <AccessibleForm
 *       onSubmit={handleSubmit(onSubmit)}
 *       ariaLabel="Contact form"
 *     >
 *       <FormField
 *         id="name"
 *         label="Name"
 *         required
 *         error={errors.name?.message}
 *         autoComplete="name"
 *         {...register('name')}
 *       />
 *
 *       <FormField
 *         id="email"
 *         label="Email"
 *         type="email"
 *         required
 *         error={errors.email?.message}
 *         autoComplete="email"
 *         {...register('email')}
 *       />
 *
 *       <FormField
 *         id="message"
 *         label="Message"
 *         as="textarea"
 *         required
 *         error={errors.message?.message}
 *         {...register('message')}
 *       />
 *
 *       <button
 *         type="submit"
 *         className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
 *       >
 *         Send Message
 *       </button>
 *     </AccessibleForm>
 *   )
 * }
 * ```
 */

/**
 * Example: WCAG 2.2 Autocomplete Support
 *
 * Use autocomplete attribute for common fields (WCAG 3.3.7 Redundant Entry):
 *
 * ```tsx
 * <FormField
 *   id="email"
 *   label="Email"
 *   type="email"
 *   autoComplete="email"  // Browser auto-fills from saved data
 * />
 *
 * <FormField
 *   id="phone"
 *   label="Phone"
 *   type="tel"
 *   autoComplete="tel"
 * />
 *
 * <FormField
 *   id="street"
 *   label="Street Address"
 *   autoComplete="street-address"
 * />
 * ```
 *
 * Full autocomplete values:
 * https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
 */

/**
 * Testing Example (jest-axe)
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import userEvent from '@testing-library/user-event'
 * import { axe, toHaveNoViolations } from 'jest-axe'
 * import { AccessibleForm, FormField } from './accessible-form'
 *
 * expect.extend(toHaveNoViolations)
 *
 * describe('AccessibleForm', () => {
 *   it('should not have accessibility violations', async () => {
 *     const { container } = render(
 *       <AccessibleForm onSubmit={() => {}} ariaLabel="Test form">
 *         <FormField id="email" label="Email" type="email" required />
 *       </AccessibleForm>
 *     )
 *
 *     const results = await axe(container)
 *     expect(results).toHaveNoViolations()
 *   })
 *
 *   it('should associate label with input', () => {
 *     render(
 *       <AccessibleForm onSubmit={() => {}}>
 *         <FormField id="email" label="Email" />
 *       </AccessibleForm>
 *     )
 *
 *     const input = screen.getByLabelText('Email')
 *     expect(input).toHaveAttribute('id', 'email')
 *   })
 *
 *   it('should show error with aria-invalid and aria-describedby', () => {
 *     render(
 *       <AccessibleForm onSubmit={() => {}}>
 *         <FormField
 *           id="email"
 *           label="Email"
 *           error="Invalid email"
 *         />
 *       </AccessibleForm>
 *     )
 *
 *     const input = screen.getByLabelText('Email')
 *     expect(input).toHaveAttribute('aria-invalid', 'true')
 *     expect(input).toHaveAttribute('aria-describedby', 'email-error')
 *
 *     const error = screen.getByText('Invalid email')
 *     expect(error).toHaveAttribute('role', 'alert')
 *     expect(error).toHaveAttribute('aria-live', 'assertive')
 *   })
 * })
 * ```
 */
