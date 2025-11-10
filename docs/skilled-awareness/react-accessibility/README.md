# SAP-026: React Accessibility (WCAG 2.2)

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> WCAG 2.2 Level AA compliance for React apps—eslint-plugin-jsx-a11y (85% automated coverage), jest-axe/vitest-axe component testing, Radix UI accessible primitives, and focus management with react-focus-lock.

---

## 🚀 Quick Start (4 minutes)

```bash
# Install accessibility dependencies
pnpm add -D eslint-plugin-jsx-a11y@6  # ESLint a11y linting

# Choose testing library (jest-axe OR vitest-axe)
pnpm add -D jest-axe@9 axe-core@4      # For Jest
pnpm add -D vitest-axe@1 axe-core@4    # For Vitest

# Install focus management
pnpm add react-focus-lock@2

# Optional: Accessible component library
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu  # Radix UI
# OR
pnpm add react-aria-components  # React Aria
# OR
pnpm add @headlessui/react      # Headless UI
```

**Configure ESLint** (eslint.config.mjs):
```javascript
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  {
    plugins: { 'jsx-a11y': jsxA11y },
    rules: {
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      // ... (30+ rules for WCAG 2.2 compliance)
    },
  },
];
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for step-by-step setup (18-min read)

---

## 📖 What Is SAP-026?

SAP-026 provides **WCAG 2.2 Level AA compliance patterns** for React applications. Achieve 85% automated accessibility coverage through ESLint linting, component testing with axe-core, and accessible component primitives from Radix UI, React Aria, or Headless UI.

**Key Innovation**: **WCAG 2.2 compliance** (W3C Recommendation, October 2023)—9 new criteria including Focus Not Obscured (2.4.11), Target Size Minimum (2.5.8), and Accessible Authentication (3.3.8).

### How It Works

1. **ESLint Linting**: eslint-plugin-jsx-a11y catches 85% of accessibility issues at build time (alt text, ARIA, labels, keyboard support)
2. **Component Testing**: jest-axe/vitest-axe validates components against WCAG 2.2 rules (color contrast, focus management)
3. **Runtime Validation**: axe-core scans pages in development for violations (integrated with browser DevTools)
4. **Manual Testing**: 15% of WCAG criteria require manual validation (keyboard navigation, screen reader testing)

---

## 🎯 When to Use

Use SAP-026 when you need to:

1. **Achieve WCAG 2.2 Level AA compliance** - Legal requirement (ADA, Section 508, EU Accessibility Directive)
2. **Automate accessibility testing** - Catch 85% of issues with ESLint + axe-core in CI/CD
3. **Build accessible components** - Use Radix UI, React Aria, or Headless UI primitives (WCAG-compliant out-of-the-box)
4. **Support assistive technologies** - Screen readers (NVDA, JAWS, VoiceOver), keyboard navigation, voice control
5. **Improve SEO and UX** - Accessible sites rank higher, convert better (10-20% lift)

**Not needed for**: Internal tools with no accessibility requirements (though still recommended), or if using fully-managed component libraries (e.g., Material UI with accessibility enabled)

---

## ✨ Key Features

- ✅ **WCAG 2.2 Level AA Compliance** - 9 new criteria (October 2023) including Focus Not Obscured, Target Size, Accessible Auth
- ✅ **85% Automated Coverage** - eslint-plugin-jsx-a11y + axe-core catch most issues at build/test time
- ✅ **Component Testing** - jest-axe/vitest-axe validates components against WCAG rules
- ✅ **Accessible Primitives** - Radix UI, React Aria, Headless UI provide WCAG-compliant components
- ✅ **Focus Management** - react-focus-lock for modal focus traps, focus restoration
- ✅ **Runtime Validation** - axe-core browser extension scans pages in development
- ✅ **CI/CD Integration** - Lighthouse CI enforces accessibility scores in GitHub Actions

---

## 📚 Quick Reference

### WCAG 2.2 Level AA Targets

| Category | Criterion | Target | Automated Testing |
|----------|-----------|--------|-------------------|
| **Perceivable** | 1.1.1 Non-text Content | All images have alt text | ✅ jsx-a11y/alt-text |
| **Perceivable** | 1.4.3 Contrast (Minimum) | 4.5:1 text, 3:1 large text | ✅ axe-core color-contrast |
| **Operable** | 2.1.1 Keyboard | All functionality via keyboard | ⚠️ jsx-a11y (partial) |
| **Operable** | 2.4.7 Focus Visible | CSS `:focus-visible` styles | ⚠️ axe-core (partial) |
| **Operable** | 2.4.11 Focus Not Obscured (NEW) | Sticky headers don't hide focus | ❌ Manual testing |
| **Operable** | 2.5.8 Target Size Minimum (NEW) | 24×24px interactive targets | ⚠️ axe-core (partial) |
| **Understandable** | 3.3.2 Labels or Instructions | All inputs have labels | ✅ jsx-a11y/label-has-associated-control |
| **Understandable** | 3.3.8 Accessible Auth (NEW) | No CAPTCHA, allow password managers | ❌ Manual testing |
| **Robust** | 4.1.2 Name, Role, Value | Semantic HTML or ARIA | ✅ jsx-a11y/aria-props |

**Legend**:
- ✅ Fully automated (ESLint + axe-core)
- ⚠️ Partial automated (manual verification needed)
- ❌ Requires manual testing (keyboard, screen reader)

---

### ESLint Configuration (jsx-a11y)

#### ESLint 9 Flat Config

```javascript
// eslint.config.mjs
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  {
    plugins: {
      'jsx-a11y': jsxA11y,
    },
    rules: {
      // Images & Media
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/media-has-caption': 'error',
      'jsx-a11y/iframe-has-title': 'error',

      // ARIA
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-proptypes': 'error',
      'jsx-a11y/aria-role': 'error',
      'jsx-a11y/aria-unsupported-elements': 'error',
      'jsx-a11y/role-has-required-aria-props': 'error',
      'jsx-a11y/role-supports-aria-props': 'error',

      // Forms
      'jsx-a11y/label-has-associated-control': 'error',
      'jsx-a11y/autocomplete-valid': 'error',

      // Keyboard & Interaction
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/mouse-events-have-key-events': 'error',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/no-noninteractive-tabindex': 'error',
      'jsx-a11y/no-autofocus': 'warn',  // Sometimes needed

      // Semantics
      'jsx-a11y/heading-has-content': 'error',
      'jsx-a11y/anchor-has-content': 'error',
      'jsx-a11y/anchor-is-valid': 'error',
      'jsx-a11y/html-has-lang': 'error',
      'jsx-a11y/lang': 'error',

      // Anti-patterns
      'jsx-a11y/no-access-key': 'error',
      'jsx-a11y/no-distracting-elements': 'error',
      'jsx-a11y/no-redundant-roles': 'error',
      'jsx-a11y/no-static-element-interactions': 'error',

      // Target size (WCAG 2.2)
      'jsx-a11y/control-has-associated-label': 'error',
      'jsx-a11y/prefer-tag-over-role': 'warn',
    },
  },
];
```

**Coverage**: 85% of WCAG 2.2 Level AA criteria (30+ rules)

---

### Component Testing with axe-core

#### jest-axe (Jest + React Testing Library)

**Setup** (jest.setup.ts):
```typescript
import { toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);
```

**Component Test**:
```tsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import { AccessibleButton } from './accessible-button';

