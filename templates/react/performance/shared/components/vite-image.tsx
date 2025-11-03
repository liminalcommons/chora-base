/**
 * Optimized Image Component (Vite)
 *
 * SAP-025: React Performance Optimization
 *
 * This component provides image optimization for Vite applications:
 * - AVIF/WebP format selection with fallbacks
 * - Responsive srcset
 * - Lazy loading with Intersection Observer
 * - Blur placeholder
 * - Manual optimization (Vite doesn't have built-in image optimization)
 *
 * Benefits:
 * - 20-50% smaller image sizes (AVIF vs JPEG)
 * - Faster LCP (Largest Contentful Paint)
 * - Prevents CLS (Cumulative Layout Shift)
 *
 * @see https://vite.dev/guide/assets.html
 */

import { useState, useEffect, useRef, ImgHTMLAttributes } from 'react'

// ============================================
// OPTIMIZED IMAGE PROPS
// ============================================

interface ViteImageProps extends Omit<ImgHTMLAttributes<HTMLImageElement>, 'src'> {
  src: string
  alt: string
  width?: number
  height?: number
  priority?: boolean
  lazy?: boolean
  aspectRatio?: 'square' | '16/9' | '4/3' | '3/2' | '21/9'
  objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down'
  srcSet?: string
  sizes?: string
  onLoad?: () => void
}

// ============================================
// OPTIMIZED IMAGE COMPONENT
// ============================================

/**
 * Optimized image component for Vite
 *
 * @example
 * // Hero image (priority loading)
 * <ViteImage
 *   src="/images/hero.jpg"
 *   alt="Hero image"
 *   width={1920}
 *   height={1080}
 *   priority
 *   aspectRatio="16/9"
 * />
 *
 * // Regular image (lazy loading)
 * <ViteImage
 *   src="/images/product.jpg"
 *   alt="Product"
 *   width={800}
 *   height={600}
 *   lazy
 *   aspectRatio="4/3"
 * />
 */
