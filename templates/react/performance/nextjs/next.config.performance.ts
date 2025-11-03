/**
 * Next.js 15 Performance Configuration
 *
 * SAP-025: React Performance Optimization
 *
 * This configuration optimizes Next.js applications for Core Web Vitals:
 * - Image optimization (AVIF/WebP formats)
 * - Bundle analysis
 * - Compression
 * - Package import optimization
 *
 * @see https://nextjs.org/docs/app/api-reference/next-config-js
 */

import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // ============================================
  // IMAGE OPTIMIZATION
  // ============================================
  images: {
    // Modern image formats (AVIF is 20% smaller than WebP)
    formats: ['image/avif', 'image/webp'],

    // Remote image patterns (configure for your CDN)
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        port: '',
        pathname: '/images/**',
      },
    ],

    // Cache TTL for optimized images (60 seconds)
    minimumCacheTTL: 60,

    // Device sizes for responsive images
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],

    // Image sizes for different layouts
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

    // Disable image optimization during development (faster builds)
    unoptimized: process.env.NODE_ENV === 'development',
  },

  // ============================================
  // COMPRESSION
  // ============================================
  // Enable gzip/brotli compression
  compress: true,

  // ============================================
  // BUNDLE ANALYSIS
  // ============================================
  webpack: (config, { isServer }) => {
    // Bundle analysis (run with ANALYZE=true npm run build)
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer
            ? '../analyze/server.html'
            : './analyze/client.html',
          openAnalyzer: false,
          generateStatsFile: true,
          statsFilename: isServer
            ? '../analyze/server.json'
            : './analyze/client.json',
        })
      )
    }

    return config
  },

  // ============================================
  // EXPERIMENTAL OPTIMIZATIONS
  // ============================================
  experimental: {
    // Optimize package imports (reduces bundle size)
    optimizePackageImports: [
      '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu',
      '@radix-ui/react-select',
      '@radix-ui/react-tabs',
      'lucide-react',
      'date-fns',
      'lodash',
    ],

    // Server Actions body size limit (2MB)
    serverActions: {
      bodySizeLimit: '2mb',
    },

    // Turbopack (faster builds, Next.js 15+)
    turbo: {
      // Enable Turbopack for development (optional)
      // Note: Remove this if you encounter issues
    },
  },

  // ============================================
  // PERFORMANCE HEADERS
  // ============================================
  async headers() {
    return [
      {
        // Apply to all routes
        source: '/:path*',
        headers: [
          // Security headers
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
      {
        // Cache static assets (fonts, images, CSS, JS)
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ]
  },

  // ============================================
  // REDIRECTS & REWRITES
  // ============================================
  // Add permanent redirects for SEO (optional)
  // async redirects() {
  //   return [
  //     {
  //       source: '/old-route',
  //       destination: '/new-route',
  //       permanent: true,
  //     },
  //   ]
  // },

  // ============================================
  // OUTPUT
  // ============================================
  // Output mode (default: standalone)
  output: 'standalone',

  // ============================================
  // TYPESCRIPT
  // ============================================
  typescript: {
    // Type checking during builds
    ignoreBuildErrors: false,
  },

  // ============================================
  // ESLINT
  // ============================================
  eslint: {
    // Linting during builds
    ignoreDuringBuilds: false,
  },

  // ============================================
  // PRODUCTION SOURCE MAPS
  // ============================================
  // Disable source maps in production (reduces bundle size)
  productionBrowserSourceMaps: false,

  // ============================================
  // POWER BY HEADER
  // ============================================
  // Remove X-Powered-By header (security)
  poweredByHeader: false,
}

export default nextConfig