describe('AccessibleButton Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <AccessibleButton onClick={() => {}}>Click me</AccessibleButton>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should handle loading state accessibly', async () => {
    const { container } = render(
      <AccessibleButton isLoading onClick={() => {}}>Submit</AccessibleButton>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

---

#### vitest-axe (Vitest + React Testing Library)

**Setup** (vitest.setup.ts):
```typescript
import { expect } from 'vitest';
import { axe, toHaveNoViolations } from 'vitest-axe';

expect.extend(toHaveNoViolations);
export { axe };
```

**Component Test**:
```tsx
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { axe } from '../vitest.setup';
import { AccessibleModal } from './accessible-modal';

describe('AccessibleModal Accessibility', () => {
  it('should have no violations when open', async () => {
    const { container } = render(
      <AccessibleModal isOpen onClose={() => {}}>
        Modal Content
      </AccessibleModal>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

**What axe-core Tests**:
- Color contrast (4.5:1 text, 3:1 large text)
- ARIA attributes (valid roles, properties)
- Form labels (explicit association)
- Keyboard accessibility (interactive elements focusable)
- Focus management (logical tab order)
- Semantic HTML (proper heading hierarchy)

---

### Runtime Validation with axe-core

#### Development Browser Integration

```typescript
// app/layout.tsx (Next.js) or main.tsx (Vite)
if (process.env.NODE_ENV === 'development') {
  import('@axe-core/react').then((axe) => {
    const React = await import('react');
    const ReactDOM = await import('react-dom');
    axe.default(React, ReactDOM, 1000);  // Check every 1 second
  });
}
```

**Behavior**: Violations logged to browser console in development

---

### Accessible Component Patterns

#### Pattern 1: Accessible Modal/Dialog

**Requirements**:
- `role="dialog"` or `aria-modal="true"`
- `aria-labelledby` (modal title)
- Focus trap (prevent Tab from leaving)
- Focus restoration (return focus on close)
- Escape key handler

```tsx
import { useEffect, useRef } from 'react';
import FocusLock from 'react-focus-lock';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
  const titleId = useRef(`modal-title-${Math.random()}`);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
    } else if (previousFocusRef.current) {
      previousFocusRef.current.focus();  // ✅ Restore focus
    }
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();  // ✅ Close on Escape
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId.current}
      className="modal-overlay"
    >
      <FocusLock>  {/* ✅ Focus trap */}
        <div className="modal-content">
          <h2 id={titleId.current}>{title}</h2>
          {children}
          <button onClick={onClose}>Close</button>
        </div>
      </FocusLock>
    </div>
  );
}
```

**Testing**:
```tsx
const { container } = render(
  <AccessibleModal isOpen onClose={() => {}}>Content</AccessibleModal>
);
const results = await axe(container);
expect(results).toHaveNoViolations();
```

---

#### Pattern 2: Accessible Form

**Requirements**:
- `<label htmlFor>` explicit association
- `aria-describedby` for hints/errors
- `aria-invalid` for validation state
- `aria-live="assertive"` for error announcements

```tsx
import { useState } from 'react';

