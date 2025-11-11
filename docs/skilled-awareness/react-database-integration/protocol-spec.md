# SAP-034: React Database Integration - Protocol Specification

**SAP ID**: SAP-034
**Name**: react-database-integration
**Full Name**: React Database Integration
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09
**Diataxis Type**: Reference

---

## Table of Contents

1. [Overview](#overview)
2. [Prisma ORM Reference](#prisma-orm-reference)
3. [Drizzle ORM Reference](#drizzle-orm-reference)
4. [Prisma vs Drizzle Comparison](#prisma-vs-drizzle-comparison)
5. [Common Patterns](#common-patterns)
6. [Next.js 15 Integration](#nextjs-15-integration)
7. [Production Configuration](#production-configuration)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### Purpose

This protocol specification provides complete technical reference for integrating PostgreSQL databases into React/Next.js applications using **Prisma** or **Drizzle** ORMs. Use this document for:

- **Implementation Reference**: Copy-paste code examples
- **API Reference**: Complete ORM command catalog
- **Configuration Reference**: Environment variables, connection strings
- **Pattern Reference**: Type-safe queries, migrations, RLS

### Scope

**In Scope**:
- Prisma ORM (schema, queries, migrations, Prisma Studio)
- Drizzle ORM (schema, queries, migrations, drizzle-kit)
- PostgreSQL database configuration
- Next.js 15 Server Components and Server Actions integration
- Connection pooling and edge runtime compatibility
- Row-Level Security (RLS) patterns for Supabase/PostgreSQL
- Type-safe query patterns

**Out of Scope**:
- MySQL, MongoDB, SQLite (future versions)
- GraphQL integration (see SAP-030 for data fetching)
- Database branching (PlanetScale, Neon, Supabase branches)
- Advanced query optimization (see SAP-032)
- Database seeding strategies (covered in Awareness Guide)

### Prerequisites

- **Node.js**: 22.x or later
- **Next.js**: 15.x or later (with App Router)
- **PostgreSQL**: 14+ or Supabase
- **TypeScript**: 5.0+
- **Package Manager**: npm, pnpm, or yarn

### Conventions

**Notation**:
- `<REQUIRED>`: Placeholder for user-provided value
- `[OPTIONAL]`: Optional parameter
- `$VARIABLE`: Environment variable
- `# Comment`: Inline explanation

**File Paths**:
- `/` = Project root
- `/lib/db.ts` = Database singleton
- `/prisma/schema.prisma` = Prisma schema
- `/lib/schema.ts` = Drizzle schema

---

## Prisma ORM Reference

### Installation

#### 1. Install Dependencies

```bash
# Install Prisma CLI (dev dependency)
npm install -D prisma

# Install Prisma Client (runtime dependency)
npm install @prisma/client

# Install connection pooling (optional, for production)
npm install @prisma/extension-accelerate
```

#### 2. Initialize Prisma

```bash
# Initialize Prisma with PostgreSQL
npx prisma init --datasource-provider postgresql
```

**Output**:
```
✔ Created prisma/schema.prisma
✔ Created .env
```

**Generated `.env`**:
```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public"
```

### Schema Syntax

#### Basic Schema Structure

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
  // Optional: Enable edge runtime support
  // previewFeatures = ["driverAdapters"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Optional: Direct connection for migrations
  // directUrl = env("POSTGRES_URL_NON_POOLING")
}

// Models defined below...
```

#### User Model (Complete Example)

```prisma
model User {
  // Primary key (CUID for global uniqueness)
  id        String   @id @default(cuid())

  // Unique fields
  email     String   @unique
  username  String?  @unique

  // Profile fields
  name      String?
  bio       String?  @db.Text // PostgreSQL TEXT type
  avatar    String?  @db.VarChar(255)

  // Enums
  role      UserRole @default(USER)
  status    UserStatus @default(ACTIVE)

  // Relations
  posts     Post[]
  comments  Comment[]
  profile   Profile?

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime? // Soft delete

  // Indexes
  @@index([email])
  @@index([username])

  // Table name override (optional)
  @@map("users")
}

enum UserRole {
  USER
  ADMIN
  MODERATOR
}

enum UserStatus {
  ACTIVE
  SUSPENDED
  DELETED
}
```

#### Post Model (With Relations)

```prisma
model Post {
  id        String   @id @default(cuid())

  // Content fields
  title     String   @db.VarChar(255)
  slug      String   @unique
  content   String?  @db.Text
  excerpt   String?  @db.VarChar(500)

  // Publishing
  published Boolean  @default(false)
  publishedAt DateTime?

  // Relations
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  comments  Comment[]
  tags      TagsOnPosts[]

  // Metadata
  viewCount Int      @default(0)

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?

  // Indexes
  @@index([authorId])
  @@index([slug])
  @@index([published, publishedAt])

  @@map("posts")
}
```

#### Comment Model (Nested Relations)

```prisma
model Comment {
  id        String   @id @default(cuid())

  content   String   @db.Text

  // Relations
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)

  // Self-referencing (replies)
  parentId  String?
  parent    Comment?  @relation("CommentReplies", fields: [parentId], references: [id], onDelete: Cascade)
  replies   Comment[] @relation("CommentReplies")

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?

  // Indexes
  @@index([postId])
  @@index([authorId])
  @@index([parentId])

  @@map("comments")
}
```

#### Profile Model (One-to-One)

```prisma
model Profile {
  id        String   @id @default(cuid())

  // Profile data
  website   String?
  location  String?
  company   String?

  // One-to-one relation
  userId    String   @unique
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("profiles")
}
```

#### Many-to-Many Relation (Explicit Join Table)

```prisma
model Tag {
  id        String   @id @default(cuid())
  name      String   @unique
  slug      String   @unique

  posts     TagsOnPosts[]

  createdAt DateTime @default(now())

  @@map("tags")
}

// Explicit join table (recommended for additional fields)
model TagsOnPosts {
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)

  tagId     String
  tag       Tag      @relation(fields: [tagId], references: [id], onDelete: Cascade)

  assignedAt DateTime @default(now())

  @@id([postId, tagId])
  @@index([postId])
  @@index([tagId])

  @@map("tags_on_posts")
}
```

### Migration Commands

#### Development Migrations

```bash
# Create migration from schema changes
npx prisma migrate dev --name <MIGRATION_NAME>

# Example: Add user profile
npx prisma migrate dev --name add_user_profile

# What happens:
# 1. Generates SQL migration file in prisma/migrations/
# 2. Applies migration to development database
# 3. Regenerates Prisma Client with new types
```

**Generated Migration File** (`prisma/migrations/20250109123456_add_user_profile/migration.sql`):

```sql
-- CreateTable
CREATE TABLE "profiles" (
    "id" TEXT NOT NULL,
    "website" TEXT,
    "location" TEXT,
    "company" TEXT,
    "userId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "profiles_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "profiles_userId_key" ON "profiles"("userId");

-- AddForeignKey
ALTER TABLE "profiles" ADD CONSTRAINT "profiles_userId_fkey" FOREIGN KEY ("userId") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;
```

#### Production Migrations

```bash
# Apply pending migrations in production (no schema modifications)
npx prisma migrate deploy

# Typical usage in CI/CD (before deployment)
npm run build
npx prisma migrate deploy
npm start
```

#### Reset Database (Development Only)

```bash
# WARNING: Deletes all data and reapplies all migrations
npx prisma migrate reset

# Useful for:
# - Resetting test database
# - Fixing migration conflicts
# - Starting fresh in development
```

#### Migrate Resolve (Fix Conflicts)

```bash
# Mark migration as applied without running it
npx prisma migrate resolve --applied <MIGRATION_NAME>

# Mark migration as rolled back
npx prisma migrate resolve --rolled-back <MIGRATION_NAME>
```

### Prisma Client API

#### Initialize Client (Singleton Pattern)

```typescript
// lib/db.ts

import { PrismaClient } from '@prisma/client';

// Singleton pattern (prevents multiple instances in dev mode)
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

**Usage**:

```typescript
import { prisma } from '@/lib/db';

// Use prisma client throughout your app
const users = await prisma.user.findMany();
```

#### Query Operations

##### findUnique (Get Single Record)

```typescript
import { prisma } from '@/lib/db';

// Find by unique field
const user = await prisma.user.findUnique({
  where: {
    email: 'alice@example.com'
  },
});

// Find with relations
const user = await prisma.user.findUnique({
  where: { id: 'user123' },
  include: {
    posts: true,      // Include all posts
    profile: true,    // Include profile
  },
});

// Select specific fields
const user = await prisma.user.findUnique({
  where: { id: 'user123' },
  select: {
    id: true,
    name: true,
    email: true,
    posts: {
      select: {
        id: true,
        title: true,
      },
    },
  },
});

// Return type: User | null
```

##### findUniqueOrThrow (With Error)

```typescript
try {
  const user = await prisma.user.findUniqueOrThrow({
    where: { email: 'nonexistent@example.com' },
  });
} catch (error) {
  // Throws PrismaClientKnownRequestError if not found
  console.error('User not found');
}
```

##### findMany (Get Multiple Records)

```typescript
// Find all users
const users = await prisma.user.findMany();

// With filtering
const activeUsers = await prisma.user.findMany({
  where: {
    status: 'ACTIVE',
    deletedAt: null, // Not soft-deleted
  },
});

// With pagination
const users = await prisma.user.findMany({
  skip: 0,
  take: 10,
  orderBy: {
    createdAt: 'desc',
  },
});

// With complex filters
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { contains: 'example.com' } },
      { name: { startsWith: 'Alice' } },
    ],
    AND: [
      { status: 'ACTIVE' },
      { createdAt: { gte: new Date('2024-01-01') } },
    ],
  },
});

// With relations and counts
const users = await prisma.user.findMany({
  include: {
    _count: {
      select: { posts: true, comments: true },
    },
  },
});

// Return type: User[]
```

##### findFirst (Get First Match)

```typescript
// Find first admin user
const admin = await prisma.user.findFirst({
  where: { role: 'ADMIN' },
  orderBy: { createdAt: 'asc' },
});

// Return type: User | null
```

##### create (Insert Record)

```typescript
// Create single record
const user = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    name: 'Bob Smith',
    role: 'USER',
  },
});

// Create with relations (nested create)
const user = await prisma.user.create({
  data: {
    email: 'charlie@example.com',
    name: 'Charlie',
    posts: {
      create: [
        { title: 'First Post', content: 'Hello World' },
        { title: 'Second Post', content: 'More content' },
      ],
    },
    profile: {
      create: {
        website: 'https://charlie.dev',
        location: 'San Francisco',
      },
    },
  },
  include: {
    posts: true,
    profile: true,
  },
});

// Return type: User (with included relations if specified)
```

##### createMany (Bulk Insert)

```typescript
// Insert multiple records
const result = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
    { email: 'user3@example.com', name: 'User 3' },
  ],
  skipDuplicates: true, // Skip if unique constraint violated
});

// Return type: { count: number }
console.log(`Created ${result.count} users`);
```

##### update (Modify Record)

```typescript
// Update single record
const user = await prisma.user.update({
  where: { id: 'user123' },
  data: {
    name: 'Updated Name',
    updatedAt: new Date(),
  },
});

// Update with relations (nested update)
const user = await prisma.user.update({
  where: { id: 'user123' },
  data: {
    name: 'Updated Name',
    posts: {
      updateMany: {
        where: { published: false },
        data: { published: true },
      },
    },
  },
});

// Increment field
const post = await prisma.post.update({
  where: { id: 'post123' },
  data: {
    viewCount: { increment: 1 },
  },
});

// Return type: User
```

##### updateMany (Bulk Update)

```typescript
// Update multiple records
const result = await prisma.user.updateMany({
  where: {
    status: 'SUSPENDED',
    createdAt: { lt: new Date('2024-01-01') },
  },
  data: {
    status: 'DELETED',
    deletedAt: new Date(),
  },
});

// Return type: { count: number }
console.log(`Updated ${result.count} users`);
```

##### upsert (Update or Create)

```typescript
// Update if exists, create if not
const user = await prisma.user.upsert({
  where: { email: 'alice@example.com' },
  update: {
    name: 'Alice Updated',
    updatedAt: new Date(),
  },
  create: {
    email: 'alice@example.com',
    name: 'Alice New',
  },
});

// Return type: User
```

##### delete (Remove Record)

```typescript
// Delete single record
const user = await prisma.user.delete({
  where: { id: 'user123' },
});

// Soft delete (recommended)
const user = await prisma.user.update({
  where: { id: 'user123' },
  data: {
    deletedAt: new Date(),
  },
});

// Return type: User
```

##### deleteMany (Bulk Delete)

```typescript
// Delete multiple records
const result = await prisma.user.deleteMany({
  where: {
    status: 'DELETED',
    deletedAt: { lt: new Date('2024-01-01') },
  },
});

// Return type: { count: number }
console.log(`Deleted ${result.count} users`);
```

##### count (Count Records)

```typescript
// Count all records
const count = await prisma.user.count();

// Count with filter
const activeCount = await prisma.user.count({
  where: { status: 'ACTIVE' },
});

// Count by field
const countByRole = await prisma.user.groupBy({
  by: ['role'],
  _count: true,
});
// Returns: [{ role: 'USER', _count: 150 }, { role: 'ADMIN', _count: 5 }]

// Return type: number
```

##### aggregate (Aggregate Functions)

```typescript
// Get aggregates
const stats = await prisma.post.aggregate({
  _avg: { viewCount: true },
  _sum: { viewCount: true },
  _max: { viewCount: true },
  _min: { viewCount: true },
  _count: true,
});

// Return type: { _avg: { viewCount: number | null }, _sum: { viewCount: number | null }, ... }
```

#### Transaction Operations

##### Sequential Transactions

```typescript
import { prisma } from '@/lib/db';

// Sequential operations in transaction
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'tx@example.com' } }),
  prisma.post.create({ data: { title: 'TX Post', authorId: 'user123' } }),
]);
```

##### Interactive Transactions

```typescript
// Complex transaction with conditional logic
const result = await prisma.$transaction(async (tx) => {
  // Create user
  const user = await tx.user.create({
    data: { email: 'tx-interactive@example.com' },
  });

  // Check if user has profile
  const existingProfile = await tx.profile.findUnique({
    where: { userId: user.id },
  });

  // Conditionally create profile
  if (!existingProfile) {
    await tx.profile.create({
      data: { userId: user.id, website: 'https://example.com' },
    });
  }

  return user;
});
```

#### Raw SQL Queries

```typescript
import { prisma } from '@/lib/db';

// Raw query (unsafe, prefer Prisma queries)
const users = await prisma.$queryRaw`
  SELECT * FROM users WHERE status = ${'ACTIVE'}
`;

// Execute raw SQL (for mutations)
const result = await prisma.$executeRaw`
  UPDATE users SET status = 'SUSPENDED' WHERE id = ${userId}
`;

// Typed raw query (safer)
import { Prisma } from '@prisma/client';

const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM users WHERE status = ${Prisma.raw('ACTIVE')}
`;
```

### Prisma Studio (Database GUI)

```bash
# Launch Prisma Studio (browser-based GUI)
npx prisma studio

# Opens at http://localhost:5555
# Features:
# - Browse all tables
# - Create/edit/delete records
# - Filter and search
# - View relations
```

**Use Cases**:
- Manual data entry
- Quick database inspection
- Testing queries visually
- Debugging data issues

### Type Generation

```bash
# Generate Prisma Client (auto-typed from schema)
npx prisma generate

# Triggers automatically after:
# - npx prisma migrate dev
# - npm install (via postinstall hook)
```

**Generated Types** (example):

```typescript
// node_modules/.prisma/client/index.d.ts

export type User = {
  id: string;
  email: string;
  name: string | null;
  role: UserRole;
  status: UserStatus;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
};

export type Post = {
  id: string;
  title: string;
  content: string | null;
  published: boolean;
  authorId: string;
  createdAt: Date;
  updatedAt: Date;
};

// Full Prisma Client type
export const prisma: PrismaClient;
```

---

## Drizzle ORM Reference

### Installation

#### 1. Install Dependencies

```bash
# Install Drizzle ORM
npm install drizzle-orm

# Install Drizzle Kit (migrations)
npm install -D drizzle-kit

# Install PostgreSQL driver
npm install postgres
# OR use pg driver
npm install pg
npm install -D @types/pg
```

#### 2. Create Configuration File

```typescript
// drizzle.config.ts

import type { Config } from 'drizzle-kit';

export default {
  schema: './lib/schema.ts',         // Schema location
  out: './drizzle/migrations',        // Migration output
  driver: 'pg',                       // PostgreSQL driver
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

### Schema Syntax

#### Basic Schema Structure

```typescript
// lib/schema.ts

import { pgTable, text, varchar, boolean, timestamp, integer, pgEnum } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2'; // For CUID generation

// Define enums
export const userRoleEnum = pgEnum('user_role', ['USER', 'ADMIN', 'MODERATOR']);
export const userStatusEnum = pgEnum('user_status', ['ACTIVE', 'SUSPENDED', 'DELETED']);

// Tables defined below...
```

#### User Table (Complete Example)

```typescript
import { pgTable, text, varchar, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  // Primary key
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),

  // Unique fields
  email: varchar('email', { length: 255 })
    .notNull()
    .unique(),
  username: varchar('username', { length: 100 })
    .unique(),

  // Profile fields
  name: varchar('name', { length: 255 }),
  bio: text('bio'),
  avatar: varchar('avatar', { length: 255 }),

  // Enums
  role: userRoleEnum('role')
    .default('USER')
    .notNull(),
  status: userStatusEnum('status')
    .default('ACTIVE')
    .notNull(),

  // Timestamps
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
  deletedAt: timestamp('deleted_at'), // Soft delete
});

// Define relations
export const usersRelations = relations(users, ({ many, one }) => ({
  posts: many(posts),
  comments: many(comments),
  profile: one(profiles, {
    fields: [users.id],
    references: [profiles.userId],
  }),
}));
```

#### Post Table (With Relations)

```typescript
import { pgTable, text, varchar, boolean, timestamp, integer } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),

  // Content fields
  title: varchar('title', { length: 255 })
    .notNull(),
  slug: varchar('slug', { length: 255 })
    .notNull()
    .unique(),
  content: text('content'),
  excerpt: varchar('excerpt', { length: 500 }),

  // Publishing
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
  deletedAt: timestamp('deleted_at'),
});

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  comments: many(comments),
  tagsOnPosts: many(tagsOnPosts),
}));
```

#### Comment Table (Nested Relations)

```typescript
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

  // Self-referencing (replies)
  parentId: text('parent_id')
    .references(() => comments.id, { onDelete: 'cascade' }),

  // Timestamps
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
  deletedAt: timestamp('deleted_at'),
});

export const commentsRelations = relations(comments, ({ one, many }) => ({
  author: one(users, {
    fields: [comments.authorId],
    references: [users.id],
  }),
  post: one(posts, {
    fields: [comments.postId],
    references: [posts.id],
  }),
  parent: one(comments, {
    fields: [comments.parentId],
    references: [comments.id],
    relationName: 'replies',
  }),
  replies: many(comments, {
    relationName: 'replies',
  }),
}));
```

#### Profile Table (One-to-One)

```typescript
export const profiles = pgTable('profiles', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),

  // Profile data
  website: varchar('website', { length: 255 }),
  location: varchar('location', { length: 255 }),
  company: varchar('company', { length: 255 }),

  // One-to-one relation
  userId: text('user_id')
    .notNull()
    .unique()
    .references(() => users.id, { onDelete: 'cascade' }),

  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at')
    .defaultNow()
    .notNull(),
});

export const profilesRelations = relations(profiles, ({ one }) => ({
  user: one(users, {
    fields: [profiles.userId],
    references: [users.id],
  }),
}));
```

#### Many-to-Many Relation (Join Table)

```typescript
export const tags = pgTable('tags', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  name: varchar('name', { length: 100 })
    .notNull()
    .unique(),
  slug: varchar('slug', { length: 100 })
    .notNull()
    .unique(),
  createdAt: timestamp('created_at')
    .defaultNow()
    .notNull(),
});

export const tagsOnPosts = pgTable('tags_on_posts', {
  postId: text('post_id')
    .notNull()
    .references(() => posts.id, { onDelete: 'cascade' }),
  tagId: text('tag_id')
    .notNull()
    .references(() => tags.id, { onDelete: 'cascade' }),
  assignedAt: timestamp('assigned_at')
    .defaultNow()
    .notNull(),
}, (table) => ({
  // Composite primary key
  pk: primaryKey({ columns: [table.postId, table.tagId] }),
}));

export const tagsRelations = relations(tags, ({ many }) => ({
  tagsOnPosts: many(tagsOnPosts),
}));

export const tagsOnPostsRelations = relations(tagsOnPosts, ({ one }) => ({
  post: one(posts, {
    fields: [tagsOnPosts.postId],
    references: [posts.id],
  }),
  tag: one(tags, {
    fields: [tagsOnPosts.tagId],
    references: [tags.id],
  }),
}));
```

### Migration Commands

#### Generate Migration

```bash
# Generate migration from schema changes
npx drizzle-kit generate:pg

# Output: drizzle/migrations/0000_initial_schema.sql
```

**Generated Migration File** (example):

```sql
-- drizzle/migrations/0000_initial_schema.sql

CREATE TYPE "user_role" AS ENUM('USER', 'ADMIN', 'MODERATOR');
CREATE TYPE "user_status" AS ENUM('ACTIVE', 'SUSPENDED', 'DELETED');

CREATE TABLE IF NOT EXISTS "users" (
	"id" text PRIMARY KEY NOT NULL,
	"email" varchar(255) NOT NULL,
	"username" varchar(100),
	"name" varchar(255),
	"bio" text,
	"avatar" varchar(255),
	"role" "user_role" DEFAULT 'USER' NOT NULL,
	"status" "user_status" DEFAULT 'ACTIVE' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	"deleted_at" timestamp,
	CONSTRAINT "users_email_unique" UNIQUE("email"),
	CONSTRAINT "users_username_unique" UNIQUE("username")
);

CREATE TABLE IF NOT EXISTS "profiles" (
	"id" text PRIMARY KEY NOT NULL,
	"website" varchar(255),
	"location" varchar(255),
	"company" varchar(255),
	"user_id" text NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "profiles_user_id_unique" UNIQUE("user_id")
);

ALTER TABLE "profiles" ADD CONSTRAINT "profiles_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE cascade ON UPDATE no action;
```

#### Apply Migrations

**Option 1: Drizzle Kit Push** (Development):

```bash
# Push schema directly to database (no migration files)
npx drizzle-kit push:pg

# WARNING: Not recommended for production (no migration history)
```

**Option 2: Custom Migration Runner** (Production):

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

  console.log('Running migrations...');
  await migrate(db, { migrationsFolder: './drizzle/migrations' });
  console.log('Migrations complete');

  await sql.end();
};

runMigrations().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

**package.json**:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate:pg",
    "db:migrate": "tsx scripts/migrate.ts"
  }
}
```

**Usage**:

```bash
# Generate migration
npm run db:generate

# Apply migrations
npm run db:migrate
```

### Drizzle Client API

#### Initialize Client (Singleton Pattern)

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

**Usage**:

```typescript
import { db } from '@/lib/db';
import { users } from '@/lib/schema';

// Use db throughout your app
const allUsers = await db.select().from(users);
```

#### Query Operations

##### select (Get Records)

```typescript
import { db } from '@/lib/db';
import { users, posts } from '@/lib/schema';
import { eq, and, or, gte, like, isNull, desc } from 'drizzle-orm';

// Select all users
const allUsers = await db.select().from(users);

// Select specific fields
const userEmails = await db
  .select({
    id: users.id,
    email: users.email,
  })
  .from(users);

// Select with where clause
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.status, 'ACTIVE'));

// Multiple conditions
const filteredUsers = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.status, 'ACTIVE'),
      isNull(users.deletedAt)
    )
  );

