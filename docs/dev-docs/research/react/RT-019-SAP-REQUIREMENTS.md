# RT-019 React SAP Requirements Specification

**Document**: RT-019 SAP Requirements based on Research Analysis
**Date**: 2025-11-08
**Source**: RT-019-SYNTHESIS-Analysis-Summary.md
**Status**: Draft

---

## Executive Summary

Based on comprehensive analysis of RT-019-APP, RT-019-DATA, and RT-019-SCALE research reports, this document specifies:

1. **9 new SAPs** to fill identified gaps in the React ecosystem
2. **7 existing SAPs** requiring major updates with research findings
3. **Priority ranking** based on adoption targets and time savings
4. **Dependencies** between SAPs for implementation sequencing

**Total Impact**: Enable 80-90% time reduction across React development lifecycle

---

## Part 1: New SAP Requirements

### High Priority (Weeks 5-6)

#### SAP-033: Authentication & Authorization

**Rationale**: Authentication is a foundational requirement for 90% of React applications. Current SAP ecosystem lacks comprehensive auth guidance.

**Scope**:
- NextAuth.js v5 (Auth.js) setup and configuration
- Alternative providers (Clerk, Supabase Auth, Auth0) decision matrix
- Role-Based Access Control (RBAC) patterns with TypeScript
- Middleware route protection for Next.js 15 App Router
- Session management (JWT vs database sessions)
- OAuth2/OIDC flows with PKCE
- Magic links and passwordless authentication
- WebAuthn/Passkeys integration

**Time Savings**: 3-4 hours → 15 minutes (93.75% reduction)

**Evidence**:
- NextAuth v5: 50+ OAuth providers, edge runtime compatible
- Clerk: 7-minute setup benchmark, SOC2 Type II certified
- Auth0: 11k+ enterprise customers, 7M+ developers

**Dependencies**:
- SAP-034 (Database Integration) for user storage and sessions
- SAP-020 (React Foundation) for Next.js 15 setup

**Adoption Target**: 90% of React projects

**Artifacts Required**:
1. **Capability Charter**: Auth patterns, security model, provider comparison
2. **Protocol Spec**: Complete CLI/setup commands, NextAuth v5 config, middleware patterns
3. **Awareness Guide**: Decision trees for provider selection, RBAC patterns, security checklists
4. **Adoption Blueprint**: Step-by-step installation for all 4 providers
5. **Ledger**: Time savings metrics, security compliance evidence, adoption data

---

#### SAP-034: Database Integration

**Rationale**: Database setup is critical infrastructure for 80% of full-stack projects. No current SAP covers ORM selection and configuration.

**Scope**:
- Prisma ORM setup (default choice)
- Drizzle ORM setup (performance alternative)
- Decision matrix: Prisma vs Drizzle
- Schema design patterns and best practices
- Database migrations workflow
- Seeding and fixtures for development/testing
- Row-Level Security (RLS) patterns for Supabase/PostgreSQL
- Type-safe query patterns
- Connection pooling and edge runtime compatibility

**Time Savings**: 3-4 hours → 25 minutes (89.6% reduction)

**Evidence**:
- Prisma: Industry standard, ~50ms query latency, excellent DX
- Drizzle: ~30ms query latency, 40% faster than Prisma, smaller bundle
- PostgreSQL: Most popular production database for Next.js apps

**Dependencies**:
- SAP-020 (React Foundation) for Next.js 15 setup
- No blockers (foundational SAP)

**Adoption Target**: 80% of full-stack projects

**Artifacts Required**:
1. **Capability Charter**: ORM comparison, database selection, schema design philosophy
2. **Protocol Spec**: Prisma CLI, Drizzle CLI, migration commands, type generation
3. **Awareness Guide**: Decision tree for Prisma vs Drizzle, schema patterns, migration strategies
4. **Adoption Blueprint**: Step-by-step for both Prisma and Drizzle
5. **Ledger**: Performance benchmarks, setup time metrics, adoption data

---

#### SAP-041: Form Validation (NEW SAP)

