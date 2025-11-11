# SAP-041: React Form Validation - Common Workflows

**SAP**: SAP-041 (react-form-validation)
**Domain**: Workflows
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **3 step-by-step implementation workflows** for React Hook Form + Zod validation in Next.js 15+ projects.

**Workflows**:
1. **Workflow 1**: Create Simple Login Form (5 minutes)
2. **Workflow 2**: Add Server Validation to Existing Form (10 minutes)
3. **Workflow 3**: Build Multi-Step Wizard (30 minutes)

**For form complexity guidance**, see [../form-patterns/AGENTS.md](../form-patterns/AGENTS.md)

**For accessibility patterns**, see [../accessibility/AGENTS.md](../accessibility/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

**For complete technical reference**, see [../protocol-spec.md](../protocol-spec.md)

---

## Workflow 1: Create Simple Login Form (5 min)

**Use case**: User needs basic login form with email and password

**Complexity**: Tier 1 (Simple Form)

**Time**: 5 minutes

**Steps**:

### Step 1: Define Zod schema

```typescript
// lib/validations/auth.ts
import { z } from "zod"

export const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required")
})

export type LoginFormData = z.infer<typeof loginSchema>
```

**Key points**:
- Single source of truth for validation + types
- `z.infer<typeof schema>` generates TypeScript type automatically
- Custom error messages provide user guidance

---

### Step 2: Create form component

```typescript
// components/forms/LoginForm.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { loginSchema, type LoginFormData } from "@/lib/validations/auth"

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  })

  async function onSubmit(data: LoginFormData) {
    console.log("Login data:", data)
    // TODO: Send to server
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email Address <span className="text-red-600">*</span>
        </label>
        <input
          id="email"
          {...register("email")}
          type="email"
          aria-invalid={errors.email ? "true" : "false"}
          aria-describedby={errors.email ? "email-error" : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {errors.email && (
          <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password <span className="text-red-600">*</span>
        </label>
        <input
          id="password"
          {...register("password")}
          type="password"
          aria-invalid={errors.password ? "true" : "false"}
          aria-describedby={errors.password ? "password-error" : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {errors.password && (
          <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? "Logging in..." : "Login"}
      </button>
    </form>
  )
}
```

**Key points**:
- `{...register("email")}` creates uncontrolled component (no re-renders on keystroke)
- `aria-invalid` and `aria-describedby` for accessibility (WCAG 2.2 Level AA)
- `role="alert"` announces errors to screen readers
- Loading state with `isSubmitting` from `formState`

---

### Step 3: Use in page

```typescript
// app/login/page.tsx
import { LoginForm } from "@/components/forms/LoginForm"

export default function LoginPage() {
  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6">Login</h1>
      <LoginForm />
    </div>
  )
}
```

**Result**: Fully functional login form with client-side validation in 5 minutes.

**Validation mode**: `onSubmit` (default) - validates when form is submitted

**Next steps**:
- Add server validation (see Workflow 2)
- Integrate with authentication (SAP-033)
- Add accessibility testing (SAP-026)

---

## Workflow 2: Add Server Validation to Existing Form (10 min)

**Use case**: User has client-side form, wants to add server validation for security

**Complexity**: Tier 2 (Medium Form)

**Time**: 10 minutes

**Why server validation?** Client validation can be bypassed via DevTools or cURL. Server validation is mandatory for security.

**Steps**:

### Step 1: Ensure Zod schema exists

```typescript
// lib/validations/auth.ts
export const signupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})
```

**Reuse the same schema** on both client and server (DRY principle).

---

### Step 2: Create Server Action

```typescript
// actions/auth.ts
"use server"

import { signupSchema } from "@/lib/validations/auth"
import { redirect } from "next/navigation"

export async function signup(prevState: any, formData: FormData) {
  // Extract form data
  const rawData = {
    email: formData.get("email"),
    password: formData.get("password")
  }

  // Validate with Zod
  const validatedFields = signupSchema.safeParse(rawData)

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Validation failed"
    }
  }

  // TODO: Create user in database
  // const user = await prisma.user.create({
  //   data: {
  //     email: validatedFields.data.email,
  //     password: await hash(validatedFields.data.password)
  //   }
  // })

  // Success - redirect to dashboard
  redirect("/dashboard")
}
```

**Key points**:
- `"use server"` directive at top of file (required for Server Actions)
- `safeParse()` returns `{ success: boolean, data?: T, error?: ZodError }`
- `flatten().fieldErrors` converts Zod errors to `{ email: ["error"], password: ["error"] }` format
- Return errors to client if validation fails
- Redirect on success (cannot return from Server Actions after redirect)

---

### Step 3: Update form component to use useActionState

```typescript
// components/forms/SignupForm.tsx
"use client"

import { useActionState } from "react"
import { signup } from "@/actions/auth"

export function SignupForm() {
  const [state, formAction, isPending] = useActionState(signup, null)

  return (
    <form action={formAction} className="space-y-4">
      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email Address <span className="text-red-600">*</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-invalid={state?.errors?.email ? "true" : "false"}
          aria-describedby={state?.errors?.email ? "email-error" : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {state?.errors?.email && (
          <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password <span className="text-red-600">*</span>
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          aria-invalid={state?.errors?.password ? "true" : "false"}
          aria-describedby={state?.errors?.password ? "password-error" : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {state?.errors?.password && (
          <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
            {state.errors.password[0]}
          </p>
        )}
      </div>

      {/* Global error message */}
      {state?.message && (
        <div role="alert" className="p-3 bg-red-50 text-red-800 rounded-md">
          {state.message}
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={isPending}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isPending ? "Creating account..." : "Sign Up"}
      </button>
    </form>
  )
}
```

**Key differences from Workflow 1**:
- Uses `useActionState(action, initialState)` instead of `useForm()` + `handleSubmit()`
- Form uses native `action={formAction}` instead of `onSubmit` handler
- Fields use `name` attribute (required for `FormData`) instead of `{...register()}`
- Errors come from `state?.errors` (from Server Action) instead of `formState.errors`
- `isPending` indicates server action is running

**Progressive enhancement**: Form works without JavaScript (native form submission to Server Action).

**Result**: Form now validates on both client (UX) and server (security), with progressive enhancement (works without JavaScript).

**Next steps**:
- Integrate with database (SAP-034)
- Add authentication (SAP-033)
- Add optimistic UI updates (SAP-023)

---

## Workflow 3: Build Multi-Step Wizard (30 min)

**Use case**: User needs onboarding flow with 3 steps: Account → Profile → Preferences

**Complexity**: Tier 4 (Wizard Form)

**Time**: 30 minutes

**Steps**:

### Step 1: Define schemas for each step

```typescript
// lib/validations/onboarding.ts
import { z } from "zod"

export const step1Schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters")
})

export const step2Schema = z.object({
  name: z.string().min(1, "Name is required"),
  company: z.string().min(1, "Company is required"),
  role: z.string().min(1, "Role is required")
})

export const step3Schema = z.object({
  newsletter: z.boolean(),
  notifications: z.boolean(),
  theme: z.enum(["light", "dark", "system"])
})

export type OnboardingStep1 = z.infer<typeof step1Schema>
export type OnboardingStep2 = z.infer<typeof step2Schema>
export type OnboardingStep3 = z.infer<typeof step3Schema>
```

**Key points**:
- Separate schema per step (validates current step only)
- Each schema is independent
- Final submission combines all steps

---

### Step 2: Create wizard component

```typescript
// components/forms/OnboardingWizard.tsx
"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useRouter, useSearchParams } from "next/navigation"
import {
  step1Schema,
  step2Schema,
  step3Schema,
  type OnboardingStep1,
  type OnboardingStep2,
  type OnboardingStep3
} from "@/lib/validations/onboarding"

export function OnboardingWizard() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const step = parseInt(searchParams.get("step") || "1")
  const [formData, setFormData] = useState<Partial<OnboardingStep1 & OnboardingStep2 & OnboardingStep3>>({})

  // Select schema based on current step
  const schema = step === 1 ? step1Schema : step === 2 ? step2Schema : step3Schema

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: formData
  })

  function nextStep(data: any) {
    setFormData({ ...formData, ...data })
    router.push(`?step=${step + 1}`)
  }

  function prevStep() {
    router.push(`?step=${step - 1}`)
  }

  async function onFinalSubmit(data: any) {
    const finalData = { ...formData, ...data }
    console.log("Final onboarding data:", finalData)

    // TODO: Send to server
    // await createUser(finalData)

    router.push("/dashboard")
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium">Step {step} of 3</span>
          <span className="text-sm text-gray-600">
            {step === 1 ? "Account" : step === 2 ? "Profile" : "Preferences"}
          </span>
        </div>
        <div className="w-full bg-gray-200 h-2 rounded">
          <div
            className="bg-blue-600 h-2 rounded transition-all"
            style={{ width: `${(step / 3) * 100}%` }}
          />
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit(step === 3 ? onFinalSubmit : nextStep)} className="space-y-6">
        {/* Step 1: Account */}
        {step === 1 && (
          <>
            <h2 className="text-2xl font-bold">Create your account</h2>

            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-1">
                Email Address <span className="text-red-600">*</span>
              </label>
              <input
                id="email"
                {...register("email")}
                type="email"
                aria-invalid={errors.email ? "true" : "false"}
                aria-describedby={errors.email ? "email-error" : undefined}
                className="w-full px-3 py-2 border rounded-md"
              />
              {errors.email && (
                <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-1">
                Password <span className="text-red-600">*</span>
              </label>
              <input
                id="password"
                {...register("password")}
                type="password"
                aria-invalid={errors.password ? "true" : "false"}
                aria-describedby={errors.password ? "password-error" : undefined}
                className="w-full px-3 py-2 border rounded-md"
              />
              {errors.password && (
                <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
                  {errors.password.message}
                </p>
              )}
            </div>
          </>
        )}

        {/* Step 2: Profile */}
        {step === 2 && (
          <>
            <h2 className="text-2xl font-bold">Tell us about yourself</h2>

            <div>
              <label htmlFor="name" className="block text-sm font-medium mb-1">
                Full Name <span className="text-red-600">*</span>
              </label>
              <input
                id="name"
                {...register("name")}
                type="text"
                aria-invalid={errors.name ? "true" : "false"}
                aria-describedby={errors.name ? "name-error" : undefined}
                className="w-full px-3 py-2 border rounded-md"
              />
              {errors.name && (
                <p id="name-error" role="alert" className="mt-1 text-sm text-red-600">
                  {errors.name.message}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="company" className="block text-sm font-medium mb-1">
                Company <span className="text-red-600">*</span>
              </label>
              <input
                id="company"
                {...register("company")}
                type="text"
                aria-invalid={errors.company ? "true" : "false"}
                aria-describedby={errors.company ? "company-error" : undefined}
                className="w-full px-3 py-2 border rounded-md"
              />
              {errors.company && (
                <p id="company-error" role="alert" className="mt-1 text-sm text-red-600">
                  {errors.company.message}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium mb-1">
                Role <span className="text-red-600">*</span>
              </label>
              <input
                id="role"
                {...register("role")}
                type="text"
                aria-invalid={errors.role ? "true" : "false"}
                aria-describedby={errors.role ? "role-error" : undefined}
                className="w-full px-3 py-2 border rounded-md"
              />
              {errors.role && (
                <p id="role-error" role="alert" className="mt-1 text-sm text-red-600">
                  {errors.role.message}
                </p>
              )}
            </div>
          </>
        )}

        {/* Step 3: Preferences */}
        {step === 3 && (
          <>
            <h2 className="text-2xl font-bold">Set your preferences</h2>

            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  {...register("newsletter")}
                  type="checkbox"
                  className="mr-2"
                />
                <span>Subscribe to newsletter</span>
              </label>

              <label className="flex items-center">
                <input
                  {...register("notifications")}
                  type="checkbox"
                  className="mr-2"
                />
                <span>Enable email notifications</span>
              </label>
            </div>

            <div>
              <label htmlFor="theme" className="block text-sm font-medium mb-1">
                Theme Preference
              </label>
              <select
                id="theme"
                {...register("theme")}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System</option>
              </select>
            </div>
          </>
        )}

        {/* Navigation */}
        <div className="flex justify-between pt-4">
          {step > 1 && (
            <button
              type="button"
              onClick={prevStep}
              className="px-4 py-2 border rounded-md hover:bg-gray-50"
            >
              Back
            </button>
          )}
          <button
            type="submit"
            disabled={isSubmitting}
            className="ml-auto px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {isSubmitting
              ? "Processing..."
              : step === 3
              ? "Complete Setup"
              : "Next"}
          </button>
        </div>
      </form>
    </div>
  )
}
```

**Key points**:
- URL-based step persistence (`useSearchParams` + `router.push`)
- Browser back/forward buttons work (progressive enhancement)
- Progress indicator shows current step
- Schema changes per step (validates only current step fields)
- Form data persisted in React state across steps
- Back button allows review/editing of previous steps

---

### Step 3: Create wizard page

```typescript
// app/onboarding/page.tsx
import { OnboardingWizard } from "@/components/forms/OnboardingWizard"

export default function OnboardingPage() {
  return <OnboardingWizard />
}
```

**Result**: 3-step wizard with URL-based navigation, per-step validation, progress indicator, and form data persistence across steps.

**Benefits of URL-based persistence**:
- Shareable URLs (can bookmark specific step)
- Browser back/forward buttons work
- Progressive enhancement (URL reflects application state)
- No session storage needed

**Next steps**:
- Add server validation with Server Actions (Workflow 2)
- Persist wizard state to database between sessions
- Add step validation on back button (optional)

---

## Workflow Summary

| Workflow | Complexity | Time | Use Case |
|----------|------------|------|----------|
| **Workflow 1** | Tier 1 (Simple) | 5 min | Login form with client validation |
| **Workflow 2** | Tier 2 (Medium) | 10 min | Add server validation for security |
| **Workflow 3** | Tier 4 (Wizard) | 30 min | Multi-step onboarding with URL persistence |

**Total time for all 3 workflows**: 45 minutes

**Next steps after workflows**:
- Review [../form-patterns/AGENTS.md](../form-patterns/AGENTS.md) for form complexity decision tree
- Review [../accessibility/AGENTS.md](../accessibility/AGENTS.md) for WCAG 2.2 Level AA compliance
- Review [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md) for common issues

---

## Version History

**1.0.0 (2025-11-10)** - Initial workflows extraction from awareness-guide.md
- Workflow 1: Create Simple Login Form (5 min)
- Workflow 2: Add Server Validation (10 min)
- Workflow 3: Build Multi-Step Wizard (30 min)
