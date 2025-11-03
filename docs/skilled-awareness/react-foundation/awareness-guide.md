# SAP-020: React Project Foundation - Awareness Guide

**SAP ID**: SAP-020
**Version**: 1.0.0
**Last Updated**: 2025-10-31
**Status**: Active

---

## Overview

This guide provides comprehensive awareness for AI agents and developers working with the React Project Foundation capability package (SAP-020). It covers workflows, decision trees, common pitfalls, and cross-domain integration patterns for building modern React applications.

**Audience**: AI agents (Claude Code, GPT-4, etc.), developers building React applications
**Prerequisite SAPs**: SAP-000 (SAP Framework), SAP-003 (Project Bootstrap - optional)
**Complementary SAPs**: SAP-021 (Testing), SAP-022 (Linting), SAP-023 (State), SAP-024 (Styling)

---

## When to Use SAP-020

### Use Case 1: Building Full-Stack React Applications with SSR

**Scenario**: You're building a web application that needs server-side rendering (SSR), SEO optimization, dynamic routes, and modern React patterns (React Server Components).

**Why SAP-020**:
- ✅ Next.js 15 App Router provides SSR, SSG, ISR out of the box
- ✅ React Server Components reduce bundle size by 40-60%
- ✅ File-based routing eliminates configuration overhead
- ✅ Built-in optimizations (images, fonts, code splitting)
- ✅ Battle-tested templates reduce setup time from 8-12h to 45min

**Example**:
```typescript
// app/posts/[id]/page.tsx - Dynamic route with SSR
export default async function PostPage({ params }: { params: { id: string } }) {
  // Direct database call in Server Component
  const post = await db.posts.findUnique({ where: { id: params.id } })

  return (
    <article>
      <h1>{post.title}</h1>
      <PostContent content={post.content} />
    </article>
  )
}
```

**Alternatives**:
- Remix (e-commerce focus, Shopify integration)
- Astro (content-heavy sites, MDX support)
- Vite + React Router (no SSR, SPA only)

**Decision Criteria**: Use Next.js 15 if you need SSR, SEO, or full-stack capabilities.

---

### Use Case 2: Building Single-Page Applications (SPAs) Without SSR

**Scenario**: You're building an internal dashboard, admin panel, or authenticated app where SEO doesn't matter and you want maximum dev speed with minimal configuration.

**Why SAP-020**:
- ✅ Vite 7 provides 20x faster dev server than Webpack
- ✅ React Router v6 gives flexible client-side routing
- ✅ No server-side complexity (easier deployment)
- ✅ Smaller learning curve than Next.js App Router
- ✅ Perfect for apps behind authentication (no SEO needs)

**Example**:
```typescript
// src/router.tsx
import { createBrowserRouter } from 'react-router-dom'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'settings', element: <SettingsPage /> },
      {
        path: 'users/:id',
        element: <UserDetailPage />,
        loader: async ({ params }) => {
          // Client-side data loading
          return fetch(`/api/users/${params.id}`).then(r => r.json())
        },
      },
    ],
  },
])
```

