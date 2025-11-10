# SAP-041: React Form Validation - Awareness Guide (AGENTS.md)

---
nested_structure: true
nested_files:
  - "workflows/AGENTS.md"
  - "form-patterns/AGENTS.md"
  - "accessibility/AGENTS.md"
  - "troubleshooting/AGENTS.md"
version: 2.0.0
last_updated: 2025-11-10
---

**SAP**: SAP-041 (react-form-validation)
**Version**: 2.0.0
**Status**: pilot
**Last Updated**: 2025-11-10

---

## 📖 Quick Reference

**New to SAP-041?** → Read **[README.md](README.md)** first (9-min read)

The README provides:
- 🚀 **Quick Start** - 20-minute setup (React Hook Form + Zod + Server Actions)
- 📚 **88.9% Time Savings** - 2-3 hours → 20 minutes per form with production templates
- 🎯 **Type-Safe** - 100% TypeScript inference from Zod schemas (zero manual types)
- 🔧 **Accessible** - WCAG 2.2 Level AA compliance built-in (role="alert", aria-invalid)
- 📊 **Performant** - 5x fewer re-renders than Formik, 50% smaller bundle
- 🔗 **Integration** - Works with SAP-020 (Next.js 15), SAP-033 (Auth), SAP-026 (Accessibility)

This awareness-guide.md provides: Agent-specific form validation workflows, tier selection patterns (client vs server validation), and accessibility best practices for AI coding assistants.

---

## ⚠️ Critical Workflows (Read This First!)

**This section highlights the 5 most frequently-missed patterns for React Hook Form + Zod validation.**

---

### 1. Simple Login Form (5 min) ⚠️ MOST COMMON

**When**: User needs basic login/signup form with email and password

**Common Mistake**: Agents build overly complex forms for simple authentication use cases.

**Correct Action**: Use Tier 1 pattern (client-side validation only).

```typescript
const loginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(1, "Password required")
})

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(loginSchema)
})

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register("email")} type="email" />
  {errors.email && <p role="alert">{errors.email.message}</p>}

  <input {...register("password")} type="password" />
  {errors.password && <p role="alert">{errors.password.message}</p>}

  <button type="submit">Login</button>
</form>
```

**Time**: 5 minutes