export function AccessibleForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const emailId = 'email-input';
  const errorId = 'email-error';
  const hintId = 'email-hint';

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email.includes('@')) {
      setError('Please enter a valid email address');
    } else {
      setError('');
      // Submit form
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor={emailId}>Email Address</label>  {/* ✅ Explicit label */}

      <input
        id={emailId}
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        aria-describedby={error ? `${hintId} ${errorId}` : hintId}
        aria-invalid={!!error}  {/* ✅ Validation state */}
        required
      />

      <span id={hintId} className="hint">
        We'll never share your email
      </span>

      {error && (
        <span
          id={errorId}
          role="alert"
          aria-live="assertive"  {/* ✅ Screen reader announcement */}
          className="error"
        >
          {error}
        </span>
      )}

      <button type="submit">Subscribe</button>
    </form>
  );
}
```

---

#### Pattern 3: Accessible Button

**Requirements**:
- Semantic `<button>` (not `<div onClick>`)
- `aria-label` for icon-only buttons
- `aria-disabled` for disabled state (if not using `disabled` attribute)
- Loading state with `aria-busy`

```tsx
interface ButtonProps {
  onClick: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
}

export function AccessibleButton({ onClick, isLoading, disabled, children }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      aria-busy={isLoading}  {/* ✅ Loading state */}
      aria-disabled={disabled || isLoading}
      type="button"
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
}

// Icon-only button
export function AccessibleIconButton({ onClick, label }: { onClick: () => void; label: string }) {
  return (
    <button
      onClick={onClick}
      aria-label={label}  {/* ✅ Screen reader text */}
      type="button"
    >
      <Icon />  {/* Visual icon */}
    </button>
  );
}
```

---

### Accessible Component Libraries

#### Option 1: Radix UI (Recommended)

**Why Radix UI**:
- WCAG 2.2 Level AA compliant out-of-the-box
- Unstyled (bring your own CSS/Tailwind)
- Excellent TypeScript support
- Used by shadcn/ui, Vercel, Linear

**Installation**:
```bash
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
```

**Example** (Accessible Dialog):
```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>Open Dialog</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="overlay" />
        <Dialog.Content className="content">
          <Dialog.Title>Dialog Title</Dialog.Title>
          <Dialog.Description>Dialog description</Dialog.Description>
          <Dialog.Close>Close</Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

**What Radix Provides**:
- Focus trap (automatic)
- Focus restoration (automatic)
- Escape key handling (automatic)
- ARIA attributes (role, aria-labelledby, aria-describedby)
- Keyboard navigation (Arrow keys, Home, End)

---

#### Option 2: React Aria

