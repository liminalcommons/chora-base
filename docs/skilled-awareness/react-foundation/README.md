# SAP-020: React Project Foundation

**SAP ID**: SAP-020
**Version**: 1.0.0
**React Version**: 19.x
**Next.js Version**: 15.5.x
**TypeScript Version**: 5.7.x
**Research Foundation**: RT-019 Series (Q4 2024 - Q1 2025)

---

## Quick Start (5 minutes)

```bash
# Option 1: Next.js 15 App Router (recommended for full-stack)
npx create-next-app@latest my-app --typescript --tailwind --app --no-src-dir --import-alias "@/*"
cd my-app
pnpm install
pnpm dev

# Option 2: Vite + React Router (recommended for SPA)
npm create vite@latest my-app -- --template react-ts
cd my-app
pnpm install
pnpm dev

# Verify setup
curl http://localhost:3000  # Next.js: Port 3000
curl http://localhost:5173  # Vite: Port 5173
```

**Expected output**:
```
✔ Creating Next.js app in /path/to/my-app
✔ Installing dependencies (pnpm)
✔ Initializing project
✔ Success! Created my-app at /path/to/my-app

Starting development server...
  ▲ Next.js 15.5.0
  - Local:        http://localhost:3000
  - Ready in 1.2s
```

---

## What Is It?

SAP-020 provides **production-ready React 19 + Next.js 15 foundations** with TypeScript strict mode, server-first architecture, and modern tooling.

### Purpose

- **React 19 Baseline**: Server Components (RSC), Actions API, `use()` hook, concurrent features
- **Next.js 15 App Router**: File-based routing, Server Components default, streaming SSR
- **TypeScript Strict Mode**: Catch 40% more errors at compile time, eliminate `any` types
- **Server-First Architecture**: Progressive enhancement, optimized for performance
- **Template Ecosystem**: 2 starter templates (Next.js App Router, Vite SPA) with best practices

### How It Works

1. **Initialize** with Next.js 15 (App Router) or Vite 7 (SPA) starter
2. **Configure** TypeScript strict mode, ESLint, Prettier
3. **Structure** feature-based organization with `src/app/` (Next.js) or `src/pages/` (Vite)
4. **Develop** using React 19 patterns (RSC, Actions, `use()` hook)
5. **Build** for production with optimized bundles (<200 KB gzipped baseline)

---

## When to Use

### ✅ Use React Foundation (SAP-020) When

- **New React Project**: Starting from scratch with React 19 + Next.js 15
- **Server-First Architecture**: Need SSR, RSC, or full-stack capabilities (Next.js)
- **SPA Requirements**: Building client-side only application (Vite + React Router)
- **TypeScript Projects**: Strict mode enforcement for production quality
- **Modern Stack**: Want latest React 19 features (Actions, `use()`, ref as prop)
- **Performance Critical**: Optimized bundles, streaming SSR, edge runtime
- **Foundation for Other SAPs**: Base layer for SAP-021 (Testing), SAP-022 (Linting), SAP-023 (State), etc.

### ❌ Don't Use When

- **Legacy React 16/17**: Use upgrade guide first, then adopt SAP-020
- **Class Components**: SAP-020 uses functional components + hooks only
- **JavaScript (no TypeScript)**: SAP-020 requires TypeScript strict mode
- **Custom Bundlers**: SAP-020 uses Next.js or Vite (not Webpack/Parcel)

---

## Key Features

### React 19 Production Features

1. **React Server Components (RSC)**
   - Server-first rendering (default in Next.js 15)
   - Zero client bundle for server components
   - Automatic code splitting

2. **Actions API**
   - Form handling without client-side JavaScript
   - Server Actions with type safety
   - Progressive enhancement

3. **`use()` Hook**
   - Async data fetching in components
   - Suspense integration
   - Streaming support

4. **Ref as Prop**
   - No more `forwardRef` wrapper
   - Direct `ref` prop on custom components
   - Cleaner component APIs

