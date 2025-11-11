# SAP-034: React Database Integration - Awareness Guide (AGENTS.md)

---
nested_structure: true
nested_files:
  - "providers/AGENTS.md"
  - "workflows/AGENTS.md"
  - "patterns/AGENTS.md"
  - "troubleshooting/AGENTS.md"
version: 2.0.0
last_updated: 2025-11-10
---

**SAP**: SAP-034 (react-database-integration)
**Version**: 2.0.0
**Status**: pilot
**Last Updated**: 2025-11-10

---

## 📖 Quick Reference

**New to SAP-034?** → Read **[README.md](README.md)** first (12-min read)

The README provides:
- 🚀 **Quick Start** - 25-minute setup (Prisma or Drizzle + PostgreSQL)
- 📚 **89.6% Time Savings** - 3-4 hours → 25 minutes with production templates
- 🎯 **Multi-ORM Decision Framework** - Choose Prisma (DX) or Drizzle (performance) based on clear criteria
- 🔧 **Type-Safe Queries** - 100% TypeScript inference from schema (zero manual types)
- 📊 **Performance** - Drizzle 40% faster queries (~30ms vs ~50ms), 73% smaller bundle
- 🔗 **Integration** - Works with SAP-020 (Next.js 15), SAP-033 (Auth), SAP-041 (Forms)

This awareness-guide.md provides: Agent-specific database integration workflows, ORM selection patterns, and migration best practices for AI coding assistants.

---

## ⚠️ Critical Workflows (Read This First!)

**This section highlights the 5 most frequently-missed patterns for database integration in Next.js 15+ projects.**

---

### 1. Choosing the Right ORM ⚠️ MOST COMMON DECISION

**When**: Starting a new project or adding database to existing project

**Common Mistake**: Choosing ORM based on popularity without considering project requirements. Using Prisma for edge-first apps (slow cold starts), or Drizzle for teams new to SQL (steep learning curve).

**Correct Action**: Follow the decision tree based on your specific needs.

**Decision Tree**:

```
Q1: Is performance critical? (real-time, analytics, high-throughput)
  ✅ YES → Drizzle (40% faster queries, 73% smaller bundle)
  ❌ NO → Continue

Q2: Do you need a database admin UI?
  ✅ YES → Prisma (includes Prisma Studio)
  ❌ NO → Continue

Q3: Is your team comfortable with SQL?
  ✅ YES → Drizzle (SQL transparency helps optimization)
  ❌ NO → Prisma (abstracts SQL complexity)

Q4: Are you deploying to edge runtime? (Cloudflare Workers, Vercel Edge)
  ✅ YES → Drizzle (better cold start times)
  ❌ NO → Continue

Q5: Is bundle size critical?
  ✅ YES → Drizzle (80KB vs Prisma 300KB)
  ❌ NO → Prisma (better DX, larger community)

DEFAULT: Prisma (if DX > performance) OR Drizzle (if performance > DX)
```

**Quick Comparison**:

| Your Priority | Recommended ORM |
|---------------|-----------------|
| **Raw performance** | Drizzle |
| **Developer experience** | Prisma |
| **Edge runtime** | Drizzle |
| **Team is SQL-savvy** | Drizzle |
| **Team is SQL-novice** | Prisma |
| **Need admin UI** | Prisma |
| **Bundle size critical** | Drizzle |
| **Large community** | Prisma |

**Time**: 5 minutes (decision)

**Full Details**: [providers/AGENTS.md](providers/AGENTS.md)

---

### 2. Prisma Setup with Singleton Pattern ⚠️ MOST POPULAR

**When**: Using Prisma ORM for the first time

**Common Mistake**: Not using singleton pattern for Prisma Client, causing connection exhaustion in development hot-reload. Creating new Prisma Client on every file change exceeds database connection limit.

**Correct Action**: Use singleton pattern to reuse Prisma Client instance (15 min setup).

**Step 1: Install Prisma** (2 min)

