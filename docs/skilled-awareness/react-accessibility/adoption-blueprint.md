# SAP-026: React Accessibility - Adoption Blueprint

**Quick Start Guide for Implementing WCAG 2.2 Level AA Compliance**

This blueprint provides step-by-step instructions for adopting SAP-026 in your React project.

---

## Prerequisites

Before starting, ensure you have:

- ✅ **SAP-020** (React Foundation) - Next.js 15 or Vite 7 project
- ✅ **SAP-021** (React Testing) - Vitest or Jest configured
- ✅ **SAP-022** (React Linting) - ESLint 9 with jsx-a11y plugin (already includes accessibility linting)
- ✅ React 19+, TypeScript 5.7+, Node.js 22.x

---

## Implementation Steps

### Step 1: Install Dependencies (5 minutes)

```bash
# Accessibility testing dependencies
npm install --save-dev jest-axe @axe-core/react  # For Next.js with Jest
# OR
npm install --save-dev vitest-axe @axe-core/react  # For Vite with Vitest

# Focus management for modals
npm install react-focus-lock

# Optional: Accessible component libraries (choose one or none)
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tabs
# OR
npm install @headlessui/react
# OR
npm install react-aria
```

### Step 2: Configure Testing (10 minutes)

**For Next.js (Jest):**

1. Copy `templates/react/accessibility/nextjs/jest.setup.ts` to your project root
2. Update `jest.config.js`:
   ```javascript
   module.exports = {
     setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
     // ... other config
   }
   ```

**For Vite (Vitest):**

1. Copy `templates/react/accessibility/vite/vitest.setup.ts` to your project root
2. Update `vitest.config.ts`:
   ```typescript
   export default defineConfig({
     test: {
       setupFiles: ['./vitest.setup.ts'],
       // ... other config
     },
   })
   ```

### Step 3: Copy Component Templates (15 minutes)

Copy the 6 essential component templates from `templates/react/accessibility/shared/components/` to your project:

1. `accessible-modal.tsx` - Modal/dialog with focus trap
2. `accessible-form.tsx` - Form with validation and error handling
3. `accessible-button.tsx` - Button with loading states and icon support
4. `accessible-dropdown.tsx` - Dropdown with keyboard navigation
5. `skip-link.tsx` - Skip navigation link
6. `accessible-tabs.tsx` - Tabs with arrow key navigation

Customize styling and props to match your design system.

### Step 4: Add Skip Link to Layout (2 minutes)

**Next.js App Router:**

```tsx
// app/layout.tsx
import { SkipLink } from '@/components/skip-link'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <SkipLink />
        <header>
          <nav>{/* Navigation */}</nav>
        </header>
        <main id="main-content" tabIndex={-1}>
          {children}
        </main>
      </body>
    </html>
  )
}
```

**Vite:**

```tsx
// src/App.tsx
import { SkipLink } from './components/skip-link'

function App() {
  return (
    <>
      <SkipLink />
      <header>
        <nav>{/* Navigation */}</nav>
      </header>
      <main id="main-content" tabIndex={-1}>
        {/* Content */}
      </main>
    </>
  )
}
```

### Step 5: Write Accessibility Tests (Ongoing)

For every component, add an accessibility test:

```typescript
import { axe, toHaveNoViolations } from 'jest-axe' // or 'vitest-axe'
expect.extend(toHaveNoViolations)

it('should not have accessibility violations', async () => {
  const { container } = render(<MyComponent />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

See `templates/react/accessibility/shared/example.test.tsx` for comprehensive examples.

### Step 6: Manual Testing (10 minutes per page)

**Keyboard Navigation:**
1. Press Tab repeatedly, verify all interactive elements reachable
2. Verify focus indicators visible
3. Test modal opens/closes with Escape

**Screen Reader (NVDA recommended):**
1. Download NVDA: https://www.nvaccess.org/
2. Navigate page with Tab and Arrow keys
3. Verify headings, labels, and errors announced

**Color Contrast:**
1. Use Chrome DevTools or axe DevTools
2. Verify all text meets 4.5:1 ratio (normal) or 3:1 (large)

See [awareness-guide.md](./awareness-guide.md#testing-workflows) for detailed workflows.

---

## Verification Checklist

Use [ledger.md](./ledger.md) for comprehensive WCAG 2.2 Level AA compliance audit.

**Quick Checks:**
- [ ] All images have `alt` attributes
- [ ] All form inputs have labels
- [ ] Buttons use semantic `<button>` (not `<div onClick>`)
- [ ] Color contrast meets 4.5:1 for text
- [ ] Interactive elements ≥ 24×24px
- [ ] Skip link present and functional
- [ ] All pages have unique `<title>`
- [ ] No autoplaying media
- [ ] Keyboard navigation works everywhere
- [ ] Automated tests (axe) pass with 0 violations

---

## Resources

- **[capability-charter.md](./capability-charter.md)** - Business value, scope, dependencies
- **[protocol-spec.md](./protocol-spec.md)** - Complete technical specification
- **[awareness-guide.md](./awareness-guide.md)** - Common pitfalls, decision trees
- **[ledger.md](./ledger.md)** - WCAG 2.2 compliance checklist
- **[README.md](./README.md)** - Quick reference and links

---

## Support

For questions or issues:
1. Check [awareness-guide.md](./awareness-guide.md) for common pitfalls
2. Review [protocol-spec.md](./protocol-spec.md) for implementation patterns
3. Consult WCAG 2.2 specification: https://www.w3.org/TR/WCAG22/

---

**Version**: 1.0.0
**Last Updated**: 2025-11-02