// OR conditions
const users = await db
  .select()
  .from(users)
  .where(
    or(
      like(users.email, '%@example.com'),
      like(users.name, 'Alice%')
    )
  );

// With pagination
const paginatedUsers = await db
  .select()
  .from(users)
  .limit(10)
  .offset(0)
  .orderBy(desc(users.createdAt));

// Return type: User[]
```

##### Relational Queries

```typescript
import { db } from '@/lib/db';
import { users } from '@/lib/schema';
import { eq } from 'drizzle-orm';

// Query with relations (using relational query API)
const user = await db.query.users.findFirst({
  where: eq(users.email, 'alice@example.com'),
  with: {
    posts: true,
    profile: true,
  },
});

// Nested relations
const user = await db.query.users.findFirst({
  where: eq(users.id, 'user123'),
  with: {
    posts: {
      with: {
        comments: true,
      },
    },
  },
});

// Return type: User & { posts: Post[], profile: Profile | null }
```

##### insert (Create Records)

```typescript
import { db } from '@/lib/db';
import { users } from '@/lib/schema';

// Insert single record
const [user] = await db
  .insert(users)
  .values({
    email: 'bob@example.com',
    name: 'Bob Smith',
    role: 'USER',
  })
  .returning();

// Insert multiple records
const newUsers = await db
  .insert(users)
  .values([
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ])
  .returning();

