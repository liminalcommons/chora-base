# SAP-033: React Authentication & Authorization - Protocol Specification

**SAP ID**: SAP-033
**Name**: react-authentication
**Version**: 1.0.0
**Last Updated**: 2025-11-09
**Diataxis Type**: Reference

---

## Table of Contents

1. [Overview](#overview)
2. [Provider Comparison Matrix](#provider-comparison-matrix)
3. [NextAuth.js v5 (Auth.js)](#nextauthjs-v5-authjs)
4. [Clerk](#clerk)
5. [Supabase Auth](#supabase-auth)
6. [Auth0](#auth0)
7. [Common Authentication Patterns](#common-authentication-patterns)
8. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
9. [Security Specifications](#security-specifications)
10. [TypeScript Types](#typescript-types)
11. [Error Handling](#error-handling)
12. [Testing Specifications](#testing-specifications)

---

## Overview

This protocol specification defines the complete technical implementation for authentication and authorization in React applications using **four major providers**: NextAuth.js v5, Clerk, Supabase Auth, and Auth0.

**Design Principles**:
- **Security First**: OAuth2 PKCE, HTTP-only cookies, server-side validation
- **Type Safety**: Full TypeScript support across all providers
- **Developer Experience**: Clear APIs, minimal configuration, fast setup
- **Production Ready**: Battle-tested patterns used by millions of applications

---

## Provider Comparison Matrix

### Feature Comparison

| Feature | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|---------|-------------|-------|---------------|-------|
| **OAuth Providers** | 50+ | ~20 | ~15 | ~30 |
| **Pre-Built UI** | ❌ No | ✅ YES | ❌ No | ⚠️ Universal Login |
| **Edge Runtime** | ✅ Full | ✅ Full | ⚠️ Limited | ⚠️ Limited |
| **Database Sessions** | ✅ Adapters | ❌ Managed | ✅ Native | ❌ Managed |
| **Magic Links** | ⚠️ DIY | ✅ YES | ✅ YES | ✅ YES |
| **Phone OTP** | ⚠️ DIY | ✅ YES | ✅ YES | ✅ YES |
| **WebAuthn/Passkeys** | ⚠️ DIY | ✅ YES | ✅ YES | ✅ YES |
| **MFA** | ⚠️ DIY | ✅ Built-in | ⚠️ Phone only | ✅ Advanced |
| **SSO/SAML** | ⚠️ DIY | ⚠️ Limited | ❌ No | ✅ YES |
| **Self-Hosted** | ✅ YES | ❌ No | ❌ No | ❌ No |
| **Open Source** | ✅ MIT | ❌ No | ⚠️ Partial | ❌ No |
| **Free Tier** | ✅ Unlimited | 5k MAU | 50k MAU | 7k MAU |
| **Setup Time** | 30 min | **7 min** | 20 min | 30 min |

### API Surface Comparison

| Operation | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|-----------|-------------|-------|---------------|-------|
| **Get Session** | `auth()` | `currentUser()` | `getSession()` | `getSession()` |
| **Sign In** | `signIn(provider)` | `signIn()` | `signIn({email, password})` | `handleLogin()` |
| **Sign Out** | `signOut()` | `signOut()` | `signOut()` | `handleLogout()` |
| **Get User** | `session.user` | `await currentUser()` | `session.user` | `user` |
| **Check Auth** | `!!session` | `!!userId` | `!!session` | `!!user` |
| **Middleware** | `auth` (export) | `clerkMiddleware()` | `createMiddleware()` | `withMiddlewareAuth()` |

---

## NextAuth.js v5 (Auth.js)

### Overview

**NextAuth v5** (rebranded as **Auth.js**) is the most flexible, open-source authentication solution with support for 50+ OAuth providers, edge runtime compatibility, and full database session management.

**Best For**:
- Self-hosted authentication (no vendor lock-in)
- Custom OAuth providers
- Maximum flexibility and extensibility
- Open-source projects

**Documentation**: https://authjs.dev/

---

### Installation

```bash
npm install next-auth@beta
# Beta version required for NextAuth v5 (Auth.js)
```

**Dependencies**:
```json
{
  "dependencies": {
    "next-auth": "^5.0.0-beta.25",
    "@auth/core": "^0.35.0"
  }
}
```

---

### Core Configuration

#### 1. Create `auth.ts` (Root Configuration)

```typescript
// auth.ts (project root)
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";
import bcrypt from "bcryptjs";
import { z } from "zod";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),

  session: {
    strategy: "jwt", // or "database" for database sessions
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },

  providers: [
    // 1. Google OAuth Provider
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

    // 2. GitHub OAuth Provider
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    }),

    // 3. Credentials Provider (email/password)
    Credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        // Validate input
        const parsedCredentials = z
          .object({
            email: z.string().email(),
            password: z.string().min(6)
          })
          .safeParse(credentials);

        if (!parsedCredentials.success) {
          return null;
        }

        const { email, password } = parsedCredentials.data;

        // Query user from database
        const user = await prisma.user.findUnique({
          where: { email }
        });

        if (!user || !user.hashedPassword) {
          return null;
        }

        // Verify password
        const passwordMatch = await bcrypt.compare(
          password,
          user.hashedPassword
        );

        if (!passwordMatch) {
          return null;
        }

        // Return user object (stored in session)
        return {
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.image
        };
      }
    })
  ],

  callbacks: {
    // JWT callback: Add custom fields to JWT
    async jwt({ token, user, account }) {
      if (user) {
        token.userId = user.id;
        token.role = user.role; // Custom field
      }
      return token;
    },

    // Session callback: Add custom fields to session
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
    error: '/error',
    verifyRequest: '/verify-request',
    newUser: '/welcome'
  },

  // Security settings
  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true,  // ✅ XSS protection
        sameSite: "lax", // ✅ CSRF protection
        path: "/",
        secure: process.env.NODE_ENV === "production" // HTTPS only in prod
      }
    }
  }
});
```

---

#### 2. API Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

---

#### 3. Middleware (Route Protection)

```typescript
// middleware.ts (project root)
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // Public routes (no auth required)
  const publicRoutes = ["/", "/login", "/signup", "/api/auth"];
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
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

### Usage Patterns

#### 1. Server Components (Session Access)

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  // Server-side authentication check
  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

---

#### 2. Client Components (Sign In/Out)

```typescript
// components/auth/LoginButton.tsx
"use client";

import { signIn, signOut } from "next-auth/react";

export function LoginButton() {
  return (
    <button onClick={() => signIn("google")}>
      Sign in with Google
    </button>
  );
}

export function LogoutButton() {
  return (
    <button onClick={() => signOut({ callbackUrl: "/" })}>
      Sign out
    </button>
  );
}
```

---

#### 3. Login Form (Credentials)

```typescript
// app/login/page.tsx
"use client";

import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const result = await signIn("credentials", {
      email: formData.get("email") as string,
      password: formData.get("password") as string,
      redirect: false
    });

    if (result?.error) {
      setError("Invalid credentials");
    } else {
      router.push("/dashboard");
      router.refresh(); // Refresh server components
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      {error && <p>{error}</p>}
      <button type="submit">Sign in</button>
    </form>
  );
}
```

---

#### 4. API Route Protection

```typescript
// app/api/users/route.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await auth();

  if (!session) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  // Protected API logic
  return NextResponse.json({
    user: session.user
  });
}
```

---

### Database Adapter Setup (Prisma)

#### Prisma Schema

```prisma
// prisma/schema.prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  hashedPassword String? // For credentials provider
  role          String    @default("user") // Custom field
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

---

### Environment Variables

```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-generate-with-openssl

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

**Generate Secret**:
```bash
openssl rand -base64 32
```

---

### Advantages

✅ **50+ OAuth providers** (most comprehensive)
✅ **Self-hosted** (no vendor lock-in, MIT license)
✅ **Edge runtime compatible** (Vercel Edge, Cloudflare Workers)
✅ **Database adapters** (Prisma, Drizzle, TypeORM)
✅ **Free** (unlimited usage)
✅ **Custom providers** (internal OAuth servers)

### Disadvantages

⚠️ **Custom UI required** (no pre-built components)
⚠️ **30-minute setup** (configuration overhead)
⚠️ **DIY enterprise features** (SSO/SAML requires custom implementation)

---

## Clerk

### Overview

**Clerk** is a complete authentication and user management platform with pre-built UI components, 7-minute setup time, and beautiful UX out of the box.

**Best For**:
- Rapid prototyping (MVP, startup)
- Pre-built UI requirements
- Organization/team management
- Beautiful user experience

**Documentation**: https://clerk.com/docs

---

### Installation

```bash
npm install @clerk/nextjs
```

**Dependencies**:
```json
{
  "dependencies": {
    "@clerk/nextjs": "^6.0.0"
  }
}
```

---

### Core Configuration

#### 1. Environment Variables

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Redirect URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_URL=/dashboard
NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_URL=/onboarding
```

---

#### 2. Root Layout Wrapper

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

#### 3. Middleware (Route Protection)

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhook(.*)'
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
```

---

### Usage Patterns

#### 1. Pre-Built Sign-In Page

```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <SignIn
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-lg'
          }
        }}
      />
    </div>
  );
}
```

---

#### 2. Pre-Built Sign-Up Page

```typescript
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <SignUp
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-lg'
          }
        }}
      />
    </div>
  );
}
```

---

#### 3. User Button (Profile Dropdown)

```typescript
// components/Header.tsx
import { UserButton } from '@clerk/nextjs';