**Rationale**: Existing SAP-018 needs major overhaul with React Hook Form + Zod patterns, Server Actions, and accessibility compliance. Forms are ubiquitous (95% adoption).

**Current State**: SAP-018 exists but lacks:
- React Hook Form integration
- Zod schema validation
- Server Action patterns
- WCAG 2.2 Level AA guidance
- Progressive enhancement

**Enhanced Scope**:
- React Hook Form (RHF) setup and patterns
- Zod schema-first validation
- TypeScript type inference from Zod schemas
- Server Action integration with `useFormStatus`, `useFormState`
- Client-side + server-side validation (dual validation)
- Accessibility patterns (WCAG 2.2 AA compliance)
- Progressive enhancement (works without JavaScript)
- Optimistic updates with `useOptimistic`
- Field arrays and nested forms
- Multi-step form wizards with state machines (XState)

**Time Savings**: 2-3 hours → 20 minutes (88.9% reduction)

**Evidence**:
- React Hook Form: 39k GitHub stars, 3M weekly npm downloads
- Zod: 10M+ weekly downloads, TypeScript-first standard
- Bundle size: RHF 12KB gzipped (minimal re-renders)

**Dependencies**:
- SAP-033 (Authentication) for protected forms
- SAP-020 (React Foundation) for Server Actions

**Adoption Target**: 95% of React projects

**Update Tasks**:
1. **Capability Charter**: Add RHF vs alternatives analysis, accessibility rationale
2. **Protocol Spec**: Complete RHF API, Zod schemas, Server Action patterns
3. **Awareness Guide**: Decision tree for simple vs complex forms, accessibility checklist
4. **Adoption Blueprint**: Update with RHF + Zod + Server Actions workflow
5. **Ledger**: Add evidence (npm downloads, bundle size, time savings)

---

### Medium Priority (Weeks 7-9)

#### SAP-035: File Upload & Storage

**Rationale**: File uploads are common (60% of apps) but complex to implement securely and performantly.

**Scope**:
- UploadThing setup (default Next.js solution)
- Vercel Blob Storage integration
- Supabase Storage integration
- AWS S3 with signed URLs
- Client-side file validation (size, type, security)
- Server-side processing (virus scanning, image optimization)
- Presigned URLs and direct uploads
- Progress indicators and chunked uploads
- Image transformation (resizing, format conversion)
- CDN integration for delivery

**Time Savings**: 4-6 hours → 30 minutes (91.7% reduction)

**Evidence**:
- UploadThing: Next.js-first, type-safe, built-in components
- Vercel Blob: Edge-optimized, global CDN, simple API
- Supabase Storage: RLS support, image transformations
- Pricing comparison: UploadThing free tier, Blob $0.05/GB

**Dependencies**:
- SAP-034 (Database) for file metadata storage
- SAP-033 (Authentication) for upload authorization

**Adoption Target**: 60% of React projects

---

#### SAP-036: Error Handling & Monitoring

**Rationale**: Production error handling is critical but often an afterthought. This SAP formalizes best practices.

**Scope**:
- Next.js 15 Error Boundaries (`error.tsx`, `global-error.tsx`)
- React error boundaries with `react-error-boundary`
- Sentry integration for error tracking
- PII scrubbing for privacy compliance (GDPR/CCPA)
- Source map configuration
- User-facing error UX patterns
- Toast notifications for transient errors
- Retry mechanisms with exponential backoff
- Custom 404/500 error pages
- TanStack Query error handling (`onError`, `retry`)
- Network error detection (`navigator.onLine`)

**Time Savings**: 3-4 hours → 30 minutes (87.5% reduction)

**Evidence**:
- Sentry: Industry standard, <1% performance overhead with sampling
- react-error-boundary: Standard library for reusable boundaries
- Target: 0% app crashes, 95%+ user recovery rate

**Dependencies**:
- SAP-020 (React Foundation) for Next.js 15 error boundaries
- SAP-025 (Performance) for performance monitoring integration

**Adoption Target**: 100% of production React projects

---

