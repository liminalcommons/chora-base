# SAP-026: React Accessibility Compliance Ledger

**WCAG 2.2 Level AA Compliance Checklist for React Applications**

This ledger provides a comprehensive checklist for verifying WCAG 2.2 Level AA compliance in your React application. Use this as a quality gate before production deployment.

---

## How to Use This Ledger

1. **During Development**: Check items as you implement features
2. **Pre-Launch**: Complete full audit using this checklist
3. **Continuous**: Re-audit after major UI changes
4. **Documentation**: Track compliance status in project docs

**Compliance Levels**:
- ✅ **Compliant**: Meets WCAG 2.2 Level AA
- ⚠️ **Partial**: Some compliance, needs improvement
- ❌ **Non-Compliant**: Does not meet requirements
- N/A **Not Applicable**: Criterion doesn't apply to this project

---

## WCAG 2.2 Level A Criteria (Required for AA)

### Principle 1: Perceivable

#### 1.1 Text Alternatives

- [ ] **1.1.1 Non-text Content (A)**
  - [ ] All images have `alt` attributes
  - [ ] Decorative images use `alt=""`
  - [ ] Functional images describe action (e.g., "Search")
  - [ ] Complex images (charts) have detailed descriptions
  - [ ] Icons in buttons have `aria-label` or visually hidden text
  - **Testing**: Run `axe` or check ESLint `jsx-a11y/alt-text`

#### 1.2 Time-based Media

- [ ] **1.2.1 Audio-only and Video-only (A)**
  - [ ] Audio-only content has transcript
  - [ ] Video-only content has audio description or transcript
  - **Note**: If no audio/video content, mark N/A

- [ ] **1.2.2 Captions (Prerecorded) (A)**
  - [ ] Prerecorded videos have captions (WebVTT format)
  - [ ] Captions synchronized with audio
  - **Implementation**: `<track kind="captions" src="captions.vtt" />`

- [ ] **1.2.3 Audio Description or Media Alternative (A)**
  - [ ] Videos with visual-only information have audio description
  - [ ] Or provide full text transcript
  - **Note**: If no video content, mark N/A

#### 1.3 Adaptable

- [ ] **1.3.1 Info and Relationships (A)**
  - [ ] Semantic HTML used (`<button>`, `<a>`, `<nav>`, `<main>`, `<header>`)
  - [ ] Form labels associated with inputs (`htmlFor`/`id` or `aria-labelledby`)
  - [ ] Headings use `<h1>` through `<h6>` (not styled `<div>`)
  - [ ] Lists use `<ul>`, `<ol>`, `<li>`
  - [ ] Tables use `<th>` for headers with `scope` attribute
  - **Testing**: ESLint `jsx-a11y` rules, manual inspection

- [ ] **1.3.2 Meaningful Sequence (A)**
  - [ ] Tab order is logical (matches visual order)
  - [ ] Reading order makes sense with CSS disabled
  - [ ] No `tabIndex` values > 0 (avoids tab order manipulation)
  - **Testing**: Press Tab repeatedly, verify logical flow

- [ ] **1.3.3 Sensory Characteristics (A)**
  - [ ] Instructions don't rely solely on shape ("click the square button")
  - [ ] Instructions don't rely solely on color ("click the red button")
  - [ ] Instructions don't rely solely on location ("button on the right")
  - [ ] Provide text labels in addition to visual cues
  - **Example**: "Click Submit (blue button on right)"

#### 1.4 Distinguishable

- [ ] **1.4.1 Use of Color (A)**
  - [ ] Information not conveyed by color alone
  - [ ] Links distinguishable by underline or bold (not just color)
  - [ ] Form errors indicated with icons + text (not just red border)
  - **Testing**: Use browser grayscale mode, verify info still clear

- [ ] **1.4.2 Audio Control (A)**
  - [ ] No autoplaying audio > 3 seconds
  - [ ] Autoplaying media has pause/stop button
  - [ ] Volume control independent of system volume
  - **Best Practice**: Never use `autoPlay` on `<audio>` or `<video>`

---

### Principle 2: Operable

#### 2.1 Keyboard Accessible

