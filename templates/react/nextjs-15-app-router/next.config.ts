import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Turbopack configuration (dev mode only)
  experimental: {
    // Enable Turbopack for faster dev server
    turbo: {
      rules: {
        // Custom Turbopack rules can be added here
      },
    },
  },

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    // Add your CDN domains here
    remotePatterns: [
      // Example:
      // {
      //   protocol: 'https',
      //   hostname: 'cdn.example.com',
      // },
    ],
  },

  // TypeScript configuration
  typescript: {
    // Fail build on type errors
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    // Fail build on linting errors
    ignoreDuringBuilds: false,
  },
}

export default nextConfig