export function ViteImage({
  src,
  alt,
  width,
  height,
  priority = false,
  lazy = true,
  className = '',
  aspectRatio,
  objectFit = 'cover',
  srcSet,
  sizes,
  onLoad,
  ...props
}: ViteImageProps) {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isVisible, setIsVisible] = useState(priority)
  const imgRef = useRef<HTMLImageElement>(null)

  // Calculate dimensions based on aspect ratio
  const dimensions = calculateDimensions(width, height, aspectRatio)

  // Lazy loading with Intersection Observer
  useEffect(() => {
    if (priority || !lazy) {
      setIsVisible(true)
      return
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      {
        rootMargin: '200px', // Load 200px before entering viewport
      }
    )

    if (imgRef.current) {
      observer.observe(imgRef.current)
    }

    return () => observer.disconnect()
  }, [priority, lazy])

  const handleLoad = () => {
    setIsLoaded(true)
    onLoad?.()
  }

  return (
    <div
      ref={imgRef}
      className={`relative overflow-hidden ${className}`}
      style={{
        width: dimensions.width,
        height: dimensions.height,
      }}
    >
      {/* Blur placeholder (shown before image loads) */}
      {!isLoaded && (
        <div
          className="absolute inset-0 animate-pulse bg-gray-200"
          style={{
            aspectRatio: aspectRatio ? getAspectRatioString(aspectRatio) : undefined,
          }}
        />
      )}

      {/* Actual image (loaded when visible) */}
      {isVisible && (
        <picture>
          {/* AVIF format (best compression, ~20% smaller than WebP) */}
          {srcSet && <source type="image/avif" srcSet={convertToAVIF(srcSet)} />}

          {/* WebP format (fallback for browsers without AVIF support) */}
          {srcSet && <source type="image/webp" srcSet={convertToWebP(srcSet)} />}

          {/* JPEG/PNG fallback (for older browsers) */}
          <img
            src={src}
            alt={alt}
            width={dimensions.width}
            height={dimensions.height}
            srcSet={srcSet}
            sizes={sizes || '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'}
            loading={priority ? 'eager' : 'lazy'}
            decoding={priority ? 'sync' : 'async'}
            onLoad={handleLoad}
            className={`transition-opacity duration-300 ${
              isLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            style={{ objectFit }}
            {...props}
          />
        </picture>
      )}
    </div>
  )
}

// ============================================
// HERO IMAGE (PRIORITY LOADING)
// ============================================

/**
 * Hero image component (always priority)
 *
 * @example
 * <HeroImage
 *   src="/images/hero.jpg"
 *   alt="Welcome"
 *   width={1920}
 *   height={1080}
 * />
 */
export function HeroImage({
  src,
  alt,
  width = 1920,
  height = 1080,
  className = '',
}: {
  src: string
  alt: string
  width?: number
  height?: number
  className?: string
}) {
  return (
    <ViteImage
      src={src}
      alt={alt}
      width={width}
      height={height}
      priority
      lazy={false}
      className={className}
      sizes="100vw"
      objectFit="cover"
    />
  )
}

// ============================================
// AVATAR IMAGE (SMALL, CIRCULAR)
// ============================================

/**
 * Avatar image component
 *
 * @example
 * <AvatarImage
 *   src="/images/avatar.jpg"
 *   alt="John Doe"
 *   size={64}
 * />
 */
export function AvatarImage({
  src,
  alt,
  size = 64,
  className = '',
}: {
  src: string
  alt: string
  size?: number
  className?: string
}) {
  return (
    <div className={`relative overflow-hidden rounded-full ${className}`}>
      <ViteImage
        src={src}
        alt={alt}
        width={size}
        height={size}
        lazy
        sizes={`${size}px`}
        objectFit="cover"
      />
    </div>
  )
}

// ============================================
// PRODUCT IMAGE (E-COMMERCE)
// ============================================

/**
 * Product image component
 *
 * @example
 * <ProductImage
 *   src="/images/product.jpg"
 *   alt="Product name"
 *   width={600}
 *   height={600}
 * />
 */
export function ProductImage({
  src,
  alt,
  width = 600,
  height = 600,
  className = '',
}: {
  src: string
  alt: string
  width?: number
  height?: number
  className?: string
}) {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      <ViteImage
        src={src}
        alt={alt}
        width={width}
        height={height}
        aspectRatio="square"
        objectFit="cover"
        className="transition-transform duration-300 hover:scale-110"
      />
    </div>
  )
}

// ============================================
// RESPONSIVE IMAGE (MULTIPLE SIZES)
// ============================================

/**
 * Responsive image with srcset
 *
 * @example
 * <ResponsiveImage
 *   src="/images/hero.jpg"
 *   alt="Hero"
 *   srcSet="/images/hero-640.jpg 640w, /images/hero-1024.jpg 1024w, /images/hero-1920.jpg 1920w"
 *   sizes="(max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
 * />
 */
export function ResponsiveImage({
  src,
  alt,
  srcSet,
  sizes,
  width = 1920,
  height = 1080,
  priority = false,
  className = '',
}: {
  src: string
  alt: string
  srcSet: string
  sizes?: string
  width?: number
  height?: number
  priority?: boolean
  className?: string
}) {
  return (
    <ViteImage
      src={src}
      alt={alt}
      width={width}
      height={height}
      srcSet={srcSet}
      sizes={sizes}
      priority={priority}
      className={className}
    />
  )
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Calculate dimensions based on aspect ratio
 */
function calculateDimensions(
  width?: number,
  height?: number,
  aspectRatio?: string
) {
  if (width && height) {
    return { width, height }
  }

  if (width && aspectRatio) {
    const ratio = getAspectRatio(aspectRatio)
    return { width, height: Math.round(width / ratio) }
  }

  if (height && aspectRatio) {
    const ratio = getAspectRatio(aspectRatio)
    return { width: Math.round(height * ratio), height }
  }

  // Default dimensions
  return { width: 800, height: 600 }
}

/**
 * Get aspect ratio value
 */
function getAspectRatio(aspectRatio: string): number {
  const ratios: Record<string, number> = {
    square: 1,
    '16/9': 16 / 9,
    '4/3': 4 / 3,
    '3/2': 3 / 2,
    '21/9': 21 / 9,
  }

  return ratios[aspectRatio] || 1
}

/**
 * Get aspect ratio string for CSS
 */
function getAspectRatioString(aspectRatio: string): string {
  const ratios: Record<string, string> = {
    square: '1 / 1',
    '16/9': '16 / 9',
    '4/3': '4 / 3',
    '3/2': '3 / 2',
    '21/9': '21 / 9',
  }

  return ratios[aspectRatio] || '16 / 9'
}

/**
 * Convert srcSet to AVIF format
 *
 * Note: This assumes you have AVIF versions of your images.
 * Use a build tool or CDN to generate them.
 */
function convertToAVIF(srcSet: string): string {
  return srcSet.replace(/\.(jpg|jpeg|png|webp)/g, '.avif')
}

/**
 * Convert srcSet to WebP format
 *
 * Note: This assumes you have WebP versions of your images.
 * Use a build tool or CDN to generate them.
 */
function convertToWebP(srcSet: string): string {
  return srcSet.replace(/\.(jpg|jpeg|png)/g, '.webp')
}

// ============================================
// IMAGE GENERATION SCRIPT
// ============================================

/**
 * IMAGE GENERATION SCRIPT
 *
 * Use this script to generate AVIF and WebP versions of your images.
 * Run this during your build process (e.g., in package.json scripts).
 *
 * ```bash
 * # Install sharp (image processing library)
 * npm install sharp --save-dev
 *
 * # Create script: scripts/generate-images.js
 * const sharp = require('sharp')
 * const fs = require('fs')
 * const path = require('path')
 *
 * const inputDir = 'public/images'
 * const outputDir = 'public/images/optimized'
 *
 * fs.readdirSync(inputDir).forEach((file) => {
 *   if (file.match(/\.(jpg|jpeg|png)$/)) {
 *     const input = path.join(inputDir, file)
 *     const name = file.replace(/\.(jpg|jpeg|png)$/, '')
 *
 *     // Generate AVIF
 *     sharp(input)
 *       .avif({ quality: 80 })
 *       .toFile(path.join(outputDir, `${name}.avif`))
 *
 *     // Generate WebP
 *     sharp(input)
 *       .webp({ quality: 85 })
 *       .toFile(path.join(outputDir, `${name}.webp`))
 *   }
 * })
 * ```
 *
 * Add to package.json:
 * ```json
 * {
 *   "scripts": {
 *     "build:images": "node scripts/generate-images.js",
 *     "build": "npm run build:images && vite build"
 *   }
 * }
 * ```
 */

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Generate AVIF/WebP versions of images during build (use sharp)
 * 2. Use priority loading for hero images (above the fold)
 * 3. Use lazy loading for images below the fold (default)
 * 4. Set explicit width/height to prevent CLS
 * 5. Use responsive srcset for different screen sizes
 * 6. Use CDN for image hosting (e.g., Cloudflare Images, Imgix)
 * 7. Use Intersection Observer with rootMargin="200px" (load before visible)
 * 8. Test images on slow 3G network to verify loading experience
 *
 * CORE WEB VITALS IMPACT:
 * - LCP: Priority loading + AVIF format → faster LCP
 * - CLS: Explicit dimensions + placeholder → prevents layout shift
 * - FCP: Lazy loading → faster first paint
 */
