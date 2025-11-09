# SAP-026: React Accessibility Awareness Guide

**Common Pitfalls, Decision Trees, and Best Practices for WCAG 2.2 Level AA Compliance**

This guide complements [protocol-spec.md](./protocol-spec.md) by providing practical guidance on avoiding common accessibility mistakes and making the right implementation choices.

---

## Table of Contents

1. [Common Pitfalls](#common-pitfalls)
2. [Decision Trees](#decision-trees)
3. [WCAG 2.2 Quick Reference](#wcag-22-quick-reference)
4. [Testing Workflows](#testing-workflows)
5. [Component Library Selection](#component-library-selection)

---

## Common Pitfalls

### 1. Using `<div onClick>` Instead of `<button>`

**Problem**: Non-semantic elements with click handlers are not keyboard accessible and confuse screen readers.

```tsx
// ❌ BAD: Not keyboard accessible
<div onClick={handleClick} className="button">
  Click me
</div>

// ❌ ALSO BAD: Still requires manual keyboard handling
<div onClick={handleClick} onKeyDown={handleKeyDown} role="button">
  Click me
</div>

// ✅ GOOD: Use semantic <button>
<button onClick={handleClick} className="button">
  Click me
</button>
```

**Why**: `<button>` provides:
- Built-in keyboard support (Enter and Space keys)
- Correct role announcement to screen readers
- Focus management
- Disabled state handling

**ESLint Rule**: `jsx-a11y/no-static-element-interactions`, `jsx-a11y/click-events-have-key-events`

---

### 2. Missing Alt Text on Images

**Problem**: Images without `alt` attributes are invisible to screen readers.

```tsx
// ❌ BAD: No alt text
<img src="/logo.png" />

// ❌ ALSO BAD: Generic alt text
<img src="/hero.jpg" alt="image" />

// ✅ GOOD: Descriptive alt text
<img src="/hero.jpg" alt="Team collaborating on project in modern office" />

// ✅ GOOD: Decorative images use empty alt
<img src="/decorative-border.png" alt="" />
```

**Decision Tree**:
- **Informative image** (conveys meaning): Use descriptive alt text
- **Functional image** (button/link): Describe action (e.g., "Search" not "Magnifying glass icon")
- **Decorative image** (visual design only): Use `alt=""`
- **Complex image** (chart/diagram): Use `alt` for summary + detailed description nearby

**ESLint Rule**: `jsx-a11y/alt-text`

---

### 3. Form Inputs Without Labels

**Problem**: Screen readers can't identify form fields without associated labels.

```tsx
// ❌ BAD: No label
<input type="email" placeholder="Enter email" />

// ❌ ALSO BAD: Label not associated with input
<label>Email</label>
<input type="email" />

// ✅ GOOD: Label with htmlFor/id association
<label htmlFor="email">Email</label>
<input id="email" type="email" name="email" />

// ✅ ALSO GOOD: Wrapping label
<label>
  Email
  <input type="email" name="email" />
</label>

// ✅ GOOD: aria-label when visible label not possible
<input type="search" aria-label="Search products" />
```

**WCAG Criteria**: 1.3.1 Info and Relationships, 3.3.2 Labels or Instructions

**ESLint Rule**: `jsx-a11y/label-has-associated-control`

---

### 4. Missing Error Messages on Invalid Fields

**Problem**: Screen readers don't announce validation errors without proper ARIA attributes.

```tsx
// ❌ BAD: Error not associated with input
<input type="email" className="error" />
<p className="error-text">Invalid email</p>

// ✅ GOOD: aria-describedby links error to input
<input
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<p id="email-error" role="alert">
  Invalid email address
</p>
```

**Key Attributes**:
- `aria-invalid="true"` marks field as invalid
- `aria-describedby="error-id"` links error message to input
- `role="alert"` announces error to screen readers immediately

**WCAG Criteria**: 3.3.1 Error Identification, 3.3.3 Error Suggestion

**ESLint Rule**: `jsx-a11y/aria-proptypes`

---

### 5. Icon-Only Buttons Without Accessible Names

**Problem**: Icon buttons without text labels are meaningless to screen readers.

```tsx
// ❌ BAD: Icon with no accessible name
<button onClick={handleDelete}>
  <TrashIcon />
</button>

// ❌ ALSO BAD: aria-label on SVG (wrong element)
<button onClick={handleDelete}>
  <TrashIcon aria-label="Delete" />
</button>

// ✅ GOOD: aria-label on button
<button onClick={handleDelete} aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>

// ✅ ALSO GOOD: Visually hidden text
<button onClick={handleDelete}>
  <TrashIcon aria-hidden="true" />
  <span className="sr-only">Delete item</span>
</button>
```

**Best Practice**: Mark icons as `aria-hidden="true"` and provide accessible name on button.

**ESLint Rule**: `jsx-a11y/control-has-associated-label`

---

### 6. Low Color Contrast

**Problem**: Text with insufficient contrast is hard to read for users with low vision.

```tsx
// ❌ BAD: 2.5:1 contrast ratio (fails WCAG AA)
<p className="text-gray-400">This text is too light</p>

// ✅ GOOD: 4.5:1+ contrast ratio (WCAG AA compliant)
<p className="text-gray-700">This text meets contrast requirements</p>
```

**WCAG Requirements** (WCAG 1.4.3):
- **Normal text** (< 18pt): 4.5:1 contrast ratio
- **Large text** (≥ 18pt or 14pt bold): 3:1 contrast ratio
- **UI components** (buttons, icons): 3:1 contrast ratio

**Testing Tools**:
- Chrome DevTools: Inspect element → Contrast ratio
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- axe DevTools browser extension

---

### 7. Modals Without Focus Trap

**Problem**: Keyboard users can tab outside modal to background content.

```tsx
// ❌ BAD: No focus trap
function BadModal({ isOpen, onClose, children }) {
  return isOpen ? (
    <div className="modal">
      <button onClick={onClose}>Close</button>
      {children}
    </div>
  ) : null
}

// ✅ GOOD: Use react-focus-lock
import FocusLock from 'react-focus-lock'

function GoodModal({ isOpen, onClose, children }) {
  return isOpen ? (
    <FocusLock returnFocus>
      <div role="dialog" aria-modal="true">
        <button onClick={onClose}>Close</button>
        {children}
      </div>
    </FocusLock>
  ) : null
}
```

**Requirements**:
- Tab key cycles within modal (focus trap)
- Escape key closes modal
- Focus returns to trigger element on close
- `aria-modal="true"` on dialog

**See**: [accessible-modal.tsx](../../templates/react/accessibility/shared/components/accessible-modal.tsx)

---

### 8. Missing Skip Links

**Problem**: Keyboard users must tab through entire navigation to reach main content.

```tsx
// ❌ BAD: No skip link
export default function Layout({ children }) {
  return (
    <html>
      <body>
        <nav>{/* 20+ navigation links */}</nav>
        <main>{children}</main>
      </body>
    </html>
  )
}

// ✅ GOOD: Skip link allows bypassing navigation
import { SkipLink } from '@/components/skip-link'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        <SkipLink />
        <nav>{/* 20+ navigation links */}</nav>
        <main id="main-content" tabIndex={-1}>
          {children}
        </main>
      </body>
    </html>
  )
}
```

**WCAG Criteria**: 2.4.1 Bypass Blocks (Level A)

**See**: [skip-link.tsx](../../templates/react/accessibility/shared/components/skip-link.tsx)

---

### 9. Tiny Click Targets (<24×24px)

**Problem**: Small buttons/links are hard to click, especially on mobile.

```tsx
// ❌ BAD: 16×16px button (too small)
<button className="h-4 w-4 p-0">×</button>

// ✅ GOOD: 32×32px minimum (meets WCAG 2.5.8)
<button className="h-8 w-8 flex items-center justify-center">×</button>

// ✅ BETTER: 40×40px (comfortable)
<button className="h-10 w-10 flex items-center justify-center">×</button>
```

**WCAG 2.5.8 Target Size (Minimum)**: All interactive elements must be at least **24×24 CSS pixels**.

**Exceptions**:
- Inline links within sentences (exempt)
- Essential controls (e.g., map pins where size conveys meaning)
- Controls with sufficient spacing (24px between targets)

---

### 10. Autoplaying Media Without Controls

**Problem**: Autoplaying audio/video distracts screen reader users and violates WCAG.

```tsx
// ❌ BAD: Autoplay without user control
<video src="/promo.mp4" autoPlay loop />

// ✅ GOOD: User-initiated playback
<video src="/promo.mp4" controls>
  <track kind="captions" src="/captions.vtt" srcLang="en" label="English" />
</video>
```

**WCAG 1.4.2 Audio Control**: If audio plays automatically for more than 3 seconds, provide:
- Pause/stop mechanism
- Volume control independent of system volume

**Best Practice**: Never use `autoPlay` on videos/audio. Always provide `controls`.

---

## Decision Trees

### When to Use Semantic HTML vs ARIA

```
Is there a native HTML element that does what you need?
├─ YES → Use semantic HTML (e.g., <button>, <a>, <input>)
└─ NO → Is this a standard widget pattern (tabs, modal, dropdown)?
    ├─ YES → Use ARIA pattern from APG (https://www.w3.org/WAI/ARIA/apg/)
    └─ NO → Create custom widget with ARIA
```

**Examples**:
- **Button**: Use `<button>`, not `<div role="button">`
- **Link**: Use `<a href>`, not `<span onClick>`
- **Modal**: Use `<div role="dialog" aria-modal="true">` (no native element)
- **Tabs**: Use ARIA pattern (no native HTML equivalent)

**First Rule of ARIA**: If you can use a native HTML element, use it. ARIA is for filling gaps.

---

### Image Alt Text Decision Tree

```
Is the image informative (conveys meaning)?
├─ YES → Is it simple (can be described in <150 characters)?
│   ├─ YES → Use alt="descriptive text"
│   └─ NO → Use alt="summary" + detailed description nearby
└─ NO → Is it decorative (visual design only)?
    ├─ YES → Use alt="" (empty string)
    └─ NO → Is it a functional image (button/link)?
        └─ YES → Describe action (e.g., alt="Search")
```

**Examples**:
- Product photo: `alt="Blue cotton t-shirt with crew neck"`
- Company logo: `alt="Acme Corp"` (if functional) or `alt=""` (if decorative)
- Search icon: `alt="Search"` (or use aria-label on button)
- Decorative border: `alt=""`

---

### Form Validation Error Handling

```
Does the field have validation errors?
├─ YES → Are errors visible on screen?
│   ├─ YES → Link errors with aria-describedby + aria-invalid="true"
│   │       → Use role="alert" or aria-live="assertive" for announcements
│   └─ NO → Make errors visible AND link with aria-describedby
└─ NO → Ensure required fields have required attribute
        → Provide clear labels (not just placeholders)
```

**Best Practice Pattern**:
```tsx
<input
  type="email"
  id="email"
  required
  aria-invalid={hasError}
  aria-describedby={hasError ? "email-error" : undefined}
/>
{hasError && (
  <p id="email-error" role="alert">
    Please enter a valid email address
  </p>
)}
```

---

### Keyboard Navigation Pattern Selection

```
What type of component?
├─ Single interactive element → Use <button> or <a> (built-in keyboard support)
├─ List of items → Use standard Tab order (all items tabbable)
├─ Toolbar/menu → Use roving tabindex (Arrow keys navigate, one item in Tab order)
├─ Modal/dialog → Use focus trap (Tab cycles within modal)
└─ Complex widget → Follow ARIA APG patterns
```

**Roving Tabindex** (for toolbars, tabs, radio groups):
- Only one element has `tabIndex={0}` (in Tab order)
- All others have `tabIndex={-1}` (not in Tab order)
- Arrow keys move focus and update tabindex

**See**: [accessible-tabs.tsx](../../templates/react/accessibility/shared/components/accessible-tabs.tsx)

---

## WCAG 2.2 Quick Reference

### New Criteria (9 criteria added in WCAG 2.2)

| Criterion | Level | Requirement | React Implementation |
|-----------|-------|-------------|---------------------|
| **2.4.11 Focus Not Obscured (Minimum)** | AA | Focused element not fully hidden by other content | Avoid fixed headers obscuring focus, use `z-index`, `scroll-margin-top` |
| **2.4.12 Focus Not Obscured (Enhanced)** | AAA | Focused element fully visible | Out of scope (Level AAA) |
| **2.4.13 Focus Appearance** | AAA | High-contrast focus indicators | Out of scope (Level AAA) |
| **2.5.7 Dragging Movements** | AA | Provide alternative to drag-and-drop | Add keyboard shortcuts, click-based alternatives |
| **2.5.8 Target Size (Minimum)** | AA | Interactive elements ≥ 24×24px | Use `h-8 w-8` (32px) minimum in Tailwind |
| **3.2.6 Consistent Help** | A | Help links in same order across pages | Place help link in consistent location (e.g., footer) |
| **3.3.7 Redundant Entry** | A | Don't ask for same info twice | Use `autoComplete` attributes, session storage |
| **3.3.8 Accessible Authentication (Minimum)** | AA | No cognitive tests (CAPTCHA, memory) | Use WebAuthn, magic links, not CAPTCHAs |
| **3.3.9 Accessible Authentication (Enhanced)** | AAA | No authentication barriers | Out of scope (Level AAA) |

---

### Core Criteria (Must-Know for React Developers)

| Criterion | Level | Requirement | React Implementation |
|-----------|-------|-------------|---------------------|
| **1.1.1 Non-text Content** | A | Alt text for images | `<img alt="description" />` |
| **1.3.1 Info and Relationships** | A | Semantic markup | Use `<button>`, `<a>`, `<label>`, not `<div>` |
| **1.4.3 Contrast (Minimum)** | AA | 4.5:1 text contrast | Use Tailwind `text-gray-700` or darker |
| **2.1.1 Keyboard** | A | All functionality via keyboard | Use semantic HTML (`<button>`, `<a>`) |
| **2.4.1 Bypass Blocks** | A | Skip navigation links | `<SkipLink />` component |
| **2.4.7 Focus Visible** | AA | Visible focus indicators | Use `focus-visible:ring-2` in Tailwind |
| **3.3.1 Error Identification** | A | Errors clearly identified | `aria-invalid="true"` + `aria-describedby` |
| **3.3.2 Labels or Instructions** | A | Form fields have labels | `<label htmlFor>` or `aria-label` |
| **4.1.2 Name, Role, Value** | A | Accessible names for controls | `aria-label`, `aria-labelledby` |

**Full List**: See [protocol-spec.md](./protocol-spec.md#wcag-22-compliance-matrix)

---

## Testing Workflows

### Keyboard Navigation Testing (5 minutes)

**Goal**: Verify all interactive elements are keyboard accessible.

1. **Load page** in browser
2. **Press Tab** repeatedly:
   - ✅ Focus moves to all interactive elements (buttons, links, inputs)
   - ✅ Focus indicators clearly visible
   - ✅ Tab order is logical (left-to-right, top-to-bottom)
   - ❌ Focus jumps unexpectedly
   - ❌ Elements not reachable by keyboard

3. **Test interactive elements**:
   - ✅ Buttons activate with Enter and Space
   - ✅ Links activate with Enter
   - ✅ Modals close with Escape
   - ✅ Dropdowns open/navigate with Arrow keys

4. **Test forms**:
   - ✅ Tab moves between fields in logical order
   - ✅ Radio buttons navigate with Arrow keys
   - ✅ Checkboxes toggle with Space
   - ✅ Submit button activates with Enter

**Common Issues**:
- `<div onClick>` instead of `<button>` (not keyboard accessible)
- Missing `tabIndex={-1}` on modal container (background elements focusable)
- Focus indicators removed with `outline: none` (invisible focus)

---

### Screen Reader Testing (10 minutes)

**Recommended Tool**: NVDA (Windows, free) or VoiceOver (macOS, built-in)

**NVDA Installation**:
1. Download from [nvaccess.org](https://www.nvaccess.org/)
2. Install and run NVDA
3. Navigate with:
   - **Tab**: Move to next interactive element
   - **Down Arrow**: Read next item
   - **H**: Jump to next heading
   - **B**: Jump to next button
   - **K**: Jump to next link

**Testing Checklist**:
- ✅ Page title announced on load
- ✅ Headings announced with level (e.g., "Heading level 1, Welcome")
- ✅ Buttons announced with role (e.g., "Save, button")
- ✅ Links announced with role (e.g., "Learn more, link")
- ✅ Form labels announced (e.g., "Email, edit, required")
- ✅ Error messages announced (e.g., "Alert, Invalid email")
- ✅ Images have alt text (decorative images skipped)

**Common Issues**:
- Missing alt text on images (silence or "image" announced)
- No labels on form inputs (field purpose unclear)
- Generic link text ("click here" instead of "Download report")
- Error messages not linked to inputs (no announcement)

---

### Color Contrast Testing (2 minutes)

**Tools**:
- **Chrome DevTools**: Inspect element → Check contrast ratio
- **axe DevTools**: Browser extension, automated contrast checking
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/

**Process**:
1. Right-click text element → Inspect
2. Check contrast ratio in DevTools (shows ratio like "4.52" with AA/AAA badges)
3. ✅ Normal text: ≥ 4.5:1
4. ✅ Large text (18pt+): ≥ 3:1
5. ✅ UI components: ≥ 3:1

**Common Issues**:
- Light gray text on white background (2-3:1, fails AA)
- Placeholder text too light (often 2.5:1, fails AA)
- Disabled button text too light (aim for 3:1 even when disabled)

---

### Automated Testing with axe-core (Continuous)

**Jest/Vitest Setup**:
```typescript
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('should not have accessibility violations', async () => {
  const { container } = render(<MyComponent />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

**What Automated Tools Catch** (~85%):
- ✅ Missing alt text
- ✅ Missing form labels
- ✅ Low color contrast
- ✅ Missing ARIA attributes
- ✅ Invalid ARIA usage
- ✅ Missing document language

**What Automated Tools Miss** (~15%):
- ❌ Logical keyboard tab order
- ❌ Meaningful alt text (tools only detect presence, not quality)
- ❌ Screen reader experience (aria-live announcements)
- ❌ Focus trap functionality
- ❌ Context-specific link text ("click here" vs "Download PDF report")

**Best Practice**: Use automated tests (85% coverage) + manual testing (15% coverage) = 100% confidence.

---

## Component Library Selection

### When to Use Radix UI

**Use Radix UI if**:
- ✅ You need pre-built accessible primitives (Modal, Dropdown, Tabs)
- ✅ You want full styling control (unstyled components)
- ✅ You use Tailwind CSS or custom CSS
- ✅ You need React 18+ features (Suspense, Server Components)

**Pros**:
- Accessibility built-in (keyboard, ARIA, focus management)
- Unstyled (no CSS to override)
- TypeScript support
- Tree-shakeable (small bundle size)

**Cons**:
- Requires manual styling (more setup than Material UI)
- Learning curve (composition API)

**Example**:
```tsx
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Edit Profile</Dialog.Title>
      <Dialog.Close>×</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

---

### When to Use React Aria (Adobe)

**Use React Aria if**:
- ✅ You prefer hooks over components
- ✅ You need maximum flexibility (full control over DOM structure)
- ✅ You're building a design system from scratch
- ✅ You need advanced interactions (drag-and-drop, virtualization)

**Pros**:
- Hooks-based (compose behaviors)
- Extremely flexible
- Excellent internationalization support
- Battle-tested (powers Adobe Spectrum)

**Cons**:
- More boilerplate than Radix UI
- Steeper learning curve

**Example**:
```tsx
import { useButton } from '@react-aria/button'

function Button(props) {
  const ref = useRef()
  const { buttonProps } = useButton(props, ref)
  return <button {...buttonProps} ref={ref}>{props.children}</button>
}
```

---

### When to Use Headless UI

**Use Headless UI if**:
- ✅ You use Tailwind CSS (official Tailwind Labs library)
- ✅ You want simpler API than Radix UI
- ✅ You need common components only (Modal, Dropdown, Tabs, etc.)

**Pros**:
- Simple API
- Tailwind CSS integration (official)
- Good documentation

**Cons**:
- Fewer components than Radix UI
- Less flexible than React Aria

**Example**:
```tsx
import { Dialog } from '@headlessui/react'

<Dialog open={isOpen} onClose={() => setIsOpen(false)}>
  <Dialog.Panel>
    <Dialog.Title>Edit Profile</Dialog.Title>
    <Dialog.Description>Update your information</Dialog.Description>
  </Dialog.Panel>
</Dialog>
```

---

### Decision Matrix

| Feature | Radix UI | React Aria | Headless UI | Custom |
|---------|----------|------------|-------------|--------|
| **Accessibility** | ⭐⭐⭐⭐⭐ Built-in | ⭐⭐⭐⭐⭐ Built-in | ⭐⭐⭐⭐⭐ Built-in | ⭐⭐ Manual |
| **Styling** | ⭐⭐⭐⭐⭐ Unstyled | ⭐⭐⭐⭐⭐ Unstyled | ⭐⭐⭐⭐ Unstyled | ⭐⭐⭐⭐⭐ Full control |
| **API Simplicity** | ⭐⭐⭐⭐ Component API | ⭐⭐⭐ Hooks API | ⭐⭐⭐⭐⭐ Simple API | ⭐⭐ Complex |
| **Flexibility** | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Maximum | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Maximum |
| **Bundle Size** | ⭐⭐⭐⭐ Small | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Small | ⭐⭐⭐⭐⭐ Minimal |
| **Learning Curve** | ⭐⭐⭐⭐ Easy | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Very Easy | ⭐ Difficult |

**Recommendation**:
- **Default choice**: Radix UI (best balance of DX and flexibility)
- **Maximum control**: React Aria (hooks-based, compose behaviors)
- **Tailwind projects**: Headless UI (official Tailwind integration)
- **Simple components**: Use custom templates from SAP-026 (no library dependency)

---

## Additional Resources

- **WCAG 2.2 Specification**: https://www.w3.org/TR/WCAG22/
- **ARIA Authoring Practices Guide**: https://www.w3.org/WAI/ARIA/apg/
- **React Accessibility Docs**: https://react.dev/learn/accessibility
- **axe DevTools**: https://www.deque.com/axe/devtools/
- **NVDA Screen Reader**: https://www.nvaccess.org/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/

---

**Version**: 1.0.0
**Last Updated**: 2025-11-02
**Next Review**: 2026-02-02