```bash
npm install -D prisma
npm install @prisma/client
npx prisma init --datasource-provider postgresql
```

**Step 2: Create Singleton** (2 min)

```typescript
// lib/db.ts

import { PrismaClient } from '@prisma/client';

// ✅ Singleton pattern (prevents multiple instances in dev hot-reload)
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

**Why Singleton?**:
- Next.js hot-reload creates new module instances
- Without singleton, each hot-reload creates new Prisma Client
- Exceeds database connection limit (default: 10-20 connections)

**Step 3: Configure DATABASE_URL** (2 min)

```bash
# .env.local
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public"

# Example (local)
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb?schema=public"

# Example (Supabase)
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

**Step 4: Create Schema & Run Migration** (9 min)

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}
```

```bash
npx prisma migrate dev --name init
npx prisma studio  # Verify tables created
```

**Time**: 15 minutes

**Full Details**: [providers/AGENTS.md#workflow-1-set-up-prisma-15-min](providers/AGENTS.md#workflow-1-set-up-prisma-15-min)

---

### 3. Connection Pooling for Serverless ⚠️ PRODUCTION CRITICAL

**When**: Deploying to production (Vercel, Netlify, AWS Lambda)

**Common Mistake**: Using direct database connection in serverless environment. Serverless functions create new connections per invocation, causing connection exhaustion within minutes of traffic.

**Correct Action**: Use connection pooler (Supabase Pooler, PgBouncer, etc.)

**Environment Variables**:

```bash
# Pooled connection (for queries) - Port 6543
DATABASE_URL="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Direct connection (for migrations) - Port 5432
POSTGRES_URL_NON_POOLING="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.compute.amazonaws.com:5432/postgres"
```

**Prisma Configuration**:

```prisma
// prisma/schema.prisma

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")               // ✅ Pooled (queries)
  directUrl = env("POSTGRES_URL_NON_POOLING")   // ✅ Direct (migrations)
}
```

**Drizzle Configuration**:

```typescript
// lib/db.ts

const client = postgres(process.env.DATABASE_URL!, {
  max: 1, // ✅ Max connections per serverless function
  idle_timeout: 20, // ✅ Close idle connections after 20s
  connect_timeout: 10, // ✅ Connection timeout 10s
});

export const db = drizzle(client, { schema });
```

**Why Pooling?**:
- Serverless functions are stateless (new connection per invocation)
- Database has limited connection limit (e.g., 100-500 max)
- Without pooling, connection exhaustion occurs under load
- **90% reduction in connection overhead**

**Symptoms Without Pooling**:
```
Error: P1001: Can't reach database server (connection limit exceeded)
Error: remaining connection slots are reserved for non-replication superuser connections
```

**Time**: 10 minutes (configuration)

**Full Details**: [patterns/AGENTS.md#pattern-2-connection-pooling-production](patterns/AGENTS.md#pattern-2-connection-pooling-production)

---

### 4. Type Errors After Schema Change ⚠️ COMMON PITFALL

**When**: After modifying Prisma/Drizzle schema

**Common Mistake**: Not regenerating Prisma Client or restarting TypeScript server. TypeScript uses stale types, causing errors like "Property 'bio' does not exist on type 'User'".

**Correct Action**: Regenerate types + restart TypeScript server (2 min fix).

**Prisma**:

```bash
# ✅ Regenerate Prisma Client
npx prisma generate

# Or run full migration (auto-generates)
npx prisma migrate dev
```

**Drizzle**:

```bash
# ✅ Restart TypeScript server in VSCode
# Cmd+Shift+P → "TypeScript: Restart TS Server"