export function Header() {
  return (
    <header>
      <nav>
        <UserButton
          afterSignOutUrl="/"
          appearance={{
            elements: {
              avatarBox: 'w-10 h-10'
            }
          }}
        />
      </nav>
    </header>
  );
}
```

---

#### 4. Server Components (Session Access)

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
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.firstName}!</p>
      <p>Email: {user?.emailAddresses[0]?.emailAddress}</p>
    </div>
  );
}
```

---

#### 5. Client Components (Auth State)

```typescript
// components/WelcomeMessage.tsx
"use client";

import { useUser } from '@clerk/nextjs';

export function WelcomeMessage() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <div>Please sign in</div>;
  }

  return <div>Welcome, {user.firstName}!</div>;
}
```

---

#### 6. API Route Protection

```typescript
// app/api/users/route.ts
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  return NextResponse.json({
    userId,
    message: 'Protected data'
  });
}
```

---

### Organization Management

```typescript
// app/organizations/page.tsx
import { OrganizationSwitcher, OrganizationProfile } from '@clerk/nextjs';

export default function OrganizationsPage() {
  return (
    <div>
      {/* Dropdown to switch between organizations */}
      <OrganizationSwitcher
        appearance={{
          elements: {
            rootBox: 'flex items-center'
          }
        }}
      />

      {/* Full organization management UI */}
      <OrganizationProfile
        appearance={{
          elements: {
            rootBox: 'w-full max-w-4xl mx-auto'
          }
        }}
      />
    </div>
  );
}
```

