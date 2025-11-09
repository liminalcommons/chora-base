/**
 * Accessibility Testing Example
 *
 * This file demonstrates how to write accessibility tests using jest-axe or vitest-axe.
 * Copy patterns from this file into your component tests.
 *
 * Testing Philosophy:
 * - Automated tools catch ~85% of issues (axe-core)
 * - Manual testing catches remaining ~15% (keyboard nav, screen readers)
 * - Run axe tests on ALL components, not just "important" ones
 *
 * See: SAP-026 protocol-spec.md for complete testing guidance
 */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe' // or 'vitest-axe' for Vite

// Extend matchers
expect.extend(toHaveNoViolations)

// Example component to test
function LoginForm() {
  return (
    <form aria-label="Login form">
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        name="email"
        autoComplete="email"
        required
      />

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        name="password"
        autoComplete="current-password"
        required
      />

      <button type="submit">Sign In</button>
    </form>
  )
}

describe('LoginForm Accessibility', () => {
  /**
   * Test 1: Automated axe-core scan
   *
   * This catches ~85% of accessibility issues:
   * - Missing alt text
   * - Missing form labels
   * - Low color contrast
   * - Invalid ARIA usage
   * - Semantic HTML issues
   */
  it('should not have accessibility violations', async () => {
    const { container } = render(<LoginForm />)

    // Run axe on entire component
    const results = await axe(container)

    // Assert no violations
    expect(results).toHaveNoViolations()
  })

  /**
   * Test 2: Form labels association
   *
   * Verify labels are correctly associated with inputs.
   * While axe catches missing labels, this provides explicit documentation.
   */
  it('should have properly associated labels', () => {
    render(<LoginForm />)

    // getByLabelText throws if label not associated
    const emailInput = screen.getByLabelText('Email')
    const passwordInput = screen.getByLabelText('Password')

    expect(emailInput).toHaveAttribute('type', 'email')
    expect(passwordInput).toHaveAttribute('type', 'password')
  })

  /**
   * Test 3: Keyboard navigation
   *
   * Verify form is keyboard accessible.
   * Automated tools DON'T catch tab order issues.
   */
  it('should be keyboard navigable', async () => {
    render(<LoginForm />)

    const emailInput = screen.getByLabelText('Email')
    const passwordInput = screen.getByLabelText('Password')
    const submitButton = screen.getByRole('button', { name: 'Sign In' })

    // Tab should move through inputs in order
    await userEvent.tab()
    expect(emailInput).toHaveFocus()

    await userEvent.tab()
    expect(passwordInput).toHaveFocus()

    await userEvent.tab()
    expect(submitButton).toHaveFocus()
  })

  /**
   * Test 4: Required field indicators
   *
   * Verify required fields are marked both visually and programmatically.
   */
  it('should mark required fields', () => {
    render(<LoginForm />)

    const emailInput = screen.getByLabelText('Email')
    const passwordInput = screen.getByLabelText('Password')

    expect(emailInput).toBeRequired()
    expect(passwordInput).toBeRequired()
  })

  /**
   * Test 5: AutoComplete attributes (WCAG 3.3.7)
   *
   * Verify inputs have autocomplete for password managers.
   * Improves UX and meets WCAG 2.2 Redundant Entry criterion.
   */
  it('should have autocomplete attributes', () => {
    render(<LoginForm />)

    const emailInput = screen.getByLabelText('Email')
    const passwordInput = screen.getByLabelText('Password')

    expect(emailInput).toHaveAttribute('autoComplete', 'email')
    expect(passwordInput).toHaveAttribute('autoComplete', 'current-password')
  })
})

/**
 * Example: Testing Form Validation Errors
 */
function FormWithErrors() {
  const [error, setError] = React.useState<string>()

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        setError('Invalid email address')
      }}
    >
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!error}
        aria-describedby={error ? 'email-error' : undefined}
      />
      {error && (
        <p id="email-error" role="alert">
          {error}
        </p>
      )}
      <button type="submit">Submit</button>
    </form>
  )
}

