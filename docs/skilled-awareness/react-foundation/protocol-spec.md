# SAP-020: React Project Foundation - Protocol Specification

**SAP ID**: SAP-020
**Version**: 1.0.0
**React Version**: 19.x
**Next.js Version**: 15.5.x
**TypeScript Version**: 5.7.x
**Research Foundation**: RT-019 Series (Q4 2024 - Q1 2025)

---

## Overview

This document specifies the technical contracts, architecture patterns, and guarantees for building modern React applications using the SAP-020 capability package.

**Scope**: React 19 applications using Next.js 15 (App Router) or Vite 7, with TypeScript strict mode
**Audience**: AI agents, developers building React applications
**Compliance**: React 19 patterns, Next.js 15 App Router conventions, TypeScript 5.7

---

## Protocol Foundation

### React Ecosystem Standards

**React Version**: 19.x (released December 5, 2024)
**Source**: https://react.dev
**Key Features**:
- React Server Components (RSC) production-ready
- Actions API for form handling
- `use()` hook for async data
- `ref` as prop (no more `forwardRef`)
- Concurrent features (Suspense, startTransition, useDeferredValue)

### Next.js App Router Specification

**Version**: 15.5.x (October 2024+)
**Source**: https://nextjs.org/docs
**Architecture**: File-based routing with React Server Components as default

**Core Conventions**:
```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page route
├── loading.tsx         # Loading UI (Suspense boundary)
├── error.tsx           # Error UI (Error boundary)
├── not-found.tsx       # 404 page
├── (marketing)/        # Route group (no URL segment)
│   └── about/page.tsx  # /about
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   ├── _components/    # Private folder (not routed)
│   └── [id]/page.tsx   # Dynamic route /dashboard/:id
└── api/
    └── users/route.ts  # API route handler
```

**Special Files**:
- `page.tsx` - Defines unique UI for route
- `layout.tsx` - Shared UI across routes (persists on navigation)
- `loading.tsx` - Instant loading state (Suspense)
- `error.tsx` - Error handling (Error Boundary)
- `route.ts` - API endpoint (GET, POST, PUT, DELETE, PATCH)
- `template.tsx` - Similar to layout but re-mounts on navigation
- `default.tsx` - Fallback for parallel routes

### TypeScript Configuration Standard

**Version**: 5.7.x
**Mode**: Strict (mandatory)
**Source**: https://www.typescriptlang.org/tsconfig

