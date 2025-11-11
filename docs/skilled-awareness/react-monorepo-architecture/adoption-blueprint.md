# SAP-040: React Monorepo Architecture - Adoption Blueprint

**SAP ID**: SAP-040
**Name**: react-monorepo-architecture
**Version**: 1.0.0
**Status**: pilot
**Last Updated**: 2025-11-09

---

## Overview

This guide provides step-by-step instructions for adopting SAP-040 (React Monorepo Architecture) in your project. Choose from **three options**:

- **Option A: Turborepo** (20 min) - Fastest, simple, Vercel-backed, free remote cache
- **Option B: Nx** (25 min) - Powerful, enterprise-grade, code generation
- **Option C: pnpm workspaces** (15 min) - Baseline, lightweight, no orchestration

**Total estimated time**: 50 minutes (including tool selection)

---

## Prerequisites

### Required Tools

- **Node.js**: 20.0.0+ (LTS recommended)
- **pnpm**: 9.0.0+ (recommended package manager)
- **Git**: 2.40.0+ (for affected detection)

**Check versions**:
```bash
node --version    # Should be 20.0.0+
pnpm --version    # Should be 9.0.0+
git --version     # Should be 2.40.0+
```

**Install pnpm** (if needed):
```bash
npm install -g pnpm@latest
```

---

### Existing Project Structure

This guide assumes you're either:
1. Starting a new monorepo from scratch
2. Migrating existing apps to a monorepo

**Example starting point**:
```
web-app/          # Existing Next.js app (separate repo)
mobile-app/       # Existing React Native app (separate repo)
```

**Target structure**:
```
my-monorepo/
├── apps/
│   ├── web/      # Migrated Next.js app
│   └── mobile/   # Migrated React Native app
└── packages/
    ├── ui/       # Shared UI components
    └── utils/    # Shared utilities
```

---

## Phase 1: Tool Selection (5 minutes)

### Decision Matrix

Use this decision tree to select the right tool:

```
Q1: Do you need code generation (nx generate @nx/react:component)?
├─ YES → Nx (Option B)
└─ NO  → Continue to Q2

Q2: Do you have 100+ packages?
├─ YES → Nx (Option B)
└─ NO  → Continue to Q3

Q3: Do you need remote caching?
├─ YES → Turborepo (Option A)
└─ NO  → Continue to Q4

Q4: Do you need task orchestration (build pipelines)?
├─ YES → Turborepo (Option A)
└─ NO  → pnpm workspaces (Option C)

DEFAULT: Turborepo (Option A) - 80% of use cases
```

---

### Comparison Table

| Criteria | Turborepo (A) | Nx (B) | pnpm workspaces (C) |
|----------|---------------|--------|---------------------|
| **Setup Time** | 20 min | 25 min | 15 min |
| **Learning Curve** | Low | High | Very Low |
| **Remote Cache** | ✅ Free (Vercel) | ✅ 500h/mo free | ❌ No |
| **Code Generation** | ❌ No | ✅ Yes | ❌ No |
| **Build Speed** | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| **Affected Detection** | ✅ Good | ✅ Excellent | ❌ No |
| **Best For** | 2-50 packages, Next.js | 50-500+ packages | 2-5 packages |

---

### Selection Checklist

Choose **Turborepo (Option A)** if:
- ✅ Building Next.js apps
- ✅ Want fast builds with minimal config
- ✅ Need free remote caching
- ✅ Team is 2-50 developers
- ✅ Have 2-50 packages

Choose **Nx (Option B)** if:
- ✅ Need code generation (standardized component creation)
- ✅ Have 50-500+ packages
- ✅ Enterprise organization (multiple teams)
- ✅ Want advanced features (module boundaries, constraints)
- ✅ Need dependency graph visualization

Choose **pnpm workspaces (Option C)** if:
- ✅ Have 2-5 packages
- ✅ No need for orchestration or caching
- ✅ Want minimal tooling
- ✅ Just need baseline linking

