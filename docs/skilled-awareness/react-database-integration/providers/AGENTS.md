# SAP-034: React Database Integration - ORM Setup (Providers)

**SAP**: SAP-034 (react-database-integration)
**Domain**: Providers
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **2 ORM setup workflows** and a **decision tree** for choosing between Prisma and Drizzle in Next.js 15+ projects.

**Workflows Covered**:
1. Set Up Prisma (15 min) - Popular ORM with admin UI
2. Set Up Drizzle (15 min) - Performance-focused ORM for edge

**For advanced workflows** (migrations, queries, RLS), see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For common patterns** (seeding, pooling, soft deletes), see [../patterns/AGENTS.md](../patterns/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Decision Tree: Which ORM Should I Use?

Use this decision tree to choose between **Prisma** and **Drizzle**:

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

### Quick Decision Matrix

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

### Detailed Comparison

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

## Workflow 1: Set Up Prisma (15 min)

**Time**: 15 minutes

**Best For**: Developer experience, rapid development, teams new to SQL

**Prerequisites**:
- ✅ Next.js 15 project (see SAP-020)
- ✅ PostgreSQL database (local or Supabase)
- ✅ DATABASE_URL environment variable

---

### Step 1: Install Prisma (2 min)

```bash
# Install Prisma CLI (dev dependency)
npm install -D prisma

# Install Prisma Client (runtime dependency)
npm install @prisma/client

# Initialize Prisma with PostgreSQL
npx prisma init --datasource-provider postgresql
```

**Output**:
```
✔ Created prisma/schema.prisma
✔ Created .env
```

---

### Step 2: Configure Database Connection (2 min)

Edit `.env.local`:

```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public"

# Example (local)
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb?schema=public"

# Example (Supabase)
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

**Verify Connection**:

```bash
# Test database connection
npx prisma db pull

# Expected: "Introspecting based on datasource defined in prisma/schema.prisma"
```

---

### Step 3: Create Schema (5 min)

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
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relations
  posts     Post[]

  @@map("users")
}

// Post model
model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)

  // Foreign key
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}
```

**Schema Features**:
- `@id @default(cuid())` - Auto-generated primary key
- `@unique` - Unique constraint
- `@db.Text` - PostgreSQL TEXT type (unlimited length)
- `@relation` - Foreign key relationship
- `onDelete: Cascade` - Delete posts when user deleted
- `@@index` - Index for faster queries
- `@@map("users")` - Custom table name

---

### Step 4: Run First Migration (3 min)

```bash
# Create and apply migration
npx prisma migrate dev --name init

# What happens:
# 1. Generates SQL migration file in prisma/migrations/
# 2. Applies migration to database
# 3. Generates Prisma Client with TypeScript types
```

**Verify Migration**:

```bash
# View database schema
npx prisma studio

# Opens browser at http://localhost:5555
# You should see "users" and "posts" tables
```

---

### Step 5: Create Database Singleton (2 min)

Create `lib/db.ts`:

```typescript
// lib/db.ts

import { PrismaClient } from '@prisma/client';

// Singleton pattern (prevents multiple instances in dev hot-reload)
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

---

### Step 6: Test First Query (1 min)

Create `app/test-db/page.tsx`:

```typescript
// app/test-db/page.tsx

import { prisma } from '@/lib/db';

export default async function TestPage() {
  // Create test user
  const user = await prisma.user.create({
    data: {
      email: 'test@example.com',
      name: 'Test User',
    },
  });

  // Query users
  const users = await prisma.user.findMany();

  return (
    <div>
      <h1>Database Test</h1>
      <p>Created user: {user.name}</p>
      <p>Total users: {users.length}</p>
    </div>
  );
}
```

**Verify**:

```bash
# Run dev server
npm run dev

# Visit http://localhost:3000/test-db
# Expected: "Created user: Test User" and "Total users: 1"
```

---

### ✅ Success Criteria

- ✅ Prisma CLI installed (`npx prisma --version`)
- ✅ Database connected (`.env` configured)
- ✅ Schema created (`prisma/schema.prisma`)
- ✅ Migration applied (`prisma/migrations/XXX_init/migration.sql`)
- ✅ Prisma Client generated (`node_modules/.prisma/client`)
- ✅ First query successful (test page renders)

**Total Time**: 15 minutes

---

## Workflow 2: Set Up Drizzle (15 min)

**Time**: 15 minutes

**Best For**: Performance-critical apps, edge runtime, SQL-savvy teams

**Prerequisites**:
- ✅ Next.js 15 project (see SAP-020)
- ✅ PostgreSQL database (local or Supabase)
- ✅ DATABASE_URL environment variable

---

### Step 1: Install Drizzle (2 min)

```bash
# Install Drizzle ORM
npm install drizzle-orm

# Install Drizzle Kit (migrations)
npm install -D drizzle-kit

# Install PostgreSQL driver
npm install postgres

# Install CUID generator (for primary keys)
npm install @paralleldrive/cuid2
```

---

### Step 2: Create Drizzle Config (2 min)

Create `drizzle.config.ts`:

```typescript
// drizzle.config.ts

import type { Config } from 'drizzle-kit';

export default {
  schema: './lib/schema.ts',         // Schema location
  out: './drizzle/migrations',        // Migration output directory
  driver: 'pg',                       // PostgreSQL driver
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

**Configure Environment**:

Edit `.env.local`:

```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE"

# Example (local)
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb"

# Example (Supabase)
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

---

### Step 3: Create Schema (5 min)

Create `lib/schema.ts`:

```typescript
// lib/schema.ts

import { pgTable, text, varchar, boolean, timestamp } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2';

// User table
export const users = pgTable('users', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  email: varchar('email', { length: 255 })
    .notNull()
    .unique(),
  name: varchar('name', { length: 255 }),
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

// Post table
export const posts = pgTable('posts', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  title: varchar('title', { length: 255 })
    .notNull(),
  content: text('content'),
  published: boolean('published')
    .default(false)
    .notNull(),

  // Foreign key
  authorId: text('author_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),

  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

**Schema Features**:
- `pgTable()` - Define PostgreSQL table
- `.$defaultFn()` - Auto-generated primary key
- `.unique()` - Unique constraint
- `references()` - Foreign key relationship
- `relations()` - Relational queries (join support)

---

### Step 4: Generate and Apply Migration (5 min)

```bash
# Generate migration from schema
npx drizzle-kit generate:pg

# Output: drizzle/migrations/0000_initial_schema.sql
```

**Create Migration Runner**:

Create `scripts/migrate.ts`:

```typescript
// scripts/migrate.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';

const runMigrations = async () => {
  const connectionString = process.env.DATABASE_URL!;

  // Create connection for migrations
  const sql = postgres(connectionString, { max: 1 });
  const db = drizzle(sql);

  console.log('⏳ Running migrations...');
  await migrate(db, { migrationsFolder: './drizzle/migrations' });
  console.log('✅ Migrations complete');

  await sql.end();
};

runMigrations().catch((err) => {
  console.error('❌ Migration failed:', err);
  process.exit(1);
});
```

**Add Script to package.json**:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate:pg",
    "db:migrate": "tsx scripts/migrate.ts"
  }
}
```

**Run Migration**:

```bash
# Install tsx (TypeScript executor)
npm install -D tsx

# Run migration
npm run db:migrate

# Expected: "✅ Migrations complete"
```

---

### Step 5: Create Database Connection (2 min)

Create `lib/db.ts`:

```typescript
// lib/db.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

// Singleton pattern
const globalForDrizzle = globalThis as unknown as {
  conn: postgres.Sql | undefined;
};

const conn = globalForDrizzle.conn ?? postgres(process.env.DATABASE_URL!);

if (process.env.NODE_ENV !== 'production') {
  globalForDrizzle.conn = conn;
}

export const db = drizzle(conn, { schema });
```

---

### Step 6: Test First Query (1 min)

Create `app/test-db/page.tsx`:

```typescript
// app/test-db/page.tsx

import { db } from '@/lib/db';
import { users } from '@/lib/schema';

export default async function TestPage() {
  // Create test user
  const [user] = await db
    .insert(users)
    .values({
      email: 'test@example.com',
      name: 'Test User',
    })
    .returning();

  // Query users
  const allUsers = await db.select().from(users);

  return (
    <div>
      <h1>Database Test</h1>
      <p>Created user: {user.name}</p>
      <p>Total users: {allUsers.length}</p>
    </div>
  );
}
```

**Verify**:

```bash
# Run dev server
npm run dev

# Visit http://localhost:3000/test-db
# Expected: "Created user: Test User" and "Total users: 1"
```

---

### ✅ Success Criteria

- ✅ Drizzle ORM installed (`npm list drizzle-orm`)
- ✅ Database connected (`.env` configured)
- ✅ Schema created (`lib/schema.ts`)
- ✅ Migration applied (`drizzle/migrations/0000_initial_schema.sql`)
- ✅ Database connection initialized (`lib/db.ts`)
- ✅ First query successful (test page renders)

**Total Time**: 15 minutes

---

## Version History

**1.0.0 (2025-11-10)** - Initial providers extraction from awareness-guide.md
- Decision tree for ORM selection
- Workflow 1: Set Up Prisma (15 min)
- Workflow 2: Set Up Drizzle (15 min)
- Complete comparison matrix and decision factors
