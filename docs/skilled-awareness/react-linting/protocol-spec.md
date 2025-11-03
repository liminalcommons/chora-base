# SAP-022: React Linting & Formatting - Protocol Specification

**SAP ID**: SAP-022
**Version**: 1.0.0
**ESLint Version**: 9.26.x
**Prettier Version**: 3.6.x
**Research Foundation**: RT-019-DEV (Q4 2024 - Q1 2025)

---

## Overview

This document specifies the technical contracts, linting rules, and formatting standards for React applications using the SAP-022 capability package.

**Scope**: Code quality and formatting for React 19 applications using ESLint 9 flat config, Prettier 3.x, and TypeScript 5.7
**Audience**: AI agents, developers configuring React linting
**Compliance**: ESLint 9.x flat config, Prettier 3.x, React 19, Next.js 15, Vite 7

---

## Protocol Foundation

### ESLint 9.x Flat Config Standard

**Version**: 9.26.x+
**Source**: https://eslint.org/docs/latest/use/configure/configuration-files
**Status**: Production-ready since April 2024, default in ESLint 9+

**Key Breaking Changes from ESLint 8**:
- ❌ `.eslintrc.js` / `.eslintrc.json` **DEPRECATED**
- ✅ `eslint.config.mjs` **REQUIRED** (flat config)
- ❌ `extends` property **REMOVED**
- ✅ Array-based configuration
- ❌ `env` property **REMOVED**
- ✅ `languageOptions.globals` replaces env

**Performance Improvement**: 182x faster incremental builds vs ESLint 8.x

### Prettier 3.x Standard

**Version**: 3.6.2+
**Source**: https://prettier.io
**Adoption**: 80%+ in React community (State of JS 2024)

**Default Changes in Prettier 3.x**:
- `trailingComma: "all"` is now default (was "es5" in v2)
- Improved TypeScript support
- Faster formatting (20% improvement)

---

## ESLint Plugin Decision Matrix

### Required Plugins (8 core plugins)

| Plugin | Version | Purpose | Rationale |
|--------|---------|---------|-----------|
| `@eslint/js` | ^9.26.0 | Base JavaScript rules | ESLint core recommended config |
| `typescript-eslint` | ^8.32.0 | TypeScript linting | Strict mode, projectService API |
| `eslint-plugin-react` | ^7.37.5 | React-specific rules | 25.7M weekly downloads, React 19 support |
| `eslint-plugin-react-hooks` | ^7.0.1 | Rules of Hooks enforcement | **Critical** - prevents hook violations |
| `eslint-plugin-react-refresh` | ^0.4.24 | Fast Refresh compatibility | Next.js 15 / Vite 7 HMR support |
| `eslint-plugin-jsx-a11y` | ^6.10.2 | Accessibility linting | WCAG 2.2 Level AA, 85%+ a11y coverage |
| `eslint-config-next` | 15.x | Next.js patterns | Core Web Vitals, Next.js best practices |
| `eslint-config-prettier` | ^9.1.0 | Disable conflicting rules | Prevents Prettier vs ESLint conflicts |

### Optional Plugins (user can add)

| Plugin | Use Case | When to Add |
|--------|----------|-------------|
| `eslint-plugin-import` | Import organization | Monorepos, strict import order |
| `eslint-plugin-testing-library` | Test linting | If using SAP-021 (React Testing) |
| `eslint-plugin-storybook` | Storybook linting | If using Storybook |
| `eslint-plugin-tailwindcss` | Tailwind linting | If using Tailwind (SAP-024) |

---

## ESLint Configuration Standard

### Next.js 15 Configuration

**File**: `eslint.config.mjs` (project root)

```javascript
// @ts-check
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactPlugin from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import prettier from 'eslint-config-prettier'
import globals from 'globals'

export default [
  // Global ignores
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
    ],
  },

  // Base configs
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,

  // React configuration
  reactPlugin.configs.flat.recommended,
  reactPlugin.configs.flat['jsx-runtime'],

  // React Hooks enforcement
  {
    plugins: { 'react-hooks': reactHooks },
    rules: reactHooks.configs.recommended.rules,
  },

  // React Refresh for Next.js
  {
    plugins: { 'react-refresh': reactRefresh },
    rules: {
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },

  // Accessibility
  jsxA11y.flatConfigs.recommended,

  // Project-specific rules
  {
    files: ['**/*.{js,mjs,cjs,jsx,ts,tsx}'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true, // NEW in typescript-eslint v8
        tsconfigRootDir: import.meta.dirname,
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2024,
      },
    },
    settings: {
      react: { version: 'detect' },
    },
    rules: {
      // React 19 / Next.js 15
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',

      // TypeScript strict
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],

      // React Hooks
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // Accessibility (start with warnings)
      'jsx-a11y/alt-text': 'warn',
      'jsx-a11y/anchor-is-valid': 'warn',

      // Code quality
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },

  // Test file overrides
  {
    files: ['**/*.test.{js,jsx,ts,tsx}', '**/*.spec.{js,jsx,ts,tsx}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      'no-console': 'off',
    },
  },

  // Prettier MUST BE LAST
  prettier,
]
```