5. **Concurrent Features**
   - Suspense for data fetching
   - `startTransition` for non-urgent updates
   - `useDeferredValue` for expensive computations

### Next.js 15 App Router Features

1. **File-Based Routing**
   - `app/page.tsx` → `/`
   - `app/dashboard/page.tsx` → `/dashboard`
   - `app/blog/[slug]/page.tsx` → `/blog/:slug`

2. **Special Files**
   - `layout.tsx` - Shared UI across routes
   - `loading.tsx` - Instant loading state (Suspense)
   - `error.tsx` - Error handling (Error Boundary)
   - `route.ts` - API endpoint (GET, POST, etc.)

3. **Server Components Default**
   - Components are server-rendered by default
   - Use `'use client'` directive for client components
   - Automatic optimization

4. **Streaming SSR**
   - Progressive page rendering
   - Faster Time to First Byte (TTFB)
   - Improved Core Web Vitals

5. **Edge Runtime**
   - Deploy to edge locations globally
   - Sub-100ms cold starts
   - Optimized for performance

### TypeScript Strict Mode Benefits

- **40% More Compile-Time Errors**: Catch issues before runtime
- **No `any` Types**: Explicit typing for all variables
- **Index Signature Safety**: `obj[key]` requires null check
- **Better IDE Support**: Autocomplete, refactoring, go-to-definition

---

## Quick Reference

### Project Initialization

**Next.js 15 App Router** (full-stack, SSR):
```bash
npx create-next-app@latest my-app \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"
```

**Vite + React Router** (SPA):
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
pnpm add react-router-dom@7
```

### Directory Structure

**Next.js App Router**:
```
my-app/
├── app/
│   ├── layout.tsx              # Root layout (required)
│   ├── page.tsx                # Home page (/)
│   ├── loading.tsx             # Loading UI
│   ├── error.tsx               # Error boundary
│   ├── not-found.tsx           # 404 page
│   ├── dashboard/
│   │   ├── layout.tsx          # Nested layout
│   │   ├── page.tsx            # /dashboard
│   │   └── [id]/page.tsx       # /dashboard/:id
│   └── api/
│       └── users/route.ts      # API endpoint
├── components/
│   ├── ui/                     # Shared UI components
│   └── providers/              # Context providers
├── lib/
│   ├── api.ts                  # API client
│   └── utils.ts                # Utility functions
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── next.config.ts
└── .env.local
```

**Vite SPA**:
```
my-app/
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   ├── router.tsx              # React Router config
│   ├── components/
│   │   └── ui/                 # Shared UI components
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Utility functions
│   ├── features/               # Feature-based organization
│   └── pages/                  # Page components
├── public/                     # Static assets
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### TypeScript Configuration

