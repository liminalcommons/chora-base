# SAP-026: React Accessibility Protocol Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-02

---

## Overview

This protocol specification defines the **technical implementation standards** for building WCAG 2.2 Level AA compliant React applications. It covers ESLint configuration, automated testing protocols, component accessibility patterns, and manual testing workflows.

**Compliance Target**: WCAG 2.2 Level AA (W3C Recommendation, October 5, 2023)

**Technology Stack**:
- `eslint-plugin-jsx-a11y@^6.10.2` - Automated linting (85% coverage)
- `jest-axe@^9.0.0` / `vitest-axe@^1.0.0` - Component testing
- `axe-core@^4.10.2` - Runtime validation
- `react-focus-lock@^2.13.2` - Focus management
- Radix UI / React Aria / Headless UI - Accessible component libraries (optional)

---

## WCAG 2.2 Level AA Compliance Matrix

### New WCAG 2.2 Criteria (9 additions)

| Criterion | Level | Requirement | React Implementation | Automated Testing | Manual Testing |
|-----------|-------|-------------|---------------------|-------------------|----------------|
| **2.4.11** | AA | Focus Not Obscured (Minimum) | Prevent sticky headers from hiding focus | ❌ Manual | ✅ Tab through page, verify focus visible |
| **2.4.12** | AAA | Focus Not Obscured (Enhanced) | Focus fully visible, not partially | ❌ Manual | ✅ Visual inspection |
| **2.4.13** | AAA | Focus Appearance | High contrast focus (3:1 ratio) | ⚠️ axe-core | ✅ Contrast checker |
| **2.5.7** | AA | Dragging Movements | Provide click alternative to drag | ❌ Manual | ✅ Test without mouse |
| **2.5.8** | AA | Target Size (Minimum) | 24×24 CSS pixels interactive | ⚠️ axe-core | ✅ Measure with DevTools |
| **3.2.6** | A | Consistent Help | Help link in same location | ❌ Manual | ✅ Check across pages |
| **3.3.7** | A | Redundant Entry | Don't re-ask for information | ❌ Manual | ✅ Test multi-step flows |
| **3.3.8** | AA | Accessible Authentication | No cognitive tests, allow password managers | ❌ Manual | ✅ Test login with password manager |
| **3.3.9** | AAA | Accessible Auth (Enhanced) | No object recognition | ❌ Manual | ✅ Verify no CAPTCHA images |

### Foundational WCAG 2.1 Level AA Criteria

| Criterion | Requirement | React Implementation | Automated Testing |
|-----------|-------------|---------------------|-------------------|
| **1.1.1** | Non-text Content | `<img alt="description">` or decorative `alt=""` | ✅ jsx-a11y/alt-text |
| **1.4.3** | Contrast (Minimum) | 4.5:1 text, 3:1 large text | ✅ axe-core color-contrast |
| **2.1.1** | Keyboard | All functionality via keyboard | ⚠️ jsx-a11y (partial) |
| **2.4.7** | Focus Visible | CSS `:focus-visible` styles | ⚠️ axe-core (partial) |
| **3.3.2** | Labels or Instructions | `<label htmlFor>`, `aria-label` | ✅ jsx-a11y/label-has-associated-control |
| **4.1.2** | Name, Role, Value | Semantic HTML or ARIA | ✅ jsx-a11y/aria-props |

**Legend**:
- ✅ Fully automated detection
- ⚠️ Partial automated detection (manual verification needed)
- ❌ Requires manual testing

---

## ESLint Configuration (jsx-a11y)

### Recommended Configuration

**File**: `eslint.config.mjs` (ESLint 9 flat config)

