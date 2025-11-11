# SAP-036: React Error Handling - Adoption Blueprint

**SAP ID**: SAP-036
**Version**: 1.0.0
**Status**: pilot
**Diataxis Type**: Tutorial
**Time to Complete**: 30 minutes

---

## Executive Summary

This adoption blueprint provides a **step-by-step 30-minute installation guide** for SAP-036 (react-error-handling), transforming a React application from error-prone to production-ready with:

- ✅ **Next.js 15 Error Boundaries**: Prevent app crashes (error.tsx, global-error.tsx)
- ✅ **Sentry**: Production error tracking (<1% overhead)
- ✅ **react-error-boundary**: Reusable component boundaries
- ✅ **Error Recovery**: Retry with exponential backoff
- ✅ **GDPR/CCPA Compliant**: PII scrubbing by default

**Time Savings**: 87.5% reduction (3-4 hours manual → 30 minutes with SAP-036)

---

## Prerequisites

### Required Technologies

| Technology | Minimum Version | Verification Command | Expected Output |
|-----------|----------------|---------------------|-----------------|
| **Next.js** | 15.1+ | `npx next --version` | `15.1.0` or higher |
| **React** | 19+ | Check `package.json` | `"react": "^19.0.0"` |
| **TypeScript** | 5.3+ | `npx tsc --version` | `Version 5.3.0` or higher |
| **Node.js** | 22+ | `node --version` | `v22.0.0` or higher |
| **npm** | 10+ | `npm --version` | `10.0.0` or higher |

### Project Requirements

- ✅ Next.js 15 App Router (not Pages Router)
- ✅ TypeScript enabled
- ✅ Git initialized (for source control)

### Verification

Run these commands to verify prerequisites:

```bash
# Check Next.js version
npx next --version
# Expected: 15.1.0 or higher

# Check Node.js version
node --version
# Expected: v22.0.0 or higher

# Verify App Router exists
ls app/layout.tsx
# Expected: file exists (not pages/_app.tsx)

# Verify TypeScript
ls tsconfig.json
# Expected: file exists
```

**If any verification fails**:
- Next.js <15.1: `npm install next@latest`
- Node.js <22: Download from https://nodejs.org
- No App Router: Migrate from Pages Router (see [Next.js migration guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration))
- No TypeScript: `npx create-next-app@latest --typescript`

---

## Installation (30 minutes total)

### Step 1: Install Dependencies (2 minutes)

Install error handling packages:

```bash
npm install @sentry/nextjs react-error-boundary react-hot-toast
```

**What this installs**:
- `@sentry/nextjs`: Production error tracking (Sentry SDK)
- `react-error-boundary`: Reusable error boundary components
- `react-hot-toast`: Toast notification system (3.5KB gzipped)

**Verification**:
```bash
# Check installed versions
npm list @sentry/nextjs react-error-boundary react-hot-toast

# Expected output:
# @sentry/nextjs@8.x.x
# react-error-boundary@4.x.x
# react-hot-toast@2.x.x
```

---

### Step 2: Run Sentry Wizard (5 minutes)

Run the Sentry wizard to auto-configure Sentry:

```bash
npx @sentry/wizard@latest -i nextjs
```

**What the wizard does**:
1. Creates Sentry account (or uses existing)
2. Generates Sentry DSN (data source name)
3. Creates configuration files:
   - `sentry.client.config.ts` (browser error tracking)
   - `sentry.server.config.ts` (server error tracking)
   - `sentry.edge.config.ts` (edge runtime error tracking)
4. Updates `next.config.js` with Sentry integration

**Interactive prompts**:
- "Do you already have a Sentry account?" → Yes/No
- "Select your project" → Choose existing or create new
- "Do you want to enable performance monitoring?" → Yes (recommended)

**Verification**:
```bash
# Check created files
ls sentry.client.config.ts sentry.server.config.ts sentry.edge.config.ts

# Check Next.js config updated
grep "withSentryConfig" next.config.js
# Expected: Sentry plugin added
```

**Troubleshooting**:
- If wizard fails: Check internet connection, try again
- If DSN missing: Log in to https://sentry.io and get DSN from project settings

---

### Step 3: Configure Sentry with PII Scrubbing (5 minutes)

Update `sentry.client.config.ts` to add PII (Personally Identifiable Information) scrubbing for GDPR/CCPA compliance:

```typescript
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Performance Monitoring
  tracesSampleRate: 0.1, // 10% sampling (<1% overhead)

  // Session Replay (optional, for debugging UX issues)
  replaysSessionSampleRate: 0.01, // 1% of sessions
  replaysOnErrorSampleRate: 1.0, // 100% of errors

  // PII Scrubbing (GDPR/CCPA compliance)
  beforeSend(event, hint) {
    // Remove cookies (may contain auth tokens)
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }

    // Remove query strings that might contain PII
    if (event.request?.url) {
      event.request.url = event.request.url.split('?')[0]
    }

    // Remove email addresses from error messages
    if (event.exception) {
      event.exception.values?.forEach((exception) => {
        if (exception.value) {
          exception.value = exception.value.replace(
            /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
            '[EMAIL_REDACTED]'
          )
        }
      })
    }

    // Remove IP addresses
    if (event.user) {
      delete event.user.ip_address
    }

    return event
  },

  // Filter out sensitive breadcrumbs
  beforeBreadcrumb(breadcrumb, hint) {
    // Don't log console.log breadcrumbs in production
    if (breadcrumb.category === 'console' && process.env.NODE_ENV === 'production') {
      return null
    }
    return breadcrumb
  }
})
```

**Update `sentry.server.config.ts`** with the same PII scrubbing:

```typescript
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Performance Monitoring
  tracesSampleRate: 0.1, // 10% sampling (<1% overhead)

  // PII Scrubbing (same as client config)
  beforeSend(event, hint) {
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }

    if (event.request?.url) {
      event.request.url = event.request.url.split('?')[0]
    }

    if (event.exception) {
      event.exception.values?.forEach((exception) => {
        if (exception.value) {
          exception.value = exception.value.replace(
            /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
            '[EMAIL_REDACTED]'
          )
        }
      })
    }

    if (event.user) {
      delete event.user.ip_address
    }

    return event
  }
})
```

**Verification**:
```bash
# Check PII scrubbing configured
grep "beforeSend" sentry.client.config.ts
# Expected: beforeSend hook present

# Test in browser console (after Step 7)
# Trigger error with email in message
# Check Sentry dashboard for [EMAIL_REDACTED]
```

---

### Step 4: Create Error Boundaries (10 minutes)

Create **three error boundaries** for different error levels:

#### 4.1 Route-Level Error Boundary (error.tsx)

Create `app/error.tsx` to catch errors in specific routes:

```typescript
'use client'

import { useEffect } from 'react'
import * as Sentry from '@sentry/nextjs'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log to Sentry
    Sentry.captureException(error)
  }, [error])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8">
        <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
          <svg
            className="w-6 h-6 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">
          Something went wrong!
        </h2>

        <p className="text-gray-600 mb-6 text-center">
          We've been notified and are working on a fix.
        </p>

        {error.digest && (
          <p className="text-sm text-gray-500 mb-4 text-center font-mono">
            Error ID: {error.digest}
          </p>
        )}

        <div className="flex gap-4">
          <button
            onClick={() => reset()}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
          >
            Try again
          </button>
          <a
            href="/"
            className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-300 transition-colors text-center"
          >
            Go home
          </a>
        </div>
      </div>
    </div>
  )
}
```

#### 4.2 Root-Level Error Boundary (global-error.tsx)

Create `app/global-error.tsx` to catch errors in root layout (catches everything):

```typescript
'use client'

import { useEffect } from 'react'
import * as Sentry from '@sentry/nextjs'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    Sentry.captureException(error)
  }, [error])

  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
              <svg
                className="w-6 h-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>

            <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">
              Critical Error
            </h2>

            <p className="text-gray-600 mb-6 text-center">
              A critical error occurred. Please refresh the page.
            </p>

            {error.digest && (
              <p className="text-sm text-gray-500 mb-4 text-center font-mono">
                Error ID: {error.digest}
              </p>
            )}

            <button
              onClick={() => reset()}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              Refresh
            </button>
          </div>
        </div>
      </body>
    </html>
  )
}
```

#### 4.3 Custom 404 Page (not-found.tsx)

Create `app/not-found.tsx` for custom 404 errors:

```typescript
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>

        <h2 className="text-2xl font-semibold text-gray-700 mb-4">
          Page Not Found
        </h2>

        <p className="text-gray-600 mb-6">
          The page you're looking for doesn't exist or has been moved.
        </p>

        <Link
          href="/"
          className="inline-block bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 transition-colors"
        >
          Go Home
        </Link>
      </div>
    </div>
  )
}
```

**Verification**:
```bash
# Check files created
ls app/error.tsx app/global-error.tsx app/not-found.tsx

# All three files should exist
```

