# SAP-026: React Accessibility Capability Charter

**SAP ID**: SAP-026
**Name**: React Accessibility
**Version**: 1.0.0
**Status**: Active
**Category**: React Development / Quality Assurance
**Created**: 2025-11-02
**Last Updated**: 2025-11-02

---

## What This Is

SAP-026 (React Accessibility) provides **WCAG 2.2 Level AA compliance** capability for React applications. This SAP delivers automated accessibility testing, linting, and accessible component patterns that enable developers to build legally compliant, usable applications without specialized accessibility expertise.

### Key Capabilities

**Automated Accessibility**:
- ESLint integration with `eslint-plugin-jsx-a11y` (catches 85% of common violations)
- Automated testing with `jest-axe` (Next.js) and `vitest-axe` (Vite)
- Pre-commit hooks prevent accessibility regressions
- CI/CD integration blocks builds with critical violations

**Component Patterns**:
- 6 production-ready accessible component templates (Modal, Form, Button, Dropdown, Skip-link, Tabs)
- Focus management and keyboard navigation patterns
- ARIA attribute usage examples
- Screen reader announcements

**WCAG 2.2 Compliance**:
- All 9 new WCAG 2.2 criteria documented with React implementation patterns
- Level AA compliance (industry-standard for legal requirements)
- Testing workflows for manual verification (keyboard, screen readers)
- Integration with accessible component libraries (Radix UI, React Aria, Headless UI)

### Time Savings

**Manual Implementation**: 4-6 hours per project
- Research WCAG 2.2 requirements (1-2h)
- Configure accessibility linting (1h)
- Set up testing infrastructure (1-2h)
- Implement accessible patterns (1-2h)

**With SAP-026**: 30 minutes
- Install dependencies (5 min)
- Copy configuration templates (10 min)
- Copy component patterns (15 min)

**Time Reduction**: 87-90% (4-6h → 30min)

---

## Why This Exists

### The Problem

**Accessibility is legally required but poorly understood**:

1. **Legal Compliance Gap**: Web Content Accessibility Guidelines (WCAG) 2.2 became the W3C Recommendation on October 5, 2023, introducing 9 new success criteria beyond WCAG 2.1. Most React developers are unfamiliar with these requirements, creating legal liability under:
   - Americans with Disabilities Act (ADA) in the US
   - European Accessibility Act (EAA) in the EU
   - Section 508 for government contracts
   - **Average accessibility lawsuit settlement: $50,000-250,000**

2. **Complex Implementation**: Accessible React components require understanding of:
   - Semantic HTML vs ARIA (when to use which)
   - Focus management (focus traps, focus restoration, roving tabindex)
   - Keyboard navigation patterns (Tab, Enter, Space, Escape, Arrow keys)
   - Screen reader announcements (aria-live, role="alert", aria-describedby)
   - WCAG 2.2 new criteria (Focus Not Obscured, Target Size Minimum, Accessible Authentication)

3. **Testing Challenges**: Manual accessibility testing is time-consuming:
   - Screen reader setup and learning curve (NVDA, JAWS, VoiceOver)
   - Keyboard navigation testing for every interactive element
   - Color contrast validation
   - Automated tools catch ~85%, manual testing required for remaining ~15%

4. **Maintenance Burden**: Without systematic testing, accessibility regressions are common:
   - New features introduce violations
   - Refactoring breaks keyboard navigation
   - Dynamic content fails to announce to screen readers

### The Solution

SAP-026 provides a **complete accessibility stack** that automates 85% of compliance checking and provides clear patterns for the remaining 15%:

**Automated Prevention** (85% coverage):
- `eslint-plugin-jsx-a11y` catches violations during development (before commit)
- `jest-axe`/`vitest-axe` validates components in tests (before merge)
- Pre-commit hooks block code with critical violations
- CI/CD integration prevents deployment of inaccessible code

**Manual Testing Guidance** (15% coverage):
- Keyboard navigation checklists
- Screen reader testing workflows (NVDA recommended)
- Color contrast testing tools
- Focus visibility verification

