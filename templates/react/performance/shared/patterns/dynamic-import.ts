/**
 * Dynamic Import Utilities
 *
 * SAP-025: React Performance Optimization
 *
 * This module provides utilities for dynamic imports with:
 * - Retry logic (handle network failures)
 * - Timeout handling (prevent hanging imports)
 * - Preloading (load before needed)
 * - Error tracking
 *
 * Use cases:
 * - Load heavy libraries on-demand (e.g., PDF.js, Chart.js)
 * - Load feature modules conditionally (e.g., admin panel)
 * - Load polyfills for older browsers
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import
 */

// ============================================
// DYNAMIC IMPORT WITH RETRY
// ============================================

/**
 * Dynamic import with retry logic
 *
 * Retries the import up to N times if it fails (e.g., network error).
 * Useful for unreliable networks or CDN failures.
 *
 * @param importFunc - Function that returns a dynamic import
 * @param retries - Number of retries (default: 3)
 * @param delay - Delay between retries in ms (default: 1000)
 * @returns Promise that resolves to the imported module
 *
 * @example
 * const Chart = await importWithRetry(() => import('chart.js'))
 */
export async function importWithRetry<T>(
  importFunc: () => Promise<T>,
  retries = 3,
  delay = 1000
): Promise<T> {
  try {
    return await importFunc()
  } catch (error) {
    if (retries <= 0) {
      console.error('Failed to import after retries:', error)
      throw error
    }

    console.warn(`Import failed, retrying... (${retries} attempts left)`)

    // Wait before retrying (exponential backoff)
    await new Promise((resolve) => setTimeout(resolve, delay))

    // Retry with exponential backoff (delay * 2)
    return importWithRetry(importFunc, retries - 1, delay * 2)
  }
}

// ============================================
// DYNAMIC IMPORT WITH TIMEOUT
// ============================================

/**
 * Dynamic import with timeout
 *
 * Throws an error if the import takes longer than the timeout.
 * Prevents hanging imports on slow networks.
 *
 * @param importFunc - Function that returns a dynamic import
 * @param timeout - Timeout in ms (default: 10000 = 10 seconds)
 * @returns Promise that resolves to the imported module
 *
 * @example
 * const Chart = await importWithTimeout(() => import('chart.js'), 5000)
 */
export async function importWithTimeout<T>(
  importFunc: () => Promise<T>,
  timeout = 10000
): Promise<T> {
  return Promise.race([
    importFunc(),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('Import timeout')), timeout)
    ),
  ])
}

// ============================================
// DYNAMIC IMPORT WITH RETRY + TIMEOUT
// ============================================

/**
 * Dynamic import with retry + timeout
 *
 * Combines retry logic and timeout handling.
 * This is the recommended approach for production.
 *
 * @param importFunc - Function that returns a dynamic import
 * @param options - Configuration options
 * @returns Promise that resolves to the imported module
 *
 * @example
 * const Chart = await importWithRetryAndTimeout(() => import('chart.js'), {
 *   retries: 3,
 *   timeout: 5000,
 *   delay: 1000,
 * })
 */
export async function importWithRetryAndTimeout<T>(
  importFunc: () => Promise<T>,
  options: {
    retries?: number
    timeout?: number
    delay?: number
  } = {}
): Promise<T> {
  const { retries = 3, timeout = 10000, delay = 1000 } = options

  const importWithTimeoutWrapper = () => importWithTimeout(importFunc, timeout)

  return importWithRetry(importWithTimeoutWrapper, retries, delay)
}

// ============================================
// PRELOAD UTILITY
// ============================================

/**
 * Preload a module without executing it
 *
 * This loads the module in the background, so it's available
 * instantly when needed. Useful for preloading on hover.
 *
 * @param importFunc - Function that returns a dynamic import
 * @returns Promise that resolves when module is preloaded
 *
 * @example
 * // Preload on hover
 * <Link
 *   to="/dashboard"
 *   onMouseEnter={() => preloadModule(() => import('@/pages/dashboard'))}
 * >
 *   Dashboard
 * </Link>
 */
export function preloadModule<T>(importFunc: () => Promise<T>): Promise<T> {
  return importFunc()
}

// ============================================
// CONDITIONAL IMPORT
// ============================================

/**
 * Conditionally import a module
 *
 * Only imports the module if a condition is met.
 * Useful for feature flags or environment-based imports.
 *
 * @param condition - Condition to check
 * @param importFunc - Function that returns a dynamic import
 * @returns Promise that resolves to the imported module or null
 *
 * @example
 * // Only import admin panel for admin users
 * const AdminPanel = await conditionalImport(
 *   user.role === 'admin',
 *   () => import('@/components/admin-panel')
 * )
 */
export async function conditionalImport<T>(
  condition: boolean,
  importFunc: () => Promise<T>
): Promise<T | null> {
  if (!condition) {
    return null
  }

  return importFunc()
}

// ============================================
// BATCH IMPORT
// ============================================

/**
 * Import multiple modules in parallel
 *
 * This is faster than importing modules sequentially.
 *
 * @param importFuncs - Array of import functions
 * @returns Promise that resolves to an array of imported modules
 *
 * @example
 * const [Chart, Table, Map] = await batchImport([
 *   () => import('chart.js'),
 *   () => import('react-table'),
 *   () => import('mapbox-gl'),
 * ])
 */
