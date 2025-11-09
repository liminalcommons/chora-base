/**
 * Accessible Button Component
 *
 * WCAG 2.2 Level AA compliant button with:
 * - Semantic <button> element (keyboard support built-in)
 * - Loading state with aria-busy and disabled
 * - Icon-only buttons with aria-label
 * - Minimum 24×24px target size (WCAG 2.5.8)
 * - Clear focus indicators (3:1 contrast)
 * - Disabled state properly announced
 *
 * Based on WCAG 2.2 criteria:
 * - 2.1.1 Keyboard (built-in with <button>)
 * - 2.4.7 Focus Visible
 * - 2.5.8 Target Size (Minimum) - 24×24px
 * - 4.1.2 Name, Role, Value
 *
 * Usage:
 * ```tsx
 * <AccessibleButton onClick={handleClick} variant="primary">
 *   Click Me
 * </AccessibleButton>
 *
 * <AccessibleButton
 *   onClick={handleSave}
 *   isLoading={saving}
 *   loadingText="Saving..."
 * >
 *   Save
 * </AccessibleButton>
 *
 * <AccessibleButton
 *   onClick={handleDelete}
 *   icon={<TrashIcon />}
 *   aria-label="Delete item"
 * />
 * ```
 */

import { type ButtonHTMLAttributes, type ReactNode } from 'react'

interface AccessibleButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button content */
  children?: ReactNode
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  /** Button size (all meet 24×24px minimum) */
  size?: 'sm' | 'md' | 'lg'
  /** Loading state (disables button, shows loading text) */
  isLoading?: boolean
  /** Loading text (overrides children when loading) */
  loadingText?: string
  /** Icon-only button (requires aria-label) */
  icon?: ReactNode
  /** Icon position (when used with text) */
  iconPosition?: 'left' | 'right'
  /** Full width button */
  fullWidth?: boolean
}