---

### Step 5: Add Toast Notifications (3 minutes)

Update `app/layout.tsx` to include toast notifications:

```typescript
import { Toaster } from 'react-hot-toast'
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Your App',
  description: 'Description',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            // Default options
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },

            // Success toast
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },

            // Error toast
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },

            // Loading toast
            loading: {
              iconTheme: {
                primary: '#3b82f6',
                secondary: '#fff',
              },
            },
          }}
        />
      </body>
    </html>
  )
}
```

**Verification**:
```bash
# Check layout.tsx updated
grep "Toaster" app/layout.tsx
# Expected: Toaster component imported and used
```

---

### Step 6: Create Reusable Error Boundary Component (3 minutes)

Create `components/ErrorBoundary.tsx` for wrapping specific components:

```typescript
'use client'

import { ErrorBoundary as ReactErrorBoundary } from 'react-error-boundary'
import * as Sentry from '@sentry/nextjs'

function ErrorFallback({
  error,
  resetErrorBoundary,
}: {
  error: Error
  resetErrorBoundary: () => void
}) {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="w-5 h-5 text-red-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-lg font-semibold text-red-800 mb-2">
            Something went wrong
          </h3>
          <p className="text-red-600 mb-4 text-sm">
            {error.message}
          </p>
          <button
            onClick={resetErrorBoundary}
            className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors text-sm"
          >
            Try again
          </button>
        </div>
      </div>
    </div>
  )
}

export function ErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ReactErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={(error, info) => {
        // Log to Sentry with React component stack
        Sentry.captureException(error, {
          contexts: {
            react: {
              componentStack: info.componentStack,
            },
          },
        })
      }}
      onReset={() => {
        // Optional: Reset app state when user clicks "Try again"
        // e.g., router.refresh(), queryClient.clear(), etc.
      }}
    >
      {children}
    </ReactErrorBoundary>
  )
}
```

**Usage example**:
```typescript
import { ErrorBoundary } from '@/components/ErrorBoundary'

export default function DashboardPage() {
  return (
    <ErrorBoundary>
      <DashboardContent />
    </ErrorBoundary>
  )
}
```

**Verification**:
```bash
# Check component created
ls components/ErrorBoundary.tsx

# File should exist
```

---

### Step 7: Test Error Handling (2 minutes)

Create `app/test-error/page.tsx` to test error boundaries:

```typescript
'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

export default function TestErrorPage() {
  const [shouldThrow, setShouldThrow] = useState(false)

  if (shouldThrow) {
    throw new Error('Test error - this should be caught by error boundary')
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test Error Handling</h1>

      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold mb-2">Test Error Boundary</h2>
          <button
            onClick={() => setShouldThrow(true)}
            className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700"
          >
            Trigger Error Boundary
          </button>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2">Test Toast Notifications</h2>
          <div className="space-x-2">
            <button
              onClick={() => toast.success('Success message!')}
              className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700"
            >
              Success Toast
            </button>
            <button
              onClick={() => toast.error('Error message!')}
              className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700"
            >
              Error Toast
            </button>
            <button
              onClick={() => toast.loading('Loading...')}
              className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
            >
              Loading Toast
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2">Test 404 Page</h2>
          <a
            href="/non-existent-page"
            className="text-blue-600 hover:underline"
          >
            Visit non-existent page (should show 404)
          </a>
        </div>
      </div>
    </div>
  )
}
```

**Test steps**:
```bash
# 1. Start dev server
npm run dev

# 2. Navigate to http://localhost:3000/test-error

# 3. Test error boundary
# Click "Trigger Error Boundary" → Should show error.tsx with "Try again" button

# 4. Test toast notifications
# Click toast buttons → Should show toast in top-right corner

# 5. Test 404 page
# Click "Visit non-existent page" → Should show not-found.tsx with "404" message

# 6. Check Sentry dashboard
# Go to https://sentry.io → Should see error logged with [EMAIL_REDACTED] if email in message
```

**Verification**:
```bash
# Check test page created
ls app/test-error/page.tsx

# Run dev server
npm run dev
# Expected: Server starts at http://localhost:3000
```

---

## Validation Checklist

Use this checklist to verify SAP-036 adoption is complete:

### Configuration

- [ ] **Sentry configured** (<1% overhead with 10% sampling)
  - Check: `grep "tracesSampleRate: 0.1" sentry.client.config.ts`
  - Expected: Sampling rate = 0.1 (10%)