// Insert with onConflictDoNothing (skip duplicates)
const result = await db
  .insert(users)
  .values({ email: 'existing@example.com' })
  .onConflictDoNothing()
  .returning();

// Return type: User[]
```

##### update (Modify Records)

```typescript
import { db } from '@/lib/db';
import { users, posts } from '@/lib/schema';
import { eq } from 'drizzle-orm';

// Update single record
const [updatedUser] = await db
  .update(users)
  .set({
    name: 'Updated Name',
    updatedAt: new Date(),
  })
  .where(eq(users.id, 'user123'))
  .returning();

// Update multiple records
const updatedUsers = await db
  .update(users)
  .set({
    status: 'DELETED',
    deletedAt: new Date(),
  })
  .where(eq(users.status, 'SUSPENDED'))
  .returning();

// Increment field (SQL expression)
import { sql } from 'drizzle-orm';

await db
  .update(posts)
  .set({
    viewCount: sql`${posts.viewCount} + 1`,
  })
  .where(eq(posts.id, 'post123'));

// Return type: User[]
```

##### delete (Remove Records)

```typescript
import { db } from '@/lib/db';
import { users } from '@/lib/schema';
import { eq, and, lt } from 'drizzle-orm';

// Delete single record
const [deletedUser] = await db
  .delete(users)
  .where(eq(users.id, 'user123'))
  .returning();