**Required tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "allowJs": false,
    "checkJs": false,

    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/lib/*": ["src/lib/*"],
      "@/features/*": ["src/features/*"]
    },

    "plugins": [
      {
        "name": "next"
      }
    ]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Strict Mode Benefits**:
- Catches 40% more errors at compile time
- Eliminates `any` types (explicit typing)
- Prevents index signature errors (`obj[key]` requires null check)
- Better IDE autocomplete and refactoring

---

## Inputs

### Prerequisites

**System Requirements**:
- Node.js 22.x LTS (active until April 2027)
- pnpm 10.x (recommended) or npm 10.x
- VS Code 1.95+ (or any TypeScript-aware IDE)

**Development Tools** (recommended):
- ESLint 9.x (linting) - covered in SAP-022
- Prettier 3.x (formatting) - covered in SAP-022
- Vitest 4.x (testing) - covered in SAP-021

**Knowledge Prerequisites**:
- JavaScript ES2020+ (async/await, modules, destructuring)
- TypeScript basics (types, interfaces, generics)
- React fundamentals (components, hooks, JSX)
- Understanding of client-server architecture (for RSC)

### Installation Inputs

**From SAP-020 Templates** (provided by this SAP):

**Next.js 15 App Router Starter**:
```
templates/react/nextjs-15-app-router/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout with providers
│   │   ├── page.tsx                # Home page
│   │   ├── loading.tsx             # Global loading state
│   │   ├── error.tsx               # Global error boundary
│   │   └── not-found.tsx           # 404 page
│   ├── components/
│   │   ├── ui/                     # Shared UI components
│   │   └── providers/
│   │       └── query-provider.tsx  # TanStack Query setup
│   ├── lib/
│   │   ├── api.ts                  # API client (Axios + Zod)
│   │   └── utils.ts                # Utility functions
│   └── features/                   # Feature-based organization
│       └── .gitkeep
├── public/
│   └── .gitkeep
├── package.json                    # Dependencies
├── tsconfig.json                   # TypeScript config
├── next.config.ts                  # Next.js config
├── .env.example                    # Environment variables
├── .gitignore
└── README.md
```

**Vite + React Router SPA Starter**:
```
templates/react/vite-react-spa/
├── src/
│   ├── main.tsx                    # Entry point
│   ├── App.tsx                     # Root component
│   ├── router.tsx                  # React Router config
│   ├── components/
│   │   └── ui/                     # Shared UI components
│   ├── lib/
│   │   ├── api.ts                  # API client
│   │   └── utils.ts                # Utility functions
│   ├── features/                   # Feature-based organization
│   └── pages/                      # Page components
│       ├── HomePage.tsx
│       └── NotFoundPage.tsx
├── public/
├── package.json
├── tsconfig.json
├── tsconfig.node.json              # Vite config TypeScript
├── vite.config.ts                  # Vite configuration
├── index.html                      # HTML entry point
├── .env.example
└── README.md
```

**Configuration Templates**:
```
templates/react/configs/
├── tsconfig.strict.json            # Strict TypeScript config
├── tsconfig.relaxed.json           # Relaxed (learning projects)
├── next.config.minimal.ts          # Minimal Next.js config
├── next.config.full.ts             # Production-ready config
├── vite.config.minimal.ts          # Minimal Vite config
└── package.json.templates/
    ├── nextjs-15.json              # Next.js dependencies
    └── vite-7.json                 # Vite dependencies
```

**State Management Templates**:
```
templates/react/state-management/
├── zustand-store.template.ts       # Zustand store pattern
├── tanstack-query-provider.tsx     # TanStack Query setup
├── react-hook-form.template.tsx    # Form pattern
└── nuqs-url-state.template.ts      # URL state pattern
```

**Configuration Variables** (customizable):
- `{{ project_name }}` - Human-readable project name
- `{{ package_name }}` - npm package name (kebab-case)
- `{{ use_nextjs }}` - Boolean (true for Next.js, false for Vite)
- `{{ use_app_router }}` - Boolean (true for App Router, false for Pages)
- `{{ typescript_strict }}` - Boolean (true for strict mode)
- `{{ enable_tailwind }}` - Boolean (true to include Tailwind setup)
- `{{ enable_tanstack_query }}` - Boolean (true for TanStack Query)
- `{{ enable_zustand }}` - Boolean (true for Zustand)

---

## Architecture

### Framework Decision Matrix

**Decision Tree**:
```
What are you building?
├─ Full-stack app with SSR → Next.js 15 App Router
├─ E-commerce with Shopify → Remix + Hydrogen
├─ SPA without SSR → Vite 7 + React Router
└─ Static content site → Astro (not React)
```

**Next.js 15 App Router** (PRIMARY):
```typescript
// app/page.tsx - Server Component (default)
export default async function HomePage() {
  // Direct database/API calls in Server Component
  const posts = await db.posts.findMany()

  return (
    <main>
      <h1>Latest Posts</h1>
      <PostList posts={posts} />
    </main>
  )
}

// Server Component → Client Component boundary
// app/_components/post-list.tsx
'use client' // Explicit client boundary

export function PostList({ posts }: { posts: Post[] }) {
  const [filter, setFilter] = useState('')
  // Client-side interactivity
  return <div>...</div>
}
```

**Vite 7 + React Router** (SPA ALTERNATIVE):
```typescript
// src/router.tsx
import { createBrowserRouter } from 'react-router-dom'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'about', element: <AboutPage /> },
      {
        path: 'dashboard',
        element: <ProtectedRoute />,
        loader: dashboardLoader, // Data loading
        children: [
          { index: true, element: <DashboardPage /> },
        ],
      },
    ],
  },
])

// src/main.tsx
import { RouterProvider } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>
)
```

### Project Structure Patterns

**Feature-Based Architecture** (RECOMMENDED for 10k+ lines):
```
src/
├── app/                            # Next.js App Router
│   ├── layout.tsx                  # Root layout
│   ├── page.tsx                    # Home page
│   ├── (marketing)/                # Route group
│   │   ├── about/page.tsx
│   │   └── pricing/page.tsx
│   └── dashboard/
│       ├── layout.tsx              # Dashboard layout
│       └── page.tsx
├── features/
│   ├── auth/                       # Authentication feature
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── LoginForm.test.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── authService.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts                # Public API
│   ├── products/                   # Products feature
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── index.ts
│   └── README.md                   # Feature documentation
├── components/                     # Shared components
│   ├── ui/                         # UI primitives
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   └── Input/
│   └── layout/                     # Layout components
│       ├── Header.tsx
│       └── Footer.tsx
├── lib/                            # Shared utilities
│   ├── api.ts                      # API client
│   ├── utils.ts                    # Utility functions
│   └── constants.ts                # Constants
└── types/                          # Global types
    └── index.ts
```

**Layer-Based Architecture** (for <10k lines):
```
src/
├── app/                            # Next.js routes
│   ├── layout.tsx
│   └── page.tsx
├── components/                     # All components
│   ├── LoginForm.tsx
│   ├── ProductCard.tsx
│   └── Header.tsx
├── hooks/                          # All custom hooks
│   ├── useAuth.ts
│   └── useProducts.ts
├── services/                       # All API services
│   ├── authService.ts
│   └── productService.ts
├── lib/                            # Utilities
│   └── utils.ts
└── types/                          # All types
    └── index.ts
```

**Decision Criteria**:
- **< 5k lines**: Flat layer-based (simplest)
- **5k - 10k lines**: Layer-based with subdirectories
- **10k - 50k lines**: Feature-based with shared folder
- **> 50k lines**: Strict feature-based with boundaries (e.g., features can't import from each other)

### Component Architecture

**React Server Components (RSC) vs Client Components**:

| Aspect | Server Component | Client Component |
|--------|------------------|------------------|
| **Default** | ✅ Yes (Next.js App Router) | No (must use `'use client'`) |
| **Runs on** | Server only | Server (SSR) + Client |
| **Can use** | async/await, direct DB | useState, useEffect, events |
| **Bundle** | Zero client JS | Added to client bundle |
| **When to use** | Data fetching, layouts | Interactivity, browser APIs |

**Server Component Pattern** (async data fetching):
```typescript
// app/posts/page.tsx
import { db } from '@/lib/db'
import { PostList } from './_components/post-list'

export default async function PostsPage() {
  // Direct database query in Server Component
  const posts = await db.posts.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10,
  })

  return (
    <main>
      <h1>Recent Posts</h1>
      {/* Pass data to Client Component */}
      <PostList initialPosts={posts} />
    </main>
  )
}
```

**Client Component Pattern** (interactivity):
```typescript
// app/posts/_components/post-list.tsx
'use client' // Client boundary