---

### Webhooks (User Events)

```typescript
// app/api/webhooks/clerk/route.ts
import { headers } from 'next/headers';
import { Webhook } from 'svix';
import { WebhookEvent } from '@clerk/nextjs/server';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    throw new Error('Please add WEBHOOK_SECRET to .env');
  }

  // Get headers
  const headerPayload = await headers();
  const svix_id = headerPayload.get('svix-id');
  const svix_timestamp = headerPayload.get('svix-timestamp');
  const svix_signature = headerPayload.get('svix-signature');

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Error: Missing svix headers', { status: 400 });
  }

  // Get body
  const payload = await req.json();
  const body = JSON.stringify(payload);

  // Create Svix instance
  const wh = new Webhook(WEBHOOK_SECRET);

  let evt: WebhookEvent;

  // Verify webhook
  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    console.error('Error verifying webhook:', err);
    return new Response('Error: Verification failed', { status: 400 });
  }

  // Handle events
  const eventType = evt.type;

  if (eventType === 'user.created') {
    const { id, email_addresses, first_name, last_name } = evt.data;
    console.log('User created:', { id, email: email_addresses[0]?.email_address });
  }

  if (eventType === 'user.updated') {
    const { id } = evt.data;
    console.log('User updated:', id);
  }

  return new Response('Webhook received', { status: 200 });
}
```

---

### Advantages

✅ **7-minute setup** (fastest time to production)
✅ **Pre-built UI components** (`<SignIn>`, `<SignUp>`, `<UserButton>`)
✅ **Organization/team management** (built-in multi-tenancy)
✅ **SOC2 Type II certified** (enterprise security)
✅ **Beautiful UX** (customizable branding, dark mode)
✅ **Webhooks** (user.created, session.created events)

### Disadvantages