// Delete multiple records
const deletedUsers = await db
  .delete(users)
  .where(
    and(
      eq(users.status, 'DELETED'),
      lt(users.deletedAt, new Date('2024-01-01'))
    )
  )
  .returning();

// Soft delete (recommended)
const [softDeletedUser] = await db
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, 'user123'))
  .returning();

// Return type: User[]
```

#### Transaction Operations

```typescript
import { db } from '@/lib/db';
import { users, posts } from '@/lib/schema';

// Transaction with multiple operations
const result = await db.transaction(async (tx) => {
  // Create user
  const [user] = await tx
    .insert(users)
    .values({ email: 'tx@example.com' })
    .returning();

  // Create post
  const [post] = await tx
    .insert(posts)
    .values({
      title: 'Transaction Post',
      authorId: user.id,
    })
    .returning();

  return { user, post };
});

// If any operation fails, entire transaction rolls back
```

#### Raw SQL Queries

```typescript
import { db } from '@/lib/db';
import { sql } from 'drizzle-orm';

// Raw query
const result = await db.execute(sql`
  SELECT * FROM users WHERE status = ${'ACTIVE'}
`);

// Typed raw query
import { users } from '@/lib/schema';

const activeUsers = await db.execute<typeof users.$inferSelect>(sql`
  SELECT * FROM users WHERE status = 'ACTIVE'
`);
```

---

## Prisma vs Drizzle Comparison

### Performance Comparison

| Metric | Prisma | Drizzle | Difference |
|--------|--------|---------|------------|
| **Query Latency (avg)** | ~50ms | ~30ms | **40% faster** (Drizzle) |
| **Query Latency (p95)** | ~80ms | ~50ms | **37.5% faster** (Drizzle) |
| **Bundle Size** | ~300KB | ~80KB | **73% smaller** (Drizzle) |
| **Cold Start (serverless)** | ~250ms | ~150ms | **40% faster** (Drizzle) |
| **Memory Usage** | ~50MB | ~20MB | **60% lower** (Drizzle) |

**Source**: RT-019 Research Report, benchmarks from Vercel Edge Runtime

**When Performance Matters**:
- **High-throughput apps**: Choose Drizzle (real-time, analytics)
- **Edge-first apps**: Choose Drizzle (Cloudflare Workers, Vercel Edge)
- **Bundle-sensitive**: Choose Drizzle (client-side apps with SSR)
- **Moderate workloads**: Either ORM acceptable

---

### Developer Experience Comparison

| Aspect | Prisma | Drizzle | Winner |
|--------|--------|---------|--------|
| **Schema Syntax** | Declarative (`.prisma` DSL) | TypeScript (code-first) | Prisma |
| **Database GUI** | Prisma Studio (built-in) | None (use pgAdmin/TablePlus) | Prisma |
| **Type Generation** | Auto-generated (`npx prisma generate`) | Inferred from schema | Tie |
| **Documentation** | Excellent, comprehensive | Good, growing | Prisma |
| **Community** | 1.5M weekly downloads | 200K+ weekly downloads | Prisma |
| **Learning Curve** | Low (intuitive) | Medium (SQL knowledge helpful) | Prisma |
| **Migration DX** | `npx prisma migrate dev` (seamless) | Custom script needed | Prisma |
| **SQL Transparency** | Hidden (abstracted) | Exposed (visible) | Drizzle |
| **Query Builder** | Method chaining (intuitive) | SQL-like (explicit) | Preference |

**When DX Matters**:
- **Junior developers**: Choose Prisma (lower learning curve)
- **Need admin UI**: Choose Prisma (Prisma Studio)
- **SQL experts**: Choose Drizzle (SQL transparency helps optimization)
- **Large teams**: Choose Prisma (better docs, larger community)

---

### Feature Comparison

| Feature | Prisma | Drizzle | Notes |
|---------|--------|---------|-------|
| **PostgreSQL Support** | ✅ Full | ✅ Full | Both excellent |
| **MySQL Support** | ✅ Full | ✅ Full | Both excellent |
| **SQLite Support** | ✅ Full | ✅ Full | Both excellent |
| **MongoDB Support** | ✅ Full | ❌ No | Prisma only |
| **Edge Runtime** | ✅ (Prisma Accelerate) | ✅ Native | Drizzle slightly better |
| **Connection Pooling** | ✅ (Accelerate, external) | ✅ (pg-pool, external) | Both need external service |
| **Migrations** | ✅ Built-in | ✅ Via drizzle-kit | Prisma more seamless |
| **Type Safety** | ✅ Excellent | ✅ Excellent | Both excellent |
| **Transactions** | ✅ Interactive | ✅ Standard | Prisma more flexible |
| **Raw SQL** | ✅ `$queryRaw` | ✅ `db.execute` | Both supported |
| **Soft Deletes** | ✅ Manual pattern | ✅ Manual pattern | Both require custom impl |
| **Database GUI** | ✅ Prisma Studio | ❌ None | Prisma major advantage |
| **Schema Introspection** | ✅ `npx prisma db pull` | ✅ `drizzle-kit introspect` | Both supported |

---

### Decision Matrix

Use this table to choose between Prisma and Drizzle:

| Your Priority | Recommended ORM | Reason |
|---------------|-----------------|--------|
| **Raw performance** | Drizzle | 40% faster queries, 73% smaller bundle |
| **Developer experience** | Prisma | Prisma Studio, better docs, lower learning curve |
| **Edge runtime** | Drizzle | Better cold start times, native edge support |
| **Team is SQL-savvy** | Drizzle | SQL transparency helps optimization |
| **Team is SQL-novice** | Prisma | Abstraction hides SQL complexity |
| **Need admin UI** | Prisma | Prisma Studio included |
| **Bundle size critical** | Drizzle | 73% smaller bundle (80KB vs 300KB) |
| **Large community** | Prisma | 1.5M vs 200K weekly downloads |
| **Production stability** | Tie | Both production-proven (Vercel, Supabase) |

**Default Recommendation**:
- **Choose Prisma** if: DX > performance, need admin UI, team new to SQL
- **Choose Drizzle** if: Performance critical, edge-first, SQL-comfortable team

---

## Common Patterns

### 1. Timestamps (createdAt, updatedAt)

**Prisma**:

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt  // Auto-updates on every change
}
```

