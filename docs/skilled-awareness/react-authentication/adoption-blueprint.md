# SAP-033: React Authentication & Authorization - Adoption Blueprint

**SAP ID**: SAP-033
**Name**: react-authentication
**Version**: 1.0.0
**Last Updated**: 2025-11-09
**Diataxis Type**: Tutorial

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Decision Point: Provider Selection](#decision-point-provider-selection)
3. [Path A: NextAuth v5 Setup](#path-a-nextauth-v5-setup)
4. [Path B: Clerk Setup](#path-b-clerk-setup)
5. [Path C: Supabase Auth Setup](#path-c-supabase-auth-setup)
6. [Path D: Auth0 Setup](#path-d-auth0-setup)
7. [Verification](#verification)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before adopting SAP-033, ensure you have:

### Required

- ✅ **Node.js 22.x** installed
- ✅ **SAP-020** (React Project Foundation) adopted
  - Next.js 15 App Router configured
  - TypeScript enabled
  - Basic project structure in place
- ✅ **Git repository** initialized
- ✅ **Code editor** (VS Code recommended)

### Optional (Provider-Specific)

- **NextAuth v5**: SAP-034 (Database Integration) - Prisma or Drizzle configured
- **Clerk**: Clerk account created at https://clerk.com
- **Supabase Auth**: Supabase project created at https://supabase.com
- **Auth0**: Auth0 account created at https://auth0.com

### Knowledge Requirements

- ✅ Basic React/Next.js knowledge
- ✅ Understanding of environment variables
- ✅ Familiarity with async/await
- ⚠️ OAuth2 knowledge (helpful but not required)

---

## Decision Point: Provider Selection

**Before starting**, choose your authentication provider using this 4-way comparison:

### Quick Decision Matrix

| If you need... | Choose | Reason |
|----------------|--------|--------|
| **Fastest setup (<10 min)** | Clerk | 7-minute setup, pre-built UI |
| **Self-hosted (no vendor lock-in)** | NextAuth v5 | MIT open-source, full control |
| **Supabase database integration** | Supabase Auth | Native RLS, tight integration |
| **Enterprise SSO/SAML** | Auth0 | 11k+ customers, 99.99% SLA |
| **Maximum OAuth providers (50+)** | NextAuth v5 | Most comprehensive |
| **Pre-built beautiful UI** | Clerk | Best-in-class components |
| **Free tier (unlimited)** | NextAuth v5 | No usage fees |
| **Phone OTP authentication** | Supabase Auth or Clerk | Built-in SMS support |

---

### Detailed Comparison Table

| Feature | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|---------|-------------|-------|---------------|-------|
| **Setup Time** | 30 min | **7 min** | 20 min | 30 min |
| **Cost** | **FREE** | $25+/mo | FREE (50k MAU) | Enterprise |
| **Self-Hosted** | ✅ | ❌ | ❌ | ❌ |
| **Pre-Built UI** | ❌ | ✅ | ❌ | ⚠️ Universal Login |
| **OAuth Providers** | 50+ | ~20 | ~15 | ~30 |
| **Edge Runtime** | ✅ | ✅ | ⚠️ Limited | ⚠️ Limited |
| **Database Sessions** | ✅ | ❌ Managed | ✅ Native | ❌ Managed |
| **Magic Links** | ⚠️ DIY | ✅ | ✅ | ✅ |
| **MFA** | ⚠️ DIY | ✅ | ⚠️ Phone only | ✅ Advanced |
| **SSO/SAML** | ⚠️ DIY | ⚠️ Limited | ❌ | ✅ |
| **Learning Curve** | Medium | Low | Medium | High |

---

### Decision Tree

```
START: Which provider should I use?

├─ Q1: Need self-hosted (full control)?
│  ├─ YES → NextAuth v5 (Path A)
│  └─ NO → Continue
│
├─ Q2: Need rapid setup (<10 min)?
│  ├─ YES → Clerk (Path B)
│  └─ NO → Continue
│
├─ Q3: Using Supabase?
│  ├─ YES → Supabase Auth (Path C)
│  └─ NO → Continue
│
├─ Q4: Enterprise SSO/SAML?
│  ├─ YES → Auth0 (Path D)
│  └─ NO → NextAuth v5 (Path A - default)
```

**Made your choice?** Jump to your provider's path:
- [Path A: NextAuth v5](#path-a-nextauth-v5-setup) (30 min)
- [Path B: Clerk](#path-b-clerk-setup) (7 min - fastest)
- [Path C: Supabase Auth](#path-c-supabase-auth-setup) (20 min)
- [Path D: Auth0](#path-d-auth0-setup) (30 min)

---

## Path A: NextAuth v5 Setup

**Total Time**: 30 minutes
**Cost**: FREE (unlimited)
**Best For**: Self-hosted, custom requirements, maximum flexibility

---

### Step 1: Install Dependencies (3 min)

```bash
# Install NextAuth v5 (beta)
npm install next-auth@beta @auth/prisma-adapter

# Install password hashing
npm install bcryptjs
npm install -D @types/bcryptjs

# Verify installation
npm list next-auth
# Should show: next-auth@5.0.0-beta.25 or higher
```

**Expected Output**:
```
added 15 packages, and audited 350 packages in 45s
```

---

### Step 2: Generate Secret Key (2 min)

```bash
# Generate NEXTAUTH_SECRET
openssl rand -base64 32
```

**Expected Output** (example):
```
jH8kL9mN3pQ5rS7tU1vW2xY4zA6bC8dE0fG2hI4jK6mN8pQ
```

**Copy this output** - you'll use it in Step 3.

---

### Step 3: Configure Environment Variables (2 min)

Create or update `.env.local`:

```bash
# .env.local

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=jH8kL9mN3pQ5rS7tU1vW2xY4zA6bC8dE0fG2hI4jK6mN8pQ

# Google OAuth (optional - get from https://console.cloud.google.com)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here

# GitHub OAuth (optional - get from https://github.com/settings/developers)
GITHUB_CLIENT_ID=your-github-client-id-here
GITHUB_CLIENT_SECRET=your-github-client-secret-here
```

**Note**: Replace `NEXTAUTH_SECRET` with your generated value from Step 2.

**For OAuth Setup** (optional, can skip for now):
- Google: https://console.cloud.google.com → Create project → Credentials
- GitHub: https://github.com/settings/developers → New OAuth App

---

### Step 4: Update Prisma Schema (4 min)

**If using SAP-034 with Prisma:**

```prisma
// prisma/schema.prisma

// Add these models (keep existing models)
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  role          String    @default("user") // Custom field for RBAC
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String?
  access_token      String?
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String?
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

**Run migration**:
```bash
npx prisma migrate dev --name add-nextauth-tables
npx prisma generate
```

**Expected Output**:
```
Environment variables loaded from .env.local
Prisma schema loaded from prisma/schema.prisma

✔ Generated Prisma Client (5.0.0) to ./node_modules/@prisma/client
```

---

### Step 5: Create Auth Configuration (5 min)

Create `auth.ts` in project root:

```typescript
// auth.ts
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma"; // Adjust path if needed

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),

  session: {
    strategy: "jwt", // or "database" for database sessions
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },

  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code" // PKCE enabled
        }
      }
    }),

    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    })
  ],

  callbacks: {
    // Add custom fields to JWT
    async jwt({ token, user }) {
      if (user) {
        token.userId = user.id;
        token.role = user.role || "user";
      }
      return token;
    },

    // Add custom fields to session
    async session({ session, token }) {
      if (token) {
        session.user.id = token.userId as string;
        session.user.role = token.role as string;
      }
      return session;
    }
  },

  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/error'
  },

  // Security settings
  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true,  // XSS protection
        sameSite: "lax", // CSRF protection
        path: "/",
        secure: process.env.NODE_ENV === "production"
      }
    }
  }
});
```

**Update TypeScript types** (`types/next-auth.d.ts`):

```typescript
// types/next-auth.d.ts
import NextAuth, { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      role: string;
    } & DefaultSession["user"];
  }

  interface User {
    role: string;
  }
}

