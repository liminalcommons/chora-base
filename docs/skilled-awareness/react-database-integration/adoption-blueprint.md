# SAP-034: React Database Integration - Adoption Blueprint

**SAP ID**: SAP-034
**Name**: react-database-integration
**Full Name**: React Database Integration
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09
**Diataxis Type**: Tutorial

---

## Overview

This blueprint guides you through adopting SAP-034 (React Database Integration) in your Next.js project. You'll integrate PostgreSQL using either **Prisma** (DX-focused) or **Drizzle** (performance-focused) ORM.

**Estimated Time**: 25 minutes
**Difficulty**: Intermediate
**Prerequisites**: Node.js 22.x, Next.js 15, PostgreSQL/Supabase

---

## Prerequisites

Before starting, ensure you have:

### Required

- ✅ **Next.js 15 Project**: SAP-020 React Foundation adopted
  - App Router enabled
  - TypeScript configured
  - Environment variables setup (`.env.local`)

- ✅ **PostgreSQL Database**: One of the following
  - Local PostgreSQL (14+)
  - Supabase project (recommended for beginners)
  - Vercel Postgres
  - Neon, PlanetScale, or other hosted PostgreSQL

- ✅ **Node.js**: Version 22.x or later
  ```bash
  node --version  # Should be v22.x or higher
  ```

- ✅ **Package Manager**: npm, pnpm, or yarn installed

### Optional (Recommended)

- ✅ **Database Client**: pgAdmin, TablePlus, or Postico (for manual inspection)
- ✅ **Authentication**: SAP-033 adopted (for Row-Level Security integration)

### Verify Prerequisites

```bash
# Check Node.js version
node --version

# Check Next.js version (should be 15.x)
npm list next

# Check if database is accessible
psql $DATABASE_URL -c "SELECT version();"
# OR for Supabase: Test connection via Supabase dashboard
```

**If any prerequisite fails**, resolve it before continuing.

---

## Decision Point: Prisma or Drizzle?

Before proceeding, choose your ORM based on project needs:

### Choose Prisma if:
- ✅ You need a database admin UI (Prisma Studio)
- ✅ Developer experience is more important than raw performance
- ✅ Your team is new to SQL or databases
- ✅ You want comprehensive documentation and large community
- ✅ Migration workflow simplicity is important

### Choose Drizzle if:
- ✅ Performance is critical (40% faster queries, 73% smaller bundle)
- ✅ You're deploying to edge runtime (Cloudflare Workers, Vercel Edge)
- ✅ Your team is comfortable with SQL
- ✅ Bundle size matters (80KB vs Prisma's 300KB)
- ✅ You want SQL transparency for query optimization

### Still Unsure?

**Default recommendation**: Start with **Prisma** (easier learning curve, better DX)

You can always migrate to Drizzle later if performance becomes a bottleneck.

---

## Path A: Prisma Setup (25 minutes)

Follow this path if you chose Prisma.

### Step 1: Install Prisma Dependencies (3 min)

```bash
# Install Prisma CLI (dev dependency)
npm install -D prisma

# Install Prisma Client (runtime dependency)
npm install @prisma/client

# Verify installation
npx prisma --version
# Expected: prisma: 5.x.x
```

**What just happened?**
- `prisma`: CLI for schema management, migrations, Prisma Studio
- `@prisma/client`: Type-safe database client for queries

---

### Step 2: Initialize Prisma (2 min)

```bash
# Initialize Prisma with PostgreSQL
npx prisma init --datasource-provider postgresql
```

**Generated files**:
- `prisma/schema.prisma`: Database schema definition
- `.env`: Environment variables template

**Configure database connection**:

Edit `.env.local` (or `.env`):

```bash
# PostgreSQL connection string format:
# postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public

# Example 1: Local PostgreSQL
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb?schema=public"

# Example 2: Supabase
DATABASE_URL="postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Example 3: Vercel Postgres (from Vercel dashboard)
DATABASE_URL="postgres://default:xxxx@ep-xxxx.us-east-1.postgres.vercel-storage.com:5432/verceldb"
```

**Replace placeholders**:
- `USER`: Database username (e.g., `postgres`)
- `PASSWORD`: Database password
- `HOST`: Database host (e.g., `localhost`, `db.xxx.supabase.co`)
- `PORT`: Database port (default: `5432` direct, `6543` pooled)
- `DATABASE`: Database name (e.g., `mydb`, `postgres`)

**Verify connection**:

```bash
# Test database connection
npx prisma db pull

# Expected output: "Introspecting based on datasource defined in prisma/schema.prisma"
# If error: Check DATABASE_URL, verify database is running
```

---

### Step 3: Create Database Schema (5 min)

Edit `prisma/schema.prisma`:

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// User model
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  bio       String?  @db.Text

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relations
  posts     Post[]
  comments  Comment[]

  // Table name override
  @@map("users")
}