**Implementation Patterns**:
- 6 accessible component templates (copy-paste ready)
- Radix UI integration examples (pre-built accessible primitives)
- ARIA usage decision trees (semantic HTML first, ARIA when necessary)
- React-specific patterns (Server Components, Suspense, error boundaries)

### Key Principles

1. **Semantic HTML First**: Use `<button>` instead of `<div onClick>`, `<a href>` instead of `<span onClick>`. Semantic elements provide keyboard navigation, focus management, and screen reader context automatically.

2. **ARIA as Enhancement**: Only use ARIA when semantic HTML is insufficient. Invalid ARIA is worse than no ARIA. Follow ARIA Authoring Practices Guide patterns.

3. **Automated Testing**: 85% of accessibility issues are detectable by automated tools (eslint-plugin-jsx-a11y, axe-core). Catch violations before manual testing.

4. **Progressive Enhancement**: Build for keyboard users first, then enhance for mouse/touch. If it works with keyboard, it works for assistive technology.

5. **Focus Visibility**: Ensure focus indicators are always visible and meet 3:1 contrast ratio. Use `:focus-visible` to show focus only for keyboard users.

---

## Who Should Use This

### Primary Audience

**React Developers Building Accessible UIs**:
- Web applications with public-facing interfaces (legal requirement)
- Government contracts requiring Section 508 compliance
- Enterprise SaaS products (WCAG 2.2 Level AA increasingly required)
- E-commerce sites (accessibility = better UX = more conversions)
- Any application serving diverse user populations

**Prerequisites**:
- SAP-020 (React Foundation) - Next.js 15 or Vite 7 project setup
- SAP-021 (React Testing) - Vitest/Jest testing infrastructure
- SAP-022 (React Linting) - ESLint 9 flat config (jsx-a11y plugin already included)
- React 19+, TypeScript 5.7+

### Secondary Audience

**QA Engineers & Accessibility Specialists**:
- Validating React applications for WCAG compliance
- Setting up automated accessibility testing
- Training developers on accessible patterns
- Auditing existing React applications

**NOT For**:
- React Native developers (mobile accessibility uses different patterns - future SAP)
- Legacy React applications <18 (use class-based patterns not covered here)
- Teams requiring WCAG 2.2 Level AAA (this SAP focuses on Level AA, the legal standard)

---

## Business Value

### Quantitative Benefits

**Time Savings**:
- **First Project**: 4-6 hours → 30 minutes (87-90% reduction)
- **Subsequent Projects**: 2-3 hours → 20 minutes (85-88% reduction)
- **Annual Savings** (10 projects): 40-60 hours saved
- **Cost Savings** @ $100/hour: **$4,000-6,000/year**

**Quality Improvements**:
- 85% of accessibility issues caught pre-commit (automated linting)
- 100% of components tested for violations (jest-axe/vitest-axe)
- Zero accessibility regressions (pre-commit hooks + CI/CD)
- WCAG 2.2 Level AA compliance on critical user paths

**Risk Mitigation**:
- Legal compliance (ADA, EAA, Section 508)
- Lawsuit avoidance ($50,000-250,000 average settlement)
- Brand reputation protection (accessible = inclusive)
- Government contract eligibility (Section 508 required)

### Qualitative Benefits

**Developer Experience**:
- No accessibility expertise required (templates + linting)
- Immediate feedback during development (ESLint in IDE)
- Clear error messages (jsx-a11y explains violations)
- Copy-paste component patterns (skip research phase)

**User Experience**:
- Keyboard navigation works everywhere (Tab, Enter, Escape)
- Screen reader users can navigate and interact
- Better UX for all users (semantic HTML, clear focus indicators)
- 24×24px minimum touch targets (easier clicking/tapping)

---

## Scope

### In Scope

**WCAG 2.2 Level AA Compliance**:
- All 9 new WCAG 2.2 criteria (Focus Not Obscured, Target Size, Accessible Auth, etc.)
- Foundational WCAG 2.1 Level AA criteria (contrast, keyboard, ARIA)
- React-specific implementation patterns
- Next.js 15 and Vite 7 configurations