#### SAP-037: Real-Time Data Synchronization

**Rationale**: Real-time features (chat, notifications, live updates) are increasingly expected (40% adoption).

**Scope**:
- WebSockets with Socket.IO
- Server-Sent Events (SSE) for one-way updates
- Supabase Realtime integration (PostgreSQL Change Data Capture)
- Pusher channels integration
- Optimistic updates with TanStack Query
- Conflict resolution strategies (last-write-wins, CRDTs)
- Offline-first patterns with service workers
- React Query cache invalidation strategies
- Presence indicators and typing status

**Time Savings**: 6-8 hours → 45 minutes (90.6% reduction)

**Evidence**:
- Supabase Realtime: Built-in with Supabase, minimal setup
- Socket.IO: 59k GitHub stars, battle-tested
- Pusher: Managed service, 99.999% uptime SLA

**Dependencies**:
- SAP-034 (Database) for data source
- SAP-023 (State Management) for real-time state updates
- SAP-030 (Data Fetching) for TanStack Query integration

**Adoption Target**: 40% of React projects

---

### Lower Priority (Weeks 10-12)

#### SAP-038: Internationalization (i18n)

**Rationale**: Global applications require i18n, but it's complex to implement correctly (30% adoption).

**Scope**:
- next-intl setup (Next.js 15 App Router native)
- react-i18next alternative
- Translation file management (JSON, namespaces)
- Dynamic locale detection (URL, cookies, browser)
- Server-side translation with Server Components
- Client-side locale switching
- Date/time/currency formatting (Intl API)
- RTL (right-to-left) support
- SEO with hreflang tags
- Translation workflow with Crowdin/Lokalise

**Time Savings**: 8-12 hours → 1 hour (91.7% reduction)

**Evidence**:
- next-intl: Next.js 15 native, Server Component support
- react-i18next: 8k GitHub stars, mature ecosystem
- Adoption: 30% of enterprise apps require i18n

**Dependencies**:
- SAP-020 (React Foundation) for Next.js 15 routing
- SAP-041 (Form Validation) for multilingual forms

**Adoption Target**: 30% of React projects (but critical for those 30%)

---

#### SAP-039: End-to-End Testing

**Rationale**: E2E testing is essential for production confidence but time-consuming to set up (70% adoption target).

**Scope**:
- Playwright setup (default choice, 47k stars)
- Cypress integration (legacy alternative)
- Test structure and organization
- Fixtures and test data management
- Authentication flow testing
- Visual regression testing
- Accessibility testing integration (axe-core)
- CI/CD integration (parallel execution, sharding)
- Trace viewing and debugging
- Screenshot/video capture on failure

**Time Savings**: 4-6 hours → 45 minutes (87.5% reduction)

**Evidence**:
- Playwright: 47k GitHub stars, Microsoft-backed, cross-browser
- Cypress: 45k GitHub stars, established ecosystem (but slower)
- Playwright advantages: Faster execution, better TypeScript support

**Dependencies**:
- SAP-020 (React Foundation) for test target
- SAP-033 (Authentication) for auth flow testing
- SAP-005 (CI/CD) for GitHub Actions integration

**Adoption Target**: 70% of production React projects

---

#### SAP-040: Monorepo Architecture

**Rationale**: Monorepos enable code sharing and consistency for multi-app projects (20% adoption, but high impact).

**Scope**:
- Turborepo setup with pnpm workspaces
- Shared UI component library
- Shared TypeScript configurations
- Shared ESLint/Prettier configurations
- Dependency management and version consistency
- Build caching and remote caching
- Task orchestration and parallelization
- Changesets for versioning and changelogs
- Package publishing workflows

**Time Savings**: 12-16 hours → 2 hours (87.5% reduction)
**Performance Impact**: 80% build time reduction with caching

**Evidence**:
- Turborepo: Industry standard (acquired by Vercel), 80% faster builds
- pnpm: Efficient disk usage, fast installs, strict dependency isolation
- Adoption: 20% of projects, but critical for multi-app companies