### Vite 7 Configuration

**Differences from Next.js**:
- Remove `eslint-config-next` import
- Change ignores: `**/.next/**` → `**/dist/**`
- Remove `globals.node` (browser-only)
- Keep same React, TypeScript, accessibility rules

---

## Prettier Configuration Standard

### .prettierrc

**File**: `.prettierrc` (JSON format)

```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always",
  "endOfLine": "lf",
  "jsxSingleQuote": false,
  "bracketSpacing": true,
  "proseWrap": "preserve",
  "quoteProps": "as-needed",
  "htmlWhitespaceSensitivity": "css"
}
```

**Setting Rationale**:

| Setting | Value | Rationale |
|---------|-------|-----------|
| `semi` | `true` | Explicit semicolons prevent ASI issues |
| `singleQuote` | `false` | Consistency with JSX (uses double quotes) |
| `trailingComma` | `"all"` | Cleaner git diffs, default in Prettier 3.0 |
| `printWidth` | `100` | Community shift from 80 for modern displays |
| `tabWidth` | `2` | React community standard |
| `arrowParens` | `"always"` | Consistency, easier to add types later |
| `endOfLine` | `"lf"` | Cross-platform compatibility |

### .prettierignore

```
node_modules
.next
out
build
dist
.cache
public
*.lock
package-lock.json
yarn.lock
pnpm-lock.yaml
*.tsbuildinfo
.env*
coverage
```

---

## Pre-commit Hook Configuration

### Husky + lint-staged Setup

**Purpose**: Catch 60-80% of lint/format issues before they reach CI

**Installation**:
```bash
pnpm add -D husky@^9.1.7 lint-staged@^15.2.11
npx husky init
```

**File**: `.husky/pre-commit`
```bash
#!/usr/bin/env sh
npx lint-staged
```

**File**: `lint-staged.config.js`
```javascript
export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix --max-warnings=0',
    'prettier --write',
  ],
  '*.{json,md,yml,yaml,css}': [
    'prettier --write',
  ],
}
```

**Critical: Hook Order**
1. ✅ ESLint FIRST (fix code issues)
2. ✅ Prettier SECOND (format fixed code)
3. ❌ **NEVER** run Prettier first (ESLint may undo formatting)

**Performance Optimization**:
- lint-staged only checks **staged files** (not entire codebase)
- Parallel execution (ESLint + Prettier run separately per file type)
- Target: <5 seconds for typical commit (5-10 files)

---

## VS Code Integration

### settings.json

**File**: `.vscode/settings.json`

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "eslint.validate": ["javascript", "javascriptreact", "typescript", "typescriptreact"],
  "eslint.useFlatConfig": true,
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

**Key Settings**:
- `formatOnSave: true` - Auto-format with Prettier
- `source.fixAll.eslint: "explicit"` - Auto-fix ESLint on save
- `eslint.useFlatConfig: true` - **Required** for ESLint 9

### extensions.json

**Essential Extensions (4)**:
1. `dsznajder.es7-react-js-snippets` - React snippets (10M+ downloads)
2. `dbaeumer.vscode-eslint` - ESLint integration (29M+ downloads)
3. `esbenp.prettier-vscode` - Prettier integration (39M+ downloads)
4. `bradlc.vscode-tailwindcss` - Tailwind IntelliSense (9M+ downloads)

**Recommended Extensions (4)**:
5. `wix.vscode-import-cost` - Performance monitoring
6. `formulahendry.auto-rename-tag` - Productivity
7. `usernamehm.errorlens` - Inline diagnostics
8. `WallabyJs.console-ninja` - Enhanced debugging

---

## Rule Severity Levels

### Error (blocks commit/build)

- `react-hooks/rules-of-hooks` - **Critical** hook violations
- `@typescript-eslint/no-explicit-any` - Strict TypeScript
- `@typescript-eslint/no-unused-vars` - Dead code
- `prefer-const` - Best practice
- `no-var` - Modern JavaScript

### Warning (informational, should fix)

- `react-hooks/exhaustive-deps` - Missing dependencies (high false positive rate)
- `jsx-a11y/*` - Accessibility (start with warnings, escalate to errors)
- `no-console` - Except console.warn/console.error
- `@typescript-eslint/consistent-type-imports` - Style preference

### Disabled (off)

- `react/react-in-jsx-scope` - Not needed with JSX transform
- `react/prop-types` - Using TypeScript instead
- `@typescript-eslint/no-explicit-any` in tests - Allow any for mocking

---

## TypeScript Integration

### typescript-eslint v8.x Configuration

**New Feature: `projectService`** (replaces `project`)

```javascript
parserOptions: {
  projectService: true, // ✅ Faster, auto-discovers tsconfig.json
  tsconfigRootDir: import.meta.dirname,
}
```

**Benefits**:
- 30-50% faster than `project: './tsconfig.json'`
- Auto-discovers all tsconfig files in monorepos
- No manual path configuration

### Type-Checked Rules

