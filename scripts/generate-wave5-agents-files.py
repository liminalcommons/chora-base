#!/usr/bin/env python3
"""
Generate AGENTS.md files for Wave 5 React SAPs

Part of Wave 5 React SAPs completion
Trace ID: WAVE5-COMPLETION
"""

import os
from pathlib import Path

# SAP metadata extracted from READMEs
SAP_DATA = {
    "SAP-035": {
        "sap_id": "SAP-035",
        "name": "react-file-upload",
        "title": "React File Upload & Storage",
        "time_savings": "91.7% (6 hours → 30 minutes)",
        "setup_time": "20-30 minutes",
        "key_features": [
            ("Multi-Provider Support", "UploadThing, Vercel Blob, Supabase Storage, AWS S3 with decision framework"),
            ("Security-First", "3-layer validation, virus scanning, upload authorization, signed URLs"),
            ("Pre-Built Components", "UploadThing `<UploadButton>`, `<UploadDropzone>` with progress indicators"),
            ("Image Optimization", "Sharp.js integration (WebP, AVIF, resizing), automatic CDN delivery"),
            ("Production Validation", "UploadThing (10k+ apps), Vercel (native), Supabase (200k+ projects), AWS S3 (enterprise standard)"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-034 (Database), SAP-033 (Auth), SAP-036 (Error Handling)")
        ],
        "integrations": ["SAP-020", "SAP-034", "SAP-033", "SAP-036"],
    },
    "SAP-036": {
        "sap_id": "SAP-036",
        "name": "react-error-handling",
        "title": "React Error Handling",
        "time_savings": "87.5% (3-4 hours → 30 minutes)",
        "setup_time": "30 minutes",
        "key_features": [
            ("Error Boundaries", "Next.js 15 error.tsx, global-error.tsx, not-found.tsx to prevent app crashes"),
            ("Production Monitoring", "Sentry integration (<1% overhead, <1 minute visibility), 14M+ developers"),
            ("Error Recovery", "Retry with exponential backoff, toast notifications, graceful degradation"),
            ("GDPR/CCPA Compliance", "PII scrubbing by default (cookies, headers, emails removed automatically)"),
            ("React Error Boundary", "Reusable component boundaries with fallback UI and error reset"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-034 (Database), SAP-033 (Auth), SAP-035 (File Upload)")
        ],
        "integrations": ["SAP-020", "SAP-034", "SAP-033", "SAP-035"],
    },
    "SAP-037": {
        "sap_id": "SAP-037",
        "name": "react-realtime-synchronization",
        "title": "React Real-Time Synchronization",
        "time_savings": "92.9% (7 hours → 30 minutes)",
        "setup_time": "30-45 minutes",
        "key_features": [
            ("Multi-Provider Support", "Socket.IO (self-hosted), Pusher (managed), Ably (global scale), Supabase Realtime"),
            ("Use Cases", "Live chat, notifications, collaborative editing, real-time dashboards, multiplayer games"),
            ("Production Patterns", "Connection management, reconnection logic, presence tracking, channel subscriptions"),
            ("Performance", "Sub-100ms latency, 100k+ concurrent connections (Pusher/Ably), WebSocket + fallbacks"),
            ("Next.js 15 Integration", "Server Components for initial data, client components for real-time updates"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-034 (Database), SAP-033 (Auth), SAP-023 (State Management)")
        ],
        "integrations": ["SAP-020", "SAP-034", "SAP-033", "SAP-023"],
    },
    "SAP-038": {
        "sap_id": "SAP-038",
        "name": "react-internationalization",
        "title": "React Internationalization (i18n)",
        "time_savings": "90.0% (5 hours → 30 minutes)",
        "setup_time": "30 minutes",
        "key_features": [
            ("next-intl Framework", "Server Components support, type-safe translations, 500k+ weekly downloads"),
            ("Multi-Language Support", "20+ languages, automatic locale detection, locale-based routing"),
            ("Translation Management", "Namespace organization, pluralization, variable interpolation, nested keys"),
            ("SEO Optimization", "Locale-specific URLs, hreflang tags, sitemap generation, metadata localization"),
            ("Performance", "Server-side translations (zero client JavaScript), dynamic locale switching"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-034 (Database), SAP-033 (Auth)")
        ],
        "integrations": ["SAP-020", "SAP-034", "SAP-033"],
    },
    "SAP-039": {
        "sap_id": "SAP-039",
        "name": "react-e2e-testing",
        "title": "React E2E Testing",
        "time_savings": "85.7% (3.5 hours → 30 minutes)",
        "setup_time": "30 minutes",
        "key_features": [
            ("Playwright Framework", "Cross-browser (Chromium, Firefox, WebKit), parallel execution, trace viewer"),
            ("Next.js 15 Integration", "Server Components, Server Actions, middleware, auth flows"),
            ("Test Patterns", "Page objects, fixtures, data-testid selectors, custom matchers"),
            ("CI/CD Integration", "GitHub Actions, parallel sharding, flake detection, screenshot/video artifacts"),
            ("Production Validation", "Microsoft (creator), Vercel (recommended), 7M+ weekly downloads"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-033 (Auth), SAP-034 (Database), SAP-041 (Forms)")
        ],
        "integrations": ["SAP-020", "SAP-033", "SAP-034", "SAP-041"],
    },
    "SAP-040": {
        "sap_id": "SAP-040",
        "name": "react-monorepo-architecture",
        "title": "React Monorepo Architecture",
        "time_savings": "93.3% (7.5 hours → 30 minutes)",
        "setup_time": "30-45 minutes",
        "key_features": [
            ("Turborepo Framework", "Incremental builds, remote caching, parallel execution, Vercel-native"),
            ("Package Management", "pnpm workspaces (70% faster, 50% less disk space vs npm), npm/yarn support"),
            ("Code Sharing", "Shared UI components, utilities, types, configs across apps and packages"),
            ("Build Optimization", "Task pipeline caching, remote cache (Vercel), dependency graph analysis"),
            ("Production Validation", "Vercel (creator), 1M+ weekly downloads, Netflix/Uber scale"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-021 (Testing), SAP-022 (Linting)")
        ],
        "integrations": ["SAP-020", "SAP-021", "SAP-022"],
    },
    "SAP-041": {
        "sap_id": "SAP-041",
        "name": "react-form-validation",
        "title": "React Form Validation",
        "time_savings": "88.9% (2-3 hours → 20 minutes)",
        "setup_time": "20 minutes",
        "key_features": [
            ("React Hook Form", "5x fewer re-renders than Formik, 50% smaller bundle, 3M+ weekly downloads"),
            ("Zod Schema Validation", "Type-safe validation, 100% TypeScript inference, zero manual types"),
            ("Server Actions", "Dual validation (client UX + server security), progressive enhancement"),
            ("Accessibility", "WCAG 2.2 Level AA compliance, screen reader support, keyboard navigation"),
            ("Performance", "Uncontrolled components (no re-renders), async validation, debounced input"),
            ("Integration", "Works with SAP-020 (Foundation), SAP-033 (Auth), SAP-034 (Database)")
        ],
        "integrations": ["SAP-020", "SAP-033", "SAP-034"],
    },
}

AGENTS_TEMPLATE = '''---
sap_id: {sap_id}
version: 1.0.0
status: pilot
last_updated: 2025-11-11
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 20
progressive_loading:
  phase_1: "lines 1-200"   # Quick Reference + Core Workflows
  phase_2: "lines 201-450" # Implementation Patterns
  phase_3: "full"          # Complete including best practices
phase_1_token_estimate: 4000
phase_2_token_estimate: 8500
phase_3_token_estimate: 12000
---

# {title} ({sap_id}) - Agent Awareness

**SAP ID**: {sap_id}
**Last Updated**: 2025-11-11
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to {sap_id}?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - {setup_time} setup with production-ready patterns
- 📚 **Time Savings** - {time_savings} reduction in implementation time
{feature_bullets}
This AGENTS.md provides: Agent-specific patterns for implementing {title_lower} in React/Next.js applications.

---

## Quick Reference

### When to Use

**Use {sap_id} {title} when**:
- Building React/Next.js applications requiring {primary_use_case}
- Need production-ready patterns and best practices
- Want to avoid common pitfalls and security vulnerabilities
- Require type-safe TypeScript integration
- Building scalable, maintainable applications

**Don't use when**:
- Using alternative frameworks (Vue, Svelte, Angular)
- Building simple prototypes without production requirements
- Have existing custom implementation that works well
- Project doesn't require {primary_use_case}

---

## Core Workflows

### Workflow 1: Initial Setup

**Context**: Agent needs to set up {title_lower} in a Next.js 15 project

**Prerequisites**:
- SAP-020 (React Foundation) adopted → Next.js 15 project exists
- Node.js 22.x LTS installed
- TypeScript configured

**Implementation Steps**:

1. **Read the Adoption Blueprint**:
   - [Step-by-step setup guide](./adoption-blueprint.md)
   - Provider-specific instructions (if applicable)
   - Configuration examples

2. **Install Dependencies**:
   - Follow package installation instructions
   - Configure environment variables
   - Set up TypeScript types

3. **Implement Core Patterns**:
   - Follow established workflows
   - Use type-safe patterns
   - Test implementation

4. **Verify Setup**:
   - Run test suite
   - Check TypeScript compilation
   - Validate production build

---

## Integration with Other SAPs

{integration_sections}

---

## Best Practices

### 1. Type Safety

**Always use TypeScript**:
- Leverage type inference
- Avoid `any` types
- Use strict mode

### 2. Error Handling

**Graceful error handling**:
- Try/catch blocks for async operations
- User-friendly error messages
- Error logging and monitoring

### 3. Performance

**Optimize for production**:
- Follow Next.js performance best practices
- Use Server Components where appropriate
- Minimize client-side JavaScript

### 4. Security

**Security-first approach**:
- Validate all user input
- Sanitize data
- Follow OWASP guidelines

---

## Common Pitfalls

### Pitfall 1: Missing Environment Variables

**Symptom**: Configuration errors at runtime

**Fix**:
1. Create `.env.local` in project root
2. Add all required environment variables
3. Restart Next.js dev server
4. Verify `.env.local` is gitignored

---

### Pitfall 2: TypeScript Errors

**Symptom**: Type mismatches or missing types

**Fix**:
1. Ensure all dependencies have types installed
2. Run `npm install` to update type definitions
3. Check TypeScript configuration (tsconfig.json)
4. Restart TypeScript server in IDE

---

## Learn More

### Documentation

- **[Protocol Spec](protocol-spec.md)** - Complete technical reference
- **[Awareness Guide](awareness-guide.md)** - Practical how-to workflows
- **[Adoption Blueprint](adoption-blueprint.md)** - Step-by-step setup guide
- **[Capability Charter](capability-charter.md)** - Problem statement and solution design
- **[Ledger](ledger.md)** - Adoption tracking and production case studies

### Related SAPs

{related_saps}

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Production-ready patterns
  - Next.js 15 integration
  - TypeScript support
  - {time_savings} time savings validation

---

**Quick Links**:
- 🚀 [Initial Setup](#workflow-1-initial-setup) - Get started quickly
- 🔗 [Integration with Other SAPs](#integration-with-other-saps) - Related capabilities
- 💡 [Best Practices](#best-practices) - Production recommendations
- ⚠️ [Common Pitfalls](#common-pitfalls) - Avoid common mistakes
'''


def generate_feature_bullets(features):
    """Generate feature bullet points for Quick Reference"""
    bullets = []
    for i, (emoji_label, description) in enumerate(features, 1):
        bullets.append(f"- {['🎯', '🔧', '📊', '🔗'][min(i-1, 3)]} **{emoji_label}** - {description}")
    return "\n".join(bullets)


def generate_integration_sections(integrations):
    """Generate integration sections"""
    if not integrations:
        return "This SAP works standalone but integrates well with other React SAPs."

    sections = []
    for sap in integrations:
        sections.append(f"### {sap}: Related Capability\n\n**Integration Points**: See [Protocol Spec](protocol-spec.md) for detailed integration patterns.\n")

    return "\n".join(sections)


def generate_related_saps(integrations):
    """Generate related SAPs list"""
    if not integrations:
        return "- **[SAP-020 (React Foundation)](../react-foundation/)** - Next.js 15 baseline"

    sap_names = {
        "SAP-020": "React Foundation",
        "SAP-021": "React Testing",
        "SAP-022": "React Linting",
        "SAP-023": "State Management",
        "SAP-033": "Authentication",
        "SAP-034": "Database Integration",
        "SAP-035": "File Upload",
        "SAP-036": "Error Handling",
        "SAP-041": "Form Validation",
    }

    links = []
    for sap in integrations:
        name = sap_names.get(sap, sap)
        dir_name = SAP_DATA.get(sap, {}).get("name", "unknown")
        if dir_name != "unknown":
            links.append(f"- **[{sap} ({name})](../{dir_name}/)** - Integration point")

    return "\n".join(links) if links else "- **[SAP-020 (React Foundation)](../react-foundation/)** - Next.js 15 baseline"


def generate_agents_md(sap_id):
    """Generate AGENTS.md content for a SAP"""
    data = SAP_DATA[sap_id]

    feature_bullets = generate_feature_bullets(data["key_features"])
    integration_sections = generate_integration_sections(data.get("integrations", []))
    related_saps = generate_related_saps(data.get("integrations", []))

    # Determine primary use case from title
    title_lower = data["title"].lower()
    primary_use_case = title_lower.replace("react ", "").replace(" (i18n)", "")

    content = AGENTS_TEMPLATE.format(
        sap_id=sap_id,
        title=data["title"],
        title_lower=title_lower,
        setup_time=data["setup_time"],
        time_savings=data["time_savings"],
        feature_bullets=feature_bullets,
        integration_sections=integration_sections,
        related_saps=related_saps,
        primary_use_case=primary_use_case,
    )

    return content


def main():
    """Generate AGENTS.md files for all Wave 5 React SAPs"""
    repo_root = Path(__file__).parent.parent

    for sap_id, data in SAP_DATA.items():
        sap_dir = repo_root / "docs" / "skilled-awareness" / data["name"]
        agents_file = sap_dir / "AGENTS.md"

        print(f"Generating {sap_id} ({data['name']})...")

        if agents_file.exists():
            print(f"  ⚠️  AGENTS.md already exists, skipping...")
            continue

        content = generate_agents_md(sap_id)

        with open(agents_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Created {agents_file}")

    print(f"\n✅ All AGENTS.md files generated successfully!")


if __name__ == "__main__":
    main()