**Alternatives**:
- Next.js App Router (overkill if no SSR needed)
- Create React App (deprecated as of February 2024 - DON'T USE)

**Decision Criteria**: Use Vite if you don't need SSR and want maximum dev speed.

---

### Use Case 3: Migrating from Create React App (CRA)

**Scenario**: You have an existing Create React App project that needs to migrate off CRA (officially deprecated February 2024).

**Why SAP-020**:
- ✅ Provides clear migration path to Vite 7
- ✅ Minimal code changes (CRA → Vite mostly config)
- ✅ Dramatically faster dev server (10-30s → <1s)
- ✅ Modern build tooling (ESM, faster HMR)

**Migration Steps**:
1. Use Vite 7 template from SAP-020
2. Copy `src/` folder to new project
3. Update imports (remove `%PUBLIC_URL%`, update paths)
4. Replace `react-scripts` commands with Vite
5. Test and deploy

**Example**:
```typescript
// Before (CRA): index.tsx
import ReactDOM from 'react-dom'
ReactDOM.render(<App />, document.getElementById('root'))

// After (Vite): main.tsx
import ReactDOM from 'react-dom/client'
ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
```

**Alternatives**:
- Migrate to Next.js (bigger change, requires SSR understanding)
- Stay on CRA (security risk, no updates, deprecated)

**Decision Criteria**: Vite is the lowest-friction CRA migration path.

---

### Use Case 4: Building Type-Safe React Applications

**Scenario**: You want end-to-end type safety from API responses to UI components, preventing runtime errors and improving developer productivity.

**Why SAP-020**:
- ✅ TypeScript strict mode catches 40% more errors at compile time
- ✅ Zod schemas validate API responses at runtime
- ✅ TanStack Query provides full type inference
- ✅ Path aliases eliminate brittle relative imports

**Example**:
```typescript
// lib/api.ts - Type-safe API client
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
      return z.array(UserSchema).parse(data) // Runtime validation
    },
  },
}

// hooks/useUsers.ts - Type-safe hook
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: api.users.list, // Type inferred automatically
  })
}

// components/UserList.tsx - Fully typed component
export function UserList() {
  const { data: users } = useUsers() // users: User[] | undefined
  return <div>{users?.map(u => u.name)}</div> // Full autocomplete
}
```

**Alternatives**:
- JavaScript without TypeScript (no compile-time safety)
- TypeScript without strict mode (weaker type checking)

**Decision Criteria**: TypeScript strict mode is mandatory in SAP-020.

---

### Use Case 5: Standardizing React Architecture Across Teams

**Scenario**: You have multiple teams building React apps with inconsistent project structures, state management patterns, and tooling choices, leading to maintenance headaches.

**Why SAP-020**:
- ✅ Provides opinionated, research-backed defaults
- ✅ Feature-based structure scales from small to large apps
- ✅ Clear state management patterns (server vs client state)
- ✅ Consistent tooling (TypeScript, pnpm, Next.js/Vite)

**Example**:
```
# Team A before SAP-020
my-app/
├── components/  (250 files, flat)
├── utils/       (mixed concerns)
└── pages/       (Redux everywhere)

# Team A after SAP-020
my-app/
├── features/auth/       (authentication feature)
├── features/products/   (products feature)
├── components/ui/       (shared UI primitives)
└── lib/                 (utilities, API client)

# Team B also follows same structure → easy knowledge transfer
```

**Alternatives**:
- Each team chooses their own structure (chaos)
- Mandate structure without tooling support (low adoption)

**Decision Criteria**: Use SAP-020 to enforce architectural standards.

---

## Anti-Patterns (When NOT to Use SAP-020)

### Anti-Pattern 1: React Native Mobile Apps

**Scenario**: You're building a mobile app with React Native for iOS/Android.

**Why NOT SAP-020**:
- ❌ SAP-020 targets web React (Next.js, Vite)
- ❌ React Native uses different routing (React Navigation)
- ❌ Different build tools (Metro bundler, not Webpack/Vite)
- ❌ Different styling (StyleSheet, not CSS/Tailwind)

**Alternative**:
- Use React Native CLI or Expo
- Wait for potential SAP-XXX (React Native Development) in future

---

### Anti-Pattern 2: Static Content Sites

**Scenario**: You're building a blog, documentation site, or marketing site with mostly static content and minimal interactivity.

**Why NOT SAP-020**:
- ❌ React is overkill for static content
- ❌ Larger bundle size than static site generators
- ❌ Slower builds than Astro/Hugo/11ty

**Alternative**:
- **Astro** (supports React components but outputs HTML)
- **Next.js with Static Export** (if you must use React)
- **Hugo, 11ty, Jekyll** (pure static)

**Decision Criteria**: Use static site generator if <10% of pages have interactivity.

---

### Anti-Pattern 3: Legacy React Projects (React <18)

**Scenario**: You have an existing React 16/17 app with class components and legacy patterns.

**Why NOT SAP-020**:
- ❌ SAP-020 templates use React 19 features (Actions, use() hook)
- ❌ Next.js 15 requires React 19
- ❌ Migration effort high (class → function components)

**Alternative**:
- Gradual migration: Stay on current stack, slowly adopt hooks
- Fork SAP-020 templates to use React 18 (lose RSC benefits)

**Decision Criteria**: Only use SAP-020 for greenfield or React 18+ projects.

---

### Anti-Pattern 4: Non-JavaScript Back-Ends with No Client JS Needs

**Scenario**: You have a Django/Rails/Laravel back-end and only need simple interactivity (dropdowns, modals, form validation).

**Why NOT SAP-020**:
- ❌ React adds 40-100KB minimum bundle size
- ❌ Build complexity (Node.js, npm, bundlers)
- ❌ SEO complexity (need SSR or static generation)

**Alternative**:
- **htmx** (HTML-over-the-wire, no JS bundles)
- **Alpine.js** (lightweight reactivity, 15KB)
- **Vanilla JS** (modern browsers are very capable)

**Decision Criteria**: Use React only if you need complex state management or reusable component libraries.

---

### Anti-Pattern 5: Electron Desktop Apps

**Scenario**: You're building a desktop application with Electron + React.

**Why NOT SAP-020**:
- ❌ Electron uses different bundling (webpack/vite configured for Node.js environment)
- ❌ No routing needed (single window app)
- ❌ Different security model (CSP, Node.js integration)

**Alternative**:
- Use Electron-specific React templates (electron-react-boilerplate)
- Adapt SAP-020 Vite template for Electron renderer process

**Decision Criteria**: SAP-020 is web-focused; Electron needs specialized config.

---

## Decision Trees

### Decision Tree 1: Framework Selection (Next.js vs Vite)

```
What are you building?
├─ Need SSR or SEO?
│  └─ YES → Next.js 15 App Router
│     ├─ E-commerce with Shopify? → Remix + Hydrogen
│     └─ General full-stack → Next.js 15 ✅
└─ NO (SPA behind auth) → Vite 7 + React Router ✅
   ├─ Need static export? → Next.js with static export
   └─ Maximum dev speed? → Vite 7 ✅
```

**Implementation**:
```typescript
function selectFramework(requirements: {
  needsSSR: boolean
  needsSEO: boolean
  isEcommerce: boolean
  maxDevSpeed: boolean
}): 'nextjs' | 'vite' | 'remix' {
  if (requirements.isEcommerce) return 'remix'
  if (requirements.needsSSR || requirements.needsSEO) return 'nextjs'
  if (requirements.maxDevSpeed) return 'vite'
  return 'nextjs' // default for production apps
}
```

---

### Decision Tree 2: Project Structure (Feature-Based vs Layer-Based)

```
How large will the codebase be?
├─ < 5,000 lines → Flat layer-based
│  src/
│  ├── components/
│  ├── hooks/
│  └── lib/
│
├─ 5,000 - 10,000 lines → Layer-based with subdirectories
│  src/
│  ├── components/ui/, components/forms/
│  ├── hooks/
│  └── lib/
│
└─ > 10,000 lines → Feature-based ✅
   src/
   ├── features/auth/
   ├── features/products/
   └── components/ui/ (shared)
```

**Implementation**:
```typescript
function selectProjectStructure(estimatedLines: number): 'flat' | 'layered' | 'feature-based' {
  if (estimatedLines < 5000) return 'flat'
  if (estimatedLines < 10000) return 'layered'
  return 'feature-based'
}
```

---

### Decision Tree 3: State Management Selection

```
What state do you need?
├─ Server data (API, database) → TanStack Query ✅ (always)
├─ Form data → React Hook Form ✅
├─ URL parameters → nuqs (Next.js) or React Router ✅
└─ Client UI state (theme, sidebar, modals) → How many?
   ├─ 1-2 simple states → Context API
   ├─ 3+ states OR performance issues → Zustand ✅
   └─ 50+ developers, strict patterns → Redux Toolkit
```

**Implementation**:
```typescript
interface StateNeeds {
  hasServerData: boolean
  hasComplexForms: boolean
  sharedUIStatesCount: number
  teamSize: 'small' | 'medium' | 'large'
}

function selectStateManagement(needs: StateNeeds) {
  return {
    serverState: needs.hasServerData ? 'tanstack-query' : null,
    formState: needs.hasComplexForms ? 'react-hook-form' : 'useState',
    uiState:
      needs.teamSize === 'large' ? 'redux-toolkit' :
      needs.sharedUIStatesCount >= 3 ? 'zustand' :
      'context-api',
  }
}
```

---

### Decision Tree 4: Server Component vs Client Component (Next.js)

```
Does this component need...
├─ useState, useEffect, or event handlers?
│  └─ YES → Client Component ('use client') ✅
├─ Browser APIs (localStorage, window)?
│  └─ YES → Client Component ✅
├─ Direct database/API calls?
│  └─ YES → Server Component (async function) ✅
└─ Static content, no interactivity?
   └─ YES → Server Component (default) ✅
```

**Rule of Thumb**: Start with Server Components (default), add `'use client'` only when needed.

**Example**:
```typescript
// Server Component (no 'use client')
export default async function PostsPage() {
  const posts = await db.posts.findMany()
  return <PostList posts={posts} />
}

// Client Component (needs interactivity)
'use client'
export function PostList({ posts }: { posts: Post[] }) {
  const [filter, setFilter] = useState('')
  return <input onChange={(e) => setFilter(e.target.value)} />
}
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Using `any` Type in TypeScript

**Problem**: TypeScript strict mode errors are annoying, so developers use `any` to bypass them, losing type safety.

**Symptoms**:
```typescript
// ❌ BAD
const users: any = await fetchUsers()
users.forEach((user: any) => console.log(user.name)) // No autocomplete
```

**Solution**: Use proper types or `unknown` + type guards
```typescript
// ✅ GOOD
const UserSchema = z.object({ id: z.string(), name: z.string() })
type User = z.infer<typeof UserSchema>

const users: User[] = z.array(UserSchema).parse(await fetchUsers())
users.forEach(user => console.log(user.name)) // Full autocomplete ✅
```

**SAP-020 Enforcement**: Templates use `noImplicitAny` and `strict: true` to catch this.

---

### Pitfall 2: Mixing Server State with Client State

**Problem**: Using Zustand/Redux for server data leads to cache invalidation bugs and stale data.

**Symptoms**:
```typescript
// ❌ BAD: Server data in Zustand
const useStore = create((set) => ({
  users: [],
  fetchUsers: async () => {
    const users = await api.users.list()
    set({ users }) // Manual cache management, bugs inevitable
  },
}))
```

**Solution**: Use TanStack Query for server data, Zustand for UI state
```typescript
// ✅ GOOD: Separate concerns
// Server state
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: api.users.list, // TanStack Query handles caching
})