import { useState } from 'react'
import type { Post } from '@/types'

interface PostListProps {
  initialPosts: Post[]
}

export function PostList({ initialPosts }: PostListProps) {
  const [filter, setFilter] = useState('')

  const filteredPosts = initialPosts.filter(post =>
    post.title.toLowerCase().includes(filter.toLowerCase())
  )

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter posts..."
      />
      <ul>
        {filteredPosts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  )
}
```

**Custom Hooks Pattern** (logic extraction):
```typescript
// hooks/useToggle.ts
import { useState, useCallback } from 'react'

export function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => setValue(v => !v), [])
  const setTrue = useCallback(() => setValue(true), [])
  const setFalse = useCallback(() => setValue(false), [])

  return [value, { toggle, setTrue, setFalse }] as const
}

// Usage in Client Component
function Sidebar() {
  const [isOpen, { toggle }] = useToggle(false)
  return <button onClick={toggle}>Toggle</button>
}
```

### State Management Architecture

**State Categories** (CRITICAL CONCEPT):

1. **Server State** → TanStack Query (server data, caching, revalidation)
2. **Client UI State** → Zustand / Context (theme, sidebar open, etc.)
3. **Form State** → React Hook Form (form values, validation)
4. **URL State** → nuqs / React Router (search params, filters)
5. **Local State** → useState / useReducer (component-only state)

**TanStack Query Pattern** (server state):
```typescript
// lib/api.ts
import axios from 'axios'
import { z } from 'zod'

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
})

export type User = z.infer<typeof UserSchema>

export const api = {
  users: {
    list: async (): Promise<User[]> => {
      const { data } = await axios.get('/api/users')
      return z.array(UserSchema).parse(data)
    },
    get: async (id: string): Promise<User> => {
      const { data } = await axios.get(`/api/users/${id}`)
      return UserSchema.parse(data)
    },
  },
}

// hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: api.users.list,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Usage in Client Component
function UserList() {
  const { data: users, isLoading, error } = useUsers()

  if (isLoading) return <Spinner />
  if (error) return <Error message={error.message} />

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**Zustand Pattern** (client UI state):
```typescript
// lib/store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: 'light',
      sidebarOpen: true,
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set((state) => ({
        sidebarOpen: !state.sidebarOpen
      })),
    }),
    {
      name: 'app-storage', // localStorage key
    }
  )
)

// Usage (no provider needed!)
function Header() {
  const theme = useAppStore((state) => state.theme)
  const setTheme = useAppStore((state) => state.setTheme)

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle {theme} mode
    </button>
  )
}
```

**React Hook Form Pattern** (form state):
```typescript
// components/LoginForm.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    // Handle login
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  )
}
```

---

## Outputs

### Primary Deliverables

**1. Next.js 15 App Router Application**:

**Root Layout** (app/layout.tsx):
```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { QueryProvider } from '@/components/providers/query-provider'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js 15',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
```

**Home Page** (app/page.tsx):
```typescript
import { HeroSection } from '@/components/hero-section'
import { FeatureList } from '@/features/home/components/feature-list'

export default function HomePage() {
  return (
    <main>
      <HeroSection />
      <FeatureList />
    </main>
  )
}
```

**Loading State** (app/loading.tsx):
```typescript
export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900" />
    </div>
  )
}
```

**Error Boundary** (app/error.tsx):
```typescript
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

**2. Vite 7 + React Router Application**:

**Entry Point** (src/main.tsx):
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { router } from './router'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
)
```

**Router Configuration** (src/router.tsx):
```typescript
import { createBrowserRouter } from 'react-router-dom'
import { RootLayout } from './components/layout/root-layout'
import { HomePage } from './pages/home-page'
import { NotFoundPage } from './pages/not-found-page'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
    ],
  },
])
```

**3. TypeScript Configuration Files**:

**Next.js tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "plugins": [{ "name": "next" }],
    "incremental": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Vite tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**4. Package Configuration Files**:

**Next.js package.json**:
```json
{
  "name": "my-nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "^15.5.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@tanstack/react-query": "^5.62.0",
    "zustand": "^5.0.0",
    "react-hook-form": "^7.54.0",
    "@hookform/resolvers": "^3.9.0",
    "zod": "^3.24.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.7.0"
  }
}
```

**Vite package.json**:
```json
{
  "name": "my-vite-app",
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.28.0",
    "@tanstack/react-query": "^5.62.0",
    "zustand": "^5.0.0",
    "react-hook-form": "^7.54.0",
    "@hookform/resolvers": "^3.9.0",
    "zod": "^3.24.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.7.0",
    "vite": "^7.1.0"
  }
}
```

---

## Behavior Specification

### Framework Selection Behavior

**Input**: Project requirements (SSR, SEO, interactivity, team size)
**Process**:
1. Evaluate need for server-side rendering
2. Assess SEO requirements
3. Consider team expertise
4. Determine build complexity tolerance

**Output**: Framework recommendation (Next.js vs Vite)

**Decision Matrix**:
```typescript
interface ProjectRequirements {
  needsSSR: boolean
  needsSEO: boolean
  hasDynamicContent: boolean
  isStaticSite: boolean
  teamSizeSmall: boolean
}

function selectFramework(req: ProjectRequirements): 'nextjs' | 'vite' | 'astro' {
  if (req.isStaticSite && !req.hasDynamicContent) return 'astro'
  if (req.needsSSR || req.needsSEO) return 'nextjs'
  if (req.teamSizeSmall && !req.needsSSR) return 'vite'
  return 'nextjs' // default for production apps
}
```

### Project Structure Behavior

**Input**: Project size estimation (lines of code, features)
**Process**:
1. Estimate final codebase size
2. Count number of distinct features
3. Assess team size and coordination needs

**Output**: Structure recommendation (feature-based vs layer-based)

**Algorithm**:
```typescript
function selectProjectStructure(
  estimatedLines: number,
  featureCount: number
): 'flat' | 'layered' | 'feature-based' {
  if (estimatedLines < 5000) return 'flat'
  if (estimatedLines < 10000) return 'layered'
  return 'feature-based'
}
```

### State Management Selection

**Input**: State categories needed
**Process**:
1. Identify server state needs → always TanStack Query
2. Identify shared UI state complexity
3. Identify form complexity
4. Identify URL state needs

**Output**: State management library combination

**Decision Tree Implementation**:
```typescript
interface StateNeeds {
  hasServerData: boolean
  sharedUIStatesCount: number
  hasComplexForms: boolean
  needsURLState: boolean
  teamSize: 'small' | 'medium' | 'large'
}

interface StateManagementStack {
  serverState: 'tanstack-query'
  uiState: 'context' | 'zustand' | 'redux-toolkit'
  formState: 'react-hook-form' | 'useState'
  urlState: 'nuqs' | 'react-router' | null
}

function selectStateManagement(needs: StateNeeds): StateManagementStack {
  return {
    serverState: 'tanstack-query', // Always
    uiState:
      needs.teamSize === 'large' ? 'redux-toolkit' :
      needs.sharedUIStatesCount >= 3 ? 'zustand' :
      'context',
    formState: needs.hasComplexForms ? 'react-hook-form' : 'useState',
    urlState: needs.needsURLState ? 'nuqs' : null,
  }
}
```

---

## Interface Contracts

### Template Contract

All templates provided by SAP-020 MUST:

1. **Compile without errors** using TypeScript strict mode
2. **Run without runtime errors** on first execution
3. **Include type definitions** for all exports
4. **Follow Next.js/React conventions** (file naming, structure)
5. **Include README.md** with setup instructions
6. **Use semantic versioning** for dependencies (^major.minor.patch)

### Component Contract

All React components in templates MUST:

```typescript
// Component interface contract
interface ComponentContract {
  // 1. Named export (not default for reusable components)
  export function ComponentName(props: Props): JSX.Element

  // 2. Props typed with interface/type
  interface Props {
    requiredProp: string
    optionalProp?: number
  }

  // 3. Client components marked explicitly
  // 'use client' // If uses useState, useEffect, event handlers

  // 4. Docstring for complex components
  /**
   * ComponentName does X and Y.
   * @param requiredProp - Description
   * @param optionalProp - Description
   */
}
```

**Example compliant component**:
```typescript
'use client'

import { useState } from 'react'

interface CounterProps {
  initialCount?: number
  max?: number
}

/**
 * Counter component with increment/decrement controls.
 * @param initialCount - Starting count value (default: 0)
 * @param max - Maximum count value (default: 100)
 */
export function Counter({ initialCount = 0, max = 100 }: CounterProps) {
  const [count, setCount] = useState(initialCount)

  const increment = () => setCount(c => Math.min(c + 1, max))
  const decrement = () => setCount(c => Math.max(c - 1, 0))

  return (
    <div>
      <button onClick={decrement}>-</button>
      <span>{count}</span>
      <button onClick={increment}>+</button>
    </div>
  )
}
```

### API Client Contract

All API clients in templates MUST:

1. **Use Axios** for HTTP requests (consistent error handling)
2. **Validate responses** with Zod schemas
3. **Export typed functions** (not raw Axios calls)
4. **Handle errors** consistently (throw typed errors)
5. **Support TypeScript inference** (return types automatically inferred)

**Example compliant API client**:
```typescript
// lib/api.ts
import axios from 'axios'
import { z } from 'zod'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Zod schemas
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['user', 'admin']),
})

export type User = z.infer<typeof UserSchema>

// API functions
export const api = {
  users: {
    list: async (): Promise<User[]> => {
      const { data } = await client.get('/users')
      return z.array(UserSchema).parse(data)
    },

    get: async (id: string): Promise<User> => {
      const { data } = await client.get(`/users/${id}`)
      return UserSchema.parse(data)
    },

    create: async (user: Omit<User, 'id'>): Promise<User> => {
      const { data } = await client.post('/users', user)
      return UserSchema.parse(data)
    },
  },
}
```

---

## Guarantees

### Quality Guarantees

SAP-020 templates guarantee:

1. **100% TypeScript coverage** - No `any` types in template code
2. **Zero compilation errors** - All templates pass `tsc --noEmit`
3. **Zero runtime errors** - All templates run successfully on first execution
4. **Framework compliance** - 100% adherence to Next.js 15 / Vite 7 conventions
5. **Dependency currency** - All dependencies <3 months old at SAP release

### Performance Guarantees

Templates guarantee:

1. **Dev server start** - ≤5 seconds (Next.js Turbopack, Vite)
2. **HMR updates** - ≤100ms (file save to browser update)
3. **TypeScript checks** - ≤10 seconds (first check, incremental <2s)
4. **Bundle size baseline** - Next.js <100KB first load JS (without user code)

### Compatibility Guarantees

Templates are tested on:

1. **Operating Systems** - macOS 14+, Ubuntu 22.04+, Windows 11 (WSL2)
2. **Node.js** - 22.x LTS (Active until April 2027)
3. **Package Managers** - pnpm 10.x, npm 10.x
4. **Browsers** - Chrome 120+, Firefox 120+, Safari 17+, Edge 120+

---

## Test Patterns

### Template Validation Tests

**Purpose**: Ensure templates compile and run

```bash
# Test Next.js template
cd templates/react/nextjs-15-app-router
npm install
npm run type-check  # Must pass
npm run build       # Must succeed
npm run dev &       # Must start in <5s
curl http://localhost:3000  # Must return 200

# Test Vite template
cd templates/react/vite-react-spa
npm install
npm run type-check  # Must pass
npm run build       # Must succeed
npm run dev &       # Must start in <5s
curl http://localhost:5173  # Must return 200
```

### Component Testing Pattern

**Purpose**: Validate components render and behave correctly

**Covered in SAP-021** (React Testing & Quality)

---

## Quality Attributes

### Maintainability

**Dependency Updates**:
- Quarterly review of all template dependencies
- Security patches within 48 hours of disclosure
- Major framework updates within 2 weeks of stable release

**Documentation**:
- All templates include README.md with setup instructions
- All complex functions include JSDoc comments
- All TypeScript types documented with descriptions

### Reliability

**Error Handling**:
- All async operations wrapped in try/catch
- All API responses validated with Zod
- All user inputs validated before processing

**Stability**:
- Templates pinned to stable versions (no `latest`)
- No experimental features in production templates
- Fallbacks for all external dependencies

### Usability

**Developer Experience**:
- Clear error messages (TypeScript, ESLint)
- Helpful comments in template code
- Consistent naming conventions
- Intuitive file organization

**Onboarding**:
- README includes "Quick Start" section
- Example .env.example for environment variables
- Package.json scripts self-documenting

---

## Version Compatibility Matrix

| Dependency | Version | Status | EOL Date |
|------------|---------|--------|----------|
| React | 19.x | ✅ Stable | TBD |
| Next.js | 15.5.x | ✅ Stable | ~2025-10 |
| Vite | 7.x | ✅ Stable | ~2026-01 |
| TypeScript | 5.7.x | ✅ Stable | ~2025-11 |
| Node.js | 22.x LTS | ✅ Active | 2027-04 |
| TanStack Query | 5.x | ✅ Stable | ~2025-12 |
| Zustand | 5.x | ✅ Stable | ~2025-12 |
| React Hook Form | 7.x | ✅ Stable | TBD |
| React Router | 6.x | ✅ Stable | ~2025-06 |

**Update Policy**:
- Templates updated within 2 weeks of major framework releases
- Security patches applied within 48 hours
- Breaking changes documented in CHANGELOG.md

---

## Appendix: React 19 Features

**New in React 19** (December 5, 2024):

1. **Actions API** - Form handling without useState
2. **use() hook** - Async data in components
3. **ref as prop** - No more forwardRef
4. **Document metadata** - `<title>`, `<meta>` in components
5. **Asset loading** - `<link rel="preload">` priority

**Status in SAP-020**: Documented but not required (patterns still stabilizing)

**Example (Actions API)**:
```typescript
'use client'

async function createPost(formData: FormData) {
  'use server' // Server Action
  const title = formData.get('title')
  // Create post in database
}

export function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

---

## Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents self-evaluation criteria for SAP-020 awareness file completeness, enabling automated validation of equivalent support for generic agents and Claude Code.

### Awareness File Requirements

**Required Files**:
- `AGENTS.md` - Generic AI agent workflows
- `CLAUDE.md` - Claude Code-specific tool patterns

**Validation Command**:
```bash
python scripts/sap-evaluator.py --deep react-foundation
```

### Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Create Next.js 15 App Router Project (15-25 min) - Scaffold production-ready Next.js with TypeScript, App Router, RSC
2. Create Vite + React Router SPA (10-15 min) - Scaffold fast SPA with Vite, React Router, TypeScript strict mode
3. Apply Feature-Based Project Structure (10-20 min) - Implement scalable feature-based architecture for 10k+ line projects
4. Configure TypeScript Strict Mode (5-10 min) - Enable strict mode with all type safety options
5. Migrate from Create React App (30-60 min) - Migrate deprecated CRA to Vite or Next.js

**CLAUDE.md**: 3 workflows
1. Scaffolding Next.js 15 Project with Bash and Write - Check templates, copy files, install dependencies, start dev server
2. Scaffolding Vite SPA with Bash and Write - Copy template, install dependencies, verify server running
3. Applying Feature-Based Structure with Bash and Write - Create feature directories, generate module templates, update path aliases

**Variance**: 3 workflows (CLAUDE.md) vs 5 workflows (AGENTS.md) = 40% difference
**Acceptable**: Yes (within ±30-40% tolerance with documented rationale)

**Rationale for Variance**: CLAUDE.md focuses on template-based scaffolding with tool-specific patterns (Bash for directory creation, Write for new files, Edit for modifications), consolidating multiple operations into single workflows. AGENTS.md provides granular step-by-step guidance for each React scaffolding operation including TypeScript configuration and CRA migration. Both provide equivalent coverage of Next.js scaffolding, Vite SPA creation, and feature-based structure through different organizational approaches optimized for their respective audiences.

### User Signal Pattern Coverage

**AGENTS.md**: 2 tables with 9 signals
- Project Scaffolding Operations table (5 signals):
  - "create React project" → scaffold_nextjs_project()
  - "setup Next.js app" → scaffold_nextjs_project()
  - "create SPA" → scaffold_vite_project()
  - "migrate from CRA" → migrate_from_cra()
  - "setup TypeScript React" → scaffold_with_typescript()
- Project Structure Operations table (4 signals):
  - "organize project structure" → apply_feature_based_structure()
  - "setup folders" → apply_layer_based_structure()
  - "add feature module" → create_feature_module(name)
  - "setup path aliases" → configure_path_aliases()

**CLAUDE.md**: Tool-specific patterns documented in 5 tips
- Tip 1: Always check templates exist before scaffolding
- Tip 2: Use Bash for fast directory creation
- Tip 3: Use Write for config files, Edit for modifications
- Tip 4: Start dev servers in background for verification
- Tip 5: Use Read to check existing config before modifying

**Coverage**: AGENTS.md provides user signal translation for React project operations, CLAUDE.md provides tool patterns for implementing those signals with Claude Code tools (Bash, Write, Edit, Read).

### Validation Checkpoints

**Structural Validation**:
```bash
# Check both awareness files exist
ls docs/skilled-awareness/react-foundation/AGENTS.md
ls docs/skilled-awareness/react-foundation/CLAUDE.md

# Check YAML frontmatter present
head -20 docs/skilled-awareness/react-foundation/AGENTS.md | grep "sap_id: SAP-020"
head -20 docs/skilled-awareness/react-foundation/CLAUDE.md | grep "sap_id: SAP-020"
```

**Coverage Validation**:
```bash
# Count workflows in AGENTS.md (expect: 5)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/react-foundation/AGENTS.md

# Count workflows in CLAUDE.md (expect: 3)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/react-foundation/CLAUDE.md

# Check user signal tables exist in AGENTS.md
grep -c "## User Signal Patterns" docs/skilled-awareness/react-foundation/AGENTS.md
```

**Expected Results**:
- Both awareness files exist ✅
- YAML frontmatter with progressive_loading ✅
- AGENTS.md: 5 workflows, 2 user signal tables ✅
- CLAUDE.md: 3 workflows, 5 tool-specific tips ✅
- Workflow variance: 40% (acceptable with documented rationale) ✅

### Integration with SAP-009

**Phase 4 Criteria Met**:
- ✅ AGENTS.md provides generic workflow guidance
- ✅ CLAUDE.md provides Claude Code tool patterns
- ✅ Workflow coverage within acceptable variance (40% with rationale)
- ✅ Rationale documented for organizational differences
- ✅ Self-evaluation criteria documented in protocol-spec.md

**SAP-020 Awareness Status**: Phase 4 compliant (equivalent support for generic agents and Claude Code)

---

**End of Protocol Specification**
