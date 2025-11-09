/**
 * Vitest Setup for Accessibility Testing (Vite)
 *
 * This file configures vitest-axe for automated accessibility testing.
 * Place this file in your project root and reference it in vitest.config.ts.
 *
 * Setup Instructions:
 * 1. Install dependencies:
 *    npm install --save-dev vitest-axe @axe-core/react
 *
 * 2. Add to vitest.config.ts:
 *    export default defineConfig({
 *      test: {
 *        setupFiles: ['./vitest.setup.ts'],
 *        // ... other config
 *      },
 *    })
 *
 * 3. Use in tests:
 *    import { axe, toHaveNoViolations } from 'vitest-axe'
 *    expect.extend(toHaveNoViolations)
 *
 *    it('should not have a11y violations', async () => {
 *      const { container } = render(<Component />)
 *      const results = await axe(container)
 *      expect(results).toHaveNoViolations()
 *    })
 */

import '@testing-library/jest-dom/vitest'
import { toHaveNoViolations } from 'vitest-axe'
import { expect } from 'vitest'

// Extend Vitest matchers with vitest-axe
expect.extend(toHaveNoViolations)

// Optional: Configure axe-core rules
// This is the default configuration; customize as needed
// See: https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#api-name-axeconfigure

// Example: Disable specific rules (use sparingly)
// import { configureAxe } from 'vitest-axe'
//
// const axe = configureAxe({
//   rules: {
//     // Disable "landmark-one-main" rule for tests
//     'landmark-one-main': { enabled: false },
//   },
// })

// Suppress console warnings for known test scenarios
const originalWarn = console.warn
beforeAll(() => {
  console.warn = (...args: any[]) => {
    // Suppress specific warnings you expect in tests
    if (
      typeof args[0] === 'string' &&
      args[0].includes('some expected warning')
    ) {
      return
    }
    originalWarn.call(console, ...args)
  }
})

afterAll(() => {
  console.warn = originalWarn
})