export function AccessibleButton({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  loadingText,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  disabled,
  className = '',
  type = 'button',
  ...props
}: AccessibleButtonProps) {
  const isIconOnly = icon && !children

  // Icon-only buttons MUST have aria-label
  if (isIconOnly && !props['aria-label']) {
    console.warn('Icon-only buttons require aria-label for accessibility')
  }

  // Base styles (all sizes meet WCAG 2.5.8 24×24px minimum)
  const baseStyles = 'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60'

  // Variant styles
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus-visible:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500',
  }

  // Size styles (all meet 24×24px minimum target size)
  const sizeStyles = {
    sm: isIconOnly ? 'h-8 w-8' : 'h-8 px-3 text-sm',      // 32×32px
    md: isIconOnly ? 'h-10 w-10' : 'h-10 px-4 text-base', // 40×40px
    lg: isIconOnly ? 'h-12 w-12' : 'h-12 px-6 text-lg',   // 48×48px
  }

  const widthStyle = fullWidth ? 'w-full' : ''

  const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${widthStyle} ${className}`

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      aria-busy={isLoading || undefined}
      className={combinedClassName}
      {...props}
    >
      {/* Loading spinner */}
      {isLoading && (
        <svg
          className="h-4 w-4 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}

      {/* Icon (left position) */}
      {!isLoading && icon && iconPosition === 'left' && (
        <span aria-hidden="true">{icon}</span>
      )}

      {/* Button text */}
      {!isIconOnly && (
        <span>{isLoading && loadingText ? loadingText : children}</span>
      )}

      {/* Icon (right position or icon-only) */}
      {!isLoading && icon && (iconPosition === 'right' || isIconOnly) && (
        <span aria-hidden="true">{icon}</span>
      )}
    </button>
  )
}

/**
 * Example: Icon-only Button
 *
 * ```tsx
 * function TrashIcon() {
 *   return (
 *     <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
 *       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
 *     </svg>
 *   )
 * }
 *
 * <AccessibleButton
 *   icon={<TrashIcon />}
 *   aria-label="Delete item"
 *   onClick={handleDelete}
 * />
 * ```
 */

/**
 * Example: Button with Icon and Text
 *
 * ```tsx
 * <AccessibleButton
 *   icon={<DownloadIcon />}
 *   iconPosition="left"
 *   onClick={handleDownload}
 * >
 *   Download
 * </AccessibleButton>
 *
 * <AccessibleButton
 *   icon={<ArrowRightIcon />}
 *   iconPosition="right"
 *   variant="secondary"
 * >
 *   Next
 * </AccessibleButton>
 * ```
 */

/**
 * Example: Loading State
 *
 * ```tsx
 * function SaveButton() {
 *   const [saving, setSaving] = useState(false)
 *
 *   const handleSave = async () => {
 *     setSaving(true)
 *     try {
 *       await saveData()
 *     } finally {
 *       setSaving(false)
 *     }
 *   }
 *
 *   return (
 *     <AccessibleButton
 *       onClick={handleSave}
 *       isLoading={saving}
 *       loadingText="Saving..."
 *     >
 *       Save Changes
 *     </AccessibleButton>
 *   )
 * }
 * ```
 */

/**
 * Common Pitfalls (AVOID)
 *
 * ❌ DON'T: Use <div onClick> instead of <button>
 * ```tsx
 * <div onClick={handleClick}>Click me</div> // No keyboard support!
 * ```
 *
 * ✅ DO: Use semantic <button>
 * ```tsx
 * <AccessibleButton onClick={handleClick}>Click me</AccessibleButton>
 * ```
 *
 * ❌ DON'T: Icon button without aria-label
 * ```tsx
 * <button><TrashIcon /></button> // Screen readers can't identify purpose
 * ```
 *
 * ✅ DO: Provide aria-label for icon-only buttons
 * ```tsx
 * <AccessibleButton icon={<TrashIcon />} aria-label="Delete item" />
 * ```
 *
 * ❌ DON'T: Tiny click targets (<24×24px)
 * ```tsx
 * <button className="h-4 w-4">×</button> // Too small!
 * ```
 *
 * ✅ DO: Meet 24×24px minimum (WCAG 2.5.8)
 * ```tsx
 * <AccessibleButton size="sm">×</AccessibleButton> // 32×32px
 * ```
 */

/**
 * Testing Example (jest-axe)
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import userEvent from '@testing-library/user-event'
 * import { axe, toHaveNoViolations } from 'jest-axe'
 * import { AccessibleButton } from './accessible-button'
 *
 * expect.extend(toHaveNoViolations)
 *
 * describe('AccessibleButton', () => {
 *   it('should not have accessibility violations', async () => {
 *     const { container } = render(
 *       <AccessibleButton>Click me</AccessibleButton>
 *     )
 *
 *     const results = await axe(container)
 *     expect(results).toHaveNoViolations()
 *   })
 *
 *   it('should be keyboard accessible', async () => {
 *     const onClick = jest.fn()
 *     render(<AccessibleButton onClick={onClick}>Click</AccessibleButton>)
 *
 *     const button = screen.getByRole('button')
 *     await userEvent.tab()
 *     expect(button).toHaveFocus()
 *
 *     await userEvent.keyboard('{Enter}')
 *     expect(onClick).toHaveBeenCalled()
 *   })
 *
 *   it('should have aria-busy when loading', () => {
 *     render(<AccessibleButton isLoading>Save</AccessibleButton>)
 *
 *     const button = screen.getByRole('button')
 *     expect(button).toHaveAttribute('aria-busy', 'true')
 *     expect(button).toBeDisabled()
 *   })
 *
 *   it('should require aria-label for icon-only buttons', () => {
 *     const consoleSpy = jest.spyOn(console, 'warn').mockImplementation()
 *
 *     render(<AccessibleButton icon={<span>X</span>} />)
 *     expect(consoleSpy).toHaveBeenCalledWith(
 *       expect.stringContaining('aria-label')
 *     )
 *
 *     consoleSpy.mockRestore()
 *   })
 * })
 * ```
 */