**Dependencies**:
- SAP-020 (React Foundation) for app templates
- SAP-005 (CI/CD) for build orchestration
- SAP-026 (UI Components) for shared component library

**Adoption Target**: 20% of React projects (enterprise/multi-app)

---

## Part 2: Existing SAP Updates

### Priority 1: Foundation SAPs (Week 2)

#### SAP-020: React Foundation

**Current State**: Covers Next.js 15 setup, App Router, Server Components

**Updates Needed**:
- **Protocol Spec**: Add Next.js 15.1+ features (React 19, Server Actions enhancements)
- **Awareness Guide**: Add decision tree for Pages Router vs App Router migration
- **Ledger**: Update with Next.js 15 adoption metrics (npm downloads, migration success rates)
- **Integration**: Link to SAP-033 (Auth), SAP-034 (Database), SAP-018 (Forms)

**RT-019 Findings to Integrate**:
- Server-first architecture emphasis
- Progressive enhancement patterns
- Edge runtime compatibility
- Type safety across client/server boundaries

**Estimated Effort**: 4 hours

---

#### SAP-023: State Management

**Current State**: Covers React Context, Zustand, Jotai

**Updates Needed**:
- **Protocol Spec**: Add client vs server state separation patterns (TanStack Query for server state)
- **Awareness Guide**: Decision tree for Context vs Zustand vs TanStack Query
- **Ledger**: Add evidence from State of JS 2024 survey data
- **Integration**: Link to SAP-030 (Data Fetching), SAP-037 (Real-Time)

**RT-019 Findings to Integrate**:
- Three-pillar architecture: Server state (TanStack Query), Client state (Zustand), URL state (Next.js routing)
- Optimistic updates patterns
- Offline-first considerations

**Estimated Effort**: 5 hours

---

#### SAP-025: Performance Optimization

**Current State**: Covers React.memo, lazy loading, code splitting

**Updates Needed**:
- **Protocol Spec**: Add Core Web Vitals (INP focus), React Server Components optimization, bundle analysis
- **Awareness Guide**: Decision tree for optimization priorities (measure first!)
- **Ledger**: Add Core Web Vitals benchmarks, bundle size targets
- **Integration**: Link to SAP-040 (Monorepo), SAP-032 (build tools)

**RT-019 Findings to Integrate**:
- Interaction to Next Paint (INP) as new Core Web Vital
- React Server Components performance benefits
- Bundle size budgets (initial <100KB, total <300KB)
- Performance monitoring integration (Vercel Analytics, Google Lighthouse CI)

**Estimated Effort**: 6 hours

---

### Priority 2: Developer Experience SAPs (Week 3)

#### SAP-021: React Testing

**Current State**: Covers Vitest, React Testing Library

**Updates Needed**:
- **Protocol Spec**: Add Vitest vs Jest 2025 comparison (Vitest winning), Server Action testing, Server Component testing
- **Awareness Guide**: Testing Trophy diagram, decision tree for unit vs integration vs E2E
- **Ledger**: Add Vitest adoption metrics (State of JS 2024), time savings evidence
- **Integration**: Link to SAP-039 (E2E Testing), SAP-033 (Auth testing)

**RT-019 Findings to Integrate**:
- Vitest as default (faster, native ESM, Vite ecosystem)
- Server Component testing strategies
- Server Action testing with MSW v2
- Accessibility testing with jest-axe/vitest-axe

**Estimated Effort**: 5 hours

---

#### SAP-022: React Linting

**Current State**: Covers ESLint setup with React rules

**Updates Needed**:
- **Protocol Spec**: Add ESLint 9 flat config (182x faster!), React 19 rules, Next.js 15 rules
- **Awareness Guide**: Migration guide from ESLint 8 to ESLint 9
- **Ledger**: Add performance evidence (182x faster parsing)
- **Integration**: Link to SAP-020 (Foundation), SAP-024 (Styling with Prettier)

**RT-019 Findings to Integrate**:
- ESLint 9 flat config format (new standard)
- 182x performance improvement
- React Compiler linting support (React 19)
- Server Component linting rules