```javascript
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  {
    plugins: {
      'jsx-a11y': jsxA11y,
    },
    rules: {
      // Critical errors (block build)
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/anchor-has-content': 'error',
      'jsx-a11y/anchor-is-valid': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-proptypes': 'error',
      'jsx-a11y/aria-role': 'error',
      'jsx-a11y/aria-unsupported-elements': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/heading-has-content': 'error',
      'jsx-a11y/html-has-lang': 'error',
      'jsx-a11y/iframe-has-title': 'error',
      'jsx-a11y/img-redundant-alt': 'error',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      'jsx-a11y/media-has-caption': 'error',
      'jsx-a11y/mouse-events-have-key-events': 'error',
      'jsx-a11y/no-access-key': 'error',
      'jsx-a11y/no-autofocus': 'warn', // Warn only (sometimes needed)
      'jsx-a11y/no-distracting-elements': 'error',
      'jsx-a11y/no-interactive-element-to-noninteractive-role': 'error',
      'jsx-a11y/no-noninteractive-element-interactions': 'error',
      'jsx-a11y/no-noninteractive-element-to-interactive-role': 'error',
      'jsx-a11y/no-noninteractive-tabindex': 'error',
      'jsx-a11y/no-redundant-roles': 'error',
      'jsx-a11y/no-static-element-interactions': 'error',
      'jsx-a11y/role-has-required-aria-props': 'error',
      'jsx-a11y/role-supports-aria-props': 'error',
      'jsx-a11y/scope': 'error',
      'jsx-a11y/tabindex-no-positive': 'error',

      // Best practices (warnings)
      'jsx-a11y/accessible-emoji': 'warn',
      'jsx-a11y/aria-activedescendant-has-tabindex': 'warn',
      'jsx-a11y/autocomplete-valid': 'warn',
      'jsx-a11y/control-has-associated-label': 'warn',
      'jsx-a11y/lang': 'warn',
      'jsx-a11y/no-aria-hidden-on-focusable': 'warn',
    },
  },
];
```

### Rule Severity Levels

**Errors** (block commit/build):
- Missing alt text (`alt-text`)
- Invalid ARIA attributes (`aria-props`, `aria-proptypes`)
- Interactive elements without keyboard handlers (`click-events-have-key-events`)
- Missing form labels (`label-has-associated-control`)
- Positive tabindex values (`tabindex-no-positive`)

**Warnings** (fix soon, don't block):
- Autofocus usage (`no-autofocus`) - Sometimes legitimate (modals)
- Missing control labels (`control-has-associated-label`) - May have visually hidden labels
- Emoji without `role="img"` (`accessible-emoji`)

### Disabling Rules (When Necessary)

```tsx
// Disable for single line (with justification comment)
{/* eslint-disable-next-line jsx-a11y/no-autofocus -- Modal needs focus on open */}
<input autoFocus />

// Disable for file (only when entire file is exempt)
/* eslint-disable jsx-a11y/media-has-caption */
// Video player component with external caption controls
```

**When to Disable**:
- `no-autofocus`: Modals, dialogs, search inputs (with user intent)
- `no-noninteractive-tabindex`: Custom scrollable regions (with keyboard handlers)
- `click-events-have-key-events`: When parent element handles keyboard (avoid duplication)

**Never Disable**:
- `alt-text` (images must have alt text or be decorative)
- `aria-props` (invalid ARIA breaks assistive technology)
- `label-has-associated-control` (forms must have labels)

---

## Automated Testing Protocols

### jest-axe (Next.js with Jest)

**Installation**:
```bash
npm install --save-dev jest-axe @axe-core/react
```

**Setup File**: `jest.setup.ts`
```typescript
import { toHaveNoViolations } from 'jest-axe';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Configure axe-core
import { configureAxe } from 'jest-axe';

export const axe = configureAxe({
  rules: {
    // Disable rules that conflict with dynamic React patterns
    'region': { enabled: false }, // React portals cause false positives
  },
});
```

**Component Test Example**:
```typescript
import { render } from '@testing-library/react';
import { axe } from '../jest.setup';
import { AccessibleModal } from './accessible-modal';

describe('AccessibleModal Accessibility', () => {
  it('should have no accessibility violations when open', async () => {
    const { container } = render(
      <AccessibleModal isOpen={true} onClose={() => {}}>
        <h2>Modal Title</h2>
        <p>Modal content</p>
      </AccessibleModal>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no violations when closed', async () => {
    const { container } = render(
      <AccessibleModal isOpen={false} onClose={() => {}}>
        Content
      </AccessibleModal>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### vitest-axe (Vite with Vitest)

**Installation**:
```bash
npm install --save-dev vitest-axe axe-core
```

**Setup File**: `vitest.setup.ts`
```typescript
import { expect } from 'vitest';
import { axe, toHaveNoViolations } from 'vitest-axe';

// Extend Vitest matchers
expect.extend(toHaveNoViolations);

// Export configured axe instance
export { axe };
```

**Component Test Example**:
```typescript
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { axe } from '../vitest.setup';
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
      <AccessibleButton isLoading onClick={() => {}}>
        Submit
      </AccessibleButton>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### axe-core Runtime Testing

**Browser Integration** (Development):
```typescript
// app/layout.tsx (Next.js) or main.tsx (Vite)
if (process.env.NODE_ENV === 'development') {
  import('@axe-core/react').then((axe) => {
    axe.default(React, ReactDOM, 1000); // Check every 1 second
  });
}
```

**Manual Scan**:
```typescript
import axe from 'axe-core';

// Run on current page
axe.run(document.body).then((results) => {
  console.log('Violations:', results.violations);
  console.log('Passes:', results.passes);
});
```

**CI/CD Integration** (Lighthouse CI):
```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests
on: [pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npm run test:a11y # Runs jest-axe tests
      - uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: './lighthouserc.json'
```

---

## Component Accessibility Patterns

### Pattern 1: Accessible Modal/Dialog

**ARIA Requirements**:
- `role="dialog"` or `aria-modal="true"` (signal modal state)
- `aria-labelledby` (reference to modal title)
- `aria-describedby` (reference to modal description, optional)
- Focus trap (prevent Tab from leaving modal)
- Focus restoration (return focus on close)
- Escape key handler (close modal)

**Implementation**:
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
      // Store current focus
      previousFocusRef.current = document.activeElement as HTMLElement;
    } else if (previousFocusRef.current) {
      // Restore focus on close
      previousFocusRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
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
      <FocusLock>
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

**Key Points**:
- `FocusLock` component traps Tab key within modal
- `aria-modal="true"` signals to screen readers this is a modal
- `aria-labelledby` references title (screen reader announces)
- Escape key closes modal (expected behavior)
- Focus restoration returns to triggering element

---

### Pattern 2: Accessible Form

**ARIA Requirements**:
- `<label htmlFor>` explicit association (NOT implicit wrapping)
- `aria-describedby` for hints and error messages
- `aria-invalid` for validation state
- `aria-live="assertive"` for error announcements
- `aria-required` for required fields (or HTML5 `required`)

**Implementation**:
```tsx
import { useState } from 'react';

export function AccessibleForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const emailId = 'email-input';
  const hintId = 'email-hint';
  const errorId = 'email-error';

  const validate = () => {
    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return false;
    }
    setError('');
    return true;
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); validate(); }}>
      <div>
        <label htmlFor={emailId}>
          Email Address <span aria-label="required">*</span>
        </label>

        <input
          id={emailId}
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-describedby={`${hintId} ${error ? errorId : ''}`}
          aria-invalid={!!error}
          aria-required="true"
          required
        />

        <p id={hintId} className="hint">
          We'll never share your email
        </p>

        {error && (
          <p id={errorId} role="alert" aria-live="assertive" className="error">
            {error}
          </p>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

**Key Points**:
- Explicit `<label htmlFor>` (NOT implicit `<label><input></label>`)
- `aria-describedby` references both hint and error
- `aria-invalid="true"` when validation fails
- `role="alert"` + `aria-live="assertive"` announces errors
- Both `aria-required` and `required` (redundant but compatible)

---

### Pattern 3: Accessible Button

**ARIA Requirements**:
- Semantic `<button>` element (NOT `<div onClick>`)
- `aria-label` for icon-only buttons
- `aria-busy="true"` for loading states
- `disabled` attribute (NOT `aria-disabled` alone)

**Implementation**:
```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  isLoading?: boolean;
  icon?: React.ReactNode;
  children?: React.ReactNode;
}

