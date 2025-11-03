/**
 * Next.js 15 Instrumentation
 *
 * SAP-025: React Performance Optimization
 *
 * This file runs once when the Next.js server starts.
 * Use it to initialize monitoring, tracing, and Web Vitals collection.
 *
 * @see https://nextjs.org/docs/app/building-your-application/optimizing/instrumentation
 */

/**
 * Register function that runs once on server startup
 *
 * This is the ideal place to:
 * - Initialize APM (Application Performance Monitoring) tools
 * - Set up error tracking (e.g., Sentry)
 * - Configure Web Vitals reporting
 * - Initialize database connections
 */
export async function register() {
  // ============================================
  // ENVIRONMENT CHECK
  // ============================================

  // Only run instrumentation in production or when explicitly enabled
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    console.log('[Instrumentation] Running in Node.js runtime')

    // ============================================
    // WEB VITALS MONITORING
    // ============================================

    // Log Web Vitals to console (useful for local testing)
    if (process.env.NODE_ENV === 'development') {
      console.log('[Instrumentation] Web Vitals logging enabled')
    }

    // ============================================
    // APM SETUP (e.g., Vercel Analytics, Sentry, etc.)
    // ============================================

    // Example: Sentry initialization
    // if (process.env.SENTRY_DSN) {
    //   const Sentry = await import('@sentry/nextjs')
    //   Sentry.init({
    //     dsn: process.env.SENTRY_DSN,
    //     tracesSampleRate: 0.1, // Sample 10% of transactions
    //     environment: process.env.NODE_ENV,
    //   })
    //   console.log('[Instrumentation] Sentry initialized')
    // }

    // Example: Vercel Analytics initialization
    // if (process.env.VERCEL_ANALYTICS_ID) {
    //   console.log('[Instrumentation] Vercel Analytics enabled')
    // }

    // ============================================
    // OPENTELEMETRY (optional)
    // ============================================

    // Example: OpenTelemetry setup for distributed tracing
    // const { NodeSDK } = await import('@opentelemetry/sdk-node')
    // const { getNodeAutoInstrumentations } = await import(
    //   '@opentelemetry/auto-instrumentations-node'
    // )
    //
    // const sdk = new NodeSDK({
    //   traceExporter: new ConsoleSpanExporter(),
    //   instrumentations: [getNodeAutoInstrumentations()],
    // })
    //
    // sdk.start()
    // console.log('[Instrumentation] OpenTelemetry initialized')

    // ============================================
    // CUSTOM MONITORING
    // ============================================

    // Example: Custom performance monitoring
    // setupCustomMonitoring()

    console.log('[Instrumentation] Setup complete')
  }

  // ============================================
  // EDGE RUNTIME
  // ============================================

  if (process.env.NEXT_RUNTIME === 'edge') {
    console.log('[Instrumentation] Running in Edge runtime')
    // Edge runtime has limited APIs - be careful what you initialize here
  }
}

/**
 * Example: Custom monitoring setup
 *
 * This function demonstrates how to set up custom performance monitoring.
 */
function setupCustomMonitoring() {
  // Track server startup time
  const startupTime = Date.now()

  // Log memory usage
  if (process.memoryUsage) {
    const memory = process.memoryUsage()
    console.log('[Instrumentation] Memory usage:', {
      rss: `${Math.round(memory.rss / 1024 / 1024)}MB`,
      heapTotal: `${Math.round(memory.heapTotal / 1024 / 1024)}MB`,
      heapUsed: `${Math.round(memory.heapUsed / 1024 / 1024)}MB`,
    })
  }

  // Track server startup duration
  const startupDuration = Date.now() - startupTime
  console.log(`[Instrumentation] Server started in ${startupDuration}ms`)
}

/**
 * Optional: onRequestError handler for catching errors
 *
 * This is an experimental Next.js feature that allows you to catch
 * errors during request handling.
 *
 * @see https://nextjs.org/docs/app/api-reference/next-config-js/onRequestError
 */
// export async function onRequestError(
//   err: Error,
//   request: Request,
//   context: { routerKind: 'app' | 'pages'; routePath: string }
// ) {
//   console.error('[Instrumentation] Request error:', {
//     error: err.message,
//     stack: err.stack,
//     url: request.url,
//     method: request.method,
//     routerKind: context.routerKind,
//     routePath: context.routePath,
//   })
//
//   // Send to error tracking service (e.g., Sentry)
//   // if (process.env.SENTRY_DSN) {
//   //   const Sentry = await import('@sentry/nextjs')
//   //   Sentry.captureException(err, {
//   //     contexts: {
//   //       request: {
//   //         url: request.url,
//   //         method: request.method,
//   //       },
//   //       nextjs: {
//   //         routerKind: context.routerKind,
//   //         routePath: context.routePath,
//   //       },
//   //     },
//   //   })
//   // }
// }