⚠️ **SaaS only** (vendor dependency, no self-hosting)
⚠️ **Paid tiers** (free tier limited to 5k MAU)
⚠️ **Less OAuth providers** (~20 vs NextAuth's 50+)

---

## Supabase Auth

### Overview

**Supabase Auth** is a complete authentication system with tight integration to Supabase's PostgreSQL database, Row-Level Security (RLS), and real-time capabilities.

**Best For**:
- Supabase projects
- Row-Level Security (RLS) requirements
- Magic link authentication
- Real-time auth state changes

**Documentation**: https://supabase.com/docs/guides/auth

---

### Installation

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Dependencies**:
```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.45.0",
    "@supabase/ssr": "^0.5.0"
  }
}
```

---

### Core Configuration

#### 1. Supabase Client (Server)

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

---

#### 2. Supabase Client (Client)

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

#### 3. Middleware (Session Refresh)

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: any) {
          request.cookies.set({
            name,
            value,
            ...options,
          });
          supabaseResponse = NextResponse.next({
            request,
          });
          supabaseResponse.cookies.set({
            name,
            value,
            ...options,
          });
        },
        remove(name: string, options: any) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          });
          supabaseResponse = NextResponse.next({
            request,
          });
          supabaseResponse.cookies.set({
            name,
            value: '',
            ...options,
          });
        },
      },
    }
  );

  // Refresh session if expired
  const {
    data: { session },
  } = await supabase.auth.getSession();

  // Protected routes
  const protectedRoutes = ['/dashboard', '/profile', '/settings'];
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  if (isProtectedRoute && !session) {
    const redirectUrl = new URL('/login', request.url);
    redirectUrl.searchParams.set('redirectTo', request.nextUrl.pathname);
    return NextResponse.redirect(redirectUrl);
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

### Usage Patterns

#### 1. Sign Up (Email/Password)

```typescript
// app/signup/page.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function SignUpPage() {
  const router = useRouter();
  const supabase = createClient();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const { data, error } = await supabase.auth.signUp({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
        data: {
          first_name: formData.get('firstName') as string,
          last_name: formData.get('lastName') as string,
        }
      }
    });

    if (error) {
      setError(error.message);
    } else {
      router.push('/verify-email');
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="firstName" placeholder="First name" required />
      <input name="lastName" placeholder="Last name" required />
      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit">Sign up</button>
    </form>
  );
}
```

---

#### 2. Sign In (Email/Password)

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

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const { data, error } = await supabase.auth.signInWithPassword({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });

    if (error) {
      setError(error.message);
    } else {
      router.push('/dashboard');
      router.refresh();
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit">Sign in</button>
    </form>
  );
}
```

---

#### 3. Magic Link Authentication

```typescript
// app/login/magic-link/page.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useState } from 'react';

export default function MagicLinkPage() {
  const supabase = createClient();
  const [sent, setSent] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const { error } = await supabase.auth.signInWithOtp({
      email: formData.get('email') as string,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      }
    });

    if (!error) {
      setSent(true);
    }
  }

  if (sent) {
    return <div>Check your email for the magic link!</div>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit">Send magic link</button>
    </form>
  );
}
```

---

#### 4. Phone OTP Authentication

```typescript
// app/login/phone/page.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useState } from 'react';

export default function PhoneLoginPage() {
  const supabase = createClient();
  const [step, setStep] = useState<'phone' | 'otp'>('phone');
  const [phone, setPhone] = useState('');

  async function sendOTP(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const phoneNumber = formData.get('phone') as string;

    const { error } = await supabase.auth.signInWithOtp({
      phone: phoneNumber,
    });

    if (!error) {
      setPhone(phoneNumber);
      setStep('otp');
    }
  }

  async function verifyOTP(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const { error } = await supabase.auth.verifyOtp({
      phone,
      token: formData.get('otp') as string,
      type: 'sms',
    });

    if (!error) {
      window.location.href = '/dashboard';
    }
  }

  if (step === 'otp') {
    return (
      <form onSubmit={verifyOTP}>
        <p>Enter the code sent to {phone}</p>
        <input name="otp" placeholder="123456" required />
        <button type="submit">Verify</button>
      </form>
    );
  }

  return (
    <form onSubmit={sendOTP}>
      <input name="phone" type="tel" placeholder="+1234567890" required />
      <button type="submit">Send OTP</button>
    </form>
  );
}
```

---

#### 5. OAuth Providers (Google)

```typescript
// components/GoogleSignIn.tsx
"use client";

import { createClient } from '@/lib/supabase/client';

export function GoogleSignIn() {
  const supabase = createClient();

  async function signInWithGoogle() {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        },
      },
    });

    if (error) {
      console.error('Error signing in with Google:', error);
    }
  }

  return (
    <button onClick={signInWithGoogle}>
      Sign in with Google
    </button>
  );
}
```

---

#### 6. Server Components (Session Access)

```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const supabase = await createClient();

  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    redirect('/login');
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.email}!</p>
    </div>
  );
}
```

---

#### 7. Row-Level Security (RLS) Policies

```sql
-- Enable RLS on todos table
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own todos
CREATE POLICY "Users can view own todos"
ON todos
FOR SELECT
USING (auth.uid() = user_id);

