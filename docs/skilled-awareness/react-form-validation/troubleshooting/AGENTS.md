# SAP-041: React Form Validation - Troubleshooting & Common Pitfalls

**SAP**: SAP-041 (react-form-validation)
**Domain**: Troubleshooting
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **common pitfalls and solutions** for React Hook Form + Zod validation, plus a **troubleshooting guide** for frequent issues.

**Sections**:
1. Common Pitfalls and Solutions (6 anti-patterns)
2. Troubleshooting Guide (8 common issues + fixes)

**For implementation workflows**, see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For form patterns**, see [../form-patterns/AGENTS.md](../form-patterns/AGENTS.md)

**For accessibility**, see [../accessibility/AGENTS.md](../accessibility/AGENTS.md)

---

## Common Pitfalls and Solutions

### Pitfall 1: Controlled Component Re-Renders

**Problem**: Using `watch()` or `value` prop causes re-render on every keystroke

**Symptom**: Form feels sluggish, React DevTools shows excessive re-renders

**Example**:
```typescript
// ❌ Bad: Re-renders entire form on every keystroke
const email = watch("email")

<input value={email} onChange={e => setValue("email", e.target.value)} />
```

**Solution**: Use uncontrolled components with `register()`

```typescript
// ✅ Good: No re-renders
<input {...register("email")} />
```

**Exception**: Use controlled when needed for third-party components:
```typescript
<Controller
  name="birthdate"
  control={control}
  render={({ field }) => <DatePicker {...field} />}
/>
```

**When to use controlled**:
- Third-party components (react-datepicker, react-select)
- Rich text editors (Tiptap, Slate)
- Custom UI libraries (Radix UI, shadcn/ui)

**Performance Impact**:
- Uncontrolled: 0 re-renders on keystroke
- Controlled: 1 re-render per keystroke (60-100 re-renders for "hello@example.com")
- 5x performance difference

---

### Pitfall 2: Client-Only Validation

**Problem**: Client validation can be bypassed via DevTools or cURL

**Security Risk**: HIGH - Allows malicious input to reach server/database

**Example**:
```typescript
// ❌ Bad: Client-only validation (insecure)
async function onSubmit(data: FormData) {
  await fetch("/api/signup", { body: JSON.stringify(data) })
}
```

**Solution**: Always validate on server with Server Actions

```typescript
// ✅ Good: Server validation (secure)
"use server"
export async function signup(formData: FormData) {
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Create user...
}
```

**Why this matters**:
- Client validation is for UX (instant feedback)
- Server validation is for security (cannot bypass)
- Always use both for production forms (Tier 2+)

