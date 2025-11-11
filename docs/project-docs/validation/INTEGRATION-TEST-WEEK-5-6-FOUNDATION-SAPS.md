# Integration Testing: Week 5-6 Foundation SAPs

**Test Date**: 2025-11-09
**SAPs Under Test**: SAP-033 (Authentication), SAP-034 (Database), SAP-041 (Forms)
**Test Type**: Integration Testing + SAP-027 Dogfooding Validation
**Status**: Pending

---

## Overview

This document provides a comprehensive integration testing plan for the 3 Foundation SAPs created in Week 5-6:
- **SAP-034**: Database Integration (Prisma/Drizzle)
- **SAP-033**: Authentication (NextAuth v5/Clerk/Supabase/Auth0)
- **SAP-041**: Form Validation (React Hook Form + Zod)

**Test Goals**:
1. Validate each SAP works independently (setup time ≤30 minutes)
2. Validate SAP pairs integrate correctly (SAP-034+SAP-033, SAP-033+SAP-041)
3. Validate all 3 SAPs create complete signup flow (form → auth → database)
4. Collect SAP-027 dogfooding metrics (time savings, developer satisfaction)

---

## Test Environment Setup

### Prerequisites

- Node.js 22.x LTS (verified: `node --version`)
- pnpm 9.x or npm 10.x (verified: `pnpm --version`)
- PostgreSQL 16.x (local or cloud - Supabase/Vercel recommended)
- Git (for version control)

### Project Structure

```
foundation-saps-test/
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.local
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   ├── login/
│   │   └── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   └── api/
│       └── auth/
│           └── [...nextauth]/
│               └── route.ts
├── components/
│   └── forms/
│       ├── SignupForm.tsx
│       └── LoginForm.tsx
├── lib/
│   ├── prisma.ts
│   ├── validations/
│   │   └── auth.ts
│   └── auth.ts
├── actions/
│   └── auth.ts
├── prisma/
│   ├── schema.prisma
│   └── seed.ts
└── middleware.ts
```

---

## Phase 1: Individual SAP Testing (Setup Time Validation)

### Test 1.1: SAP-034 (Database Integration) - Target: 25 minutes

**Test Objective**: Validate Prisma setup, schema creation, migrations, and basic CRUD operations

**Steps**:

1. **Create fresh Next.js 15 project** (2 min)
   ```bash
   npx create-next-app@latest foundation-saps-test --typescript --tailwind --app --no-src-dir
   cd foundation-saps-test
   ```

2. **Follow SAP-034 adoption-blueprint.md** (20 min)
   - Install Prisma: `npm install @prisma/client prisma`
   - Initialize Prisma: `npx prisma init`
   - Create schema (User model):
     ```prisma
     model User {
       id        String   @id @default(cuid())
       email     String   @unique
       name      String?
       password  String
       createdAt DateTime @default(now())
       updatedAt DateTime @updatedAt
     }
     ```
   - Run migration: `npx prisma migrate dev --name init`
   - Create Prisma client singleton (`lib/prisma.ts`)
   - Verify database connection

3. **Test CRUD operations** (3 min)
   ```typescript
   // Test script: scripts/test-prisma.ts
   import { prisma } from '../lib/prisma'

   async function testCrud() {
     // Create
     const user = await prisma.user.create({
       data: {
         email: 'test@example.com',
         name: 'Test User',
         password: 'hashed_password'
       }
     })
     console.log('✅ Created user:', user.id)

     // Read
     const found = await prisma.user.findUnique({
       where: { email: 'test@example.com' }
     })
     console.log('✅ Found user:', found?.name)

     // Update
     const updated = await prisma.user.update({
       where: { id: user.id },
       data: { name: 'Updated Name' }
     })
     console.log('✅ Updated user:', updated.name)

     // Delete
     await prisma.user.delete({ where: { id: user.id } })
     console.log('✅ Deleted user')
   }

   testCrud().then(() => prisma.$disconnect())
   ```

   Run: `npx tsx scripts/test-prisma.ts`

**Success Criteria**:
- [ ] Setup completed in ≤25 minutes
- [ ] Database migrations run successfully
- [ ] Prisma client generates types
- [ ] CRUD operations work (create, read, update, delete)
- [ ] TypeScript type inference works (no manual types needed)
- [ ] No TypeScript errors

**Metrics to Collect**:
- Actual setup time: _____ minutes
- Deviations from adoption blueprint: _____
- Issues encountered: _____

---