export function AccessibleButton({
  variant = 'primary',
  isLoading = false,
  icon,
  children,
  disabled,
  ...props
}: ButtonProps) {
  // Icon-only button requires aria-label
  const isIconOnly = icon && !children;

  return (
    <button
      {...props}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      aria-label={isIconOnly ? props['aria-label'] : undefined}
      className={`button button-${variant}`}
    >
      {isLoading ? (
        <>
          <span className="spinner" aria-hidden="true" />
          <span className="sr-only">Loading...</span>
        </>
      ) : (
        <>
          {icon && <span aria-hidden="true">{icon}</span>}
          {children}
        </>
      )}
    </button>
  );
}

// Usage
<AccessibleButton icon={<SearchIcon />} aria-label="Search">
  {/* Icon-only needs aria-label */}
</AccessibleButton>

<AccessibleButton isLoading onClick={handleSubmit}>
  Submit Form
</AccessibleButton>
```

**Key Points**:
- Semantic `<button>` (gets role, keyboard behavior automatically)
- `disabled` attribute (grays out, prevents click/focus)
- `aria-busy="true"` during loading (screen reader announces)
- Icons marked `aria-hidden="true"` (decorative)
- Loading text in `sr-only` class (screen reader only)

---

### Pattern 4: Accessible Dropdown

**ARIA Requirements**:
- `aria-expanded` (true/false based on open state)
- `aria-controls` (references dropdown menu ID)
- `aria-haspopup="true"` (signals dropdown exists)
- Arrow keys navigate options
- Enter/Space select option
- Escape closes dropdown

**Implementation** (simplified, use Radix UI in production):
```tsx
import { useState, useRef, useEffect } from 'react';