// Post model
model Post {
  id        String   @id @default(cuid())
  title     String   @db.VarChar(255)
  slug      String   @unique
  content   String?  @db.Text
  published Boolean  @default(false)
  publishedAt DateTime?

  // Foreign key
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  // Relations
  comments  Comment[]

  // Metadata
  viewCount Int      @default(0)

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Indexes
  @@index([authorId])
  @@index([slug])

  @@map("posts")
}

// Comment model
model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text

  // Foreign keys
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Indexes
  @@index([authorId])
  @@index([postId])

  @@map("comments")
}
```

**Key concepts**:
- `@id`: Primary key
- `@default(cuid())`: Auto-generate globally unique ID
- `@unique`: Enforce uniqueness constraint
- `@relation`: Define foreign key relationship
- `@updatedAt`: Auto-update on record change
- `@@index([field])`: Create database index for query performance
- `@@map("table_name")`: Override table name (snake_case in DB, PascalCase in Prisma)

---

### Step 4: Run First Migration (5 min)

```bash
# Create migration from schema
npx prisma migrate dev --name init

# What happens:
# 1. Generates SQL migration file in prisma/migrations/
# 2. Applies migration to database (creates tables)
# 3. Generates Prisma Client with TypeScript types
```

**Expected output**:

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (v5.x.x) to ./node_modules/@prisma/client in Xms
```

**Verify migration**:

```bash
# View generated migration SQL
cat prisma/migrations/*/migration.sql

# Expected: CREATE TABLE statements for users, posts, comments
```

**Inspect database**:

```bash
# Option 1: Prisma Studio (GUI)
npx prisma studio

# Opens browser at http://localhost:5555
# You should see empty "users", "posts", "comments" tables

# Option 2: psql (CLI)
psql $DATABASE_URL

# List tables
\dt

# Describe users table
\d users;

# Exit psql
\q
```

---

### Step 5: Generate Prisma Client (3 min)

```bash
# Generate Prisma Client (auto-typed from schema)
npx prisma generate

# Expected: "Generated Prisma Client (v5.x.x) to ./node_modules/@prisma/client"
```

**Note**: This step is automatic after `prisma migrate dev`, but shown explicitly for clarity.

---

### Step 6: Create Database Singleton (5 min)

Create `lib/db.ts`:

```typescript
// lib/db.ts

import { PrismaClient } from '@prisma/client';

/**
 * Database singleton
 *
 * Prevents multiple PrismaClient instances during development hot-reload.
 * In production, creates a single instance.
 */

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development'
      ? ['query', 'error', 'warn']
      : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

**Why singleton pattern?**

In Next.js development mode, hot-reload can create multiple PrismaClient instances, exhausting database connections. The singleton pattern ensures only one instance exists.

**Logging configuration**:
- **Development**: Log queries, errors, warnings (helps debugging)
- **Production**: Log errors only (reduces noise)

---

### Step 7: Test First Query (2 min)

Create `app/test-db/page.tsx`:

```typescript
// app/test-db/page.tsx

import { prisma } from '@/lib/db';

