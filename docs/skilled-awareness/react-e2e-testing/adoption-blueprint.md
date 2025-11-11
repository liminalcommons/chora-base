# SAP-039: React E2E Testing - Adoption Blueprint

**SAP ID**: SAP-039
**Name**: react-e2e-testing
**Status**: pilot
**Version**: 1.0.0
**Last Updated**: 2025-11-09
**Diataxis Type**: How-To (Step-by-Step Installation)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Framework Selection (5 min)](#framework-selection-5-min)
3. [Option A: Playwright Setup (25 min)](#option-a-playwright-setup-25-min)
4. [Option B: Cypress Setup (25 min)](#option-b-cypress-setup-25-min)
5. [Common Post-Setup Steps (10 min)](#common-post-setup-steps-10-min)
6. [Validation & Testing](#validation--testing)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Prerequisites

### System Requirements

| Requirement | Minimum Version | Recommended | Check Command |
|-------------|----------------|-------------|---------------|
| **Node.js** | 22.x LTS | 22.11+ | `node --version` |
| **npm** | 10.x | 10.9+ | `npm --version` |
| **React** | 19.x | 19.0.0+ | Check package.json |
| **Next.js** | 15.x | 15.1+ | Check package.json |
| **TypeScript** | 5.7.x | 5.7.2+ | `npx tsc --version` |

**Operating System**:
- macOS 12+ (for Safari/WebKit testing)
- Windows 10/11 (WSL2 recommended for Linux compatibility)
- Linux (Ubuntu 20.04+, Debian 11+)

---

### SAP Dependencies

#### Required SAPs (MUST have)

**SAP-020: React Foundation**
- **Why**: Provides Next.js 15 + React 19 project setup
- **Verify**: Check if you have a working Next.js 15 app running on http://localhost:3000
- **Status**: Must be adopted before SAP-039

#### Recommended SAPs (Enhance E2E testing)

**SAP-021: React Testing**
- **Why**: Share MSW mocks between unit tests and E2E tests
- **Integration**: Reuse handlers from Vitest for E2E API mocking
- **Status**: Optional (highly recommended)

**SAP-033: React Authentication**
- **Why**: Test auth flows (login, signup, OAuth)
- **Integration**: E2E test authentication workflows
- **Status**: Optional (required if app has authentication)

**SAP-041: React Form Validation**
- **Why**: Test form validation, submission flows
- **Integration**: E2E test Zod schemas, React Hook Form
- **Status**: Optional (required if app has forms)

---

### Pre-Flight Checklist

Before starting, verify:

```bash
# ✅ Next.js app runs locally
npm run dev
# Open http://localhost:3000 (should load)

# ✅ TypeScript compiles
npx tsc --noEmit

# ✅ Git repo exists (for version control)
git status

# ✅ Dependencies up to date
npm outdated
# Update if needed: npm update
```

---

## Framework Selection (5 min)

### Decision Matrix

Use this matrix to choose between Playwright and Cypress:

| Question | Answer | Recommendation |
|----------|--------|----------------|
| Do you need Safari testing? | YES | **Playwright** (only framework with WebKit) |
| Do you need mobile browser testing (Chrome Android, Safari iOS)? | YES | **Playwright** (native mobile support) |
| Do you prioritize time-travel debugging? | YES | **Cypress** (best debugging experience) |
| Do you need free parallelization (no paid tier)? | YES | **Playwright** (built-in workers, sharding) |
| Do you need built-in visual regression? | YES | **Playwright** (native screenshots) |
| Are you migrating from Selenium? | YES | **Playwright** (similar API, easier migration) |
| Do you have a mature Cypress setup already? | YES | **Cypress** (stick with what works) |

**Default Recommendation**: **Playwright** (more modern, cross-browser, cost-effective)

---

### Quick Decision Tree

```
START: Choose E2E Framework

Q1: Need Safari or mobile (Chrome Android, Safari iOS) testing?
├─ YES → Playwright ✅
└─ NO  → Continue

Q2: Need time-travel debugging (see DOM at every step)?
├─ YES → Cypress ✅
└─ NO  → Continue

Q3: Need free parallelization (no Cypress Cloud subscription)?
├─ YES → Playwright ✅
└─ NO  → Either framework works

DEFAULT: Playwright ✅
```

**Make your choice, then proceed to Option A or Option B below.**

---

## Option A: Playwright Setup (25 min)

### Step 1: Install Playwright (3 min)

**Initialize Playwright**:
```bash
npm init playwright@latest
```

**Interactive prompts**:
- **TypeScript or JavaScript?** → TypeScript
- **Where to put tests?** → tests/e2e
- **Add GitHub Actions workflow?** → Yes
- **Install Playwright browsers?** → Yes (downloads Chrome, Firefox, WebKit)

**What gets installed**:
- `@playwright/test` - Test runner and assertions
- `playwright` - Browser binaries (Chrome, Firefox, WebKit)
- `playwright.config.ts` - Configuration file
- `.github/workflows/playwright.yml` - CI/CD workflow

**Verify installation**:
```bash
npx playwright --version
# Expected: Version 1.40.0 or later
```

---

### Step 2: Configure Playwright (5 min)

**Edit playwright.config.ts**:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './tests/e2e',

  // Timeout per test
  timeout: 30000, // 30 seconds

  // Expect timeout (for assertions)
  expect: {
    timeout: 10000, // 10 seconds
  },

  // Retries
  retries: process.env.CI ? 3 : 0, // Retry 3x in CI, 0x locally

  // Parallel execution
  workers: process.env.CI ? 4 : 1, // 4 workers in CI, 1 locally
  fullyParallel: true,

  // Reporter
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list'], // Console output
  ],

  // Shared settings for all projects
  use: {
    // Base URL
    baseURL: 'http://localhost:3000',

    // Trace (for debugging)
    trace: 'on-first-retry', // Only on retries

    // Screenshots
    screenshot: 'only-on-failure', // Only on failure

    // Videos
    video: 'retain-on-failure', // Only on failure

    // Viewport
    viewport: { width: 1280, height: 720 },

    // Ignore HTTPS errors (for local dev)
    ignoreHTTPSErrors: true,

    // User agent
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  },

  // Projects (browsers to test)
  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile browsers (optional, comment out if not needed)
    // {
    //   name: 'mobile-chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'mobile-safari',
    //   use: { ...devices['iPhone 13'] },
    // },
  ],

  // Web server (auto-start Next.js dev server)
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI, // Reuse server locally, restart in CI
    timeout: 120000, // 2 minutes to start
  },
});
```

**Why these settings?**:
- **Retries**: 3x in CI reduces flakiness (transient errors)
- **Workers**: 4 parallel workers = 4x faster tests
- **Trace/screenshot/video**: Debug failures without re-running tests
- **webServer**: Automatically starts Next.js dev server before tests

---

### Step 3: Create First Test (5 min)

**Create tests/e2e/homepage.spec.ts**:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    await page.goto('/');

    // Wait for page to fully load
    await page.waitForLoadState('networkidle');

    // Verify page title
    await expect(page).toHaveTitle(/Home/i);

    // Verify main heading exists
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should navigate to login page', async ({ page }) => {
    await page.goto('/');

    // Click login link
    await page.click('a[href="/login"]');

    // Verify navigation
    await expect(page).toHaveURL('/login');
    await expect(page.locator('h1')).toHaveText(/Login/i);
  });
});
```