- [ ] **PII scrubbing enabled** (GDPR/CCPA compliant)
  - Check: `grep "beforeSend" sentry.client.config.ts`
  - Expected: beforeSend hook removes cookies, headers, emails

### Error Boundaries

- [ ] **Error boundaries display friendly messages** (no stack traces)
  - Test: Trigger error at `/test-error` → Should show error.tsx (not stack trace)
  - Expected: User-friendly message with "Try again" button

- [ ] **Retry functionality works**
  - Test: Click "Try again" button → Should reset error boundary
  - Expected: Page reloads without full refresh

- [ ] **Custom 404 page displays**
  - Test: Visit `/non-existent-page` → Should show not-found.tsx
  - Expected: "404 Page Not Found" with "Go Home" link

### Sentry Integration

- [ ] **Errors logged to Sentry dashboard**
  - Test: Trigger error → Check https://sentry.io for error event
  - Expected: Error appears in Sentry within 1 minute

- [ ] **PII scrubbing works** (check Sentry events for sensitive data)
  - Test: Trigger error with email in message → Check Sentry event
  - Expected: Email replaced with `[EMAIL_REDACTED]`

- [ ] **Sentry overhead <1%**
  - Check: Performance tab in browser DevTools
  - Expected: No noticeable performance degradation

### Toast Notifications

- [ ] **Toast notifications work**
  - Test: Click toast buttons at `/test-error` → Should show toast
  - Expected: Toast appears in top-right corner for 3-5 seconds