-- Policy: Users can insert their own todos
CREATE POLICY "Users can insert own todos"
ON todos
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own todos
CREATE POLICY "Users can update own todos"
ON todos
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can delete their own todos
CREATE POLICY "Users can delete own todos"
ON todos
FOR DELETE
USING (auth.uid() = user_id);
```

---

#### 8. Real-Time Auth State Changes

```typescript
// components/AuthListener.tsx
"use client";

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function AuthListener() {
  const router = useRouter();
  const supabase = createClient();

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN') {
        console.log('User signed in:', session?.user.email);
        router.push('/dashboard');
      }

      if (event === 'SIGNED_OUT') {
        console.log('User signed out');
        router.push('/login');
      }

      if (event === 'TOKEN_REFRESHED') {
        console.log('Token refreshed');
      }

      if (event === 'USER_UPDATED') {
        console.log('User updated');
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, [supabase, router]);

  return null;
}
```

---

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

### Advantages

✅ **Tight Supabase integration** (automatic RLS with `auth.uid()`)
✅ **Magic links** (passwordless email authentication)
✅ **Phone OTP** (SMS-based authentication)
✅ **Real-time auth state** (WebSocket-based session changes)
✅ **Social providers** (Google, GitHub, Azure, etc.)
✅ **Free tier** (50k MAU)

### Disadvantages

⚠️ **Supabase coupling** (requires Supabase database)
⚠️ **Custom UI required** (no pre-built components)
⚠️ **Limited edge runtime** (relies on Supabase infrastructure)

---

## Auth0

### Overview

**Auth0** is an enterprise-grade authentication and authorization platform with 11,000+ customers, 99.99% uptime SLA, and advanced SSO/SAML capabilities.

**Best For**:
- Enterprise B2B applications
- SSO/SAML requirements
- Compliance (SOC2, HIPAA, GDPR)
- Advanced MFA (SMS, authenticator apps, biometrics)

**Documentation**: https://auth0.com/docs

---

### Installation

```bash
npm install @auth0/nextjs-auth0
```

**Dependencies**:
```json
{
  "dependencies": {
    "@auth0/nextjs-auth0": "^3.5.0"
  }
}
```

---

### Core Configuration

#### 1. Environment Variables

```bash
# .env.local
AUTH0_SECRET=your-auth0-secret-generate-with-openssl
AUTH0_BASE_URL=http://localhost:3000
AUTH0_ISSUER_BASE_URL=https://your-tenant.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
```

**Generate Secret**:
```bash
openssl rand -hex 32
```

---

#### 2. API Route Handler

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth } from '@auth0/nextjs-auth0';

export const GET = handleAuth();
```

---

#### 3. Middleware (Route Protection)

```typescript
// middleware.ts
import { withMiddlewareAuthRequired } from '@auth0/nextjs-auth0/edge';

export default withMiddlewareAuthRequired();

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/settings/:path*'],
};
```

---

### Usage Patterns

#### 1. Server Components (Session Access)

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
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

---

#### 2. Client Components (Auth State)

```typescript
// components/UserProfile.tsx
"use client";

import { useUser } from '@auth0/nextjs-auth0/client';

export function UserProfile() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>Not logged in</div>;

  return (
    <div>
      <img src={user.picture} alt={user.name} />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

---

#### 3. Login/Logout Buttons

```typescript
// components/AuthButtons.tsx
export function LoginButton() {
  return (
    <a href="/api/auth/login">
      <button>Log in</button>
    </a>
  );
}

export function LogoutButton() {
  return (
    <a href="/api/auth/logout">
      <button>Log out</button>
    </a>
  );
}
```

---

#### 4. API Route Protection

```typescript
// app/api/users/route.ts
import { getSession } from '@auth0/nextjs-auth0';
import { NextResponse } from 'next/server';

export async function GET() {
  const session = await getSession();

  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  return NextResponse.json({
    user: session.user,
    message: 'Protected data'
  });
}
```

---

#### 5. SSO/SAML Configuration

```typescript
// lib/auth0-config.ts
export const auth0Config = {
  authorizationParams: {
    connection: 'google-oauth2', // or 'samlp' for SAML
    prompt: 'login',
    scope: 'openid profile email',
  },
};

// Usage in login redirect
// /api/auth/login?connection=samlp&organization=org_abc123
```

---

#### 6. Organization-Based Access

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth, handleLogin } from '@auth0/nextjs-auth0';

export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      organization: process.env.AUTH0_ORGANIZATION,
    },
  }),
});

// Access organization in session
const session = await getSession();
const orgId = session?.user.org_id;
```

---

#### 7. MFA Configuration