---

### Step 4: Add Page Object Model (5 min)

**Create tests/pages/LoginPage.ts**:
```typescript
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly heading: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.heading = page.locator('h1');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }

  async waitForRedirect(url: string) {
    await this.page.waitForURL(url);
  }
}
```

**Create tests/e2e/auth/login.spec.ts**:
```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';

test.describe('Login Flow', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('should login with valid credentials', async ({ page }) => {
    await loginPage.login('test@example.com', 'password');
    await loginPage.waitForRedirect('/dashboard');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toHaveText('Dashboard');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await loginPage.login('invalid@example.com', 'wrong');

    const error = await loginPage.getErrorMessage();
    expect(error).toBe('Invalid email or password');
  });
});
```

---

### Step 5: Add Authentication (Session Persistence) (5 min)

**Create tests/auth.setup.ts**:
```typescript
import { test as setup, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  const loginPage = new LoginPage(page);

  // Navigate to login page
  await loginPage.goto();

  // Login
  await loginPage.login('test@example.com', 'password');

  // Wait for redirect to dashboard
  await page.waitForURL('/dashboard');

  // Verify logged in
  await expect(page.locator('h1')).toHaveText('Dashboard');

  // Save session cookies + localStorage
  await page.context().storageState({ path: authFile });
});
```

