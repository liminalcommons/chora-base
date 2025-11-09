/**
 * Accessible Tabs Component
 *
 * WCAG 2.2 Level AA compliant tabs with:
 * - Arrow key navigation (Left/Right to switch tabs)
 * - Home/End key support
 * - Roving tabindex (only active tab is in Tab order)
 * - aria-selected on active tab
 * - aria-controls linking tabs to panels
 * - Keyboard activation (Enter/Space)
 *
 * Based on ARIA Authoring Practices Guide:
 * https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
 *
 * Usage:
 * ```tsx
 * const tabs = [
 *   { id: 'profile', label: 'Profile', content: <ProfilePanel /> },
 *   { id: 'settings', label: 'Settings', content: <SettingsPanel /> },
 *   { id: 'notifications', label: 'Notifications', content: <NotificationsPanel /> },
 * ]
 *
 * <AccessibleTabs tabs={tabs} defaultTab="profile" />
 * ```
 */

import { useState, useRef, useEffect, type KeyboardEvent } from 'react'

export interface Tab {
  id: string
  label: string
  content: React.ReactNode
  disabled?: boolean
}

interface AccessibleTabsProps {
  /** Array of tab configurations */
  tabs: Tab[]
  /** Default active tab ID */
  defaultTab?: string
  /** Optional className for container */
  className?: string
  /** Optional onChange handler */
  onChange?: (tabId: string) => void
}