- [ ] **2.1.1 Keyboard (A)**
  - [ ] All interactive elements accessible via keyboard
  - [ ] Buttons activate with Enter and Space
  - [ ] Links activate with Enter
  - [ ] No keyboard traps (can navigate away with Tab/Shift+Tab)
  - [ ] Custom widgets follow ARIA APG keyboard patterns
  - **Testing**: Unplug mouse, navigate entire app with keyboard

- [ ] **2.1.2 No Keyboard Trap (A)**
  - [ ] Focus can move away from every component
  - [ ] Modals allow Escape key to close (focus trap is intentional)
  - [ ] No infinite loops in tab order
  - **Testing**: Tab through app, verify no stuck focus

- [ ] **2.1.4 Character Key Shortcuts (A)**
  - [ ] Single-key shortcuts (non-modifier) can be turned off
  - [ ] Or remapped to use modifier keys (Ctrl, Alt, Cmd)
  - [ ] Or only active when component has focus
  - **Note**: If no single-key shortcuts, mark N/A

#### 2.2 Enough Time

- [ ] **2.2.1 Timing Adjustable (A)**
  - [ ] User can turn off, adjust, or extend time limits
  - [ ] Or time limit > 20 hours (considered no limit)
  - **Example**: Session timeout warning with "Extend session" button

- [ ] **2.2.2 Pause, Stop, Hide (A)**
  - [ ] Auto-updating content can be paused/stopped
  - [ ] Moving/blinking/scrolling content lasting > 5s can be paused
  - [ ] Auto-updating info (stock tickers) can be paused
  - **Example**: Carousel with pause button

#### 2.3 Seizures and Physical Reactions

- [ ] **2.3.1 Three Flashes or Below Threshold (A)**
  - [ ] No content flashes more than 3 times per second
  - [ ] Or flashes below general and red flash thresholds
  - **Note**: If no animations, mark N/A

#### 2.4 Navigable

- [ ] **2.4.1 Bypass Blocks (A)**
  - [ ] Skip link to main content (visible on focus)
  - [ ] Or ARIA landmarks (`<main>`, `<nav>`, `<aside>`)
  - **Implementation**: `<SkipLink />` component
  - **Testing**: Press Tab from URL bar, skip link appears

- [ ] **2.4.2 Page Titled (A)**
  - [ ] Every page has unique, descriptive `<title>`
  - [ ] Title describes page content/purpose
  - **Next.js**: Use `<title>` in `metadata` export
  - **Vite**: Use `<Helmet>` or `document.title`

- [ ] **2.4.3 Focus Order (A)**
  - [ ] Tab order is logical and meaningful
  - [ ] Matches visual layout (left-to-right, top-to-bottom)
  - [ ] No unexpected focus jumps
  - **Testing**: Tab through page, verify order makes sense

- [ ] **2.4.4 Link Purpose (In Context) (A)**
  - [ ] Link text describes destination/purpose
  - [ ] Avoid generic "click here" or "read more"
  - [ ] Or provide context via `aria-label` or `aria-describedby`
  - **Good**: "Download PDF report (2.5 MB)"
  - **Bad**: "Click here"

#### 2.5 Input Modalities

- [ ] **2.5.1 Pointer Gestures (A)**
  - [ ] Multipoint gestures (pinch zoom) have single-pointer alternative
  - [ ] Path-based gestures (swipe) have single-pointer alternative
  - **Example**: Provide +/- buttons in addition to pinch zoom

- [ ] **2.5.2 Pointer Cancellation (A)**
  - [ ] Click events fire on `mouseup` (not `mousedown`)
  - [ ] User can abort action by moving pointer away before release
  - **React**: Use `onClick` (fires on mouseup), not custom `onMouseDown`

- [ ] **2.5.3 Label in Name (A)**
  - [ ] Accessible name includes visible text label
  - [ ] `aria-label` contains visible label text
  - **Example**: If button shows "Submit", `aria-label="Submit form"` ✅
  - **Bad**: Button shows "Submit", `aria-label="Send"` ❌

- [ ] **2.5.4 Motion Actuation (A)**
  - [ ] Motion-activated features (shake to undo) have UI alternative
  - [ ] Or user can disable motion activation
  - **Note**: If no motion features, mark N/A

- [ ] **2.5.7 Dragging Movements (AA)** ⭐ New in WCAG 2.2
  - [ ] Drag-and-drop has single-pointer alternative
  - [ ] Provide keyboard shortcuts or click-based reordering
  - **Example**: File upload supports both drag-drop and "Browse files" button