**Update playwright.config.ts**:
```typescript
export default defineConfig({
  // ... existing config

  projects: [
    // Setup project (runs first)
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },

    // Chromium with auth
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: authFile, // Reuse session
      },
      dependencies: ['setup'], // Wait for setup to complete
    },

    // Firefox with auth
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: authFile,
      },
      dependencies: ['setup'],
    },

    // WebKit with auth
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: authFile,
      },
      dependencies: ['setup'],
    },
  ],
});
```

**Now all tests use authenticated session**:
```typescript
test('access dashboard', async ({ page }) => {
  await page.goto('/dashboard'); // Already logged in!
  await expect(page).toHaveURL('/dashboard');
});
```

---

### Step 6: Add API Mocking (Optional, 2 min)

**Create tests/utils/api-mocks.ts**:
```typescript
import { Page } from '@playwright/test';

export async function mockUserAPI(page: Page) {
  await page.route('/api/user', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
      }),
    });
  });
}

export async function mockErrorAPI(page: Page, endpoint: string, status: number = 500) {
  await page.route(endpoint, async (route) => {
    await route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Internal Server Error' }),
    });
  });
}
```

**Use in tests**:
```typescript
import { mockUserAPI } from '../utils/api-mocks';

test('should display user profile with mocked API', async ({ page }) => {
  await mockUserAPI(page);

  await page.goto('/profile');
  await expect(page.locator('[data-testid="user-name"]')).toHaveText('John Doe');
});
```

---

### Step 7: Run Tests (2 min)

**Run all tests**:
```bash
npx playwright test
```

**Run specific test**:
```bash
npx playwright test tests/e2e/auth/login.spec.ts
```

**Run in headed mode** (see browser):
```bash
npx playwright test --headed
```

**Run in debug mode**:
```bash
npx playwright test --debug
```

**View HTML report**:
```bash
npx playwright show-report
```

**Expected output**:
```
Running 12 tests using 4 workers

  ✓ tests/e2e/homepage.spec.ts:5:1 › Homepage › should load successfully (1.2s)
  ✓ tests/e2e/homepage.spec.ts:15:1 › Homepage › should navigate to login page (0.8s)
  ✓ tests/e2e/auth/login.spec.ts:10:1 › Login Flow › should login with valid credentials (1.5s)
  ✓ tests/e2e/auth/login.spec.ts:18:1 › Login Flow › should show error with invalid credentials (1.1s)

  12 passed (8.2s)
```

---

## Option B: Cypress Setup (25 min)

### Step 1: Install Cypress (3 min)

**Install Cypress**:
```bash
npm install --save-dev cypress
```

**Open Cypress** (first-time setup):
```bash
npx cypress open
```

**Interactive setup**:
1. Choose "E2E Testing"
2. Choose "Chrome" browser
3. Click "Create new spec" → Creates example spec
4. Click "Okay, run the spec" → Runs example test

**What gets created**:
- `cypress/` directory
- `cypress.config.ts` - Configuration file
- `cypress/e2e/` - Test files
- `cypress/support/` - Commands, helpers
- `cypress/fixtures/` - Test data

**Verify installation**:
```bash
npx cypress --version
# Expected: Cypress 13.x or later
```

---

### Step 2: Configure Cypress (5 min)

**Edit cypress.config.ts**:
```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    // Base URL
    baseUrl: 'http://localhost:3000',

    // Viewport
    viewportWidth: 1280,
    viewportHeight: 720,

    // Timeouts
    defaultCommandTimeout: 10000, // 10 seconds for commands
    pageLoadTimeout: 30000, // 30 seconds for page loads
    requestTimeout: 10000, // 10 seconds for XHR/fetch requests

    // Retries
    retries: {
      runMode: 2, // CI (headless)
      openMode: 0, // Local (headed)
    },

    // Screenshots
    screenshotOnRunFailure: true,
    screenshotsFolder: 'cypress/screenshots',

    // Videos
    video: true,
    videosFolder: 'cypress/videos',
    videoCompression: 32, // Compression quality (0-51, lower = better quality)

    // Spec pattern
    specPattern: 'cypress/e2e/**/*.cy.{ts,tsx}',

    // Support file
    supportFile: 'cypress/support/e2e.ts',

    // Setup Node events
    setupNodeEvents(on, config) {
      // Add custom tasks, plugins here
      return config;
    },
  },
});
```