declare module "@auth/core/jwt" {
  interface JWT {
    userId: string;
    role: string;
  }
}
```

---

### Step 6: Add API Route Handler (2 min)

Create API route:

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

---

### Step 7: Create Middleware (5 min)

Create `middleware.ts` in project root:

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // Public routes (no auth required)
  const publicRoutes = ["/", "/login", "/signup", "/api/auth", "/error"];
  const isPublicRoute = publicRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Protected routes (auth required)
  if (!isAuthenticated) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

### Step 8: Create Login Page (4 min)

```typescript
// app/login/page.tsx
"use client";

import { signIn } from "next-auth/react";
import { useSearchParams } from "next/navigation";

export default function LoginPage() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard";

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Welcome</h1>
          <p className="mt-2 text-gray-600">Sign in to continue</p>
        </div>

        <div className="space-y-3">
          <button
            onClick={() => signIn("google", { callbackUrl })}
            className="w-full flex items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <svg className="h-5 w-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>

          <button
            onClick={() => signIn("github", { callbackUrl })}
            className="w-full flex items-center justify-center gap-3 rounded-lg bg-gray-900 px-4 py-3 text-sm font-medium text-white hover:bg-gray-800"
          >
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd"/>
            </svg>
            Continue with GitHub
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

### Step 9: Create Dashboard Page (2 min)

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="mt-6 rounded-lg bg-white p-6 shadow">
          <h2 className="text-xl font-semibold">Welcome back!</h2>
          <div className="mt-4 space-y-2">
            <p><strong>Name:</strong> {session.user.name}</p>
            <p><strong>Email:</strong> {session.user.email}</p>
            <p><strong>Role:</strong> {session.user.role}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