- [ ] **2.5.8 Target Size (Minimum) (AA)** ⭐ New in WCAG 2.2
  - [ ] Interactive elements are ≥ 24×24 CSS pixels
  - [ ] Or have 24px spacing from other targets
  - [ ] Inline links exempt (links within sentences)
  - **Implementation**: Use `h-8 w-8` minimum (32px) in Tailwind
  - **Testing**: Inspect element, verify `width` and `height` ≥ 24px

---

### Principle 3: Understandable

#### 3.1 Readable

- [ ] **3.1.1 Language of Page (A)**
  - [ ] `<html lang="en">` attribute set
  - [ ] Language code is valid (ISO 639-1)
  - **Next.js**: Set in `app/layout.tsx`
  - **Vite**: Set in `index.html`

- [ ] **3.1.2 Language of Parts (AA)**
  - [ ] Content in different language has `lang` attribute
  - **Example**: `<p lang="es">Hola, mundo</p>`
  - **Note**: If single language only, mark N/A

#### 3.2 Predictable

- [ ] **3.2.1 On Focus (A)**
  - [ ] Focusing an element doesn't trigger context change
  - [ ] No automatic form submission on focus
  - [ ] No automatic navigation on focus
  - **Bad**: Dropdown opens modal when focused (use onChange instead)

- [ ] **3.2.2 On Input (A)**
  - [ ] Changing input value doesn't trigger unexpected context change
  - [ ] Form doesn't auto-submit when selecting dropdown option
  - [ ] Navigation doesn't happen without user confirmation
  - **Good**: Provide "Go" button for search filters

- [ ] **3.2.6 Consistent Help (A)** ⭐ New in WCAG 2.2
  - [ ] Help mechanisms (contact, FAQ) in consistent location across pages
  - [ ] Same relative order on every page
  - **Example**: "Help" link always in footer, right side
  - **Note**: If no help mechanisms, mark N/A

#### 3.3 Input Assistance

- [ ] **3.3.1 Error Identification (A)**
  - [ ] Form errors identified in text
  - [ ] Error messages describe which field has error
  - [ ] Errors visible and announced to screen readers
  - **Implementation**: `aria-invalid="true"` + `aria-describedby="field-error"`

- [ ] **3.3.2 Labels or Instructions (A)**
  - [ ] All form inputs have labels
  - [ ] Labels describe purpose of input
  - [ ] Required fields indicated (visually + `required` attribute)
  - **Implementation**: `<label htmlFor="email">Email *</label>`

- [ ] **3.3.3 Error Suggestion (AA)**
  - [ ] Error messages suggest how to fix error
  - [ ] Not just "Invalid input" but "Email must include @ symbol"
  - [ ] Provide examples of correct format
  - **Good**: "Password must be at least 8 characters and include a number"

- [ ] **3.3.4 Error Prevention (Legal, Financial, Data) (AA)**
  - [ ] Reversible: User can undo submission
  - [ ] Or Checked: Data is validated before submission
  - [ ] Or Confirmed: User confirms before final submission
  - **Example**: Show confirmation modal before deleting account

- [ ] **3.3.7 Redundant Entry (A)** ⭐ New in WCAG 2.2
  - [ ] Information entered earlier in process is auto-filled
  - [ ] Or available to select from list
  - [ ] Or user can confirm previous entry without re-entering
  - **Implementation**: Use `autoComplete` attribute, session storage
  - **Example**: Billing address = shipping address (checkbox to copy)

- [ ] **3.3.8 Accessible Authentication (Minimum) (AA)** ⭐ New in WCAG 2.2
  - [ ] No cognitive function tests (CAPTCHA, memory games)
  - [ ] Use authentication methods that don't require memorization
  - [ ] Support for password managers (autocomplete="current-password")
  - [ ] Or use passwordless auth (magic links, WebAuthn, OAuth)
  - **Good**: Email magic link, biometric auth, OAuth
  - **Bad**: "Select all images with traffic lights" CAPTCHA

---

### Principle 4: Robust

#### 4.1 Compatible

- [ ] **4.1.2 Name, Role, Value (A)**
  - [ ] All UI components have accessible names
  - [ ] Roles are correct (implicit from semantic HTML or explicit ARIA)
  - [ ] States and properties announced (aria-expanded, aria-checked)
  - **Testing**: ESLint `jsx-a11y` rules, screen reader testing