// Client UI state
const useAppStore = create((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}))
```

**SAP-020 Guidance**: Protocol spec clearly separates state categories.

---

### Pitfall 3: Using `'use client'` on Every Component (Next.js)

**Problem**: Developers add `'use client'` to all files to avoid thinking about Server vs Client Components, losing RSC benefits.

**Symptoms**:
```typescript
// ❌ BAD: Unnecessary 'use client'
'use client'

export function Header({ title }: { title: string }) {
  return <h1>{title}</h1> // No interactivity, no hooks
}
```

**Solution**: Only use `'use client'` when needed
```typescript
// ✅ GOOD: Server Component (default)
export function Header({ title }: { title: string }) {
  return <h1>{title}</h1> // Zero client JS
}

// 'use client' only for interactivity
'use client'
export function DarkModeToggle() {
  const [theme, setTheme] = useState('light')
  return <button onClick={() => setTheme(...)}>Toggle</button>
}
```

**SAP-020 Guidance**: Templates show clear examples of Server vs Client Components.

---

### Pitfall 4: Relative Import Hell

**Problem**: Deep nested imports like `../../../../lib/utils` are brittle and hard to refactor.

**Symptoms**:
```typescript
// ❌ BAD
import { formatDate } from '../../../../lib/utils'
import { Button } from '../../../components/ui/button'
```

**Solution**: Use TypeScript path aliases (`@/*`)
```typescript
// ✅ GOOD (with tsconfig paths)
import { formatDate } from '@/lib/utils'
import { Button } from '@/components/ui/button'

// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**SAP-020 Default**: All templates include `@/*` path alias configured.

---

### Pitfall 5: Not Using Package Manager Workspaces (Monorepos)

**Problem**: Multiple related packages (web app, mobile app, shared lib) are in separate repos, causing version drift.

**Symptoms**:
- Shared code duplicated across repos
- Version mismatches (`app1` uses `v1.0`, `app2` uses `v2.0`)
- Changes require manual syncing

**Solution**: Use pnpm workspaces (monorepo)
```json
// pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'

// apps/web/package.json
{
  "dependencies": {
    "@myorg/shared": "workspace:*"
  }
}
```

**SAP-020 Status**: Monorepo patterns not covered (future SAP-XXX planned).

---

## Integration with Other SAPs

### Integration 1: SAP-021 (React Testing & Quality)

**Connection**: SAP-020 provides project foundation, SAP-021 adds testing infrastructure.

**Workflow**:
1. Install SAP-020 (Next.js/Vite project with TypeScript)
2. Install SAP-021 (adds Vitest, React Testing Library, MSW)
3. Write tests for components created with SAP-020 patterns

**Example**:
```typescript
// Component from SAP-020
export function Counter({ initialCount = 0 }: { initialCount?: number }) {
  const [count, setCount] = useState(initialCount)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// Test from SAP-021
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { Counter } from './counter'

test('increments count on click', async () => {
  render(<Counter initialCount={5} />)
  const button = screen.getByRole('button')
  expect(button).toHaveTextContent('5')

  await userEvent.click(button)
  expect(button).toHaveTextContent('6')
})
```

**Cross-Reference**: [SAP-021 awareness-guide.md](../react-testing/awareness-guide.md)

---

### Integration 2: SAP-022 (React Linting & Formatting)

**Connection**: SAP-020 provides code, SAP-022 enforces code quality.

**Workflow**:
1. Install SAP-020 (project foundation)
2. Install SAP-022 (adds ESLint 9, Prettier, pre-commit hooks)
3. Code quality enforced automatically

**Example**:
```bash
# After SAP-020 + SAP-022
git commit -m "Add feature"

# Pre-commit hook runs automatically:
# 1. ESLint checks (Next.js rules, React hooks rules)
# 2. Prettier formats code
# 3. TypeScript type checks
# 4. If any fail, commit is blocked
```

**Cross-Reference**: [SAP-022 adoption-blueprint.md](../react-linting/adoption-blueprint.md)

---

### Integration 3: SAP-023 (React State Management)

**Connection**: SAP-020 includes basic state patterns, SAP-023 provides advanced patterns.

**Workflow**:
1. SAP-020: TanStack Query + Zustand setup basics
2. SAP-023: Optimistic updates, pagination, infinite scroll, persistence

**Example**:
```typescript
// SAP-020: Basic query
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: api.users.list,
})

// SAP-023: Optimistic update with mutation
const { mutate: createUser } = useMutation({
  mutationFn: api.users.create,
  onMutate: async (newUser) => {
    // Optimistic update
    await queryClient.cancelQueries({ queryKey: ['users'] })
    const previous = queryClient.getQueryData(['users'])
    queryClient.setQueryData(['users'], (old) => [...old, newUser])
    return { previous }
  },
  onError: (err, newUser, context) => {
    // Rollback on error
    queryClient.setQueryData(['users'], context.previous)
  },
})
```

**Cross-Reference**: [SAP-023 protocol-spec.md](../react-state-management/protocol-spec.md)

---

### Integration 4: SAP-003 (Project Bootstrap)

**Connection**: SAP-003 provides Copier scaffolding, SAP-020 provides React templates.

**Workflow** (future integration):
1. Use Copier to generate project from SAP-020 templates
2. Answer prompts (Next.js vs Vite, TypeScript strict, etc.)
3. Generated project ready to run

**Example**:
```bash
# Future integration (not yet implemented)
copier copy gh:liminalcommons/chora-base/templates/react/nextjs-15 my-app

# Prompts:
# - Project name: my-app
# - Use TypeScript strict mode? (yes)
# - Include TanStack Query? (yes)
# - Include Zustand? (no)

cd my-app
npm install
npm run dev  # Running in 45 minutes from project idea
```

**Status**: Integration planned but not yet implemented.

---

### Integration 5: SAP-009 (Agent Awareness)

**Connection**: SAP-020 React projects should include AGENTS.md for AI agent guidance.

**Workflow**:
1. SAP-020 templates include AGENTS.md
2. AGENTS.md references React-specific patterns
3. AI agents use AGENTS.md for context-aware assistance

**Example AGENTS.md** (Next.js project):
```markdown
# Project: My Next.js App

## Architecture
- Framework: Next.js 15 App Router
- State: TanStack Query (server), Zustand (client UI)
- Styling: Tailwind CSS v4

## Patterns
- Server Components default, use 'use client' only when needed
- Co-locate tests: Button.tsx → Button.test.tsx
- API calls via lib/api.ts (Axios + Zod validation)

## SAPs Installed
- SAP-020 (React Foundation)
- SAP-021 (React Testing)
- SAP-022 (React Linting)
```

**Cross-Reference**: [SAP-009 protocol-spec.md](../agent-awareness/protocol-spec.md)

---

## Workflows

### Workflow 1: Creating a New Next.js 15 Project from Scratch

**Goal**: Go from zero to running Next.js app in 45 minutes.

**Steps**:
1. **Choose template** (45 seconds)
   ```bash
   cd templates/react/nextjs-15-app-router
   ```

2. **Copy template to new project** (1 minute)
   ```bash
   cp -r templates/react/nextjs-15-app-router ../my-nextjs-app
   cd ../my-nextjs-app
   ```

3. **Install dependencies** (3-5 minutes)
   ```bash
   pnpm install  # or npm install
   ```

4. **Configure environment** (2 minutes)
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys, database URL, etc.
   ```

5. **Start dev server** (30 seconds)
   ```bash
   pnpm dev --turbo
   # Opens http://localhost:3000
   ```

6. **Customize for your use case** (30-40 minutes)
   - Update `app/layout.tsx` with your app name
   - Create first feature in `src/features/`
   - Add first route in `app/`
   - Test data fetching with TanStack Query

**Total Time**: ~45 minutes to running, customized app

---

### Workflow 2: Migrating from Create React App to Vite

**Goal**: Move existing CRA project to modern Vite 7 stack.

**Steps**:
1. **Backup existing project** (1 minute)
   ```bash
   git checkout -b migrate-to-vite
   ```

2. **Copy Vite template** (2 minutes)
   ```bash
   cp -r path/to/sap-020/templates/vite-react-spa/* .
   ```

3. **Migrate src/ files** (10-20 minutes)
   ```bash
   # Keep your existing src/ folder
   # Update imports:
   # - Remove %PUBLIC_URL% references
   # - Update to use @/* path aliases
   # - Change React 18 to React 19 patterns
   ```

4. **Update index.html** (2 minutes)
   ```html
   <!-- Old CRA: public/index.html with %PUBLIC_URL% -->
   <!-- New Vite: index.html in root with <script src="/src/main.tsx"> -->
   ```

5. **Update package.json** (5 minutes)
   ```json
   {
     "scripts": {
       "dev": "vite",  // was "start": "react-scripts start"
       "build": "vite build",  // was "build": "react-scripts build"
       "preview": "vite preview"  // new
     }
   }
   ```

6. **Test and fix imports** (10-30 minutes)
   ```bash
   pnpm dev
   # Fix any import errors, update to ESM syntax
   ```

**Total Time**: ~1-2 hours (much faster than rewriting)

---

### Workflow 3: Adding a New Feature (Feature-Based Architecture)

**Goal**: Add a new feature (e.g., "products") following SAP-020 patterns.

**Steps**:
1. **Create feature directory** (1 minute)
   ```bash
   mkdir -p src/features/products/{components,hooks,services,types}
   ```

2. **Define types** (3 minutes)
   ```typescript
   // src/features/products/types/product.types.ts
   import { z } from 'zod'

   export const ProductSchema = z.object({
     id: z.string(),
     name: z.string(),
     price: z.number(),
   })

   export type Product = z.infer<typeof ProductSchema>
   ```

3. **Create service** (5 minutes)
   ```typescript
   // src/features/products/services/productService.ts
   import { api } from '@/lib/api'
   import { ProductSchema, type Product } from '../types/product.types'

   export const productService = {
     list: () => api.get('/products').then(r => z.array(ProductSchema).parse(r.data)),
     get: (id: string) => api.get(`/products/${id}`).then(r => ProductSchema.parse(r.data)),
   }
   ```

4. **Create hook** (3 minutes)
   ```typescript
   // src/features/products/hooks/useProducts.ts
   import { useQuery } from '@tanstack/react-query'
   import { productService } from '../services/productService'

   export function useProducts() {
     return useQuery({
       queryKey: ['products'],
       queryFn: productService.list,
     })
   }
   ```

5. **Create component** (10 minutes)
   ```typescript
   // src/features/products/components/ProductList.tsx
   'use client'
   import { useProducts } from '../hooks/useProducts'

   export function ProductList() {
     const { data: products, isLoading } = useProducts()
     if (isLoading) return <div>Loading...</div>
     return <ul>{products?.map(p => <li key={p.id}>{p.name}</li>)}</ul>
   }
   ```

6. **Export public API** (2 minutes)
   ```typescript
   // src/features/products/index.ts
   export { ProductList } from './components/ProductList'
   export { useProducts } from './hooks/useProducts'
   export type { Product } from './types/product.types'
   ```

7. **Use in app** (2 minutes)
   ```typescript
   // app/products/page.tsx
   import { ProductList } from '@/features/products'

   export default function ProductsPage() {
     return <ProductList />
   }
   ```

**Total Time**: ~25 minutes for complete feature with types, services, hooks, components

---

## Cross-Domain References

### Dev Docs (docs/dev-docs/)

**Research Documents**:
- [RT-019-CORE: Foundation Stack](../../dev-docs/research/react/RT-019-CORE%20Research%20Report-%20Foundation%20Stack%20%26%20Architecture%20for%20SAP-019.md)
- [RT-019-DEV: Developer Experience](../../dev-docs/research/react/RT-019-DEV%20Research%20Report-%20Developer%20Experience%20%26%20Quality%20Tooling%20for%20SAP-019.md)
- [RT-019-PROD: Production Excellence](../../dev-docs/research/react/RT-019-PROD%20Research%20Report-%20Production%20Excellence%20for%20SAP-019.md)

**Workflows**:
- React component creation workflow (future)
- Next.js App Router routing patterns (future)

### User Docs (docs/user-docs/)

**How-To Guides** (future):
- How to create a Next.js 15 project with SAP-020
- How to add a new route in Next.js App Router
- How to set up TanStack Query for API calls
- How to create a Zustand store for UI state
- How to migrate from Create React App to Vite

**Reference**:
- React stack decision criteria (Next.js vs Vite vs Remix)
- TypeScript configuration reference
- State management decision matrix

### Project Docs (docs/project-docs/)

**Adoption Metrics** (future):
- SAP-020 adoption tracking (projects created, time saved)
- Framework choice breakdown (Next.js vs Vite usage)
- TypeScript strict mode adoption rate

### System Files

**Templates**:
- `templates/react/nextjs-15-app-router/` - Next.js 15 starter
- `templates/react/vite-react-spa/` - Vite 7 SPA starter
- `templates/react/configs/` - TypeScript, Next.js, Vite configs

**Configuration**:
- `sap-catalog.json` - SAP-020 entry with metadata
- `.gitignore` - React-specific ignores (node_modules, .next, dist)

---

## Agent-Specific Guidance

### For Claude Code

**When creating React projects**:
1. Ask user: "Next.js (full-stack with SSR) or Vite (SPA)?"
2. Use appropriate SAP-020 template
3. Follow feature-based architecture for medium+ projects
4. Always use TypeScript strict mode
5. Separate server state (TanStack Query) from client state (Zustand)

**When debugging React issues**:
1. Check if component needs `'use client'` (useState, useEffect, events)
2. Verify TypeScript strict mode compliance
3. Ensure API responses validated with Zod
4. Check for proper error boundaries

**Common mistakes to avoid**:
- Don't use `any` type (use proper types or `unknown`)
- Don't mix server state in Zustand (use TanStack Query)
- Don't use relative imports (use `@/*` aliases)
- Don't add `'use client'` to every file (only when needed)

### For Other AI Agents

**Workflow Execution**:
1. Read `capability-charter.md` for business context
2. Read `protocol-spec.md` for technical patterns
3. Read `awareness-guide.md` (this file) for decision trees
4. Read `adoption-blueprint.md` for installation steps
5. Execute installation, following agent-executable format

**Decision Making**:
- Use decision trees above for framework selection
- Reference RT-019 research for ecosystem data
- Check protocol-spec for code examples
- Validate against guarantees (TypeScript strict, zero errors)

---

## Version-Specific Notes

### React 19 (December 2024)

**New Features**:
- **Actions API**: Form handling without useState
- **use() hook**: Async data fetching in components
- **ref as prop**: No more forwardRef

**Status**: Stable, production-ready

**Adoption in SAP-020**: Documented but not required (Actions still stabilizing)

### Next.js 15 (October 2024)

**Key Changes**:
- Turbopack stable for dev mode (`next dev --turbo`)
- React 19 support
- Improved caching behavior
- Async request APIs (cookies, headers, params)

**Status**: Stable, recommended

### Vite 7 (January 2025)

**Key Changes**:
- 20x faster cold start than Webpack
- Native ESM everywhere
- Lightning-fast HMR (<50ms)

**Status**: Stable, production-ready

---

## Maintenance & Updates

### Quarterly Reviews

SAP-020 reviewed quarterly for:
- Next.js/React/Vite version updates
- Dependency security patches
- Ecosystem shifts (npm download trends)
- New patterns (React 19 Actions adoption)

**Last Review**: 2025-10-31
**Next Review**: 2026-01-31

### Annual Research Updates

RT-019 research updated annually:
- Re-evaluate framework popularity (Next.js vs Remix vs Vite)
- Re-assess state management (Zustand vs Redux Toolkit)
- Update TypeScript best practices
- Review Core Web Vitals targets

**Last Research**: RT-019 (Q4 2024 - Q1 2025)
**Next Research**: RT-019 v2 (Q4 2025)

---

## FAQ

**Q: Should I use Next.js Pages Router or App Router?**
A: App Router (default in SAP-020). Pages Router is legacy as of Next.js 13+.

**Q: Is TypeScript required?**
A: Yes, SAP-020 enforces TypeScript strict mode (78% industry adoption, 40% productivity gain).

**Q: Can I use SAP-020 with Vue/Svelte/Angular?**
A: No, SAP-020 is React-specific. Wait for future SAPs for other frameworks.

**Q: What about Tailwind CSS?**
A: Styling covered in SAP-024 (React Styling), not SAP-020 (foundation only).

**Q: How do I update Next.js/React versions?**
A: Templates pin to stable versions. Update manually or wait for SAP-020 quarterly update.

---

**End of Awareness Guide**