```typescript
// Enforce MFA (configured in Auth0 dashboard)
// Rules > New Rule > Multifactor Authentication

function (user, context, callback) {
  if (context.protocol === 'redirect-callback') {
    return callback(null, user, context);
  }

  const requireMFA = context.request.query.requireMFA === 'true';

  if (requireMFA) {
    context.multifactor = {
      provider: 'any',
      allowRememberBrowser: false
    };
  }

  callback(null, user, context);
}
```

---

### Advanced: Role-Based Access Control (RBAC)

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth, handleLogin } from '@auth0/nextjs-auth0';
import { NextRequest } from 'next/server';

export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      scope: 'openid profile email read:users',
    },
  }),
  onError(req: NextRequest, error: any) {
    console.error('Auth0 error:', error);
  },
});

// Check roles in session
const session = await getSession();
const roles = session?.user['https://your-app.com/roles'] || [];
const isAdmin = roles.includes('admin');
```

---

### Environment Variables (Complete)

```bash
# .env.local

# Required
AUTH0_SECRET=your-auth0-secret
AUTH0_BASE_URL=http://localhost:3000
AUTH0_ISSUER_BASE_URL=https://your-tenant.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret

# Optional (Organization)
AUTH0_ORGANIZATION=org_abc123

# Optional (Custom Claims)
AUTH0_SCOPE=openid profile email read:users

# Optional (Session)
AUTH0_SESSION_COOKIE_LIFETIME=604800 # 7 days in seconds
AUTH0_SESSION_ROLLING=true
AUTH0_SESSION_ABSOLUTE_DURATION=2592000 # 30 days
```

---

### Advantages

✅ **Enterprise SSO/SAML** (Okta, Azure AD, Google Workspace)
✅ **11k+ enterprise customers** (proven at scale)
✅ **7M+ developers worldwide**
✅ **99.99% uptime SLA** (enterprise-grade reliability)
✅ **Universal Login** (hosted login pages, customizable)
✅ **Advanced MFA** (SMS, authenticator apps, biometrics)

### Disadvantages

⚠️ **Expensive** (enterprise pricing, free tier limited)
⚠️ **SaaS only** (no self-hosting option)
⚠️ **Configuration complexity** (enterprise features require setup)

---

## Common Authentication Patterns

### Pattern 1: Protected Routes (Middleware)

All providers support middleware-based route protection. See provider-specific sections above for implementation details.

**Key Principle**: Always validate sessions server-side (never trust client-side state).

---

### Pattern 2: Session Refresh

#### NextAuth v5
```typescript
// Automatic JWT refresh (configured in auth.ts)
session: {
  strategy: "jwt",
  maxAge: 30 * 24 * 60 * 60, // 30 days
  updateAge: 24 * 60 * 60     // 24 hours (refresh interval)
}
```

#### Clerk
```typescript
// Automatic session refresh (managed by Clerk)
// No configuration needed
```

#### Supabase Auth
```typescript
// Automatic refresh in middleware (see Supabase middleware section)
await supabase.auth.getSession(); // Triggers refresh if expired
```

#### Auth0
```typescript
// Automatic refresh (configured in .env)
AUTH0_SESSION_ROLLING=true
AUTH0_SESSION_ABSOLUTE_DURATION=2592000 # 30 days
```

---

### Pattern 3: Logout (Client + Server)

#### NextAuth v5
```typescript
import { signOut } from "next-auth/react";

// Client-side logout
await signOut({ callbackUrl: "/" });
```

#### Clerk
```typescript
import { useClerk } from "@clerk/nextjs";

const { signOut } = useClerk();

// Client-side logout
await signOut({ redirectUrl: "/" });
```

#### Supabase Auth
```typescript
import { createClient } from '@/lib/supabase/client';

const supabase = createClient();

// Client-side logout
await supabase.auth.signOut();
```

#### Auth0
```typescript
// Navigate to logout endpoint
window.location.href = "/api/auth/logout";
```

---

### Pattern 4: Email Verification

#### NextAuth v5
```typescript
// Configure email provider in auth.ts
import { EmailProvider } from "next-auth/providers/email";

providers: [
  EmailProvider({
    server: process.env.EMAIL_SERVER,
    from: process.env.EMAIL_FROM
  })
]
```

#### Clerk
```typescript
// Email verification automatic (pre-built UI)
// Configured in Clerk dashboard
```

#### Supabase Auth
```typescript
// Email confirmation required by default
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password',
  options: {
    emailRedirectTo: `${window.location.origin}/auth/callback`,
  }
});
```

#### Auth0
```typescript
// Email verification automatic (Universal Login)
// Configured in Auth0 dashboard
```

---

### Pattern 5: Password Reset

#### NextAuth v5 (Credentials)
```typescript
// Custom implementation required
// 1. Generate reset token
// 2. Send email with reset link
// 3. Validate token and update password
```

#### Clerk
```typescript
// Pre-built UI (no code needed)
// Handled automatically by Clerk
```

#### Supabase Auth
```typescript
// Send reset email
const { error } = await supabase.auth.resetPasswordForEmail(
  'user@example.com',
  {
    redirectTo: `${window.location.origin}/reset-password`,
  }
);

