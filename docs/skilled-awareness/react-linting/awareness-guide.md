# SAP-022: React Linting & Formatting - Awareness Guide

**SAP ID**: SAP-022
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-11-01
**Category**: Technology-Specific SAP (Front-End Quality)

---

## Purpose of This Guide

This Awareness Guide helps you understand **when**, **where**, and **how** to apply SAP-022 (React Linting & Formatting) effectively. Unlike the Protocol Spec (which defines technical standards) and the Adoption Blueprint (which provides step-by-step instructions), this guide focuses on **decision-making** and **awareness**.

**You should read this guide if**:
- You're deciding whether SAP-022 is right for your project
- You want to understand when to customize linting rules
- You're troubleshooting linting issues or conflicts
- You need to integrate SAP-022 with other SAPs or tools
- You want to avoid common pitfalls and anti-patterns

---

## Table of Contents

1. [Use Cases: When to Use SAP-022](#use-cases-when-to-use-sap-022)
2. [Anti-Patterns: What NOT to Do](#anti-patterns-what-not-to-do)
3. [Decision Trees](#decision-trees)
4. [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)
5. [Integration Patterns](#integration-patterns)
6. [Customization Workflows](#customization-workflows)
7. [Migration Scenarios](#migration-scenarios)
8. [Team Adoption Strategies](#team-adoption-strategies)
9. [Performance Considerations](#performance-considerations)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## Use Cases: When to Use SAP-022

### ✅ Use SAP-022 When...

#### 1. Starting a New React Project from SAP-020

**Context**: You've just scaffolded a React project using SAP-020 (React Foundation) templates.

**Why SAP-022 Fits**:
- Fresh codebase with zero linting violations
- Team alignment from day one
- Pre-commit hooks prevent violations from accumulating
- Auto-fix reduces onboarding friction

**Setup Time**: 20 minutes

**Example**:
```bash
# After creating project with SAP-020
cd my-react-app
# Follow SAP-022 adoption-blueprint.md
# Install dependencies, copy configs, run lint:fix
pnpm install
pnpm lint:fix
git add . && git commit -m "chore: Add SAP-022 linting infrastructure"
```

---

#### 2. Standardizing Code Quality Across Multiple React Projects

**Context**: You maintain 3+ React projects with inconsistent linting setups.

**Why SAP-022 Fits**:
- Single source of truth for linting standards
- Copy configs to all projects (5 minutes per project)
- Consistent developer experience across projects
- Centralized updates (update SAP-022, copy to projects)

**Setup Time**: 5 minutes per project

**ROI**: If you have 10 projects, saves 9.5 hours total (55 minutes × 10 projects)

---

#### 3. Onboarding Junior Developers

**Context**: Junior developers joining team, need automated quality guardrails.

**Why SAP-022 Fits**:
- Auto-fix on save reduces friction ("it just works")
- Clear error messages teach best practices
- Pre-commit hooks catch violations before code review
- Reduces code review time (no style discussions)

**Team Impact**: 50% reduction in onboarding time for code quality standards

---

#### 4. Enforcing Accessibility Standards (WCAG 2.2)

**Context**: Building public-facing applications requiring accessibility compliance.

**Why SAP-022 Fits**:
- eslint-plugin-jsx-a11y catches 70% of common violations
- Warnings guide developers to fix issues during development
- Pre-commit hooks prevent accessibility regressions
- Integrates with SAP-026 (Accessibility) when available

**Quality Impact**: 70% fewer accessibility issues reaching QA

---

#### 5. Migrating from Legacy ESLint 8 Setup

**Context**: Existing React project with ESLint 8 (eslintrc) configuration.

**Why SAP-022 Fits**:
- ESLint 9 flat config is 182x faster (incremental builds)
- typescript-eslint v8 projectService is 30-50% faster
- Modern plugin ecosystem (React 19, Next.js 15, Vite 7)
- Path to future ESLint features

**Migration Time**: 1-2 hours (see [Migration Scenarios](#migration-scenarios))

---

### ❌ Do NOT Use SAP-022 When...

#### 1. Building Non-React Projects

**Why**: SAP-022 is optimized for React 19 + TypeScript patterns.

**Alternative**: Use language-specific linting SAPs (Python, Rust, etc.)

---

#### 2. Using React <18

**Why**: SAP-022 assumes React 17+ JSX transform, React Hooks patterns.

**Alternative**: Customize eslint.config.mjs to enable react/react-in-jsx-scope, add prop-types support.

---

#### 3. Team Strongly Prefers Different Tools (StandardJS, XO)

**Why**: SAP-022 uses ESLint + Prettier. Forcing tool change creates team friction.

**Alternative**: Document your team's tool choice as a local SAP variant, or skip SAP-022.

---

#### 4. Legacy Codebase with 500+ Linting Violations

**Why**: Fixing 500+ violations is a multi-day project. Pre-commit hooks will block all commits.

**Alternative**:
1. Migrate incrementally (see [Migration Scenarios](#migration-scenarios))
2. Use `eslint-disable-next-line` for legacy code
3. Enable rules gradually (start with warnings, escalate to errors)

---

#### 5. CI/CD Pipeline Has Custom Linting Requirements

**Why**: SAP-022 provides opinionated configs. If your CI requires specific rules, you'll need to customize.

**Alternative**: Use SAP-022 as a starting point, customize rules in eslint.config.mjs.

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Using eslint-plugin-prettier

**What**: Installing `eslint-plugin-prettier` and running Prettier through ESLint.

**Why This Is Bad**:
- Slower (ESLint runs Prettier as a plugin, adds overhead)
- Prettier violations shown as ESLint errors (confusing)
- Conflicts with eslint-config-prettier (which disables formatting rules)

**What to Do Instead**:
```javascript
// ❌ WRONG: eslint-plugin-prettier
import prettierPlugin from 'eslint-plugin-prettier'
export default [
  prettierPlugin.configs.recommended, // DON'T DO THIS
]

// ✅ CORRECT: eslint-config-prettier
import prettier from 'eslint-config-prettier'
export default [
  // ... other configs
  prettier, // Disables conflicting rules, MUST BE LAST
]
```

**Correct Workflow**:
1. ESLint fixes code quality issues (`eslint --fix`)
2. Prettier formats code (`prettier --write`)
3. Pre-commit hook runs both in sequence (lint-staged.config.js)

---

### ❌ Anti-Pattern 2: Running Prettier BEFORE ESLint

**What**: Configuring lint-staged to run Prettier before ESLint.

**Why This Is Bad**:
- ESLint auto-fixes may undo Prettier's formatting
- Results in infinite loop (Prettier formats, ESLint unformats)
- Pre-commit hook fails with "unstaged changes" error

**What to Do Instead**:
```javascript
// ❌ WRONG ORDER
export default {
  '*.{js,jsx,ts,tsx}': [
    'prettier --write',
    'eslint --fix', // May undo Prettier's work
  ],
}

// ✅ CORRECT ORDER
export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix', // Fix code quality first
    'prettier --write', // Format after fixing
  ],
}
```

---

### ❌ Anti-Pattern 3: Disabling TypeScript Type-Aware Linting

**What**: Removing `projectService` or `tseslint.configs.recommendedTypeChecked` to speed up linting.

**Why This Is Bad**:
- Loses 50% of TypeScript linting value (no type checking)
- Misses critical bugs (async Promise misuse, type mismatches)
- ESLint 9 + typescript-eslint v8 already optimized (projectService is fast)

**What to Do Instead**:
```javascript
// ❌ WRONG: No type-aware linting
export default [
  ...tseslint.configs.recommended, // Base rules only
]

// ✅ CORRECT: Type-aware linting (REQUIRED)
export default [
  ...tseslint.configs.recommendedTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true, // NEW in v8, faster than project
      },
    },
  },
]
```

**Performance**: projectService is 30-50% faster than old `project` option.

---

### ❌ Anti-Pattern 4: Committing with `--no-verify`

**What**: Regularly bypassing pre-commit hooks with `git commit --no-verify`.

**Why This Is Bad**:
- Pre-commit hooks exist to catch violations early
- Bypassing hooks pushes violations to CI (slower feedback)
- Creates inconsistent codebase (some commits linted, some not)

**What to Do Instead**:
```bash
# ❌ WRONG: Bypass hooks regularly
git commit --no-verify -m "Quick fix"

# ✅ CORRECT: Fix violations, commit normally
pnpm lint:fix
git add .
git commit -m "fix: Resolve linting violations"

# ✅ ACCEPTABLE: Emergency bypass (rare)
# Document why in commit message
git commit --no-verify -m "hotfix: Critical production bug (lint violations to fix in follow-up)"
```

---

### ❌ Anti-Pattern 5: Ignoring Accessibility Warnings

**What**: Disabling jsx-a11y rules or ignoring warnings long-term.

**Why This Is Bad**:
- Accessibility violations harm 15% of users (disabilities)
- Ignoring warnings normalizes poor accessibility practices
- Violations may become legal liability (ADA compliance)

**What to Do Instead**:
```javascript
// ❌ WRONG: Disable accessibility rules
export default [
  {
    rules: {
      'jsx-a11y/alt-text': 'off', // DON'T DO THIS
    },
  },
]

// ✅ CORRECT: Start with warnings, escalate to errors
export default [
  jsxA11y.flatConfigs.recommended, // Warnings by default
  {
    rules: {
      // Escalate critical rules to errors over time
      'jsx-a11y/alt-text': 'error', // After team is trained
    },
  },
]
```

**Progressive Approach**:
1. **Week 1-4**: Warnings only (educate team)
2. **Week 5-8**: Fix warnings in new code
3. **Week 9+**: Escalate to errors, fix legacy violations

---

### ❌ Anti-Pattern 6: Not Configuring VS Code Integration

**What**: Installing SAP-022 but not setting up `.vscode/settings.json` and `.vscode/extensions.json`.

**Why This Is Bad**:
- Developers don't get auto-fix on save (friction)
- Manual linting required (slows workflow)
- Inconsistent experience across team members

**What to Do Instead**:
1. Copy `.vscode/settings.json` from SAP-022 templates
2. Copy `.vscode/extensions.json` from SAP-022 templates
3. Install recommended extensions (VS Code prompts automatically)

**Developer Experience Impact**: 80% reduction in manual linting commands.

---

## Decision Trees

### Decision Tree 1: Should I Migrate to ESLint 9? (NEW - from RT-019)

**CRITICAL DECISION**: ESLint 9 flat config is the NEW STANDARD. ESLint 8 is LEGACY.

```
START: Are you using ESLint 8 (.eslintrc)?
├─ NO (using ESLint 9) → ✅ You're good! Skip to next decision tree
└─ YES (using ESLint 8) → Want 182x faster linting?
    ├─ NO → ⚠️ Still migrate (ESLint 10 will remove .eslintrc)
    └─ YES → How many custom plugins/rules?
        ├─ 0-3 plugins → ✅ Migrate now (30-60 min)
        ├─ 4-10 plugins → ✅ Migrate now, verify plugin compatibility (1-2 hours)
        └─ >10 plugins → ⚠️ Audit plugins first, then migrate (2-4 hours)
```

**Decision Factors**:

| Factor | Migrate Now | Wait |
|--------|-------------|------|
| **ESLint version** | ESLint 8 (.eslintrc) | N/A - must migrate |
| **Performance need** | Incremental lint >2s | N/A - migrate anyway |
| **Plugin compatibility** | All plugins support flat config | Some plugins don't support flat config yet |
| **Team availability** | 30-60 min available | No time (but schedule soon!) |

**Key Insight from RT-019**: The 182x performance improvement (9,100ms → 50ms for incremental lint) is so significant that migration pays for itself in 1 week of development.

---

### Decision Tree 2: Should I Use SAP-022?

```
START: Do you have a React project?
├─ NO → Use language-specific linting SAP
└─ YES → Is it React 18+?
    ├─ NO → Customize SAP-022 for older React
    └─ YES → Does your team agree on automated formatting?
        ├─ NO → Discuss team standards first
        └─ YES → Is this a new project or existing?
            ├─ NEW → ✅ Use SAP-022 (20 min setup)
            └─ EXISTING → How many linting violations?
                ├─ <50 → ✅ Use SAP-022, fix violations
                ├─ 50-200 → ✅ Use SAP-022, gradual migration
                └─ >200 → ⚠️ Use SAP-022, incremental adoption
```

---

### Decision Tree 2: Which ESLint Config (Next.js or Vite)?

```
START: Which React framework?
├─ Next.js → Use nextjs/eslint.config.mjs
│   └─ Includes: eslint-config-next, App Router rules, API route overrides
│
├─ Vite → Use vite/eslint.config.mjs
│   └─ Includes: eslint-plugin-react-refresh, browser-only globals
│
├─ Create React App (CRA) → Use vite/eslint.config.mjs
│   └─ CRA is deprecated, Vite config is closer match
│
├─ Remix → Use nextjs/eslint.config.mjs as base
│   └─ Customize: Remove Next.js-specific rules
│
└─ Other (Gatsby, Astro) → Start with vite/eslint.config.mjs
    └─ Customize: Add framework-specific plugins
```

---

### Decision Tree 3: Should I Customize Rules?

```
START: Should I change SAP-022 default rules?
├─ Team has strong style preferences? (e.g., single quotes)
│   └─ ✅ Customize .prettierrc
│       └─ Document in project README
│
├─ Need stricter TypeScript rules?
│   └─ ✅ Customize tseslint rules
│       └─ Example: Enable @typescript-eslint/strict configs
│
├─ Building public-facing app?
│   └─ ✅ Escalate jsx-a11y rules to errors
│       └─ Start with warnings, escalate after team training
│
├─ Using specific libraries? (e.g., React Query, Zustand)
│   └─ ✅ Add library-specific ESLint plugins
│       └─ Example: @tanstack/eslint-plugin-query
│
└─ Just don't like a rule?
    └─ ⚠️ Discuss with team first
        └─ SAP-022 rules are community-validated
        └─ Avoid "personal preference" customizations
```

---

### Decision Tree 4: Strict vs Relaxed Linting

```
START: What's your team's linting philosophy?
├─ STRICT: Zero warnings, enforce all rules
│   └─ ✅ Recommended for:
│       ├─ New projects
│       ├─ Teams with senior developers
│       ├─ Public-facing applications
│       └─ High-quality codebases
│   └─ Configuration:
│       ├─ Set all jsx-a11y rules to 'error'
│       ├─ Enable @typescript-eslint/strict
│       └─ Set --max-warnings=0 in CI
│
├─ BALANCED: Errors block, warnings allowed
│   └─ ✅ Recommended for:
│       ├─ SAP-022 default (ships this way)
│       ├─ Teams with junior developers
│       ├─ Internal applications
│       └─ Most use cases
│   └─ Configuration:
│       ├─ Keep SAP-022 defaults
│       ├─ jsx-a11y rules as 'warn'
│       └─ Escalate critical rules over time
│
└─ RELAXED: Warnings only, manual enforcement
    └─ ⚠️ Only recommended for:
        ├─ Legacy codebases (500+ violations)
        ├─ Gradual migration projects
        └─ Proof-of-concept / prototype code
    └─ Configuration:
        ├─ Downgrade most rules to 'warn'
        ├─ No --max-warnings in CI
        └─ Schedule "linting cleanup" sprints
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Slow Pre-Commit Hooks (>10 seconds)

**Symptom**: `git commit` takes >10 seconds, developers complain.

**Diagnosis**:
```bash
# Test pre-commit performance
time pnpm lint-staged
# Should be <5 seconds for typical commit
```

**Possible Causes**:
1. Linting entire codebase (not just staged files)
2. TypeScript type-checking every file
3. Too many files staged at once

**Solutions**:

**Solution 1**: Verify lint-staged only checks staged files
```javascript
// lint-staged.config.js
export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix', // Only staged files
    'prettier --write',
  ],
}
```

**Solution 2**: Use projectService (faster than project)
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true, // NEW in v8, 30-50% faster
}
```

**Solution 3**: Stage files incrementally
```bash
# ❌ Avoid staging 100+ files at once
git add .

# ✅ Stage related files together
git add src/components/Button.tsx src/components/Button.test.tsx
git commit -m "feat: Add Button component"
```

---

### Pitfall 2: Prettier vs ESLint Conflicts

**Symptom**: Auto-fix on save keeps changing code back and forth.

**Diagnosis**:
- Save file → ESLint formats one way
- Save again → Prettier formats differently
- Infinite loop of formatting changes

**Possible Causes**:
1. eslint-plugin-prettier installed (anti-pattern)
2. Prettier not LAST in eslint.config.mjs
3. Custom ESLint formatting rules conflicting with Prettier

**Solutions**:

**Solution 1**: Remove eslint-plugin-prettier
```bash
pnpm remove eslint-plugin-prettier
```

**Solution 2**: Ensure Prettier is LAST in config
```javascript
// eslint.config.mjs
export default [
  // ... all other configs
  prettier, // MUST BE LAST
]
```

**Solution 3**: Check for conflicting rules
```bash
# Use eslint-config-prettier CLI to detect conflicts
npx eslint-config-prettier eslint.config.mjs
```

---

### Pitfall 3: TypeScript Type Errors in ESLint

**Symptom**: ESLint fails with "Parsing error: Cannot find tsconfig.json".

**Diagnosis**:
```bash
pnpm lint
# Error: Parsing error: ESLint was configured to run on `<file>` using `parserOptions.project`
```

**Possible Causes**:
1. Missing tsconfig.json in project root
2. Incorrect tsconfigRootDir in parserOptions
3. File excluded in tsconfig.json (e.g., test files)

**Solutions**:

**Solution 1**: Verify tsconfig.json exists
```bash
ls tsconfig.json
# If missing, create one (SAP-020 should have provided this)
```

**Solution 2**: Set correct tsconfigRootDir
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true,
  tsconfigRootDir: import.meta.dirname, // REQUIRED for ESM
}
```

**Solution 3**: Include linted files in tsconfig.json
```json
// tsconfig.json
{
  "include": ["src/**/*", "test/**/*", "**/*.config.ts"],
  "exclude": ["node_modules", "dist"]
}
```

---

### Pitfall 4: React Hooks Violations Not Caught

**Symptom**: Violating Rules of Hooks (e.g., conditional hooks), but no ESLint error.

**Diagnosis**:
```javascript
// This should error but doesn't
function MyComponent({ condition }) {
  if (condition) {
    const [state, setState] = useState(0); // ❌ Conditional hook
  }
}
```

**Possible Causes**:
1. react-hooks plugin not configured
2. react-hooks rules set to 'warn' instead of 'error'
3. ESLint not running (check VS Code ESLint extension)

**Solutions**:

**Solution 1**: Verify react-hooks plugin configured
```javascript
// eslint.config.mjs
{
  plugins: { 'react-hooks': reactHooks },
  rules: reactHooks.configs.recommended.rules, // REQUIRED
}
```

**Solution 2**: Escalate to errors
```javascript
rules: {
  'react-hooks/rules-of-hooks': 'error', // Enforce
  'react-hooks/exhaustive-deps': 'warn', // Start with warn
}
```

**Solution 3**: Check VS Code ESLint status
- Open VS Code Output panel
- Select "ESLint" from dropdown
- Look for errors (e.g., "ESLint server crashed")

---

### Pitfall 5: CI Linting Passes, Local Fails (or vice versa)

**Symptom**: `pnpm lint` passes locally, fails in CI (or vice versa).

**Diagnosis**:
```bash
# Local
pnpm lint # ✅ No errors

# CI
npm run lint # ❌ 10 errors
```

**Possible Causes**:
1. Different Node.js versions (local vs CI)
2. Different package manager (pnpm vs npm)
3. Cached node_modules (stale dependencies)
4. .eslintcache not gitignored

**Solutions**:

**Solution 1**: Match Node.js versions
```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with:
    node-version: 22 # Match local version
```

**Solution 2**: Use same package manager
```yaml
# If using pnpm locally, use pnpm in CI
- uses: pnpm/action-setup@v2
  with:
    version: 10
```

**Solution 3**: Clear caches
```bash
# Local
rm -rf node_modules .eslintcache
pnpm install

# CI: Add cache-busting step
```

**Solution 4**: Gitignore ESLint cache
```gitignore
# .gitignore
.eslintcache
```

---

## Integration Patterns

### Integration 1: SAP-022 + SAP-020 (React Foundation)

**Scenario**: New React project from SAP-020 template.

**Integration Steps**:
1. Scaffold project with SAP-020 (Next.js or Vite)
2. Install SAP-022 immediately (before writing code)
3. Run `pnpm lint:fix` to catch any scaffolding violations
4. Commit linting infrastructure

**Timeline**: 25 minutes total (SAP-020: 5 min, SAP-022: 20 min)

**Benefits**:
- Zero legacy violations (fresh codebase)
- Team aligned from day one
- Pre-commit hooks prevent violations

---

### Integration 2: SAP-022 + SAP-021 (React Testing)

**Scenario**: React project with testing infrastructure, need linting for test files.

**Integration Steps**:
1. Install SAP-022 (base linting)
2. Install SAP-021 (testing infrastructure)
3. Add `eslint-plugin-testing-library` (optional)
4. Configure test file overrides in eslint.config.mjs

**Example Configuration**:
```javascript
// eslint.config.mjs
{
  files: ['**/*.test.{js,jsx,ts,tsx}', '**/__tests__/**'],
  plugins: {
    'testing-library': testingLibrary,
  },
  rules: {
    ...testingLibrary.configs.react.rules,
    '@typescript-eslint/no-explicit-any': 'off', // Allow any in tests
  },
}
```

**Benefits**:
- Test-specific linting rules (e.g., no waitFor nesting)
- Relaxed rules in tests (allow any for mocks)
- Consistent test code quality

---

### Integration 3: SAP-022 + SAP-006 (Quality Gates)

**Scenario**: Python + React monorepo, standardize pre-commit hooks.

**Integration Steps**:
1. Install SAP-006 (Python pre-commit)
2. Install SAP-022 (React linting)
3. Configure .pre-commit-config.yaml for Python
4. Configure Husky + lint-staged for React
5. (Optional) Unify under pre-commit framework

**Example Unified Configuration**:
```yaml
# .pre-commit-config.yaml (Python)
repos:
  - repo: local
    hooks:
      - id: eslint
        name: ESLint (React)
        entry: pnpm lint-staged
        language: system
        pass_filenames: false
```

**Benefits**:
- Consistent pre-commit experience (Python + React)
- Single quality gate for entire monorepo
- Centralized hook management

---

### Integration 4: SAP-022 + SAP-005 (CI/CD)

**Scenario**: Add linting checks to CI pipeline.

**Integration Steps**:
1. Install SAP-022 (linting infrastructure)
2. Add lint job to GitHub Actions (SAP-005 patterns)
3. Cache node_modules and .eslintcache
4. Fail CI on linting violations

**Example CI Configuration**:
```yaml
# .github/workflows/ci.yml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint # From SAP-022 package.json
      - run: pnpm format:check # Prettier check
```

**Benefits**:
- Automated quality enforcement (no manual reviews)
- Pre-commit catches 80%, CI catches remaining 20%
- Fast feedback (lint job runs in parallel with tests)

---

### Integration 5: SAP-022 + Tailwind CSS

**Scenario**: React project using Tailwind CSS, need class sorting.

**Integration Steps**:
1. Install SAP-022 (base linting)
2. Install `prettier-plugin-tailwindcss` (official Prettier plugin)
3. Configure Prettier to use plugin
4. (Optional) Add `eslint-plugin-tailwindcss` for class validation

**Example Configuration**:
```json
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindConfig": "./tailwind.config.js"
}
```

**Benefits**:
- Automatic Tailwind class sorting (consistent order)
- Validates Tailwind class names (catches typos)
- Integrates with SAP-022 auto-fix on save

---

## Customization Workflows

### Workflow 1: Changing Prettier Settings (Team Preference)

**Scenario**: Team prefers single quotes instead of double quotes.

**Steps**:
1. Open `.prettierrc`
2. Change `"singleQuote": false` to `"singleQuote": true`
3. Run `pnpm format` to reformat entire codebase
4. Commit changes (large git diff expected)
5. Document in project README

**Example**:
```json
// .prettierrc
{
  "singleQuote": true, // ← Team preference
  "semi": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

**Recommendation**: Make Prettier changes early (before codebase grows).

---

### Workflow 2: Adding Custom ESLint Rule

**Scenario**: Team wants to enforce `import type` for all TypeScript imports.

**Steps**:
1. Open `eslint.config.mjs`
2. Find the `rules` section
3. Add or modify rule
4. Test with `pnpm lint`
5. Document rationale in comment

**Example**:
```javascript
// eslint.config.mjs
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

### Workflow 3: Disabling Rule for Specific Files

**Scenario**: Need to allow `console.log` in scripts/ directory.

**Steps**:
1. Open `eslint.config.mjs`
2. Add file-specific override
3. Use glob patterns for file matching

**Example**:
```javascript
// eslint.config.mjs
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

### Workflow 4: Escalating Warnings to Errors

**Scenario**: Team is ready to enforce accessibility rules strictly.

**Steps**:
1. Open `eslint.config.mjs`
2. Find jsx-a11y rules (currently 'warn')
3. Change to 'error'
4. Run `pnpm lint` to see violations
5. Fix violations before committing

**Example**:
```javascript
// eslint.config.mjs
rules: {
  // Before: Warnings
  'jsx-a11y/alt-text': 'warn',

  // After: Errors (blocks commits)
  'jsx-a11y/alt-text': 'error',
}
```

**Timeline**: Escalate 1-2 rules per sprint (gradual approach).

---

## Migration Scenarios

### Scenario 1: Fresh React Project (No Existing Linting)

**Starting Point**: React project with no ESLint or Prettier.

**Migration Steps**:
1. Follow SAP-022 adoption-blueprint.md (20 minutes)
2. Install dependencies
3. Copy all configs
4. Run `pnpm lint:fix` (auto-fix all violations)
5. Commit

**Expected Violations**: 0-10 (fresh codebase)

**Timeline**: 20 minutes

---

### Scenario 2: Migrate from ESLint 8 (eslintrc) to ESLint 9 (Flat Config) [PRIORITY - from RT-019]

**Starting Point**: React project with `.eslintrc.json` or `.eslintrc.js`.

**Why Migrate**: **182x faster incremental linting** (9,100ms → 50ms), future-proof (ESLint 10 removes .eslintrc)

**Migration Steps**:

**Step 1**: Backup existing config
```bash
cp .eslintrc.json .eslintrc.json.backup
cp .eslintignore .eslintignore.backup
```

**Step 2**: Install ESLint 9 dependencies
```bash
# Remove ESLint 8 packages
pnpm remove eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Install ESLint 9 (combined typescript-eslint package)
pnpm add -D eslint@^9.26.0 typescript-eslint@^8.32.0
```

**Step 3**: Convert .eslintrc to flat config

**Old .eslintrc.js (ESLint 8)**:
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
  },
}
```

**New eslint.config.mjs (ESLint 9 Flat Config)**:
```javascript
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactPlugin from 'eslint-plugin-react'
import reactHooksPlugin from 'eslint-plugin-react-hooks'
import prettierConfig from 'eslint-config-prettier'
import globals from 'globals'

export default tseslint.config(
  // Global ignores (replaces .eslintignore)
  {
    ignores: ['**/node_modules/**', '**/.next/**', '**/dist/**'],
  },

  // Base configs (replaces extends)
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  reactPlugin.configs.flat.recommended,

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

  // React Hooks (replaces plugins)
  {
    plugins: {
      'react-hooks': reactHooksPlugin,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
    },
  },

  // Prettier integration (MUST be last)
  prettierConfig,
)
```

**Key Changes**:
- ❌ `extends` → ✅ Import and spread configs (`...tseslint.configs.recommended`)
- ❌ `plugins: []` → ✅ `plugins: {}` (object instead of array)
- ❌ `env` → ✅ `languageOptions.globals`
- ❌ `.eslintignore` → ✅ `ignores: []` in flat config
- ❌ `@typescript-eslint/parser` → ✅ `typescript-eslint` (combined package)
- ✅ **NEW**: `projectService: true` (30-50% faster than old `project` option)

**Step 4**: Delete old config files
```bash
rm .eslintrc.js .eslintrc.json .eslintrc
rm .eslintignore
```

**Step 5**: Update VS Code settings
```json
// .vscode/settings.json
{
  "eslint.useFlatConfig": true  // Required for ESLint 9
}
```

**Step 6**: Test migration
```bash
# Test linting
pnpm lint

# Fix any violations
pnpm lint:fix

# Verify 182x performance improvement (watch mode)
# Before: ~9,100ms for incremental lint
# After: ~50ms for incremental lint
```

**Step 7**: Update CI scripts (if needed)
```yaml
# .github/workflows/ci.yml
# No changes needed (ESLint 9 uses same CLI)
```

**Timeline**: 30-60 minutes (depends on custom plugins)

**Performance Validation** (from RT-019):
```bash
# Test incremental lint speed
# 1. Make a small change in a file
# 2. Run lint in watch mode
# 3. Should see ~50ms lint time (vs ~9,100ms before)
```

**Common Migration Issues**:

**Issue 1: "Cannot find module '@typescript-eslint/parser'"**
- **Cause**: ESLint 9 uses `typescript-eslint` combined package
- **Fix**: Install `typescript-eslint@^8.32.0` (not separate parser/plugin)

**Issue 2: "extends is not allowed"**
- **Cause**: Flat config doesn't support `extends`
- **Fix**: Import configs and spread: `...tseslint.configs.recommended`

**Issue 3: "env is not allowed"**
- **Cause**: Flat config uses `languageOptions.globals`
- **Fix**: `languageOptions: { globals: { ...globals.browser } }`

**Issue 4: Plugins not found**
- **Cause**: Some plugins may not have flat config support yet
- **Fix**: Check plugin docs for flat config compatibility

**Migration Checklist**:
- [ ] Backup .eslintrc and .eslintignore
- [ ] Install ESLint 9.26.0+ and typescript-eslint@^8.32.0
- [ ] Create eslint.config.mjs with flat config
- [ ] Convert extends → imported configs
- [ ] Convert plugins array → plugins object
- [ ] Convert env → languageOptions.globals
- [ ] Convert .eslintignore → ignores in flat config
- [ ] Remove old .eslintrc files
- [ ] Update VS Code settings (eslint.useFlatConfig: true)
- [ ] Test with pnpm lint
- [ ] Verify 182x performance improvement

---

### Scenario 3: Large Codebase (500+ Violations)

**Starting Point**: React project with 500+ linting violations.

**Migration Approach**: Gradual adoption (incremental enforcement).

**Step 1**: Install SAP-022 with all rules as warnings
```javascript
// eslint.config.mjs
// Override all rules to 'warn' (temp)
rules: {
  '@typescript-eslint/no-explicit-any': 'warn', // ← Changed from 'error'
  'react-hooks/rules-of-hooks': 'warn', // ← Changed from 'error'
  // ... (copy all SAP-022 rules, change to 'warn')
}
```

**Step 2**: Fix violations incrementally
```bash
# Week 1-2: Fix critical violations (React Hooks, TypeScript any)
pnpm lint --fix

# Week 3-4: Fix accessibility violations
pnpm lint --fix

# Week 5+: Fix remaining warnings
```

**Step 3**: Escalate rules to errors (one at a time)
```javascript
// Week 1: Escalate React Hooks to error
rules: {
  'react-hooks/rules-of-hooks': 'error', // ← Escalated
}
```

**Step 4**: Repeat until all rules are errors

**Timeline**: 4-8 weeks (depends on team size and codebase)

---

### Scenario 4: Migrate from StandardJS or XO

**Starting Point**: React project using StandardJS or XO.

**Migration Approach**: Replace tool entirely (breaking change).

**Step 1**: Document team discussion and decision
- Why migrate? (Prettier auto-format, better TypeScript support)
- Team vote or consensus?

**Step 2**: Remove StandardJS/XO
```bash
pnpm remove standard xo
```

**Step 3**: Install SAP-022
- Follow adoption-blueprint.md
- Expect large git diff (formatting changes)

**Step 4**: Reformat entire codebase
```bash
pnpm format # Prettier reformats all files
```

**Step 5**: Commit with clear message
```bash
git add .
git commit -m "refactor: Migrate from StandardJS to SAP-022 (ESLint 9 + Prettier)"
```

**Timeline**: 2-3 hours (includes team discussion)

**Risk**: Team resistance (mitigate with clear communication).

---

## Team Adoption Strategies

### Strategy 1: Top-Down (Management-Driven)

**Approach**: Technical lead decides on SAP-022, mandates adoption.

**Steps**:
1. Lead installs SAP-022
2. Lead announces in team meeting ("starting Monday, pre-commit hooks enabled")
3. Lead provides training session (30 minutes)
4. Lead monitors adoption (first week)

**Pros**:
- Fast adoption (1 week)
- Consistent enforcement

**Cons**:
- May face resistance
- Requires strong leadership

**Best For**: Teams with clear hierarchy, urgent quality needs.

---

### Strategy 2: Bottom-Up (Developer-Driven)

**Approach**: Developer proposes SAP-022, team discusses and agrees.

**Steps**:
1. Developer creates RFC (Request for Comments) document
2. Team discusses in meeting (30-60 minutes)
3. Team votes (majority or consensus)
4. If approved, developer installs SAP-022
5. Team adopts gradually (1-2 weeks)

**Pros**:
- High buy-in (team agreed)
- Low resistance

**Cons**:
- Slower adoption (2-3 weeks)
- Requires team alignment

**Best For**: Collaborative teams, flat hierarchy.

---

### Strategy 3: Gradual Onboarding

**Approach**: Enable SAP-022 features incrementally.

**Timeline**:

**Week 1**: ESLint + Prettier (no pre-commit hooks)
```bash
pnpm lint:fix # Manual for now
pnpm format
```

**Week 2**: VS Code integration (auto-fix on save)
- Copy `.vscode/settings.json`
- Install recommended extensions

**Week 3**: Pre-commit hooks (enforce on commit)
```bash
pnpm add -D husky lint-staged
npx husky init
```

**Week 4**: CI integration (enforce in pipeline)
- Add lint job to GitHub Actions

**Pros**:
- Low friction (gradual learning)
- Team adapts incrementally

**Cons**:
- Slower full adoption (4 weeks)

**Best For**: Junior teams, risk-averse organizations.

---

### Strategy 4: Pilot Project

**Approach**: Test SAP-022 on one project before rolling out.

**Steps**:
1. Choose pilot project (small, active development)
2. Install SAP-022 on pilot (follow adoption-blueprint.md)
3. Monitor for 2-4 weeks (collect feedback)
4. Retrospective (what worked, what didn't)
5. Roll out to all projects (if successful)

**Pros**:
- Low risk (test on one project)
- Real-world validation

**Cons**:
- Slower organization-wide adoption (6-8 weeks)

**Best For**: Large organizations, multiple teams.

---

## Performance Considerations

### Benchmark: Linting Performance

**Test Environment**:
- Next.js 15 project with 50 TypeScript files
- MacBook Pro M2, 16GB RAM
- ESLint 9.26.0, typescript-eslint 8.32.0

**Results**:

| Operation | Time | Notes |
|-----------|------|-------|
| `pnpm lint` (first run) | 2.8s | Includes type-checking |
| `pnpm lint` (cached) | 0.6s | Uses .eslintcache |
| `pnpm format` | 0.4s | Prettier is fast |
| Pre-commit hook (3 files staged) | 1.2s | lint-staged optimized |
| Pre-commit hook (20 files staged) | 3.5s | Still acceptable |

**Key Takeaway**: ESLint 9 flat config is **182x faster** than ESLint 8 for incremental builds (per ESLint blog).

---

### Optimization 1: Enable ESLint Caching

**Configuration**:
```json
// package.json
{
  "scripts": {
    "lint": "eslint . --cache",
    "lint:fix": "eslint . --fix --cache"
  }
}
```

**Impact**: 2-5x faster linting (after first run).

**Caveat**: Add `.eslintcache` to `.gitignore`.

---

### Optimization 2: Use projectService (Not project)

**Configuration**:
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true, // NEW in typescript-eslint v8
  // OLD: project: './tsconfig.json', // 30-50% slower
}
```

**Impact**: 30-50% faster TypeScript type-checking.

---

### Optimization 3: Limit Pre-Commit Hook Scope

**Configuration**:
```javascript
// lint-staged.config.js
export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix --max-warnings=0', // Only staged files
  ],
}
```

**Impact**: Pre-commit hook only lints staged files (not entire codebase).

---

## Troubleshooting Guide

### Issue 1: "Cannot find module 'eslint-plugin-react'"

**Error**:
```
Error: Cannot find module 'eslint-plugin-react'
```

**Cause**: Missing dependency.

**Solution**:
```bash
pnpm install # Reinstall dependencies
# Or manually install
pnpm add -D eslint-plugin-react
```

---

### Issue 2: "Parsing error: Cannot read file 'tsconfig.json'"

**Error**:
```
Parsing error: ESLint was configured to run on `src/App.tsx` using `parserOptions.project`
```

**Cause**: Missing or incorrect tsconfig.json path.

**Solution**:
```javascript
// eslint.config.mjs
parserOptions: {
  projectService: true,
  tsconfigRootDir: import.meta.dirname, // REQUIRED
}
```

---

### Issue 3: "Prettier and ESLint are fighting"

**Symptom**: Auto-fix on save keeps changing code back and forth.

**Cause**: eslint-plugin-prettier installed (anti-pattern).

**Solution**: Remove eslint-plugin-prettier
```bash
pnpm remove eslint-plugin-prettier
```

---

### Issue 4: "Pre-commit hook takes 30 seconds"

**Symptom**: `git commit` hangs for 30+ seconds.

**Cause**: Linting entire codebase (not just staged files).

**Solution**: Verify lint-staged.config.js only lints staged files
```javascript
// lint-staged.config.js
export default {
  '*.{js,jsx,ts,tsx}': ['eslint --fix'], // Only staged
}
```

---

### Issue 5: "ESLint fails in CI but passes locally"

**Symptom**: CI fails with linting errors, but `pnpm lint` passes locally.

**Cause**: Different Node.js versions or cached dependencies.

**Solution**: Match Node.js versions
```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with:
    node-version: 22 # Match local
```

---

## Summary: Key Takeaways

### ✅ DO

1. Use SAP-022 for React 18+ projects
2. Install immediately on new projects (before writing code)
3. Run ESLint BEFORE Prettier (correct order)
4. Use projectService for faster TypeScript linting
5. Configure VS Code integration (auto-fix on save)
6. Escalate accessibility warnings to errors gradually
7. Customize rules for team preferences (document changes)

### ❌ DON'T

1. Use eslint-plugin-prettier (anti-pattern)
2. Run Prettier before ESLint (wrong order)
3. Disable type-aware linting (loses 50% of value)
4. Commit with `--no-verify` regularly
5. Ignore accessibility warnings long-term
6. Skip VS Code integration (reduces developer experience)

### 🔑 Critical Patterns

- **Pre-commit hook order**: ESLint → Prettier
- **ESLint config**: Prettier MUST BE LAST in array
- **TypeScript linting**: Use projectService (30-50% faster)
- **Performance**: Enable --cache for 2-5x speedup

---

**End of Awareness Guide**
