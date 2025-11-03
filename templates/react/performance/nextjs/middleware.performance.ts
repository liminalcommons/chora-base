/**
 * Next.js 15 Performance Middleware
 *
 * SAP-025: React Performance Optimization
 *
 * This middleware injects performance and security headers on every request.
 * It also handles Web Vitals reporting endpoints.
 *
 * @see https://nextjs.org/docs/app/building-your-application/routing/middleware
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Middleware function that runs before each request
 *
 * @param request - The incoming request
 * @returns NextResponse with performance headers
 */
export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // ============================================
  // PERFORMANCE HEADERS
  // ============================================

  // Enable DNS prefetch (resolve domain names early)
  response.headers.set('X-DNS-Prefetch-Control', 'on')

  // ============================================
  // SECURITY HEADERS
  // ============================================

  // Prevent clickjacking (disallow embedding in iframes)
  response.headers.set('X-Frame-Options', 'DENY')

  // Prevent MIME type sniffing
  response.headers.set('X-Content-Type-Options', 'nosniff')

  // Referrer policy (control what information is sent in Referer header)
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

  // ============================================
  // CACHE CONTROL (for static assets)
  // ============================================

  const pathname = request.nextUrl.pathname

  // Cache static assets (fonts, images, CSS, JS) for 1 year
  if (
    pathname.startsWith('/static/') ||
    pathname.startsWith('/_next/static/') ||
    pathname.match(/\.(woff2|woff|ttf|jpg|jpeg|png|webp|avif|svg|ico|css|js)$/)
  ) {
    response.headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  }

  // Cache HTML pages for 60 seconds (stale-while-revalidate pattern)
  if (pathname.endsWith('/') || pathname.match(/\.html?$/)) {
    response.headers.set(
      'Cache-Control',
      'public, max-age=60, stale-while-revalidate=86400'
    )
  }

  // ============================================
  // CONTENT SECURITY POLICY (CSP)
  // ============================================

  // Uncomment and configure CSP for production
  // const cspHeader = `
  //   default-src 'self';
  //   script-src 'self' 'unsafe-eval' 'unsafe-inline';
  //   style-src 'self' 'unsafe-inline';
  //   img-src 'self' data: blob: https:;
  //   font-src 'self' data:;
  //   connect-src 'self' https:;
  //   frame-ancestors 'none';
  // `.replace(/\s{2,}/g, ' ').trim()
  //
  // response.headers.set('Content-Security-Policy', cspHeader)

  // ============================================
  // CORS (if needed for API routes)
  // ============================================

  if (pathname.startsWith('/api/')) {
    // Allow CORS for API routes (configure origins as needed)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set(
      'Access-Control-Allow-Methods',
      'GET, POST, PUT, DELETE, OPTIONS'
    )
    response.headers.set(
      'Access-Control-Allow-Headers',
      'Content-Type, Authorization'
    )

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new NextResponse(null, { status: 200, headers: response.headers })
    }
  }

  return response
}

/**
 * Middleware configuration
 *
 * Specify which paths the middleware should run on.
 * Use negative lookahead to exclude specific paths.
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/web-vitals (already handled by route handler)
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico (favicon)
     */
    '/((?!api/web-vitals|_next/static|_next/image|favicon.ico).*)',
  ],
}