// Update password (after clicking link)
const { error } = await supabase.auth.updateUser({
  password: 'new-password'
});
```

#### Auth0
```typescript
// Handled by Universal Login (no code needed)
// User clicks "Forgot password?" on login page
```

---

## Role-Based Access Control (RBAC)

### TypeScript Role Definitions

```typescript
// types/auth.ts
export const ROLES = {
  ADMIN: 'admin',
  EDITOR: 'editor',
  VIEWER: 'viewer',
} as const;

export type Role = typeof ROLES[keyof typeof ROLES];

export interface UserWithRole {
  id: string;
  email: string;
  name: string;
  role: Role;
}

// Permission matrix
export const PERMISSIONS = {
  [ROLES.ADMIN]: ['read', 'write', 'delete', 'manage_users'],
  [ROLES.EDITOR]: ['read', 'write'],
  [ROLES.VIEWER]: ['read'],
} as const;

export function hasPermission(role: Role, permission: string): boolean {
  return PERMISSIONS[role]?.includes(permission as any) || false;
}
```

---

### RBAC Middleware (Next.js)

```typescript
// middleware.ts
import { auth } from "@/auth"; // NextAuth v5 example
import { NextResponse } from "next/server";
import { ROLES } from "@/types/auth";

export default auth((req) => {
  const session = req.auth;
  const { pathname } = req.nextUrl;

  // Admin-only routes
  if (pathname.startsWith('/admin')) {
    if (session?.user?.role !== ROLES.ADMIN) {
      return NextResponse.redirect(new URL('/unauthorized', req.url));
    }
  }

  // Editor+ routes
  if (pathname.startsWith('/editor')) {
    const allowedRoles = [ROLES.ADMIN, ROLES.EDITOR];
    if (!session || !allowedRoles.includes(session.user.role as Role)) {
      return NextResponse.redirect(new URL('/unauthorized', req.url));
    }
  }

  return NextResponse.next();
});
```

---

### RBAC Server Component

```typescript
// app/admin/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { ROLES } from "@/types/auth";

export default async function AdminPage() {
  const session = await auth();

  if (!session || session.user.role !== ROLES.ADMIN) {
    redirect('/unauthorized');
  }

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Only visible to admins</p>
    </div>
  );
}
```

---

### RBAC Client Component (Permission Check)

```typescript
// components/ProtectedAction.tsx
"use client";

import { useSession } from "next-auth/react"; // NextAuth example
import { hasPermission } from "@/types/auth";

interface ProtectedActionProps {
  permission: string;
  children: React.ReactNode;
}

export function ProtectedAction({ permission, children }: ProtectedActionProps) {
  const { data: session } = useSession();

  if (!session || !hasPermission(session.user.role, permission)) {
    return null;
  }

  return <>{children}</>;
}

// Usage
<ProtectedAction permission="delete">
  <button onClick={handleDelete}>Delete</button>
</ProtectedAction>
```

---

## Security Specifications

### 1. OAuth2 PKCE Enforcement

**All providers enforce PKCE by default** (Proof Key for Code Exchange, RFC 7636).

**What is PKCE?**
- Protection against authorization code interception attacks
- Client generates `code_verifier` (random string)
- Sends `code_challenge` (SHA256 hash) during authorization
- Sends `code_verifier` during token exchange (server verifies hash)

**Implementation** (automatic in all providers):
- NextAuth v5: Automatic (no configuration)
- Clerk: Automatic (no configuration)
- Supabase Auth: Automatic (no configuration)
- Auth0: Automatic (no configuration)

---

### 2. HTTP-Only Cookies

**All providers use HTTP-only cookies by default** (XSS protection).

```typescript
// ✅ CORRECT: HTTP-only cookies (automatic)
cookies: {
  sessionToken: {
    options: {
      httpOnly: true,  // JavaScript cannot access
      sameSite: "lax", // CSRF protection
      secure: true     // HTTPS-only
    }
  }
}