### Test 1.2: SAP-033 (Authentication) - Target: 15 minutes

**Test Objective**: Validate NextAuth v5 setup, session management, route protection

**Steps**:

1. **Follow SAP-033 adoption-blueprint.md** (12 min)
   - Install NextAuth: `npm install next-auth@beta`
   - Create `auth.config.ts`:
     ```typescript
     import type { NextAuthConfig } from "next-auth"
     import Credentials from "next-auth/providers/credentials"

     export default {
       providers: [
         Credentials({
           credentials: {
             email: { label: "Email", type: "email" },
             password: { label: "Password", type: "password" }
           },
           async authorize(credentials) {
             // TODO: Verify credentials with database (SAP-034 integration)
             if (credentials.email === "test@example.com") {
               return { id: "1", email: credentials.email, name: "Test User" }
             }
             return null
           }
         })
       ]
     } satisfies NextAuthConfig
     ```
   - Create `auth.ts`:
     ```typescript
     import NextAuth from "next-auth"
     import authConfig from "./auth.config"

     export const { handlers, auth, signIn, signOut } = NextAuth(authConfig)
     ```
   - Create API route: `app/api/auth/[...nextauth]/route.ts`
   - Create middleware for route protection: `middleware.ts`
   - Add `.env.local` variables:
     ```
     AUTH_SECRET=your-secret-here
     AUTH_URL=http://localhost:3000
     ```

2. **Test authentication flow** (3 min)
   - Create login page: `app/login/page.tsx`
   - Test sign-in: Navigate to `/login`, enter credentials
   - Verify session: Check `await auth()` returns user
   - Test protected route: Create `/dashboard` with middleware protection
   - Test sign-out: Verify session cleared after sign-out

**Success Criteria**:
- [ ] Setup completed in ≤15 minutes
- [ ] NextAuth v5 configured successfully
- [ ] Sign-in works (session created)
- [ ] Session persists across page refreshes
- [ ] Protected routes require authentication
- [ ] Sign-out works (session cleared)
- [ ] TypeScript types work (no errors)

**Metrics to Collect**:
- Actual setup time: _____ minutes
- Provider chosen (NextAuth/Clerk/Supabase/Auth0): _____
- Deviations from adoption blueprint: _____
- Issues encountered: _____

---

### Test 1.3: SAP-041 (Form Validation) - Target: 20 minutes

**Test Objective**: Validate React Hook Form + Zod setup, client/server validation, accessibility

**Steps**:

1. **Follow SAP-041 adoption-blueprint.md** (15 min)
   - Install dependencies: `npm install react-hook-form zod @hookform/resolvers`
   - Create Zod schema (`lib/validations/auth.ts`):
     ```typescript
     import { z } from "zod"

     export const signupSchema = z.object({
       email: z.string().email("Invalid email address"),
       password: z.string().min(8, "Password must be at least 8 characters"),
       confirmPassword: z.string()
     }).refine((data) => data.password === data.confirmPassword, {
       message: "Passwords don't match",
       path: ["confirmPassword"]
     })

     export type SignupFormData = z.infer<typeof signupSchema>
     ```
   - Create signup form component (`components/forms/SignupForm.tsx`)
   - Create Server Action (`actions/auth.ts`)
   - Add ARIA accessibility attributes

2. **Test form validation** (5 min)
   - Test client-side validation:
     - Submit empty form → See required field errors
     - Enter invalid email → See email error
     - Enter short password → See password length error
     - Enter mismatched passwords → See confirmPassword error
   - Test server-side validation:
     - Bypass client validation with DevTools
     - Verify server still validates and returns errors
   - Test accessibility:
     - Tab through fields (check focus order)
     - Screen reader announces errors (use NVDA/VoiceOver)
     - Errors associated with fields (aria-describedby)

**Success Criteria**:
- [ ] Setup completed in ≤20 minutes
- [ ] Client-side validation works (immediate feedback)
- [ ] Server-side validation works (cannot bypass)
- [ ] TypeScript types inferred from Zod schemas
- [ ] Error messages accessible (ARIA attributes)
- [ ] Forms work without JavaScript (progressive enhancement)
- [ ] No axe-core violations (run axe DevTools)

**Metrics to Collect**:
- Actual setup time: _____ minutes
- Deviations from adoption blueprint: _____
- Accessibility violations found: _____
- Issues encountered: _____

---

## Phase 2: Pairwise Integration Testing