**Continue to your selected option**:
- [Option A: Turborepo](#option-a-turborepo-20-min)
- [Option B: Nx](#option-b-nx-25-min)
- [Option C: pnpm workspaces](#option-c-pnpm-workspaces-15-min)

---

<a id="option-a-turborepo-20-min"></a>
## Option A: Turborepo (20 min)

**Target time**: 20 minutes
**Difficulty**: Easy
**Best for**: Next.js, Vercel, fast builds

---

### Step A1: Create Monorepo Structure (2 min)

```bash
# Create root directory
mkdir my-monorepo
cd my-monorepo

# Initialize Git
git init

# Create directory structure
mkdir -p apps/web apps/admin
mkdir -p packages/ui/src packages/utils/src packages/config

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules
.turbo
.next
dist
build
.env.local
.DS_Store
EOF
```

---

### Step A2: Create Root Configuration (3 min)

**Create package.json**:
```bash
cat > package.json << 'EOF'
{
  "name": "my-monorepo",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "clean": "turbo run clean"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.5.0"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=9.0.0"
  }
}
EOF
```

**Create pnpm-workspace.yaml**:
```bash
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'apps/*'
  - 'packages/*'
EOF
```

**Create turbo.json**:
```bash
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "remoteCache": {
    "enabled": true,
    "signature": true
  },
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "build/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "lint": {
      "outputs": [],
      "cache": true
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    }
  },
  "globalDependencies": [
    ".env",
    "tsconfig.json"
  ]
}
EOF
```

---

### Step A3: Create Shared UI Package (5 min)

**Create package.json**:
```bash
cat > packages/ui/package.json << 'EOF'
{
  "name": "@acme/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "lint": "eslint src --ext .ts,.tsx",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "eslint": "^8.57.0",
    "typescript": "^5.5.0"
  }
}
EOF
```

**Create Button component**:
```bash
cat > packages/ui/src/button.tsx << 'EOF'
import * as React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  children: React.ReactNode;
}

export function Button({
  variant = 'default',
  children,
  className,
  ...props
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded font-medium transition-colors';
  const variantStyles = {
    default: 'bg-blue-600 text-white hover:bg-blue-700',
    outline: 'border border-gray-300 hover:bg-gray-100',
    ghost: 'hover:bg-gray-100',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className || ''}`}
      {...props}
    >
      {children}
    </button>
  );
}
EOF
```

**Create barrel export**:
```bash
cat > packages/ui/src/index.ts << 'EOF'
export { Button, type ButtonProps } from './button';
EOF
```

**Create tsconfig.json**:
```bash
cat > packages/ui/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
EOF
```

---

### Step A4: Create Shared Utils Package (3 min)

**Create package.json**:
```bash
cat > packages/utils/package.json << 'EOF'
{
  "name": "@acme/utils",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "lint": "eslint src --ext .ts",
    "clean": "rm -rf dist"
  },
  "devDependencies": {
    "eslint": "^8.57.0",
    "typescript": "^5.5.0"
  }
}
EOF
```

**Create cn utility**:
```bash
cat > packages/utils/src/cn.ts << 'EOF'
/**
 * Combines class names, filtering out falsy values
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
EOF
```

**Create formatDate utility**:
```bash
cat > packages/utils/src/format-date.ts << 'EOF'
/**
 * Formats a date to YYYY-MM-DD
 */
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}
EOF
```

**Create barrel export**:
```bash
cat > packages/utils/src/index.ts << 'EOF'
export { cn } from './cn';
export { formatDate } from './format-date';
EOF
```

**Create tsconfig.json**:
```bash
cat > packages/utils/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
EOF
```

---

### Step A5: Create Next.js Web App (5 min)

```bash
# Create Next.js app
cd apps/web
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Update package.json to use workspace protocol
cat > package.json << 'EOF'
{
  "name": "@acme/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "clean": "rm -rf .next"
  },
  "dependencies": {
    "@acme/ui": "workspace:*",
    "@acme/utils": "workspace:*",
    "next": "^15.0.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.20",
    "eslint": "^8.57.0",
    "eslint-config-next": "^15.0.0",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.5.0"
  }
}
EOF

