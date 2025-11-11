# SAP-041: React Form Validation - Adoption Blueprint

**SAP**: SAP-041 (react-form-validation)
**Version**: 1.0.0
**Status**: pilot
**Last Updated**: 2025-11-09

---

## Overview

This guide walks you through setting up React Hook Form + Zod form validation in your Next.js 15+ project in **20 minutes**.

**What you'll build**:
- Client-side validation with React Hook Form
- Server-side validation with Zod + Server Actions
- TypeScript type inference from Zod schemas
- WCAG 2.2 Level AA accessible forms
- Progressive enhancement (works without JavaScript)

**Time commitment**: 20 minutes
**Skill level**: Intermediate React/Next.js

---

## Prerequisites

### Required Technologies

- **Next.js 15.1+** (App Router required)
- **React 19+** (for `useActionState` hook)
- **TypeScript 5.3+**
- **Node.js 18+**

### Verification

Run these commands to verify your environment:

```bash
# Check Next.js version (should be 15.1+)
npx next --version

# Check Node.js version (should be 18+)
node --version

# Check if TypeScript is installed
npx tsc --version
```

**Expected output**:
```
15.1.0 (or higher)
v18.x.x (or higher)
5.3.x (or higher)
```

### Project Structure

This guide assumes you have a Next.js 15+ App Router project with this structure:

```
your-project/
├── app/
│   └── (routes)/
├── components/
├── lib/
└── package.json
```

If you don't have a Next.js project yet:

```bash
npx create-next-app@latest my-app --typescript --app
cd my-app
```

---

## Installation (5 minutes)

### Step 1: Install Dependencies (1 min)

Install React Hook Form, Zod, and the resolver:

```bash
npm install react-hook-form zod @hookform/resolvers
```

**Package details**:
- `react-hook-form`: Form state management (12KB gzipped)
- `zod`: TypeScript-first validation (12KB gzipped)
- `@hookform/resolvers`: Integrates Zod with React Hook Form (<1KB gzipped)

**Total bundle size**: ~25KB gzipped

---

### Step 2: Create Validation Schemas Directory (30 sec)

Create a directory for Zod schemas:

```bash
mkdir -p lib/validations
touch lib/validations/auth.ts
```

**Why separate schemas**:
- Reuse schemas client + server (DRY)
- Single source of truth for validation
- Easy to find and update validation rules

---

### Step 3: Define Your First Zod Schema (3 min)

Create `lib/validations/auth.ts`:

```typescript
import { z } from "zod"

// Signup form schema
export const signupSchema = z.object({
  email: z.string()
    .min(1, "Email is required")
    .email("Invalid email address"),

  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[a-z]/, "Password must contain at least one lowercase letter")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),

  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"] // Error will appear on confirmPassword field
})

// Infer TypeScript type from schema (no manual types needed!)
export type SignupFormData = z.infer<typeof signupSchema>

// Login form schema
export const loginSchema = z.object({
  email: z.string()
    .min(1, "Email is required")
    .email("Invalid email address"),

  password: z.string()
    .min(1, "Password is required")
})

export type LoginFormData = z.infer<typeof loginSchema>
```

**Key concepts**:
- `z.object()`: Define object schema
- `.min()`, `.email()`, `.regex()`: Validation rules
- `.refine()`: Cross-field validation (e.g., password confirmation)
- `z.infer<typeof schema>`: Infer TypeScript type from schema (no manual types!)

---

### Step 4: Verify Installation (30 sec)

Check that packages were installed correctly:

```bash
npm list react-hook-form zod @hookform/resolvers
```

**Expected output**:
```
your-project@0.1.0
├── @hookform/resolvers@3.x.x
├── react-hook-form@7.x.x
└── zod@3.x.x
```

---

## Quick Start: Your First Form (15 minutes)

You have two options:

- **Option A**: Client-side only form (5 min) - Simple, but less secure
- **Option B**: Full-stack form with Server Actions (15 min) - Production-ready

Choose **Option B** for production applications.

---

## Option A: Client-Side Only Form (5 min)

**Use case**: Simple forms with basic validation, no sensitive data

