/**
 * lint-staged Configuration
 *
 * Runs linters on git staged files before commit
 * Part of SAP-022 (React Linting & Formatting)
 *
 * Integration with Husky:
 * 1. Install: npm install -D husky@^9.1.7 lint-staged@^15.2.11
 * 2. Init Husky: npx husky init
 * 3. Create .husky/pre-commit with: npx lint-staged
 *
 * @see https://github.com/lint-staged/lint-staged
 */

export default {
  // JavaScript/TypeScript files
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix --max-warnings=0', // Fix and enforce zero warnings
    'prettier --write', // Format after linting
  ],

  // JSON, Markdown, YAML, CSS files
  '*.{json,md,yml,yaml,css}': [
    'prettier --write',
  ],

  // Package.json specific
  'package.json': [
    'prettier --write',
  ],
}