**Why React Aria**:
- Adobe-maintained (industry-leading accessibility)
- Behavior hooks + styled components
- Cross-platform (web, React Native)

**Installation**:
```bash
pnpm add react-aria-components
```

**Example** (Accessible Button):
```tsx
import { Button } from 'react-aria-components';

export function MyButton() {
  return (
    <Button onPress={() => console.log('Pressed')}>
      Click me
    </Button>
  );
}
```

---

#### Option 3: Headless UI

**Why Headless UI**:
- Tailwind Labs official library
- Perfect integration with Tailwind CSS
- Smaller bundle size than Radix

**Installation**:
```bash
pnpm add @headlessui/react
```

**Example** (Accessible Menu):
```tsx
import { Menu } from '@headlessui/react';

export function MyMenu() {
  return (
    <Menu>
      <Menu.Button>Options</Menu.Button>
      <Menu.Items>
        <Menu.Item>{({ active }) => <a href="/edit">Edit</a>}</Menu.Item>
        <Menu.Item>{({ active }) => <a href="/delete">Delete</a>}</Menu.Item>
      </Menu.Items>
    </Menu>
  );
}
```

---

### Manual Testing Checklist

**15% of WCAG criteria require manual testing** (keyboard navigation, screen reader, visual inspection):

#### 1. Keyboard Navigation

- [ ] Tab through all interactive elements (visible focus indicator)
- [ ] Shift+Tab reverses tab order
- [ ] Enter/Space activates buttons and links
- [ ] Arrow keys navigate menus, selects, tabs
- [ ] Escape closes modals and menus
- [ ] No keyboard traps (can Tab out of all components)

#### 2. Screen Reader Testing

**Test with**:
- **Windows**: NVDA (free), JAWS (paid)
- **macOS**: VoiceOver (built-in)
- **iOS**: VoiceOver (Settings → Accessibility)
- **Android**: TalkBack (Settings → Accessibility)

**Checklist**:
- [ ] All images have descriptive alt text (or alt="" for decorative)
- [ ] Form inputs announced with labels
- [ ] Buttons announce role ("button") and state ("expanded", "pressed")
- [ ] Error messages announced via aria-live
- [ ] Modal title announced when opened
- [ ] Skip links work ("Skip to main content")

#### 3. Visual Inspection

- [ ] Focus indicator visible on all interactive elements (4.5:1 contrast)
- [ ] Text contrast ≥4.5:1 (small text), ≥3:1 (large text)
- [ ] Interactive targets ≥24×24px (WCAG 2.2 Target Size Minimum)
- [ ] Sticky headers don't obscure focused elements (WCAG 2.2 Focus Not Obscured)
- [ ] No text in images (use real text with CSS styling)

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-022** (React Linting) | ESLint Configuration | Add jsx-a11y plugin to eslint.config.mjs alongside React/TypeScript rules |
| **SAP-021** (Testing) | Component Testing | Use jest-axe or vitest-axe with React Testing Library for accessibility tests |
| **SAP-024** (Styling) | Focus Indicators | Use Tailwind's `focus-visible:ring` utilities for accessible focus styles |
| **SAP-020** (Next.js 15 Foundation) | Image Alt Text | Next.js Image component requires alt prop (enforced by jsx-a11y/alt-text) |
| **SAP-005** (CI/CD) | Automated Validation | Run ESLint + axe tests in GitHub Actions, fail builds on violations |
| **SAP-025** (Performance) | Lighthouse CI | Lighthouse accessibility score enforced alongside performance metrics |

---

## 🏆 Success Metrics

- **ESLint Coverage**: 85% of WCAG criteria (30+ rules enforced)
- **Component Test Coverage**: 100% of custom components tested with axe-core
- **Lighthouse Accessibility Score**: ≥90 (A), 75-89 (B), 50-74 (C), <50 (F)
- **Manual Testing**: 100% of critical user flows tested with keyboard + screen reader
- **Zero High/Critical Violations**: axe-core reports no high or critical issues
- **CI/CD**: 100% Pull Requests validated with ESLint + axe tests

---

## 🔧 Troubleshooting

### Problem: ESLint jsx-a11y/alt-text Errors

**Symptom**: `Missing alt attribute on <img>`

**Common Causes**:
1. Image missing alt prop
2. Decorative image with non-empty alt
3. next/image without alt

**Solutions**:

```tsx
// ❌ Missing alt
<img src="/logo.png" />

// ✅ Descriptive alt (functional image)
<img src="/logo.png" alt="Company Logo" />

// ✅ Empty alt (decorative image)
<img src="/divider.png" alt="" />

// ✅ Next.js Image
<Image src="/hero.jpg" alt="Hero image showing product" width={1920} height={1080} />
```

**Validation**: Run `pnpm eslint .` and verify no jsx-a11y/alt-text errors

---

### Problem: axe-core Color Contrast Violations

**Symptom**: `Elements must meet enhanced color contrast ratio thresholds`

**Common Causes**:
1. Light gray text on white background (contrast <4.5:1)
2. Colored text without sufficient contrast
3. Button text on colored background

**Solutions**:

```css
/* ❌ Low contrast (2.8:1) */
.text {
  color: #999;  /* Light gray */
  background: #fff;  /* White */
}

/* ✅ High contrast (7.0:1) */
.text {
  color: #333;  /* Dark gray */
  background: #fff;  /* White */
}

/* ✅ Use Tailwind contrast-safe colors */
.text {
  @apply text-gray-900;  /* Very dark gray, 15.8:1 on white */
}
```

**Tool**: Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) or browser DevTools

**Validation**: Run axe-core tests, verify no color-contrast violations

---

### Problem: jest-axe/vitest-axe Fails with "Element is not focusable"

**Symptom**: `Ensures elements with click handlers are focusable`

**Common Causes**:
1. `<div onClick>` without `role="button"` and `tabIndex={0}`
2. Interactive element without keyboard handler

**Solutions**:

```tsx
// ❌ Non-focusable click handler
<div onClick={handleClick}>Click me</div>

// ✅ Option 1: Use semantic button
<button onClick={handleClick}>Click me</button>

// ✅ Option 2: Make div focusable (not recommended)
<div
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  role="button"
  tabIndex={0}
>
  Click me
</div>
```

**Best Practice**: Always use semantic `<button>` for interactive elements

**Validation**: Run `pnpm test` and verify axe tests pass

---

### Problem: Focus Trap Not Working in Modal

**Symptom**: Tab key escapes modal, focusing elements behind overlay

**Common Causes**:
1. react-focus-lock not installed or imported
2. FocusLock wrapping only part of modal
3. Multiple modals open simultaneously

**Solutions**:

```tsx
// ❌ Focus trap missing
<div role="dialog">
  <h2>Modal Title</h2>
  <button onClick={onClose}>Close</button>
</div>

// ✅ Focus trap with react-focus-lock
import FocusLock from 'react-focus-lock';

<div role="dialog" aria-modal="true">
  <FocusLock>  {/* ✅ Wrap entire modal content */}
    <h2>Modal Title</h2>
    <button onClick={onClose}>Close</button>
  </FocusLock>
</div>
```

**Validation**: Open modal, press Tab repeatedly, verify focus stays within modal

---

### Problem: Screen Reader Not Announcing Error Messages

**Symptom**: Form error appears visually but screen reader silent

**Common Causes**:
1. Error message missing `aria-live="assertive"`
2. Error not associated with input via `aria-describedby`
3. Error appearing before input renders

**Solutions**:

```tsx
// ❌ Error not announced
{error && <span className="error">{error}</span>}

// ✅ Error with aria-live
const errorId = 'email-error';

<input
  aria-describedby={error ? errorId : undefined}
  aria-invalid={!!error}
/>

{error && (
  <span
    id={errorId}
    role="alert"
    aria-live="assertive"  {/* ✅ Screen reader announces */}
  >
    {error}
  </span>
)}
```

**Validation**: Open VoiceOver/NVDA, trigger error, verify screen reader announces message

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete accessibility specification (62KB, 31-min read)
- **[AGENTS.md](AGENTS.md)** - Agent accessibility workflows (19KB, 10-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (17KB, 9-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Setup guide (36KB, 18-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

### External Resources

- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/) - Official W3C reference
- [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) - ESLint a11y rules
- [jest-axe](https://github.com/nickcolley/jest-axe) - Jest + axe-core integration
- [Radix UI](https://www.radix-ui.com/) - Accessible React primitives
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Color contrast tool
- [A11y Project Checklist](https://www.a11yproject.com/checklist/) - Manual testing guide

---

**Version History**:
- **1.0.0** (2025-11-05) - Initial React Accessibility with WCAG 2.2 Level AA compliance, jsx-a11y, axe-core

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