**When to use**:
- Login forms (validation only, actual auth uses Server Actions)
- Newsletter signup
- Search bars
- Contact forms (non-critical data)

**Security note**: Client validation can be bypassed via DevTools. Always use Option B (Server Actions) for sensitive data.

---

### Step 1: Create Form Component (3 min)

Create `components/forms/SignupForm.tsx`:

```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { signupSchema, type SignupFormData } from "@/lib/validations/auth"

export function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema)
  })

  async function onSubmit(data: SignupFormData) {
    console.log("Form data:", data)
    // TODO: Send to server (see Option B for Server Actions)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email field */}
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
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.email && (
          <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password field */}
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
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.password && (
          <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* Confirm Password field */}
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
          Confirm Password <span className="text-red-600">*</span>
        </label>
        <input
          id="confirmPassword"
          {...register("confirmPassword")}
          type="password"
          aria-invalid={errors.confirmPassword ? "true" : "false"}
          aria-describedby={errors.confirmPassword ? "confirmPassword-error" : undefined}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.confirmPassword && (
          <p id="confirmPassword-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        {isSubmitting ? "Creating account..." : "Sign Up"}
      </button>
    </form>
  )
}
```

**Code breakdown**:

1. **`useForm()`**: Initialize form with Zod resolver
   ```typescript
   const { register, handleSubmit, formState } = useForm({
     resolver: zodResolver(signupSchema)
   })
   ```

2. **`register()`**: Connect input to form state (uncontrolled component)
   ```typescript
   <input {...register("email")} />
   ```

3. **`formState.errors`**: Access validation errors
   ```typescript
   {errors.email && <p>{errors.email.message}</p>}
   ```

4. **Accessibility attributes**:
   - `aria-invalid`: Identifies fields with errors
   - `aria-describedby`: Links error message to field
   - `role="alert"`: Announces errors to screen readers

---

### Step 2: Use Form in Page (1 min)

Create `app/signup/page.tsx`:

```typescript
import { SignupForm } from "@/components/forms/SignupForm"

export default function SignupPage() {
  return (
    <div className="max-w-md mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-6">Create an account</h1>
      <SignupForm />
    </div>
  )
}
```

---

### Step 3: Test the Form (1 min)

1. Start dev server:
   ```bash
   npm run dev
   ```

2. Navigate to `http://localhost:3000/signup`

3. Test validation:
   - Submit empty form → See "Email is required" error
   - Enter invalid email (`test`) → See "Invalid email address"
   - Enter short password (`pass`) → See "Password must be at least 8 characters"
   - Enter mismatched passwords → See "Passwords don't match"
   - Enter valid data → Form submits, data logged to console

**Result**: Working client-side form validation in 5 minutes!

---

## Option B: Full-Stack Form with Server Actions (15 min)

**Use case**: Production forms with sensitive data

**When to use**:
- User registration/signup
- Profile updates
- Payment forms
- Any form with sensitive data

**Security**: Client + Server validation (cannot bypass with DevTools)

---

### Step 1: Create Server Action (5 min)

Create `actions/auth.ts`:

```typescript
"use server"

import { signupSchema } from "@/lib/validations/auth"
import { redirect } from "next/navigation"

export async function signup(prevState: any, formData: FormData) {
  // Extract form data
  const rawData = {
    email: formData.get("email"),
    password: formData.get("password"),
    confirmPassword: formData.get("confirmPassword")
  }

  // Validate with Zod
  const validatedFields = signupSchema.safeParse(rawData)

  // Return errors if validation fails
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Validation failed. Please check your inputs."
    }
  }

  // TODO: Create user in database (see SAP-034 for Prisma/Drizzle integration)
  // Example:
  // const hashedPassword = await bcrypt.hash(validatedFields.data.password, 10)
  // const user = await prisma.user.create({
  //   data: {
  //     email: validatedFields.data.email,
  //     password: hashedPassword
  //   }
  // })

  // Simulate database operation
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Success - redirect to login or dashboard
  redirect("/login")
}
```

**Code breakdown**:

