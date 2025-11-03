/**
 * React Hook Form - Complex Form Patterns
 *
 * SAP-023: React State Management Patterns
 * Template: form-complex.tsx
 *
 * Purpose:
 * - Dynamic field arrays (add/remove items)
 * - Nested fields
 * - Conditional fields
 * - File uploads
 * - Multi-step forms
 *
 * @see https://react-hook-form.com/docs/usefieldarray
 */

'use client'

import { useForm, useFieldArray, SubmitHandler } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useState } from 'react'

/**
 * Example 1: Dynamic Field Array (Add/Remove Items)
 *
 * - Add/remove phone numbers dynamically
 * - Each item has validation
 * - Array validation (min/max items)
 */

const contactSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  emails: z
    .array(
      z.object({
        email: z.string().email('Invalid email'),
        isPrimary: z.boolean(),
      }),
    )
    .min(1, 'At least one email is required'),
})

type ContactFormData = z.infer<typeof contactSchema>

export function DynamicEmailForm() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: '',
      emails: [{ email: '', isPrimary: true }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'emails',
  })

  const onSubmit: SubmitHandler<ContactFormData> = (data) => {
    console.log('Contact data:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Name</label>
        <input {...register('name')} className="w-full rounded border p-2" />
        {errors.name && <p className="text-red-600">{errors.name.message}</p>}
      </div>

      <div className="space-y-2">
        <label className="font-medium">Email Addresses</label>

        {fields.map((field, index) => (
          <div key={field.id} className="flex gap-2">
            <input
              {...register(`emails.${index}.email`)}
              placeholder="email@example.com"
              className="flex-1 rounded border p-2"
            />

            <label className="flex items-center gap-1">
              <input type="checkbox" {...register(`emails.${index}.isPrimary`)} />
              Primary
            </label>

            {fields.length > 1 && (
              <button
                type="button"
                onClick={() => remove(index)}
                className="rounded bg-red-500 px-2 py-1 text-white"
              >
                Remove
              </button>
            )}
          </div>
        ))}

        {errors.emails?.message && (
          <p className="text-red-600">{errors.emails.message}</p>
        )}

        {errors.emails && typeof errors.emails !== 'string' && (
          <>
            {errors.emails.map((error, index) => (
              error?.email && (
                <p key={index} className="text-red-600">
                  Email {index + 1}: {error.email.message}
                </p>
              )
            ))}
          </>
        )}

        <button
          type="button"
          onClick={() => append({ email: '', isPrimary: false })}
          className="rounded bg-blue-500 px-3 py-1 text-white"
        >
          Add Email
        </button>
      </div>

      <button type="submit" className="rounded bg-green-600 px-4 py-2 text-white">
        Submit
      </button>
    </form>
  )
}

/**
 * Example 2: Conditional Fields
 *
 * - Show/hide fields based on other field values
 * - Use watch() to monitor field values
 */

const accountSchema = z.object({
  accountType: z.enum(['personal', 'business']),
  email: z.string().email(),
  // Conditional fields
  businessName: z.string().optional(),
  taxId: z.string().optional(),
})

type AccountFormData = z.infer<typeof accountSchema>

