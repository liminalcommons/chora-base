// @ts-check
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactPlugin from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import nextPlugin from 'eslint-config-next'
import prettier from 'eslint-config-prettier'
import globals from 'globals'

/**
 * ESLint 9 Flat Config for Next.js 15 + React 19 + TypeScript
 *
 * Based on RT-019-DEV research (Q4 2024 - Q1 2025)
 * Configured for SAP-022 (React Linting & Formatting)
 *
 * Features:
 * - ESLint 9.x flat config (182x faster incremental builds)
 * - TypeScript strict mode integration
 * - React 19 + Next.js 15 patterns
 * - Accessibility enforcement (WCAG 2.2 Level AA)
 * - Pre-commit optimization
 *
 * @see https://eslint.org/docs/latest/use/configure/configuration-files
 * @see https://typescript-eslint.io/getting-started
 */

export default [
  // ============================================================================
  // Global Ignores
  // ============================================================================
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/out/**',
      '**/build/**',
      '**/dist/**',
      '**/.cache/**',
      '**/public/**',
      'next-env.d.ts',
      '*.config.js',
      '*.config.mjs',
      '*.config.ts',
    ],
  },

  // ============================================================================
  // Base Configs
  // ============================================================================
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,

  // ============================================================================
  // React Configuration
  // ============================================================================
  reactPlugin.configs.flat.recommended,
  reactPlugin.configs.flat['jsx-runtime'], // React 17+ JSX transform

  // ============================================================================
  // React Hooks Enforcement (CRITICAL)
  // ============================================================================
  {
    plugins: { 'react-hooks': reactHooks },
    rules: reactHooks.configs.recommended.rules,
  },

  // ============================================================================
  // React Refresh for Next.js Fast Refresh
  // ============================================================================
  {
    plugins: { 'react-refresh': reactRefresh },
    rules: {
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },

  // ============================================================================
  // Accessibility (WCAG 2.2 Level AA)
  // ============================================================================
  jsxA11y.flatConfigs.recommended,

  // ============================================================================
  // Project-Specific Configuration
  // ============================================================================
  {
    files: ['**/*.{js,mjs,cjs,jsx,ts,tsx}'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true, // NEW in typescript-eslint v8 - faster than project
        tsconfigRootDir: import.meta.dirname,
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2024,
      },
    },
    settings: {
      react: {
        version: 'detect', // Auto-detect React version
      },
      next: {
        rootDir: process.cwd(),
      },
    },
    rules: {
      // ========================================================================
      // React 19 / Next.js 15 Specific
      // ========================================================================
      'react/react-in-jsx-scope': 'off', // Not needed with JSX transform
      'react/prop-types': 'off', // Using TypeScript instead

      // ========================================================================
      // TypeScript Strict Mode
      // ========================================================================
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/consistent-type-imports': [
        'warn',
        {
          prefer: 'type-imports',
          fixStyle: 'inline-type-imports',
        },
      ],
      '@typescript-eslint/no-misused-promises': [
        'error',
        {
          checksVoidReturn: {
            attributes: false, // Allow async event handlers
          },
        },
      ],

      // ========================================================================
      // React Hooks - Enforce as Errors
      // ========================================================================
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // ========================================================================
      // Accessibility - Start with Warnings, Escalate to Errors Over Time
      // ========================================================================
      'jsx-a11y/alt-text': 'warn',
      'jsx-a11y/anchor-is-valid': 'warn',
      'jsx-a11y/aria-props': 'warn',
      'jsx-a11y/aria-proptypes': 'warn',
      'jsx-a11y/aria-unsupported-elements': 'warn',
      'jsx-a11y/role-has-required-aria-props': 'warn',
      'jsx-a11y/role-supports-aria-props': 'warn',

      // ========================================================================
      // Code Quality
      // ========================================================================
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
      'object-shorthand': ['warn', 'always'],
      'prefer-template': 'warn',
      'prefer-arrow-callback': 'warn',

      // ========================================================================
      // Import Organization (Optional - uncomment if using eslint-plugin-import)
      // ========================================================================
      // 'import/order': [
      //   'warn',
      //   {
      //     groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
      //     'newlines-between': 'always',
      //     alphabetize: { order: 'asc', caseInsensitive: true },
      //   },
      // ],
    },
  },

  // ============================================================================
  // Test File Overrides
  // ============================================================================
  {
    files: ['**/*.test.{js,jsx,ts,tsx}', '**/*.spec.{js,jsx,ts,tsx}', '**/__tests__/**'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off', // Allow any in tests
      'no-console': 'off', // Allow console in tests
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
    },
  },

  // ============================================================================
  // Next.js API Route Overrides
  // ============================================================================
  {
    files: ['**/app/api/**/*.{js,ts}', '**/pages/api/**/*.{js,ts}'],
    rules: {
      'no-console': 'off', // Allow console in API routes
    },
  },

  // ============================================================================
  // Next.js Config File Overrides
  // ============================================================================
  {
    files: ['next.config.{js,mjs,ts}'],
    rules: {
      '@typescript-eslint/no-var-requires': 'off',
      'no-console': 'off',
    },
  },

  // ============================================================================
  // Prettier MUST BE LAST - Disables Conflicting Rules
  // ============================================================================
  prettier,
]
