# SAP-034: React Database Integration - Advanced Workflows

**SAP**: SAP-034 (react-database-integration)
**Domain**: Workflows
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **3 advanced database workflows** for Next.js 15+ projects:

1. Create and Run Migrations (10 min) - Schema changes
2. Implement Type-Safe Queries (15 min) - CRUD operations
3. Add Row-Level Security (20 min) - Multi-tenant security

**For ORM setup** (Prisma, Drizzle), see [../providers/AGENTS.md](../providers/AGENTS.md)

**For common patterns** (seeding, pooling, soft deletes), see [../patterns/AGENTS.md](../patterns/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Workflow 3: Create and Run Migrations (10 min)

**Time**: 10 minutes

**Goal**: Add new fields/tables to schema and safely migrate database

**Scenario**: Add a `bio` field to users and create a new `Comment` model

---

### Prisma Migration Workflow (5 min)

#### Step 1: Update Schema

Edit `prisma/schema.prisma`:

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  bio       String?  @db.Text  // NEW FIELD
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts     Post[]
  comments  Comment[]  // NEW RELATION

  @@map("users")
}

// NEW MODEL
model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text

  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([postId])
  @@map("comments")
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)

  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  comments  Comment[]  // NEW RELATION

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}
```

#### Step 2: Create Migration

```bash
# Create migration
npx prisma migrate dev --name add_bio_and_comments

# What happens:
# 1. Generates SQL migration file
# 2. Applies migration to database
# 3. Regenerates Prisma Client
```

**Generated Migration** (`prisma/migrations/XXX_add_bio_and_comments/migration.sql`):

```sql
-- AlterTable
ALTER TABLE "users" ADD COLUMN "bio" TEXT;

-- CreateTable
CREATE TABLE "comments" (
    "id" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "author_id" TEXT NOT NULL,
    "post_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "comments_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "comments_author_id_idx" ON "comments"("author_id");
CREATE INDEX "comments_post_id_idx" ON "comments"("post_id");

-- AddForeignKey
ALTER TABLE "comments" ADD CONSTRAINT "comments_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "comments" ADD CONSTRAINT "comments_post_id_fkey" FOREIGN KEY ("post_id") REFERENCES "posts"("id") ON DELETE CASCADE ON UPDATE CASCADE;
```

#### Step 3: Verify Migration

```bash
# Open Prisma Studio
npx prisma studio

# Verify:
# - "users" table has "bio" column
# - "comments" table exists with correct schema
```

---

### Drizzle Migration Workflow (5 min)

#### Step 1: Update Schema

Edit `lib/schema.ts`:

```typescript
// lib/schema.ts

import { pgTable, text, varchar, boolean, timestamp } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2';

// User table
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 255 }),
  bio: text('bio'), // NEW FIELD
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Post table
export const posts = pgTable('posts', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  title: varchar('title', { length: 255 }).notNull(),
  content: text('content'),
  published: boolean('published').default(false).notNull(),
  authorId: text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// NEW TABLE: Comment
export const comments = pgTable('comments', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  content: text('content').notNull(),
  authorId: text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  postId: text('post_id').notNull().references(() => posts.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments), // NEW RELATION
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
  comments: many(comments), // NEW RELATION
}));

export const commentsRelations = relations(comments, ({ one }) => ({
  author: one(users, { fields: [comments.authorId], references: [users.id] }),
  post: one(posts, { fields: [comments.postId], references: [posts.id] }),
}));
```

#### Step 2: Generate Migration

```bash
# Generate migration from schema changes
npm run db:generate

# Output: drizzle/migrations/0001_add_bio_and_comments.sql
```

**Generated Migration** (`drizzle/migrations/0001_add_bio_and_comments.sql`):

```sql
-- Add bio column to users
ALTER TABLE "users" ADD COLUMN "bio" text;

-- Create comments table
CREATE TABLE IF NOT EXISTS "comments" (
	"id" text PRIMARY KEY NOT NULL,
	"content" text NOT NULL,
	"author_id" text NOT NULL,
	"post_id" text NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);

-- Add foreign keys
ALTER TABLE "comments" ADD CONSTRAINT "comments_author_id_users_id_fk" FOREIGN KEY ("author_id") REFERENCES "users"("id") ON DELETE cascade ON UPDATE no action;
ALTER TABLE "comments" ADD CONSTRAINT "comments_post_id_posts_id_fk" FOREIGN KEY ("post_id") REFERENCES "posts"("id") ON DELETE cascade ON UPDATE no action;
```

#### Step 3: Apply Migration

```bash
# Apply migration
npm run db:migrate