**See**: [../workflows/AGENTS.md#workflow-2](../workflows/AGENTS.md#workflow-2) for server validation implementation

---

### Pitfall 3: Missing Error Accessibility

**Problem**: Errors not announced to screen readers

**WCAG Violation**: 3.3.1 Error Identification (Level A)

**Example**:
```typescript
// ❌ Bad: Not accessible
{errors.email && <p className="text-red-600">{errors.email.message}</p>}
```

**Solution**: Use `role="alert"` and `aria-describedby`

```typescript
// ✅ Good: Accessible
<input
  aria-invalid={errors.email ? "true" : "false"}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert" aria-live="assertive" className="text-red-600">
    {errors.email.message}
  </p>
)}
```

**Accessibility Requirements**:
- `aria-invalid="true"` on error fields
- `aria-describedby` linking to error message
- `role="alert"` for immediate announcement
- `aria-live="assertive"` for interrupting current speech

**See**: [../accessibility/AGENTS.md](../accessibility/AGENTS.md) for complete accessibility checklist

---

### Pitfall 4: TypeScript Type Mismatches

**Problem**: Manual types drift from Zod schemas

**Symptom**: TypeScript errors when schema changes, runtime validation passes but TypeScript fails

**Example**:
```typescript
// ❌ Bad: Types can drift
interface SignupData {
  email: string
  password: string
}

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string() // Added to schema, but not to interface!
})
```

**Solution**: Infer types from schemas

```typescript
// ✅ Good: Types always match schema
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string()
})

type SignupData = z.infer<typeof schema> // Automatically includes all fields
```

**Benefits**:
- Single source of truth (schema defines validation + types)
- No type drift (types always match validation)
- IntelliSense support (TypeScript autocomplete)
- Refactoring safety (change schema, types update automatically)

---

### Pitfall 5: No Progressive Enhancement

**Problem**: Forms don't work without JavaScript

**Symptom**: Users with JavaScript disabled cannot submit forms

**Example**:
```typescript
// ❌ Bad: Requires JavaScript
<form onSubmit={handleSubmit(async (data) => {
  await fetch("/api/submit", { body: JSON.stringify(data) })
})}>
```

**Solution**: Use Server Actions with native form submission

```typescript
// ✅ Good: Works without JavaScript
<form action={formAction}>
  {/* Native form submission works without JS */}
  {/* React Hook Form adds client validation layer */}
</form>
```

**Progressive Enhancement Benefits**:
- Core functionality works without JavaScript
- Enhanced UX with JavaScript enabled
- Better SEO (search engines can crawl forms)
- Accessibility (assistive tech relies on native form behavior)

**See**: [../workflows/AGENTS.md#workflow-2](../workflows/AGENTS.md#workflow-2) for progressive enhancement implementation

---

### Pitfall 6: Incorrect Error Message Format

**Problem**: Error messages from server don't match expected format

**Symptom**: `TypeError: Cannot read property '0' of string`

**Example**:
```typescript
// Server Action returns errors
return {
  errors: {
    email: "Email is invalid" // ❌ String instead of array
  }
}

// Form expects array
{state?.errors?.email && <p>{state.errors.email[0]}</p>} // ❌ Error: email is string
```

**Solution**: Consistent error format using Zod's `flatten()`

```typescript
// Server Action
const validated = schema.safeParse(data)
if (!validated.success) {
  return {
    errors: validated.error.flatten().fieldErrors // ✅ Returns { email: ["Email is invalid"] }
  }
}

// Form component
{state?.errors?.email && <p>{state.errors.email[0]}</p>} // ✅ Correct
```

**Zod `flatten()` Output Format**:
```typescript
// Before flatten()
{
  email: {
    _errors: ["Email is invalid", "Email is required"]
  }
}

// After flatten().fieldErrors
{
  email: ["Email is invalid", "Email is required"]
}
```

---

## Troubleshooting Guide

### Issue: "resolver is not a function" error

**Cause**: Missing `@hookform/resolvers` package

**Symptom**:
```
TypeError: resolver is not a function
  at useForm (react-hook-form.js:123)
```

**Fix**:
```bash
npm install @hookform/resolvers
```

**Verify**:
```typescript
import { zodResolver } from "@hookform/resolvers/zod"

useForm({
  resolver: zodResolver(schema) // Should work now
})
```

**Package Versions**:
- `react-hook-form`: ^7.50.0
- `@hookform/resolvers`: ^3.3.0
- `zod`: ^3.22.0

---

### Issue: TypeScript errors with `z.infer<typeof schema>`

**Cause**: Zod version <3.20

**Symptom**:
```
Type 'ZodObject<...>' does not satisfy the constraint 'ZodType<any, any, any>'
```

**Fix**:
```bash
npm install zod@latest
```

**Verify**:
```bash
npm list zod
# Should show zod@3.22.0 or higher
```

**Breaking Changes**:
- Zod 3.20+: `z.infer<typeof schema>` syntax
- Zod <3.20: `z.TypeOf<typeof schema>` syntax (deprecated)

---

### Issue: Server Actions not working

**Cause**: Missing `"use server"` directive

**Symptom**:
```
Error: Functions cannot be passed directly to Client Components
```

**Fix**: Add `"use server"` at top of actions file

```typescript
// ✅ Correct
"use server"

import { signupSchema } from "@/lib/validations/auth"

export async function signup(formData: FormData) {
  // ...
}
```

**Common Mistakes**:
```typescript
// ❌ Wrong: "use server" inside function
export async function signup(formData: FormData) {
  "use server"
  // ...
}

// ❌ Wrong: Missing directive entirely
export async function signup(formData: FormData) {
  // ...
}
```

**Requirements**:
- Next.js 13.4+ (Server Actions stable)
- `"use server"` at top of file or inside function
- Server Actions must be async functions

---

### Issue: Forms submit without validation

**Cause**: Using `<button>` instead of `<button type="submit">`

**Symptom**: Form submits immediately without running validation

**Fix**: Always specify `type="submit"`

```typescript
// ❌ Bad: Button has type="button" by default in some cases
<button>Submit</button>

// ✅ Good: Explicit type="submit"
<button type="submit">Submit</button>
```

**Button Type Reference**:
- `type="submit"`: Triggers form submission (default for `<button>` inside `<form>`)
- `type="button"`: No action (default for `<button>` outside `<form>`)
- `type="reset"`: Resets form to default values

---

### Issue: Validation not firing

**Cause**: Incorrect validation mode

**Symptom**: Errors only appear after form submission, not on blur or change

**Fix**: Set `mode` in `useForm()`

```typescript
useForm({
  resolver: zodResolver(schema),
  mode: "onSubmit" // Validate on submit (default)
})

// Or for real-time validation
useForm({
  resolver: zodResolver(schema),
  mode: "onChange" // Validate on every keystroke
})
```

**Validation Modes**:
- `onSubmit` (default): Validate when form is submitted
- `onBlur`: Validate when field loses focus
- `onChange`: Validate on every keystroke (after first submit)
- `onTouched`: Validate after field is touched
- `all`: Validate on blur + change

**Recommendation**: Start with `onSubmit` (default), upgrade to `onBlur` or `onChange` if users request real-time feedback.

---

### Issue: Error messages not displaying

**Cause**: Not checking `formState.errors`

**Symptom**: Form validation runs but errors don't appear

**Fix**: Destructure and check errors

```typescript
// ❌ Bad: Not destructuring formState
const { register, handleSubmit } = useForm()

// ✅ Good: Destructure formState.errors
const {
  register,
  handleSubmit,
  formState: { errors }
} = useForm()

{errors.email && <p>{errors.email.message}</p>}
```

**Important**: `formState` must be accessed before `errors` for React Hook Form to track error state.

```typescript
// ✅ Correct order
const { formState: { errors } } = useForm()

// ❌ Wrong (may not work)
const { errors } = useForm().formState
```

---

### Issue: File upload validation not working

**Cause**: `FormData.get()` returns `File | string | null`, need type guard

**Symptom**:
```
Type 'string | File | null' is not assignable to type 'File'
```

**Fix**: Check file type before validation

```typescript
"use server"
export async function uploadFile(formData: FormData) {
  const file = formData.get("file")

  // Type guard
  if (!(file instanceof File)) {
    return { errors: { file: ["File is required"] } }
  }

  // Now validate
  const validated = fileSchema.safeParse({ file })
  // ...
}
```

**File Validation Schema**:
```typescript
const fileSchema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, {
      message: "File must be less than 5MB"
    })
    .refine(file => ["image/jpeg", "image/png", "image/webp"].includes(file.type), {
      message: "Only JPEG, PNG, and WebP images are allowed"
    })
})
```

**See**: [../workflows/AGENTS.md](../workflows/AGENTS.md) and SAP-035 (react-file-upload) for complete file upload patterns

---

### Issue: Cross-field validation not working

**Cause**: Using `.refine()` incorrectly

**Symptom**: Password confirmation validation doesn't work

**Fix**: Use correct syntax for cross-field validation

```typescript
// ✅ Correct: Refine entire object
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"] // Error will appear on confirmPassword field
})

// ❌ Wrong: Refining individual field (can't access other fields)
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string().refine((val) => val === /* can't access password here */)
})
```

**Refine Syntax**:
- `.refine(callback, options)`: Validates entire object
- `callback`: Receives full object, returns `true` (valid) or `false` (invalid)
- `options.message`: Error message
- `options.path`: Which field to attach error to (array of field names)

**Multiple Cross-Field Validations**:
```typescript
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
  email: z.string().email(),
  confirmEmail: z.string().email()
})
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  })
  .refine((data) => data.email === data.confirmEmail, {
    message: "Emails don't match",
    path: ["confirmEmail"]
  })
```

---

## Quick Reference: Error Messages by Issue

| Issue | Error Message | Solution |
|-------|---------------|----------|
| Missing resolver package | `resolver is not a function` | `npm install @hookform/resolvers` |
| Old Zod version | `ZodObject<...> does not satisfy constraint` | `npm install zod@latest` |
| Missing "use server" | `Functions cannot be passed to Client Components` | Add `"use server"` at top of file |
| Wrong button type | Form submits without validation | Use `type="submit"` |
| Incorrect mode | Validation doesn't fire on blur/change | Set `mode: "onBlur"` or `mode: "onChange"` |
| Missing formState | Errors don't display | Destructure `formState: { errors }` |
| File upload type error | `string | File | null not assignable to File` | Add type guard `if (!(file instanceof File))` |
| Cross-field validation | Password confirmation doesn't work | Use `.refine()` on entire object, not individual field |

---

## Debugging Tips

### Enable React Hook Form DevTools

```bash
npm install -D @hookform/devtools
```

```typescript
import { useForm } from "react-hook-form"
import { DevTool } from "@hookform/devtools"

function MyForm() {
  const { register, control } = useForm()

  return (
    <>
      <form>{/* fields */}</form>
      <DevTool control={control} />
    </>
  )
}
```

**DevTools Features**:
- View current form state
- See all registered fields
- Track validation errors
- Monitor form submission status

---

### Log Form State

```typescript
const { formState } = useForm()

console.log("Form state:", {
  isDirty: formState.isDirty,
  isValid: formState.isValid,
  isSubmitting: formState.isSubmitting,
  errors: formState.errors
})
```

---

### Validate Schema Manually

```typescript
const schema = z.object({ email: z.string().email() })

// Test validation
const result = schema.safeParse({ email: "invalid" })

if (!result.success) {
  console.log("Validation errors:", result.error.flatten().fieldErrors)
}
```

---

## Version History

**1.0.0 (2025-11-10)** - Initial troubleshooting extraction from awareness-guide.md
- 6 common pitfalls and solutions
- 8 troubleshooting issues with fixes
- Quick reference error message table
- Debugging tips (DevTools, logging, manual validation)