**Automated Testing**:
- `eslint-plugin-jsx-a11y` configuration (recommended rules)
- `jest-axe` setup (Next.js with Jest)
- `vitest-axe` setup (Vite with Vitest)
- `axe-core` runtime testing patterns
- Pre-commit hook integration (Husky + lint-staged)

**Component Patterns** (6 templates):
- Accessible Modal (focus trap, aria-modal, keyboard handling)
- Accessible Form (labels, validation, error messages, aria-live)
- Accessible Button (semantic HTML, loading states, icon buttons)
- Accessible Dropdown (keyboard navigation, aria-expanded)
- Skip Link (keyboard-only navigation, hidden until focused)
- Accessible Tabs (arrow key navigation, aria-selected, roving tabindex)

**Accessible Component Library Integration**:
- Radix UI patterns (primitives with built-in accessibility)
- React Aria (Adobe) hooks usage
- Headless UI (Tailwind CSS integration)
- Decision matrix: when to use which library

**Testing Workflows**:
- Keyboard navigation checklists
- Screen reader testing guide (NVDA, VoiceOver, JAWS)
- Color contrast validation tools
- Manual testing complement to automated tools

### Out of Scope

**Not Included in SAP-026**:
- WCAG 2.2 Level AAA compliance (beyond legal requirements for most organizations)
- React Native accessibility (mobile-specific patterns - future SAP-030)
- PDF accessibility (different specification)
- Video/audio accessibility (captions, transcripts - future SAP)
- Visual regression testing (separate concern - SAP-028)
- E2E accessibility testing at scale (future integration with Playwright - SAP-027)

**Deferred to Future Versions**:
- Advanced ARIA patterns (Combobox, Command palette, Tree view)
- Internationalization + accessibility (RTL languages, screen reader localization)
- Accessibility performance optimization (reducing ARIA tree complexity)
- Custom screen reader announcements (advanced aria-live patterns)

---

## Success Outcomes

### Measurable Outcomes

**Technical Metrics**:
- 85%+ automated accessibility coverage (ESLint + axe-core)
- 0 critical violations on main user flows (jest-axe tests pass)
- 100% keyboard navigability (all interactive elements reachable)
- 4.5:1 minimum color contrast on text (WCAG 2.2 Level AA)
- 24×24px minimum target size on buttons/links (WCAG 2.5.8)

**Process Metrics**:
- Accessibility violations caught in IDE (immediate feedback)
- Pre-commit hooks prevent merging violations
- CI/CD blocks deployment of accessibility regressions
- Accessibility testing takes <5 minutes per component (automated)

**Compliance Metrics**:
- WCAG 2.2 Level AA compliance on critical paths
- Lighthouse accessibility score ≥90 (good)
- axe-core reports 0 violations on key pages
- Manual keyboard testing passes (Tab order, focus visible)

### Qualitative Outcomes

**Developer Confidence**:
- Developers understand when to use semantic HTML vs ARIA
- Clear error messages guide fixes (jsx-a11y explanations)
- Component templates demonstrate correct patterns
- No specialized accessibility training required

**User Experience**:
- Screen reader users can complete critical tasks
- Keyboard users can navigate without mouse
- Error messages are clear and associated with form fields
- Focus indicators always visible during keyboard navigation

---

## Dependencies

### Required SAPs

**SAP-000 (SAP Framework)**: Core SAP structure and conventions
**SAP-020 (React Foundation)**: Next.js 15 or Vite 7 project setup
**SAP-021 (React Testing)**: Vitest/Jest testing infrastructure
**SAP-022 (React Linting)**: ESLint 9 with jsx-a11y plugin (already includes accessibility linting)

### Optional Integrations

**SAP-005 (CI/CD Workflows)**: GitHub Actions accessibility checks
**SAP-024 (React Styling)**: Color contrast with Tailwind CSS design tokens
**SAP-025 (React Performance)**: Lighthouse CI includes accessibility scoring

### Technology Dependencies

**Core Dependencies**:
- React 19+ (JSX transform, Suspense, Server Components)
- TypeScript 5.7+ (strict mode recommended)
- Node.js 22.x