export function ConditionalFieldsForm() {
  const {
    register,
    watch,
    handleSubmit,
    formState: { errors },
  } = useForm<AccountFormData>({
    resolver: zodResolver(accountSchema),
    defaultValues: {
      accountType: 'personal',
    },
  })

  // Watch accountType to show/hide business fields
  const accountType = watch('accountType')

  const onSubmit: SubmitHandler<AccountFormData> = (data) => {
    console.log('Account:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Account Type</label>
        <select {...register('accountType')} className="w-full rounded border p-2">
          <option value="personal">Personal</option>
          <option value="business">Business</option>
        </select>
      </div>

      <div>
        <label>Email</label>
        <input type="email" {...register('email')} className="w-full rounded border p-2" />
        {errors.email && <p className="text-red-600">{errors.email.message}</p>}
      </div>

      {/* Conditional: Show only for business accounts */}
      {accountType === 'business' && (
        <>
          <div>
            <label>Business Name</label>
            <input {...register('businessName')} className="w-full rounded border p-2" />
          </div>

          <div>
            <label>Tax ID</label>
            <input {...register('taxId')} className="w-full rounded border p-2" />
          </div>
        </>
      )}

      <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white">
        Create Account
      </button>
    </form>
  )
}

/**
 * Example 3: Multi-Step Form
 *
 * - Split form into multiple steps
 * - Validate each step
 * - Progress indicator
 */

const multiStepSchema = z.object({
  // Step 1
  email: z.string().email(),
  password: z.string().min(8),
  // Step 2
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  // Step 3
  address: z.string().min(1),
  city: z.string().min(1),
  zip: z.string().min(5),
})

type MultiStepFormData = z.infer<typeof multiStepSchema>

export function MultiStepForm() {
  const [step, setStep] = useState(1)

  const {
    register,
    handleSubmit,
    trigger,
    formState: { errors },
  } = useForm<MultiStepFormData>({
    resolver: zodResolver(multiStepSchema),
    mode: 'onBlur', // Validate on blur
  })

  const nextStep = async () => {
    let fieldsToValidate: (keyof MultiStepFormData)[] = []

    if (step === 1) fieldsToValidate = ['email', 'password']
    if (step === 2) fieldsToValidate = ['firstName', 'lastName']

    const isValid = await trigger(fieldsToValidate)
    if (isValid) setStep(step + 1)
  }

  const prevStep = () => setStep(step - 1)

  const onSubmit: SubmitHandler<MultiStepFormData> = (data) => {
    console.log('Complete data:', data)
  }

  return (
    <div className="max-w-md">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span>Step {step} of 3</span>
          <span>{Math.round((step / 3) * 100)}%</span>
        </div>
        <div className="h-2 bg-gray-200 rounded">
          <div
            className="h-2 bg-blue-600 rounded transition-all"
            style={{ width: `${(step / 3) * 100}%` }}
          />
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Step 1: Account */}
        {step === 1 && (
          <>
            <h2 className="text-xl font-bold">Account Information</h2>
            <div>
              <label>Email</label>
              <input type="email" {...register('email')} className="w-full rounded border p-2" />
              {errors.email && <p className="text-red-600">{errors.email.message}</p>}
            </div>
            <div>
              <label>Password</label>
              <input
                type="password"
                {...register('password')}
                className="w-full rounded border p-2"
              />
              {errors.password && <p className="text-red-600">{errors.password.message}</p>}
            </div>
          </>
        )}

        {/* Step 2: Personal */}
        {step === 2 && (
          <>
            <h2 className="text-xl font-bold">Personal Information</h2>
            <div>
              <label>First Name</label>
              <input {...register('firstName')} className="w-full rounded border p-2" />
              {errors.firstName && <p className="text-red-600">{errors.firstName.message}</p>}
            </div>
            <div>
              <label>Last Name</label>
              <input {...register('lastName')} className="w-full rounded border p-2" />
              {errors.lastName && <p className="text-red-600">{errors.lastName.message}</p>}
            </div>
          </>
        )}

        {/* Step 3: Address */}
        {step === 3 && (
          <>
            <h2 className="text-xl font-bold">Address</h2>
            <div>
              <label>Street Address</label>
              <input {...register('address')} className="w-full rounded border p-2" />
              {errors.address && <p className="text-red-600">{errors.address.message}</p>}
            </div>
            <div>
              <label>City</label>
              <input {...register('city')} className="w-full rounded border p-2" />
              {errors.city && <p className="text-red-600">{errors.city.message}</p>}
            </div>
            <div>
              <label>ZIP Code</label>
              <input {...register('zip')} className="w-full rounded border p-2" />
              {errors.zip && <p className="text-red-600">{errors.zip.message}</p>}
            </div>
          </>
        )}

        {/* Navigation */}
        <div className="flex justify-between">
          {step > 1 && (
            <button
              type="button"
              onClick={prevStep}
              className="rounded bg-gray-500 px-4 py-2 text-white"
            >
              Previous
            </button>
          )}

          {step < 3 ? (
            <button
              type="button"
              onClick={nextStep}
              className="ml-auto rounded bg-blue-600 px-4 py-2 text-white"
            >
              Next
            </button>
          ) : (
            <button type="submit" className="ml-auto rounded bg-green-600 px-4 py-2 text-white">
              Submit
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

/**
 * Key Concepts:
 *
 * 1. useFieldArray: Manage dynamic arrays
 *    - fields: Array items with unique IDs
 *    - append: Add new item
 *    - remove: Remove item by index
 *    - register(`arrayName.${index}.fieldName`)
 *
 * 2. watch(): Monitor field values
 *    - const value = watch('fieldName')
 *    - Re-renders on change (use sparingly)
 *    - For conditional rendering
 *
 * 3. trigger(): Manual validation
 *    - const isValid = await trigger(['field1', 'field2'])
 *    - Use for multi-step forms
 *    - Validate specific fields
 *
 * 4. mode: Validation timing
 *    - 'onSubmit': Only on submit (default)
 *    - 'onBlur': On field blur
 *    - 'onChange': On every change
 *    - 'all': All of above
 */