### Step 10: Test Authentication (3 min)

```bash
# Start development server
npm run dev
```

**Manual Testing**:
1. ✅ Navigate to `http://localhost:3000/dashboard`
   - Should redirect to `/login?callbackUrl=/dashboard`
2. ✅ Click "Continue with Google" or "Continue with GitHub"
   - OAuth flow should open in new window/tab
3. ✅ Complete OAuth authorization
   - Should redirect back to `/dashboard`
4. ✅ Verify user data displayed on dashboard
   - Name, email, role should be visible
5. ✅ Refresh page
   - Session should persist (no redirect to login)

**Expected Result**: You should see your dashboard with user information.

---

### ✅ Path A Complete!

**Congratulations!** You've successfully set up NextAuth v5.

**What you've built**:
- ✅ OAuth authentication (Google, GitHub)
- ✅ Session management with JWT
- ✅ Protected routes via middleware
- ✅ Type-safe session data
- ✅ OWASP-compliant security (PKCE, HTTP-only cookies)

**Total Time**: 30 minutes

**Next**: Jump to [Verification](#verification)

---

## Path B: Clerk Setup

**Total Time**: 7 minutes (fastest)
**Cost**: FREE tier (5k MAU), then $25+/mo
**Best For**: Rapid prototyping, pre-built UI, beautiful UX

---

### Step 1: Create Clerk Account (2 min)

1. Go to https://clerk.com
2. Click "Start building for free"
3. Sign up with email or GitHub
4. Create new application:
   - Name: "Your App Name"
   - Sign-in options: Email, Google, GitHub (select all)
   - Click "Create application"

**Expected Result**: Dashboard showing API keys

---

### Step 2: Copy API Keys (1 min)

In Clerk Dashboard:
1. Go to "API Keys" (left sidebar)
2. Copy **Publishable key** and **Secret key**

**Example keys**:
```
Publishable key: pk_test_Z3JlYXQtcGFycm90LTU4LmNsZXJrLmFjY291bnRzLmRldiQ
Secret key: sk_test_abcdefghijklmnopqrstuvwxyz123456
```

---

### Step 3: Install Clerk SDK (1 min)

```bash
npm install @clerk/nextjs
```

**Expected Output**:
```
added 12 packages, and audited 362 packages in 38s
```

---

### Step 4: Configure Environment Variables (1 min)

Create or update `.env.local`:

```bash
# .env.local

# Clerk Configuration
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your-key-here
CLERK_SECRET_KEY=sk_test_your-secret-here

# Redirect URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_URL=/dashboard
NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_URL=/dashboard
```

**Replace** `pk_test_your-key-here` and `sk_test_your-secret-here` with your actual keys from Step 2.

---

### Step 5: Wrap App with ClerkProvider (1 min)

Update root layout:

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

---

### Step 6: Create Sign-In and Sign-Up Pages (1 min)

**Sign-In Page**:
```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn />
    </div>
  );
}
```

**Sign-Up Page**:
```typescript
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignUp />
    </div>
  );
}
```

---

### Step 7: Create Dashboard Page (1 min)

```typescript
// app/dashboard/page.tsx
import { auth, currentUser } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect('/sign-in');
  }

  const user = await currentUser();

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="mt-6 rounded-lg bg-white p-6 shadow">
          <h2 className="text-xl font-semibold">Welcome back!</h2>
          <div className="mt-4 space-y-2">
            <p><strong>Name:</strong> {user?.firstName} {user?.lastName}</p>
            <p><strong>Email:</strong> {user?.emailAddresses[0]?.emailAddress}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

### Step 8: Test Authentication (1 min)

```bash
# Start development server
npm run dev
```

**Manual Testing**:
1. ✅ Navigate to `http://localhost:3000/sign-up`
   - Should see beautiful Clerk sign-up UI
2. ✅ Create account with email/password
3. ✅ Check email for verification link
4. ✅ Click verification link
5. ✅ Navigate to `/dashboard`
   - Should see your dashboard with user data

**Expected Result**: Pre-built, beautiful authentication UI with zero custom code.

---

### ✅ Path B Complete!

**Congratulations!** You've successfully set up Clerk in **7 minutes**.

**What you've built**:
- ✅ Pre-built sign-in/sign-up UI (zero custom code)
- ✅ Email verification (automatic)
- ✅ Session management (automatic)
- ✅ Protected routes
- ✅ SOC2 Type II certified security

**Total Time**: 7 minutes (fastest setup)

**Next**: Jump to [Verification](#verification)

---

## Path C: Supabase Auth Setup

**Total Time**: 20 minutes
**Cost**: FREE tier (50k MAU)
**Best For**: Supabase projects, Row-Level Security (RLS)

---

### Step 1: Create Supabase Project (3 min)

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New project"
5. Fill in project details:
   - Name: "Your App Name"
   - Database Password: (generate strong password)
   - Region: (select closest to you)
   - Pricing Plan: Free
6. Click "Create new project"
7. **Wait ~2 minutes** for database provisioning

**Expected Result**: Project dashboard with "Project is ready" message

---

### Step 2: Copy API Credentials (1 min)

In Supabase Dashboard:
1. Go to "Settings" (left sidebar, gear icon)
2. Click "API" tab
3. Copy:
   - **Project URL**: `https://abcdefghijklmn.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### Step 3: Install Supabase SDK (2 min)

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Expected Output**:
```
added 8 packages, and audited 358 packages in 32s
```

---

### Step 4: Configure Environment Variables (1 min)

Create or update `.env.local`:

```bash
# .env.local

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Replace** with your actual values from Step 2.

---

### Step 5: Create Supabase Clients (4 min)

**Server Client**:
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: any) {
          try {
            cookieStore.set({ name, value, ...options });
          } catch (error) {
            // Server component cannot set cookies
          }
        },
        remove(name: string, options: any) {
          try {
            cookieStore.set({ name, value: '', ...options });
          } catch (error) {
            // Server component cannot remove cookies
          }
        },
      },
    }
  );
}
```

**Client Client**:
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

---

### Step 6: Create Middleware (3 min)

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: any) {
          request.cookies.set({ name, value, ...options });
          supabaseResponse = NextResponse.next({ request });
          supabaseResponse.cookies.set({ name, value, ...options });
        },
        remove(name: string, options: any) {
          request.cookies.set({ name, value: '', ...options });
          supabaseResponse = NextResponse.next({ request });
          supabaseResponse.cookies.set({ name, value: '', ...options });
        },
      },
    }
  );

  const { data: { session } } = await supabase.auth.getSession();

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

### Step 7: Create Login Page (4 min)

```typescript
// app/login/page.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function LoginPage() {
  const router = useRouter();
  const supabase = createClient();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);

    const { error } = await supabase.auth.signInWithPassword({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      router.push('/dashboard');
      router.refresh();
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-lg"
      >
        <div className="text-center">
          <h1 className="text-3xl font-bold">Sign In</h1>
          <p className="mt-2 text-gray-600">Welcome back</p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-blue-600 px-4 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>

        <p className="text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/signup" className="font-medium text-blue-600 hover:underline">
            Sign up
          </a>
        </p>
      </form>
    </div>
  );
}
```

**Sign-Up Page** (similar):
```typescript
// app/signup/page.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function SignupPage() {
  const router = useRouter();
  const supabase = createClient();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);

    const { error } = await supabase.auth.signUp({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      }
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      router.push('/verify-email');
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6 p-8">
      <h1 className="text-3xl font-bold text-center">Sign Up</h1>

      <input
        name="email"
        type="email"
        placeholder="Email"
        className="w-full px-4 py-2 border rounded"
        required
      />

      <input
        name="password"
        type="password"
        placeholder="Password (min 6 chars)"
        className="w-full px-4 py-2 border rounded"
        required
      />

      {error && <p className="text-red-500">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        {loading ? 'Creating account...' : 'Sign up'}
      </button>
    </form>
  );
}
```

---

### Step 8: Create Dashboard Page (2 min)

```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const supabase = await createClient();

  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="mt-6 rounded-lg bg-white p-6 shadow">
          <h2 className="text-xl font-semibold">Welcome back!</h2>
          <div className="mt-4 space-y-2">
            <p><strong>Email:</strong> {session.user.email}</p>
            <p><strong>User ID:</strong> {session.user.id}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