---

### Step 3: Create Custom Commands (5 min)

**Edit cypress/support/commands.ts**:
```typescript
/// <reference types="cypress" />

// Login command (with session caching)
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  }, {
    validate() {
      // Verify session is still valid
      cy.request('/api/auth/session').its('status').should('eq', 200);
    },
  });
});

// Database seeding command
Cypress.Commands.add('seedDatabase', () => {
  cy.task('db:seed');
});

// Wait for API calls to complete
Cypress.Commands.add('waitForAPI', () => {
  cy.intercept('GET', '/api/**').as('apiCalls');
  cy.wait('@apiCalls');
});

// Type definitions
declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Login with email and password (session cached)
       * @example cy.login('test@example.com', 'password')
       */
      login(email: string, password: string): Chainable<void>;

      /**
       * Seed database with test data
       * @example cy.seedDatabase()
       */
      seedDatabase(): Chainable<void>;

      /**
       * Wait for all API calls to complete
       * @example cy.waitForAPI()
       */
      waitForAPI(): Chainable<void>;
    }
  }
}

export {};
```

**Edit cypress/support/e2e.ts**:
```typescript
import './commands';
```

---

### Step 4: Create First Test (5 min)

**Create cypress/e2e/homepage.cy.ts**:
```typescript
describe('Homepage', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should load successfully', () => {
    // Verify page title
    cy.title().should('match', /Home/i);

    // Verify main heading exists
    cy.get('h1').should('be.visible');
  });

  it('should navigate to login page', () => {
    // Click login link
    cy.get('a[href="/login"]').click();

    // Verify navigation
    cy.url().should('include', '/login');
    cy.get('h1').should('contain.text', 'Login');
  });
});
```

---

### Step 5: Add Page Object Model (5 min)

**Create cypress/support/pages/LoginPage.ts**:
```typescript
export class LoginPage {
  visit() {
    cy.visit('/login');
    return this;
  }

  fillEmail(email: string) {
    cy.get('input[name="email"]').type(email);
    return this;
  }

  fillPassword(password: string) {
    cy.get('input[name="password"]').type(password);
    return this;
  }

  submit() {
    cy.get('button[type="submit"]').click();
    return this;
  }

  getErrorMessage() {
    return cy.get('[data-testid="error-message"]');
  }

  expectDashboard() {
    cy.url().should('include', '/dashboard');
    cy.get('h1').should('contain.text', 'Dashboard');
    return this;
  }
}
```

**Create cypress/e2e/auth/login.cy.ts**:
```typescript
import { LoginPage } from '../../support/pages/LoginPage';

describe('Login Flow', () => {
  const loginPage = new LoginPage();

  beforeEach(() => {
    loginPage.visit();
  });

  it('should login with valid credentials', () => {
    loginPage
      .fillEmail('test@example.com')
      .fillPassword('password')
      .submit()
      .expectDashboard();
  });

  it('should show error with invalid credentials', () => {
    loginPage
      .fillEmail('invalid@example.com')
      .fillPassword('wrong')
      .submit();

    loginPage.getErrorMessage()
      .should('be.visible')
      .and('contain.text', 'Invalid email or password');
  });
});
```

---

### Step 6: Add API Mocking (Optional, 2 min)

**Create cypress/e2e/profile.cy.ts**:
```typescript
describe('User Profile', () => {
  beforeEach(() => {
    // Mock /api/user endpoint
    cy.intercept('GET', '/api/user', {
      statusCode: 200,
      body: {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
      },
    }).as('getUser');
  });

  it('should display user profile with mocked API', () => {
    cy.visit('/profile');
    cy.wait('@getUser');

    cy.get('[data-testid="user-name"]').should('have.text', 'John Doe');
    cy.get('[data-testid="user-email"]').should('have.text', 'john@example.com');
  });

  it('should handle API errors gracefully', () => {
    // Override mock with error response
    cy.intercept('GET', '/api/user', {
      statusCode: 500,
      body: { error: 'Internal Server Error' },
    }).as('getUserError');

    cy.visit('/profile');
    cy.wait('@getUserError');

    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain.text', 'Failed to load user');
  });
});
```

---

### Step 7: Run Tests (2 min)

**Run all tests (headless)**:
```bash
npx cypress run
```

**Run specific test**:
```bash
npx cypress run --spec cypress/e2e/auth/login.cy.ts
```