### Test 2.1: SAP-034 + SAP-033 (Database + Auth) - Target: 10 minutes

**Test Objective**: Validate user authentication with database persistence

**Integration Points**:
1. Prisma schema includes User model with email/password
2. NextAuth Credentials provider verifies against database
3. Session stores user ID from database
4. Protected routes access user from database

**Steps**:

1. **Update Prisma schema** (2 min)
   ```prisma
   model User {
     id        String   @id @default(cuid())
     email     String   @unique
     name      String?
     password  String   // Hashed with bcrypt
     createdAt DateTime @default(now())
     updatedAt DateTime @updatedAt
   }
   ```
   Run migration: `npx prisma migrate dev --name add_user_auth`

2. **Update NextAuth to use database** (5 min)
   ```typescript
   // auth.config.ts
   import Credentials from "next-auth/providers/credentials"
   import { prisma } from "@/lib/prisma"
   import { compare } from "bcryptjs"

   export default {
     providers: [
       Credentials({
         async authorize(credentials) {
           const user = await prisma.user.findUnique({
             where: { email: credentials.email as string }
           })

           if (!user) return null

           const passwordMatch = await compare(
             credentials.password as string,
             user.password
           )

           if (!passwordMatch) return null

           return { id: user.id, email: user.email, name: user.name }
         }
       })
     ]
   } satisfies NextAuthConfig
   ```

3. **Test end-to-end flow** (3 min)
   - Create user in database (seed script or manual)
   - Sign in with database credentials
   - Verify session contains database user ID
   - Query database for user in protected route
   - Verify correct user data displayed

**Success Criteria**:
- [ ] Integration completed in ≤10 minutes
- [ ] NextAuth authenticates against Prisma database
- [ ] User sessions persist to database (if using database sessions)
- [ ] Protected routes can query user from database
- [ ] TypeScript types work across SAPs (User type shared)
- [ ] No TypeScript errors

**Metrics to Collect**:
- Actual integration time: _____ minutes
- Issues encountered: _____

---

### Test 2.2: SAP-033 + SAP-041 (Auth + Forms) - Target: 10 minutes

**Test Objective**: Validate protected form submission with authentication

**Integration Points**:
1. Form submission requires authentication
2. Server Actions access user session
3. Form errors handled with user context
4. Optimistic updates with user data

**Steps**:

1. **Create protected form** (3 min)
   ```typescript
   // app/profile/page.tsx
   import { auth } from "@/auth"
   import { redirect } from "next/navigation"
   import { ProfileForm } from "@/components/forms/ProfileForm"

   export default async function ProfilePage() {
     const session = await auth()

     if (!session) {
       redirect("/login")
     }

     return (
       <div>
         <h1>Update Profile</h1>
         <ProfileForm user={session.user} />
       </div>
     )
   }
   ```

2. **Create form with auth context** (5 min)
   ```typescript
   // actions/profile.ts
   "use server"

   import { auth } from "@/auth"
   import { profileSchema } from "@/lib/validations/profile"

   export async function updateProfile(formData: FormData) {
     const session = await auth()

     if (!session) {
       return { error: "Unauthorized" }
     }

     const validated = profileSchema.safeParse({
       name: formData.get("name"),
       email: formData.get("email")
     })

     if (!validated.success) {
       return { errors: validated.error.flatten().fieldErrors }
     }

     // Update user in database with session.user.id
     // ...

     return { success: true }
   }
   ```

3. **Test protected form flow** (2 min)
   - Access form while logged out → Redirected to login
   - Sign in → Access form with user data pre-filled
   - Submit form → Server Action verifies session
   - Invalid submission → Errors returned with user context
   - Valid submission → User data updated in database

**Success Criteria**:
- [ ] Integration completed in ≤10 minutes
- [ ] Forms require authentication (middleware protection)
- [ ] Server Actions access user session
- [ ] Form validation works with user context
- [ ] Optimistic updates preserve user data
- [ ] No TypeScript errors

**Metrics to Collect**:
- Actual integration time: _____ minutes
- Issues encountered: _____

---

## Phase 3: Full Integration Testing (All 3 SAPs)

### Test 3.1: Complete Signup Flow - Target: 15 minutes

**Test Objective**: Validate form → auth → database flow for new user signup

**Integration Flow**:
```
User submits signup form (SAP-041)
    ↓
Form validates client-side (Zod schema)
    ↓
Server Action validates server-side (Zod schema)
    ↓
Password hashed (bcrypt)
    ↓
User created in database (SAP-034, Prisma)
    ↓
User signed in (SAP-033, NextAuth)
    ↓
Redirected to dashboard with session
```

