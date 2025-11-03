# SAP-020: React Project Foundation - Adoption Blueprint

**SAP ID**: SAP-020
**Version**: 1.0.0
**Last Updated**: 2025-10-31
**Status**: Active

---

## Overview

This blueprint provides step-by-step instructions for adopting the React Project Foundation capability package (SAP-020) to create modern React applications. It covers prerequisites, template selection, installation, and validation.

**Time Estimate**: 45 minutes (first project), 25 minutes (subsequent projects)
**Complexity**: Intermediate (requires JavaScript/TypeScript experience)
**Prerequisites**: Node.js 22.x LTS, pnpm/npm, text editor

---

## Prerequisites

### System Requirements

**Required**:
- Node.js 22.x LTS (download from [nodejs.org](https://nodejs.org/))
- pnpm 10.x (recommended) or npm 10.x
- Text editor or IDE (VS Code recommended)
- Terminal/command line access
- Git (version control)

**Operating Systems**:
- ✅ macOS 14+ (native support)
- ✅ Linux (Ubuntu 22.04+, Debian, Fedora)
- ✅ Windows 11 with WSL2 (recommended over native Windows)

**Disk Space**:
- ~500MB for Node.js + dependencies
- ~50-100MB per React project

### Verify Prerequisites

```bash
# Check Node.js version (must be 22.x)
node --version
# Expected: v22.0.0 or higher

# Check npm version
npm --version
# Expected: 10.0.0 or higher

# Install pnpm (recommended, faster than npm)
npm install -g pnpm@latest

# Check pnpm version
pnpm --version
# Expected: 10.0.0 or higher

# Check Git
git --version
# Expected: 2.30.0 or higher
```

**Troubleshooting**:
- If Node.js is not 22.x: Download from [nodejs.org](https://nodejs.org/) or use [nvm](https://github.com/nvm-sh/nvm)
- If pnpm install fails: Use npm instead (slightly slower but fully compatible)
- On Windows: Use WSL2 for best compatibility

### Knowledge Prerequisites

**Required**:
- JavaScript ES2020+ (const/let, arrow functions, async/await, modules)
- Basic TypeScript (types, interfaces, generics)
- React basics (components, JSX, props, state)
- Command line basics (cd, ls, npm install)

**Helpful but not required**:
- Next.js App Router concepts (Server Components, file-based routing)
- React hooks (useState, useEffect, useContext)
- API integration patterns (fetch, axios)
- Git basics (commit, push, pull)

---

## Installing the SAP

### Quick Install (Future)

**Note**: Automated installation will be available in future versions via SAP-003 integration.

```bash
# Future command (not yet implemented)
python scripts/install-sap.py SAP-020 --source /path/to/chora-base
```

### Part of Sets

This SAP is included in:
- **react-development** - Complete React development stack (SAP-020 through SAP-026)
- **full** - All chora-base SAPs

To install the complete React development set (future):
```bash
# Future command
python scripts/install-sap.py --set react-development --source /path/to/chora-base
```

### Manual Verification

Verify SAP-020 artifacts exist in chora-base:

```bash
# Navigate to chora-base
cd /path/to/chora-base

# Verify 5 core artifacts
ls docs/skilled-awareness/react-foundation/
# Expected:
# - capability-charter.md
# - protocol-spec.md
# - awareness-guide.md
# - adoption-blueprint.md (this file)
# - ledger.md

# Verify templates
ls templates/react/
# Expected:
# - nextjs-15-app-router/
# - vite-react-spa/
# - configs/
# - state-management/
```

---

## Decision Point: Choose Your Framework

Before proceeding, decide which framework fits your needs:

### Option A: Next.js 15 App Router (Recommended for Most Projects)

**Choose if you need**:
- ✅ Server-side rendering (SSR) or static site generation (SSG)
- ✅ SEO optimization (search engines index your content)
- ✅ Full-stack capabilities (API routes, server actions)
- ✅ Image/font optimization out of the box
- ✅ Production-ready architecture

**Skip if**:
- ❌ Building SPA behind authentication (no SEO needed)
- ❌ Want fastest dev server (Vite is faster for hot reload)
- ❌ Need minimal complexity (Vite simpler)

**Time to First Running App**: ~45 minutes

**👉 Go to**: [Option A Installation](#option-a-next-js-15-installation)

---

### Option B: Vite 7 + React Router (SPA Alternative)

**Choose if you need**:
- ✅ Single-page application (SPA) without SSR
- ✅ Fastest dev server (< 100ms cold start)
- ✅ Minimal configuration
- ✅ App behind authentication (no SEO requirements)
- ✅ Simpler deployment (static files only)

**Skip if**:
- ❌ Need SEO (Google, Bing indexing)
- ❌ Need server-side rendering
- ❌ Want API routes in same project

**Time to First Running App**: ~30 minutes

**👉 Go to**: [Option B Installation](#option-b-vite-7-installation)

---

## Option A: Next.js 15 Installation

### Step 1: Copy Template

```bash
# Navigate to where you want to create your project
cd ~/projects  # Or your preferred location

# Copy Next.js template from chora-base
cp -r /path/to/chora-base/templates/react/nextjs-15-app-router ./my-nextjs-app

# Navigate into project
cd my-nextjs-app
```

**Verification**:
```bash
ls -la
# Expected files:
# - package.json
# - tsconfig.json
# - next.config.ts
# - src/app/layout.tsx
# - src/app/page.tsx
# - README.md
```

---

### Step 2: Install Dependencies

```bash
# Install all dependencies (takes 2-4 minutes)
pnpm install

# Or with npm (takes 4-6 minutes)
# npm install
```

**What Gets Installed**:
- Next.js 15.5.x (framework)
- React 19.x (UI library)
- TypeScript 5.7.x (type safety)
- TanStack Query 5.x (server state management)
- Zustand 5.x (client UI state)
- Axios + Zod (API client + validation)

**Verification**:
```bash
# Check if node_modules exists
ls node_modules | head -n 5

# Verify key dependencies
pnpm list next react typescript
# Should show versions matching package.json
```

**Troubleshooting**:
- If install fails with "EACCES": Run `sudo chown -R $USER ~/.npm` (npm) or `sudo chown -R $USER ~/.local/share/pnpm` (pnpm)
- If peer dependency warnings: Safe to ignore (pnpm warns, npm doesn't)
- If out of disk space: Clear npm cache with `npm cache clean --force`

---

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your values
# Use your preferred editor (code, vim, nano)
code .env.local
```

**Required Variables** (edit as needed):
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://user:password@localhost:5432/mydb  # If using database
NEXTAUTH_SECRET=your-secret-key-here  # If using NextAuth.js
```

**Notes**:
- `NEXT_PUBLIC_*` variables are exposed to the browser
- Non-prefixed variables are server-only (secure)
- `.env.local` is git-ignored (safe for secrets)

---

### Step 4: Customize Project

```bash
# Update package.json with your project name
code package.json
# Change "name": "my-nextjs-app" to your app name

# Update app metadata
code src/app/layout.tsx
```

**In src/app/layout.tsx**, update metadata:
```typescript
export const metadata: Metadata = {
  title: 'Your App Name',
  description: 'Your app description',
}
```

---

### Step 5: Start Development Server

```bash
# Start Next.js dev server with Turbopack (fast!)
pnpm dev --turbo

# Or without Turbopack
# pnpm dev

# Server will start at http://localhost:3000
```

**Expected Output**:
```
  ▲ Next.js 15.5.0
  - Local:        http://localhost:3000
  - Turbopack:    enabled

 ✓ Ready in 1.2s
```

**Verification**:
1. Open browser to [http://localhost:3000](http://localhost:3000)
2. You should see the Next.js welcome page
3. Hot reload: Edit `src/app/page.tsx`, see changes instantly (<100ms)

**Troubleshooting**:
- Port 3000 in use: Change port with `pnpm dev --turbo -p 3001`
- TypeScript errors: Run `pnpm type-check` to see full error list
- Build errors: Delete `.next/` folder and restart: `rm -rf .next && pnpm dev`

---

### Step 6: Validate Installation

Run validation checks:

```bash
# 1. Type checking (must pass)
pnpm type-check
# Expected: "Found 0 errors"

# 2. Build production bundle (must succeed)
pnpm build
# Expected: "Compiled successfully"

# 3. Run production build locally
pnpm start
# Visit http://localhost:3000, should work

# 4. Check bundle size
cat .next/static/chunks/*.js | wc -c
# Expected: < 300KB total (without your code)
```

**All validations should pass**. If any fail:
- Type errors: Fix in code, re-run `pnpm type-check`
- Build errors: Check `next.config.ts`, ensure all imports resolve
- Bundle too large: Normal for first build, optimize later with SAP-025

---

### Step 7: Create First Feature

Create a simple "users" feature to validate architecture:

```bash
# Create feature structure
mkdir -p src/features/users/{components,hooks,services,types}

# Create types
cat > src/features/users/types/user.types.ts << 'EOF'
import { z } from 'zod'

export const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
})

export type User = z.infer<typeof UserSchema>
EOF

# Create service
cat > src/features/users/services/userService.ts << 'EOF'
import axios from 'axios'
import { z } from 'zod'
import { UserSchema, type User } from '../types/user.types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api'

export const userService = {
  async list(): Promise<User[]> {
    const { data } = await axios.get(`${API_BASE}/users`)
    return z.array(UserSchema).parse(data)
  },
}
EOF

# Create hook
cat > src/features/users/hooks/useUsers.ts << 'EOF'
import { useQuery } from '@tanstack/react-query'
import { userService } from '../services/userService'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: userService.list,
  })
}
EOF

# Create component
cat > src/features/users/components/UserList.tsx << 'EOF'
'use client'

import { useUsers } from '../hooks/useUsers'

export function UserList() {
  const { data: users, isLoading, error } = useUsers()

  if (isLoading) return <div>Loading users...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul className="space-y-2">
      {users?.map(user => (
        <li key={user.id}>
          {user.name} ({user.email})
        </li>
      ))}
    </ul>
  )
}
EOF

# Create public API
cat > src/features/users/index.ts << 'EOF'
export { UserList } from './components/UserList'
export { useUsers } from './hooks/useUsers'
export type { User } from './types/user.types'
EOF
```

**Use in page**:
```bash
cat > src/app/users/page.tsx << 'EOF'
import { UserList } from '@/features/users'

export default function UsersPage() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      <UserList />
    </main>
  )
}
EOF
```

**Test it**:
1. Visit [http://localhost:3000/users](http://localhost:3000/users)
2. Should see "Loading users..." then error (no API yet - normal)
3. Feature structure validated ✅

---

### Step 8: Next Steps

**Your Next.js 15 project is ready!** 🎉

**Recommended next steps**:
1. **Add testing** - Install SAP-021 (React Testing & Quality)
2. **Add linting** - Install SAP-022 (React Linting & Formatting)
3. **Add styling** - Install SAP-024 (React Styling with Tailwind)
4. **Build features** - Follow the users feature pattern above

**Resources**:
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [SAP-020 Protocol Spec](./protocol-spec.md) - Architecture patterns
- [SAP-020 Awareness Guide](./awareness-guide.md) - Decision trees, common pitfalls

**Time taken**: ~45 minutes ⏱️

---

## Option B: Vite 7 Installation

### Step 1: Copy Template

```bash
# Navigate to where you want to create your project
cd ~/projects  # Or your preferred location

# Copy Vite template from chora-base
cp -r /path/to/chora-base/templates/react/vite-react-spa ./my-vite-app

# Navigate into project
cd my-vite-app
```

**Verification**:
```bash
ls -la
# Expected files:
# - package.json
# - tsconfig.json
# - vite.config.ts
# - index.html
# - src/main.tsx
# - src/App.tsx
# - README.md
```

---

### Step 2: Install Dependencies

```bash
# Install all dependencies (takes 1-3 minutes, faster than Next.js)
pnpm install

# Or with npm
# npm install
```

**What Gets Installed**:
- Vite 7.x (build tool)
- React 19.x (UI library)
- React Router v6 (client-side routing)
- TypeScript 5.7.x (type safety)
- TanStack Query 5.x (server state)
- Zustand 5.x (client UI state)
- Axios + Zod (API client + validation)

**Verification**:
```bash
pnpm list vite react typescript
# Should show versions matching package.json
```

---

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your values
code .env
```

**Required Variables**:
```env
# .env
VITE_API_URL=http://localhost:3000/api
```

**Notes**:
- Vite uses `VITE_*` prefix for browser-exposed variables (like `NEXT_PUBLIC_*`)
- `.env` is git-ignored (safe for local secrets)
- Use `.env.production` for production-specific values

---

### Step 4: Customize Project

```bash
# Update package.json with your project name
code package.json
# Change "name": "my-vite-app" to your app name

# Update app title
code index.html
```

**In index.html**, update title:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Your App Name</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

### Step 5: Start Development Server

```bash
# Start Vite dev server (extremely fast!)
pnpm dev

# Server will start at http://localhost:5173
```

**Expected Output**:
```
  VITE v7.1.0  ready in 245 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Verification**:
1. Open browser to [http://localhost:5173](http://localhost:5173)
2. You should see the Vite + React welcome page
3. Hot reload: Edit `src/App.tsx`, see changes instantly (10-50ms, ultra fast!)

**Troubleshooting**:
- Port 5173 in use: Change port in `vite.config.ts` or use `pnpm dev --port 3000`
- Module not found: Clear Vite cache with `rm -rf node_modules/.vite && pnpm dev`

---

### Step 6: Validate Installation

```bash
# 1. Type checking (must pass)
pnpm type-check
# Expected: "Found 0 errors"

# 2. Build production bundle (must succeed)
pnpm build
# Expected: "built in X ms"

# 3. Preview production build
pnpm preview
# Visit http://localhost:4173, should work

# 4. Check bundle size
ls -lh dist/assets/*.js
# Expected: Main bundle < 150KB (without your code)
```

---

### Step 7: Create First Feature

```bash
# Create feature structure
mkdir -p src/features/users/{components,hooks,services,types}

# Create types (same as Next.js example)
cat > src/features/users/types/user.types.ts << 'EOF'
import { z } from 'zod'

export const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
})

export type User = z.infer<typeof UserSchema>
EOF

# Create service
cat > src/features/users/services/userService.ts << 'EOF'
import axios from 'axios'
import { z } from 'zod'
import { UserSchema, type User } from '../types/user.types'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

export const userService = {
  async list(): Promise<User[]> {
    const { data } = await axios.get(`${API_BASE}/users`)
    return z.array(UserSchema).parse(data)
  },
}
EOF

# Create hook (same as Next.js)
cat > src/features/users/hooks/useUsers.ts << 'EOF'
import { useQuery } from '@tanstack/react-query'
import { userService } from '../services/userService'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: userService.list,
  })
}
EOF

# Create component (same as Next.js, no 'use client' needed)
cat > src/features/users/components/UserList.tsx << 'EOF'
import { useUsers } from '../hooks/useUsers'

export function UserList() {
  const { data: users, isLoading, error } = useUsers()

  if (isLoading) return <div>Loading users...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>
          {user.name} ({user.email})
        </li>
      ))}
    </ul>
  )
}
EOF

# Create public API
cat > src/features/users/index.ts << 'EOF'
export { UserList } from './components/UserList'
export { useUsers } from './hooks/useUsers'
export type { User } from './types/user.types'
EOF
```

**Add route**:
```typescript
// src/router.tsx
import { createBrowserRouter } from 'react-router-dom'
import { UserList } from '@/features/users'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'users', element: <UserList /> },  // Add this
    ],
  },
])
```

**Test it**:
1. Visit [http://localhost:5173/users](http://localhost:5173/users)
2. Feature structure validated ✅

---

### Step 8: Next Steps

**Your Vite 7 project is ready!** 🎉

**Recommended next steps**:
1. **Add testing** - Install SAP-021 (React Testing & Quality)
2. **Add linting** - Install SAP-022 (React Linting & Formatting)
3. **Add styling** - Install SAP-024 (React Styling with Tailwind)
4. **Configure routing** - Expand `src/router.tsx` with more routes

**Resources**:
- [Vite Documentation](https://vite.dev)
- [React Router v6 Docs](https://reactrouter.com/)
- [SAP-020 Protocol Spec](./protocol-spec.md)

**Time taken**: ~30 minutes ⏱️

---

## Validation Checklist

After completing installation, verify all requirements:

### ✅ Required Validations

- [ ] **TypeScript compiles**: `pnpm type-check` shows 0 errors
- [ ] **Build succeeds**: `pnpm build` completes without errors
- [ ] **Dev server runs**: `pnpm dev` starts successfully
- [ ] **Hot reload works**: Edit file, see change in browser <1s
- [ ] **Path aliases work**: Import with `@/` works (e.g., `import { api } from '@/lib/api'`)
- [ ] **Environment variables load**: `process.env.NEXT_PUBLIC_*` or `import.meta.env.VITE_*` accessible

### ✅ Optional Validations

- [ ] **Feature structure works**: Created users feature, no errors
- [ ] **Type safety enforced**: TypeScript catches errors (try `const x: number = 'string'`)
- [ ] **API client works**: Axios + Zod validation in place
- [ ] **State management ready**: TanStack Query + Zustand available

---

## Troubleshooting

### Issue: "Cannot find module '@/...'"

**Cause**: TypeScript path aliases not configured correctly.

**Solution**:
```bash
# Verify tsconfig.json has:
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}

# Restart dev server
pnpm dev
```

---

### Issue: "Error: listen EADDRINUSE: address already in use"

**Cause**: Port 3000 (Next.js) or 5173 (Vite) already in use.

**Solution**:
```bash
# Option 1: Kill process on port
# macOS/Linux:
lsof -ti:3000 | xargs kill -9  # Next.js
lsof -ti:5173 | xargs kill -9  # Vite

# Option 2: Use different port
pnpm dev -p 3001  # Next.js
pnpm dev --port 3001  # Vite
```

---

### Issue: "Type error: Property 'X' does not exist on type 'Y'"

**Cause**: TypeScript strict mode catches type errors.

**Solution** (in order of preference):
1. **Add proper types**: Define interface/type for Y
2. **Use type guard**: Check if property exists before accessing
3. **Use optional chaining**: `obj?.property` instead of `obj.property`
4. **Last resort**: Use type assertion `as` (avoid if possible)

```typescript
// ❌ BAD
const name = user.name  // Error if user might not have name

// ✅ GOOD
const name = user?.name  // Safe, returns undefined if no name

// ✅ BETTER
interface User {
  name: string  // Guarantee name exists
}
const user: User = { name: 'Alice' }
const name = user.name  // No error, type-safe
```

---

### Issue: "Failed to fetch" in browser console

**Cause**: API endpoint doesn't exist or CORS issue.

**Solution**:
1. **Check API URL**: Verify `NEXT_PUBLIC_API_URL` / `VITE_API_URL` is correct
2. **Mock data** for development:
```typescript
// lib/api.ts
export const api = {
  users: {
    list: async (): Promise<User[]> => {
      // Mock data for now
      return [
        { id: '1', name: 'Alice', email: 'alice@example.com' },
        { id: '2', name: 'Bob', email: 'bob@example.com' },
      ]
    },
  },
}
```
3. **Install SAP-021** for MSW (Mock Service Worker) to intercept API calls

---

### Issue: "pnpm install" fails with permission errors

**Cause**: No permission to write to global pnpm directory.

**Solution**:
```bash
# Option 1: Fix pnpm permissions
sudo chown -R $USER ~/.local/share/pnpm

# Option 2: Use npm instead
npm install
```

---

## Ledger Entry

After successful installation, record in ledger:

```bash
# Add entry to SAP-020 ledger
echo "$(date +%Y-%m-%d) | Your Name/Team | 1.0.0 | Initial installation (Next.js/Vite)" >> docs/skilled-awareness/react-foundation/ledger.md
```

See [ledger.md](./ledger.md) for adoption tracking.

---

## Next SAPs to Install

After SAP-020, install complementary React SAPs in order:

### Priority 1 (Recommended)
1. **SAP-021** (React Testing & Quality) - Vitest + React Testing Library
2. **SAP-022** (React Linting & Formatting) - ESLint 9 + Prettier

### Priority 2 (High Value)
3. **SAP-024** (React Styling) - Tailwind CSS v4 + shadcn/ui
4. **SAP-023** (React State Management) - Advanced state patterns

### Priority 3 (Production Readiness)
5. **SAP-025** (React Performance) - Core Web Vitals optimization
6. **SAP-026** (React Accessibility) - WCAG 2.2 compliance

**Complete React Development Set**:
```bash
# Future command (installs SAP-020 through SAP-026)
python scripts/install-sap.py --set react-development
```

---

## Support & Resources

### Documentation

- [SAP-020 Capability Charter](./capability-charter.md) - Business value, scope
- [SAP-020 Protocol Spec](./protocol-spec.md) - Technical architecture
- [SAP-020 Awareness Guide](./awareness-guide.md) - Decision trees, pitfalls
- [SAP-020 Ledger](./ledger.md) - Adoption tracking

### External Resources

- [Next.js 15 Documentation](https://nextjs.org/docs)
- [Vite Documentation](https://vite.dev)
- [React 19 Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TanStack Query Docs](https://tanstack.com/query/latest)

### Community

- [chora-base GitHub Discussions](https://github.com/liminalcommons/chora-base/discussions)
- [React Discord](https://discord.gg/react)
- [Next.js Discord](https://nextjs.org/discord)

### Reporting Issues

If you encounter issues with SAP-020:
1. Check [Troubleshooting](#troubleshooting) section above
2. Search existing [GitHub Issues](https://github.com/liminalcommons/chora-base/issues)
3. Open new issue with "SAP-020:" prefix

---

## Appendix: Template Customization

### Customizing Next.js Template

After installation, you can customize:

**1. Update Next.js Config** (`next.config.ts`):
```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Customize as needed
  images: {
    domains: ['your-cdn.com'],  // Allow external images
  },
  experimental: {
    serverActions: true,  // Enable Server Actions (React 19)
  },
}

export default nextConfig
```

**2. Add Middleware** (`src/middleware.ts`):
```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add custom logic (auth, redirects, etc.)
  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*',  // Protect dashboard routes
}
```

### Customizing Vite Template

**1. Update Vite Config** (`vite.config.ts`):
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // Change default port
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Proxy API calls
        changeOrigin: true,
      },
    },
  },
})
```

---

**End of Adoption Blueprint**
