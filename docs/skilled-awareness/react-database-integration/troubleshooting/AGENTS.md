# SAP-034: React Database Integration - Troubleshooting

**SAP**: SAP-034 (react-database-integration)
**Domain**: Troubleshooting
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **3 common database issues and fixes** for Next.js 15+ projects.

**Issues Covered**:
1. "Can't reach database server" - Connection errors
2. "Migration conflict" - Migration failures
3. "Type errors after schema change" - TypeScript errors

**For ORM setup** (Prisma, Drizzle), see [../providers/AGENTS.md](../providers/AGENTS.md)

**For advanced workflows** (migrations, queries, RLS), see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For common patterns** (seeding, pooling, soft deletes), see [../patterns/AGENTS.md](../patterns/AGENTS.md)

---

## Issue 1: "Can't reach database server"

**Symptom**: Connection errors when running migrations or queries

**Common Error Messages**:
```
Error: P1001: Can't reach database server at `localhost:5432`
Error: connect ECONNREFUSED 127.0.0.1:5432
Error: getaddrinfo ENOTFOUND db.xxx.supabase.co
```

---

### Solution 1: Check DATABASE_URL

**Verify environment variable**:

```bash
# Check if DATABASE_URL is set
echo $DATABASE_URL

# Expected format:
# postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public

# Example (local):
# postgresql://postgres:password@localhost:5432/mydb?schema=public

# Example (Supabase):
# postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
```

**Common Mistakes**:
- ❌ Missing `postgresql://` protocol
- ❌ Wrong port (5432 for PostgreSQL, 6543 for Supabase pooler)
- ❌ Missing or incorrect password
- ❌ Using `DATABASE_URL` from `.env.example` instead of `.env.local`

**Fix**:

```bash
# Copy .env.example to .env.local
cp .env.example .env.local

# Edit .env.local with correct credentials
vim .env.local
```

---

### Solution 2: Test Connection

**Using psql**:

```bash
# Test connection directly
psql $DATABASE_URL

# If successful, you'll see:
# psql (14.x)
# Type "help" for help.
# postgres=>

# Exit with \q
\q
```

**If psql fails**:
- Check credentials (username, password)
- Verify host is reachable (ping, telnet)
- Check firewall rules

---

### Solution 3: Verify Database Server is Running

**For Supabase**:

1. Open Supabase Dashboard
2. Check project status
3. If paused, click "Resume Project"
4. Wait 30-60 seconds for startup

**For local PostgreSQL** (macOS/Linux):

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql

# Or check status
pg_ctl status

# If not found, install PostgreSQL
brew install postgresql
```

**For local PostgreSQL** (Windows):

```bash
# Check if PostgreSQL service is running
sc query postgresql-x64-14

# Start service
net start postgresql-x64-14
```

---

### Solution 4: Check Docker Container (if using Docker)

```bash
# List running containers
docker ps

# Check if postgres container is running
docker ps | grep postgres

# Start postgres container
docker-compose up -d postgres

# View container logs
docker-compose logs postgres
```

---

## Issue 2: "Migration conflict"

**Symptom**: Migration fails with "already exists" errors

**Common Error Messages**:
```
Error: P3005: Database already contains objects that exist in the migration
Error: relation "users" already exists
Error: column "bio" of relation "users" already exists
```

**Cause**: Database schema doesn't match migration history (e.g., manual SQL changes, partial migrations)

---

### Solution 1: Reset Database (Development Only)

**Prisma**:

```bash
# ⚠️ WARNING: Deletes ALL data
npx prisma migrate reset

# What happens:
# 1. Drops database
# 2. Creates new database
# 3. Applies all migrations from scratch
# 4. Runs seed script (if configured)
```

**Drizzle**:

```bash
# Manually drop all tables
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Regenerate and apply migrations
npm run db:generate
npm run db:migrate
```

---

### Solution 2: Mark Migration as Applied (Prisma)

**When to Use**: Migration already applied manually, but Prisma doesn't know about it

```bash
# List pending migrations
npx prisma migrate status