**Drizzle**:

```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: varchar('email', { length: 255 }).notNull().unique(),

  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
  // Note: Drizzle doesn't auto-update updatedAt, must set manually
});

// Manual update pattern
await db
  .update(users)
  .set({
    email: 'newemail@example.com',
    updatedAt: new Date(), // Manually set
  })
  .where(eq(users.id, userId));
```

**Recommendation**: Prisma's `@updatedAt` is more ergonomic, but Drizzle's manual approach gives control.

---

### 2. Soft Deletes (deletedAt)

**Prisma**:

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  deletedAt DateTime?  // Nullable = not deleted
}
```

**Query Pattern**:

```typescript
// Soft delete
await prisma.user.update({
  where: { id: userId },
  data: { deletedAt: new Date() },
});

// Exclude soft-deleted records
const activeUsers = await prisma.user.findMany({
  where: { deletedAt: null },
});

// Global middleware (exclude soft-deleted by default)
prisma.$use(async (params, next) => {
  if (params.action === 'findMany' && params.model === 'User') {
    params.args.where = {
      ...params.args.where,
      deletedAt: null,
    };
  }
  return next(params);
});
```

**Drizzle**:

```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  deletedAt: timestamp('deleted_at'), // Nullable
});

// Soft delete
await db
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, userId));