export default async function TestDatabasePage() {
  // Create a test user
  const user = await prisma.user.create({
    data: {
      email: `test-${Date.now()}@example.com`,
      name: 'Test User',
      bio: 'This is a test user created during SAP-034 adoption',
    },
  });

  // Query all users
  const allUsers = await prisma.user.findMany({
    select: {
      id: true,
      email: true,
      name: true,
      createdAt: true,
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Database Test</h1>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Created User</h2>
        <pre className="bg-gray-100 p-4 rounded">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2">
          All Users ({allUsers.length})
        </h2>
        <ul className="space-y-2">
          {allUsers.map((u) => (
            <li key={u.id} className="bg-gray-50 p-3 rounded">
              <p className="font-medium">{u.name}</p>
              <p className="text-sm text-gray-600">{u.email}</p>
              <p className="text-xs text-gray-400">
                Created: {u.createdAt.toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

**Run test**:

```bash
# Start dev server
npm run dev

# Visit http://localhost:3000/test-db
```

**Expected result**:
- ✅ Page renders without errors
- ✅ "Created User" section shows user object with generated ID
- ✅ "All Users" section shows list of users (including just-created user)

**If errors occur**, see [Troubleshooting](#troubleshooting-common-issues).

---

### ✅ Prisma Adoption Complete!

You've successfully adopted SAP-034 with Prisma. You now have:

- ✅ Prisma ORM installed and configured
- ✅ Database schema defined (`prisma/schema.prisma`)
- ✅ Migration applied (tables created in database)
- ✅ Prisma Client generated (type-safe queries)
- ✅ Database singleton created (`lib/db.ts`)
- ✅ First query successful (test page works)

**Next steps**:
1. [Verify installation](#verification-checklist) (5 min)
2. [Create real Server Actions](#next-steps-after-adoption) (see Awareness Guide)
3. [Add authentication integration](#optional-integrations) (SAP-033)
4. [Set up production configuration](#production-readiness) (if deploying)

---

## Path B: Drizzle Setup (25 minutes)

Follow this path if you chose Drizzle.

### Step 1: Install Drizzle Dependencies (3 min)

```bash
# Install Drizzle ORM
npm install drizzle-orm

# Install Drizzle Kit (migrations CLI)
npm install -D drizzle-kit

# Install PostgreSQL driver
npm install postgres

# Install CUID generator (for primary keys)
npm install @paralleldrive/cuid2

# Verify installation
npx drizzle-kit --version
# Expected: drizzle-kit: version X.X.X
```

**What just happened?**
- `drizzle-orm`: Core ORM library
- `drizzle-kit`: CLI for migrations and schema management
- `postgres`: PostgreSQL driver (alternatives: `pg`, `@neondatabase/serverless`)
- `@paralleldrive/cuid2`: Generate globally unique IDs

---

### Step 2: Create Drizzle Config (3 min)

Create `drizzle.config.ts`:

```typescript
// drizzle.config.ts

import type { Config } from 'drizzle-kit';

export default {
  schema: './lib/schema.ts',        // Schema location
  out: './drizzle/migrations',       // Migration output directory
  driver: 'pg',                      // PostgreSQL driver
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
  verbose: true,                     // Show detailed logs
  strict: true,                      // Strict mode (safer migrations)
} satisfies Config;
```

**Configure database connection**:

Edit `.env.local` (or `.env`):

```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE"

# Example 1: Local PostgreSQL
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb"

# Example 2: Supabase
DATABASE_URL="postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Example 3: Vercel Postgres
DATABASE_URL="postgres://default:xxxx@ep-xxxx.us-east-1.postgres.vercel-storage.com:5432/verceldb"
```

**Verify connection**:

```bash
# Test connection via psql
psql $DATABASE_URL -c "SELECT version();"

# Expected: PostgreSQL version info
# If error: Check DATABASE_URL, verify database is running
```

---

### Step 3: Create Database Schema (5 min)

Create `lib/schema.ts`:

```typescript
// lib/schema.ts

import { pgTable, text, varchar, boolean, timestamp, integer } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2';

/**
 * User table
 */
export const users = pgTable('users', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  email: varchar('email', { length: 255 })
    .notNull()
    .unique(),
  name: varchar('name', { length: 255 }),
  bio: text('bio'),

  // Timestamps
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

/**
 * Post table
 */
export const posts = pgTable('posts', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  title: varchar('title', { length: 255 })
    .notNull(),
  slug: varchar('slug', { length: 255 })
    .notNull()
    .unique(),
  content: text('content'),
  published: boolean('published')
    .default(false)
    .notNull(),
  publishedAt: timestamp('published_at'),

  // Foreign key
  authorId: text('author_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),

  // Metadata
  viewCount: integer('view_count')
    .default(0)
    .notNull(),

  // Timestamps
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

/**
 * Comment table
 */
export const comments = pgTable('comments', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  content: text('content')
    .notNull(),

  // Foreign keys
  authorId: text('author_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),
  postId: text('post_id')
    .notNull()
    .references(() => posts.id, { onDelete: 'cascade' }),

  // Timestamps
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

/**
 * Relations (for relational query API)
 */
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  comments: many(comments),
}));

export const commentsRelations = relations(comments, ({ one }) => ({
  author: one(users, {
    fields: [comments.authorId],
    references: [users.id],
  }),
  post: one(posts, {
    fields: [comments.postId],
    references: [posts.id],
  }),
}));
```

**Key concepts**:
- `pgTable('table_name', {...})`: Define table
- `.primaryKey()`: Mark as primary key
- `.notNull()`: Non-nullable field
- `.unique()`: Enforce uniqueness
- `.references(() => table.column)`: Foreign key
- `relations()`: Define relationships for relational query API
- `.$defaultFn()`: Generate default value (e.g., CUID)

---

### Step 4: Generate Migration (7 min)

```bash
# Generate migration from schema
npx drizzle-kit generate:pg

# Expected output: "Generated 1 migration"
```

**Verify generated migration**:

```bash
# View migration SQL
cat drizzle/migrations/0000_initial_schema.sql

# Expected: CREATE TABLE statements for users, posts, comments
```

**Create migration runner script**:

Create `scripts/migrate.ts`:

```typescript
// scripts/migrate.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';

async function runMigrations() {
  const connectionString = process.env.DATABASE_URL;

  if (!connectionString) {
    throw new Error('DATABASE_URL environment variable is not set');
  }

  console.log('⏳ Running migrations...');

  // Create connection (max 1 for migrations)
  const sql = postgres(connectionString, { max: 1 });
  const db = drizzle(sql);

  // Run migrations
  await migrate(db, { migrationsFolder: './drizzle/migrations' });

  console.log('✅ Migrations completed successfully');

  // Close connection
  await sql.end();
}

runMigrations().catch((err) => {
  console.error('❌ Migration failed:');
  console.error(err);
  process.exit(1);
});
```

**Add npm scripts**:

Edit `package.json`:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate:pg",
    "db:migrate": "tsx scripts/migrate.ts",
    "db:studio": "drizzle-kit studio"
  }
}
```

**Install tsx** (TypeScript executor):

```bash
npm install -D tsx
```

**Run migration**:

```bash
npm run db:migrate

# Expected output:
# ⏳ Running migrations...
# ✅ Migrations completed successfully
```

**Verify migration**:

```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Expected: users, posts, comments, __drizzle_migrations

# Describe users table
\d users;

# Exit psql
\q
```

---

### Step 5: Create Database Connection (4 min)

Create `lib/db.ts`:

```typescript
// lib/db.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

/**
 * Database connection singleton
 *
 * Prevents multiple connections during development hot-reload.
 */

const globalForDrizzle = globalThis as unknown as {
  conn: postgres.Sql | undefined;
};

// Create connection (reuse in development)
const conn = globalForDrizzle.conn ?? postgres(process.env.DATABASE_URL!);

if (process.env.NODE_ENV !== 'production') {
  globalForDrizzle.conn = conn;
}

// Create Drizzle instance with schema
export const db = drizzle(conn, { schema });
```

**Why singleton pattern?**

Similar to Prisma, Next.js hot-reload can create multiple connections. The singleton ensures only one connection exists.

---

### Step 6: Test First Query (3 min)

Create `app/test-db/page.tsx`:

```typescript
// app/test-db/page.tsx

import { db } from '@/lib/db';
import { users } from '@/lib/schema';
import { desc } from 'drizzle-orm';

export default async function TestDatabasePage() {
  // Create a test user
  const [user] = await db
    .insert(users)
    .values({
      email: `test-${Date.now()}@example.com`,
      name: 'Test User',
      bio: 'This is a test user created during SAP-034 adoption',
    })
    .returning();

  // Query all users
  const allUsers = await db
    .select({
      id: users.id,
      email: users.email,
      name: users.name,
      createdAt: users.createdAt,
    })
    .from(users)
    .orderBy(desc(users.createdAt));

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Database Test</h1>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Created User</h2>
        <pre className="bg-gray-100 p-4 rounded">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2">
          All Users ({allUsers.length})
        </h2>
        <ul className="space-y-2">
          {allUsers.map((u) => (
            <li key={u.id} className="bg-gray-50 p-3 rounded">
              <p className="font-medium">{u.name}</p>
              <p className="text-sm text-gray-600">{u.email}</p>
              <p className="text-xs text-gray-400">
                Created: {u.createdAt?.toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

**Run test**:

```bash
# Start dev server
npm run dev

# Visit http://localhost:3000/test-db
```

**Expected result**:
- ✅ Page renders without errors
- ✅ "Created User" section shows user object with generated ID
- ✅ "All Users" section shows list of users (including just-created user)

**If errors occur**, see [Troubleshooting](#troubleshooting-common-issues).

---

### ✅ Drizzle Adoption Complete!

You've successfully adopted SAP-034 with Drizzle. You now have:

- ✅ Drizzle ORM installed and configured
- ✅ Database schema defined (`lib/schema.ts`)
- ✅ Migration applied (tables created in database)
- ✅ Database connection initialized (`lib/db.ts`)
- ✅ First query successful (test page works)

**Next steps**:
1. [Verify installation](#verification-checklist) (5 min)
2. [Create real Server Actions](#next-steps-after-adoption) (see Awareness Guide)
3. [Add authentication integration](#optional-integrations) (SAP-033)
4. [Set up production configuration](#production-readiness) (if deploying)

---

## Verification Checklist

After completing either Path A (Prisma) or Path B (Drizzle), verify your installation:

### Database Connection

```bash
# Test database connection
psql $DATABASE_URL -c "SELECT version();"

# Expected: PostgreSQL version info
```

**✅ Pass**: PostgreSQL version displayed
**❌ Fail**: Connection error → Check DATABASE_URL in `.env.local`

---

### Schema Created

**Prisma**:

```bash
# Verify schema file exists
cat prisma/schema.prisma | grep "model User"

# Expected: "model User {"
```

**Drizzle**:

```bash
# Verify schema file exists
cat lib/schema.ts | grep "export const users"

# Expected: "export const users = pgTable..."
```

**✅ Pass**: Schema file contains expected models/tables
**❌ Fail**: Schema missing → Re-run setup steps

---

### Migration Applied

```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Expected: users, posts, comments (+ migration tables)
```

**✅ Pass**: All tables exist
**❌ Fail**: Tables missing → Re-run migration step

---

### TypeScript Types Generated

**Prisma**:

```bash
# Check if Prisma Client exists
ls node_modules/.prisma/client/index.d.ts

# Expected: File exists
```

**Drizzle**:

```bash
# Check if schema exports types
cat lib/schema.ts | grep "export const"

# Expected: Table exports visible
```

**✅ Pass**: Types are available
**❌ Fail**: Types missing → Run `npx prisma generate` (Prisma) or restart TS server (Drizzle)

---

### First Query Successful

```bash
# Visit test page
npm run dev
# Open http://localhost:3000/test-db

# Expected:
# - Page renders without errors
# - "Created User" section shows user data
# - "All Users" section shows user list
```

**✅ Pass**: Test page renders successfully
**❌ Fail**: Errors in browser → Check browser console, see [Troubleshooting](#troubleshooting-common-issues)

---

### Environment Variables Configured

```bash
# Verify DATABASE_URL is set
echo $DATABASE_URL

# Expected: postgresql://... connection string
```

**✅ Pass**: DATABASE_URL is set and valid
**❌ Fail**: Not set → Add to `.env.local`

---

## Next Steps After Adoption

### 1. Create Real Server Actions

Delete `app/test-db/page.tsx` and create production Server Actions:

**Example** (`app/actions/users.ts`):

```typescript
'use server';

import { prisma } from '@/lib/db'; // Or: import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function getUsers() {
  return prisma.user.findMany({
    orderBy: { createdAt: 'desc' },
  });
}

export async function createUser(formData: FormData) {
  const email = formData.get('email') as string;
  const name = formData.get('name') as string;

  const user = await prisma.user.create({
    data: { email, name },
  });

  revalidatePath('/users');
  return user;
}
```

See [Awareness Guide - Workflow 4](awareness-guide.md#workflow-4-implement-type-safe-queries-15-min) for complete examples.

---

### 2. Add Database Seeding (Optional)

Create seed script for development data:

**Prisma**: See [Awareness Guide - Pattern 1](awareness-guide.md#pattern-1-database-seeding-developmenttesting)

**Drizzle**: See [Awareness Guide - Pattern 1](awareness-guide.md#pattern-1-database-seeding-developmenttesting)

---

### 3. Update Project AGENTS.md

Add SAP-034 adoption notice to your project's `AGENTS.md`:

```markdown
## Database Integration (SAP-034)

**Status**: Adopted
**ORM**: Prisma (or Drizzle)
**Database**: PostgreSQL (Supabase/local/Vercel)

### Key Files
- Schema: `prisma/schema.prisma` (or `lib/schema.ts`)
- Database Client: `lib/db.ts`
- Migrations: `prisma/migrations/` (or `drizzle/migrations/`)
- Server Actions: `app/actions/*.ts`

### Common Tasks
- Run migrations: `npx prisma migrate dev` (or `npm run db:migrate`)
- Open Studio: `npx prisma studio` (Prisma only)
- Generate types: `npx prisma generate` (Prisma only)

### Related SAPs
- SAP-020: React Project Foundation (required)
- SAP-033: Authentication Integration (recommended)
```

---

## Optional Integrations

### Integration 1: Authentication (SAP-033)

**Why**: Database queries often need user context (current user ID)

**How**: Adopt SAP-033 React Authentication, then integrate:

```typescript
// app/actions/posts.ts (with auth)
'use server';

import { auth } from '@/lib/auth'; // From SAP-033
import { prisma } from '@/lib/db';

export async function getUserPosts() {
  const session = await auth();

  if (!session?.user) {
    throw new Error('Unauthorized');
  }

  // Query posts for authenticated user
  return prisma.post.findMany({
    where: { authorId: session.user.id },
  });
}
```

**See**: [SAP-033 Adoption Blueprint](../react-authentication-integration/adoption-blueprint.md)

---

### Integration 2: Form Validation (SAP-041)

**Why**: Validate form data before database writes

**How**: Adopt SAP-041 React Form Validation, then integrate:

```typescript
// app/actions/posts.ts (with validation)
'use server';

import { z } from 'zod'; // From SAP-041
import { prisma } from '@/lib/db';

const postSchema = z.object({
  title: z.string().min(1).max(255),
  content: z.string().optional(),
});

export async function createPost(formData: FormData) {
  // Validate before database write
  const parsed = postSchema.parse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  return prisma.post.create({ data: parsed });
}
```

**See**: [SAP-041 Adoption Blueprint](../react-form-validation/adoption-blueprint.md)

---

### Integration 3: State Management (SAP-023)

**Why**: Optimistic UI updates during database mutations

**How**: Adopt SAP-023 React State Management, then integrate:

```typescript
// Client component with optimistic update
'use client';

import { useOptimistic } from 'react';
import { createPost } from '@/app/actions/posts';

export function CreatePostForm({ posts }) {
  const [optimisticPosts, addOptimisticPost] = useOptimistic(
    posts,
    (state, newPost) => [...state, newPost]
  );

  async function handleSubmit(formData: FormData) {
    // Optimistically add post
    addOptimisticPost({ title: formData.get('title'), id: 'temp' });

    // Submit to database
    await createPost(formData);
  }

  return <form action={handleSubmit}>...</form>;
}
```

**See**: [SAP-023 Adoption Blueprint](../state-management/adoption-blueprint.md)

---

## Production Readiness

Before deploying to production, configure:

### 1. Connection Pooling

**Why**: Serverless functions exhaust connections without pooling

**Supabase Pooler** (recommended):

```bash
# .env.production
DATABASE_URL="postgresql://...pooler.supabase.com:6543/postgres" # Pooled
POSTGRES_URL_NON_POOLING="postgresql://...compute.amazonaws.com:5432/postgres" # Direct
```

**Prisma Config**:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")              // Pooled
  directUrl = env("POSTGRES_URL_NON_POOLING")  // Direct (migrations)
}
```

**See**: [Awareness Guide - Pattern 2](awareness-guide.md#pattern-2-connection-pooling-production)

---

### 2. CI/CD Migrations

**GitHub Actions** (example):

```yaml
# .github/workflows/deploy.yml
- name: Run migrations
  run: npx prisma migrate deploy # Or: npm run db:migrate
  env:
    DATABASE_URL: ${{ secrets.POSTGRES_URL_NON_POOLING }}
```

**See**: [Protocol Spec - CI/CD Section](protocol-spec.md#cicd-migration-workflow)

---

### 3. Row-Level Security (Multi-Tenant Apps)

**Why**: Prevent cross-tenant data leaks

**How**: Enable RLS and create policies:

```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = author_id);
```

**See**: [Awareness Guide - Workflow 5](awareness-guide.md#workflow-5-add-row-level-security-supabase-20-min)

---

## Troubleshooting Common Issues

### Issue 1: "Can't reach database server"

**Symptoms**: Connection errors during setup

**Solutions**:

1. **Check DATABASE_URL**:
   ```bash
   echo $DATABASE_URL
   # Verify format: postgresql://USER:PASSWORD@HOST:PORT/DATABASE
   ```

2. **Test connection**:
   ```bash
   psql $DATABASE_URL
   # If fails: Check credentials, host, port
   ```

3. **For Supabase**: Verify project not paused (Supabase dashboard)

4. **For local**: Ensure PostgreSQL running:
   ```bash
   # macOS
   brew services start postgresql

   # Linux
   sudo systemctl start postgresql
   ```

---

### Issue 2: "Migration failed"

**Symptoms**: Migration errors, "already exists" errors

**Solutions**:

**Prisma**:

```bash
# Option 1: Reset database (development only!)
npx prisma migrate reset

# Option 2: Mark migration as applied
npx prisma migrate resolve --applied <MIGRATION_NAME>
```

**Drizzle**:

```bash
# Manually fix SQL in migration file
vim drizzle/migrations/<MIGRATION>.sql

# Or regenerate
rm -rf drizzle/migrations/*
npm run db:generate
npm run db:migrate
```

---

### Issue 3: "TypeScript errors after schema change"

**Symptoms**: Type errors in IDE after modifying schema

**Solutions**:

**Prisma**:

```bash
# Regenerate Prisma Client
npx prisma generate

# Or run migration (auto-generates)
npx prisma migrate dev
```

**Drizzle**:

```bash
# Restart TypeScript server in VSCode
# Cmd+Shift+P → "TypeScript: Restart TS Server"
```

---

### Issue 4: "Multiple PrismaClient instances"

**Symptoms**: Warning in development logs

**Solutions**:

Ensure `lib/db.ts` uses singleton pattern (see Step 6 in Path A).

---

## Summary

Congratulations! You've successfully adopted SAP-034 (React Database Integration).

**What you accomplished**:

- ✅ **25 minutes**: Complete database integration (vs 3-4 hours manual setup)
- ✅ **Type Safety**: 100% type-safe database operations
- ✅ **Production Patterns**: Migrations, connection pooling, RLS (optional)
- ✅ **Next.js 15**: Server Components and Server Actions integration

**Time Savings**: **89.6% reduction** (3.5 hours → 25 minutes)

**Next steps**:
1. Create real Server Actions (see Awareness Guide)
2. Add authentication (SAP-033) for user-scoped queries
3. Set up production configuration (connection pooling, RLS)
4. Deploy to Vercel/Supabase

**Need help?**
- **Protocol Spec**: Complete API reference
- **Awareness Guide**: Common workflows and patterns
- **Capability Charter**: Design rationale and evidence

**Provide feedback**: Report adoption metrics to SAP-034 Ledger for continuous improvement.

---

**End of Adoption Blueprint**