1. **`"use server"`**: Directive marking this as a Server Action
2. **`formData.get()`**: Extract form data (works without JavaScript)
3. **`safeParse()`**: Validate data with Zod (returns `{ success, data, error }`)
4. **`flatten().fieldErrors`**: Convert Zod errors to field-specific errors
5. **`redirect()`**: Navigate to another page after success

**Error format**:
```typescript
{
  errors: {
    email: ["Invalid email address"],
    password: ["Password must be at least 8 characters"],
    confirmPassword: ["Passwords don't match"]
  },
  message: "Validation failed. Please check your inputs."
}
```

---

### Step 2: Create Form Component with useActionState (5 min)

Create `components/forms/SignupForm.tsx`:

```typescript
"use client"

import { useActionState } from "react"
import { signup } from "@/actions/auth"

export function SignupForm() {
  const [state, formAction, isPending] = useActionState(signup, null)

  return (
    <form action={formAction} className="space-y-4">
      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email Address <span className="text-red-600">*</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-invalid={state?.errors?.email ? "true" : "false"}
          aria-describedby={state?.errors?.email ? "email-error" : undefined}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {state?.errors?.email && (
          <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1">
          Password <span className="text-red-600">*</span>
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          aria-invalid={state?.errors?.password ? "true" : "false"}
          aria-describedby={state?.errors?.password ? "password-error" : undefined}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {state?.errors?.password && (
          <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
            {state.errors.password[0]}
          </p>
        )}
      </div>

      {/* Confirm Password field */}
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
          Confirm Password <span className="text-red-600">*</span>
        </label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          required
          aria-invalid={state?.errors?.confirmPassword ? "true" : "false"}
          aria-describedby={state?.errors?.confirmPassword ? "confirmPassword-error" : undefined}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {state?.errors?.confirmPassword && (
          <p id="confirmPassword-error" role="alert" className="mt-1 text-sm text-red-600">
            {state.errors.confirmPassword[0]}
          </p>
        )}
      </div>

      {/* Global error message */}
      {state?.message && (
        <div role="alert" className="p-3 bg-red-50 text-red-800 rounded-md border border-red-200">
          {state.message}
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={isPending}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        {isPending ? "Creating account..." : "Sign Up"}
      </button>
    </form>
  )
}
```

**Code breakdown**:

1. **`useActionState()`**: React 19 hook for Server Actions
   ```typescript
   const [state, formAction, isPending] = useActionState(signup, null)
   ```
   - `state`: Return value from Server Action (errors, message)
   - `formAction`: Function to call on form submit
   - `isPending`: Loading state (true during server execution)

2. **`action={formAction}`**: Submit form to Server Action
   ```typescript
   <form action={formAction}>
   ```
   - Works without JavaScript (native form submission)
   - JavaScript adds loading state and error handling

3. **`state?.errors?.email`**: Display server-side errors
   ```typescript
   {state?.errors?.email && <p>{state.errors.email[0]}</p>}
   ```

---

### Step 3: Use Form in Page (2 min)

Create `app/signup/page.tsx`:

```typescript
import { SignupForm } from "@/components/forms/SignupForm"

export default function SignupPage() {
  return (
    <div className="max-w-md mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-6">Create an account</h1>
      <SignupForm />
    </div>
  )
}
```

---

### Step 4: Test the Form (3 min)

1. **Start dev server**:
   ```bash
   npm run dev
   ```

2. **Navigate to** `http://localhost:3000/signup`

3. **Test validation**:
   - Submit empty form → See required errors
   - Enter invalid email (`test`) → See "Invalid email address"
   - Enter short password (`pass`) → See "Password must be at least 8 characters"
   - Enter mismatched passwords → See "Passwords don't match"
   - Enter valid data → Loading state, then redirect to `/login`

4. **Test accessibility** (keyboard navigation):
   - Press `Tab` to navigate through fields
   - Press `Enter` on submit button (should submit form)
   - Check error announcements (use screen reader if available)

5. **Test progressive enhancement** (disable JavaScript):
   - Open DevTools → Settings → Disable JavaScript
   - Refresh page, fill form, submit
   - Form should still work (native submission to Server Action)

**Result**: Production-ready form with client + server validation in 15 minutes!