# Update next.config.ts to transpile packages
cat > next.config.ts << 'EOF'
import type { NextConfig } from 'next';

const config: NextConfig = {
  transpilePackages: ['@acme/ui', '@acme/utils'],
};

export default config;
EOF

# Update app/page.tsx
cat > app/page.tsx << 'EOF'
import { Button } from '@acme/ui';
import { cn, formatDate } from '@acme/utils';

export default function HomePage() {
  return (
    <main className={cn('flex', 'min-h-screen', 'items-center', 'justify-center', 'p-24')}>
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">Web App</h1>
        <p className="text-gray-600">Built with Turborepo + Next.js 15</p>
        <p className="text-sm text-gray-500">{formatDate(new Date())}</p>
        <div className="flex gap-2 justify-center">
          <Button variant="default">Default Button</Button>
          <Button variant="outline">Outline Button</Button>
          <Button variant="ghost">Ghost Button</Button>
        </div>
      </div>
    </main>
  );
}
EOF

cd ../..
```

---

### Step A6: Install Dependencies & Build (2 min)

```bash
# Install all dependencies
pnpm install

# Build all packages
turbo run build

# Output:
# @acme/ui:build: cached (no build script)
# @acme/utils:build: cached (no build script)
# @acme/web:build: executing
# Build succeeded
```

**Expected output**:
```
• Packages in scope: @acme/web, @acme/ui, @acme/utils
• Running build in 3 packages
@acme/ui:build: cache miss, executing
@acme/utils:build: cache miss, executing
@acme/web:build: cache miss, executing
```

---

### Step A7: Setup Remote Caching (Optional, 5 min)

**Login to Vercel**:
```bash
npx turbo login
# Opens browser, authenticate with Vercel account
```

**Link to Vercel project**:
```bash
npx turbo link
# Select team + project
# Creates .turbo/ directory with config
```

**Add to .env (gitignored)**:
```bash
cat > .env << 'EOF'
TURBO_TOKEN="your-token-from-turbo-link"
TURBO_TEAM="your-team-id-from-turbo-link"
EOF
```

**Test remote cache**:
```bash
# First run: builds from scratch, uploads to cache
turbo run build
# Output: "cache miss, executing build"
# Time: ~2 minutes

# Clean local cache
rm -rf .turbo

# Second run: downloads from remote cache
turbo run build
# Output: "cache hit, replaying output"
# Time: ~5 seconds (96% faster!)
```

---

### Step A8: Verification (2 min)

**Run development servers**:
```bash
# Run all dev servers
turbo run dev

# Or run specific app
turbo run dev --filter=@acme/web
# Visit http://localhost:3000
```

**Test build**:
```bash
# Build all packages
turbo run build

# Verify output
ls apps/web/.next  # Should exist
```

**Test hot reload**:
```bash
# Terminal 1: Run dev
turbo run dev --filter=@acme/web

# Terminal 2: Edit Button component
# Edit packages/ui/src/button.tsx
# Save file
# Browser should hot reload automatically (thanks to transpilePackages)
```

---

### Step A9: Setup CI/CD (Optional, 5 min)

**Create GitHub Actions workflow**:
```bash
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for affected detection

      - uses: pnpm/action-setup@v2
        with:
          version: 9.0.0

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Build
        run: turbo run build
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

      - name: Test
        run: turbo run test
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

      - name: Lint
        run: turbo run lint
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}
EOF
```

**Add secrets to GitHub**:
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add `TURBO_TOKEN` (from `.env`)
3. Add `TURBO_TEAM` (from `.env`)

---

### Option A Complete!

**What you built**:
- ✅ Monorepo with Turborepo + pnpm
- ✅ 2 shared packages (@acme/ui, @acme/utils)
- ✅ 1 Next.js app (@acme/web)
- ✅ Remote caching (Vercel Remote Cache)
- ✅ CI/CD pipeline (GitHub Actions)

**Performance**:
- Build time: 2 min (first run) → 5s (cached)
- Hot reload: Works across packages (transpilePackages)
- Cache hit rate: 90-95%

**Next steps**:
- Add more apps (admin, mobile, docs)
- Add more packages (config, tsconfig, api)
- Setup changesets for versioning
- See [protocol-spec.md](./protocol-spec.md) for advanced patterns

---

<a id="option-b-nx-25-min"></a>
## Option B: Nx (25 min)

**Target time**: 25 minutes
**Difficulty**: Medium
**Best for**: Enterprise, 100+ packages, code generation

---

### Step B1: Create Nx Workspace (3 min)

```bash
# Create Nx workspace with Next.js preset
npx create-nx-workspace@latest my-monorepo \
  --preset=next \
  --appName=web \
  --style=css \
  --packageManager=pnpm

