#!/usr/bin/env python3
"""
Add 9 Wave 5 React SAPs to sap-catalog.json

Part of Wave 5 React SAPs completion
Trace ID: WAVE5-COMPLETION
"""

import json
from pathlib import Path

# Wave 5 React SAPs data
WAVE5_SAPS = [
    {
        "id": "SAP-033",
        "name": "react-authentication",
        "full_name": "React Authentication & Authorization",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 185,
        "description": "Production-ready authentication with 4 providers (NextAuth v5, Clerk, Supabase Auth, Auth0) reducing setup from 3-4h to 15min (93.75% time savings), OWASP Top 10 compliance",
        "capabilities": [
            "Multi-provider support (NextAuth v5, Clerk, Supabase Auth, Auth0)",
            "OAuth/social login (50+ providers)",
            "Role-based access control (RBAC)",
            "Protected routes and middleware",
            "Session management and token refresh",
            "OWASP Top 10 compliance (8/10 coverage)",
            "SOC2 certified options"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "authentication", "security", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-authentication",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 2",
        "priority": "P1",
        "domain": "Foundation"
    },
    {
        "id": "SAP-034",
        "name": "react-database-integration",
        "full_name": "React Database Integration",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 220,
        "description": "PostgreSQL integration with Prisma/Drizzle ORM decision framework reducing setup from 3-4h to 25min (89.6% time savings), type-safe queries, Row-Level Security, edge runtime support",
        "capabilities": [
            "Multi-ORM support (Prisma vs Drizzle decision framework)",
            "Type-safe database operations (100% TypeScript inference)",
            "Migration workflows and schema evolution",
            "Connection pooling and edge runtime compatibility",
            "Row-Level Security (RLS) patterns",
            "Server Components and Server Actions integration",
            "Performance optimization (Drizzle 40% faster, 73% smaller bundle)"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "database", "postgresql", "orm", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-database-integration",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 2",
        "priority": "P1",
        "domain": "Foundation"
    },
    {
        "id": "SAP-035",
        "name": "react-file-upload",
        "full_name": "React File Upload & Storage",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 165,
        "description": "File upload with 4 providers (UploadThing, Vercel Blob, Supabase Storage, AWS S3) reducing setup from 6h to 30min (91.7% time savings), security validation, image optimization, CDN delivery",
        "capabilities": [
            "Multi-provider support (UploadThing, Vercel Blob, Supabase Storage, AWS S3)",
            "3-layer security validation (client, server, storage)",
            "Pre-built upload components with progress indicators",
            "Image optimization (Sharp.js: WebP, AVIF, resizing)",
            "Virus scanning and file type validation",
            "CDN delivery and global edge caching",
            "Database metadata storage integration"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "file-upload", "storage", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-file-upload",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 3",
        "priority": "P2",
        "domain": "User-Facing"
    },
    {
        "id": "SAP-036",
        "name": "react-error-handling",
        "full_name": "React Error Handling",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 145,
        "description": "Error boundaries + Sentry monitoring reducing setup from 3-4h to 30min (87.5% time savings), GDPR/CCPA compliant PII scrubbing, retry logic, production error tracking",
        "capabilities": [
            "Next.js 15 error boundaries (error.tsx, global-error.tsx, not-found.tsx)",
            "Sentry production monitoring (<1% overhead, <1min visibility)",
            "GDPR/CCPA compliant PII scrubbing",
            "Error recovery with exponential backoff retry",
            "Toast notifications and user-friendly messages",
            "react-error-boundary for reusable component boundaries"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "error-handling", "monitoring", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-error-handling",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 3",
        "priority": "P2",
        "domain": "User-Facing"
    },
    {
        "id": "SAP-037",
        "name": "react-realtime-synchronization",
        "full_name": "React Real-Time Synchronization",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 175,
        "description": "WebSocket/real-time with 4 providers (Socket.IO, Pusher, Ably, Supabase Realtime) reducing setup from 7h to 30min (92.9% time savings), sub-100ms latency, 100k+ concurrent connections",
        "capabilities": [
            "Multi-provider support (Socket.IO, Pusher, Ably, Supabase Realtime)",
            "Real-time use cases (chat, notifications, collaborative editing, dashboards)",
            "Connection management and auto-reconnection",
            "Presence tracking and channel subscriptions",
            "Sub-100ms latency, 100k+ concurrent connections",
            "Next.js 15 Server Components + client updates integration"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "realtime", "websockets", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-realtime-synchronization",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 4",
        "priority": "P3",
        "domain": "Advanced"
    },
    {
        "id": "SAP-038",
        "name": "react-internationalization",
        "full_name": "React Internationalization (i18n)",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 155,
        "description": "next-intl framework reducing setup from 5h to 30min (90% time savings), 20+ languages, Server Components support, type-safe translations, locale-based routing, SEO optimization",
        "capabilities": [
            "next-intl framework (500k+ weekly downloads)",
            "20+ language support with automatic locale detection",
            "Server Components support (zero client JavaScript)",
            "Type-safe translations with namespace organization",
            "Locale-based routing and SEO (hreflang tags, sitemaps)",
            "Pluralization, variable interpolation, nested keys"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "i18n", "internationalization", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-internationalization",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 4",
        "priority": "P3",
        "domain": "Advanced"
    },
    {
        "id": "SAP-039",
        "name": "react-e2e-testing",
        "full_name": "React E2E Testing",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 140,
        "description": "Playwright E2E testing reducing setup from 3.5h to 30min (85.7% time savings), cross-browser support (Chromium, Firefox, WebKit), parallel execution, CI/CD integration",
        "capabilities": [
            "Playwright framework (7M+ weekly downloads)",
            "Cross-browser testing (Chromium, Firefox, WebKit)",
            "Next.js 15 integration (Server Components, Server Actions, middleware)",
            "Page objects, fixtures, custom matchers",
            "Parallel execution and trace viewer",
            "CI/CD integration (GitHub Actions, screenshot/video artifacts)"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "testing", "e2e", "playwright", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-e2e-testing",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 4",
        "priority": "P3",
        "domain": "Advanced"
    },
    {
        "id": "SAP-040",
        "name": "react-monorepo-architecture",
        "full_name": "React Monorepo Architecture",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 180,
        "description": "Turborepo monorepo reducing setup from 7.5h to 30min (93.3% time savings), incremental builds, remote caching, pnpm workspaces (70% faster, 50% less disk space)",
        "capabilities": [
            "Turborepo framework (1M+ weekly downloads, Vercel-native)",
            "pnpm workspaces (70% faster, 50% less disk space vs npm)",
            "Code sharing (UI components, utilities, types, configs)",
            "Incremental builds and task pipeline caching",
            "Remote cache (Vercel) and dependency graph analysis",
            "Multi-app + multi-package architecture"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "monorepo", "turborepo", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-monorepo-architecture",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 4",
        "priority": "P3",
        "domain": "Advanced"
    },
    {
        "id": "SAP-041",
        "name": "react-form-validation",
        "full_name": "React Form Validation",
        "status": "pilot",
        "version": "1.0.0",
        "included_by_default": False,
        "size_kb": 135,
        "description": "React Hook Form + Zod reducing setup from 2-3h to 20min (88.9% time savings), type-safe validation, WCAG 2.2 Level AA accessibility, 5x fewer re-renders than Formik, 50% smaller bundle",
        "capabilities": [
            "React Hook Form (3M+ weekly downloads, uncontrolled components)",
            "Zod schema validation (100% TypeScript inference)",
            "Server Actions dual validation (client UX + server security)",
            "WCAG 2.2 Level AA accessibility compliance",
            "Performance (5x fewer re-renders than Formik, 50% smaller bundle)",
            "Progressive enhancement (works without JavaScript)"
        ],
        "dependencies": ["SAP-000", "SAP-020"],
        "tags": ["react", "nextjs", "forms", "validation", "technology-specific"],
        "author": "chora-base",
        "location": "docs/skilled-awareness/react-form-validation",
        "artifacts": {
            "capability_charter": True,
            "protocol_spec": True,
            "awareness_guide": True,
            "adoption_blueprint": True,
            "ledger": True
        },
        "system_files": [],
        "phase": "Phase 2",
        "priority": "P1",
        "domain": "Foundation"
    }
]


def add_wave5_saps_to_catalog():
    """Add Wave 5 React SAPs to sap-catalog.json"""
    repo_root = Path(__file__).parent.parent
    catalog_path = repo_root / "sap-catalog.json"

    print(f"Reading {catalog_path}...")
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Check which SAPs already exist
    existing_ids = {sap["id"] for sap in catalog["saps"]}
    new_saps = [sap for sap in WAVE5_SAPS if sap["id"] not in existing_ids]

    if not new_saps:
        print("✅ All Wave 5 SAPs already in catalog")
        return

    print(f"Adding {len(new_saps)} new SAPs to catalog...")

    # Add new SAPs to catalog
    catalog["saps"].extend(new_saps)

    # Update total_saps count
    catalog["total_saps"] = len(catalog["saps"])

    # Update version and timestamp
    catalog["version"] = "5.1.0"  # Bump minor version
    catalog["updated"] = "2025-11-11"

    # Write updated catalog
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add trailing newline

    print(f"\n📊 Summary:")
    print(f"   • Added {len(new_saps)} Wave 5 React SAPs")
    print(f"   • Total SAPs: {catalog['total_saps']}")
    print(f"   • Version: {catalog['version']}")
    print(f"   • Updated: {catalog['updated']}")

    for sap in new_saps:
        print(f"     - {sap['id']}: {sap['full_name']}")

    print(f"\n✅ sap-catalog.json updated successfully!")


if __name__ == "__main__":
    add_wave5_saps_to_catalog()