**Full Details**: [workflows/AGENTS.md#workflow-1-create-simple-login-form-5-min](workflows/AGENTS.md#workflow-1-create-simple-login-form-5-min)

---

### 2. Server Validation Required ⚠️ SECURITY CRITICAL

**When**: Form creates user accounts, modifies data, or handles sensitive information

**Common Mistake**: Using client-side validation only. Client validation can be bypassed via DevTools or cURL.

**Correct Action**: ALWAYS add server validation for security (Tier 2+).

```typescript
// Server Action
"use server"
export async function signup(prevState: any, formData: FormData) {
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Create user...
}

// Form Component
const [state, formAction, isPending] = useActionState(signup, null)

<form action={formAction}>
  {/* fields */}
  {state?.errors?.email && <p role="alert">{state.errors.email[0]}</p>}
</form>
```

**Time**: 10 minutes additional

**Security**: Client validation = UX (instant feedback), Server validation = Security (cannot bypass)

**Full Details**: [workflows/AGENTS.md#workflow-2-add-server-validation-to-existing-form-10-min](workflows/AGENTS.md#workflow-2-add-server-validation-to-existing-form-10-min)

---

### 3. Accessibility Patterns ⚠️ COMPLIANCE REQUIREMENT

**When**: All production forms (WCAG 2.2 Level AA requirement)

**Common Mistake**: Missing `aria-invalid`, `aria-describedby`, `role="alert"` patterns. Errors not announced to screen readers.

**Correct Action**: Always include accessibility attributes.

```typescript
<input
  aria-invalid={errors.email ? "true" : "false"}
  aria-describedby={errors.email ? "email-error" : undefined}
  aria-required="true"
/>
{errors.email && (
  <p id="email-error" role="alert" aria-live="assertive">
    {errors.email.message}
  </p>
)}
```

**Checklist**:
- [ ] `aria-invalid="true"` on error fields
- [ ] `aria-describedby` linking to error message
- [ ] `role="alert"` for screen reader announcements
- [ ] Labels with `htmlFor` matching input `id`

**Full Details**: [accessibility/AGENTS.md](accessibility/AGENTS.md)

---

### 4. Cross-Field Validation ⚠️ COMMON PITFALL

**When**: Password confirmation, email confirmation, conditional fields

**Common Mistake**: Using `.refine()` on individual fields instead of entire object. Cross-field validation doesn't work.

**Correct Action**: Use `.refine()` on schema object.

```typescript
// ✅ Correct: Refine entire object
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"] // Error appears on confirmPassword field
})

// ❌ Wrong: Refining individual field
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string().refine((val) => val === /* can't access password */)
})
```

**Full Details**: [troubleshooting/AGENTS.md#issue-cross-field-validation-not-working](troubleshooting/AGENTS.md#issue-cross-field-validation-not-working)

---

### 5. Progressive Enhancement ⚠️ UX REQUIREMENT

**When**: Forms with server validation (Tier 2+)

**Common Mistake**: Using `onSubmit` handler with `fetch()`. Forms don't work without JavaScript.

**Correct Action**: Use Server Actions with native `action` attribute.

```typescript
// ❌ Bad: Requires JavaScript
<form onSubmit={handleSubmit(async (data) => {
  await fetch("/api/submit", { body: JSON.stringify(data) })
})}>

// ✅ Good: Works without JavaScript
<form action={formAction}>
  {/* Native form submission works without JS */}
  {/* React Hook Form adds client validation layer */}
</form>
```

**Benefits**:
- Core functionality works without JavaScript
- Better SEO (search engines can crawl forms)
- Accessibility (assistive tech relies on native behavior)

**Full Details**: [troubleshooting/AGENTS.md#pitfall-5-no-progressive-enhancement](troubleshooting/AGENTS.md#pitfall-5-no-progressive-enhancement)

---

## Quick Reference (30-second overview)

SAP-041 enables React Hook Form + Zod form validation in Next.js 15+ projects:

- **Setup Time**: 20 minutes (vs 2-3 hours manual)
- **Time Savings**: 88.9% reduction
- **Validation**: Three-layer (Client UX + Server security + Database constraints)
- **Type Safety**: 100% TypeScript inference from Zod schemas (zero manual types)
- **Accessibility**: WCAG 2.2 Level AA compliance built-in
- **Progressive Enhancement**: Forms work without JavaScript
- **Bundle Size**: 24KB gzipped (RHF 12KB + Zod 12KB)
- **Performance**: 5x fewer re-renders than Formik (uncontrolled components)

**Key Technologies**:
- React Hook Form 7.x (3M weekly npm downloads, 94% retention)
- Zod 3.x (10M+ weekly npm downloads, 90% retention)
- Next.js 15.1+ App Router with Server Actions
- React 19+ (useActionState, useOptimistic, useFormStatus)

---

## When to Use This SAP

### Use SAP-041 when:

✅ **Building forms in Next.js 15+ App Router projects**
- Requires App Router (not Pages Router)
- Requires React 19+ for useActionState hook
- Requires Server Actions for server-side validation

✅ **Need client + server validation**
- Client validation for instant UX feedback
- Server validation for security (cannot bypass)
- Same Zod schema reused client + server (DRY)

✅ **Want TypeScript type safety without manual type definitions**
- Types inferred from Zod schemas: `type FormData = z.infer<typeof schema>`
- Zero manual type definitions
- No type drift between validation and TypeScript

✅ **Require WCAG 2.2 Level AA accessibility compliance**
- Built-in patterns for label association, error announcements, keyboard navigation
- 0 axe-core violations with SAP-041 patterns
- Screen reader support (NVDA, VoiceOver, JAWS)

✅ **Building multi-step forms or wizards**
- URL-based step persistence (searchParams)
- Per-step validation with Zod schemas
- Progress indicators and back/forward navigation

### Skip SAP-041 when:

❌ **Simple static forms (no validation needed)**
- Contact forms with 1-2 fields
- Forms where HTML5 validation is sufficient
- Read-only or display-only forms

❌ **Using Pages Router (not App Router)**
- SAP-041 requires App Router for Server Actions
- Use alternative validation patterns for Pages Router

❌ **Non-React frameworks**
- Vue.js, Angular, Svelte, etc.
- Use framework-specific validation libraries

---

## Key Concepts

### Controlled vs Uncontrolled Components

**Uncontrolled Components** (React Hook Form default):
- Form state stored in DOM (not React state)
- No re-renders on every keystroke
- 5x better performance than controlled components
- Use `register()` to connect field to form state

```typescript
// ✅ Uncontrolled (recommended)
<input {...register("email")} />
```

**Controlled Components** (when needed):
- Form state stored in React state
- Re-renders on every keystroke
- Needed for: date pickers, rich text editors, custom UI components
- Use `Controller` wrapper

```typescript
// ✅ Controlled (when needed)
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

---

### Validation Strategies

React Hook Form supports 4 validation modes:

**1. onSubmit (default)**:
- Validate only when form is submitted
- Best for simple forms (Tier 1)
- Minimal validation overhead

```typescript
useForm({ mode: "onSubmit" })
```

**2. onChange**:
- Validate on every keystroke (after first submit)
- Best for complex forms with real-time feedback
- Higher performance cost

```typescript
useForm({ mode: "onChange" })
```

**3. onBlur**:
- Validate when field loses focus
- Best for medium forms (Tier 2)
- Good balance of UX and performance

```typescript
useForm({ mode: "onBlur" })
```

**4. onTouched**:
- Validate after field is touched
- Similar to onBlur
- Used for custom validation timing

```typescript
useForm({ mode: "onTouched" })
```

**Recommendation**: Start with `onSubmit` (default), upgrade to `onBlur` or `onChange` if users request real-time feedback.

---

### Schema-First Validation

SAP-041 uses **schema-first validation** with Zod:

**1. Define schema once** (single source of truth):
```typescript
const signupSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters")
})
```

**2. Infer TypeScript type** (zero manual types):
```typescript
type SignupFormData = z.infer<typeof signupSchema>
// Type: { email: string; password: string }
```

**3. Use schema in form** (client validation):
```typescript
const { register } = useForm<SignupFormData>({
  resolver: zodResolver(signupSchema)
})
```

**4. Reuse schema in Server Action** (server validation):
```typescript
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

**Benefits**:
- Single source of truth (schema defines validation + types)
- No type drift (types always match validation)
- DRY principle (schema reused client + server)
- IntelliSense support (TypeScript autocomplete)

---

## Navigation: Nested Domain Files

**This awareness guide uses nested structure.** For detailed patterns, navigate to domain-specific files:

### [workflows/AGENTS.md](workflows/AGENTS.md) - Implementation Workflows

**3 step-by-step workflows** for implementing React Hook Form + Zod:

1. **Workflow 1**: Create Simple Login Form (5 min) - Tier 1 (client-side validation)
2. **Workflow 2**: Add Server Validation (10 min) - Tier 2 (client + server validation)
3. **Workflow 3**: Build Multi-Step Wizard (30 min) - Tier 4 (wizard with URL state)

**When to read**: When implementing forms, need step-by-step code examples.

---

### [form-patterns/AGENTS.md](form-patterns/AGENTS.md) - Complexity Decision Tree

**4 form complexity tiers** with decision flowchart:

1. **Tier 1**: Simple Forms (1-3 fields, 5 min setup)
2. **Tier 2**: Medium Forms (4-8 fields, 15 min setup)
3. **Tier 3**: Complex Forms (9+ fields, dynamic fields, 30 min setup)
4. **Tier 4**: Wizard Forms (multi-step, 45 min setup)

**When to read**: When deciding which form pattern to use, need complexity assessment.

---

### [accessibility/AGENTS.md](accessibility/AGENTS.md) - WCAG 2.2 Level AA Compliance

**WCAG 2.2 Level AA checklist** with code examples:

- Error Identification (3.3.1, Level A)
- Labels or Instructions (3.3.2, Level A)
- Error Suggestion (3.3.3, Level AA)
- Error Prevention (3.3.4, Level AA)
- Focus Order (2.4.3, Level A)
- Status Messages (4.1.3, Level AA)

**When to read**: When implementing production forms, need accessibility compliance.

---

### [troubleshooting/AGENTS.md](troubleshooting/AGENTS.md) - Common Issues & Fixes

**6 common pitfalls** + **8 troubleshooting issues** with solutions:

- Pitfall 1: Controlled component re-renders (performance)
- Pitfall 2: Client-only validation (security)
- Pitfall 3: Missing error accessibility (WCAG)
- Pitfall 4: TypeScript type mismatches
- Pitfall 5: No progressive enhancement
- Pitfall 6: Incorrect error message format

**When to read**: When encountering errors, unexpected behavior, or performance issues.

---

## Integration with Other SAPs

### SAP-020 (react-foundation)

**Integration**: Server Actions for server-side validation

**Required for**: All forms using server validation (Tier 2+)

**Pattern**:
```typescript
"use server"

import { signupSchema } from "@/lib/validations/auth"

export async function signup(prevState: any, formData: FormData) {
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Process signup...
}
```

**Use in form**:
```typescript
import { useActionState } from "react"
import { signup } from "@/actions/auth"

const [state, formAction, isPending] = useActionState(signup, null)

<form action={formAction}>
  {/* fields */}
  {state?.errors?.email && <p>{state.errors.email}</p>}
</form>
```

---

### SAP-033 (react-authentication)

**Integration**: Protected forms require authentication

**Required for**: Forms that modify user data (profile updates, settings)

**Pattern**:
```typescript
"use server"

import { auth } from "@/auth"
import { profileSchema } from "@/lib/validations/profile"

export async function updateProfile(formData: FormData) {
  // Check authentication
  const session = await auth()
  if (!session) {
    throw new Error("Unauthorized")
  }

  // Validate form data
  const validated = profileSchema.safeParse({
    name: formData.get("name"),
    bio: formData.get("bio")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Update user profile
  await prisma.user.update({
    where: { id: session.user.id },
    data: validated.data
  })

  return { success: true }
}
```

**Authentication context in forms**:
```typescript
// Server Component
import { auth } from "@/auth"
import { ProfileForm } from "@/components/forms/ProfileForm"

export default async function ProfilePage() {
  const session = await auth()
  if (!session) redirect("/login")

  return <ProfileForm user={session.user} />
}
```

---

### SAP-034 (react-database-integration)

**Integration**: Form data persisted to Prisma/Drizzle

**Required for**: Forms that store data in database

**Pattern**:
```typescript
"use server"

import { prisma } from "@/lib/prisma"
import { signupSchema } from "@/lib/validations/auth"
import bcrypt from "bcryptjs"

export async function signup(formData: FormData) {
  // Validate with Zod
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(validated.data.password, 10)

  // Create user in database
  try {
    const user = await prisma.user.create({
      data: {
        email: validated.data.email,
        password: hashedPassword
      }
    })

    return { userId: user.id }
  } catch (error: any) {
    // Handle unique constraint violation
    if (error.code === "P2002") {
      return {
        errors: { email: ["Email already exists"] }
      }
    }
    throw error
  }
}
```

**Match Zod schema to Prisma schema**:
```typescript
import { Prisma } from "@prisma/client"

const userSchema = z.object({
  email: z.string().email(),
  name: z.string(),
  role: z.enum(["USER", "ADMIN"])
}) satisfies z.ZodType<Prisma.UserCreateInput>
```

---

### SAP-026 (react-accessibility)

**Integration**: WCAG 2.2 Level AA compliance patterns

**Required for**: All production forms (accessibility requirement)

**Pattern**: See [accessibility/AGENTS.md](accessibility/AGENTS.md) for complete checklist

**Validation**:
```bash
# Install axe-core
npm install -D @axe-core/react

# Run accessibility tests
npm run test:a11y
```

---

### SAP-023 (react-state-management)

**Integration**: Wizard forms with URL state persistence

**Required for**: Multi-step forms (Tier 4)

**Pattern**:
```typescript
import { useSearchParams, useRouter } from "next/navigation"

const searchParams = useSearchParams()
const router = useRouter()
const step = parseInt(searchParams.get("step") || "1")

function nextStep() {
  router.push(`?step=${step + 1}`)
}

function prevStep() {
  router.push(`?step=${step - 1}`)
}
```

**Benefits**:
- URL reflects application state
- Browser back/forward buttons work
- Shareable URLs (user can bookmark specific step)
- Progressive enhancement (works without JavaScript)

---

## Next Steps After Adoption

### 1. Add Real-Time Validation

Upgrade from `onSubmit` to `onChange` or `onBlur` validation:

```typescript
useForm({
  resolver: zodResolver(schema),
  mode: "onChange" // Validate on every keystroke (after first submit)
})
```

---

### 2. Add Async Validation

Check username availability, email uniqueness, etc.:

```typescript
const usernameSchema = z.object({
  username: z.string()
    .min(3)
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

---

### 3. Add File Upload Validation

See protocol-spec.md for complete file upload patterns.

---

### 4. Integrate with Authentication (SAP-033)

Protect forms with authentication:

```typescript
"use server"
import { auth } from "@/auth"

export async function updateProfile(formData: FormData) {
  const session = await auth()
  if (!session) throw new Error("Unauthorized")

  // Validate and update...
}
```

---

### 5. Integrate with Database (SAP-034)

Persist form data to Prisma/Drizzle:

```typescript
"use server"
import { prisma } from "@/lib/prisma"

export async function createPost(formData: FormData) {
  const validated = postSchema.safeParse({ /* data */ })

  const post = await prisma.post.create({
    data: validated.data
  })

  return { postId: post.id }
}
```

---

### 6. Add Accessibility Testing (SAP-026)

```bash
npm install -D @axe-core/react
```

Run axe DevTools in browser to check WCAG 2.2 Level AA compliance.

---

## Version History

**2.0.0 (2025-11-10)** - Nested awareness pattern applied (SAP-009 v2.1.0)
- Added Critical Workflows section (5 frequently-missed patterns)
- Extracted 4 domain-specific files (workflows, form-patterns, accessibility, troubleshooting)
- Reduced from 1,951 → ~700 lines (64% reduction)
- Added frontmatter with nested_structure declaration
- Streamlined root file with navigation to nested domains

**1.0.0 (2025-11-09)** - Initial Release
- Complete awareness guide
- Form complexity decision tree (Tier 1-4)
- 3 common workflows (simple form, server validation, wizard)
- Integration patterns for SAP-020, SAP-033, SAP-034, SAP-026, SAP-023
- WCAG 2.2 Level AA accessibility checklist
- Common pitfalls and solutions
- Troubleshooting guide
- Next steps after adoption

---

**Related Artifacts**:
- [Capability Charter](capability-charter.md) - Problem/solution design
- [Protocol Spec](protocol-spec.md) - Complete technical documentation
- [Adoption Blueprint](adoption-blueprint.md) - 20-minute installation guide
- [Ledger](ledger.md) - Metrics, evidence, adoption tracking
- [CLAUDE.md](CLAUDE.md) - Claude agent patterns
- [README.md](README.md) - One-page overview