cd my-monorepo
```

**Answer prompts**:
- Package manager: `pnpm`
- App name: `web`
- Styling: `Tailwind`
- Test runner: `None` (or Vitest)
- CI/CD: `github` (if using GitHub)

---

### Step B2: Create Shared UI Library (5 min)

```bash
# Generate React library
nx generate @nx/react:library ui --directory=packages/ui --importPath=@acme/ui

# Generate Button component
nx generate @nx/react:component button --project=ui --export
```

**Update Button component**:
```bash
cat > packages/ui/src/lib/button/button.tsx << 'EOF'
import * as React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  children: React.ReactNode;
}

export function Button({
  variant = 'default',
  children,
  className,
  ...props
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded font-medium transition-colors';
  const variantStyles = {
    default: 'bg-blue-600 text-white hover:bg-blue-700',
    outline: 'border border-gray-300 hover:bg-gray-100',
    ghost: 'hover:bg-gray-100',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className || ''}`}
      {...props}
    >
      {children}
    </button>
  );
}
EOF
```

**Update barrel export**:
```bash
cat > packages/ui/src/index.ts << 'EOF'
export { Button, type ButtonProps } from './lib/button/button';
EOF
```

---

### Step B3: Create Shared Utils Library (3 min)

```bash
# Generate utils library
nx generate @nx/js:library utils --directory=packages/utils --importPath=@acme/utils
```

**Create cn utility**:
```bash
cat > packages/utils/src/lib/cn.ts << 'EOF'
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
EOF
```

**Create formatDate utility**:
```bash
cat > packages/utils/src/lib/format-date.ts << 'EOF'
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}
EOF
```

**Update barrel export**:
```bash
cat > packages/utils/src/index.ts << 'EOF'
export { cn } from './lib/cn';
export { formatDate } from './lib/format-date';
EOF
```

---

### Step B4: Update Web App (3 min)

**Update app/page.tsx**:
```bash
cat > apps/web/app/page.tsx << 'EOF'
import { Button } from '@acme/ui';
import { cn, formatDate } from '@acme/utils';

export default function HomePage() {
  return (
    <main className={cn('flex', 'min-h-screen', 'items-center', 'justify-center', 'p-24')}>
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">Web App</h1>
        <p className="text-gray-600">Built with Nx + Next.js 15</p>
        <p className="text-sm text-gray-500">{formatDate(new Date())}</p>
        <div className="flex gap-2 justify-center">
          <Button variant="default">Default Button</Button>
          <Button variant="outline">Outline Button</Button>
          <Button variant="ghost">Ghost Button</Button>
        </div>
      </div>
    </main>
  );
}
EOF
```

---

### Step B5: Configure Nx (3 min)

**Update nx.json**:
```bash
cat > nx.json << 'EOF'
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "test": {
      "cache": true
    },
    "lint": {
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json"
    ]
  },
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  }
}
EOF
```

---

### Step B6: Setup Nx Cloud (Optional, 5 min)

```bash
# Connect to Nx Cloud (500 compute hours/month free)
nx connect-to-nx-cloud

# Follow prompts:
# - Create new workspace or connect to existing
# - Enable distributed task execution
```

**Test remote cache**:
```bash
# First run: builds from scratch, uploads to cache
nx build web
# Time: ~2 minutes

# Clean local cache
rm -rf .nx

# Second run: downloads from Nx Cloud
nx build web
# Output: "cache hit, replaying output"
# Time: ~5 seconds (96% faster!)
```

---

### Step B7: Verification (3 min)

**Run development server**:
```bash
nx serve web
# Visit http://localhost:4200
```

**Build all projects**:
```bash
nx run-many --target=build --all
```

**Test affected builds**:
```bash
# Make a change in packages/ui
echo "// test" >> packages/ui/src/index.ts

# Build only affected projects
nx affected:build --base=HEAD~1
# Only builds web (depends on ui)
```

**View dependency graph**:
```bash
nx graph
# Opens interactive graph in browser
```

---

### Step B8: Setup CI/CD (Optional, 5 min)

**Create GitHub Actions workflow**:
```bash
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
        with:
          version: 9.0.0

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Build affected
        run: nx affected:build --base=origin/main
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

      - name: Test affected
        run: nx affected:test --base=origin/main
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

      - name: Lint affected
        run: nx affected:lint --base=origin/main
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
EOF
```

**Add NX_CLOUD_ACCESS_TOKEN to GitHub Secrets**:
1. Go to GitHub repo → Settings → Secrets
2. Add `NX_CLOUD_ACCESS_TOKEN` (from `nx.json`)

---

### Option B Complete!

**What you built**:
- ✅ Monorepo with Nx + pnpm
- ✅ 2 shared libraries (@acme/ui, @acme/utils)
- ✅ 1 Next.js app (@acme/web)
- ✅ Nx Cloud (remote caching + distributed execution)
- ✅ CI/CD pipeline (GitHub Actions)

**Performance**:
- Build time: 2 min (first run) → 5s (cached)
- Code generation: `nx generate @nx/react:component`
- Dependency graph: `nx graph`
- Cache hit rate: 85-90%

**Next steps**:
- Generate more apps: `nx generate @nx/next:app admin`
- Generate components: `nx generate @nx/react:component`
- Setup module boundaries (Nx constraints)
- See [protocol-spec.md](./protocol-spec.md) for advanced patterns

---

<a id="option-c-pnpm-workspaces-15-min"></a>
## Option C: pnpm workspaces (15 min)

**Target time**: 15 minutes
**Difficulty**: Very Easy
**Best for**: 2-5 packages, baseline linking, no orchestration

---

### Step C1: Create Monorepo Structure (2 min)

```bash
# Create root directory
mkdir my-monorepo
cd my-monorepo

# Initialize Git
git init

# Create directory structure
mkdir -p apps/web packages/ui/src packages/utils/src

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules
.next
dist
.DS_Store
EOF
```

---

### Step C2: Create Root Configuration (2 min)

**Create package.json**:
```bash
cat > package.json << 'EOF'
{
  "name": "my-monorepo",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "pnpm -r build",
    "dev": "pnpm --parallel -r dev",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=9.0.0"
  }
}
EOF
```

**Create pnpm-workspace.yaml**:
```bash
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'apps/*'
  - 'packages/*'
EOF
```

---

### Step C3: Create Shared Packages (3 min)

**UI package**:
```bash
cat > packages/ui/package.json << 'EOF'
{
  "name": "@acme/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
EOF

cat > packages/ui/src/button.tsx << 'EOF'
import * as React from 'react';

export function Button({ children }: { children: React.ReactNode }) {
  return <button>{children}</button>;
}
EOF

cat > packages/ui/src/index.ts << 'EOF'
export { Button } from './button';
EOF
```

**Utils package**:
```bash
cat > packages/utils/package.json << 'EOF'
{
  "name": "@acme/utils",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts"
}
EOF

cat > packages/utils/src/cn.ts << 'EOF'
export function cn(...classes: string[]): string {
  return classes.filter(Boolean).join(' ');
}
EOF

cat > packages/utils/src/index.ts << 'EOF'
export { cn } from './cn';
EOF
```

---

### Step C4: Create Next.js App (5 min)

```bash
cd apps/web
npx create-next-app@latest . --typescript --tailwind

# Update package.json
cat > package.json << 'EOF'
{
  "name": "@acme/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@acme/ui": "workspace:*",
    "@acme/utils": "workspace:*",
    "next": "^15.0.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
EOF

# Update next.config.ts
cat > next.config.ts << 'EOF'
export default {
  transpilePackages: ['@acme/ui', '@acme/utils'],
};
EOF

cd ../..
```

---

### Step C5: Install Dependencies (2 min)

```bash
pnpm install
```

---

### Step C6: Verification (1 min)

**Run dev server**:
```bash
pnpm --filter @acme/web dev
# Visit http://localhost:3000
```

**Build**:
```bash
pnpm -r build
```

---

### Option C Complete!

**What you built**:
- ✅ Monorepo with pnpm workspaces
- ✅ 2 shared packages (@acme/ui, @acme/utils)
- ✅ 1 Next.js app (@acme/web)
- ✅ Baseline linking (no orchestration)

**Limitations**:
- ❌ No remote caching
- ❌ No affected detection
- ❌ Manual build scripts

**When to upgrade**:
- Add Turborepo when you need remote caching
- Add Nx when you need code generation

---

## Post-Adoption Validation

### Validation Checklist

After completing your chosen option, verify:

- [ ] **Dependencies installed**: `node_modules/` exists
- [ ] **Packages linked**: `node_modules/@acme/ui` is symlink
- [ ] **Build succeeds**: All packages build without errors
- [ ] **Dev server runs**: App runs at http://localhost:3000 (or 4200)
- [ ] **Hot reload works**: Changes in packages reflect in app
- [ ] **Imports work**: Can import from `@acme/ui` and `@acme/utils`
- [ ] **Remote cache works** (if enabled): Second build is 90% faster
- [ ] **CI/CD works** (if enabled): GitHub Actions passes

---

### Common Issues & Solutions

**Issue 1: Package not found**
```bash
# Solution: Install dependencies
pnpm install
```

**Issue 2: Hot reload not working**
```typescript
// Solution: Add transpilePackages to next.config.ts
export default {
  transpilePackages: ['@acme/ui', '@acme/utils'],
};
```

**Issue 3: TypeScript errors**
```bash
# Solution: Restart TypeScript server
# VS Code: Cmd+Shift+P → "TypeScript: Restart TS Server"
```

---

## Next Steps

After adoption, consider:

1. **Add more shared packages**:
   - `@acme/config` - Shared ESLint, Tailwind configs
   - `@acme/tsconfig` - Shared TypeScript configs
   - `@acme/api` - Shared API client (tRPC, GraphQL)

2. **Setup changesets** (versioning):
   ```bash
   pnpm add -Dw @changesets/cli
   npx changeset init
   ```

3. **Add more apps**:
   - Admin dashboard
   - Mobile app (React Native)
   - Documentation site

4. **Optimize CI/CD**:
   - Add affected detection
   - Enable remote caching
   - Parallelize tests

5. **Monitor performance**:
   - Track cache hit rate
   - Measure build times
   - Monitor CI/CD duration

---

## Support & Resources

**Documentation**:
- [protocol-spec.md](./protocol-spec.md) - Complete API reference
- [AGENTS.md](./AGENTS.md) - Quick reference for agents
- [CLAUDE.md](./CLAUDE.md) - Claude-specific patterns

**Official Docs**:
- [Turborepo](https://turbo.build/repo/docs)
- [Nx](https://nx.dev/getting-started/intro)
- [pnpm workspaces](https://pnpm.io/workspaces)

**Community**:
- [Turborepo Discord](https://turbo.build/discord)
- [Nx Discord](https://discord.gg/nx)
- [pnpm Discord](https://discord.gg/pnpm)

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release
- Option A: Turborepo (20 min)
- Option B: Nx (25 min)
- Option C: pnpm workspaces (15 min)
- Complete step-by-step instructions
- Validation checklist
- Troubleshooting guide

---

**Congratulations!** You've successfully adopted SAP-040 and set up a production-ready monorepo. For advanced patterns and optimization tips, see [protocol-spec.md](./protocol-spec.md).
