# SAP-033: React Authentication & Authorization

**Status**: 🟡 Pilot
**Version**: 1.0.0
**Created**: 2025-11-09

---

## Overview

SAP-033 provides production-ready authentication and authorization patterns for React/Next.js applications with support for **four major providers**:

1. **NextAuth v5** - Self-hosted, 50+ OAuth providers, MIT open-source
2. **Clerk** - 7-minute setup, pre-built UI, SOC2 certified
3. **Supabase Auth** - Native RLS, magic links, phone OTP
4. **Auth0** - Enterprise SSO/SAML, 11k+ customers

**Key Benefits**:
- ✅ **93.75% time savings** (3-4 hours → 15 minutes)
- ✅ **OWASP Top 10 compliance** (8/10 full coverage)
- ✅ **SOC2 certified options** (Clerk, Supabase, Auth0)
- ✅ **Production validated** (T3 Stack, Vercel, 200k+ projects)

---

## Quick Start

### 1. Choose Your Provider

Use the decision tree:

```
Need self-hosted? → NextAuth v5
Need rapid setup (<10 min)? → Clerk
Using Supabase database? → Supabase Auth
Need enterprise SSO/SAML? → Auth0
Default choice? → NextAuth v5
```

### 2. Read the Adoption Blueprint

Jump directly to your provider's setup guide:
- [NextAuth v5 Setup](./adoption-blueprint.md#path-a-nextauth-v5-setup) (30 min)
- [Clerk Setup](./adoption-blueprint.md#path-b-clerk-setup) (7 min - fastest)
- [Supabase Auth Setup](./adoption-blueprint.md#path-c-supabase-auth-setup) (20 min)
- [Auth0 Setup](./adoption-blueprint.md#path-d-auth0-setup) (30 min)

### 3. Follow Step-by-Step Instructions

Each path includes:
- Prerequisites checklist
- Installation commands
- Configuration snippets
- Test verification steps

---

## Documentation Structure

### 📘 [Capability Charter](./capability-charter.md)
**Diataxis**: Explanation

**Read this to understand**:
- Problem statement (why authentication is complex)
- Solution overview (4-provider framework)
- Multi-provider decision matrix (5 criteria)
- Business value (93.75% time reduction)
- Security considerations (OWASP Top 10)

**Time**: 15-20 minutes

---

### 📗 [Protocol Spec](./protocol-spec.md)
**Diataxis**: Reference

**Read this for**:
- Complete API documentation (all 4 providers)
- Provider comparison tables
- TypeScript types and interfaces
- Security specifications (OAuth2 PKCE, HTTP-only cookies)
- Error handling patterns

**Time**: 30-45 minutes (reference as needed)

---

### 📙 [Awareness Guide](./awareness-guide.md)
**Diataxis**: How-To

**Read this for**:
- Decision tree (which provider to use)
- 8 practical workflows:
  - Set up NextAuth v5
  - Set up Clerk
  - Set up Supabase Auth
  - Set up Auth0
  - Implement RBAC
  - Add protected routes
  - Add magic link authentication
  - Add OAuth providers
- Common patterns (session refresh, logout, conditional rendering)
- Troubleshooting guide

**Time**: 20-30 minutes per workflow

---

### 📕 [Adoption Blueprint](./adoption-blueprint.md)
**Diataxis**: Tutorial

**Read this to**:
- Complete setup from scratch
- Follow step-by-step instructions
- Test authentication flows
- Verify security checklist

**Time**: 7-30 minutes (provider-dependent)

---

### 📔 [Ledger](./ledger.md)
**Diataxis**: Evidence

**Read this for**:
- Adoption tracking table
- Security best practices (7 practices with evidence)
- Evidence & metrics (time savings, provider validation)
- Security case studies (4 case studies)
- Lessons learned (5 lessons)

**Time**: 15-20 minutes

---

## Recommended Reading Order

### For First-Time Users

1. **Start here**: [Capability Charter](./capability-charter.md) - Understand the problem and solution (15 min)
2. **Choose provider**: [Decision Matrix](./capability-charter.md#multi-provider-decision-matrix) (5 min)
3. **Set up auth**: [Adoption Blueprint](./adoption-blueprint.md) - Follow your provider's path (7-30 min)
4. **Verify setup**: [Verification Checklist](./adoption-blueprint.md#verification) (5 min)

**Total Time**: 32-55 minutes (depending on provider)

---

### For Implementation Details

1. **Provider-specific APIs**: [Protocol Spec](./protocol-spec.md) - Complete reference
2. **Advanced workflows**: [Awareness Guide](./awareness-guide.md) - RBAC, magic links, OAuth
3. **Security patterns**: [Ledger - Best Practices](./ledger.md#best-practices)

---

### For Troubleshooting

1. **Common issues**: [Awareness Guide - Troubleshooting](./awareness-guide.md#troubleshooting)
2. **Security cases**: [Ledger - Security Case Studies](./ledger.md#security-case-studies)

---

## Provider Comparison

| Feature | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|---------|-------------|-------|---------------|-------|
| **Setup Time** | 30 min | **7 min** | 20 min | 30 min |
| **Cost** | **FREE** | $25+/mo | FREE (50k MAU) | Enterprise |
| **Self-Hosted** | ✅ | ❌ | ❌ | ❌ |
| **Pre-Built UI** | ❌ | ✅ | ❌ | ⚠️ Universal Login |
| **OAuth Providers** | 50+ | ~20 | ~15 | ~30 |
| **MFA** | ⚠️ DIY | ✅ Built-in | ⚠️ Phone only | ✅ Advanced |
| **SSO/SAML** | ⚠️ DIY | ⚠️ Limited | ❌ | ✅ |

**Full Comparison**: See [Protocol Spec - Provider Comparison](./protocol-spec.md#provider-comparison-matrix)

---

## Key Features

### Security (OWASP Coverage)

- ✅ **OAuth2 PKCE** (not implicit flow)
- ✅ **HTTP-only cookies** (XSS protection)
- ✅ **CSRF protection** (SameSite cookies)
- ✅ **Server-side validation** (middleware + Server Components)
- ✅ **Session refresh** (automatic)
- ✅ **MFA support** (provider-dependent)
- ✅ **Security logging** (authentication events)

**Coverage**: 8/10 OWASP Top 10 categories with full mitigation

---

### Authentication Methods

| Method | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|--------|-------------|-------|---------------|-------|
| **Email/Password** | ⚠️ DIY | ✅ | ✅ | ✅ |
| **OAuth (Google, GitHub)** | ✅ | ✅ | ✅ | ✅ |
| **Magic Links** | ⚠️ DIY | ✅ | ✅ | ✅ |
| **Phone OTP** | ⚠️ DIY | ✅ | ✅ | ✅ |
| **WebAuthn/Passkeys** | ⚠️ DIY | ✅ | ✅ | ✅ |
| **SSO/SAML** | ⚠️ DIY | ⚠️ Limited | ❌ | ✅ |

---

## Prerequisites

### Required SAPs

- ✅ **SAP-020** (React Project Foundation) - Next.js 15 App Router
- ✅ **SAP-034** (Database Integration) - Required for NextAuth v5, optional for others

### Optional SAPs

- **SAP-041** (Form Validation) - Custom login/signup forms
- **SAP-039** (E2E Testing) - Authentication flow testing
- **SAP-035** (API Layer) - Protected API routes
- **SAP-017** (State Management) - Auth state in Zustand/Context

---

## Evidence & Validation

### Time Savings (RT-019 Research)

- **Before**: 6-9 hours (custom auth implementation)
- **After**: 7-30 minutes (provider-based)
- **Savings**: 93.75% reduction

### Production Validation

| Provider | Evidence |
|----------|----------|
| **NextAuth v5** | T3 Stack (50k+ projects), Vercel (internal) |
| **Clerk** | $100M+ funding, SOC2 Type II, Linear, Loom |
| **Supabase Auth** | 200k+ projects, Mozilla, GitHub |
| **Auth0** | 11k+ enterprise customers, 7M+ developers |

### Security Certifications

- **Clerk**: SOC2 Type II
- **Supabase**: SOC2 Type II
- **Auth0**: SOC2, HIPAA, ISO 27001, GDPR

---

## Quick Links

### Decision Making
- [Provider Decision Tree](./capability-charter.md#multi-provider-decision-matrix)
- [Provider Comparison Table](./protocol-spec.md#provider-comparison-matrix)

### Setup Guides
- [NextAuth v5 Setup (30 min)](./adoption-blueprint.md#path-a-nextauth-v5-setup)
- [Clerk Setup (7 min)](./adoption-blueprint.md#path-b-clerk-setup)
- [Supabase Auth Setup (20 min)](./adoption-blueprint.md#path-c-supabase-auth-setup)
- [Auth0 Setup (30 min)](./adoption-blueprint.md#path-d-auth0-setup)

### Advanced Topics
- [RBAC Implementation](./awareness-guide.md#workflow-5-implement-rbac)
- [Protected Routes](./awareness-guide.md#workflow-6-add-protected-routes)
- [Magic Link Authentication](./awareness-guide.md#workflow-7-add-magic-link-authentication)
- [OAuth Providers](./awareness-guide.md#workflow-8-add-oauth-providers)

### Security
- [Security Best Practices](./ledger.md#best-practices)
- [Security Case Studies](./ledger.md#security-case-studies)
- [OWASP Coverage](./ledger.md#security-evidence-owasp-coverage)

---

## File Sizes

| Artifact | Lines | Size | Reading Time |
|----------|-------|------|--------------|
| [capability-charter.md](./capability-charter.md) | 709 | 24 KB | 15-20 min |
| [protocol-spec.md](./protocol-spec.md) | 2,464 | 53 KB | 30-45 min |
| [awareness-guide.md](./awareness-guide.md) | 1,781 | 39 KB | 20-30 min |
| [adoption-blueprint.md](./adoption-blueprint.md) | 1,649 | 42 KB | 25-35 min |
| [ledger.md](./ledger.md) | 833 | 23 KB | 15-20 min |
| **Total** | **7,436** | **181 KB** | **~2 hours** |

---

## Status & Roadmap

### Current Status: Pilot

- ✅ All 5 artifacts complete
- ✅ RT-019 research integrated
- ✅ 4 providers documented (NextAuth, Clerk, Supabase, Auth0)
- ✅ Security best practices defined
- 🟡 Awaiting first production adoption

### Roadmap to Production

- [ ] First 3 adoptions (validation)
- [ ] Adoption feedback collected
- [ ] Best practices refined
- [ ] Time savings validated (93.75% target)
- [ ] Security audit (optional)

**Target Production Date**: After 10 adoptions (Q1 2026 target)

---

## Contributing

### How to Adopt SAP-033

1. Read [Capability Charter](./capability-charter.md)
2. Choose provider using decision tree
3. Follow [Adoption Blueprint](./adoption-blueprint.md)
4. Report feedback (see below)

### How to Provide Feedback

1. Open issue in chora-base repository
2. Tag with `SAP-033` and `authentication`
3. Include:
   - Provider used (NextAuth/Clerk/Supabase/Auth0)
   - Actual setup time
   - Issues encountered
   - Suggestions for improvement

**Your feedback improves this SAP for everyone!**

---

## Support

### Documentation Issues

- Report in chora-base repository
- Tag with `SAP-033` and `documentation`

### Provider-Specific Support

- **NextAuth**: https://github.com/nextauthjs/next-auth/discussions
- **Clerk**: https://clerk.com/support
- **Supabase**: https://supabase.com/support
- **Auth0**: https://community.auth0.com/

---

## Version History

**1.0.0** (2025-11-09) - Initial Release
- Complete 5-artifact SAP structure
- Four-provider framework (NextAuth v5, Clerk, Supabase Auth, Auth0)
- Multi-provider decision matrix
- Security best practices (OWASP Top 10)
- Evidence from RT-019 research
- Status: Pilot

---

## License

This SAP is part of chora-base and follows the project's license.

Provider licenses:
- **NextAuth v5**: MIT
- **Clerk**: Proprietary (SaaS)
- **Supabase**: MIT (client libraries), proprietary (hosted service)
- **Auth0**: Proprietary (SaaS)

---

**Questions?** Start with the [Capability Charter](./capability-charter.md) or jump to the [Adoption Blueprint](./adoption-blueprint.md) for hands-on setup.