**Estimated Effort**: 4 hours

---

#### SAP-024: React Styling

**Current State**: Covers Tailwind CSS, CSS Modules

**Updates Needed**:
- **Protocol Spec**: Add Tailwind v4 (5x faster, CSS-first config), shadcn/ui adoption
- **Awareness Guide**: Decision tree for Tailwind vs CSS-in-JS vs CSS Modules
- **Ledger**: Add Tailwind v4 performance metrics, shadcn/ui adoption data
- **Integration**: Link to SAP-026 (Accessibility), SAP-040 (Monorepo shared styles)

**RT-019 Findings to Integrate**:
- Tailwind v4: 5x faster builds, CSS-first configuration, zero-JS
- shadcn/ui: Copy-paste components, full customization, 100k+ GitHub stars
- CSS-in-JS deprecation trend (RSC incompatibility)

**Estimated Effort**: 5 hours

---

### Priority 3: Quality & Accessibility (Week 4)

#### SAP-026: React Accessibility

**Current State**: Covers WCAG guidelines, aria attributes

**Updates Needed**:
- **Protocol Spec**: Add WCAG 2.2 (9 new criteria!), Level AA compliance checklist, testing tools
- **Awareness Guide**: Accessibility patterns for forms, modals, navigation
- **Ledger**: Add compliance evidence, legal case studies
- **Integration**: Link to SAP-018 (Form Accessibility), SAP-039 (A11y Testing)

**RT-019 Findings to Integrate**:
- WCAG 2.2 Level AA as baseline (new criteria: focus appearance, dragging, target size)
- Automated testing tools (axe-core, Lighthouse, Pa11y)
- Server Component accessibility benefits (progressive enhancement)
- Focus management patterns

**Estimated Effort**: 6 hours

---

## Part 3: Implementation Sequencing

### Phase 1: Foundation (Weeks 5-6)

**Goal**: Establish core infrastructure SAPs

**SAPs to Create**:
1. SAP-034 (Database Integration) - No dependencies
2. SAP-033 (Authentication) - Depends on SAP-034

**SAPs to Update**:
1. SAP-020 (React Foundation) - Foundational, no blockers

**Rationale**: Database and auth are prerequisites for most other SAPs. Foundation SAP updates enable better integration.

**Deliverables**:
- SAP-034: Complete 5 artifacts (Prisma + Drizzle)
- SAP-033: Complete 5 artifacts (4 auth providers)
- SAP-020: Updated with Next.js 15.1+, integration links

---

### Phase 2: User-Facing Features (Weeks 7-8)

**Goal**: Build on foundation with user-facing capabilities

**SAPs to Create/Update**:
1. SAP-041 (Form Validation) - Major update, depends on SAP-033
2. SAP-036 (Error Handling) - New SAP, depends on SAP-020
3. SAP-035 (File Upload) - New SAP, depends on SAP-033 + SAP-034

**SAPs to Update**:
1. SAP-023 (State Management) - Update with TanStack Query patterns
2. SAP-025 (Performance) - Update with Core Web Vitals, INP

**Deliverables**:
- SAP-018: Comprehensive RHF + Zod update
- SAP-036: Complete error handling framework
- SAP-035: File upload with 3 providers
- SAP-023 & SAP-025: Updated with research findings

---

### Phase 3: Developer Experience (Week 9)

**Goal**: Enhance developer productivity and code quality

**SAPs to Update**:
1. SAP-021 (Testing) - Vitest as default, Server Component testing
2. SAP-022 (Linting) - ESLint 9 flat config migration
3. SAP-024 (Styling) - Tailwind v4, shadcn/ui
4. SAP-026 (Accessibility) - WCAG 2.2 Level AA

**Deliverables**:
- All 4 SAPs updated with latest ecosystem trends
- Evidence-based metrics in all ledgers
- Decision trees in all awareness guides

---

### Phase 4: Advanced Patterns (Weeks 10-12)

**Goal**: Support advanced use cases (real-time, i18n, E2E, monorepo)