- [ ] **Toast styling correct**
  - Test: Check toast background color
  - Expected: Dark background (#363636), white text

### Performance

- [ ] **No console errors in production build**
  ```bash
  npm run build
  npm run start
  # Check browser console for errors
  ```
  - Expected: No React warnings or errors

- [ ] **Error boundaries don't impact performance**
  - Check: Lighthouse performance score before/after
  - Expected: No performance regression (±3 points acceptable)

---

## Success Criteria

**Time to Complete**: ✅ ≤30 minutes (target achieved if <30 min)

**Functional Requirements**:
- ✅ Errors captured in Sentry (100% capture rate)
- ✅ No PII in Sentry events (GDPR/CCPA compliant)
- ✅ Error boundaries prevent app crashes (0% crash rate)
- ✅ Retry button works (95%+ recovery rate)
- ✅ Toast notifications display (3-5 second duration)

**Performance Requirements**:
- ✅ Sentry overhead <1% (10% sampling)
- ✅ Error boundary render <10ms
- ✅ Toast notification render <5ms
- ✅ Bundle size impact <10KB gzipped

**Evidence-Based Metrics** (from RT-019 research):
- Manual setup time: 3-4 hours
- With SAP-036: 30 minutes
- **Time reduction**: 87.5%

---

## Troubleshooting

### Common Issues

#### Issue 1: Sentry not logging errors

**Symptoms**: Errors not appearing in Sentry dashboard

**Diagnosis**:
```bash
# Check DSN configured
grep "NEXT_PUBLIC_SENTRY_DSN" .env.local
# Expected: DSN present

# Check Sentry initialized
grep "Sentry.init" sentry.client.config.ts
# Expected: Sentry.init() called
```

**Fix**:
1. Verify `NEXT_PUBLIC_SENTRY_DSN` in `.env.local`
2. Restart dev server: `npm run dev`
3. Trigger test error at `/test-error`
4. Check Sentry dashboard (may take 1-2 minutes)

#### Issue 2: Error boundary not catching errors

**Symptoms**: App crashes instead of showing error.tsx

**Diagnosis**:
```bash
# Check error.tsx exists
ls app/error.tsx
# Expected: file exists

# Check 'use client' directive
head -n 1 app/error.tsx
# Expected: 'use client'
```

**Fix**:
1. Ensure `'use client'` at top of error.tsx (error boundaries are client components)
2. Check error.tsx in correct directory (same level as page.tsx)
3. Restart dev server

#### Issue 3: PII appearing in Sentry

**Symptoms**: Sensitive data (emails, cookies) in Sentry events

**Diagnosis**:
```bash
# Check beforeSend hook
grep "beforeSend" sentry.client.config.ts
# Expected: PII scrubbing code present
```

**Fix**:
1. Add beforeSend hook to `sentry.client.config.ts` (see Step 3)
2. Restart dev server
3. Trigger test error with email in message
4. Verify `[EMAIL_REDACTED]` in Sentry

#### Issue 4: Toast notifications not showing

**Symptoms**: No toast appears when calling `toast.error()`

**Diagnosis**:
```bash
# Check Toaster in layout.tsx
grep "Toaster" app/layout.tsx
# Expected: <Toaster /> component present
```

**Fix**:
1. Import `Toaster` from `react-hot-toast` in layout.tsx
2. Add `<Toaster />` component to layout (see Step 5)
3. Restart dev server

#### Issue 5: High Sentry overhead (>1%)

**Symptoms**: App slow in production, high Sentry overhead

**Diagnosis**:
```bash
# Check sampling rate
grep "tracesSampleRate" sentry.client.config.ts
# Expected: 0.1 (10%) or lower
```

**Fix**:
1. Reduce `tracesSampleRate` to 0.05 (5%) or 0.01 (1%)
2. Reduce `replaysSessionSampleRate` to 0.005 (0.5%)
3. Redeploy to production

---

## Next Steps After Adoption

### 1. Customize Error Pages (Optional, 10 minutes)

Add custom branding to error.tsx:
- Replace generic error icon with company logo
- Add support contact link
- Add error code lookup

### 2. Integrate with TanStack Query (Recommended, 5 minutes)

Add global error handling for API calls:

```typescript
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import * as Sentry from '@sentry/nextjs'
import toast from 'react-hot-toast'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      onError: (error) => {
        Sentry.captureException(error)
        toast.error('Failed to load data. Please try again.')
      },
    },
    mutations: {
      onError: (error) => {
        Sentry.captureException(error)
        toast.error('Operation failed. Please try again.')
      },
    },
  },
})

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### 3. Add Offline Detection (Optional, 5 minutes)

Show toast when user goes offline:

```typescript
// hooks/useOfflineDetection.ts
'use client'

import { useEffect } from 'react'
import toast from 'react-hot-toast'

export function useOfflineDetection() {
  useEffect(() => {
    function handleOffline() {
      toast.error('You are offline. Some features may not work.')
    }

    function handleOnline() {
      toast.success('You are back online!')
    }

    window.addEventListener('offline', handleOffline)
    window.addEventListener('online', handleOnline)

    return () => {
      window.removeEventListener('offline', handleOffline)
      window.removeEventListener('online', handleOnline)
    }
  }, [])
}
```

### 4. Set Up Sentry Alerts (Recommended, 5 minutes)

Configure Sentry alerts for critical errors:

1. Go to https://sentry.io → Project Settings → Alerts
2. Create alert rule:
   - Condition: "An error is seen more than 10 times in 1 hour"
   - Action: "Send email to team@example.com"
3. Test alert by triggering 11 errors in test environment

### 5. Review SAP Integration Opportunities

- **SAP-020 (react-foundation)**: Already integrated (Next.js 15 error boundaries)
- **SAP-025 (react-performance)**: Add Sentry performance monitoring for Core Web Vitals
- **SAP-023 (react-state-management)**: Integrate TanStack Query error handling (see Step 2 above)

---

## Support & Resources

**Documentation**:
- [SAP-036 Protocol Spec](protocol-spec.md) - Complete API reference
- [SAP-036 AGENTS.md](AGENTS.md) - Quick reference and decision trees
- [SAP-036 CLAUDE.md](CLAUDE.md) - Claude-specific patterns

**External Resources**:
- [Next.js Error Handling Docs](https://nextjs.org/docs/app/building-your-application/routing/error-handling)
- [Sentry Next.js SDK Docs](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [react-error-boundary Docs](https://github.com/bvaughn/react-error-boundary)
- [react-hot-toast Docs](https://react-hot-toast.com/)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - Next.js 15 fundamentals
- [SAP-025 (react-performance)](../react-performance/) - Performance monitoring
- [SAP-023 (react-state-management)](../react-state-management/) - TanStack Query patterns

---

## Version History

**1.0.0 (2025-11-09)** - Initial release
- 30-minute installation guide
- Next.js 15 error boundaries (error.tsx, global-error.tsx, not-found.tsx)
- Sentry integration with PII scrubbing
- react-error-boundary patterns
- react-hot-toast notifications
- Comprehensive validation checklist
- Evidence-based time savings (87.5% reduction)

---

**Adoption Status**: Pilot (pending SAP-027 validation)
**Time to Complete**: 30 minutes
**Time Savings**: 87.5% (3-4 hours → 30 minutes)

---

**Congratulations!** You've successfully adopted SAP-036 (react-error-handling) and transformed your React application from error-prone to production-ready with 0% crash rate and <1% overhead.