export function AccessibleTabs({
  tabs,
  defaultTab,
  className = '',
  onChange,
}: AccessibleTabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id)
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([])

  const activeIndex = tabs.findIndex(tab => tab.id === activeTab)

  // Update active tab and call onChange
  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId)
    onChange?.(tabId)
  }

  // Handle keyboard navigation
  const handleKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    let newIndex = index

    switch (event.key) {
      case 'ArrowLeft':
        event.preventDefault()
        newIndex = index > 0 ? index - 1 : tabs.length - 1
        break

      case 'ArrowRight':
        event.preventDefault()
        newIndex = index < tabs.length - 1 ? index + 1 : 0
        break

      case 'Home':
        event.preventDefault()
        newIndex = 0
        break

      case 'End':
        event.preventDefault()
        newIndex = tabs.length - 1
        break

      default:
        return
    }

    // Skip disabled tabs
    while (tabs[newIndex]?.disabled) {
      if (event.key === 'ArrowLeft' || event.key === 'End') {
        newIndex = newIndex > 0 ? newIndex - 1 : tabs.length - 1
      } else {
        newIndex = newIndex < tabs.length - 1 ? newIndex + 1 : 0
      }

      // Prevent infinite loop if all tabs are disabled
      if (newIndex === index) return
    }

    handleTabChange(tabs[newIndex].id)
    tabRefs.current[newIndex]?.focus()
  }

  // Focus active tab when it changes (for programmatic changes)
  useEffect(() => {
    if (activeIndex >= 0) {
      tabRefs.current[activeIndex]?.focus()
    }
  }, [activeTab, activeIndex])

  return (
    <div className={className}>
      {/* Tab list */}
      <div
        role="tablist"
        aria-label="Content tabs"
        className="flex border-b border-gray-200"
      >
        {tabs.map((tab, index) => {
          const isActive = tab.id === activeTab
          const isDisabled = tab.disabled || false

          return (
            <button
              key={tab.id}
              ref={el => (tabRefs.current[index] = el)}
              role="tab"
              id={`tab-${tab.id}`}
              aria-selected={isActive}
              aria-controls={`panel-${tab.id}`}
              aria-disabled={isDisabled || undefined}
              tabIndex={isActive ? 0 : -1} // Roving tabindex
              disabled={isDisabled}
              onClick={() => handleTabChange(tab.id)}
              onKeyDown={e => handleKeyDown(e, index)}
              className={`px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                isActive
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              } ${
                isDisabled
                  ? 'cursor-not-allowed opacity-50'
                  : 'cursor-pointer'
              }`}
            >
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Tab panels */}
      {tabs.map(tab => {
        const isActive = tab.id === activeTab

        return (
          <div
            key={tab.id}
            role="tabpanel"
            id={`panel-${tab.id}`}
            aria-labelledby={`tab-${tab.id}`}
            hidden={!isActive}
            tabIndex={0}
            className="py-4 focus:outline-none"
          >
            {isActive && tab.content}
          </div>
        )
      })}
    </div>
  )
}

/**
 * Example: Tabs with Complex Content
 *
 * ```tsx
 * function UserSettings() {
 *   const tabs = [
 *     {
 *       id: 'profile',
 *       label: 'Profile',
 *       content: (
 *         <div>
 *           <h2>Profile Settings</h2>
 *           <form>
 *             <input type="text" placeholder="Name" />
 *             <button type="submit">Save</button>
 *           </form>
 *         </div>
 *       ),
 *     },
 *     {
 *       id: 'security',
 *       label: 'Security',
 *       content: (
 *         <div>
 *           <h2>Security Settings</h2>
 *           <button>Change Password</button>
 *           <button>Enable 2FA</button>
 *         </div>
 *       ),
 *     },
 *     {
 *       id: 'notifications',
 *       label: 'Notifications',
 *       content: (
 *         <div>
 *           <h2>Notification Preferences</h2>
 *           <label>
 *             <input type="checkbox" /> Email notifications
 *           </label>
 *         </div>
 *       ),
 *       disabled: true, // Coming soon
 *     },
 *   ]
 *
 *   return (
 *     <AccessibleTabs
 *       tabs={tabs}
 *       defaultTab="profile"
 *       onChange={(tabId) => console.log('Tab changed:', tabId)}
 *     />
 *   )
 * }
 * ```
 */

/**
 * Alternative: Radix UI Tabs
 *
 * For more features (lazy loading, orientation, activation mode), use Radix UI:
 *
 * ```tsx
 * import * as Tabs from '@radix-ui/react-tabs'
 *
 * function RadixTabsExample() {
 *   return (
 *     <Tabs.Root defaultValue="profile">
 *       <Tabs.List aria-label="Settings">
 *         <Tabs.Trigger value="profile">Profile</Tabs.Trigger>
 *         <Tabs.Trigger value="security">Security</Tabs.Trigger>
 *         <Tabs.Trigger value="notifications">Notifications</Tabs.Trigger>
 *       </Tabs.List>
 *
 *       <Tabs.Content value="profile">
 *         <h2>Profile Settings</h2>
 *       </Tabs.Content>
 *
 *       <Tabs.Content value="security">
 *         <h2>Security Settings</h2>
 *       </Tabs.Content>
 *
 *       <Tabs.Content value="notifications">
 *         <h2>Notification Preferences</h2>
 *       </Tabs.Content>
 *     </Tabs.Root>
 *   )
 * }
 * ```
 *
 * Radix UI handles keyboard navigation, ARIA attributes, and roving tabindex automatically.
 */

/**
 * ARIA Pattern Explanation
 *
 * **Roving Tabindex**:
 * Only the active tab is in the Tab order (tabIndex={0}).
 * Inactive tabs have tabIndex={-1} (not in Tab order).
 * This prevents keyboard users from tabbing through all tabs.
 *
 * **Keyboard Navigation**:
 * - Tab: Focus tab list (active tab) or move to next focusable element
 * - Arrow Left/Right: Navigate between tabs
 * - Home/End: Jump to first/last tab
 * - Enter/Space: Activate focused tab (handled by <button>)
 *
 * **ARIA Attributes**:
 * - role="tablist" on container
 * - role="tab" on each tab button
 * - role="tabpanel" on each panel
 * - aria-selected="true" on active tab
 * - aria-controls links tab to panel (tab-profile → panel-profile)
 * - aria-labelledby links panel to tab
 */

/**
 * Testing Example (jest-axe)
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import userEvent from '@testing-library/user-event'
 * import { axe, toHaveNoViolations } from 'jest-axe'
 * import { AccessibleTabs, type Tab } from './accessible-tabs'
 *
 * expect.extend(toHaveNoViolations)
 *
 * const mockTabs: Tab[] = [
 *   { id: 'tab1', label: 'Tab 1', content: <div>Content 1</div> },
 *   { id: 'tab2', label: 'Tab 2', content: <div>Content 2</div> },
 *   { id: 'tab3', label: 'Tab 3', content: <div>Content 3</div> },
 * ]
 *
 * describe('AccessibleTabs', () => {
 *   it('should not have accessibility violations', async () => {
 *     const { container } = render(<AccessibleTabs tabs={mockTabs} />)
 *
 *     const results = await axe(container)
 *     expect(results).toHaveNoViolations()
 *   })
 *
 *   it('should show default tab', () => {
 *     render(<AccessibleTabs tabs={mockTabs} defaultTab="tab2" />)
 *
 *     const tab2 = screen.getByRole('tab', { name: 'Tab 2' })
 *     expect(tab2).toHaveAttribute('aria-selected', 'true')
 *     expect(screen.getByText('Content 2')).toBeVisible()
 *   })
 *
 *   it('should switch tabs with Arrow keys', async () => {
 *     render(<AccessibleTabs tabs={mockTabs} />)
 *
 *     const tab1 = screen.getByRole('tab', { name: 'Tab 1' })
 *     tab1.focus()
 *
 *     await userEvent.keyboard('{ArrowRight}')
 *
 *     const tab2 = screen.getByRole('tab', { name: 'Tab 2' })
 *     expect(tab2).toHaveFocus()
 *     expect(tab2).toHaveAttribute('aria-selected', 'true')
 *     expect(screen.getByText('Content 2')).toBeVisible()
 *   })
 *
 *   it('should use roving tabindex', () => {
 *     render(<AccessibleTabs tabs={mockTabs} defaultTab="tab2" />)
 *
 *     const tab1 = screen.getByRole('tab', { name: 'Tab 1' })
 *     const tab2 = screen.getByRole('tab', { name: 'Tab 2' })
 *     const tab3 = screen.getByRole('tab', { name: 'Tab 3' })
 *
 *     expect(tab1).toHaveAttribute('tabindex', '-1')
 *     expect(tab2).toHaveAttribute('tabindex', '0') // Active
 *     expect(tab3).toHaveAttribute('tabindex', '-1')
 *   })
 *
 *   it('should skip disabled tabs', async () => {
 *     const tabsWithDisabled = [
 *       ...mockTabs,
 *       { id: 'tab4', label: 'Tab 4 (disabled)', content: <div>Content 4</div>, disabled: true },
 *     ]
 *
 *     render(<AccessibleTabs tabs={tabsWithDisabled} />)
 *
 *     const tab3 = screen.getByRole('tab', { name: 'Tab 3' })
 *     tab3.focus()
 *
 *     await userEvent.keyboard('{ArrowRight}')
 *
 *     // Should wrap to tab 1, skipping disabled tab 4
 *     const tab1 = screen.getByRole('tab', { name: 'Tab 1' })
 *     expect(tab1).toHaveFocus()
 *   })
 * })
 * ```
 */