**SAPs to Create**:
1. SAP-037 (Real-Time) - Depends on SAP-034, SAP-023, SAP-030
2. SAP-038 (i18n) - Depends on SAP-020, SAP-018
3. SAP-039 (E2E Testing) - Depends on SAP-020, SAP-033, SAP-005
4. SAP-040 (Monorepo) - Depends on SAP-020, SAP-005, SAP-026

**Deliverables**:
- 4 advanced SAPs with complete 5-artifact sets
- Integration examples across multiple SAPs
- React SAP Excellence Initiative retrospective

---

## Part 4: Success Criteria

### Quality Standards (All SAPs)

**Diataxis Compliance** (SAP-000 §6.4):
- ✅ Capability Charter: Explanation-driven
- ✅ Protocol Spec: Reference-driven
- ✅ Awareness Guide: How-to-driven
- ✅ Adoption Blueprint: Tutorial-driven
- ✅ Ledger: Explanation-driven (metrics)

**Evidence Requirements**:
- ✅ Time savings metrics (before/after setup time)
- ✅ Adoption data (npm downloads, GitHub stars, surveys)
- ✅ Performance benchmarks (bundle size, query latency, build time)
- ✅ Decision trees for key selection points
- ✅ Integration patterns with related SAPs

**SAP-027 Dogfooding Validation**:
- ✅ Test adoption in sample project
- ✅ Measure actual time savings
- ✅ Collect satisfaction metrics
- ✅ GO/NO-GO decision before production promotion

### Per-SAP Targets

**New SAPs (9 total)**:
- [ ] 45 artifacts created (9 SAPs × 5 artifacts)
- [ ] 9 decision trees (1 per SAP)
- [ ] 9 time savings benchmarks
- [ ] 9 adoption metrics documented
- [ ] 9 dogfooding validation runs

**Updated SAPs (7 total)**:
- [ ] 35 artifacts updated (7 SAPs × 5 artifacts)
- [ ] 7 decision trees added/enhanced
- [ ] 7 evidence sections expanded
- [ ] 7 integration patterns documented
- [ ] 7 protocol specs refreshed with latest tools

**Integration**:
- [ ] Cross-SAP integration guide created
- [ ] React SAP ecosystem map published
- [ ] CLAUDE.md updated with React navigation patterns
- [ ] docs/skilled-awareness/INDEX.md updated

---

## Part 5: Risk Mitigation

### Ecosystem Churn Risk

**Problem**: React/Next.js ecosystem evolves rapidly. Tools recommended today may be deprecated tomorrow.

**Mitigation**:
1. **Evidence-based selection**: Only recommend tools with 10k+ GitHub stars, 1M+ weekly npm downloads
2. **Alternative providers**: Document 2-3 alternatives per category (e.g., Prisma + Drizzle)
3. **Decision trees**: Empower users to choose based on their context
4. **Quarterly reviews**: Schedule SAP reviews every 3 months to catch deprecations
5. **Version pinning**: Specify exact versions in adoption blueprints

### Over-Engineering Risk

**Problem**: SAPs might promote unnecessary complexity for simple projects.

**Mitigation**:
1. **Decision trees**: Include "Do you need this?" gate (e.g., "Skip auth if prototype")
2. **Complexity tiers**: Document simple, medium, complex approaches
3. **Progressive adoption**: Enable partial SAP adoption (e.g., just Zod, skip RHF for simple forms)
4. **Time-to-value tracking**: Measure overhead vs. benefit
5. **Escape hatches**: Document when to NOT use a SAP

### Dependency Hell Risk

**Problem**: SAPs have complex dependency graphs (e.g., SAP-037 depends on SAP-034, SAP-023, SAP-030).

**Mitigation**:
1. **Dependency documentation**: Clear dependency trees in each capability charter
2. **Minimal dependencies**: Limit SAP dependencies to 2-3 maximum
3. **Foundation-first**: Prioritize foundational SAPs (SAP-020, SAP-034) early
4. **Standalone value**: Ensure each SAP provides value independently
5. **Dependency visualization**: Create SAP dependency graph in docs/skilled-awareness/INDEX.md