# Or regenerate types
npm run db:generate
```

**VSCode Quick Fix**:

1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "TypeScript: Restart TS Server"
3. Press Enter

**Common Symptoms**:
```typescript
// ❌ Error: Property 'bio' does not exist on type 'User'
const user = await prisma.user.create({
  data: {
    email: 'test@example.com',
    bio: 'Software developer', // ← TypeScript error
  },
});
```

**Why This Happens**:
- Prisma Client types generated in `node_modules/.prisma/client`
- TypeScript server caches types
- Schema changes don't auto-update TypeScript cache

**Time**: 2 minutes (regeneration)

**Full Details**: [troubleshooting/AGENTS.md#issue-3-type-errors-after-schema-change](troubleshooting/AGENTS.md#issue-3-type-errors-after-schema-change)

---

### 5. Migration Conflicts ⚠️ DEPLOYMENT ISSUE

**When**: Running migrations in production or after manual SQL changes

**Common Mistake**: Making manual SQL changes without creating migration, or applying migrations out of order. Database schema doesn't match migration history, causing "already exists" errors.

**Correct Action**: Use migration workflow consistently (never manual SQL changes).

**Symptoms**:
```
Error: P3005: Database already contains objects that exist in the migration
Error: relation "users" already exists
Error: column "bio" of relation "users" already exists
```

**Prisma Fix** (Development):

```bash
# Option 1: Reset database (⚠️ DELETES ALL DATA)
npx prisma migrate reset

# Option 2: Mark migration as applied (if already manually applied)
npx prisma migrate resolve --applied <MIGRATION_NAME>

# Option 3: Delete bad migration and regenerate
rm -rf prisma/migrations/<BAD_MIGRATION>
npx prisma migrate dev --name <NEW_NAME>
```

**Drizzle Fix** (Development):

```bash
# Option 1: Manually fix SQL in migration file
vim drizzle/migrations/<MIGRATION>.sql