# Expected: "✅ Migrations complete"
```

#### Step 4: Verify Migration

```bash
# Connect to database (psql)
psql $DATABASE_URL

# Verify schema
\d users;    -- Should show "bio" column
\d comments; -- Should show comments table

# Exit psql
\q
```

**Total Time**: 10 minutes (5 min Prisma OR 5 min Drizzle)

---

## Workflow 4: Implement Type-Safe Queries (15 min)

**Time**: 15 minutes

**Goal**: Create Server Actions for CRUD operations with full TypeScript type safety

---

### Prisma Type-Safe Queries (7 min)

#### Step 1: Create Server Actions File

Create `app/actions/posts.ts`:

```typescript
// app/actions/posts.ts

'use server';

import { prisma } from '@/lib/db';
import { revalidatePath } from 'next/cache';

// CREATE: Create new post
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  const authorId = formData.get('authorId') as string;

  // Type-safe insert (TypeScript knows all User fields)
  const post = await prisma.post.create({
    data: {
      title,
      content,
      authorId,
    },
    include: {
      author: true, // Auto-typed as Post & { author: User }
    },
  });

  revalidatePath('/posts');
  return post;
}

// READ: Get all posts
export async function getPosts() {
  const posts = await prisma.post.findMany({
    where: { published: true },
    include: {
      author: {
        select: { id: true, name: true, email: true },
      },
      _count: {
        select: { comments: true },
      },
    },
    orderBy: { createdAt: 'desc' },
  });

  // Return type: Post & { author: { id, name, email }, _count: { comments: number } }[]
  return posts;
}

// READ: Get single post
export async function getPost(id: string) {
  const post = await prisma.post.findUnique({
    where: { id },
    include: {
      author: true,
      comments: {
        include: {
          author: true,
        },
        orderBy: { createdAt: 'desc' },
      },
    },
  });

  if (!post) {
    throw new Error('Post not found');
  }

  return post;
}

// UPDATE: Update post
export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await prisma.post.update({
    where: { id },
    data: {
      title,
      content,
      updatedAt: new Date(),
    },
  });

  revalidatePath('/posts');
  revalidatePath(`/posts/${id}`);
  return post;
}

// DELETE: Delete post
export async function deletePost(id: string) {
  await prisma.post.delete({
    where: { id },
  });

  revalidatePath('/posts');
}

// PUBLISH: Publish post
export async function publishPost(id: string) {
  const post = await prisma.post.update({
    where: { id },
    data: {
      published: true,
    },
  });

  revalidatePath('/posts');
  return post;
}
```

#### Step 2: Use in Server Component

Create `app/posts/page.tsx`:

```typescript
// app/posts/page.tsx

import { getPosts } from '@/app/actions/posts';

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>By {post.author.name}</p>
            <p>{post._count.comments} comments</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Total Time (Prisma)**: 7 minutes

---

### Drizzle Type-Safe Queries (8 min)

#### Step 1: Create Server Actions File

Create `app/actions/posts.ts`:

```typescript
// app/actions/posts.ts

'use server';

import { db } from '@/lib/db';
import { posts, users, comments } from '@/lib/schema';
import { eq, desc, and } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';

// CREATE: Create new post
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  const authorId = formData.get('authorId') as string;

  // Type-safe insert
  const [post] = await db
    .insert(posts)
    .values({
      title,
      content,
      authorId,
    })
    .returning();

  revalidatePath('/posts');
  return post;
}

// READ: Get all posts (with relations)
export async function getPosts() {
  const allPosts = await db.query.posts.findMany({
    where: eq(posts.published, true),
    with: {
      author: {
        columns: { id: true, name: true, email: true },
      },
    },
    orderBy: desc(posts.createdAt),
  });

  // Return type: Post & { author: Pick<User, 'id' | 'name' | 'email'> }[]
  return allPosts;
}

// READ: Get single post
export async function getPost(id: string) {
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, id),
    with: {
      author: true,
      comments: {
        with: {
          author: true,
        },
        orderBy: desc(comments.createdAt),
      },
    },
  });

  if (!post) {
    throw new Error('Post not found');
  }

  return post;
}

// UPDATE: Update post
export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const [post] = await db
    .update(posts)
    .set({
      title,
      content,
      updatedAt: new Date(),
    })
    .where(eq(posts.id, id))
    .returning();

  revalidatePath('/posts');
  revalidatePath(`/posts/${id}`);
  return post;
}

// DELETE: Delete post
export async function deletePost(id: string) {
  await db
    .delete(posts)
    .where(eq(posts.id, id));

  revalidatePath('/posts');
}

// PUBLISH: Publish post
export async function publishPost(id: string) {
  const [post] = await db
    .update(posts)
    .set({
      published: true,
    })
    .where(eq(posts.id, id))
    .returning();

  revalidatePath('/posts');
  return post;
}
```