// Exclude soft-deleted records
const activeUsers = await db
  .select()
  .from(users)
  .where(isNull(users.deletedAt));
```

---

### 3. Row-Level Security (RLS) with Supabase

**PostgreSQL RLS Policies** (applies to both Prisma and Drizzle):

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only SELECT their own posts
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = author_id);

-- Policy: Users can only INSERT posts as themselves
CREATE POLICY "Users can create own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = author_id);

-- Policy: Users can UPDATE their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = author_id);

-- Policy: Users can DELETE their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = author_id);
```

**Prisma Integration** (via raw SQL migration):

```bash
# Create migration file
npx prisma migrate dev --create-only --name add_rls_policies

# Edit migration file: prisma/migrations/XXX_add_rls_policies/migration.sql
# Add RLS SQL from above

# Apply migration
npx prisma migrate dev
```

**Drizzle Integration** (custom migration):

```sql
-- drizzle/migrations/0001_add_rls.sql

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = author_id);

-- ... (rest of policies)
```

**Application Code** (set Supabase user context):

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// RLS automatically enforced when using Supabase client
const { data: posts } = await supabase
  .from('posts')
  .select('*'); // Only returns user's own posts (RLS enforced)
```

**For non-Supabase PostgreSQL** (use session variables):

```typescript
// Set user context before query
await prisma.$executeRaw`
  SET LOCAL app.current_user_id = ${userId};
`;

// RLS policy uses app.current_user_id
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (author_id = current_setting('app.current_user_id')::text);
```

---

### 4. Indexes for Performance

**Prisma**:

```prisma
model User {
  id       String @id @default(cuid())
  email    String @unique  // Auto-creates unique index
  username String? @unique

  // Single-column index
  @@index([email])

  // Composite index
  @@index([status, createdAt])
}
```

**Drizzle**:

```typescript
import { pgTable, text, varchar, index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(), // Auto-index
  username: varchar('username', { length: 100 }).unique(),
  status: varchar('status', { length: 50 }),
  createdAt: timestamp('created_at').defaultNow(),
}, (table) => ({
  // Single-column index
  emailIdx: index('email_idx').on(table.email),

  // Composite index
  statusCreatedIdx: index('status_created_idx').on(table.status, table.createdAt),
}));
```

**When to Add Indexes**:
- ✅ Foreign keys (auto-indexed by Prisma, manual in Drizzle)
- ✅ Columns used in WHERE clauses
- ✅ Columns used in ORDER BY
- ✅ Columns used in JOIN conditions
- ❌ Small tables (<1000 rows)
- ❌ Write-heavy columns (indexes slow down INSERTs)

---

### 5. Enums (Database-Backed)

**Prisma**:

```prisma
enum UserRole {
  USER
  ADMIN
  MODERATOR
}

model User {
  id   String   @id @default(cuid())
  role UserRole @default(USER)
}
```

**Drizzle**:

```typescript
import { pgEnum } from 'drizzle-orm/pg-core';

export const userRoleEnum = pgEnum('user_role', ['USER', 'ADMIN', 'MODERATOR']);

export const users = pgTable('users', {
  id: text('id').primaryKey(),
  role: userRoleEnum('role').default('USER').notNull(),
});
```

**TypeScript Integration**:

```typescript
// Prisma (auto-generated)
import { UserRole } from '@prisma/client';

const role: UserRole = 'ADMIN'; // Type-safe

// Drizzle (inferred)
import { users } from '@/lib/schema';

type UserRole = typeof users.role.enumValues[number]; // 'USER' | 'ADMIN' | 'MODERATOR'
```

---

### 6. One-to-One Relations

**Prisma**:

```prisma
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  userId String @unique  // Unique ensures one-to-one
  user   User   @relation(fields: [userId], references: [id])
}
```

**Drizzle**:

```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey(),
});