**Steps**:

1. **Create complete signup page** (5 min)
   ```typescript
   // app/signup/page.tsx
   import { SignupForm } from "@/components/forms/SignupForm"

   export default function SignupPage() {
     return (
       <div className="max-w-md mx-auto mt-10">
         <h1 className="text-2xl font-bold mb-6">Create an account</h1>
         <SignupForm />
       </div>
     )
   }
   ```

2. **Create signup Server Action** (7 min)
   ```typescript
   // actions/auth.ts
   "use server"

   import { signupSchema } from "@/lib/validations/auth"
   import { prisma } from "@/lib/prisma"
   import { hash } from "bcryptjs"
   import { signIn } from "@/auth"
   import { redirect } from "next/navigation"

   export async function signup(prevState: any, formData: FormData) {
     // 1. Validate with Zod (SAP-041)
     const validated = signupSchema.safeParse({
       email: formData.get("email"),
       password: formData.get("password"),
       confirmPassword: formData.get("confirmPassword")
     })

     if (!validated.success) {
       return {
         errors: validated.error.flatten().fieldErrors,
         message: "Validation failed"
       }
     }

     // 2. Check if user exists (SAP-034)
     const existingUser = await prisma.user.findUnique({
       where: { email: validated.data.email }
     })

     if (existingUser) {
       return {
         errors: { email: ["Email already registered"] },
         message: "Email already exists"
       }
     }

     // 3. Hash password and create user (SAP-034)
     const hashedPassword = await hash(validated.data.password, 10)

     const user = await prisma.user.create({
       data: {
         email: validated.data.email,
         password: hashedPassword
       }
     })

     // 4. Sign in user (SAP-033)
     await signIn("credentials", {
       email: validated.data.email,
       password: validated.data.password,
       redirect: false
     })

     // 5. Redirect to dashboard
     redirect("/dashboard")
   }
   ```

3. **Test complete flow** (3 min)
   - Navigate to `/signup`
   - Fill form with valid data
   - Submit form
   - Verify:
     - Client validation passes
     - Server validation passes
     - User created in database (check Prisma Studio)
     - User signed in (session created)
     - Redirected to dashboard
     - Dashboard shows correct user data

**Success Criteria**:
- [ ] Complete flow works in ≤15 minutes
- [ ] Form validation (client + server) works
- [ ] User created in database with hashed password
- [ ] User automatically signed in after signup
- [ ] Session persists (refresh page, still signed in)
- [ ] TypeScript types work across all 3 SAPs
- [ ] No TypeScript errors
- [ ] No accessibility violations (axe-core)

**Metrics to Collect**:
- Actual implementation time: _____ minutes
- Issues encountered: _____
- Developer satisfaction (1-5): _____

---

## Phase 4: SAP-027 Dogfooding Validation

### Validation Criteria (Per SAP-027 Standards)

**Time Savings Validation**:
- [ ] SAP-034 setup: ≤25 minutes (vs 3-4 hours manual = 89.6% savings)
- [ ] SAP-033 setup: ≤15 minutes (vs 3-4 hours manual = 93.75% savings)
- [ ] SAP-041 setup: ≤20 minutes (vs 2-3 hours manual = 88.9% savings)
- [ ] **Total setup**: ≤60 minutes (vs 8-11 hours manual = 90.9% savings)

**Functionality Validation**:
- [ ] All 3 SAPs work independently
- [ ] All 3 SAPs integrate correctly (no conflicts)
- [ ] Complete signup flow functional (form → auth → database)
- [ ] TypeScript type inference works (100%, no manual types)
- [ ] Progressive enhancement works (forms work without JS)

**Quality Validation**:
- [ ] **TypeScript**: 0 errors (`npm run type-check`)
- [ ] **Accessibility**: 0 violations (axe-core, Lighthouse 100/100)
- [ ] **Forms without JS**: Work correctly (disable JS, test form submission)
- [ ] **Bundle size**: ≤100KB for all 3 SAPs combined
- [ ] **Performance**: Forms submit in <100ms (local), <500ms (server)

**Developer Experience Validation**:
- [ ] Adoption blueprints accurate (no missing steps)
- [ ] Code examples copy-paste ready (no modifications needed)
- [ ] Error messages clear and actionable
- [ ] Documentation complete (no gaps found)
- [ ] Developer satisfaction ≥4/5

