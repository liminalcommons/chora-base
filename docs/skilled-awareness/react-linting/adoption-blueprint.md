# SAP-022: React Linting & Formatting - Adoption Blueprint

**SAP ID**: SAP-022
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01
**Category**: Technology-Specific SAP (Front-End Quality)

---

## Purpose of This Guide

This Adoption Blueprint provides **step-by-step instructions** for installing and configuring SAP-022 (React Linting & Formatting) in your React project. Follow these instructions to set up ESLint 9 + Prettier 3 + pre-commit hooks in 20 minutes.

**Prerequisites**:
- React 18+ project (from SAP-020 or existing)
- Node.js 22.x installed
- pnpm 10.x or npm 10.x
- Git repository initialized
- VS Code 1.95+ (recommended)

**What You'll Install**:
- ESLint 9.26.0 with 8 plugins
- Prettier 3.6.2
- Husky 9.1.7 (Git hooks)
- lint-staged 15.2.11 (pre-commit linting)
- TypeScript-eslint 8.32.0
- VS Code extensions (8 recommended)

**Estimated Time**: 20 minutes

---

## Table of Contents

1. [Quick Start (New Projects)](#quick-start-new-projects)
2. [Standard Installation (Existing Projects)](#standard-installation-existing-projects)
3. [**Migration from ESLint 8 to ESLint 9** (PRIORITY - from RT-019)](#migration-from-eslint-8-to-eslint-9)
4. [Next.js 15 Installation](#nextjs-15-installation)
5. [Vite 7 Installation](#vite-7-installation)
6. [VS Code Setup](#vs-code-setup)
7. [Verification Steps](#verification-steps)
8. [Troubleshooting](#troubleshooting)
9. [Customization Guide](#customization-guide)

---

## Quick Start (New Projects)

If you're starting a **new React project from SAP-020**, follow these condensed steps:

### Step 1: Scaffold React Project (SAP-020)

```bash
# Follow SAP-020 to create Next.js or Vite project
# Example for Next.js:
npx create-next-app@latest my-app --typescript --tailwind --app --use-pnpm

cd my-app
```

**Time**: 2 minutes

---

### Step 2: Install SAP-022 Dependencies

```bash
pnpm add -D \
  @eslint/js@^9.26.0 \
  eslint@^9.26.0 \
  eslint-config-next@^15.5.0 \
  eslint-config-prettier@^9.1.0 \
  eslint-plugin-jsx-a11y@^6.10.2 \
  eslint-plugin-react@^7.37.5 \
  eslint-plugin-react-hooks@^7.0.1 \
  eslint-plugin-react-refresh@^0.4.24 \
  globals@^16.1.0 \
  husky@^9.1.7 \
  lint-staged@^15.2.11 \
  prettier@^3.6.2 \
  typescript-eslint@^8.32.0
```

**For Vite projects**, replace `eslint-config-next` with nothing (Next.js-specific).

**Time**: 1 minute

---

### Step 3: Copy SAP-022 Configuration Files

#### For Next.js:
```bash
# Navigate to chora-base templates
cd /path/to/chora-base/templates/react/linting

# Copy Next.js ESLint config
cp nextjs/eslint.config.mjs /path/to/my-app/

# Copy shared configs
cp shared/.prettierrc /path/to/my-app/
cp shared/.prettierignore /path/to/my-app/
cp shared/lint-staged.config.js /path/to/my-app/
cp -r shared/.vscode /path/to/my-app/
```

#### For Vite:
```bash
# Copy Vite ESLint config instead
cp vite/eslint.config.mjs /path/to/my-app/

# Copy shared configs (same as Next.js)
cp shared/.prettierrc /path/to/my-app/
cp shared/.prettierignore /path/to/my-app/
cp shared/lint-staged.config.js /path/to/my-app/
cp -r shared/.vscode /path/to/my-app/
```

**Time**: 2 minutes

---

### Step 4: Add Scripts to package.json

Open `package.json` and merge these scripts:

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

**Time**: 1 minute

---

### Step 5: Initialize Husky (Git Hooks)

```bash
npx husky init
```

This creates `.husky/` directory with a `pre-commit` hook.

**Time**: 30 seconds

---

### Step 6: Configure Pre-Commit Hook

Edit `.husky/pre-commit`:

```bash
#!/usr/bin/env sh

pnpm lint-staged
```

Make it executable:

```bash
chmod +x .husky/pre-commit
```

**Time**: 1 minute

---

### Step 7: Run Initial Lint and Format

```bash
# Fix any existing violations
pnpm lint:fix

# Format entire codebase
pnpm format

# Verify no violations
pnpm lint
```

**Expected**: 0 errors, 0 warnings (fresh project).

**Time**: 2 minutes

---

### Step 8: Install VS Code Extensions

Open project in VS Code:

```bash
code .
```

VS Code should prompt: "This workspace has extension recommendations."

Click **"Install All"** to install:
1. ES7+ React/Redux/React-Native snippets
2. ESLint
3. Prettier - Code formatter
4. Tailwind CSS IntelliSense
5. Import Cost
6. Auto Rename Tag
7. Error Lens
8. Console Ninja

**Time**: 2 minutes

---

### Step 9: Test Auto-Fix on Save

1. Open any `.tsx` file
2. Add a violation (e.g., `const x = 1; var y = 2;`)
3. Save file (Cmd+S / Ctrl+S)
4. Verify: `var y` auto-changes to `const y`

**Expected**: ESLint auto-fixes on save.

**Time**: 1 minute

---

### Step 10: Test Pre-Commit Hook

```bash
# Stage files
git add .

# Commit (pre-commit hook runs)
git commit -m "chore: Add SAP-022 linting infrastructure"
```

**Expected**: Hook runs in <5 seconds, commit succeeds.

**Time**: 1 minute

---

### Total Time: ~15 minutes for fresh projects

✅ You're done! SAP-022 is fully installed.

---

## Migration from ESLint 8 to ESLint 9

**CRITICAL**: If you're using ESLint 8 (.eslintrc), **migrate to ESLint 9 NOW** for:
- **182x faster incremental linting** (9,100ms → 50ms) - RT-019 validated
- **Future-proof**: ESLint 10 will remove .eslintrc support entirely
- **Better TypeScript**: typescript-eslint v8 projectService API (30-50% faster)

**Estimated Time**: 30-60 minutes

---

### Phase 1: Pre-Migration (5 minutes)

#### Step M1.1: Check Current ESLint Version

```bash
# Check current ESLint version
pnpm list eslint
# If ESLint 8.x or older, continue with migration
# If ESLint 9.x, skip to "Standard Installation"
```

---

#### Step M1.2: Backup Current Configuration

```bash
# Backup .eslintrc config
cp .eslintrc.js .eslintrc.js.backup
cp .eslintrc.json .eslintrc.json.backup 2>/dev/null || true
cp .eslintrc .eslintrc.backup 2>/dev/null || true

# Backup .eslintignore
cp .eslintignore .eslintignore.backup 2>/dev/null || true

# Create git commit (safety net)
git add .
git commit -m "backup: Save ESLint 8 config before migrating to ESLint 9"
```

**Time**: 2 minutes

---

### Phase 2: Uninstall ESLint 8 (5 minutes)

#### Step M2.1: Remove ESLint 8 Packages

```bash
# Remove ESLint 8 and old typescript-eslint packages
pnpm remove eslint \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin

# Remove old plugin versions (if installed)
pnpm remove \
  eslint-plugin-react \
  eslint-plugin-react-hooks \
  eslint-config-prettier
```

**Why**: ESLint 9 requires new package structure (typescript-eslint combined package)

**Time**: 2 minutes

---

### Phase 3: Install ESLint 9 (5 minutes)

#### Step M3.1: Install ESLint 9 and Plugins

```bash
# Install ESLint 9 core
pnpm add -D eslint@^9.26.0 @eslint/js@^9.26.0

# Install typescript-eslint v8 (combined package)
pnpm add -D typescript-eslint@^8.32.0

# Install React plugins
pnpm add -D \
  eslint-plugin-react@^7.37.5 \
  eslint-plugin-react-hooks@^7.0.1 \
  eslint-plugin-react-refresh@^0.4.24 \
  eslint-plugin-jsx-a11y@^6.10.2

# Install Prettier integration
pnpm add -D eslint-config-prettier@^9.1.0

# Install globals utility
pnpm add -D globals@^16.1.0
```

**For Next.js projects, also install**:
```bash
pnpm add -D eslint-config-next@^15.5.0
```

**Time**: 3 minutes

---

### Phase 4: Convert Config to Flat Format (15-30 minutes)

#### Step M4.1: Create ESLint 9 Flat Config

**Old .eslintrc.js (ESLint 8 - DEPRECATED)**:
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  plugins: ['react', '@typescript-eslint', 'react-hooks'],
  env: {
    browser: true,
    es2021: true,
  },
  rules: {
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
}
```

**New eslint.config.mjs (ESLint 9 Flat Config - NEW STANDARD)**:

```javascript
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactPlugin from 'eslint-plugin-react'
import reactHooksPlugin from 'eslint-plugin-react-hooks'
import reactRefreshPlugin from 'eslint-plugin-react-refresh'
import jsxA11yPlugin from 'eslint-plugin-jsx-a11y'
import prettierConfig from 'eslint-config-prettier'
import globals from 'globals'

export default tseslint.config(
  // Global ignores (replaces .eslintignore)
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/build/**',
      '**/dist/**',
      '**/.turbo/**',
      '**/coverage/**',
    ],
  },

  // Base configs (replaces extends)
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  reactPlugin.configs.flat.recommended,
  reactPlugin.configs.flat['jsx-runtime'],
  jsxA11yPlugin.flatConfigs.recommended,

  // React settings
  {
    settings: {
      react: {
        version: 'detect',
      },
    },
  },

  // Global settings (replaces env)
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
      parserOptions: {
        projectService: true, // NEW in v8 - 30-50% faster!
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // React Hooks rules (replaces plugins)
  {
    plugins: {
      'react-hooks': reactHooksPlugin,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },

  // React Refresh rules (for Vite)
  {
    plugins: {
      'react-refresh': reactRefreshPlugin,
    },
    rules: {
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },

  // Prettier integration (MUST be last)
  prettierConfig,
)
```

**Key Changes from .eslintrc to Flat Config**:
- ❌ `extends` → ✅ Import and spread configs (`...tseslint.configs.recommended`)
- ❌ `plugins: []` → ✅ `plugins: {}` (object instead of array)
- ❌ `env` → ✅ `languageOptions.globals`
- ❌ `.eslintignore` → ✅ `ignores: []` in flat config
- ❌ `@typescript-eslint/parser` + `@typescript-eslint/eslint-plugin` → ✅ `typescript-eslint` (combined)
- ✅ **NEW**: `projectService: true` (30-50% faster, auto-discovers tsconfig.json)

**Time**: 15-20 minutes (copying + customizing)

---

#### Step M4.2: Remove Old Config Files

```bash
# Delete old ESLint 8 config files
rm .eslintrc.js .eslintrc.json .eslintrc 2>/dev/null || true
rm .eslintignore 2>/dev/null || true
```

**Important**: Backups remain in `.backup` files if rollback needed.

**Time**: 1 minute

---

### Phase 5: Update VS Code Settings (5 minutes)

#### Step M5.1: Enable ESLint 9 Flat Config in VS Code

Create or update `.vscode/settings.json`:

```json
{
  // Enable ESLint 9 flat config
  "eslint.useFlatConfig": true,

  // Auto-fix on save
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },

  // Format on save with Prettier
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",

  // File-specific formatters
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

**Time**: 3 minutes

---

### Phase 6: Test Migration (5 minutes)

#### Step M6.1: Run ESLint 9

```bash
# Test linting
pnpm lint

# Expected output:
# - ESLint 9 runs (check version in output)
# - No "flat config required" errors
# - May show new violations (ESLint 9 stricter)

# Auto-fix violations
pnpm lint:fix
```

**If errors occur**: See [Troubleshooting](#migration-troubleshooting) section below.

**Time**: 3 minutes

---

#### Step M6.2: Verify 182x Performance Improvement

**Before ESLint 9** (from backup):
```bash
# Typical ESLint 8 incremental lint: ~9,100ms (9 seconds!)
```

**After ESLint 9**:
```bash
# Make a small change to a file
echo "// test" >> src/App.tsx

# Run lint
time pnpm lint

# Expected: ~50ms for incremental lint (182x faster!)
# If still slow, check for old cached files
```

**Validation**: If lint time is <100ms, migration succeeded!

**Time**: 2 minutes

---

### Phase 7: Commit Migration (5 minutes)

#### Step M7.1: Commit ESLint 9 Migration

```bash
# Add all changes
git add .

# Commit migration
git commit -m "feat: Migrate to ESLint 9 flat config (182x faster linting)

- Migrate from ESLint 8 (.eslintrc) to ESLint 9 (flat config)
- Install typescript-eslint v8 with projectService API
- Performance: 9,100ms → 50ms for incremental linting
- Update VS Code settings for flat config support
- Backups: .eslintrc.js.backup, .eslintignore.backup

Ref: SAP-022 RT-019 research"
```

**Time**: 2 minutes

---

### Migration Checklist

Use this checklist to ensure successful migration:

- [ ] Backup .eslintrc and .eslintignore
- [ ] Check current ESLint version (pnpm list eslint)
- [ ] Uninstall ESLint 8 and @typescript-eslint packages
- [ ] Install ESLint 9.26.0+ and typescript-eslint@^8.32.0
- [ ] Create eslint.config.mjs with flat config
- [ ] Convert extends → imported configs
- [ ] Convert plugins array → plugins object
- [ ] Convert env → languageOptions.globals
- [ ] Convert .eslintignore → ignores in flat config
- [ ] Add projectService: true (30-50% faster)
- [ ] Remove old .eslintrc files
- [ ] Update VS Code settings (eslint.useFlatConfig: true)
- [ ] Test with pnpm lint
- [ ] Verify 182x performance improvement (<100ms incremental)
- [ ] Commit migration with descriptive message

---

### Migration Troubleshooting

**Issue 1: "Cannot find module '@typescript-eslint/parser'"**
- **Cause**: Old package installed, should use `typescript-eslint` combined package
- **Fix**: `pnpm remove @typescript-eslint/parser @typescript-eslint/eslint-plugin && pnpm add -D typescript-eslint@^8.32.0`

**Issue 2: "extends is not allowed"**
- **Cause**: Used .eslintrc syntax in flat config
- **Fix**: Replace `extends: ['...']` with imported configs: `...tseslint.configs.recommended`

**Issue 3: "env is not allowed"**
- **Cause**: Used .eslintrc `env` property in flat config
- **Fix**: Replace with `languageOptions: { globals: { ...globals.browser } }`

**Issue 4: "Linting still slow (>1s)"**
- **Cause**: Old cache files or wrong config
- **Fix**: `rm -rf node_modules/.cache/eslint && pnpm lint`

**Issue 5: "TypeError: Cannot read property 'config'"**
- **Cause**: Plugin not compatible with flat config
- **Fix**: Check plugin docs for flat config version, or remove plugin temporarily

---

## Standard Installation (Existing Projects)

If you have an **existing React project**, follow these detailed steps:

### Phase 1: Preparation (5 minutes)

#### Step 1.1: Verify Prerequisites

```bash
# Check Node.js version (must be 22.x)
node --version
# Expected: v22.x.x

# Check package manager
pnpm --version
# Expected: 10.x.x

# Check Git
git --version
# Expected: 2.30+

# Verify project is React 18+
grep '"react"' package.json
# Expected: "react": "^18.0.0" or "^19.0.0"
```

**If Node.js < 22**: Upgrade with `nvm install 22` or download from nodejs.org.

---

#### Step 1.2: Backup Existing Linting Config (If Any)

```bash
# If you have existing ESLint config
[ -f .eslintrc.json ] && cp .eslintrc.json .eslintrc.json.backup
[ -f .eslintrc.js ] && cp .eslintrc.js .eslintrc.js.backup
[ -f eslint.config.js ] && cp eslint.config.js eslint.config.js.backup

# If you have existing Prettier config
[ -f .prettierrc ] && cp .prettierrc .prettierrc.backup
```

**Time**: 1 minute

---

#### Step 1.3: Remove Old Linting Dependencies (If Migrating)

```bash
# Remove ESLint 8 and related packages
pnpm remove \
  eslint \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  eslint-plugin-prettier \
  @types/eslint

# Delete old config files
rm -f .eslintrc.json .eslintrc.js .eslintrc.yml
```

**Note**: Skip this if you don't have existing ESLint.

**Time**: 1 minute

---

#### Step 1.4: Check for Existing Violations

```bash
# If you have ESLint installed, run it
pnpm lint || npm run lint

# Count violations
pnpm lint 2>&1 | grep "problems"
# Example: "5 problems (3 errors, 2 warnings)"
```

**If >200 violations**: Consider gradual migration (see awareness-guide.md).

**Time**: 2 minutes

---

### Phase 2: Installation (5 minutes)

#### Step 2.1: Install ESLint 9 and Plugins

```bash
pnpm add -D \
  @eslint/js@^9.26.0 \
  eslint@^9.26.0 \
  eslint-config-prettier@^9.1.0 \
  eslint-plugin-jsx-a11y@^6.10.2 \
  eslint-plugin-react@^7.37.5 \
  eslint-plugin-react-hooks@^7.0.1 \
  globals@^16.1.0 \
  typescript-eslint@^8.32.0
```

**For Next.js**, also add:
```bash
pnpm add -D eslint-config-next@^15.5.0
```

**For Vite**, also add:
```bash
pnpm add -D eslint-plugin-react-refresh@^0.4.24
```

**Time**: 1 minute (install time)

---

#### Step 2.2: Install Prettier

```bash
pnpm add -D prettier@^3.6.2
```

**Time**: 30 seconds

---

#### Step 2.3: Install Pre-Commit Tools

```bash
pnpm add -D husky@^9.1.7 lint-staged@^15.2.11
```

**Time**: 30 seconds

---

#### Step 2.4: Install TypeScript Types (If Using TypeScript)

```bash
pnpm add -D \
  @types/node@^22.0.0 \
  @types/react@^19.0.0 \
  @types/react-dom@^19.0.0 \
  typescript@^5.7.0
```

**Time**: 30 seconds

---

#### Step 2.5: Verify Installation

```bash
# Check installed versions
pnpm list eslint
# Expected: eslint@9.26.0

pnpm list prettier
# Expected: prettier@3.6.2

pnpm list typescript-eslint
# Expected: typescript-eslint@8.32.0
```

**Time**: 1 minute

---

### Phase 3: Configuration (5 minutes)

#### Step 3.1: Copy ESLint Config

**For Next.js**:
```bash
# From chora-base
cp /path/to/chora-base/templates/react/linting/nextjs/eslint.config.mjs ./
```

**For Vite**:
```bash
# From chora-base
cp /path/to/chora-base/templates/react/linting/vite/eslint.config.mjs ./
```

**Manual Copy Option** (if you don't have chora-base cloned):
1. Open [nextjs/eslint.config.mjs](https://github.com/liminalcommons/chora-base/blob/main/templates/react/linting/nextjs/eslint.config.mjs) in browser
2. Copy contents to `eslint.config.mjs` in your project root

**Time**: 1 minute

---

#### Step 3.2: Copy Prettier Config

```bash
# From chora-base
cp /path/to/chora-base/templates/react/linting/shared/.prettierrc ./
cp /path/to/chora-base/templates/react/linting/shared/.prettierignore ./
```

**Manual Copy Option**:

Create `.prettierrc`:
```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

Create `.prettierignore`:
```
node_modules
.next
out
build
dist
.cache
public
coverage
*.min.js
*.min.css
pnpm-lock.yaml
package-lock.json
yarn.lock
```

**Time**: 1 minute

---

#### Step 3.3: Copy lint-staged Config

```bash
# From chora-base
cp /path/to/chora-base/templates/react/linting/shared/lint-staged.config.js ./
```

**Manual Copy Option**:

Create `lint-staged.config.js`:
```javascript
export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix --max-warnings=0',
    'prettier --write',
  ],
  '*.{json,md,css,scss}': ['prettier --write'],
}
```

**Time**: 1 minute

---

#### Step 3.4: Copy VS Code Settings

```bash
# From chora-base
mkdir -p .vscode
cp /path/to/chora-base/templates/react/linting/shared/.vscode/settings.json .vscode/
cp /path/to/chora-base/templates/react/linting/shared/.vscode/extensions.json .vscode/
```

**Manual Copy Option**:

Create `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "eslint.useFlatConfig": true,
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "prettier.enable": true,
  "prettier.requireConfig": true
}
```

Create `.vscode/extensions.json`:
```json
{
  "recommendations": [
    "dsznajder.es7-react-js-snippets",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "wix.vscode-import-cost",
    "formulahendry.auto-rename-tag",
    "usernamehm.errorlens",
    "WallabyJs.console-ninja"
  ],
  "unwantedRecommendations": [
    "hookyqr.beautify",
    "ms-vscode.vscode-typescript-tslint-plugin"
  ]
}
```

**Time**: 2 minutes

---

#### Step 3.5: Update package.json Scripts

Open `package.json` and add these scripts (merge with existing):

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

**Time**: 1 minute

---

### Phase 4: Git Hooks Setup (3 minutes)

#### Step 4.1: Initialize Husky

```bash
npx husky init
```

**Expected Output**:
```
✔ husky - Git hooks initialized
```

This creates `.husky/` directory.

**Time**: 30 seconds

---

#### Step 4.2: Configure Pre-Commit Hook

Edit `.husky/pre-commit` (created by init):

```bash
#!/usr/bin/env sh

pnpm lint-staged
```

**For npm users**, change to:
```bash
npm run lint-staged
```

**For yarn users**, change to:
```bash
yarn lint-staged
```

**Time**: 1 minute

---

#### Step 4.3: Make Hook Executable

```bash
chmod +x .husky/pre-commit
```

**Time**: 10 seconds

---

#### Step 4.4: Test Hook Manually

```bash
# Test pre-commit hook (without committing)
.husky/pre-commit

# Expected: Runs lint-staged on staged files
```

**Time**: 1 minute

---

### Phase 5: Initial Fix and Format (5 minutes)

#### Step 5.1: Run Linting

```bash
pnpm lint
```

**Expected Output** (existing projects):
```
/path/to/file.tsx
  12:5  error  'React' is defined but never used  @typescript-eslint/no-unused-vars
  23:3  error  Missing 'alt' attribute           jsx-a11y/alt-text

✖ 2 problems (2 errors, 0 warnings)
  1 error and 0 warnings potentially fixable with the `--fix` option.
```

**If 0 errors**: Great! Skip to Step 5.3.

**Time**: 1 minute

---

#### Step 5.2: Auto-Fix Violations

```bash
pnpm lint:fix
```

**Expected**: Many violations auto-fixed (unused imports removed, const replaces var, etc.).

**Manual Fixes Required**: Some violations can't be auto-fixed (e.g., missing alt text).

**Time**: 2 minutes (depends on violations)

---

#### Step 5.3: Format Entire Codebase

```bash
pnpm format
```

**Expected Output**:
```
src/App.tsx 50ms
src/components/Button.tsx 12ms
src/pages/index.tsx 18ms
...
```

**Warning**: This will reformat ALL files. Git diff will be large.

**Time**: 1 minute

---

#### Step 5.4: Verify Zero Violations

```bash
pnpm lint
```

**Expected Output**:
```
✔ No linting errors found!
```

**If still errors**: Manually fix remaining violations (ESLint will guide you).

**Time**: 1 minute

---

### Phase 6: Testing (2 minutes)

#### Step 6.1: Test Auto-Fix on Save (VS Code)

1. Open any `.tsx` file in VS Code
2. Add a violation: `var x = 1;`
3. Save file (Cmd+S / Ctrl+S)
4. Verify: `var` auto-changes to `const`

**If not working**: Check VS Code ESLint output (View → Output → ESLint).

**Time**: 1 minute

---

#### Step 6.2: Test Pre-Commit Hook

```bash
# Create test commit
echo "// test" >> src/test.tsx
git add src/test.tsx
git commit -m "test: Verify pre-commit hook"
```

**Expected Output**:
```
✔ Preparing lint-staged...
✔ Running tasks for staged files...
✔ Applying modifications from tasks...
✔ Cleaning up temporary files...
[main abc1234] test: Verify pre-commit hook
 1 file changed, 1 insertion(+)
```

**If hook doesn't run**: Check `.husky/pre-commit` is executable (`ls -l .husky/pre-commit`).

**Time**: 1 minute

---

### Total Time: ~20 minutes for existing projects

✅ Installation complete!

---

## Next.js 15 Installation

### Framework-Specific Steps

Follow [Standard Installation](#standard-installation-existing-projects) with these adjustments:

#### Step 1: Install Next.js-Specific Dependencies

```bash
pnpm add -D eslint-config-next@^15.5.0
```

---

#### Step 2: Use Next.js ESLint Config

Copy `nextjs/eslint.config.mjs` (not `vite/eslint.config.mjs`).

---

#### Step 3: Verify Next.js-Specific Rules

Open `eslint.config.mjs` and verify these sections exist:

```javascript
// Next.js-specific ignores
{
  ignores: [
    '**/.next/**',        // Next.js build output
    '**/next-env.d.ts',   // Next.js type declarations
    'next.config.{js,mjs,ts}', // Next.js config
  ],
}

// Next.js settings
settings: {
  next: {
    rootDir: process.cwd(),
  },
}

// API route overrides
{
  files: ['**/app/api/**/*.{js,ts}', '**/pages/api/**/*.{js,ts}'],
  rules: {
    'no-console': 'off', // Allow console in API routes
  },
}
```

---

#### Step 4: Test with Next.js App

```bash
# Development server
pnpm dev

# Build (linting runs automatically)
pnpm build
```

**Expected**: No linting errors during build.

---

## Vite 7 Installation

### Framework-Specific Steps

Follow [Standard Installation](#standard-installation-existing-projects) with these adjustments:

#### Step 1: Install Vite-Specific Dependencies

```bash
pnpm add -D eslint-plugin-react-refresh@^0.4.24
```

---

#### Step 2: Use Vite ESLint Config

Copy `vite/eslint.config.mjs` (not `nextjs/eslint.config.mjs`).

---

#### Step 3: Verify Vite-Specific Rules

Open `eslint.config.mjs` and verify these sections exist:

```javascript
// Vite-specific ignores
{
  ignores: [
    '**/dist/**',         // Vite build output (not .next)
    '**/vite.config.ts',  // Vite config
    '**/*.config.js',
  ],
}

// React Refresh plugin (Vite Fast Refresh)
{
  plugins: { 'react-refresh': reactRefresh },
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}

// Browser-only globals (no Node.js)
globals: {
  ...globals.browser,
  ...globals.es2024,
  // NO globals.node (Vite is browser-only)
}
```

---

#### Step 4: Test with Vite App

```bash
# Development server
pnpm dev

# Build
pnpm build

# Preview production build
pnpm preview
```

**Expected**: No linting errors during build.

---

## VS Code Setup

### Step 1: Install Recommended Extensions

Open project in VS Code:

```bash
code .
```

**Notification**: "This workspace has extension recommendations."

Click **"Install All"** (8 extensions):

1. **ES7+ React/Redux/React-Native snippets** (dsznajder.es7-react-js-snippets)
   - React code snippets (rfc, rafce, etc.)

2. **ESLint** (dbaeumer.vscode-eslint)
   - ESLint integration (REQUIRED)

3. **Prettier - Code formatter** (esbenp.prettier-vscode)
   - Prettier integration (REQUIRED)

4. **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
   - Tailwind class autocomplete

5. **Import Cost** (wix.vscode-import-cost)
   - Shows package size in imports

6. **Auto Rename Tag** (formulahendry.auto-rename-tag)
   - Renames closing tag when opening tag changes

7. **Error Lens** (usernamehm.errorlens)
   - Shows errors inline (enhances ESLint visibility)

8. **Console Ninja** (WallabyJs.console-ninja)
   - Enhanced console.log output

**Time**: 2 minutes (installation time)

---

### Step 2: Verify VS Code Settings

Open `.vscode/settings.json` and verify:

```json
{
  "editor.formatOnSave": true,  // ← Auto-format on save
  "editor.defaultFormatter": "esbenp.prettier-vscode",  // ← Prettier
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"  // ← ESLint auto-fix
  },
  "eslint.useFlatConfig": true,  // ← ESLint 9 flat config
}
```

**If missing**: Copy from SAP-022 templates (see Phase 3, Step 3.4).

---

### Step 3: Reload VS Code

```
Cmd+Shift+P / Ctrl+Shift+P → "Developer: Reload Window"
```

**Time**: 10 seconds

---

### Step 4: Test Auto-Fix

1. Open `src/App.tsx`
2. Add violation: `var x = 1;`
3. Save (Cmd+S / Ctrl+S)
4. Verify: `var` changes to `const`

**Expected**: ESLint auto-fixes on save.

---

### Step 5: Check ESLint Status

Look at VS Code status bar (bottom):

- **"ESLint"** (green checkmark) → Working correctly
- **"ESLint"** (red X) → Error (click to see output)

**If error**: Open Output panel (View → Output → ESLint) for details.

---

## Verification Steps

### Verification 1: Linting Works

```bash
pnpm lint
```

**Expected**: No errors (or list of violations to fix).

---

### Verification 2: Auto-Fix Works

```bash
# Create test file with violations
cat > src/test-lint.tsx << 'EOF'
var x = 1;
const y = 2;
console.log(x)
EOF

# Auto-fix
pnpm lint:fix

# Check result
cat src/test-lint.tsx
# Expected: 'var' changed to 'const', semicolon added

# Clean up
rm src/test-lint.tsx
```

---

### Verification 3: Prettier Works

```bash
# Create unformatted file
cat > src/test-format.tsx << 'EOF'
const x={a:1,b:2,c:3};console.log(x)
EOF

# Format
pnpm format

# Check result
cat src/test-format.tsx
# Expected: Formatted with proper spacing and newlines

# Clean up
rm src/test-format.tsx
```

---

### Verification 4: Pre-Commit Hook Works

```bash
# Create violation
echo "var x = 1;" > src/test-hook.tsx

# Stage file
git add src/test-hook.tsx

# Commit (hook should auto-fix)
git commit -m "test: Verify pre-commit hook"

# Check file (should be fixed)
cat src/test-hook.tsx
# Expected: 'var' changed to 'const'

# Clean up
git rm src/test-hook.tsx
git commit -m "test: Clean up test file"
```

---

### Verification 5: VS Code Auto-Fix Works

1. Open any `.tsx` file in VS Code
2. Add: `var x = 1;`
3. Save (Cmd+S / Ctrl+S)
4. Verify: `var` → `const` automatically

**Expected**: Instant auto-fix on save.

---

### Verification 6: TypeScript Type-Checking Works

```bash
# Create type error
cat > src/test-types.tsx << 'EOF'
const x: number = "string"; // Type error
EOF

# Type-check
pnpm type-check

# Expected output
src/test-types.tsx:1:7 - error TS2322: Type 'string' is not assignable to type 'number'.

# ESLint should also catch this (if type-aware linting enabled)
pnpm lint

# Clean up
rm src/test-types.tsx
```

---

### Verification 7: Accessibility Linting Works

```bash
# Create accessibility violation
cat > src/test-a11y.tsx << 'EOF'
export default function TestA11y() {
  return <img src="test.png" />; // Missing alt attribute
}
EOF

# Lint
pnpm lint

# Expected output
src/test-a11y.tsx
  2:10  warning  Missing 'alt' attribute  jsx-a11y/alt-text

# Clean up
rm src/test-a11y.tsx
```

---

## Troubleshooting

### Issue 1: "Cannot find module 'eslint'"

**Symptom**:
```
Error: Cannot find module 'eslint'
```

**Solution**:
```bash
# Reinstall dependencies
rm -rf node_modules
pnpm install
```

---

### Issue 2: "Parsing error: Cannot read file 'tsconfig.json'"

**Symptom**:
```
Parsing error: ESLint was configured to run on `src/App.tsx` using `parserOptions.project`
```

**Solution 1**: Verify `tsconfig.json` exists
```bash
ls tsconfig.json
# If missing, create one
```

**Solution 2**: Set correct `tsconfigRootDir`
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true,
  tsconfigRootDir: import.meta.dirname, // Add this
}
```

---

### Issue 3: Pre-Commit Hook Doesn't Run

**Symptom**: `git commit` succeeds without running linting.

**Solution 1**: Verify hook is executable
```bash
ls -l .husky/pre-commit
# Expected: -rwxr-xr-x (x = executable)

# Make executable
chmod +x .husky/pre-commit
```

**Solution 2**: Verify hook content
```bash
cat .husky/pre-commit
# Expected:
#!/usr/bin/env sh
pnpm lint-staged
```

**Solution 3**: Test hook manually
```bash
.husky/pre-commit
# Should run lint-staged
```

---

### Issue 4: VS Code Auto-Fix Not Working

**Symptom**: Saving file doesn't auto-fix violations.

**Solution 1**: Verify ESLint extension installed
```
Cmd+Shift+X / Ctrl+Shift+X → Search "ESLint" → Install
```

**Solution 2**: Check VS Code settings
```json
// .vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit" // Required
  },
  "eslint.useFlatConfig": true // Required for ESLint 9
}
```

**Solution 3**: Reload VS Code
```
Cmd+Shift+P / Ctrl+Shift+P → "Developer: Reload Window"
```

**Solution 4**: Check ESLint output
```
View → Output → Select "ESLint" from dropdown
# Look for errors
```

---

### Issue 5: "Prettier and ESLint are fighting"

**Symptom**: Auto-fix on save keeps changing code back and forth.

**Solution 1**: Remove `eslint-plugin-prettier` (anti-pattern)
```bash
pnpm remove eslint-plugin-prettier
```

**Solution 2**: Verify Prettier is LAST in `eslint.config.mjs`
```javascript
export default [
  // ... all other configs
  prettier, // MUST BE LAST
]
```

**Solution 3**: Clear VS Code cache
```bash
rm -rf ~/Library/Caches/com.microsoft.VSCode
# Linux: rm -rf ~/.cache/vscode
# Windows: rmdir /s %APPDATA%\Code\Cache
```

---

### Issue 6: Slow Pre-Commit Hook (>10 seconds)

**Symptom**: `git commit` hangs for 10+ seconds.

**Solution 1**: Verify `lint-staged` only lints staged files
```javascript
// lint-staged.config.js
export default {
  '*.{js,jsx,ts,tsx}': ['eslint --fix'], // Only staged files
}
```

**Solution 2**: Use `projectService` (faster)
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true, // 30-50% faster than project
}
```

**Solution 3**: Stage fewer files at once
```bash
# Instead of:
git add .  # Stages 100+ files

# Do:
git add src/components/Button.tsx  # Stage incrementally
```

---

## Customization Guide

### Customization 1: Change Prettier Settings

**Example**: Prefer single quotes instead of double quotes.

**Steps**:
1. Open `.prettierrc`
2. Change `"singleQuote": false` to `"singleQuote": true`
3. Run `pnpm format` to reformat entire codebase
4. Commit changes

**Common Customizations**:
```json
{
  "singleQuote": true,        // Single quotes (default: false)
  "semi": false,              // No semicolons (default: true)
  "printWidth": 120,          // Longer lines (default: 100)
  "trailingComma": "es5",     // ES5 trailing commas (default: "all")
  "tabWidth": 4,              // 4-space indent (default: 2)
}
```

---

### Customization 2: Add Custom ESLint Rule

**Example**: Enforce `import type` for all TypeScript imports.

**Steps**:
1. Open `eslint.config.mjs`
2. Find `rules` section
3. Add or modify rule

```javascript
rules: {
  '@typescript-eslint/consistent-type-imports': [
    'error', // ← Changed from 'warn' to 'error'
    {
      prefer: 'type-imports',
      fixStyle: 'inline-type-imports',
    },
  ],
}
```

---

### Customization 3: Disable Rule for Specific Files

**Example**: Allow `console.log` in `scripts/` directory.

**Steps**:
1. Open `eslint.config.mjs`
2. Add file-specific override

```javascript
export default [
  // ... base configs
  {
    files: ['scripts/**/*.{js,ts}'],
    rules: {
      'no-console': 'off', // Allow console in scripts
    },
  },
]
```

---

### Customization 4: Escalate Accessibility Warnings to Errors

**Example**: Make missing `alt` text an error (blocks commits).

**Steps**:
1. Open `eslint.config.mjs`
2. Find jsx-a11y rules
3. Change `'warn'` to `'error'`

```javascript
rules: {
  'jsx-a11y/alt-text': 'error', // ← Changed from 'warn'
}
```

---

### Customization 5: Add Testing Library Plugin

**Example**: Lint test files with `eslint-plugin-testing-library`.

**Steps**:
1. Install plugin
```bash
pnpm add -D eslint-plugin-testing-library
```

2. Import in `eslint.config.mjs`
```javascript
import testingLibrary from 'eslint-plugin-testing-library'
```

3. Add test file override
```javascript
{
  files: ['**/*.test.{js,jsx,ts,tsx}', '**/__tests__/**'],
  plugins: {
    'testing-library': testingLibrary,
  },
  rules: {
    ...testingLibrary.configs.react.rules,
  },
}
```

---

## Next Steps

### After Installation

1. **Read awareness-guide.md** to understand when to use SAP-022 and common pitfalls
2. **Add CI linting** (SAP-005 patterns) to GitHub Actions
3. **Train team** on pre-commit hooks and auto-fix on save (30-minute session)
4. **Customize rules** based on team preferences (document changes in README)
5. **Escalate warnings to errors** gradually (1-2 rules per sprint)

---

### Integrate with Other SAPs

- **SAP-020 (React Foundation)**: Install SAP-022 immediately after scaffolding
- **SAP-021 (React Testing)**: Add `eslint-plugin-testing-library` for test linting
- **SAP-006 (Quality Gates)**: Unify pre-commit hooks (Python + React)
- **SAP-005 (CI/CD)**: Add lint job to GitHub Actions pipeline

---

### Report Issues

If you encounter issues not covered in this guide:

1. Check [awareness-guide.md](./awareness-guide.md) Common Pitfalls section
2. Check [protocol-spec.md](./protocol-spec.md) Technical Specification
3. Open issue in chora-base repository

---

## Summary Checklist

Use this checklist to verify SAP-022 is fully installed:

### Installation Checklist

- [ ] Node.js 22.x installed
- [ ] ESLint 9.26.0 installed
- [ ] Prettier 3.6.2 installed
- [ ] Husky 9.1.7 installed
- [ ] lint-staged 15.2.11 installed
- [ ] `eslint.config.mjs` copied (Next.js or Vite)
- [ ] `.prettierrc` copied
- [ ] `.prettierignore` copied
- [ ] `lint-staged.config.js` copied
- [ ] `.vscode/settings.json` copied
- [ ] `.vscode/extensions.json` copied
- [ ] `package.json` scripts added
- [ ] `.husky/pre-commit` configured
- [ ] `pnpm lint` runs successfully (0 errors)
- [ ] `pnpm format` runs successfully
- [ ] Pre-commit hook runs on commit
- [ ] VS Code auto-fixes on save
- [ ] 8 VS Code extensions installed

### Testing Checklist

- [ ] `pnpm lint` passes (0 errors)
- [ ] `pnpm lint:fix` auto-fixes violations
- [ ] `pnpm format` formats files
- [ ] `pnpm type-check` catches type errors
- [ ] Pre-commit hook runs in <5 seconds
- [ ] VS Code auto-fix works on save
- [ ] ESLint catches React Hooks violations
- [ ] ESLint catches accessibility violations
- [ ] Prettier formats on save (VS Code)

---

**End of Adoption Blueprint**
