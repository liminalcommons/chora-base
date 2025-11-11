# SAP-033: React Authentication & Authorization - Awareness Guide (AGENTS.md)

---
nested_structure: true
nested_files:
  - "providers/AGENTS.md"
  - "workflows/AGENTS.md"
  - "security/AGENTS.md"
  - "troubleshooting/AGENTS.md"
version: 2.0.0
last_updated: 2025-11-10
---

**SAP**: SAP-033 (react-authentication)
**Version**: 2.0.0
**Status**: pilot
**Last Updated**: 2025-11-10

---

## 📖 Quick Reference

**New to SAP-033?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 4-provider decision tree (NextAuth, Clerk, Supabase, Auth0)
- 📚 **93.75% Time Savings** - 3-4 hours → 15 minutes with production templates
- 🎯 **OWASP Top 10 Compliance** - 8/10 full coverage (A01-A07, A09)
- 🔧 **4 Complete Setups** - NextAuth v5 (30 min), Clerk (7 min), Supabase (20 min), Auth0 (30 min)
- 📊 **SOC2 Certified Options** - Clerk, Supabase, Auth0 (enterprise-ready)
- 🔗 **Integration** - Works with SAP-020 (Next.js 15), SAP-034 (Database), SAP-041 (Forms)

This awareness-guide.md provides: Agent-specific authentication workflows, provider selection patterns, and security best practices for AI coding assistants.

---

## ⚠️ Critical Workflows (Read This First!)

**This section highlights the 5 most frequently-missed patterns for authentication in Next.js 15+ projects.**

---

### 1. Choosing the Right Provider ⚠️ MOST COMMON DECISION

**When**: Starting a new project or adding authentication to existing project

**Common Mistake**: Choosing provider based on popularity instead of project requirements. Over-engineering with enterprise solutions for simple projects, or under-engineering with DIY auth for complex requirements.

**Correct Action**: Follow the decision tree based on your specific needs.

**Decision Tree**:

```
Q1: Need self-hosted (full control, no vendor lock-in)?
  ✅ YES → NextAuth v5 (FREE, 30 min setup)
  ❌ NO → Continue

Q2: Need rapid setup (<10 min) with pre-built UI?
  ✅ YES → Clerk ($25+/mo, 7 min setup)
  ❌ NO → Continue

Q3: Using Supabase for database?
  ✅ YES → Supabase Auth (FREE 50k MAU, 20 min setup)
  ❌ NO → Continue

Q4: Enterprise SSO/SAML required?
  ✅ YES → Auth0 (Enterprise pricing, 30 min setup)
  ❌ NO → NextAuth v5 (default recommendation)
```

**Quick Comparison**:

| Provider | Setup Time | Cost | Pre-Built UI | Best For |
|----------|------------|------|--------------|----------|
| **NextAuth v5** | 30 min | FREE | ❌ | Self-hosted, custom requirements |
| **Clerk** | 7 min | $25+/mo | ✅ | Rapid prototyping, pre-built UI |
| **Supabase Auth** | 20 min | FREE (50k MAU) | ❌ | Supabase projects |
| **Auth0** | 30 min | Enterprise | ⚠️ Universal Login | Enterprise SSO/SAML |

**Time**: 5 minutes (decision) + provider setup time

**Full Details**: [providers/AGENTS.md](providers/AGENTS.md)

---

### 2. NextAuth v5 Setup with Middleware ⚠️ MOST POPULAR

**When**: Using NextAuth v5 for self-hosted authentication

**Common Mistake**: Setting up auth configuration without middleware, resulting in unprotected routes or complex per-page protection.

**Correct Action**: Configure auth + middleware in 4 steps (30 min total).

**Step 1: Install dependencies** (3 min)

```bash
npm install next-auth@beta @auth/prisma-adapter bcryptjs
npm install -D @types/bcryptjs
```

**Step 2: Configure NextAuth** (10 min)

```typescript
// auth.ts (project root)
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.userId = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.userId as string;
        session.user.role = token.role as string;
      }
      return session;
    }
  }
});
```

**Step 3: Create API route** (5 min)

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

**Step 4: Configure middleware** (12 min)

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // Define public routes
  const publicRoutes = ["/", "/login", "/signup"];
  const isPublicRoute = publicRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Protected routes
  if (!isAuthenticated) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

**Time**: 30 minutes