export function AccessibleDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState('Option 1');
  const menuId = 'dropdown-menu';

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setIsOpen(false);
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setIsOpen(!isOpen);
    }
  };

  return (
    <div className="dropdown">
      <button
        aria-expanded={isOpen}
        aria-controls={menuId}
        aria-haspopup="true"
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
      >
        {selected}
      </button>

      {isOpen && (
        <ul id={menuId} role="menu">
          <li role="menuitem">
            <button onClick={() => { setSelected('Option 1'); setIsOpen(false); }}>
              Option 1
            </button>
          </li>
          <li role="menuitem">
            <button onClick={() => { setSelected('Option 2'); setIsOpen(false); }}>
              Option 2
            </button>
          </li>
        </ul>
      )}
    </div>
  );
}
```

**Production Recommendation**: Use Radix UI `<DropdownMenu>` or Headless UI `<Menu>` instead of building from scratch. These handle all keyboard navigation, ARIA, and focus management automatically.

---

### Pattern 5: Skip Link

**ARIA Requirements**:
- Link to main content ID (`href="#main"`)
- Visually hidden until focused
- First focusable element on page
- Keyboard accessible (Tab to reach)

**Implementation**:
```tsx
// components/skip-link.tsx
export function SkipLink() {
  return (
    <a href="#main-content" className="skip-link">
      Skip to main content
    </a>
  );
}

// CSS
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}

// Usage in layout
<body>
  <SkipLink />
  <header>...</header>
  <main id="main-content" tabIndex={-1}>
    {/* tabIndex={-1} allows programmatic focus */}
  </main>
</body>
```

**Key Points**:
- Positioned off-screen until focused (`top: -40px`)
- Moves on-screen on focus (`:focus { top: 0; }`)
- Links to `#main-content` with `tabIndex={-1}` (allows focus)
- First element in tab order

---

### Pattern 6: Accessible Tabs

**ARIA Requirements**:
- `role="tablist"` on container
- `role="tab"` on tab buttons
- `role="tabpanel"` on content panels
- `aria-selected="true"` on active tab
- `aria-controls` on tabs (references panel ID)
- Arrow keys navigate tabs (Left/Right or Up/Down)
- Enter/Space activate tab
- Home/End jump to first/last tab

**Implementation** (simplified):
```tsx
import { useState } from 'react';

export function AccessibleTabs() {
  const [activeTab, setActiveTab] = useState(0);
  const tabs = ['Tab 1', 'Tab 2', 'Tab 3'];

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      setActiveTab((index + 1) % tabs.length);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      setActiveTab((index - 1 + tabs.length) % tabs.length);
    } else if (e.key === 'Home') {
      e.preventDefault();
      setActiveTab(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      setActiveTab(tabs.length - 1);
    }
  };

  return (
    <div>
      <div role="tablist" aria-label="Example tabs">
        {tabs.map((tab, index) => (
          <button
            key={index}
            role="tab"
            aria-selected={activeTab === index}
            aria-controls={`panel-${index}`}
            tabIndex={activeTab === index ? 0 : -1}
            onClick={() => setActiveTab(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab}
          </button>
        ))}
      </div>

      {tabs.map((tab, index) => (
        <div
          key={index}
          role="tabpanel"
          id={`panel-${index}`}
          hidden={activeTab !== index}
          tabIndex={0}
        >
          Content for {tab}
        </div>
      ))}
    </div>
  );
}
```

**Key Points**:
- Roving `tabIndex` (only active tab has `tabIndex={0}`)
- Arrow keys navigate (Left/Right)
- `aria-selected="true"` on active tab
- `aria-controls` links tab to panel
- `hidden` attribute hides inactive panels

---

## Radix UI Integration

### Why Radix UI?

**Pros**:
- Unstyled (no CSS opinions, works with Tailwind/CSS-in-JS)
- Full ARIA support out of the box
- Keyboard navigation handled automatically
- Focus management included
- Production-tested (used by Vercel, Linear, Raycast)

**Cons**:
- Requires learning Radix API
- Some components are verbose (Popover, Dialog)
- SSR hydration mismatches if not careful

### Radix UI Example (Modal)