#### Step 2: Use in Server Component

Create `app/posts/page.tsx`:

```typescript
// app/posts/page.tsx

import { getPosts } from '@/app/actions/posts';

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>By {post.author.name}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Total Time (Drizzle)**: 8 minutes

**Total Time (Either ORM)**: 15 minutes

---

## Workflow 5: Add Row-Level Security (Supabase) (20 min)

**Time**: 20 minutes

**Goal**: Implement Row-Level Security (RLS) policies for multi-tenant application security

**Prerequisites**:
- ✅ Supabase project
- ✅ Prisma or Drizzle configured
- ✅ Authentication configured (see SAP-033)

---

### Step 1: Enable RLS on Tables (5 min)

**Connect to Supabase SQL Editor**:

1. Open Supabase Dashboard → SQL Editor
2. Create new query

**Enable RLS**:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
```

**Verify RLS Enabled**:

```sql
-- Check RLS status
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Expected: rowsecurity = true for users, posts, comments
```

---

### Step 2: Create RLS Policies for Users Table (5 min)

```sql
-- Policy: Users can view all profiles (public data)
CREATE POLICY "Users can view all profiles"
ON users FOR SELECT
USING (true); -- Everyone can read

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile"
ON users FOR UPDATE
USING (auth.uid() = id); -- Only update own row

-- Policy: Users can insert their own profile (during signup)
CREATE POLICY "Users can insert own profile"
ON users FOR INSERT
WITH CHECK (auth.uid() = id);

-- Policy: Users cannot delete profiles (soft delete only via app logic)
-- No DELETE policy = DELETE is denied
```

---

### Step 3: Create RLS Policies for Posts Table (5 min)

```sql
-- Policy: Everyone can view published posts
CREATE POLICY "Anyone can view published posts"
ON posts FOR SELECT
USING (published = true);

-- Policy: Users can view their own unpublished posts
CREATE POLICY "Users can view own unpublished posts"
ON posts FOR SELECT
USING (auth.uid() = author_id);

-- Policy: Users can create posts (as themselves)
CREATE POLICY "Users can create own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = author_id);

-- Policy: Users can update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = author_id);

-- Policy: Users can delete their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = author_id);
```

---

### Step 4: Create RLS Policies for Comments Table (5 min)

```sql
-- Policy: Everyone can view comments on published posts
CREATE POLICY "Anyone can view comments on published posts"
ON comments FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM posts
    WHERE posts.id = comments.post_id
    AND posts.published = true
  )
);

-- Policy: Users can create comments (as themselves)
CREATE POLICY "Users can create own comments"
ON comments FOR INSERT
WITH CHECK (auth.uid() = author_id);

-- Policy: Users can update their own comments
CREATE POLICY "Users can update own comments"
ON comments FOR UPDATE
USING (auth.uid() = author_id);

-- Policy: Users can delete their own comments
CREATE POLICY "Users can delete own comments"
ON comments FOR DELETE
USING (auth.uid() = author_id);
```

---

### Step 5: Test RLS Policies (2 min)

**Test as Authenticated User**:

```sql
-- Simulate authenticated user
SET LOCAL app.current_user_id = 'user-123';

-- Test: Can I see my own unpublished posts?
SELECT * FROM posts WHERE author_id = 'user-123' AND published = false;
-- Expected: Returns posts

-- Test: Can I see other users' unpublished posts?
SELECT * FROM posts WHERE author_id = 'user-456' AND published = false;
-- Expected: Returns empty (RLS blocks)

-- Test: Can I update my own post?
UPDATE posts SET title = 'Updated' WHERE id = 'post-123' AND author_id = 'user-123';
-- Expected: Success

-- Test: Can I update someone else's post?
UPDATE posts SET title = 'Hacked' WHERE id = 'post-456' AND author_id = 'user-456';
-- Expected: 0 rows updated (RLS blocks)
```

---

### ✅ Success Criteria

- ✅ RLS enabled on all tables
- ✅ Users can read public data (published posts)
- ✅ Users can only modify their own data
- ✅ Cross-tenant data leaks prevented (verified via tests)
- ✅ Application code doesn't change (RLS enforced at database level)

**Total Time**: 20 minutes

---

## Version History

**1.0.0 (2025-11-10)** - Initial workflows extraction from awareness-guide.md
- Workflow 3: Create and Run Migrations (10 min)
- Workflow 4: Implement Type-Safe Queries (15 min)
- Workflow 5: Add Row-Level Security (20 min)
- Complete code examples for both Prisma and Drizzle