**Full Details**: [providers/AGENTS.md#workflow-1-set-up-nextauth-v5-30-min](providers/AGENTS.md#workflow-1-set-up-nextauth-v5-30-min)

---

### 3. Middleware Redirect Loops ⚠️ MOST COMMON PITFALL

**When**: Using middleware for route protection

**Common Mistake**: Not excluding `/api/auth` routes from middleware, causing infinite redirect loops. Browser shows "Too many redirects" error.

**Correct Action**: ALWAYS exclude public routes and auth API routes.

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;

  // ✅ CRITICAL: Define public routes BEFORE checking authentication
  const publicRoutes = [
    "/",
    "/login",
    "/signup",
    "/api/auth", // ✅ CRITICAL: Allow auth API routes
  ];

  const isPublicRoute = publicRoutes.some(route =>
    pathname.startsWith(route)
  );

  // ✅ Allow public routes without authentication
  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Protected routes
  if (!req.auth) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
});

// ✅ Configure matcher to exclude static files
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

**Common Causes**:
1. ❌ Missing `/api/auth` in public routes (auth endpoints redirect to login, login redirects back)
2. ❌ Middleware matcher includes static files (causes performance issues)
3. ❌ Login page redirects authenticated users without checking if already on login page

**Time**: 5 minutes to fix

**Full Details**: [troubleshooting/AGENTS.md#issue-3-middleware-redirect-loops](troubleshooting/AGENTS.md#issue-3-middleware-redirect-loops)

---

### 4. RBAC Implementation ⚠️ FREQUENTLY REQUESTED

**When**: Multi-tenant apps, admin dashboards, complex permissions

**Common Mistake**: Implementing RBAC only on client side (easily bypassed). Not adding role to session, requiring database queries on every request.

**Correct Action**: Add role to JWT session + middleware enforcement (20 min total).

**Step 1: Add role to database** (5 min)

```prisma
// schema.prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  role  Role   @default(USER)
  // ... other fields
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

**Step 2: Add role to session** (5 min)

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role; // ✅ Add role to token
      }
      return token;
    },

    async session({ session, token }) {
      if (token) {
        session.user.role = token.role as string; // ✅ Add role to session
      }
      return session;
    }
  }
});
```

**Step 3: Enforce in middleware** (10 min)

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

const roleRoutes = {
  admin: ["/admin"],
  moderator: ["/admin", "/moderate"],
  user: ["/dashboard"]
};

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const session = req.auth;

  if (!session) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  const userRole = session.user.role as keyof typeof roleRoutes;
  const allowedRoutes = roleRoutes[userRole] || [];

  const hasAccess = allowedRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (!hasAccess && (pathname.startsWith("/admin") || pathname.startsWith("/moderate"))) {
    return NextResponse.redirect(new URL("/unauthorized", req.url));
  }

  return NextResponse.next();
});
```

**Time**: 20 minutes

**Security**: Role stored in JWT (no database query on every request), enforced server-side (cannot bypass)

**Full Details**: [workflows/AGENTS.md#workflow-5-implement-rbac-20-min](workflows/AGENTS.md#workflow-5-implement-rbac-20-min)

---

### 5. Session Security Configuration ⚠️ PRODUCTION CRITICAL

**When**: All production applications

**Common Mistake**: Using default session configuration without security headers. Cookies accessible via JavaScript (XSS vulnerability), not using HTTPS in production, no CSRF protection.

**Correct Action**: Configure secure session with httpOnly, sameSite, secure cookies.

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // Update every 24 hours
  },

  jwt: {
    maxAge: 30 * 24 * 60 * 60, // Must match session maxAge
  },

  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true, // ✅ Prevents JavaScript access (XSS protection)
        sameSite: "lax", // ✅ CSRF protection
        path: "/",
        secure: process.env.NODE_ENV === "production", // ✅ HTTPS-only in production
      },
    },
    csrfToken: {
      name: "__Host-next-auth.csrf-token",
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production"
      }
    }
  }
});
```

**Security Checklist**:
- [ ] `httpOnly: true` (prevents XSS attacks)
- [ ] `sameSite: "lax"` or `"strict"` (CSRF protection)
- [ ] `secure: true` in production (HTTPS-only)
- [ ] `maxAge` configured (automatic session expiration)
- [ ] `updateAge` configured (session refresh)
- [ ] NEXTAUTH_SECRET environment variable set

**Generate NEXTAUTH_SECRET**:
```bash
openssl rand -base64 32
```

