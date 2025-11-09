/**
 * Accessible Modal/Dialog Component
 *
 * WCAG 2.2 Level AA compliant modal dialog with:
 * - Focus trap (Tab cycles within modal)
 * - Keyboard handling (Escape to close)
 * - aria-modal and aria-labelledby
 * - Focus restoration on close
 * - Scroll lock on body
 *
 * Based on ARIA Authoring Practices Guide:
 * https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
 *
 * Usage:
 * ```tsx
 * <AccessibleModal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="Confirm Action"
 *   description="Are you sure you want to proceed?"
 * >
 *   <p>This action cannot be undone.</p>
 *   <button onClick={handleConfirm}>Confirm</button>
 * </AccessibleModal>
 * ```
 */

import { useEffect, useRef, type ReactNode } from 'react'
import FocusLock from 'react-focus-lock'

interface AccessibleModalProps {
  /** Controls modal visibility */
  isOpen: boolean
  /** Called when modal should close (Escape key or backdrop click) */
  onClose: () => void
  /** Modal title - used for aria-labelledby */
  title: string
  /** Optional description - used for aria-describedby */
  description?: string
  /** Modal content */
  children: ReactNode
  /** Optional className for modal container */
  className?: string
  /** Disable backdrop click to close (default: false) */
  disableBackdropClick?: boolean
  /** Disable Escape key to close (default: false) */
  disableEscapeKey?: boolean
}

export function AccessibleModal({
  isOpen,
  onClose,
  title,
  description,
  children,
  className = '',
  disableBackdropClick = false,
  disableEscapeKey = false,
}: AccessibleModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  // Store previously focused element for restoration on close
  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement
    } else {
      // Restore focus when modal closes
      previousFocusRef.current?.focus()
    }
  }, [isOpen])

  // Handle Escape key
  useEffect(() => {
    if (!isOpen || disableEscapeKey) return

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault()
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose, disableEscapeKey])

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (!isOpen) return

    const originalOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'

    return () => {
      document.body.style.overflow = originalOverflow
    }
  }, [isOpen])

  // Handle backdrop click
  const handleBackdropClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (disableBackdropClick) return
    if (event.target === event.currentTarget) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={handleBackdropClick}
      aria-hidden="true"
    >
      <FocusLock returnFocus>
        <div
          ref={modalRef}
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
          aria-describedby={description ? 'modal-description' : undefined}
          className={`relative max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-lg bg-white p-6 shadow-xl ${className}`}
        >
          {/* Close button for keyboard users (visible focus indicator) */}
          <button
            type="button"
            onClick={onClose}
            className="absolute right-4 top-4 rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            aria-label="Close dialog"
          >
            <svg
              className="h-5 w-5"
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          {/* Modal Title */}
          <h2
            id="modal-title"
            className="mb-4 pr-8 text-2xl font-bold text-gray-900"
          >
            {title}
          </h2>

          {/* Modal Description */}
          {description && (
            <p id="modal-description" className="mb-4 text-sm text-gray-600">
              {description}
            </p>
          )}

          {/* Modal Content */}
          <div className="text-gray-800">{children}</div>
        </div>
      </FocusLock>
    </div>
  )
}

/**
 * Example Usage with Radix UI (Alternative)
 *
 * Radix UI provides pre-built accessible primitives.
 * Use this if you prefer a headless UI library:
 *
 * ```tsx
 * import * as Dialog from '@radix-ui/react-dialog'
 *
 * function RadixModalExample() {
 *   return (
 *     <Dialog.Root>
 *       <Dialog.Trigger asChild>
 *         <button>Open Modal</button>
 *       </Dialog.Trigger>
 *
 *       <Dialog.Portal>
 *         <Dialog.Overlay className="fixed inset-0 bg-black/50" />
 *         <Dialog.Content className="fixed left-1/2 top-1/2 max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6">
 *           <Dialog.Title className="text-2xl font-bold">
 *             Edit Profile
 *           </Dialog.Title>
 *           <Dialog.Description className="text-sm text-gray-600">
 *             Make changes to your profile here.
 *           </Dialog.Description>
 *
 *           <form>
 *             <input type="text" placeholder="Name" />
 *             <button type="submit">Save</button>
 *           </form>
 *
 *           <Dialog.Close asChild>
 *             <button aria-label="Close">×</button>
 *           </Dialog.Close>
 *         </Dialog.Content>
 *       </Dialog.Portal>
 *     </Dialog.Root>
 *   )
 * }
 * ```
 *
 * Radix UI handles focus trap, Escape key, aria attributes automatically.
 */

/**
 * Testing Example (jest-axe)
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import userEvent from '@testing-library/user-event'
 * import { axe, toHaveNoViolations } from 'jest-axe'
 * import { AccessibleModal } from './accessible-modal'
 *
 * expect.extend(toHaveNoViolations)
 *
 * describe('AccessibleModal', () => {
 *   it('should not have accessibility violations', async () => {
 *     const { container } = render(
 *       <AccessibleModal
 *         isOpen={true}
 *         onClose={() => {}}
 *         title="Test Modal"
 *       >
 *         <p>Modal content</p>
 *       </AccessibleModal>
 *     )
 *
 *     const results = await axe(container)
 *     expect(results).toHaveNoViolations()
 *   })
 *
 *   it('should close on Escape key', async () => {
 *     const onClose = jest.fn()
 *     render(
 *       <AccessibleModal isOpen={true} onClose={onClose} title="Test">
 *         Content
 *       </AccessibleModal>
 *     )
 *
 *     await userEvent.keyboard('{Escape}')
 *     expect(onClose).toHaveBeenCalled()
 *   })
 *
 *   it('should trap focus within modal', async () => {
 *     render(
 *       <AccessibleModal isOpen={true} onClose={() => {}} title="Test">
 *         <button>Button 1</button>
 *         <button>Button 2</button>
 *       </AccessibleModal>
 *     )
 *
 *     const closeButton = screen.getByLabelText('Close dialog')
 *     const button1 = screen.getByText('Button 1')
 *     const button2 = screen.getByText('Button 2')
 *
 *     // Tab should cycle within modal
 *     await userEvent.tab()
 *     expect(closeButton).toHaveFocus()
 *
 *     await userEvent.tab()
 *     expect(button1).toHaveFocus()
 *
 *     await userEvent.tab()
 *     expect(button2).toHaveFocus()
 *
 *     await userEvent.tab()
 *     expect(closeButton).toHaveFocus() // Cycles back
 *   })
 * })
 * ```
 */
