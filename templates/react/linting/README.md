# React Linting & Formatting Templates (SAP-022)

This directory contains production-ready ESLint 9 + Prettier 3 configuration templates for React 19 applications.

**SAP ID**: SAP-022
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01

---

## Quick Links

- [Capability Charter](../../../docs/skilled-awareness/react-linting/capability-charter.md) - Business case and ROI
- [Protocol Spec](../../../docs/skilled-awareness/react-linting/protocol-spec.md) - Technical specification
- [Awareness Guide](../../../docs/skilled-awareness/react-linting/awareness-guide.md) - Use cases and pitfalls
- [Adoption Blueprint](../../../docs/skilled-awareness/react-linting/adoption-blueprint.md) - Step-by-step installation
- [Ledger](../../../docs/skilled-awareness/react-linting/ledger.md) - Adoption tracking

---

## What's Included

This directory provides **8 configuration files** for ESLint 9 + Prettier 3 + pre-commit hooks:

### Framework-Specific Configs

1. **[nextjs/eslint.config.mjs](./nextjs/eslint.config.mjs)** (226 lines)
   - ESLint 9 flat config for Next.js 15
   - Includes: eslint-config-next, App Router rules, API route overrides
   - Use for: Next.js 15 projects

2. **[vite/eslint.config.mjs](./vite/eslint.config.mjs)** (216 lines)
   - ESLint 9 flat config for Vite 7
   - Includes: eslint-plugin-react-refresh, browser-only globals
   - Use for: Vite 7 projects, Create React App (deprecated), Remix

### Shared Configs

3. **[shared/.prettierrc](./shared/.prettierrc)** (10 lines)
   - Prettier 3.x configuration with community-validated settings
   - Use for: All React projects

4. **[shared/.prettierignore](./shared/.prettierignore)** (16 lines)
   - Prettier exclusions (node_modules, build directories, lock files)
   - Use for: All React projects

5. **[shared/lint-staged.config.js](./shared/lint-staged.config.js)** (8 lines)
   - Pre-commit hook configuration (ESLint → Prettier order)
   - Use for: All React projects

6. **[shared/.vscode/settings.json](./shared/.vscode/settings.json)** (29 lines)
   - VS Code auto-fix on save integration
   - Use for: All React projects (VS Code users)

7. **[shared/.vscode/extensions.json](./shared/.vscode/extensions.json)** (24 lines)
   - 8 recommended VS Code extensions (ESLint, Prettier, Tailwind, etc.)
   - Use for: All React projects (VS Code users)

8. **[shared/package.json.snippet](./shared/package.json.snippet)** (30 lines)
   - Scripts (lint, format, type-check) and devDependencies
   - Use for: Merge into your package.json

---

## Technology Stack

**Linting**:
- ESLint 9.26.0 (flat config, 182x faster incremental builds)
- typescript-eslint 8.32.0 (projectService API, 30-50% faster)

**Plugins** (8 total):
- eslint-plugin-react 7.37.5 (React 19 patterns)
- eslint-plugin-react-hooks 7.0.1 (Rules of Hooks enforcement)
- eslint-plugin-jsx-a11y 6.10.2 (WCAG 2.2 Level AA)
- eslint-plugin-react-refresh 0.4.24 (Vite Fast Refresh)
- eslint-config-next 15.5.0 (Next.js 15 rules)
- eslint-config-prettier 9.1.0 (disable conflicting rules)
- @eslint/js 9.26.0 (base JavaScript rules)
- globals 16.1.0 (browser/Node.js globals)

**Formatting**:
- Prettier 3.6.2

**Pre-Commit Hooks**:
- Husky 9.1.7 (Git hooks)
- lint-staged 15.2.11 (pre-commit linting)

**TypeScript**:
- TypeScript 5.7.0
- @types/react 19.0.0
- @types/react-dom 19.0.0
- @types/node 22.0.0

**Node.js**: 22.x (required)

---

## Installation

### Option 1: New Project from SAP-020 (20 minutes)