### Security Risk

**Problem**: Security vulnerabilities in recommended tools could affect all adopters.

**Mitigation**:
1. **Security audits**: Only recommend tools with active security teams (e.g., NextAuth, Prisma)
2. **Vulnerability monitoring**: Subscribe to GitHub Security Advisories for recommended tools
3. **Quick response**: Establish process to update SAPs within 48 hours of critical CVEs
4. **Security checklists**: Include OWASP Top 10 compliance in awareness guides
5. **Penetration testing**: Include security testing in SAP-027 dogfooding validation

### Accessibility Regression Risk

**Problem**: Recommended tools may not maintain WCAG compliance in updates.

**Mitigation**:
1. **Automated testing**: Include axe-core/vitest-axe in SAP-021, SAP-039
2. **Manual audits**: Quarterly manual accessibility audits
3. **WCAG checklists**: Explicit WCAG 2.2 Level AA checklists in SAP-026
4. **Regression prevention**: CI/CD accessibility testing in SAP-005
5. **Fallback guidance**: Document accessible alternatives if primary tool fails compliance

---

## Part 6: Timeline & Milestones

### Week 1: Research Extraction (COMPLETED)
- ✅ RT-019-APP, RT-019-DATA, RT-019-SCALE converted to markdown
- ✅ RT-019-SYNTHESIS-Analysis-Summary.md created
- ✅ RT-019-SAP-REQUIREMENTS.md (this document)

### Weeks 2-4: Existing SAP Updates
- Week 2: SAP-020, SAP-023, SAP-025 (Priority 1)
- Week 3: SAP-021, SAP-022, SAP-024 (Priority 2)
- Week 4: SAP-026 (Priority 3)

### Weeks 5-6: Foundation SAPs
- SAP-034 (Database Integration)
- SAP-033 (Authentication)
- SAP-041 (Form Validation - major update)

### Weeks 7-8: User-Facing Features
- SAP-036 (Error Handling)
- SAP-035 (File Upload)

### Weeks 9-10: Advanced Patterns Part 1
- SAP-037 (Real-Time)
- SAP-038 (i18n)

### Weeks 11-12: Advanced Patterns Part 2
- SAP-039 (E2E Testing)
- SAP-040 (Monorepo)

### Week 13: Documentation & Validation
- React SAP integration guide
- CLAUDE.md updates
- INDEX.md updates
- Dogfooding validation (SAP-027)
- Retrospective

---

## Part 7: Effort Estimation

### New SAPs (9 total)

**Per SAP Effort**:
- Research synthesis: 2 hours (already done)
- Capability Charter: 3 hours
- Protocol Spec: 5 hours
- Awareness Guide: 4 hours (includes decision trees)
- Adoption Blueprint: 3 hours
- Ledger: 2 hours (evidence collection)
- **Total per SAP**: 19 hours

**9 New SAPs**: 171 hours (21.4 days)

### Existing SAP Updates (7 total)

**Per SAP Effort**:
- Capability Charter update: 1.5 hours
- Protocol Spec update: 2.5 hours
- Awareness Guide update: 2 hours (add decision trees)
- Adoption Blueprint refresh: 1.5 hours
- Ledger enhancement: 1.5 hours
- **Total per SAP**: 9 hours

**7 Updated SAPs**: 63 hours (7.9 days)

### Documentation & Integration

- React SAP integration guide: 6 hours
- CLAUDE.md updates: 3 hours
- INDEX.md updates: 2 hours
- SAP dependency graph: 3 hours
- Retrospective: 4 hours
- **Total**: 18 hours (2.25 days)

### Dogfooding Validation (SAP-027)

- Test adoptions (9 new + 7 updated = 16): 32 hours (2 hours per SAP)
- Validation reports: 16 hours (1 hour per SAP)
- **Total**: 48 hours (6 days)

### Grand Total

**Total Effort**: 300 hours (37.5 days)
**With 20% buffer**: 360 hours (45 days = 9 weeks)