- [ ] **4.1.3 Status Messages (AA)**
  - [ ] Status messages announced without receiving focus
  - [ ] Use `role="status"`, `role="alert"`, or `aria-live`
  - **Example**: "Item added to cart" message with `role="status"`
  - **Implementation**: Toast notifications with `aria-live="polite"`

---

## WCAG 2.2 Level AA Criteria (Additional Requirements)

### Principle 1: Perceivable (AA)

#### 1.2 Time-based Media (AA)

- [ ] **1.2.4 Captions (Live) (AA)**
  - [ ] Live video (webinars, streams) has live captions
  - **Note**: If no live video, mark N/A

- [ ] **1.2.5 Audio Description (Prerecorded) (AA)**
  - [ ] Prerecorded videos have audio descriptions
  - **Note**: If no video content, mark N/A

#### 1.3 Adaptable (AA)

- [ ] **1.3.4 Orientation (AA)**
  - [ ] Content works in both portrait and landscape
  - [ ] No orientation lock (unless essential, e.g., piano app)
  - **Testing**: Rotate device/browser, verify layout adapts

- [ ] **1.3.5 Identify Input Purpose (AA)**
  - [ ] Common input fields have `autoComplete` attribute
  - [ ] Email: `autoComplete="email"`
  - [ ] Name: `autoComplete="name"`
  - [ ] Phone: `autoComplete="tel"`
  - **See**: https://www.w3.org/TR/WCAG21/#input-purposes

#### 1.4 Distinguishable (AA)

- [ ] **1.4.3 Contrast (Minimum) (AA)**
  - [ ] Normal text: ≥ 4.5:1 contrast ratio
  - [ ] Large text (18pt or 14pt bold): ≥ 3:1 contrast ratio
  - [ ] UI components (buttons, icons): ≥ 3:1 contrast
  - **Testing**: Chrome DevTools, axe DevTools, WebAIM Contrast Checker

- [ ] **1.4.4 Resize Text (AA)**
  - [ ] Text can be resized up to 200% without loss of content
  - [ ] No horizontal scrolling at 200% zoom
  - [ ] Use relative units (`rem`, `em`, `%`), not fixed pixels
  - **Testing**: Browser zoom to 200%, verify layout adapts