export const profiles = pgTable('profiles', {
  id: text('id').primaryKey(),
  userId: text('user_id')
    .notNull()
    .unique() // Unique ensures one-to-one
    .references(() => users.id),
});

export const usersRelations = relations(users, ({ one }) => ({
  profile: one(profiles, {
    fields: [users.id],
    references: [profiles.userId],
  }),
}));
```

---

### 7. One-to-Many Relations

**Prisma**:

```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  authorId String
  author   User   @relation(fields: [authorId], references: [id])
}
```

**Drizzle**:

```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey(),
});

export const posts = pgTable('posts', {
  id: text('id').primaryKey(),
  authorId: text('author_id')
    .notNull()
    .references(() => users.id),
});

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

---

### 8. Many-to-Many Relations

**Prisma** (implicit join table):

```prisma
model Post {
  id   String @id @default(cuid())
  tags Tag[]
}

model Tag {
  id    String @id @default(cuid())
  posts Post[]
}

// Prisma auto-creates join table: _PostToTag
```

**Prisma** (explicit join table, recommended):

```prisma
model Post {
  id   String       @id @default(cuid())
  tags TagsOnPosts[]
}

model Tag {
  id    String       @id @default(cuid())
  posts TagsOnPosts[]
}

model TagsOnPosts {
  postId String
  post   Post   @relation(fields: [postId], references: [id])

  tagId  String
  tag    Tag    @relation(fields: [tagId], references: [id])

  assignedAt DateTime @default(now())

  @@id([postId, tagId])
}
```

**Drizzle** (explicit join table):

```typescript
export const posts = pgTable('posts', {
  id: text('id').primaryKey(),
});

export const tags = pgTable('tags', {
  id: text('id').primaryKey(),
});

export const tagsOnPosts = pgTable('tags_on_posts', {
  postId: text('post_id')
    .notNull()
    .references(() => posts.id),
  tagId: text('tag_id')
    .notNull()
    .references(() => tags.id),
  assignedAt: timestamp('assigned_at').defaultNow(),
}, (table) => ({
  pk: primaryKey({ columns: [table.postId, table.tagId] }),
}));

export const postsRelations = relations(posts, ({ many }) => ({
  tagsOnPosts: many(tagsOnPosts),
}));

export const tagsRelations = relations(tags, ({ many }) => ({
  tagsOnPosts: many(tagsOnPosts),
}));

export const tagsOnPostsRelations = relations(tagsOnPosts, ({ one }) => ({
  post: one(posts, {
    fields: [tagsOnPosts.postId],
    references: [posts.id],
  }),
  tag: one(tags, {
    fields: [tagsOnPosts.tagId],
    references: [tags.id],
  }),
}));
```

---

## Next.js 15 Integration

### Server Components (Data Fetching)

**Prisma Example**:

```typescript
// app/users/page.tsx (Server Component)

import { prisma } from '@/lib/db';

export default async function UsersPage() {
  // Direct database query in Server Component
  const users = await prisma.user.findMany({
    where: { status: 'ACTIVE' },
    orderBy: { createdAt: 'desc' },
    take: 10,
  });

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

**Drizzle Example**:

```typescript
// app/users/page.tsx (Server Component)

import { db } from '@/lib/db';
import { users } from '@/lib/schema';
import { eq, desc, isNull } from 'drizzle-orm';

export default async function UsersPage() {
  // Direct database query in Server Component
  const allUsers = await db
    .select()
    .from(users)
    .where(
      and(
        eq(users.status, 'ACTIVE'),
        isNull(users.deletedAt)
      )
    )
    .orderBy(desc(users.createdAt))
    .limit(10);

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {allUsers.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

### Server Actions (Mutations)

**Prisma Example**:

```typescript
// app/actions/users.ts

'use server';

import { prisma } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const email = formData.get('email') as string;
  const name = formData.get('name') as string;

  // Create user
  const user = await prisma.user.create({
    data: { email, name },
  });

  // Revalidate users page
  revalidatePath('/users');

  return user;
}

export async function updateUser(userId: string, formData: FormData) {
  const name = formData.get('name') as string;

  const user = await prisma.user.update({
    where: { id: userId },
    data: { name, updatedAt: new Date() },
  });

  revalidatePath('/users');
  return user;
}

export async function deleteUser(userId: string) {
  // Soft delete
  await prisma.user.update({
    where: { id: userId },
    data: { deletedAt: new Date() },
  });

  revalidatePath('/users');
}
```

**Usage in Client Component**:

```typescript
// app/users/create-form.tsx

'use client';

import { createUser } from '@/app/actions/users';
import { useActionState } from 'react';

export function CreateUserForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState: any, formData: FormData) => {
      try {
        await createUser(formData);
        return { success: true };
      } catch (error) {
        return { error: error.message };
      }
    },
    { success: false }
  );

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      <input name="name" type="text" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
      {state.error && <p>Error: {state.error}</p>}
    </form>
  );
}
```

**Drizzle Example**:

```typescript
// app/actions/users.ts

'use server';

import { db } from '@/lib/db';
import { users } from '@/lib/schema';
import { eq } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const email = formData.get('email') as string;
  const name = formData.get('name') as string;

  const [user] = await db
    .insert(users)
    .values({ email, name })
    .returning();

  revalidatePath('/users');
  return user;
}

export async function updateUser(userId: string, formData: FormData) {
  const name = formData.get('name') as string;

  const [user] = await db
    .update(users)
    .set({ name, updatedAt: new Date() })
    .where(eq(users.id, userId))
    .returning();

  revalidatePath('/users');
  return user;
}

export async function deleteUser(userId: string) {
  // Soft delete
  await db
    .update(users)
    .set({ deletedAt: new Date() })
    .where(eq(users.id, userId));

  revalidatePath('/users');
}
```

---

## Production Configuration

### Connection Pooling

**Why Connection Pooling?**
- **Serverless environments** (Vercel, AWS Lambda) create new connections per request
- **PostgreSQL** has limited connection slots (~100 default)
- **Without pooling**: Exhaust connections under load → "too many clients" errors

**Option 1: Prisma Accelerate** (Prisma only):

```bash
# Install Prisma Accelerate extension
npm install @prisma/extension-accelerate
```

```typescript
// lib/db.ts

import { PrismaClient } from '@prisma/client';
import { withAccelerate } from '@prisma/extension-accelerate';

export const prisma = new PrismaClient().$extends(withAccelerate());
```

**.env.production**:

```bash
# Use Prisma Accelerate connection string
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=YOUR_API_KEY"
```

**Option 2: Supabase Pooler** (both Prisma and Drizzle):

**.env.production**:

```bash
# Use Supabase connection pooler
DATABASE_URL="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Direct connection (for migrations)
POSTGRES_URL_NON_POOLING="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.compute.amazonaws.com:5432/postgres"
```

**Prisma Config**:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")          // Pooled connection
  directUrl = env("POSTGRES_URL_NON_POOLING")  // Direct connection for migrations
}
```

**Option 3: External Pooler** (PgBouncer, both ORMs):

```bash
# Install pg-pool
npm install pg-pool
```

```typescript
// lib/db.ts (Drizzle example)

import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Maximum connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const db = drizzle(pool, { schema });
```

---

### Edge Runtime Compatibility

**Prisma with Edge Runtime**:

```typescript
// lib/db-edge.ts

import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const adapter = new PrismaPg(pool);

export const prisma = new PrismaClient({ adapter });
```

**Drizzle with Edge Runtime** (native support):

```typescript
// lib/db-edge.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

// postgres-js works natively in edge runtime
const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });
```

**Next.js Route Handler** (Edge Runtime):

```typescript
// app/api/users/route.ts