export async function batchImport<T>(
  importFuncs: (() => Promise<T>)[]
): Promise<T[]> {
  return Promise.all(importFuncs.map((func) => func()))
}

// ============================================
// LAZY LOAD POLYFILL
// ============================================

/**
 * Lazy load polyfill for older browsers
 *
 * Checks if a feature is supported, and loads a polyfill if not.
 *
 * @param featureCheck - Function that returns true if feature is supported
 * @param polyfillImport - Function that returns a dynamic import
 * @returns Promise that resolves when polyfill is loaded (or immediately if not needed)
 *
 * @example
 * // Load IntersectionObserver polyfill for older browsers
 * await lazyLoadPolyfill(
 *   () => 'IntersectionObserver' in window,
 *   () => import('intersection-observer')
 * )
 */
export async function lazyLoadPolyfill(
  featureCheck: () => boolean,
  polyfillImport: () => Promise<any>
): Promise<void> {
  if (!featureCheck()) {
    console.log('Loading polyfill...')
    await polyfillImport()
    console.log('Polyfill loaded')
  }
}

// ============================================
// ERROR TRACKING
// ============================================

/**
 * Import with error tracking
 *
 * Tracks import errors to an analytics service (e.g., Sentry).
 *
 * @param importFunc - Function that returns a dynamic import
 * @param moduleName - Name of the module (for error tracking)
 * @returns Promise that resolves to the imported module
 *
 * @example
 * const Chart = await importWithErrorTracking(
 *   () => import('chart.js'),
 *   'chart.js'
 * )
 */
export async function importWithErrorTracking<T>(
  importFunc: () => Promise<T>,
  moduleName: string
): Promise<T> {
  try {
    return await importFunc()
  } catch (error) {
    // Log error to console
    console.error(`Failed to import ${moduleName}:`, error)

    // Track error in analytics (e.g., Sentry, Google Analytics)
    trackImportError(moduleName, error)

    throw error
  }
}

/**
 * Track import error to analytics
 *
 * @param moduleName - Name of the module
 * @param error - Error object
 */
function trackImportError(moduleName: string, error: unknown) {
  // Example: Send to Google Analytics
  if (typeof window !== 'undefined' && 'gtag' in window) {
    ;(window as any).gtag('event', 'exception', {
      description: `Import error: ${moduleName}`,
      fatal: false,
    })
  }

  // Example: Send to Sentry
  // if (typeof window !== 'undefined' && 'Sentry' in window) {
  //   (window as any).Sentry.captureException(error, {
  //     tags: { moduleName, errorType: 'import_error' },
  //   })
  // }

  // Example: Send to custom analytics endpoint
  // fetch('/api/analytics/import-error', {
  //   method: 'POST',
  //   body: JSON.stringify({ moduleName, error: String(error) }),
  // })
}

// ============================================
// USAGE EXAMPLES
// ============================================

/**
 * Example 1: Load chart library with retry + timeout
 */
export async function loadChartLibrary() {
  try {
    const ChartJS = await importWithRetryAndTimeout(() => import('chart.js'), {
      retries: 3,
      timeout: 5000,
      delay: 1000,
    })

    console.log('Chart.js loaded successfully')
    return ChartJS
  } catch (error) {
    console.error('Failed to load Chart.js:', error)
    throw error
  }
}

/**
 * Example 2: Preload module on hover
 */
export function setupHoverPreload() {
  const link = document.querySelector('a[href="/dashboard"]')

  if (link) {
    link.addEventListener('mouseenter', () => {
      preloadModule(() => import('@/pages/dashboard'))
    })
  }
}

/**
 * Example 3: Load polyfills for older browsers
 */
export async function loadPolyfills() {
  // Load IntersectionObserver polyfill
  await lazyLoadPolyfill(
    () => 'IntersectionObserver' in window,
    () => import('intersection-observer')
  )

  // Load ResizeObserver polyfill
  await lazyLoadPolyfill(
    () => 'ResizeObserver' in window,
    () => import('resize-observer-polyfill')
  )

  console.log('Polyfills loaded')
}

/**
 * Example 4: Batch import multiple libraries
 */
export async function loadAnalyticsLibraries() {
  const [GA, Sentry, Mixpanel] = await batchImport([
    () => import('react-ga4'),
    () => import('@sentry/react'),
    () => import('mixpanel-browser'),
  ])

  console.log('Analytics libraries loaded')
  return { GA, Sentry, Mixpanel }
}

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Use importWithRetryAndTimeout() for production (handles network failures)
 * 2. Preload modules on hover for better perceived performance
 * 3. Use conditional imports for feature flags (don't load unused code)
 * 4. Batch import multiple modules in parallel (faster than sequential)
 * 5. Track import errors to analytics (identify problematic modules)
 * 6. Set reasonable timeouts (5-10 seconds for most imports)
 * 7. Use exponential backoff for retries (avoid hammering the server)
 * 8. Test on slow 3G network to verify retry logic works
 *
 * CORE WEB VITALS IMPACT:
 * - LCP: Faster imports → faster content rendering
 * - INP: Retry logic → fewer failed interactions
 * - FCP: Preloading → faster first meaningful paint
 */