**tsconfig.json** (strict mode):
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

    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/lib/*": ["src/lib/*"]
    }
  }
}
```

### Component Patterns

**Server Component** (Next.js default):
```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  const data = await fetch('https://api.example.com/data');
  const json = await data.json();

  return (
    <div>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(json, null, 2)}</pre>
    </div>
  );
}
```

**Client Component** (interactive):
```tsx
'use client'

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**Server Action** (form handling):
```tsx
// app/actions.ts
'use server'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  // Save to database
  await db.users.create({ name, email });

  return { success: true };
}

// app/signup/page.tsx
import { createUser } from '../actions';

export default function SignupPage() {
  return (
    <form action={createUser}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

### React 19 Patterns

**`use()` Hook** (async data):
```tsx
import { use } from 'react';

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

**Ref as Prop** (no `forwardRef`):
```tsx
// Before (React 18)
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />;
});

// After (React 19)
function Input({ ref, ...props }: InputProps & { ref?: Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

---

## Integration with Other SAPs

### SAP-021 (React Testing)
- **Link**: Testing infrastructure for React 19 components
- **How**: Vitest + React Testing Library with RSC support
- **Benefit**: Test server components, client components, and Server Actions

### SAP-022 (React Linting)
- **Link**: ESLint 9 + Prettier for code quality
- **How**: React Hooks rules, TypeScript rules, import sorting
- **Benefit**: Consistent code style, catch common errors

### SAP-023 (React State Management)
- **Link**: TanStack Query + Zustand for state
- **How**: Server state (Query), client state (Zustand)
- **Benefit**: Optimized data fetching, global state management

### SAP-024 (React Styling)
- **Link**: Tailwind CSS + shadcn/ui components
- **How**: Utility-first CSS, accessible component library
- **Benefit**: Rapid UI development, consistent design system

### SAP-033 (React Authentication)
- **Link**: NextAuth v5, Clerk, Supabase Auth
- **How**: Secure authentication with session management
- **Benefit**: Production-ready auth in 20 minutes

### SAP-034 (React Database Integration)
- **Link**: Prisma or Drizzle ORM
- **How**: Type-safe database queries with TypeScript inference
- **Benefit**: End-to-end type safety from DB to UI

---

## Success Metrics

### Initial Setup (<5 minutes)
- ✅ **Project Created**: `npx create-next-app` completes successfully
- ✅ **Dependencies Installed**: `pnpm install` finishes without errors
- ✅ **Dev Server Running**: `pnpm dev` starts on http://localhost:3000
- ✅ **TypeScript Compiles**: No errors in `tsconfig.json`

### Development Quality
- ✅ **Strict Mode Enabled**: `"strict": true` in tsconfig.json
- ✅ **No `any` Types**: All variables explicitly typed
- ✅ **ESLint Passes**: `pnpm lint` shows no errors
- ✅ **Build Succeeds**: `pnpm build` completes in <2 minutes

### Performance Targets (Production Build)
- ✅ **Bundle Size**: <200 KB gzipped for baseline app
- ✅ **First Contentful Paint (FCP)**: <1.8s
- ✅ **Largest Contentful Paint (LCP)**: <2.5s
- ✅ **Total Blocking Time (TBT)**: <200ms
- ✅ **Cumulative Layout Shift (CLS)**: <0.1

### Adoption Indicators
- ✅ **Server Components Used**: 80%+ of components are server components
- ✅ **Client Directive**: `'use client'` only when needed (interactivity)
- ✅ **Server Actions**: Forms use Server Actions (no client-side fetch)
- ✅ **TypeScript Coverage**: 100% of files are `.tsx` (not `.jsx`)

---

## Troubleshooting

### Problem 1: "Module not found" errors after creating Next.js app

**Symptom**: `Error: Cannot find module '@/components/...'`

**Cause**: Path aliases not configured in `tsconfig.json`

**Fix**: Verify `tsconfig.json` has path mappings:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Next.js 15**: Use `--import-alias "@/*"` flag when creating app

---

### Problem 2: TypeScript strict mode errors overwhelming

**Symptom**: Hundreds of type errors after enabling `"strict": true`

**Cause**: Existing codebase not written with strict mode

**Fix**: Enable strict mode incrementally:
```json
{
  "compilerOptions": {
    "strict": false,
    "strictNullChecks": true,  // Step 1
    // Add one strict check at a time
  }
}
```

**Recommended Order**:
1. `strictNullChecks` (most valuable)
2. `noImplicitAny`
3. `strictFunctionTypes`
4. `strict: true` (all checks)

---

### Problem 3: "use client" directive needed everywhere

**Symptom**: Many components require `'use client'` directive

**Cause**: Over-reliance on client-side interactivity

**Fix**: Review component tree, move interactivity to leaf components

**Example**:
```tsx
// ❌ BAD: Entire page is client component
'use client'

export default function DashboardPage() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Header />
      <Counter count={count} setCount={setCount} />
      <Footer />
    </div>
  );
}

// ✅ GOOD: Only interactive component is client
export default function DashboardPage() {
  return (
    <div>
      <Header />
      <Counter />  {/* 'use client' inside Counter.tsx */}
      <Footer />
    </div>
  );
}
```

**Benefit**: 80-90% bundle size reduction for static content

---

### Problem 4: Slow development server (HMR takes >5 seconds)

**Symptom**: Changes take 5-10 seconds to reflect in browser

**Cause**: Large dependency tree or inefficient bundling

**Fix (Next.js 15)**:
```ts
// next.config.ts
const nextConfig = {
  experimental: {
    turbo: {
      // Enable Turbopack for 5x faster dev (Next.js 15.1+)
    },
  },
};
```

**Fix (Vite)**:
```ts
// vite.config.ts
export default defineConfig({
  server: {
    hmr: {
      overlay: false,  // Disable error overlay if slow
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom'],  // Pre-bundle heavy deps
  },
});
```

---

### Problem 5: Production build fails with type errors

**Symptom**: `pnpm build` fails but `pnpm dev` works

**Cause**: TypeScript errors ignored in dev mode

**Fix**: Run type check before build:
```bash
pnpm tsc --noEmit  # Check types without emitting files
pnpm build         # Build after types pass
```

**Prevention**: Add pre-build script:
```json
{
  "scripts": {
    "prebuild": "tsc --noEmit",
    "build": "next build"
  }
}
```

---

## Learn More

### Documentation

- **[Capability Charter](capability-charter.md)**: Problem statement, solution design, success criteria
- **[Protocol Spec](protocol-spec.md)**: Complete technical specification (React 19, Next.js 15, TypeScript)
- **[Awareness Guide](awareness-guide.md)**: Detailed workflows, component patterns, examples
- **[Adoption Blueprint](adoption-blueprint.md)**: Step-by-step installation and setup
- **[Ledger](ledger.md)**: Adoption tracking, version history, active deployments

### Official Resources

- **[React 19 Documentation](https://react.dev)**: Official React docs with Server Components guide
- **[Next.js 15 Documentation](https://nextjs.org/docs)**: App Router, Server Actions, deployment
- **[TypeScript Handbook](https://www.typescriptlang.org/docs)**: TypeScript language reference

### Related SAPs

- **[SAP-021 (react-testing)](../react-testing/)**: Vitest + React Testing Library
- **[SAP-022 (react-linting)](../react-linting/)**: ESLint 9 + Prettier
- **[SAP-023 (react-state-management)](../react-state-management/)**: TanStack Query + Zustand
- **[SAP-024 (react-styling)](../react-styling/)**: Tailwind CSS + shadcn/ui
- **[SAP-033 (react-authentication)](../react-authentication/)**: NextAuth v5, Clerk, Supabase
- **[SAP-034 (react-database-integration)](../react-database-integration/)**: Prisma, Drizzle ORM

### Research Foundation

- **RT-019-APP**: Application features and user flows research
- **RT-019-DATA**: Data layer and persistence patterns research
- **RT-019-SCALE**: Global scale and advanced patterns research

---

## Version History

- **1.0.0** (2025-11-09): Initial SAP-020 release
  - React 19 baseline (Server Components, Actions API, `use()` hook, ref as prop)
  - Next.js 15 App Router (file-based routing, streaming SSR, edge runtime)
  - TypeScript 5.7 strict mode (40% more compile-time errors)
  - 2 starter templates (Next.js App Router, Vite SPA)
  - Server-first architecture with progressive enhancement
  - Performance targets (<200 KB baseline, <1.8s FCP, <2.5s LCP)
  - Integration with 6 React SAPs (Testing, Linting, State, Styling, Auth, Database)
  - Research-backed patterns from RT-019 series

---

**Next Steps**:
1. Read [adoption-blueprint.md](adoption-blueprint.md) for installation instructions
2. Initialize project: `npx create-next-app@latest my-app --typescript --tailwind --app`
3. Verify setup: `pnpm dev` and open http://localhost:3000
4. Adopt additional SAPs: SAP-021 (Testing), SAP-022 (Linting), SAP-023 (State)