### Step 9: Test Authentication (2 min)

```bash
# Start development server
npm run dev
```

**Manual Testing**:
1. ✅ Navigate to `http://localhost:3000/signup`
2. ✅ Create account with email/password
3. ✅ Check email for verification link
4. ✅ Click verification link
5. ✅ Navigate to `/login`
6. ✅ Sign in with credentials
7. ✅ Verify redirect to `/dashboard`
8. ✅ Verify email displayed

**Expected Result**: Dashboard showing authenticated user's email.

---

### ✅ Path C Complete!

**Congratulations!** You've successfully set up Supabase Auth.

**What you've built**:
- ✅ Email/password authentication
- ✅ Email verification (automatic)
- ✅ Session management (automatic)
- ✅ Protected routes
- ✅ Ready for Row-Level Security (RLS)

**Total Time**: 20 minutes

**Next**: Jump to [Verification](#verification)

---

## Path D: Auth0 Setup

**Total Time**: 30 minutes
**Cost**: FREE tier (7k MAU), then enterprise pricing
**Best For**: Enterprise SSO, SAML, compliance

---

### Step 1: Create Auth0 Account (5 min)

1. Go to https://auth0.com
2. Click "Sign up"
3. Create account with email or GitHub
4. Create new tenant:
   - Tenant Domain: `your-company` (becomes `your-company.auth0.com`)
   - Region: (select closest)
   - Click "Create"
5. Create new application:
   - Name: "Your App Name"
   - Type: "Regular Web Applications"
   - Click "Create"

**Expected Result**: Application settings page with Client ID and Secret

---

### Step 2: Configure Application Settings (3 min)

In Auth0 Dashboard (Application settings):

1. Scroll to "Application URIs"
2. Fill in:
   - **Allowed Callback URLs**: `http://localhost:3000/api/auth/callback`
   - **Allowed Logout URLs**: `http://localhost:3000`
   - **Allowed Web Origins**: `http://localhost:3000`
3. Click "Save Changes"

**Copy these values**:
- **Domain**: `your-company.auth0.com`
- **Client ID**: `abc123...`
- **Client Secret**: `xyz789...`

---

### Step 3: Install Auth0 SDK (2 min)

```bash
npm install @auth0/nextjs-auth0
```

**Expected Output**:
```
added 10 packages, and audited 360 packages in 35s
```

---

### Step 4: Generate Secret (2 min)

```bash
openssl rand -hex 32
```

**Expected Output** (example):
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

**Copy this output** - you'll use it in Step 5.

---

### Step 5: Configure Environment Variables (2 min)

Create or update `.env.local`:

```bash
# .env.local

# Auth0 Configuration
AUTH0_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
AUTH0_BASE_URL=http://localhost:3000
AUTH0_ISSUER_BASE_URL=https://your-company.auth0.com
AUTH0_CLIENT_ID=abc123...
AUTH0_CLIENT_SECRET=xyz789...

# Optional: Session configuration
AUTH0_SESSION_COOKIE_LIFETIME=604800  # 7 days in seconds
AUTH0_SESSION_ROLLING=true
```

**Replace** placeholders with your actual values from Steps 2 and 4.

---

### Step 6: Create API Route Handler (2 min)

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth } from '@auth0/nextjs-auth0';

