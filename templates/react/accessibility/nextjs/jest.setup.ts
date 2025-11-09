/**
 * Jest Setup for Accessibility Testing (Next.js)
 *
 * This file configures jest-axe for automated accessibility testing.
 * Place this file in your project root and reference it in jest.config.js.
 *
 * Setup Instructions:
 * 1. Install dependencies:
 *    npm install --save-dev jest-axe @axe-core/react
 *
 * 2. Add to jest.config.js:
 *    module.exports = {
 *      setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
 *      // ... other config
 *    }
 *
 * 3. Use in tests:
 *    import { axe, toHaveNoViolations } from 'jest-axe'
 *    expect.extend(toHaveNoViolations)
 *
 *    it('should not have a11y violations', async () => {
 *      const { container } = render(<Component />)
 *      const results = await axe(container)
 *      expect(results).toHaveNoViolations()
 *    })
 */

import '@testing-library/jest-dom'
import { toHaveNoViolations } from 'jest-axe'

// Extend Jest matchers with jest-axe
expect.extend(toHaveNoViolations)

// Optional: Configure axe-core rules
// This is the default configuration; customize as needed
// See: https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#api-name-axeconfigure

// Example: Disable specific rules (use sparingly)
// import { configureAxe } from 'jest-axe'
//
// const axe = configureAxe({
//   rules: {
//     // Disable "landmark-one-main" rule for tests
//     'landmark-one-main': { enabled: false },
//   },
// })

// Suppress console errors for specific expected errors in tests
const originalError = console.error
beforeAll(() => {
  console.error = (...args: any[]) => {
    // Suppress React 18 ReactDOM.render deprecation warning in tests
    if (
      typeof args[0] === 'string' &&
      args[0].includes('ReactDOM.render')
    ) {
      return
    }
    originalError.call(console, ...args)
  }
})

afterAll(() => {
  console.error = originalError
})

// Optional: Global test timeout (accessibility tests can be slow)
jest.setTimeout(10000) // 10 seconds
