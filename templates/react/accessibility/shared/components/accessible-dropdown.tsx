/**
 * Accessible Dropdown/Select Component
 *
 * WCAG 2.2 Level AA compliant dropdown with:
 * - Keyboard navigation (Arrow keys, Enter, Escape)
 * - aria-expanded state
 * - aria-activedescendant for active option
 * - Focus management
 * - Screen reader announcements
 * - Minimum 24×24px click targets
 *
 * Based on ARIA Authoring Practices Guide:
 * https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
 *
 * Usage:
 * ```tsx
 * <AccessibleDropdown
 *   label="Select country"
 *   options={[
 *     { value: 'us', label: 'United States' },
 *     { value: 'ca', label: 'Canada' },
 *     { value: 'uk', label: 'United Kingdom' },
 *   ]}
 *   value={country}
 *   onChange={setCountry}
 * />
 * ```
 */

import { useState, useRef, useEffect, type KeyboardEvent } from 'react'

export interface DropdownOption {
  value: string
  label: string
  disabled?: boolean
}

interface AccessibleDropdownProps {
  /** Dropdown label */
  label: string
  /** Available options */
  options: DropdownOption[]
  /** Current selected value */
  value?: string
  /** Change handler */
  onChange: (value: string) => void
  /** Optional placeholder */
  placeholder?: string
  /** Required field */
  required?: boolean
  /** Disabled state */
  disabled?: boolean
  /** Error message */
  error?: string
  /** Help text */
  helpText?: string
  /** Optional className */
  className?: string
}