**Accessibility Dependencies**:
- `eslint-plugin-jsx-a11y@^6.10.2` (already in SAP-022)
- `jest-axe@^9.0.0` (Next.js with Jest)
- `vitest-axe@^1.0.0` (Vite with Vitest)
- `axe-core@^4.10.2` (runtime testing)
- `react-focus-lock@^2.13.2` (focus trap for modals)

**Component Libraries** (optional):
- Radix UI v1.1.2 (unstyled accessible primitives)
- React Aria (Adobe) v3.37.0 (hooks-based accessibility)
- Headless UI v2.2.0 (Tailwind CSS integration)

---

## Constraints & Risks

### Constraints

**Technical Constraints**:
- Requires React 19+ (older React versions not supported)
- Next.js 15 or Vite 7 required (SAP-020 dependency)
- TypeScript strict mode recommended (but not required)
- Modern browser support (no IE11)

**Scope Constraints**:
- WCAG 2.2 Level AA only (Level AAA out of scope)
- React web only (React Native requires different patterns)
- English-language accessibility (i18n + a11y is complex)

**Manual Testing Required**:
- Automated tools catch ~85%, manual testing needed for ~15%
- Screen reader testing cannot be fully automated
- Keyboard navigation requires manual verification
- Color contrast edge cases need manual validation

### Risks & Mitigation

**Risk 1: WCAG 2.2 Learning Curve**
**Likelihood**: Medium
**Impact**: Medium (developers may be unfamiliar with new criteria)
**Mitigation**:
- RT-019-PROD research provides comprehensive WCAG 2.2 overview
- protocol-spec.md includes decision trees and quick reference
- Common pitfalls documented with solutions in awareness-guide.md

**Risk 2: False Positives from ESLint**
**Likelihood**: Medium
**Impact**: Low (developer frustration, but linting is correct)
**Mitigation**:
- protocol-spec documents when to disable rules (with eslint-disable comments)
- Explain rationale for rules in awareness-guide
- Provide alternative patterns instead of just blocking code

**Risk 3: Incomplete Manual Testing**
**Likelihood**: Medium
**Impact**: High (accessibility issues reach production)
**Mitigation**:
- Clear testing checklists in adoption-blueprint
- Emphasize 85% automated + 15% manual = 100% coverage
- Provide NVDA installation guide (free, most accurate)

**Risk 4: Component Library Lock-in**
**Likelihood**: Low
**Impact**: Medium (teams may prefer different libraries)
**Mitigation**:
- Document Radix UI, React Aria, Headless UI equally
- Provide decision matrix, not opinionated recommendation
- Templates use semantic HTML (no library dependency)

---

## Maintenance & Versioning

### Update Triggers

**Quarterly Reviews** (Every 3 Months):
- Update `eslint-plugin-jsx-a11y` to latest version
- Review new axe-core rules
- Check for WCAG 2.3 announcements (future specification)
- Test templates with latest React/Next.js/Vite versions

**Annual Reviews** (Every 12 Months):
- Major version update if WCAG 2.3 published
- Add new component patterns based on usage
- Deprecate outdated accessibility patterns
- ROI analysis (actual time savings vs projections)

### Version History

**v1.0.0** (2025-11-02): Initial release
- WCAG 2.2 Level AA compliance
- 6 accessible component templates
- jest-axe and vitest-axe configurations
- Radix UI integration examples
- Screen reader testing guide (NVDA, VoiceOver)

---

## Related Resources

**WCAG Specifications**:
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) - W3C Recommendation
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/) - Detailed guidance

**Accessibility Testing Tools**:
- [axe DevTools](https://www.deque.com/axe/devtools/) - Browser extension
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Accessibility auditing
- [NVDA](https://www.nvaccess.org/) - Free screen reader (Windows)

**React Accessibility Resources**:
- [React Accessibility Docs](https://react.dev/learn/accessibility)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Radix UI](https://www.radix-ui.com/) - Accessible primitives

**chora-base Resources**:
- SAP-020: React Foundation
- SAP-021: React Testing & Quality
- SAP-022: React Linting & Formatting
- RT-019-PROD: Production Excellence Research (WCAG 2.2 analysis)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Next Review**: 2026-02-02 (3 months)