---

## Validation Checklist

After setup, verify these items:

### Functional Requirements

- [ ] **Client-side validation working**: Errors show immediately on submit
- [ ] **Server-side validation working**: Cannot bypass with DevTools (test by editing HTML)
- [ ] **TypeScript types inferred**: No manual type definitions needed
- [ ] **Error messages displayed**: All errors shown to user
- [ ] **Loading states shown**: Button shows "Creating account..." during submit
- [ ] **Successful submission**: Form redirects or shows success message

### Accessibility Requirements (WCAG 2.2 Level AA)

Use axe DevTools or Lighthouse to check:

- [ ] **All form fields have labels**: `<label htmlFor="email">`
- [ ] **Labels properly associated**: `htmlFor` matches input `id`
- [ ] **Errors identified**: `aria-invalid="true"` on fields with errors
- [ ] **Errors associated**: `aria-describedby` links to error message `id`
- [ ] **Errors announced**: `role="alert"` on error messages
- [ ] **Required fields indicated**: Visual indicator (`*`) and `aria-required="true"`
- [ ] **Keyboard navigation works**: Tab order is logical, Enter submits form
- [ ] **Focus visible**: Focus outline visible on all interactive elements

**How to test**:

1. Install axe DevTools browser extension
2. Open your form page
3. Click "Scan" in axe DevTools
4. Fix any violations

**Target**: 0 violations

### Performance Requirements

Check in DevTools Network tab:

- [ ] **Bundle size acceptable**:
  - react-hook-form: ~12KB gzipped
  - zod: ~12KB gzipped
  - Total added: ~24KB gzipped
- [ ] **No unnecessary re-renders**: Use React DevTools Profiler
  - Typing should not re-render entire form (uncontrolled components)

### Progressive Enhancement

Test with JavaScript disabled:

- [ ] **Form works without JavaScript**: Server Actions handle submission
- [ ] **Form works with JavaScript**: Client validation adds UX layer
- [ ] **No JavaScript errors**: Check browser console

**How to test**:

1. Open DevTools → Settings → Disable JavaScript
2. Refresh page
3. Fill and submit form
4. Form should submit to Server Action (may see page reload)

---

## Next Steps

Congratulations! You now have production-ready form validation set up. Here's what to do next:

### 1. Add More Forms

Create additional forms using the same patterns:

- Login form (see `lib/validations/auth.ts` for `loginSchema`)
- Profile update form
- Contact form
- Search form

---

### 2. Integrate with Authentication (SAP-033)

Protect forms with authentication:

```typescript
"use server"

import { auth } from "@/auth"

export async function updateProfile(formData: FormData) {
  const session = await auth()
  if (!session) throw new Error("Unauthorized")

  // Validate and update profile...
}
```

**See**: [SAP-033 (react-authentication)](../react-authentication/)

---

### 3. Integrate with Database (SAP-034)

Persist form data to database:

```typescript
"use server"

import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"

export async function signup(formData: FormData) {
  const validated = signupSchema.safeParse({ /* data */ })

  const hashedPassword = await bcrypt.hash(validated.data.password, 10)

  const user = await prisma.user.create({
    data: {
      email: validated.data.email,
      password: hashedPassword
    }
  })

  return { userId: user.id }
}
```

**See**: [SAP-034 (react-database-integration)](../react-database-integration/)

---

### 4. Add File Upload Validation

Validate file uploads (images, documents):

```typescript
const uploadSchema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, "File must be less than 5MB")
    .refine(file => ["image/jpeg", "image/png"].includes(file.type), "Only JPEG/PNG allowed")
})
```