```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function RadixModal({ trigger, title, children }: {
  trigger: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        {trigger}
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />
        <Dialog.Content className="modal-content">
          <Dialog.Title>{title}</Dialog.Title>
          <Dialog.Description>
            {children}
          </Dialog.Description>
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

**Radix UI Handles**:
- ✅ Focus trap (automatic)
- ✅ Focus restoration (automatic)
- ✅ Escape key (automatic)
- ✅ ARIA attributes (`aria-modal`, `aria-labelledby`, etc.)
- ✅ Scroll lock (prevents body scroll when open)

**You Handle**:
- ❌ Styling (Radix is unstyled)
- ❌ Animations (add with Tailwind or Framer Motion)

---

## Manual Testing Workflows

### Keyboard Navigation Testing

**Checklist**:
- [ ] Tab key moves through all interactive elements in logical order
- [ ] Shift+Tab moves backward through elements
- [ ] Enter key activates buttons and links
- [ ] Space key toggles checkboxes, presses buttons
- [ ] Arrow keys navigate dropdowns, tabs, sliders
- [ ] Escape key closes modals, dropdowns, tooltips
- [ ] Home/End keys jump to first/last item (in lists)
- [ ] Focus indicators are always visible (3:1 contrast minimum)

**Test Workflow**:
1. Put away mouse (don't touch it during test)
2. Tab through entire page from top to bottom
3. Verify every interactive element is reachable
4. Verify focus indicator is visible on each element
5. Activate elements with Enter/Space
6. Navigate modals/dropdowns with Arrow keys
7. Close overlays with Escape

### Screen Reader Testing (NVDA)

**Setup** (Windows):
1. Download NVDA (free): https://www.nvaccess.org/download/
2. Install with default settings
3. NVDA starts automatically (Ctrl+Alt+N to toggle)

**Test Workflow**:
1. Start NVDA (Ctrl+Alt+N)
2. Navigate with down arrow (reads next element)
3. Navigate headings with H key (jumps to next heading)
4. Navigate links with K key
5. Navigate form fields with F key
6. Verify form labels announce correctly
7. Test error messages announce (aria-live)
8. Verify modal title announces when opened

**Common Issues**:
- Images without alt text (NVDA says "graphic" with no description)
- Form inputs without labels (NVDA says field type but not purpose)
- Errors not announced (missing aria-live or role="alert")
- Button purpose unclear (icon-only without aria-label)

### Color Contrast Testing

**Tools**:
- Chrome DevTools (Inspect element → Accessibility tab → Contrast ratio)
- Lighthouse (Accessibility audit)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Requirements**:
- Normal text (< 18px): 4.5:1 contrast minimum
- Large text (≥ 18px or ≥ 14px bold): 3:1 contrast minimum
- UI components (buttons, form borders): 3:1 contrast minimum

**Test Workflow**:
1. Run Lighthouse accessibility audit
2. Check "Contrast" failures
3. Use DevTools to measure specific elements
4. Adjust colors in design system tokens
5. Re-test until all pass

---

## Error Handling

### Common ESLint jsx-a11y Errors

**Error**: `img elements must have an alt prop`
**Fix**: Add `alt` attribute (descriptive or empty for decorative)
```tsx
<img src="logo.png" alt="Company logo" />
<img src="decorative.png" alt="" /> {/* Decorative, screen reader skips */}
```

**Error**: `Form label must have associated control`
**Fix**: Use `htmlFor` to explicitly link label to input
```tsx
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

**Error**: `onClick must be accompanied by onKeyDown`
**Fix**: Use semantic `<button>` instead of `<div onClick>`
```tsx
{/* Bad */}
<div onClick={handleClick}>Click me</div>

{/* Good */}
<button onClick={handleClick}>Click me</button>
```

**Error**: `Avoid positive integer values for tabIndex`
**Fix**: Remove positive tabIndex, use DOM order or -1
```tsx
{/* Bad */}
<button tabIndex={1}>First</button>

{/* Good */}
<button>First (DOM order)</button>
<div tabIndex={-1}>Programmatically focusable</div>
```

---

## Performance Considerations

**ESLint jsx-a11y**: Runs at compile time, zero runtime cost
**jest-axe**: Adds ~500ms per test (acceptable for CI)
**axe-core**: Runtime checks add ~100-200ms per scan (development only)
**Focus management**: Negligible overhead (<10ms)
**ARIA attributes**: Zero runtime cost (browser native)

**Recommendation**: Run axe-core only in development, not production.

---

## Versioning & Compatibility

**Supported**:
- React 19+ (Suspense, Server Components)
- Next.js 15+ (App Router)
- Vite 7+
- TypeScript 5.7+

**Not Supported**:
- React <18 (class components, legacy patterns)
- Next.js Pages Router (different SSR patterns)
- Create React App (deprecated, use Vite)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Next Review**: 2026-02-02 (3 months)