**Recommended Team**:
- 1 senior engineer (lead, architecture, reviews): 50%
- 2 mid-level engineers (artifact creation): 100% each
- 1 technical writer (documentation polish): 25%

**Equivalent**: 2.25 FTE × 9 weeks = 20.25 person-weeks

---

## Appendix A: SAP Dependency Graph

```
Foundation Layer
├─ SAP-020 (React Foundation)
└─ SAP-034 (Database Integration)

Authentication Layer
└─ SAP-033 (Authentication) → depends on SAP-034

User-Facing Features Layer
├─ SAP-041 (Form Validation) → depends on SAP-033, SAP-020
├─ SAP-035 (File Upload) → depends on SAP-033, SAP-034
└─ SAP-036 (Error Handling) → depends on SAP-020

State Management Layer
├─ SAP-023 (State Management) → depends on SAP-020
└─ SAP-037 (Real-Time) → depends on SAP-034, SAP-023, SAP-030

Developer Experience Layer
├─ SAP-021 (Testing) → depends on SAP-020
├─ SAP-022 (Linting) → depends on SAP-020
├─ SAP-024 (Styling) → depends on SAP-020
└─ SAP-026 (Accessibility) → depends on SAP-020, SAP-018

Quality & Scale Layer
├─ SAP-025 (Performance) → depends on SAP-020, SAP-040
├─ SAP-038 (i18n) → depends on SAP-020, SAP-018
├─ SAP-039 (E2E Testing) → depends on SAP-020, SAP-033, SAP-005
└─ SAP-040 (Monorepo) → depends on SAP-020, SAP-005, SAP-026
```

---

## Appendix B: Evidence Summary

### Time Savings by SAP

| SAP | Setup Time Before | Setup Time After | Reduction | Adoption Target |
|-----|------------------|------------------|-----------|----------------|
| SAP-033 (Auth) | 3-4 hours | 15 minutes | 93.75% | 90% |
| SAP-034 (Database) | 3-4 hours | 25 minutes | 89.6% | 80% |
| SAP-018 (Forms) | 2-3 hours | 20 minutes | 88.9% | 95% |
| SAP-035 (File Upload) | 4-6 hours | 30 minutes | 91.7% | 60% |
| SAP-036 (Error Handling) | 3-4 hours | 30 minutes | 87.5% | 100% |
| SAP-037 (Real-Time) | 6-8 hours | 45 minutes | 90.6% | 40% |
| SAP-038 (i18n) | 8-12 hours | 1 hour | 91.7% | 30% |
| SAP-039 (E2E Testing) | 4-6 hours | 45 minutes | 87.5% | 70% |
| SAP-040 (Monorepo) | 12-16 hours | 2 hours | 87.5% | 20% |

**Weighted Average Time Savings**: 89.4% (weighted by adoption target)

### Tool Popularity Evidence

| Tool | GitHub Stars | Weekly npm Downloads | Status |
|------|-------------|---------------------|--------|
| React Hook Form | 39,000 | 3,000,000 | Active |
| Zod | Unknown | 10,000,000+ | Active |
| NextAuth.js | Unknown | Unknown | Active (v5 stable) |
| Prisma | Unknown | Unknown | Active (industry standard) |
| Drizzle | Unknown | Unknown | Active (fast-growing) |
| Playwright | 47,000 | Unknown | Active (Microsoft) |
| Tailwind CSS | Unknown | Unknown | Active (v4 released) |
| Turborepo | Unknown | Unknown | Active (Vercel) |

---

## Next Steps

1. **Review & Approval**: Present this requirements document to stakeholders
2. **Kickoff Week 2**: Begin Priority 1 SAP updates (SAP-020, SAP-023, SAP-025)
3. **Create Tracking**: Add all tasks to beads (SAP-015) for progress tracking
4. **Establish Cadence**: Weekly syncs to review progress, blockers, scope changes

**Document Status**: Ready for review
**Approvers**: [TBD]
**Next Review**: End of Week 2 (after Priority 1 SAP updates)