**Run in headed mode**:
```bash
npx cypress run --headed
```

**Run specific browser**:
```bash
npx cypress run --browser chrome
npx cypress run --browser firefox
```

**Open Cypress UI** (interactive):
```bash
npx cypress open
```

**Expected output**:
```
  (Run Starting)

  ┌────────────────────────────────────────────────────────────────────────────┐
  │ Cypress:        13.6.0                                                      │
  │ Browser:        Chrome 120.0.0.0 (headless)                                │
  │ Node Version:   v22.11.0                                                    │
  │ Specs:          4 found (homepage.cy.ts, login.cy.ts, profile.cy.ts)       │
  └────────────────────────────────────────────────────────────────────────────┘

  Running:  homepage.cy.ts                                                (1 of 4)

    Homepage
      ✓ should load successfully (1,234ms)
      ✓ should navigate to login page (876ms)

    2 passing (3s)

  (Results)

  ┌────────────────────────────────────────────────────────────────────────────┐
  │ Tests:        8                                                             │
  │ Passing:      8                                                             │
  │ Failing:      0                                                             │
  │ Duration:     12s                                                           │
  └────────────────────────────────────────────────────────────────────────────┘
```

---

## Common Post-Setup Steps (10 min)

### Step 1: Add CI/CD Integration (3 min)

**For Playwright** (already created by `npm init playwright`):

**Edit .github/workflows/playwright.yml**:
```yaml
name: Playwright Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests (shard ${{ matrix.shard }}/4)
        run: npx playwright test --shard=${{ matrix.shard }}/4

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.shard }}
          path: playwright-report/
          retention-days: 30
```

**For Cypress**:

**Create .github/workflows/cypress.yml**:
```yaml
name: Cypress Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        containers: [1, 2, 3, 4]

    steps:
      - uses: actions/checkout@v4

      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          start: npm run dev
          wait-on: 'http://localhost:3000'
          wait-on-timeout: 120
          browser: chrome

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-screenshots-${{ matrix.containers }}
          path: cypress/screenshots

      - name: Upload videos
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-videos-${{ matrix.containers }}
          path: cypress/videos
```

---

### Step 2: Add data-testid to Components (5 min)

**Why**: Stable selectors prevent flakiness

**Add to your React components**:
```tsx
// components/LoginForm.tsx
export function LoginForm() {
  return (
    <form>
      <input
        name="email"
        type="email"
        data-testid="email-input" // ✅ Add this
      />
      <input
        name="password"
        type="password"
        data-testid="password-input" // ✅ Add this
      />
      <button
        type="submit"
        data-testid="submit-button" // ✅ Add this
      >
        Login
      </button>
      <div data-testid="error-message"> {/* ✅ Add this */}
        {error}
      </div>
    </form>
  );
}
```

**Update tests to use data-testid**:
```typescript
// ✅ Before
await page.click('button[type="submit"]');

// ✅ After (more stable)
await page.click('[data-testid="submit-button"]');
```

---

### Step 3: Add Visual Regression Testing (Optional, 2 min)

**Playwright** (built-in):
```typescript
// tests/e2e/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // First run: saves baseline screenshot
  // Subsequent runs: compares to baseline
  await expect(page).toHaveScreenshot('homepage.png');
});
```

**Update baselines**:
```bash
npx playwright test --update-snapshots
```

**Cypress + Percy**:
```bash
npm install --save-dev @percy/cli @percy/cypress
```

```typescript
// cypress/support/e2e.ts
import '@percy/cypress';
```

```typescript
// cypress/e2e/visual/homepage.cy.ts
it('homepage visual regression', () => {
  cy.visit('/');
  cy.percySnapshot('Homepage');
});
```

---

## Validation & Testing

### Validation Checklist

Run through this checklist to verify successful setup:

#### Playwright Validation

```bash
# ✅ 1. Playwright version
npx playwright --version
# Expected: Playwright v1.40.0 or later

# ✅ 2. Browsers installed
npx playwright install --dry-run
# Expected: chromium, firefox, webkit already installed

# ✅ 3. Config file exists
cat playwright.config.ts
# Expected: File exists, contains projects, webServer

# ✅ 4. Tests run successfully
npx playwright test
# Expected: 0 failing tests

# ✅ 5. HTML report generated
npx playwright show-report
# Expected: Opens browser with test results

# ✅ 6. CI workflow exists
cat .github/workflows/playwright.yml
# Expected: File exists, contains matrix strategy
```