Follow the [Adoption Blueprint](../../../docs/skilled-awareness/react-linting/adoption-blueprint.md#quick-start-new-projects) Quick Start guide.

**Steps**:
1. Scaffold React project with SAP-020 (Next.js or Vite)
2. Install SAP-022 dependencies (`pnpm add -D eslint@^9.26.0 ...`)
3. Copy configs from this directory
4. Run `pnpm lint:fix` and `pnpm format`
5. Install VS Code extensions

**Time**: 20 minutes

---

### Option 2: Existing Project (25 minutes)

Follow the [Adoption Blueprint](../../../docs/skilled-awareness/react-linting/adoption-blueprint.md#standard-installation-existing-projects) Standard Installation guide.

**Steps**:
1. Backup existing linting configs
2. Install ESLint 9 + Prettier dependencies
3. Copy configs from this directory
4. Configure Husky + lint-staged
5. Fix existing violations (`pnpm lint:fix`)

**Time**: 25 minutes (depends on existing violations)

---

## Usage

### Linting

```bash
# Check for violations
pnpm lint

# Auto-fix violations
pnpm lint:fix

# Type-check TypeScript (no emit)
pnpm type-check
```

---

### Formatting

```bash
# Format all files
pnpm format

# Check formatting (CI)
pnpm format:check
```

---

### Pre-Commit Hook

```bash
# Commit (pre-commit hook runs automatically)
git add .
git commit -m "feat: Add new feature"

# Expected: Hook runs ESLint + Prettier on staged files (<5s)
```

---

### VS Code Integration

**Auto-fix on save**:
1. Install recommended extensions (VS Code prompts automatically)
2. Open any `.tsx` file
3. Add violation: `var x = 1;`
4. Save file (Cmd+S / Ctrl+S)
5. Verify: `var` → `const` automatically

---

## Configuration Files Explained

### nextjs/eslint.config.mjs

**Purpose**: ESLint 9 flat config for Next.js 15 projects.

**Key Features**:
- Ignores `.next/`, `out/`, Next.js config files
- Includes `eslint-config-next` (Next.js-specific rules)
- App Router and Pages Router support
- API route overrides (allow console in API routes)
- Server Components patterns (React 19)

**Use When**: Building Next.js 15 applications.

**Don't Use When**: Building with Vite, Remix, or other frameworks.

---

### vite/eslint.config.mjs

**Purpose**: ESLint 9 flat config for Vite 7 projects.

**Key Features**:
- Ignores `dist/`, Vite config files
- Includes `eslint-plugin-react-refresh` (Vite Fast Refresh)
- Browser-only globals (no Node.js)
- React 19 patterns (JSX transform, no prop-types)

**Use When**: Building Vite 7, Create React App (deprecated), or Remix applications.

**Don't Use When**: Building Next.js applications.

---

### shared/.prettierrc

**Purpose**: Prettier 3.x formatting configuration.

**Key Settings**:
- `semi: true` - Semicolons required
- `singleQuote: false` - Double quotes
- `trailingComma: "all"` - Trailing commas everywhere
- `printWidth: 100` - 100 character line width
- `tabWidth: 2` - 2-space indentation
- `arrowParens: "always"` - Parentheses around arrow function params
- `endOfLine: "lf"` - Unix line endings

**Customization**: Change settings based on team preferences (see [Awareness Guide](../../../docs/skilled-awareness/react-linting/awareness-guide.md#customization-workflows)).

---

### shared/.prettierignore

**Purpose**: Exclude files from Prettier formatting.

**Excluded**:
- `node_modules`, `.next`, `out`, `build`, `dist` (build directories)
- `coverage` (test coverage reports)
- `*.min.js`, `*.min.css` (minified files)
- `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock` (lock files)
- `public` (static assets)

**Customization**: Add project-specific exclusions (e.g., `generated/**`).

---

### shared/lint-staged.config.js

**Purpose**: Pre-commit hook configuration (runs on `git commit`).

**Key Pattern**: ESLint FIRST, Prettier SECOND (correct order).

**What It Does**:
1. On commit, lint-staged identifies staged files
2. For `.js/.jsx/.ts/.tsx` files: Run `eslint --fix --max-warnings=0`, then `prettier --write`
3. For `.json/.md/.css` files: Run `prettier --write`
4. If any command fails, commit is blocked

**Performance**: Runs in <5 seconds for typical commit (10-20 files).

**Customization**: Add other linters (e.g., stylelint for CSS).

---

### shared/.vscode/settings.json

**Purpose**: VS Code auto-fix on save integration.

**Key Settings**:
- `editor.formatOnSave: true` - Auto-format on save
- `editor.defaultFormatter: "esbenp.prettier-vscode"` - Prettier as formatter
- `editor.codeActionsOnSave.source.fixAll.eslint: "explicit"` - ESLint auto-fix
- `eslint.useFlatConfig: true` - ESLint 9 flat config support

**Behavior**: On save, VS Code runs ESLint auto-fix, then Prettier formatting.

**Requirement**: VS Code 1.95+ with ESLint and Prettier extensions installed.

---

### shared/.vscode/extensions.json

**Purpose**: Recommend 8 essential VS Code extensions.

**Recommendations**:
1. **ES7+ React snippets** - React code snippets
2. **ESLint** - ESLint integration (REQUIRED)
3. **Prettier** - Prettier integration (REQUIRED)
4. **Tailwind CSS IntelliSense** - Tailwind autocomplete
5. **Import Cost** - Package size in imports
6. **Auto Rename Tag** - Rename closing tags automatically
7. **Error Lens** - Inline error display
8. **Console Ninja** - Enhanced console.log

**Unwanted**: Beautify, TSLint (deprecated, conflicts with ESLint/Prettier).

**Behavior**: VS Code prompts to install recommended extensions on project open.

---

### shared/package.json.snippet

**Purpose**: Scripts and devDependencies to merge into your `package.json`.

**Scripts**:
- `lint` - Check for violations
- `lint:fix` - Auto-fix violations
- `format` - Format all files with Prettier
- `format:check` - Check formatting (CI)
- `type-check` - TypeScript type-checking (no emit)
- `prepare` - Husky setup (runs on `npm install`)

**DevDependencies**: All required packages with pinned versions.

**Usage**: Copy scripts and dependencies, then run `pnpm install`.

---

## File Decision Tree

**Which ESLint config should I use?**

```
START: Which React framework?
├─ Next.js 15 → Use nextjs/eslint.config.mjs
├─ Vite 7 → Use vite/eslint.config.mjs
├─ Create React App (deprecated) → Use vite/eslint.config.mjs
├─ Remix → Use nextjs/eslint.config.mjs (customize: remove Next.js rules)
└─ Other → Use vite/eslint.config.mjs as base
```

**Which files do I need?**

| File | Next.js | Vite | Required? |
|------|---------|------|-----------|
| `nextjs/eslint.config.mjs` | ✅ | ❌ | Yes (Next.js) |
| `vite/eslint.config.mjs` | ❌ | ✅ | Yes (Vite) |
| `shared/.prettierrc` | ✅ | ✅ | Yes |
| `shared/.prettierignore` | ✅ | ✅ | Yes |
| `shared/lint-staged.config.js` | ✅ | ✅ | Yes |
| `shared/.vscode/settings.json` | ✅ | ✅ | Recommended |
| `shared/.vscode/extensions.json` | ✅ | ✅ | Recommended |
| `shared/package.json.snippet` | ✅ | ✅ | Yes (merge) |

---

## Customization Examples

### Example 1: Change Prettier to Single Quotes

**File**: `shared/.prettierrc`

```json
{
  "singleQuote": true,  // ← Changed from false
  "semi": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

**Impact**: All strings formatted with single quotes.

---

### Example 2: Escalate Accessibility Rules to Errors

**File**: `nextjs/eslint.config.mjs` or `vite/eslint.config.mjs`

```javascript
rules: {
  'jsx-a11y/alt-text': 'error',  // ← Changed from 'warn'
  'jsx-a11y/anchor-is-valid': 'error',  // ← Changed from 'warn'
}
```

**Impact**: Missing alt text blocks commits (pre-commit hook).

---

### Example 3: Allow console.log in scripts/

**File**: `nextjs/eslint.config.mjs` or `vite/eslint.config.mjs`

```javascript
export default [
  // ... base configs
  {
    files: ['scripts/**/*.{js,ts}'],
    rules: {
      'no-console': 'off',  // Allow console in scripts
    },
  },
]
```

**Impact**: `console.log` allowed in `scripts/` directory.

---

### Example 4: Add Testing Library Plugin

**Install**:
```bash
pnpm add -D eslint-plugin-testing-library
```

**File**: `nextjs/eslint.config.mjs` or `vite/eslint.config.mjs`

```javascript
import testingLibrary from 'eslint-plugin-testing-library'

export default [
  // ... base configs
  {
    files: ['**/*.test.{js,jsx,ts,tsx}', '**/__tests__/**'],
    plugins: {
      'testing-library': testingLibrary,
    },
    rules: {
      ...testingLibrary.configs.react.rules,
    },
  },
]
```

**Impact**: Test-specific linting rules (e.g., no waitFor nesting).

---

## Common Pitfalls

### ❌ Pitfall 1: Using eslint-plugin-prettier

**What**: Installing `eslint-plugin-prettier` and running Prettier through ESLint.

**Why Bad**: Slower, confusing errors, conflicts with eslint-config-prettier.

**Solution**: Use `eslint-config-prettier` (disables conflicting rules), run Prettier separately.

---

### ❌ Pitfall 2: Running Prettier BEFORE ESLint

**What**: Configuring lint-staged to run Prettier before ESLint.

**Why Bad**: ESLint may undo Prettier's formatting (infinite loop).

**Solution**: ESLint FIRST, Prettier SECOND (correct order in lint-staged.config.js).

---

### ❌ Pitfall 3: Not Configuring VS Code

**What**: Installing SAP-022 but not copying `.vscode/` files.

**Why Bad**: No auto-fix on save, manual linting required.

**Solution**: Copy `.vscode/settings.json` and `.vscode/extensions.json`.

---

For more pitfalls, see [Awareness Guide](../../../docs/skilled-awareness/react-linting/awareness-guide.md#anti-patterns-what-not-to-do).

---

## Performance Benchmarks

**Test Environment**: MacBook Pro M2, 16GB RAM, Next.js 15 project (50 TypeScript files)

| Operation | Time | Notes |
|-----------|------|-------|
| `pnpm lint` (first run) | 2.8s | Includes type-checking |
| `pnpm lint` (cached) | 0.6s | Uses .eslintcache |
| `pnpm format` | 0.4s | Prettier is fast |
| Pre-commit hook (3 files) | 1.2s | lint-staged optimized |
| Pre-commit hook (20 files) | 3.5s | Still acceptable |

**Key Takeaway**: ESLint 9 flat config is **182x faster** than ESLint 8 for incremental builds.

---

## Support

**Documentation**:
- [Adoption Blueprint](../../../docs/skilled-awareness/react-linting/adoption-blueprint.md) - Step-by-step installation
- [Awareness Guide](../../../docs/skilled-awareness/react-linting/awareness-guide.md) - Use cases, pitfalls, troubleshooting
- [Protocol Spec](../../../docs/skilled-awareness/react-linting/protocol-spec.md) - Technical details

**Community**:
- GitHub Issues: [chora-base/issues](https://github.com/liminalcommons/chora-base/issues)
- Email: victor@liminalcommons.org

**Ledger**:
- [Adoption Ledger](../../../docs/skilled-awareness/react-linting/ledger.md) - Track adoption, share success stories

---

## Related SAPs

**Wave 4: React SAP Series**:
- [SAP-020](../../README.md) (React Foundation) - Project scaffolding ← *prerequisite*
- [SAP-021](../testing/README.md) (React Testing) - Testing infrastructure
- **SAP-022** (React Linting) - This SAP
- SAP-023 (State Management) - Planned
- SAP-024 (Styling) - Planned

**Complementary SAPs**:
- [SAP-006](../../../docs/skilled-awareness/quality-gates/README.md) (Quality Gates) - Pre-commit patterns
- [SAP-005](../../../docs/skilled-awareness/ci-cd/README.md) (CI/CD) - Automated pipelines
- [SAP-009](../../../docs/skilled-awareness/agent-awareness/README.md) (Agent Awareness) - AI coding patterns

---

## License

MIT License - Same as chora-base repository

---

## Changelog

### v1.0.0 (2025-11-01)

**Added**:
- ESLint 9.26.0 flat config (Next.js and Vite)
- Prettier 3.6.2 configuration
- Pre-commit hooks (Husky + lint-staged)
- VS Code integration (settings + extensions)
- 8 template files
- 5 documentation artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)

**Tested With**:
- Next.js 15.5.x
- Vite 7.x
- React 19.x
- TypeScript 5.7.x
- Node.js 22.x

**Known Issues**: None

---

**End of README**