- [ ] **1.4.5 Images of Text (AA)**
  - [ ] Use real text instead of images of text
  - [ ] Exception: Logos, essential images (screenshots)
  - **Good**: CSS for styled text, web fonts
  - **Bad**: Image with text content (not selectable, doesn't scale)

- [ ] **1.4.10 Reflow (AA)**
  - [ ] Content reflows to single column at 320px width
  - [ ] No horizontal scrolling at 400% zoom
  - [ ] Exception: Tables, maps, diagrams
  - **Testing**: Browser zoom to 400%, verify no horizontal scroll

- [ ] **1.4.11 Non-text Contrast (AA)**
  - [ ] UI components: ≥ 3:1 contrast against adjacent colors
  - [ ] Graphical objects: ≥ 3:1 contrast
  - **Example**: Button border 3:1 contrast with background
  - **Testing**: Use contrast checker on button borders, icons

- [ ] **1.4.12 Text Spacing (AA)**
  - [ ] No loss of content/functionality when user adjusts text spacing:
    - Line height: 1.5× font size
    - Paragraph spacing: 2× font size
    - Letter spacing: 0.12× font size
    - Word spacing: 0.16× font size
  - **Testing**: Use browser extension to increase spacing, verify no content cutoff

- [ ] **1.4.13 Content on Hover or Focus (AA)**
  - [ ] Tooltips/popovers can be dismissed (Escape key)
  - [ ] User can hover over tooltip content without it disappearing
  - [ ] Tooltip remains visible until user dismisses or removes hover/focus
  - **Implementation**: Add 300ms delay before hide, allow hovering tooltip

---

### Principle 2: Operable (AA)

#### 2.4 Navigable (AA)

- [ ] **2.4.5 Multiple Ways (AA)**
  - [ ] At least 2 ways to find pages (menu navigation + search)
  - [ ] Or menu navigation + sitemap
  - **Example**: Header nav + footer sitemap

- [ ] **2.4.6 Headings and Labels (AA)**
  - [ ] Headings describe topic/purpose
  - [ ] Labels describe purpose of inputs
  - [ ] Headings and labels are clear and concise
  - **Testing**: Read headings in isolation, verify they make sense

- [ ] **2.4.7 Focus Visible (AA)**
  - [ ] Keyboard focus indicators always visible
  - [ ] Focus indicators meet 3:1 contrast ratio
  - [ ] Use `:focus-visible` to show focus only for keyboard users
  - **Implementation**: Tailwind `focus-visible:ring-2 focus-visible:ring-blue-500`
  - **Testing**: Tab through page, verify all focus indicators visible

- [ ] **2.4.11 Focus Not Obscured (Minimum) (AA)** ⭐ New in WCAG 2.2
  - [ ] Focused element not fully hidden by other content
  - [ ] Fixed headers/footers don't cover focused element
  - **Implementation**: Use `scroll-margin-top` for sticky headers
  - **Testing**: Tab through page with sticky header, verify focus visible

---

## Automated Testing Compliance

- [ ] **ESLint jsx-a11y Plugin**
  - [ ] All recommended rules enabled
  - [ ] No eslint-disable comments without justification
  - [ ] CI/CD blocks builds with accessibility violations

- [ ] **jest-axe / vitest-axe**
  - [ ] All components have axe tests
  - [ ] Tests pass with 0 violations
  - [ ] Tests run in CI/CD pipeline

- [ ] **Lighthouse Accessibility Audits**
  - [ ] Lighthouse score ≥ 90 (good)
  - [ ] All manual checks documented
  - [ ] Run on every PR (Lighthouse CI)

---

## Manual Testing Compliance

- [ ] **Keyboard Navigation**
  - [ ] Full site navigable with keyboard only (no mouse)
  - [ ] All interactive elements reachable via Tab
  - [ ] Tab order is logical
  - [ ] Focus indicators visible at all times
  - [ ] Modals trap focus and close with Escape
  - [ ] Dropdowns navigate with Arrow keys

- [ ] **Screen Reader Testing (NVDA/VoiceOver)**
  - [ ] Page structure makes sense (headings, landmarks)
  - [ ] All images have alt text (or aria-label)
  - [ ] Form labels announced correctly
  - [ ] Error messages announced
  - [ ] Status messages announced (aria-live)
  - [ ] Interactive elements have clear names

- [ ] **Color Contrast**
  - [ ] All text meets 4.5:1 ratio (normal) or 3:1 (large)
  - [ ] UI components meet 3:1 ratio
  - [ ] Focus indicators meet 3:1 ratio
  - [ ] Tested with Chrome DevTools or axe DevTools

- [ ] **Zoom/Responsive Testing**
  - [ ] Content works at 200% text zoom
  - [ ] Content reflows at 400% browser zoom
  - [ ] No horizontal scrolling at 400% zoom
  - [ ] Touch targets ≥ 24×24px on mobile

---

## Documentation Compliance

- [ ] **Accessibility Statement**
  - [ ] Public accessibility statement on website
  - [ ] Lists conformance level (WCAG 2.2 Level AA)
  - [ ] Contact method for reporting issues
  - [ ] Last reviewed date

- [ ] **Known Issues**
  - [ ] Document any known violations
  - [ ] Provide timeline for remediation
  - [ ] Explain workarounds if available

---

## Compliance Summary

**Total Criteria**: 50 (Level A) + 20 (Level AA) = 70 WCAG 2.2 Level AA criteria

**Status**:
- ✅ Compliant: ___ / 70
- ⚠️ Partial: ___ / 70
- ❌ Non-Compliant: ___ / 70
- N/A: ___ / 70

**Overall Compliance**: ___%

**Certification Date**: ___________

**Next Audit Date**: ___________

---

## Additional Resources

- **WCAG 2.2 Specification**: https://www.w3.org/TR/WCAG22/
- **Understanding WCAG 2.2**: https://www.w3.org/WAI/WCAG22/Understanding/
- **How to Meet WCAG (Quick Reference)**: https://www.w3.org/WAI/WCAG22/quickref/
- **WebAIM WCAG 2 Checklist**: https://webaim.org/standards/wcag/checklist

---

**Version**: 1.0.0
**Last Updated**: 2025-11-02
**Next Review**: 2026-02-02