import { db } from '@/lib/db-edge';
import { users } from '@/lib/schema';

export const runtime = 'edge'; // Enable edge runtime

export async function GET() {
  const allUsers = await db.select().from(users);
  return Response.json(allUsers);
}
```

---

### Environment Variables

**.env.local** (Development):

```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb?schema=public"

# Optional: Direct connection (for Prisma migrations with pooling)
POSTGRES_URL_NON_POOLING="postgresql://postgres:password@localhost:5432/mydb"
```

**.env.production** (Production):

```bash
# Use connection pooler
DATABASE_URL="postgresql://user:password@host:6543/db" # Pooled

# Direct connection (migrations only)
POSTGRES_URL_NON_POOLING="postgresql://user:password@host:5432/db" # Direct
```

**Vercel Configuration**:

```bash
# Set environment variables in Vercel dashboard
# Production: DATABASE_URL, POSTGRES_URL_NON_POOLING
# Preview: DATABASE_URL (use branch-specific database)
```

---

### CI/CD Migration Workflow

**GitHub Actions** (example):

```yaml
# .github/workflows/deploy.yml

name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm install

      # Prisma migrations
      - name: Run Prisma migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: ${{ secrets.POSTGRES_URL_NON_POOLING }}

      # OR Drizzle migrations
      - name: Run Drizzle migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: ${{ secrets.POSTGRES_URL_NON_POOLING }}

      - name: Build application
        run: npm run build

      - name: Deploy to Vercel
        run: vercel deploy --prod
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
```

---

## Troubleshooting

### Common Prisma Issues

#### Issue 1: "Can't reach database server"

**Symptom**:
```
Error: Can't reach database server at `localhost:5432`
```

**Solutions**:
1. Check PostgreSQL is running: `psql -U postgres -h localhost`
2. Verify DATABASE_URL in `.env`: `echo $DATABASE_URL`
3. Check firewall/network: `telnet localhost 5432`
4. For Docker: Ensure container is running and port is exposed

#### Issue 2: "Prisma Client not generated"

**Symptom**:
```
Error: @prisma/client did not initialize yet
```

**Solutions**:
```bash
# Regenerate Prisma Client
npx prisma generate

# Or run full migration
npx prisma migrate dev
```

#### Issue 3: "Migration conflict"

**Symptom**:
```
Error: Migration `20250109_add_field` failed to apply
```

**Solutions**:
```bash
# Option 1: Reset database (development only)
npx prisma migrate reset

# Option 2: Resolve migration manually
npx prisma migrate resolve --applied 20250109_add_field

# Option 3: Delete migration file and regenerate
rm -rf prisma/migrations/20250109_add_field
npx prisma migrate dev --name add_field
```

---

### Common Drizzle Issues

#### Issue 1: "Relation not found"

**Symptom**:
```
Error: Cannot find relation "users"
```

**Solutions**:
```bash
# Generate migration
npx drizzle-kit generate:pg

# Apply migration
npm run db:migrate

# Or push schema directly (dev only)
npx drizzle-kit push:pg
```

#### Issue 2: "Type inference not working"

**Symptom**: TypeScript can't infer types from Drizzle schema

**Solutions**:
```typescript
// Ensure you're using relational query API
const user = await db.query.users.findFirst({
  with: { posts: true },
});

// NOT the select API (requires manual typing)
const user = await db.select().from(users); // Type: User[]
```

#### Issue 3: "Migration failed to apply"

**Symptom**: SQL error when running migrations

**Solutions**:
```bash
# Check migration file for errors
cat drizzle/migrations/0000_initial.sql

# Manually apply SQL (if valid)
psql $DATABASE_URL -f drizzle/migrations/0000_initial.sql

# Or regenerate migration
rm -rf drizzle/migrations/*
npx drizzle-kit generate:pg
```

---

### Performance Debugging

**Enable Query Logging** (Prisma):

```typescript
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

// Output includes SQL queries with execution time
```

**Enable Query Logging** (Drizzle):

```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const client = postgres(process.env.DATABASE_URL!, {
  onnotice: (notice) => console.log('NOTICE:', notice),
});

export const db = drizzle(client, {
  schema,
  logger: true, // Log all queries
});
```

**Analyze Slow Queries**:

```sql
-- PostgreSQL: Enable slow query logging
ALTER DATABASE mydb SET log_min_duration_statement = 100; -- Log queries >100ms

-- View query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

---

## References

### Documentation

- **Prisma**: https://www.prisma.io/docs
- **Drizzle**: https://orm.drizzle.team/docs
- **Next.js 15**: https://nextjs.org/docs
- **PostgreSQL**: https://www.postgresql.org/docs
- **Supabase**: https://supabase.com/docs

### Related SAPs

- **SAP-020**: React Project Foundation (prerequisite)
- **SAP-023**: React State Management (integration)
- **SAP-033**: React Authentication (user context)
- **SAP-041**: Form Validation (Server Actions)
- **SAP-030**: Data Fetching Patterns (client-side caching)

---

**End of Protocol Specification**