**See**: [protocol-spec.md](protocol-spec.md#file-upload-validation)

---

### 5. Build Multi-Step Forms

Create wizard forms with multiple steps:

```typescript
const step1Schema = z.object({ name: z.string(), email: z.string().email() })
const step2Schema = z.object({ company: z.string(), role: z.string() })

const searchParams = useSearchParams()
const step = parseInt(searchParams.get("step") || "1")

const schema = step === 1 ? step1Schema : step2Schema
const { register, handleSubmit } = useForm({ resolver: zodResolver(schema) })
```

**See**: [protocol-spec.md](protocol-spec.md#tutorial-multi-step-wizard-form)

---

### 6. Add Accessibility Testing (SAP-026)

Install axe-core for automated accessibility testing:

```bash
npm install -D @axe-core/react
```

**See**: [SAP-026 (react-accessibility)](../react-accessibility/)

---

### 7. Add Real-Time Validation

Upgrade to real-time validation (validate on every keystroke):

```typescript
useForm({
  resolver: zodResolver(schema),
  mode: "onChange" // Validate on every change (after first submit)
})
```

**See**: [awareness-guide.md](awareness-guide.md#validation-strategies)

---

### 8. Add Async Validation

Check username availability, email uniqueness:

```typescript
const usernameSchema = z.object({
  username: z.string()
    .refine(
      async (username) => {
        const response = await fetch(`/api/check-username?username=${username}`)
        const { available } = await response.json()
        return available
      },
      { message: "Username is already taken" }
    )
})
```

**See**: [protocol-spec.md](protocol-spec.md#async-validation)

---

## Time to Complete

| Option | Time | Features |
|--------|------|----------|
| **Option A** (Client-side only) | 5 min | Basic validation, not production-ready |
| **Option B** (Full-stack) | 15 min | Client + Server validation, production-ready |
| **Total (with installation)** | 20 min | Complete setup with working example |

**vs Manual Setup (without SAP-041)**: 2-3 hours

**Time Savings**: 88.9% reduction

---

## Troubleshooting

### Issue: "Cannot find module '@hookform/resolvers'"

**Solution**: Install the package
```bash
npm install @hookform/resolvers
```

---

### Issue: TypeScript errors with `z.infer`

**Solution**: Upgrade Zod to 3.20+
```bash
npm install zod@latest
```

---

### Issue: "useActionState is not a function"

**Solution**: Upgrade to React 19+
```bash
npm install react@latest react-dom@latest
```

---

### Issue: Server Action not working

**Solution**: Ensure `"use server"` directive at top of file
```typescript
"use server"

export async function signup(formData: FormData) {
  // ...
}
```

---

### Issue: Form submits without validation

**Solution**: Ensure button type is "submit"
```typescript
<button type="submit">Submit</button>
```

---

### Issue: Errors not displaying

**Solution**: Check `formState.errors` destructured correctly
```typescript
const {
  register,
  handleSubmit,
  formState: { errors } // ← Destructure errors
} = useForm()
```

---

## Additional Resources

- **Complete API Reference**: [protocol-spec.md](protocol-spec.md)
- **Accessibility Guide**: [awareness-guide.md](awareness-guide.md#accessibility-checklist-wcag-22-level-aa)
- **Common Workflows**: [awareness-guide.md](awareness-guide.md#common-workflows)
- **Claude Patterns**: [CLAUDE.md](CLAUDE.md)
- **React Hook Form Docs**: https://react-hook-form.com/
- **Zod Docs**: https://zod.dev/

---

## Support

**Need help?**

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [awareness-guide.md](awareness-guide.md#troubleshooting-guide) for more issues
3. Review [protocol-spec.md](protocol-spec.md) for complete API reference
4. Check React Hook Form docs: https://react-hook-form.com/
5. Check Zod docs: https://zod.dev/

---

## Version History

**1.0.0 (2025-11-09)** - Initial Release
- 20-minute installation guide
- Option A: Client-side only (5 min)
- Option B: Full-stack with Server Actions (15 min)
- Complete validation checklist (functional, accessibility, performance)
- Next steps (8 integration patterns)
- Troubleshooting guide
- Time savings metrics (88.9% reduction)

---

**Related Artifacts**:
- [Capability Charter](capability-charter.md) - Problem/solution design
- [Protocol Spec](protocol-spec.md) - Complete technical documentation
- [Awareness Guide](awareness-guide.md) - Quick reference, decision trees
- [Ledger](ledger.md) - Metrics, evidence, adoption tracking
- [CLAUDE.md](CLAUDE.md) - Claude agent patterns
- [README.md](README.md) - One-page overview