describe('Form Error Handling', () => {
  it('should announce errors to screen readers', async () => {
    render(<FormWithErrors />)

    const input = screen.getByLabelText('Email')
    const submitButton = screen.getByRole('button')

    // Trigger validation error
    await userEvent.click(submitButton)

    // Verify aria-invalid set
    expect(input).toHaveAttribute('aria-invalid', 'true')

    // Verify error message linked via aria-describedby
    expect(input).toHaveAttribute('aria-describedby', 'email-error')

    // Verify error has role="alert" for screen reader announcement
    const error = screen.getByText('Invalid email address')
    expect(error).toHaveAttribute('role', 'alert')
  })

  it('should not have violations with error state', async () => {
    const { container } = render(<FormWithErrors />)

    // Trigger error
    const submitButton = screen.getByRole('button')
    await userEvent.click(submitButton)

    // Run axe with error visible
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})

/**
 * Example: Testing Button Accessibility
 */
function IconButton({ onClick }: { onClick: () => void }) {
  return (
    <button onClick={onClick} aria-label="Delete item">
      <svg aria-hidden="true" viewBox="0 0 24 24">
        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
      </svg>
    </button>
  )
}

describe('Icon Button Accessibility', () => {
  it('should have accessible name', () => {
    const onClick = jest.fn()
    render(<IconButton onClick={onClick} />)

    // Verify button has accessible name
    const button = screen.getByRole('button', { name: 'Delete item' })
    expect(button).toBeInTheDocument()
  })

  it('should mark icon as decorative', () => {
    const onClick = jest.fn()
    const { container } = render(<IconButton onClick={onClick} />)

    // Verify SVG has aria-hidden="true"
    const svg = container.querySelector('svg')
    expect(svg).toHaveAttribute('aria-hidden', 'true')
  })

  it('should be keyboard accessible', async () => {
    const onClick = jest.fn()
    render(<IconButton onClick={onClick} />)

    const button = screen.getByRole('button')

    // Focus button
    await userEvent.tab()
    expect(button).toHaveFocus()

    // Activate with Enter
    await userEvent.keyboard('{Enter}')
    expect(onClick).toHaveBeenCalledTimes(1)

    // Activate with Space
    await userEvent.keyboard(' ')
    expect(onClick).toHaveBeenCalledTimes(2)
  })
})

/**
 * Example: Testing Modal Accessibility
 */
function SimpleModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  if (!isOpen) return null

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h2 id="modal-title">Confirm Action</h2>
      <p>Are you sure?</p>
      <button onClick={onClose}>Cancel</button>
      <button onClick={onClose}>Confirm</button>
    </div>
  )
}

describe('Modal Accessibility', () => {
  it('should have proper ARIA attributes', () => {
    render(<SimpleModal isOpen={true} onClose={() => {}} />)

    const dialog = screen.getByRole('dialog')
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog).toHaveAttribute('aria-labelledby', 'modal-title')
  })

  it('should have accessible title', () => {
    render(<SimpleModal isOpen={true} onClose={() => {}} />)

    const title = screen.getByText('Confirm Action')
    expect(title).toHaveAttribute('id', 'modal-title')
  })

  it('should not render when closed', () => {
    render(<SimpleModal isOpen={false} onClose={() => {}} />)

    const dialog = screen.queryByRole('dialog')
    expect(dialog).not.toBeInTheDocument()
  })
})

/**
 * Example: Testing Custom axe Configuration
 *
 * Sometimes you need to disable specific rules for valid reasons.
 * Document WHY you're disabling a rule.
 */
import { configureAxe } from 'jest-axe'

describe('Component with Custom axe Config', () => {
  it('should pass with custom rules', async () => {
    const { container } = render(<div>Content without landmarks</div>)

    // Disable "landmark-one-main" for this specific test
    // Reason: Testing isolated component, not full page layout
    const customAxe = configureAxe({
      rules: {
        'landmark-one-main': { enabled: false },
      },
    })

    const results = await customAxe(container)
    expect(results).toHaveNoViolations()
  })
})

/**
 * Best Practices Summary
 *
 * ✅ DO:
 * - Run axe on ALL components (not just "important" ones)
 * - Test both default and error states
 * - Test keyboard navigation explicitly
 * - Test form label associations
 * - Document why you disable axe rules
 *
 * ❌ DON'T:
 * - Rely solely on automated tests (15% needs manual testing)
 * - Disable axe rules without justification
 * - Skip testing error states
 * - Assume semantic HTML = accessible (test it!)
 *
 * Manual Testing Required:
 * - Screen reader testing (NVDA, VoiceOver)
 * - Keyboard navigation flow (logical tab order)
 * - Color contrast edge cases
 * - Zoom to 200% (text scaling)
 * - Zoom to 400% (reflow)
 *
 * See: SAP-026 awareness-guide.md for manual testing workflows
 */