**Evidence Collection**:
- [ ] Screenshots of working signup flow
- [ ] Lighthouse accessibility report (100/100)
- [ ] Bundle size analysis (webpack-bundle-analyzer)
- [ ] Time tracking for each SAP setup
- [ ] List of issues/improvements for ledger.md feedback

---

## Phase 5: Advanced Integration Testing

### Test 5.1: Multi-Step Wizard with Auth + Database

**Objective**: Test SAP-041 Tier 4 (wizard) with SAP-033/034 integration

**Steps**:
1. Create 3-step onboarding wizard
2. Step 1: Account info (email, password)
3. Step 2: Profile info (name, avatar)
4. Step 3: Preferences (notifications, theme)
5. Save progress to database after each step
6. Require authentication for steps 2-3

**Success Criteria**:
- [ ] Wizard state persists across steps (URL state)
- [ ] Form validation works per step
- [ ] Database saves after each step
- [ ] Authentication required for protected steps
- [ ] Back button works (browser navigation)

---

### Test 5.2: Optimistic Updates with All 3 SAPs

**Objective**: Test useOptimistic with form submission

**Steps**:
1. Create profile update form
2. Implement optimistic update (immediate UI feedback)
3. Submit to Server Action with database update
4. Rollback on error, confirm on success

**Success Criteria**:
- [ ] UI updates immediately (optimistic)
- [ ] Server validates and updates database
- [ ] Rollback works on validation error
- [ ] Final state matches database
- [ ] Loading states shown correctly

---

## Results Summary Template

### Test Execution Summary

**Test Date**: _____
**Tester**: _____
**Environment**: Node.js _____, Next.js _____, PostgreSQL _____

**Phase 1: Individual SAP Testing**
- SAP-034 setup time: _____ min (target: 25 min) - [ ] PASS / [ ] FAIL
- SAP-033 setup time: _____ min (target: 15 min) - [ ] PASS / [ ] FAIL
- SAP-041 setup time: _____ min (target: 20 min) - [ ] PASS / [ ] FAIL

**Phase 2: Pairwise Integration**
- SAP-034 + SAP-033: _____ min (target: 10 min) - [ ] PASS / [ ] FAIL
- SAP-033 + SAP-041: _____ min (target: 10 min) - [ ] PASS / [ ] FAIL

**Phase 3: Full Integration**
- Complete signup flow: _____ min (target: 15 min) - [ ] PASS / [ ] FAIL

**Phase 4: Quality Validation**
- TypeScript errors: _____ (target: 0)
- Accessibility violations: _____ (target: 0)
- Lighthouse score: _____ (target: 100/100)
- Bundle size: _____ KB (target: ≤100KB)
- Forms work without JS: [ ] YES / [ ] NO

**Phase 5: Developer Experience**
- Developer satisfaction (1-5): _____
- Would recommend to others: [ ] YES / [ ] NO
- Issues found: _____

### Issues Encountered

| Issue | SAP | Severity | Resolution |
|-------|-----|----------|------------|
| | | | |

### Improvements for Ledger.md

| SAP | Improvement | Priority |
|-----|-------------|----------|
| | | |

### Overall Result

- [ ] ✅ PASS - All criteria met, ready for production
- [ ] ⚠️  CONDITIONAL PASS - Minor issues, can proceed with fixes
- [ ] ❌ FAIL - Major issues, requires rework

**Recommendation**: _____

---

## Next Steps After Validation

**If PASS**:
1. Update SAP status from "pilot" to "active" in sap-catalog.json
2. Add validation results to each SAP's ledger.md
3. Update RT-019-SAP-REQUIREMENTS.md with completion status
4. Create blog post/documentation showcasing the integration
5. Proceed to Weeks 7-8: User-Facing Features (SAP-035, SAP-036)

**If CONDITIONAL PASS**:
1. Document issues in each SAP's ledger.md
2. Create GitHub issues for each improvement
3. Prioritize fixes (P0, P1, P2)
4. Re-run validation after fixes
5. Proceed cautiously with dependent SAPs

**If FAIL**:
1. Document blocking issues in each SAP's ledger.md
2. Update SAP status to "draft" in sap-catalog.json
3. Create detailed GitHub issues for each blocker
4. Schedule rework sprint
5. Do NOT proceed to dependent SAPs until resolved

---

**Document Status**: Ready for Execution
**Last Updated**: 2025-11-09
**Owner**: chora-base React SAP Excellence Initiative