#### Cypress Validation

```bash
# ✅ 1. Cypress version
npx cypress --version
# Expected: Cypress 13.x or later

# ✅ 2. Config file exists
cat cypress.config.ts
# Expected: File exists, contains e2e config

# ✅ 3. Support files exist
ls cypress/support/
# Expected: commands.ts, e2e.ts

# ✅ 4. Tests run successfully
npx cypress run
# Expected: 0 failing tests

# ✅ 5. CI workflow exists
cat .github/workflows/cypress.yml
# Expected: File exists, contains cypress-io/github-action
```

---

### Manual Testing

**Test 1: Homepage loads**:
```bash
# Playwright
npx playwright test tests/e2e/homepage.spec.ts --headed

# Cypress
npx cypress open
# Click on homepage.cy.ts
```

**Test 2: Authentication works**:
```bash
# Playwright
npx playwright test tests/e2e/auth/login.spec.ts --headed

# Cypress
npx cypress open
# Click on login.cy.ts
```

**Test 3: API mocking works**:
```bash
# Playwright
npx playwright test tests/e2e/profile.spec.ts --headed

# Cypress
npx cypress open
# Click on profile.cy.ts
```

---

## Troubleshooting

### Issue 1: Browsers Not Installed (Playwright)

**Error**:
```
browserType.launch: Executable doesn't exist at /path/to/chromium
```

**Solution**:
```bash
npx playwright install --with-deps
```

---

### Issue 2: Port 3000 Already in Use

**Error**:
```
Port 3000 is already in use by another process
```

**Solution**:
```bash
# Kill process on port 3000
npx kill-port 3000

# Or change port in playwright.config.ts / cypress.config.ts
baseURL: 'http://localhost:3001'
```

---

### Issue 3: Tests Timeout

**Error**:
```
Test timeout of 30000ms exceeded
```

**Solution**:
```typescript
// Increase timeout
export default defineConfig({
  timeout: 60000, // 60 seconds
});
```

---

### Issue 4: Authentication Session Not Persisting (Playwright)

**Error**:
Tests redirect to login despite auth.setup.ts

**Solution**:
```bash
# Delete auth file and re-run setup
rm playwright/.auth/user.json
npx playwright test --project=setup
```

---

### Issue 5: Cypress cy.session Not Working

**Error**:
cy.login() doesn't persist session

**Solution**:
```typescript
// Add validate function
cy.session([email, password], () => {
  // Login logic
}, {
  validate() {
    cy.request('/api/auth/session').its('status').should('eq', 200);
  },
});
```

---

## Next Steps

### Recommended Next Actions

1. **Add More Tests** (1-2 hours):
   - Form validation tests
   - Error handling tests
   - Protected route tests
   - API integration tests

2. **Optimize Performance** (30 min):
   - Enable parallel execution (4-10 workers)
   - Add test sharding in CI (4 machines)
   - Mock slow APIs

3. **Add Visual Regression** (30 min):
   - Playwright screenshots (built-in)
   - Cypress + Percy (paid service)

4. **Integrate with Other SAPs**:
   - **SAP-021**: Share MSW mocks with unit tests
   - **SAP-033**: Test auth flows (OAuth, SSO)
   - **SAP-041**: Test form validation (Zod, React Hook Form)

---

### Learning Resources

**Playwright**:
- Official Docs: https://playwright.dev
- Best Practices: https://playwright.dev/docs/best-practices
- API Reference: https://playwright.dev/docs/api/class-playwright

**Cypress**:
- Official Docs: https://docs.cypress.io
- Best Practices: https://docs.cypress.io/guides/references/best-practices
- API Reference: https://docs.cypress.io/api/table-of-contents

---

## Summary

**Total Time**: 45 minutes (5 min selection + 25 min setup + 10 min post-setup + 5 min validation)

**What You Built**:
- ✅ E2E testing framework (Playwright or Cypress)
- ✅ Page Object Model (reusable page logic)
- ✅ Authentication flow testing (session persistence)
- ✅ API mocking (fast, reliable tests)
- ✅ CI/CD integration (GitHub Actions)
- ✅ Visual regression (optional)

**Time Savings**: 6-8h → 45min = **90.6% reduction**

**Next Steps**: See [protocol-spec.md](./protocol-spec.md) for advanced patterns (How-To guides, tutorials, API reference).