// ❌ WRONG: localStorage (vulnerable to XSS)
localStorage.setItem('token', accessToken); // DON'T DO THIS
```

---

### 3. CSRF Protection

**SameSite cookies** (automatic CSRF protection):

```typescript
cookies: {
  sessionToken: {
    options: {
      sameSite: "lax" // or "strict"
    }
  }
}
```

**Options**:
- `strict`: Never sent with cross-site requests (most secure, may break OAuth redirects)
- `lax`: Sent with top-level navigation (recommended, balances security and UX)
- `none`: Always sent (requires `secure: true`, used for cross-site APIs)

---

### 4. Session Validation (Server-Side)

**NEVER trust client-side session state**:

```typescript
// ✅ CORRECT: Server-side validation
const session = await auth(); // NextAuth v5
if (!session) {
  redirect('/login');
}

// ❌ WRONG: Client-side trust
if (localStorage.getItem('isLoggedIn') === 'true') {
  // DON'T DO THIS (user can manipulate localStorage)
}
```

---

### 5. Security Headers (Next.js)

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' https://*.supabase.co;
    `.replace(/\s{2,}/g, ' ').trim()
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## TypeScript Types

### NextAuth v5

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

### Clerk

```typescript
// types/clerk.d.ts
export interface ClerkUser {
  id: string;
  firstName: string | null;
  lastName: string | null;
  emailAddresses: Array<{
    emailAddress: string;
    id: string;
  }>;
  publicMetadata: {
    role?: string;
  };
}
```

---

### Supabase Auth

```typescript
// types/supabase.d.ts
import { Database } from './database.types';

export interface SupabaseUser {
  id: string;
  email: string;
  user_metadata: {
    first_name?: string;
    last_name?: string;
    avatar_url?: string;
  };
  app_metadata: {
    provider?: string;
    role?: string;
  };
}
```

---

### Auth0

```typescript
// types/auth0.d.ts
export interface Auth0User {
  sub: string;
  name: string;
  email: string;
  email_verified: boolean;
  picture: string;
  'https://your-app.com/roles': string[];
  org_id?: string;
}
```

---

## Error Handling

### NextAuth v5

```typescript
// app/error.tsx
"use client";

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('NextAuth error:', error);
  }, [error]);

  return (
    <div>
      <h2>Authentication Error</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

---

### Clerk

```typescript
// components/ClerkErrorBoundary.tsx
"use client";

import { ClerkProvider } from "@clerk/nextjs";
import { useRouter } from "next/navigation";

export function ClerkWrapper({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
      navigate={(to) => router.push(to)}
    >
      {children}
    </ClerkProvider>
  );
}
```

---

### Supabase Auth

```typescript
// lib/supabase/error-handler.ts
export function handleSupabaseError(error: any) {
  if (error.message === 'Invalid login credentials') {
    return 'Incorrect email or password';
  }
  if (error.message === 'User already registered') {
    return 'Email already in use';
  }
  if (error.message === 'Email not confirmed') {
    return 'Please confirm your email';
  }
  return error.message || 'An error occurred';
}
```

---

### Auth0

```typescript
// lib/auth0/error-handler.ts
export function handleAuth0Error(error: any) {
  if (error.code === 'invalid_grant') {
    return 'Invalid credentials';
  }
  if (error.code === 'unauthorized') {
    return 'Access denied';
  }
  if (error.code === 'too_many_attempts') {
    return 'Too many login attempts. Try again later.';
  }
  return error.message || 'Authentication error';
}
```

---

## Testing Specifications

### E2E Testing (Playwright)

```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should sign in with credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('should sign out', async ({ page }) => {
    // Sign in first
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Sign out
    await page.click('button:has-text("Sign out")');
    await expect(page).toHaveURL('/');
  });

  test('should protect routes', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});
```

---

## Version History

**1.0.0** (2025-11-09) - Initial release
- Complete protocol specifications for 4 providers (NextAuth v5, Clerk, Supabase Auth, Auth0)
- Common authentication patterns (protected routes, session refresh, logout)
- RBAC patterns with TypeScript
- Security specifications (OAuth2 PKCE, HTTP-only cookies, CSRF protection)
- TypeScript types for all providers
- Error handling patterns
- E2E testing specifications

---

## Related Documentation

- [Capability Charter](./capability-charter.md) - Problem statement and business value
- [Awareness Guide](./awareness-guide.md) - How-to workflows for agents
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step setup tutorials
- [Ledger](./ledger.md) - Adoption tracking and best practices

---

**Next Steps**:
1. Select provider using [decision matrix](#provider-comparison-matrix)
2. Read provider-specific section for API reference
3. Navigate to [Adoption Blueprint](./adoption-blueprint.md) for setup tutorial
4. Implement RBAC using [RBAC patterns](#role-based-access-control-rbac)
5. Add E2E tests using [testing specifications](#testing-specifications)