export function AccessibleDropdown({
  label,
  options,
  value,
  onChange,
  placeholder = 'Select an option',
  required = false,
  disabled = false,
  error,
  helpText,
  className = '',
}: AccessibleDropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)
  const buttonRef = useRef<HTMLButtonElement>(null)
  const listboxRef = useRef<HTMLUListElement>(null)

  const selectedOption = options.find(opt => opt.value === value)
  const hasError = Boolean(error)
  const dropdownId = `dropdown-${label.toLowerCase().replace(/\s+/g, '-')}`
  const listboxId = `${dropdownId}-listbox`
  const helpId = `${dropdownId}-help`
  const errorId = `${dropdownId}-error`

  // Build aria-describedby
  const describedBy = [
    helpText && helpId,
    hasError && errorId,
  ].filter(Boolean).join(' ') || undefined

  // Handle keyboard navigation
  const handleKeyDown = (event: KeyboardEvent<HTMLButtonElement>) => {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault()
        if (!isOpen) {
          setIsOpen(true)
          setActiveIndex(0)
        } else {
          setActiveIndex(prev =>
            prev < options.length - 1 ? prev + 1 : prev
          )
        }
        break

      case 'ArrowUp':
        event.preventDefault()
        if (!isOpen) {
          setIsOpen(true)
          setActiveIndex(options.length - 1)
        } else {
          setActiveIndex(prev => (prev > 0 ? prev - 1 : prev))
        }
        break

      case 'Enter':
      case ' ':
        event.preventDefault()
        if (isOpen && activeIndex >= 0) {
          const selectedOpt = options[activeIndex]
          if (!selectedOpt.disabled) {
            onChange(selectedOpt.value)
            setIsOpen(false)
            buttonRef.current?.focus()
          }
        } else {
          setIsOpen(true)
        }
        break

      case 'Escape':
        event.preventDefault()
        setIsOpen(false)
        buttonRef.current?.focus()
        break

      case 'Home':
        event.preventDefault()
        setActiveIndex(0)
        break

      case 'End':
        event.preventDefault()
        setActiveIndex(options.length - 1)
        break
    }
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    if (!isOpen) return

    const handleClickOutside = (event: MouseEvent) => {
      if (
        buttonRef.current &&
        !buttonRef.current.contains(event.target as Node) &&
        listboxRef.current &&
        !listboxRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  // Scroll active option into view
  useEffect(() => {
    if (!isOpen || activeIndex < 0) return

    const listbox = listboxRef.current
    const activeOption = listbox?.children[activeIndex] as HTMLElement
    activeOption?.scrollIntoView({ block: 'nearest' })
  }, [activeIndex, isOpen])

  return (
    <div className={`relative ${className}`}>
      {/* Label */}
      <label
        id={`${dropdownId}-label`}
        htmlFor={dropdownId}
        className="mb-1 block text-sm font-medium text-gray-700"
      >
        {label}
        {required && (
          <span className="ml-1 text-red-500" aria-label="required">
            *
          </span>
        )}
      </label>

      {/* Help text */}
      {helpText && (
        <p id={helpId} className="mb-1 text-sm text-gray-600">
          {helpText}
        </p>
      )}

      {/* Dropdown button */}
      <button
        ref={buttonRef}
        id={dropdownId}
        type="button"
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-controls={listboxId}
        aria-labelledby={`${dropdownId}-label`}
        aria-describedby={describedBy}
        aria-invalid={hasError || undefined}
        aria-activedescendant={
          isOpen && activeIndex >= 0
            ? `${listboxId}-option-${activeIndex}`
            : undefined
        }
        disabled={disabled}
        onKeyDown={handleKeyDown}
        onClick={() => setIsOpen(!isOpen)}
        className={`flex h-10 w-full items-center justify-between rounded-md border px-3 py-2 text-left shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 ${
          hasError
            ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
            : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
        } ${disabled ? 'cursor-not-allowed bg-gray-100' : 'bg-white'}`}
      >
        <span className={selectedOption ? 'text-gray-900' : 'text-gray-500'}>
          {selectedOption?.label || placeholder}
        </span>
        <svg
          className={`h-5 w-5 text-gray-400 transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Error message */}
      {hasError && (
        <p
          id={errorId}
          role="alert"
          aria-live="assertive"
          className="mt-1 text-sm text-red-600"
        >
          {error}
        </p>
      )}

      {/* Options listbox */}
      {isOpen && (
        <ul
          ref={listboxRef}
          id={listboxId}
          role="listbox"
          aria-labelledby={`${dropdownId}-label`}
          className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md border border-gray-300 bg-white shadow-lg focus:outline-none"
        >
          {options.map((option, index) => (
            <li
              key={option.value}
              id={`${listboxId}-option-${index}`}
              role="option"
              aria-selected={option.value === value}
              aria-disabled={option.disabled || undefined}
              onClick={() => {
                if (!option.disabled) {
                  onChange(option.value)
                  setIsOpen(false)
                  buttonRef.current?.focus()
                }
              }}
              onMouseEnter={() => setActiveIndex(index)}
              className={`cursor-pointer px-3 py-2 ${
                option.disabled
                  ? 'cursor-not-allowed text-gray-400'
                  : 'text-gray-900'
              } ${
                index === activeIndex
                  ? 'bg-blue-100'
                  : option.value === value
                  ? 'bg-blue-50'
                  : 'hover:bg-gray-50'
              }`}
            >
              {option.label}
              {option.value === value && (
                <svg
                  className="ml-2 inline h-4 w-4 text-blue-600"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

/**
 * Example: Form with Dropdown
 *
 * ```tsx
 * function CountrySelector() {
 *   const [country, setCountry] = useState('')
 *
 *   const countries = [
 *     { value: 'us', label: 'United States' },
 *     { value: 'ca', label: 'Canada' },
 *     { value: 'uk', label: 'United Kingdom' },
 *     { value: 'au', label: 'Australia' },
 *     { value: 'de', label: 'Germany', disabled: true },
 *   ]
 *
 *   return (
 *     <AccessibleDropdown
 *       label="Country"
 *       options={countries}
 *       value={country}
 *       onChange={setCountry}
 *       required
 *       helpText="Select your country of residence"
 *     />
 *   )
 * }
 * ```
 */

/**
 * Alternative: Radix UI Select
 *
 * For a more feature-rich dropdown, use Radix UI:
 *
 * ```tsx
 * import * as Select from '@radix-ui/react-select'
 *
 * function RadixDropdownExample() {
 *   return (
 *     <Select.Root>
 *       <Select.Trigger className="inline-flex items-center gap-2">
 *         <Select.Value placeholder="Select a country" />
 *         <Select.Icon />
 *       </Select.Trigger>
 *
 *       <Select.Portal>
 *         <Select.Content className="overflow-hidden rounded-md bg-white shadow-lg">
 *           <Select.Viewport className="p-1">
 *             <Select.Item value="us">
 *               <Select.ItemText>United States</Select.ItemText>
 *               <Select.ItemIndicator>✓</Select.ItemIndicator>
 *             </Select.Item>
 *             <Select.Item value="ca">
 *               <Select.ItemText>Canada</Select.ItemText>
 *             </Select.Item>
 *           </Select.Viewport>
 *         </Select.Content>
 *       </Select.Portal>
 *     </Select.Root>
 *   )
 * }
 * ```
 *
 * Radix UI handles keyboard navigation, ARIA attributes, and focus management automatically.
 */

/**
 * Testing Example (jest-axe)
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import userEvent from '@testing-library/user-event'
 * import { axe, toHaveNoViolations } from 'jest-axe'
 * import { AccessibleDropdown } from './accessible-dropdown'
 *
 * expect.extend(toHaveNoViolations)
 *
 * const mockOptions = [
 *   { value: 'us', label: 'United States' },
 *   { value: 'ca', label: 'Canada' },
 * ]
 *
 * describe('AccessibleDropdown', () => {
 *   it('should not have accessibility violations', async () => {
 *     const { container } = render(
 *       <AccessibleDropdown
 *         label="Country"
 *         options={mockOptions}
 *         onChange={() => {}}
 *       />
 *     )
 *
 *     const results = await axe(container)
 *     expect(results).toHaveNoViolations()
 *   })
 *
 *   it('should open with Enter key', async () => {
 *     render(
 *       <AccessibleDropdown
 *         label="Country"
 *         options={mockOptions}
 *         onChange={() => {}}
 *       />
 *     )
 *
 *     const button = screen.getByRole('combobox')
 *     expect(button).toHaveAttribute('aria-expanded', 'false')
 *
 *     await userEvent.click(button)
 *     expect(button).toHaveAttribute('aria-expanded', 'true')
 *
 *     const listbox = screen.getByRole('listbox')
 *     expect(listbox).toBeInTheDocument()
 *   })
 *
 *   it('should navigate options with Arrow keys', async () => {
 *     const onChange = jest.fn()
 *     render(
 *       <AccessibleDropdown
 *         label="Country"
 *         options={mockOptions}
 *         onChange={onChange}
 *       />
 *     )
 *
 *     const button = screen.getByRole('combobox')
 *     await userEvent.click(button)
 *
 *     await userEvent.keyboard('{ArrowDown}')
 *     await userEvent.keyboard('{Enter}')
 *
 *     expect(onChange).toHaveBeenCalledWith('us')
 *   })
 * })
 * ```
 */