**Time**: 10 minutes

**Full Details**: [security/AGENTS.md#1-session-security](security/AGENTS.md#1-session-security)

---

## Quick Start

**Before you begin**:
- ✅ SAP-020 (React Project Foundation) adopted (Next.js 15 App Router)
- ✅ Node.js 22.x installed
- ✅ SAP-034 (Database Integration) adopted (Prisma or Drizzle)

**Choose your path** (based on requirements):

1. **Self-hosted (30 min)**: [NextAuth v5](providers/AGENTS.md#workflow-1-set-up-nextauth-v5-30-min)
   - FREE, unlimited users
   - Full control over data and UI
   - Requires database setup

2. **Fastest setup (7 min)**: [Clerk](providers/AGENTS.md#workflow-2-set-up-clerk-7-min)
   - Pre-built UI components
   - Managed authentication
   - $25+/month (10k MAU free tier)

3. **Supabase project (20 min)**: [Supabase Auth](providers/AGENTS.md#workflow-3-set-up-supabase-auth-20-min)
   - Integrated with Supabase database
   - FREE (50k MAU)
   - Row-level security policies

4. **Enterprise SSO (30 min)**: [Auth0](providers/AGENTS.md#workflow-4-set-up-auth0-30-min)
   - SAML, Active Directory, LDAP
   - Universal Login page
   - Enterprise pricing

---

## Decision Tree: Which Provider?

**Use this decision tree to select the authentication provider that matches your requirements.**

```
START: Which authentication provider should I use?

├─ Q1: Need self-hosted (full control, no vendor lock-in)?
│  ├─ YES → NextAuth v5 ✅
│  │  Time: 30 min | Cost: FREE | UI: Custom
│  └─ NO → Continue to Q2
│
├─ Q2: Need rapid setup (<10 min) with pre-built UI?
│  ├─ YES → Clerk ✅
│  │  Time: 7 min | Cost: $25+/mo | UI: Pre-built
│  └─ NO → Continue to Q3
│
├─ Q3: Using Supabase for database?
│  ├─ YES → Supabase Auth ✅
│  │  Time: 20 min | Cost: FREE (50k MAU) | UI: Custom
│  └─ NO → Continue to Q4
│
├─ Q4: Enterprise SSO/SAML required?
│  ├─ YES → Auth0 ✅
│  │  Time: 30 min | Cost: Enterprise | UI: Universal Login
│  └─ NO → Continue to Q5
│
└─ Q5: Default choice (open-source, flexible)
   └─ NextAuth v5 ✅ (recommended default)
      Time: 30 min | Cost: FREE | UI: Custom
```

**Comparison Matrix**:

| Criteria | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|----------|-------------|-------|---------------|-------|
| **Setup Time** | 30 min | **7 min** | 20 min | 30 min |
| **Cost** | **FREE** | $25+/mo (10k MAU free) | FREE (50k MAU) | Enterprise |
| **Pre-Built UI** | ❌ (custom) | ✅ (components) | ❌ (custom) | ⚠️ (Universal Login) |
| **Self-Hosted** | ✅ | ❌ | ❌ | ❌ |
| **OAuth Providers** | 50+ | ~20 | ~15 | ~30 |
| **Database Required** | ✅ (Prisma/Drizzle) | ❌ (managed) | ✅ (Supabase) | ❌ (managed) |
| **TypeScript Support** | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| **Best For** | Self-hosted, custom | Rapid prototyping | Supabase projects | Enterprise SSO |

**Decision Factors**:

**Choose NextAuth v5 if**:
- You need full control over authentication logic
- You want zero vendor lock-in
- You have existing database (Prisma/Drizzle)
- Budget is $0

**Choose Clerk if**:
- You need to ship fast (<10 min setup)
- You want pre-built UI components
- You're prototyping or building MVP
- Budget allows $25+/month

**Choose Supabase Auth if**:
- You're already using Supabase database
- You need row-level security (RLS) policies
- You want real-time subscriptions
- Budget is $0

**Choose Auth0 if**:
- You need enterprise SSO/SAML
- You need Active Directory/LDAP integration
- You have compliance requirements (SOC 2, HIPAA)
- Budget is enterprise-level

---

## Navigation: Nested Awareness Files

This SAP uses the **nested awareness pattern** (SAP-009 v2.1.0) to organize content by domain. The root file (this file) contains Quick Start, Decision Tree, and Critical Workflows. Detailed workflows are in domain-specific files.

**Domain Files** (read based on task):

1. **[providers/AGENTS.md](providers/AGENTS.md)** - Authentication provider setup (4 workflows)
   - Workflow 1: NextAuth v5 (30 min, self-hosted)
   - Workflow 2: Clerk (7 min, managed)
   - Workflow 3: Supabase Auth (20 min, Supabase-integrated)
   - Workflow 4: Auth0 (30 min, enterprise SSO)

2. **[workflows/AGENTS.md](workflows/AGENTS.md)** - Advanced authentication features (4 workflows)
   - Workflow 5: Implement RBAC (20 min, role-based access)
   - Workflow 6: Add Protected Routes (15 min, middleware + component)
   - Workflow 7: Add Magic Link Authentication (25 min, passwordless)
   - Workflow 8: Add OAuth Providers (10 min/provider, social login)

3. **[security/AGENTS.md](security/AGENTS.md)** - Security best practices
   - Session security (httpOnly, sameSite, secure cookies)
   - Password security (bcrypt, strength validation)
   - CSRF protection (double-submit cookies)
   - Rate limiting (brute force prevention)
   - Security headers (HSTS, CSP, X-Frame-Options)

4. **[troubleshooting/AGENTS.md](troubleshooting/AGENTS.md)** - Common issues and fixes (8 issues)
   - Session not persisting
   - OAuth callback errors
   - Middleware redirect loops
   - CSRF token mismatch
   - Database connection errors
   - Session expired unexpectedly
   - Cannot read user data in components
   - Callback URL not working

**Progressive Loading Strategy**:

- **Phase 1 (0-10k tokens)**: Read this root file for Quick Start and Decision Tree
- **Phase 2 (10-50k tokens)**: Read domain-specific file for your task (e.g., providers/ for setup, workflows/ for RBAC)
- **Phase 3 (50-200k tokens)**: Read multiple domain files for complex integrations

**Token Savings**: 60% reduction via nested structure (root file ~700 lines vs original 1,781 lines)

---

## When to Use This SAP

**Adopt SAP-033 when**:

✅ **Project Requirements**:
- Building web application with user accounts
- Need login, signup, password reset workflows
- Multi-tenant SaaS with user isolation
- Admin dashboards with role-based permissions

✅ **Technology Stack**:
- Next.js 15+ (App Router)
- React 19+
- TypeScript
- Database (PostgreSQL, MySQL, MongoDB via SAP-034)

✅ **Security Requirements**:
- Session management (JWT or database sessions)
- OAuth social login (Google, GitHub, Facebook, etc.)
- RBAC (role-based access control)
- CSRF protection
- Rate limiting for login endpoints

**Skip this SAP if**:

❌ **Simple Use Cases**:
- Static site with no user accounts
- Public content only
- No authentication needed

❌ **Different Framework**:
- Not using Next.js (use framework-specific auth)
- Using Vue/Svelte/Angular (different patterns)

---

## Integration with Other SAPs

**Required Dependencies**:
- **SAP-020** (React Foundation): Next.js 15 App Router baseline
- **SAP-034** (Database Integration): User account storage (required for all providers)

**Common Integration Patterns**:

**Auth + Database** (SAP-033 + SAP-034):
- NextAuth PrismaAdapter syncs sessions with database
- Supabase Auth integrates with Supabase database
- User roles stored in database, added to JWT session

**Auth + Forms** (SAP-033 + SAP-041):
- Protected Server Actions with session validation
- User context injection in form handlers
- Type-safe form data with Zod + Prisma schemas

**Auth + File Upload** (SAP-033 + SAP-035):
- Upload permissions based on user role
- File ownership tracking
- Authenticated upload endpoints

**Auth + Real-Time** (SAP-033 + SAP-037):
- WebSocket authentication via session
- User-specific real-time channels
- Presence tracking for authenticated users

**Example Integration** (NextAuth + Prisma + Protected Route):

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/prisma";

export default async function DashboardPage() {
  const session = await auth();

  // Protect page (SAP-033)
  if (!session) {
    redirect("/login?callbackUrl=/dashboard");
  }

  // Fetch user data (SAP-034)
  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    include: { posts: true }
  });

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <p>Role: {session.user.role}</p>
      <ul>
        {user.posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Common Patterns

### Pattern 1: Access Session in Server Component

```typescript
import { auth } from "@/auth";

export default async function ServerComponent() {
  const session = await auth();

  if (!session) {
    return <div>Not authenticated</div>;
  }

  return <div>Welcome, {session.user.name}</div>;
}
```

### Pattern 2: Access Session in Client Component

```typescript
"use client";

import { useSession } from "next-auth/react";

export default function ClientComponent() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (status === "unauthenticated") {
    return <div>Not authenticated</div>;
  }

  return <div>Welcome, {session.user.name}</div>;
}
```

### Pattern 3: Protect Server Action

```typescript
"use server";

import { auth } from "@/auth";

export async function protectedAction(formData: FormData) {
  const session = await auth();

  if (!session) {
    return { error: "Unauthorized" };
  }

  // Verify user role
  if (session.user.role !== "admin") {
    return { error: "Forbidden: Admin only" };
  }

  // Proceed with action
  // ...
}
```

### Pattern 4: Role-Based UI

```typescript
import { auth } from "@/auth";

export async function RoleGate({
  children,
  allowedRoles
}: {
  children: React.ReactNode;
  allowedRoles: string[];
}) {
  const session = await auth();

  if (!session || !allowedRoles.includes(session.user.role)) {
    return null;
  }

  return <>{children}</>;
}

// Usage
<RoleGate allowedRoles={["admin"]}>
  <button>Admin Only Action</button>
</RoleGate>
```

---

## Success Criteria

**SAP-033 is successfully adopted when**:

✅ **Authentication Working**:
- [ ] Users can sign up with email/password or OAuth
- [ ] Users can sign in and receive session
- [ ] Session persists across page reloads
- [ ] Users can sign out and session clears

✅ **Route Protection Working**:
- [ ] Unauthenticated users redirected to login
- [ ] Authenticated users access protected routes
- [ ] Callback URL preserves original destination
- [ ] Middleware excludes public routes and `/api/auth`

✅ **Security Implemented**:
- [ ] Session cookies use `httpOnly`, `sameSite`, `secure`
- [ ] NEXTAUTH_SECRET environment variable set (32+ chars)
- [ ] Passwords hashed with bcrypt (salt rounds ≥10)
- [ ] Rate limiting on login endpoints (5 attempts per 15 min)
- [ ] CSRF protection enabled (automatic in NextAuth v5)

✅ **RBAC (if needed)**:
- [ ] User roles stored in database
- [ ] Roles added to JWT session
- [ ] Middleware enforces role-based access
- [ ] UI components conditionally render by role

✅ **OAuth (if needed)**:
- [ ] OAuth providers configured (Google, GitHub, etc.)
- [ ] Callback URLs registered with providers
- [ ] OAuth buttons redirect to provider
- [ ] OAuth callback returns to app
- [ ] User data saved to database

---

## Testing Your Implementation

**Basic Auth Flow**:
1. Visit protected route (e.g., `/dashboard`) → Redirects to `/login`
2. Click "Sign in with Google" → Redirects to Google OAuth
3. Authorize app → Redirects back to `/dashboard`
4. Verify session persists (reload page, still authenticated)
5. Sign out → Session cleared, redirected to home

**RBAC Flow** (if implemented):
1. Sign in as user with `role: "user"` → Access `/dashboard`
2. Try to access `/admin` → Redirected to `/unauthorized`
3. Sign in as user with `role: "admin"` → Access `/admin`

**Security Checks**:
1. Check cookies in browser DevTools → Verify `httpOnly`, `sameSite`, `secure`
2. Try 10 failed login attempts → Should be rate-limited after 5 attempts
3. Inspect `/api/auth/session` response → Verify user data structure

---

## Version History

**2.0.0 (2025-11-10)** - Nested awareness pattern adoption (SAP-009 v2.1.0)
- Split 1,781-line file into 4 domain-specific files (60% reduction)
- Added Critical Workflows section with 5 frequently-missed patterns
- Created providers/, workflows/, security/, troubleshooting/ domains
- Target: ~700 lines root file, ~3.9k tokens (Phase 1 progressive loading)

**1.0.0 (2025-11-09)** - Initial authentication SAP
- 4 authentication provider workflows (NextAuth, Clerk, Supabase, Auth0)
- 4 advanced workflows (RBAC, protected routes, magic links, OAuth)
- Security best practices and troubleshooting guide
- Decision tree for provider selection