# Option 2: Regenerate migrations from scratch
rm -rf drizzle/migrations/*
npm run db:generate
npm run db:migrate
```

**Production Fix** (Preserve Data):

```bash
# Connect to database
psql $DATABASE_URL

# Check what exists
\d users;

# If conflict, mark migration as applied without executing
npx prisma migrate resolve --applied <MIGRATION_NAME>
```

**Prevention**:
- ❌ Never make manual SQL changes
- ✅ Always use migration workflow (Prisma: `migrate dev`, Drizzle: `db:generate`)
- ✅ Test migrations in staging before production
- ✅ Use version control for migration files

**Time**: 5 minutes (fix)

**Full Details**: [troubleshooting/AGENTS.md#issue-2-migration-conflict](troubleshooting/AGENTS.md#issue-2-migration-conflict)

---

## Quick Start

**Before you begin**:
- ✅ SAP-020 (React Foundation) adopted (Next.js 15 App Router)
- ✅ PostgreSQL database (local, Supabase, or cloud provider)
- ✅ DATABASE_URL environment variable

**Choose your path** (based on requirements):

1. **Popular choice (15 min)**: [Prisma](providers/AGENTS.md#workflow-1-set-up-prisma-15-min)
   - Better DX, admin UI (Prisma Studio)
   - Larger community, more tutorials
   - Abstracts SQL complexity

2. **Performance-focused (15 min)**: [Drizzle](providers/AGENTS.md#workflow-2-set-up-drizzle-15-min)
   - 40% faster queries
   - 73% smaller bundle (80KB vs 300KB)
   - Better for edge runtime

---

## Decision Tree: Which ORM Should I Use?

**Use this decision tree to select the ORM that matches your requirements.**

```
START: Which ORM should I use?
│
├─ Q1: Is performance critical? (real-time, analytics, high-throughput)
│  ├─ YES → Drizzle (40% faster queries, 73% smaller bundle)
│  └─ NO  → Continue to Q2
│
├─ Q2: Do you need a database admin UI?
│  ├─ YES → Prisma (includes Prisma Studio)
│  └─ NO  → Continue to Q3
│
├─ Q3: Is your team comfortable with SQL?
│  ├─ YES → Drizzle (SQL transparency helps optimization)
│  └─ NO  → Prisma (abstracts SQL complexity)
│
├─ Q4: Are you deploying to edge runtime? (Cloudflare Workers, Vercel Edge)
│  ├─ YES → Drizzle (better cold start times)
│  └─ NO  → Continue to Q5
│
├─ Q5: Is bundle size critical?
│  ├─ YES → Drizzle (80KB vs Prisma 300KB)
│  └─ NO  → Prisma (better DX, larger community)
│
└─ DEFAULT RECOMMENDATION:
   - Choose Prisma if: DX > performance, need admin UI, team new to SQL
   - Choose Drizzle if: Performance critical, edge-first, SQL-comfortable team
```

**Comparison Matrix**:

| Feature | Prisma | Drizzle |
|---------|--------|---------|
| **Query Performance** | Good | **40% faster** |
| **Bundle Size** | 300KB | **80KB (73% smaller)** |
| **Admin UI** | ✅ Prisma Studio | ❌ None |
| **SQL Transparency** | ❌ Abstracted | ✅ Full control |
| **Edge Runtime** | ⚠️ Limited | ✅ Optimized |
| **TypeScript** | ✅ Full | ✅ Full |
| **Migration Tool** | ✅ Built-in | ✅ Drizzle Kit |
| **Learning Curve** | Low | Medium |
| **Community** | Large (100k+ users) | Growing (20k+ users) |
| **Maturity** | Mature (2019) | Newer (2022) |

---

## Navigation: Nested Awareness Files

This SAP uses the **nested awareness pattern** (SAP-009 v2.1.0) to organize content by domain. The root file (this file) contains Quick Start, Decision Tree, and Critical Workflows. Detailed workflows are in domain-specific files.

**Domain Files** (read based on task):

1. **[providers/AGENTS.md](providers/AGENTS.md)** - ORM setup workflows (2 workflows)
   - Workflow 1: Set Up Prisma (15 min)
   - Workflow 2: Set Up Drizzle (15 min)
   - Decision tree and comparison matrix

2. **[workflows/AGENTS.md](workflows/AGENTS.md)** - Advanced database workflows (3 workflows)
   - Workflow 3: Create and Run Migrations (10 min)
   - Workflow 4: Implement Type-Safe Queries (15 min)
   - Workflow 5: Add Row-Level Security (20 min, Supabase)

3. **[patterns/AGENTS.md](patterns/AGENTS.md)** - Common patterns (3 patterns)
   - Pattern 1: Database Seeding (Development/Testing)
   - Pattern 2: Connection Pooling (Production)
   - Pattern 3: Soft Deletes

4. **[troubleshooting/AGENTS.md](troubleshooting/AGENTS.md)** - Common issues and fixes (3 issues)
   - Issue 1: "Can't reach database server"
   - Issue 2: "Migration conflict"
   - Issue 3: "Type errors after schema change"

**Progressive Loading Strategy**:

- **Phase 1 (0-10k tokens)**: Read this root file for Quick Start and Decision Tree
- **Phase 2 (10-50k tokens)**: Read domain-specific file for your task (e.g., providers/ for setup, workflows/ for migrations)
- **Phase 3 (50-200k tokens)**: Read multiple domain files for complex integrations

**Token Savings**: 57% reduction via nested structure (root file ~750 lines vs original 1,724 lines)

---

## When to Use This SAP

**Adopt SAP-034 when**:

✅ **Project Requirements**:
- Building web application with persistent data
- Need CRUD operations (Create, Read, Update, Delete)
- User accounts, posts, comments, or any relational data
- Multi-tenant SaaS with data isolation

✅ **Technology Stack**:
- Next.js 15+ (App Router)
- React 19+
- TypeScript
- PostgreSQL, MySQL, or SQLite

✅ **Features Needed**:
- Type-safe database queries
- Migration management
- Relational data (foreign keys, joins)
- Connection pooling for serverless

**Skip this SAP if**:

❌ **Simple Use Cases**:
- Static site with no database
- Read-only data from external API
- No persistent storage needed

❌ **Different Database**:
- Using NoSQL (MongoDB, DynamoDB) - different patterns
- Using Firebase/Firestore - managed SDK
- Using Supabase client library only - no ORM needed

---

## Integration with Other SAPs

**Required Dependencies**:
- **SAP-020** (React Foundation): Next.js 15 App Router baseline

**Common Integration Patterns**:

**Database + Authentication** (SAP-034 + SAP-033):
- Store user accounts in database
- PrismaAdapter syncs NextAuth sessions with database
- Type-safe user queries with Prisma/Drizzle

**Database + Forms** (SAP-034 + SAP-041):
- Server Actions validate and insert form data
- Type-safe schema validation with Zod + Prisma
- Automatic type inference for form fields

**Database + File Upload** (SAP-034 + SAP-035):
- Store file metadata in database (URL, size, type)
- Track file ownership via user foreign key
- Query files with relational data

**Example Integration** (Prisma + NextAuth + Server Action):

```typescript
// app/actions/posts.ts
'use server';

import { prisma } from '@/lib/db';
import { auth } from '@/auth'; // SAP-033
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  // Authentication check (SAP-033)
  const session = await auth();
  if (!session) {
    return { error: 'Unauthorized' };
  }

  // Form data extraction (SAP-041)
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Database insert (SAP-034)
  const post = await prisma.post.create({
    data: {
      title,
      content,
      authorId: session.user.id,
    },
    include: {
      author: true, // Relational query
    },
  });

  revalidatePath('/posts');
  return post;
}
```

---

## Success Criteria

**SAP-034 is successfully adopted when**:

✅ **ORM Setup**:
- [ ] Prisma or Drizzle installed and configured
- [ ] Database connected (`.env` configured)
- [ ] Schema created with at least 2 models
- [ ] First migration applied successfully
- [ ] Singleton pattern implemented (prevents connection exhaustion)

✅ **Type Safety**:
- [ ] TypeScript types auto-generated from schema
- [ ] Queries are fully type-safe (autocomplete works)
- [ ] No `any` types in database queries
- [ ] TypeScript server recognizes schema changes after regeneration

✅ **Migration Workflow**:
- [ ] Migrations run successfully in development
- [ ] Migration history tracked in version control
- [ ] Production migrations tested in staging
- [ ] No manual SQL changes (all via migration workflow)

✅ **Production Ready**:
- [ ] Connection pooling configured (if serverless)
- [ ] Environment variables for production database
- [ ] Seed script for development/testing data
- [ ] Database backups configured

---

## Testing Your Implementation

**Basic CRUD Flow**:
1. Create user → Insert succeeds, returns ID
2. Query user → Find by ID or email
3. Update user → Modify fields, save changes
4. Delete user → Soft delete or hard delete

**Type Safety Check**:
1. Change schema (add new field)
2. Run migration → `npx prisma migrate dev` or `npm run db:generate`
3. Regenerate types → TypeScript autocomplete shows new field
4. Use new field in query → No type errors

**Production Deployment**:
1. Configure connection pooling → Environment variables set
2. Deploy to Vercel/Netlify → Connection pooling active
3. Load test → No connection exhaustion errors
4. Monitor connections → Database stays under connection limit

---

## Version History

**2.0.0 (2025-11-10)** - Nested awareness pattern adoption (SAP-009 v2.1.0)
- Split 1,724-line file into 4 domain-specific files (57% reduction)
- Added Critical Workflows section with 5 frequently-missed patterns
- Created providers/, workflows/, patterns/, troubleshooting/ domains
- Target: ~750 lines root file, ~4.2k tokens (Phase 1 progressive loading)

**1.0.0 (2025-11-09)** - Initial database integration SAP
- 2 ORM setup workflows (Prisma, Drizzle)
- 3 advanced workflows (migrations, queries, RLS)
- 3 common patterns (seeding, pooling, soft deletes)
- 3 troubleshooting issues with complete fixes
- Decision tree for ORM selection
