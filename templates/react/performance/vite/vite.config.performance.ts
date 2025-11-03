/**
 * Vite 7 Performance Configuration
 *
 * SAP-025: React Performance Optimization
 *
 * This configuration optimizes Vite applications for Core Web Vitals:
 * - Code splitting with manual chunks
 * - Bundle visualization
 * - Compression (gzip/brotli)
 * - Tree shaking
 *
 * @see https://vite.dev/config/
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'
import { compression } from 'vite-plugin-compression2'
import path from 'path'

export default defineConfig({
  plugins: [
    // ============================================
    // REACT PLUGIN
    // ============================================
    react({
      // Enable Fast Refresh for development
      fastRefresh: true,

      // Babel configuration (optional)
      babel: {
        plugins: [],
      },
    }),

    // ============================================
    // BUNDLE VISUALIZATION
    // ============================================
    visualizer({
      // Output file for bundle analysis
      filename: 'dist/stats.html',

      // Open in browser after build
      open: false,

      // Show gzip and brotli sizes
      gzipSize: true,
      brotliSize: true,

      // Template type (sunburst, treemap, network)
      template: 'treemap',

      // Generate JSON stats file
      sourcemap: true,
    }),

    // ============================================
    // COMPRESSION (GZIP + BROTLI)
    // ============================================
    compression({
      // Algorithm: gzip
      algorithm: 'gzip',
      // Compression threshold (only compress files > 10KB)
      threshold: 10240,
      // Delete original files after compression (false = keep both)
      deleteOriginalAssets: false,
    }),
    compression({
      // Algorithm: brotli (better compression than gzip)
      algorithm: 'brotliCompress',
      // Compression threshold (only compress files > 10KB)
      threshold: 10240,
      // Delete original files after compression (false = keep both)
      deleteOriginalAssets: false,
    }),
  ],

  // ============================================
  // RESOLVE (PATH ALIASES)
  // ============================================
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@lib': path.resolve(__dirname, './src/lib'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@styles': path.resolve(__dirname, './src/styles'),
    },
  },

  // ============================================
  // BUILD CONFIGURATION
  // ============================================
  build: {
    // Output directory
    outDir: 'dist',

    // Generate sourcemaps (false in production for smaller bundles)
    sourcemap: process.env.NODE_ENV === 'development',

    // Minification (terser is slower but produces smaller bundles)
    minify: 'terser',

    // Terser options
    terserOptions: {
      compress: {
        // Remove console.log in production
        drop_console: process.env.NODE_ENV === 'production',
        // Remove debugger statements
        drop_debugger: true,
      },
    },

    // Chunk size warning limit (500KB)
    chunkSizeWarningLimit: 500,

    // Rollup options
    rollupOptions: {
      output: {
        // ============================================
        // MANUAL CHUNKS (CODE SPLITTING)
        // ============================================
        manualChunks: (id) => {
          // Vendor chunk (React, React DOM, React Router)
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'vendor-react'
          }

          if (id.includes('node_modules/react-router-dom')) {
            return 'vendor-router'
          }

          // React Query chunk
          if (id.includes('node_modules/@tanstack/react-query')) {
            return 'vendor-query'
          }

          // UI library chunk (Radix UI)
          if (id.includes('node_modules/@radix-ui')) {
            return 'vendor-ui'
          }

          // Icon library chunk (Lucide)
          if (id.includes('node_modules/lucide-react')) {
            return 'vendor-icons'
          }

          // Date library chunk (date-fns)
          if (id.includes('node_modules/date-fns')) {
            return 'vendor-date'
          }

          // Utility library chunk (lodash)
          if (id.includes('node_modules/lodash')) {
            return 'vendor-lodash'
          }

          // Other node_modules (shared vendor chunk)
          if (id.includes('node_modules')) {
            return 'vendor-other'
          }
        },

        // Chunk file names ([name] = chunk name, [hash] = content hash)
        chunkFileNames: 'assets/js/[name]-[hash].js',

        // Entry file names
        entryFileNames: 'assets/js/[name]-[hash].js',

        // Asset file names (CSS, images, fonts)
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.')
          const ext = info[info.length - 1]

          // CSS files
          if (ext === 'css') {
            return 'assets/css/[name]-[hash][extname]'
          }

          // Image files
          if (/png|jpe?g|svg|gif|webp|avif|ico/i.test(ext)) {
            return 'assets/images/[name]-[hash][extname]'
          }

          // Font files
          if (/woff2?|ttf|otf|eot/i.test(ext)) {
            return 'assets/fonts/[name]-[hash][extname]'
          }

          // Other assets
          return 'assets/[name]-[hash][extname]'
        },
      },
    },

    // ============================================
    // CSS CODE SPLITTING
    // ============================================
    cssCodeSplit: true,

    // ============================================
    // ASSET INLINE LIMIT
    // ============================================
    // Inline assets smaller than 4KB as base64 (reduces HTTP requests)
    assetsInlineLimit: 4096,
  },

  // ============================================
  // SERVER CONFIGURATION (DEVELOPMENT)
  // ============================================
  server: {
    port: 3000,
    open: false,
    cors: true,
    // Enable HMR (Hot Module Replacement)
    hmr: true,
  },

  // ============================================
  // PREVIEW CONFIGURATION (PRODUCTION)
  // ============================================
  preview: {
    port: 4173,
    open: false,
  },

  // ============================================
  // OPTIMIZATIONS
  // ============================================
  optimizeDeps: {
    // Pre-bundle dependencies for faster dev server startup
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      '@tanstack/react-query',
    ],
  },

  // ============================================
  // ESBUILD (FAST TRANSFORMS)
  // ============================================
  esbuild: {
    // Drop console.log in production
    drop: process.env.NODE_ENV === 'production' ? ['console', 'debugger'] : [],
    // JSX factory (automatic for React 17+)
    jsxInject: `import React from 'react'`,
  },
})