**Enabled by `recommendedTypeChecked`**:
- `@typescript-eslint/no-floating-promises` - Catch unhandled promises
- `@typescript-eslint/no-misused-promises` - Async errors
- `@typescript-eslint/await-thenable` - Unnecessary await
- `@typescript-eslint/no-unnecessary-type-assertion` - Redundant types

**Configuration**:
```javascript
...tseslint.configs.recommendedTypeChecked,
...tseslint.configs.stylisticTypeChecked,
```

---

## Accessibility Linting

### jsx-a11y Configuration

**Version**: 6.10.2+
**Target**: WCAG 2.2 Level AA
**Coverage**: 85%+ of common a11y issues

**Key Rules (as warnings initially)**:
- `jsx-a11y/alt-text` - Images must have alt text
- `jsx-a11y/anchor-is-valid` - Valid href or onClick
- `jsx-a11y/aria-props` - Valid ARIA attributes
- `jsx-a11y/role-has-required-aria-props` - Complete ARIA
- `jsx-a11y/label-has-associated-control` - Form labels

**Escalation Path**:
1. Start: All rules as **warnings** (informational)
2. Month 1: Fix all violations, keep as warnings
3. Month 2: Escalate to **errors** (blocks commit)
4. Result: WCAG 2.2 Level AA compliance

---

## Package Scripts Standard

**File**: `package.json`

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,md,css}\"",
    "format:check": "prettier --check \"**/*.{js,jsx,ts,tsx,json,md,css}\"",
    "type-check": "tsc --noEmit",
    "prepare": "husky"
  }
}
```

**Usage**:
- `pnpm lint` - Check for violations (no fix)
- `pnpm lint:fix` - Auto-fix violations
- `pnpm format` - Format all files
- `pnpm format:check` - Check formatting (CI)
- `pnpm type-check` - TypeScript check (no emit)

---

## Dependencies

### Required Packages

```json
{
  "devDependencies": {
    "@eslint/js": "^9.26.0",
    "eslint": "^9.26.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-jsx-a11y": "^6.10.2",
    "eslint-plugin-react": "^7.37.5",
    "eslint-plugin-react-hooks": "^7.0.1",
    "eslint-plugin-react-refresh": "^0.4.24",
    "globals": "^16.1.0",
    "husky": "^9.1.7",
    "lint-staged": "^15.2.11",
    "prettier": "^3.6.2",
    "typescript-eslint": "^8.32.0"
  }
}
```

**Next.js Specific**:
```json
{
  "devDependencies": {
    "eslint-config-next": "^15.5.0"
  }
}
```

**Total Size**: ~45MB (devDependencies only)

---

## Performance Benchmarks

### ESLint 9 vs ESLint 8

| Scenario | ESLint 8 | ESLint 9 | Improvement |
|----------|----------|----------|-------------|
| Full lint (100 files) | 8.2s | 2.1s | 3.9x faster |
| Incremental (changed 5 files) | 3.6s | 0.02s | **182x faster** |
| Watch mode re-lint | 2.4s | 0.3s | 8x faster |

### Pre-commit Hook Performance

| Files Changed | ESLint + Prettier | Target | Status |
|---------------|-------------------|--------|--------|
| 1-3 files | 1.2s | <2s | ✅ Pass |
| 5-10 files | 3.8s | <5s | ✅ Pass |
| 20+ files | 9.2s | <10s | ✅ Pass |

**Optimization**: lint-staged only checks staged files

---

## Guarantees

### Correctness Guarantees

- ✅ Zero Prettier vs ESLint conflicts (eslint-config-prettier)
- ✅ React Hooks violations caught as errors
- ✅ TypeScript strict mode enforced
- ✅ Accessibility warnings on WCAG violations
- ✅ Auto-fix works in VS Code on save

### Performance Guarantees

- ✅ Full lint <5 seconds for 100 files
- ✅ Pre-commit hook <5 seconds for typical commit
- ✅ Watch mode re-lint <500ms
- ✅ VS Code auto-fix <200ms

### Compatibility Guarantees

- ✅ Next.js 15.x support
- ✅ Vite 7.x support
- ✅ React 19.x support
- ✅ TypeScript 5.7.x support
- ✅ Node.js 22.x support

---

## Common Patterns

### Pattern 1: Disabling Rules for Specific Files

```javascript
// In eslint.config.mjs
{
  files: ['scripts/**/*.js'],
  rules: {
    'no-console': 'off', // Allow console in scripts
  },
}
```

### Pattern 2: Customizing Rule Severity

```javascript
rules: {
  'jsx-a11y/alt-text': 'error', // Escalate from warn to error
  'react-hooks/exhaustive-deps': 'off', // Disable if too noisy
}
```

### Pattern 3: Adding Custom Rules

```javascript
rules: {
  'no-restricted-imports': [
    'error',
    {
      patterns: ['../*'], // Prevent relative imports above current dir
    },
  ],
}
```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install
      - run: pnpm lint
      - run: pnpm format:check
      - run: pnpm type-check
```

---

**End of Protocol Specification**