# Mark specific migration as applied (skip execution)
npx prisma migrate resolve --applied <MIGRATION_NAME>

# Example:
npx prisma migrate resolve --applied 20231115_add_bio_column
```

---

### Solution 3: Delete and Regenerate Migration

**Prisma**:

```bash
# Delete bad migration
rm -rf prisma/migrations/<BAD_MIGRATION_FOLDER>

# Regenerate migration
npx prisma migrate dev --name <NEW_NAME>

# Example:
rm -rf prisma/migrations/20231115_bad_migration
npx prisma migrate dev --name add_bio_column
```

**Drizzle**:

```bash
# Edit migration SQL file manually
vim drizzle/migrations/<MIGRATION_FILE>.sql

# Remove duplicate CREATE TABLE or ADD COLUMN statements
# Save and apply
npm run db:migrate
```

---

### Solution 4: Manual SQL Fix

**When to Use**: Production database with data, can't reset

```bash
# Connect to database
psql $DATABASE_URL

# Check what exists
\d users;

# If "bio" column exists, remove from migration SQL
# If "comments" table exists, skip CREATE TABLE

# Mark Prisma migration as applied
npx prisma migrate resolve --applied <MIGRATION_NAME>
```

---

## Issue 3: "Type errors after schema change"

**Symptom**: TypeScript errors after modifying Prisma/Drizzle schema

**Common Error Messages**:
```
Property 'bio' does not exist on type 'User'
Type '{ email: string; name: string; bio: string; }' is not assignable to type 'UserCreateInput'
Cannot find module '@prisma/client'
```

**Cause**: TypeScript using stale types, Prisma Client not regenerated

---

### Solution 1: Regenerate Prisma Client

**Prisma**:

```bash
# Regenerate Prisma Client
npx prisma generate

# Or run full migration (auto-generates)
npx prisma migrate dev
```

**What happens**:
- Reads `prisma/schema.prisma`
- Generates TypeScript types in `node_modules/.prisma/client`
- Updates `@prisma/client` exports

---

### Solution 2: Restart TypeScript Server (Drizzle)

**VSCode**:

1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "TypeScript: Restart TS Server"
3. Press Enter

**What happens**:
- TypeScript server reloads
- Picks up new types from `lib/schema.ts`
- Clears type cache

**Alternative (if VSCode restart doesn't work)**:

```bash
# Regenerate migration (forces type refresh)
npm run db:generate

# Restart dev server
npm run dev
```

---

### Solution 3: Clear node_modules and Reinstall

**When to Use**: Types still broken after regeneration

```bash
# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install

# Regenerate Prisma Client (if using Prisma)
npx prisma generate

# Restart dev server
npm run dev
```

---

### Solution 4: Check Prisma Client Import

**Common Mistake**: Importing from wrong location

```typescript
// ❌ Wrong (stale types)
import { PrismaClient } from '.prisma/client';

// ✅ Correct (auto-updated types)
import { PrismaClient } from '@prisma/client';
```

**Fix**: Update all imports to use `@prisma/client`

---

## Quick Diagnostics Checklist

**Connection Issues**:
- [ ] DATABASE_URL environment variable set correctly
- [ ] Database server is running (check Supabase dashboard or local PostgreSQL)
- [ ] Firewall allows connection to database port
- [ ] psql connection test succeeds

**Migration Issues**:
- [ ] No manual SQL changes made to database
- [ ] Migration history (`prisma/migrations/` or `drizzle/migrations/`) matches database state
- [ ] No partial migrations (all-or-nothing)

**Type Issues**:
- [ ] Prisma Client regenerated after schema change
- [ ] TypeScript server restarted (VSCode)
- [ ] Dev server restarted
- [ ] Importing from `@prisma/client` (not `.prisma/client`)

---

## Version History

**1.0.0 (2025-11-10)** - Initial troubleshooting extraction from awareness-guide.md
- Issue 1: "Can't reach database server"
- Issue 2: "Migration conflict"
- Issue 3: "Type errors after schema change"
- Complete diagnostics and fixes for both Prisma and Drizzle