export const GET = handleAuth();
```

**That's it!** This single line handles all auth routes:
- `/api/auth/login`
- `/api/auth/logout`
- `/api/auth/callback`
- `/api/auth/me`

---

### Step 7: Create Middleware (Optional - 3 min)

```typescript
// middleware.ts
import { withMiddlewareAuthRequired } from '@auth0/nextjs-auth0/edge';

export default withMiddlewareAuthRequired();

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/settings/:path*'],
};
```

**Alternative** (more control):
```typescript
// middleware.ts
import { getSession } from '@auth0/nextjs-auth0/edge';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const session = await getSession(req, res);

  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/api/auth/login', req.url));
  }

  return res;
}
```

---

### Step 8: Create Dashboard Page (3 min)

```typescript
// app/dashboard/page.tsx
import { getSession } from '@auth0/nextjs-auth0';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await getSession();

  if (!session) {
    redirect('/api/auth/login');
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="mt-6 rounded-lg bg-white p-6 shadow">
          <h2 className="text-xl font-semibold">Welcome back!</h2>
          <div className="mt-4 space-y-2">
            <p><strong>Name:</strong> {session.user.name}</p>
            <p><strong>Email:</strong> {session.user.email}</p>
            <p><strong>User ID:</strong> {session.user.sub}</p>
          </div>

          <a
            href="/api/auth/logout"
            className="mt-6 inline-block rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700"
          >
            Log out
          </a>
        </div>
      </div>
    </div>
  );
}
```

---

### Step 9: Create Home Page with Login Button (2 min)

```typescript
// app/page.tsx
export default function HomePage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Welcome</h1>
        <p className="mt-4 text-gray-600">Sign in to continue</p>

        <a
          href="/api/auth/login"
          className="mt-6 inline-block rounded-lg bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
        >
          Log in
        </a>
      </div>
    </div>
  );
}
```

---

### Step 10: Test Authentication (3 min)

```bash
# Start development server
npm run dev
```

**Manual Testing**:
1. ✅ Navigate to `http://localhost:3000`
2. ✅ Click "Log in"
   - Should redirect to Auth0 Universal Login page
