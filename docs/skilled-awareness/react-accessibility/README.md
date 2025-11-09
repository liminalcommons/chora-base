# SAP-026: React Accessibility

**WCAG 2.2 Level AA compliance** for React applications with automated testing and accessible component patterns.

## Quick Start

### Installation

```bash
# Already included if you have SAP-022 (React Linting)
npm install --save-dev eslint-plugin-jsx-a11y

# Testing dependencies
# For Next.js projects (Jest):
npm install --save-dev jest-axe @axe-core/react

# For Vite projects (Vitest):
npm install --save-dev vitest-axe @axe-core/react

# Component dependencies
npm install react-focus-lock

# Optional: Accessible component libraries
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

### ESLint Configuration

The `eslint-plugin-jsx-a11y` plugin is already configured in SAP-022. See [protocol-spec.md](./protocol-spec.md#eslint-configuration) for rule details.

### Testing Setup

Configure accessibility testing in your test files:

**Next.js (Jest):**
```typescript
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)
```

**Vite (Vitest):**
```typescript
import { axe, toHaveNoViolations } from 'vitest-axe'
expect.extend(toHaveNoViolations)
```

See [protocol-spec.md](./protocol-spec.md#automated-testing) for complete setup.

## Component Templates

SAP-026 provides 6 production-ready accessible components:

1. **[Accessible Modal](../../templates/react/accessibility/shared/components/accessible-modal.tsx)** - Focus trap, `aria-modal`, keyboard handling (Escape key)
2. **[Accessible Form](../../templates/react/accessibility/shared/components/accessible-form.tsx)** - Labels, validation, error messages, `aria-live` announcements
3. **[Accessible Button](../../templates/react/accessibility/shared/components/accessible-button.tsx)** - Loading states, icon buttons, disabled states
4. **[Accessible Dropdown](../../templates/react/accessibility/shared/components/accessible-dropdown.tsx)** - Keyboard navigation (Arrow keys), `aria-expanded`
5. **[Skip Link](../../templates/react/accessibility/shared/components/skip-link.tsx)** - Keyboard-only navigation, hidden until focused
6. **[Accessible Tabs](../../templates/react/accessibility/shared/components/accessible-tabs.tsx)** - Arrow key navigation, `aria-selected`, roving tabindex

Copy these templates into your project and customize as needed.

## Documentation

- **[capability-charter.md](./capability-charter.md)** - Business value, scope, dependencies, success metrics
- **[protocol-spec.md](./protocol-spec.md)** - Complete WCAG 2.2 compliance guide, testing protocols, component patterns
- **[awareness-guide.md](./awareness-guide.md)** - Common pitfalls, decision trees, best practices *(coming soon)*
- **[ledger.md](./ledger.md)** - WCAG 2.2 compliance checklist *(coming soon)*

## WCAG 2.2 Level AA Compliance

This SAP covers all **9 new WCAG 2.2 criteria** plus foundational WCAG 2.1 Level AA requirements:

- **2.4.11 Focus Not Obscured (Minimum)** - Focus indicators visible
- **2.5.7 Dragging Movements** - Alternative input methods
- **2.5.8 Target Size (Minimum)** - 24×24px touch targets
- **3.2.6 Consistent Help** - Help mechanisms in consistent order
- **3.3.7 Redundant Entry** - Auto-fill and session persistence
- **3.3.8 Accessible Authentication (Minimum)** - No cognitive tests
- Plus 3 Level AAA criteria included as best practices

See [protocol-spec.md](./protocol-spec.md#wcag-22-compliance) for full compliance matrix.

## Manual Testing

Automated tools catch **~85%** of accessibility issues. Manual testing is required for:

- **Keyboard navigation** - Tab order, focus visibility, keyboard shortcuts
- **Screen reader testing** - NVDA (Windows), VoiceOver (macOS), JAWS
- **Color contrast** - Text readability, focus indicators
- **Zoom testing** - 200% zoom without content loss

See [protocol-spec.md](./protocol-spec.md#manual-testing) for detailed workflows.

## Dependencies

- **SAP-020** (React Foundation) - Next.js 15 or Vite 7
- **SAP-021** (React Testing) - Vitest/Jest infrastructure
- **SAP-022** (React Linting) - ESLint 9 with jsx-a11y plugin

## Resources

- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [axe DevTools Browser Extension](https://www.deque.com/axe/devtools/)
- [NVDA Screen Reader](https://www.nvaccess.org/) (free, Windows)
- [Radix UI Documentation](https://www.radix-ui.com/) (accessible primitives)

---

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-02