3. ✅ Click "Sign up" (on Auth0 page)
4. ✅ Create account with email/password
5. ✅ Complete email verification (check inbox)
6. ✅ Sign in
   - Should redirect back to `/dashboard`
7. ✅ Verify user data displayed
8. ✅ Test logout (click "Log out" button)
   - Should redirect to home page

**Expected Result**: Universal Login page with professional UI, then dashboard with user info.

---

### ✅ Path D Complete!

**Congratulations!** You've successfully set up Auth0.

**What you've built**:
- ✅ Universal Login (hosted login pages)
- ✅ Email/password authentication
- ✅ Email verification (automatic)
- ✅ Session management (automatic)
- ✅ Protected routes
- ✅ Enterprise-ready (99.99% uptime SLA)

**Total Time**: 30 minutes

**Next**: Jump to [Verification](#verification)

---

## Verification

**Run this checklist** regardless of which provider you chose:

### Authentication Checklist

- [ ] **Step 1**: User can navigate to login page
  ```bash
  # NextAuth: http://localhost:3000/login
  # Clerk: http://localhost:3000/sign-in
  # Supabase/Auth0: http://localhost:3000/login
  ```

- [ ] **Step 2**: User can create account (if applicable)
  - Clerk: Sign up at `/sign-up`
  - Supabase: Sign up at `/signup`
  - Auth0: Click "Sign up" on Universal Login
  - NextAuth: OAuth only (no email/password by default)

- [ ] **Step 3**: User can sign in
  - Click login button
  - Complete OAuth or email/password flow
  - Should redirect to dashboard

- [ ] **Step 4**: Dashboard displays user data
  - Name, email, or user ID visible
  - No console errors

- [ ] **Step 5**: Session persists across page reloads
  - Refresh `/dashboard`
  - Should NOT redirect to login
  - User data still visible

- [ ] **Step 6**: Protected routes redirect unauthenticated users
  - Open incognito window
  - Navigate to `/dashboard`
  - Should redirect to login page

- [ ] **Step 7**: User can sign out
  - Click logout button
  - Should clear session
  - Navigate to `/dashboard` → redirect to login

- [ ] **Step 8**: No console errors
  - Check browser DevTools console
  - No authentication errors

### Security Checklist

- [ ] **HTTPS in production** (set `secure: true` in cookies)
- [ ] **HTTP-only cookies** enabled (XSS protection)
- [ ] **SameSite cookies** configured (CSRF protection)
- [ ] **Environment variables** NOT committed to git
  - Check `.gitignore` includes `.env.local`
- [ ] **OAuth redirect URIs** match exactly
  - Development: `http://localhost:3000/api/auth/callback`
  - Production: `https://yourdomain.com/api/auth/callback`

---

## Next Steps

### Recommended Enhancements

#### 1. Add Role-Based Access Control (RBAC) (20 min)
- Define roles (admin, editor, viewer)
- Add role field to user model
- Create RBAC middleware
- Protect routes by role

**See**: [Awareness Guide - Workflow 5: Implement RBAC](./awareness-guide.md#workflow-5-implement-rbac)

---

#### 2. Integrate with SAP-041 (Form Validation) (15 min)
- Build custom login/signup forms
- Add validation with React Hook Form + Zod
- Replace provider UI with custom design

**See**: SAP-041 Adoption Blueprint

---

#### 3. Add E2E Tests with SAP-039 (Playwright) (30 min)
- Test login flow
- Test protected routes
- Test logout flow
- Test OAuth redirect flows

**See**: SAP-039 Adoption Blueprint

---

#### 4. Add Magic Link Authentication (15 min)
**Supported by**: Clerk, Supabase Auth, Auth0

**See**: [Awareness Guide - Workflow 7: Add Magic Link Authentication](./awareness-guide.md#workflow-7-add-magic-link-authentication)

---

#### 5. Add Additional OAuth Providers (10 min each)
- Google
- GitHub
- Microsoft
- Apple
- Discord
- Twitter

**See**: [Awareness Guide - Workflow 8: Add OAuth Providers](./awareness-guide.md#workflow-8-add-oauth-providers)

---

#### 6. Configure for Production (30 min)
- Update environment variables for production
- Configure OAuth redirect URIs for production domain
- Enable HTTPS-only cookies
- Set up monitoring and error tracking
- Configure session timeouts

---

### Integration with Other SAPs

**SAP-034** (Database Integration):
- Store user metadata
- Implement database sessions (NextAuth)
- Add Row-Level Security policies (Supabase)

**SAP-035** (API Layer):
- Protect API routes with middleware
- Add bearer token validation
- Implement rate limiting

**SAP-017** (State Management):
- Store auth state in Zustand or Context
- Sync session across components
- Handle optimistic updates

---

## Troubleshooting

### Common Issues

**Issue**: "Cannot find module '@/auth'"
**Solution**: Check file path in imports matches your `auth.ts` location

**Issue**: OAuth redirect URI mismatch
**Solution**: Ensure callback URL in provider dashboard matches exactly:
- NextAuth: `http://localhost:3000/api/auth/callback/google`
- Clerk: Auto-configured
- Supabase: `https://your-project.supabase.co/auth/v1/callback`
- Auth0: `http://localhost:3000/api/auth/callback`

**Issue**: Session not persisting
**Solution**: Check cookie settings - `secure: false` for localhost, `sameSite: "lax"`

**Issue**: CORS errors
**Solution**: Verify `NEXTAUTH_URL` or base URL matches current domain

**Issue**: Email verification not sending (Supabase)
**Solution**: Check Supabase email settings or disable email confirmation for testing

---

## Support Resources

### Documentation

- **NextAuth v5**: https://authjs.dev/
- **Clerk**: https://clerk.com/docs
- **Supabase Auth**: https://supabase.com/docs/guides/auth
- **Auth0**: https://auth0.com/docs

### SAP-033 Documentation

- [Capability Charter](./capability-charter.md) - Problem statement and value
- [Protocol Spec](./protocol-spec.md) - Complete API reference
- [Awareness Guide](./awareness-guide.md) - How-to workflows
- [Ledger](./ledger.md) - Best practices and lessons learned

---

## Feedback

**Help improve SAP-033!**

If you encounter issues or have suggestions:
1. Open issue in chora-base repository
2. Include provider name (NextAuth, Clerk, Supabase, Auth0)
3. Describe issue with steps to reproduce
4. Share feedback on setup time and clarity

**Your feedback makes this SAP better for everyone.**

---

**Congratulations on completing SAP-033 adoption!** You now have production-ready authentication with security best practices baked in.

**Total Setup Time** (by provider):
- NextAuth v5: 30 minutes
- Clerk: 7 minutes (fastest)
- Supabase Auth: 20 minutes
- Auth0: 30 minutes

**Next**: Explore advanced features (RBAC, magic links, OAuth providers) in the [Awareness Guide](./awareness-guide.md).
