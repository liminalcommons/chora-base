/**
 * Optimized Image Component (Next.js)
 *
 * SAP-025: React Performance Optimization
 *
 * This component wraps Next.js's next/image with best practices:
 * - AVIF/WebP format selection
 * - Responsive srcset
 * - Lazy loading (default)
 * - Priority loading for hero images
 * - Blur placeholder
 *
 * Benefits:
 * - 20-50% smaller image sizes (AVIF vs JPEG)
 * - Faster LCP (Largest Contentful Paint)
 * - Prevents CLS (Cumulative Layout Shift)
 *
 * @see https://nextjs.org/docs/app/api-reference/components/image
 */

import Image, { ImageProps as NextImageProps } from 'next/image'
import { useState } from 'react'

// ============================================
// OPTIMIZED IMAGE PROPS
// ============================================

interface OptimizedImageProps extends Omit<NextImageProps, 'src'> {
  src: string
  alt: string
  width?: number
  height?: number
  priority?: boolean
  className?: string
  aspectRatio?: 'square' | '16/9' | '4/3' | '3/2' | '21/9'
  objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down'
  onLoadingComplete?: () => void
}

// ============================================
// OPTIMIZED IMAGE COMPONENT
// ============================================

/**
 * Optimized image component with best practices
 *
 * @example
 * // Hero image (priority loading)
 * <OptimizedImage
 *   src="/hero.jpg"
 *   alt="Hero image"
 *   width={1920}
 *   height={1080}
 *   priority
 *   aspectRatio="16/9"
 * />
 *
 * // Regular image (lazy loading)
 * <OptimizedImage
 *   src="/product.jpg"
 *   alt="Product"
 *   width={800}
 *   height={600}
 *   aspectRatio="4/3"
 * />
 */
export function OptimizedImage({
  src,
  alt,
  width,
  height,
  priority = false,
  className = '',
  aspectRatio,
  objectFit = 'cover',
  onLoadingComplete,
  ...props
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true)

  // Calculate dimensions based on aspect ratio
  const dimensions = calculateDimensions(width, height, aspectRatio)

  return (
    <div className={`relative overflow-hidden ${className}`}>
      <Image
        src={src}
        alt={alt}
        width={dimensions.width}
        height={dimensions.height}
        priority={priority}
        // Responsive sizes (optimize for different screen sizes)
        sizes={
          props.sizes ||
          '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
        }
        // Blur placeholder (prevents CLS)
        placeholder="blur"
        blurDataURL={generateBlurDataURL(dimensions.width, dimensions.height)}
        // Object fit (how image fits in container)
        style={{ objectFit }}
        // Loading state
        onLoadingComplete={() => {
          setIsLoading(false)
          onLoadingComplete?.()
        }}
        // Apply loading skeleton class
        className={isLoading ? 'animate-pulse' : ''}
        {...props}
      />
    </div>
  )
}

// ============================================
// RESPONSIVE IMAGE (MULTIPLE SIZES)
// ============================================

/**
 * Responsive image with multiple sizes
 *
 * This component provides different image sizes for different screen sizes.
 * Reduces bandwidth usage on mobile devices.
 *
 * @example
 * <ResponsiveImage
 *   src="/hero.jpg"
 *   alt="Hero"
 *   sizes={{
 *     mobile: { width: 640, height: 360 },
 *     tablet: { width: 1024, height: 576 },
 *     desktop: { width: 1920, height: 1080 },
 *   }}
 * />
 */
interface ResponsiveImageProps {
  src: string
  alt: string
  sizes: {
    mobile: { width: number; height: number }
    tablet: { width: number; height: number }
    desktop: { width: number; height: number }
  }
  priority?: boolean
  className?: string
}

export function ResponsiveImage({
  src,
  alt,
  sizes,
  priority = false,
  className = '',
}: ResponsiveImageProps) {
  return (
    <OptimizedImage
      src={src}
      alt={alt}
      width={sizes.desktop.width}
      height={sizes.desktop.height}
      priority={priority}
      className={className}
      sizes="(max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
    />
  )
}

// ============================================
// HERO IMAGE (PRIORITY LOADING)
// ============================================

/**
 * Hero image component (always priority)
 *
 * This component is optimized for hero images (above the fold).
 * It always uses priority loading to improve LCP.
 *
 * @example
 * <HeroImage
 *   src="/hero.jpg"
 *   alt="Welcome to our site"
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
    <OptimizedImage
      src={src}
      alt={alt}
      width={width}
      height={height}
      priority
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
 * This component is optimized for avatars (small, circular images).
 *
 * @example
 * <AvatarImage
 *   src="/avatar.jpg"
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
      <Image
        src={src}
        alt={alt}
        width={size}
        height={size}
        sizes={`${size}px`}
        style={{ objectFit: 'cover' }}
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
 * This component is optimized for e-commerce product images.
 * It uses a 1:1 aspect ratio and includes zoom on hover.
 *
 * @example
 * <ProductImage
 *   src="/product.jpg"
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
      <OptimizedImage
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
 * Generate blur data URL (placeholder)
 *
 * This creates a tiny base64-encoded image for the blur placeholder.
 */
function generateBlurDataURL(width: number, height: number): string {
  const aspectRatio = width / height
  const svgWidth = 10
  const svgHeight = Math.round(svgWidth / aspectRatio)

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${svgWidth}" height="${svgHeight}">
      <rect width="${svgWidth}" height="${svgHeight}" fill="#e5e7eb"/>
    </svg>
  `

  const base64 = Buffer.from(svg).toString('base64')
  return `data:image/svg+xml;base64,${base64}`
}

// ============================================
// USAGE EXAMPLES
// ============================================

/**
 * Example 1: Hero image (priority loading)
 */
export function HeroExample() {
  return (
    <HeroImage
      src="/images/hero.jpg"
      alt="Welcome to our site"
      width={1920}
      height={1080}
      className="h-screen w-full"
    />
  )
}

/**
 * Example 2: Product grid (lazy loading)
 */
export function ProductGridExample() {
  const products = [
    { id: 1, name: 'Product 1', image: '/images/product-1.jpg' },
    { id: 2, name: 'Product 2', image: '/images/product-2.jpg' },
    { id: 3, name: 'Product 3', image: '/images/product-3.jpg' },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {products.map((product) => (
        <ProductImage
          key={product.id}
          src={product.image}
          alt={product.name}
          width={600}
          height={600}
        />
      ))}
    </div>
  )
}

/**
 * Example 3: User avatars (small images)
 */
export function UserListExample() {
  const users = [
    { id: 1, name: 'John Doe', avatar: '/images/avatar-1.jpg' },
    { id: 2, name: 'Jane Smith', avatar: '/images/avatar-2.jpg' },
    { id: 3, name: 'Bob Johnson', avatar: '/images/avatar-3.jpg' },
  ]

  return (
    <div className="flex gap-4">
      {users.map((user) => (
        <AvatarImage key={user.id} src={user.avatar} alt={user.name} size={64} />
      ))}
    </div>
  )
}

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Use priority loading for hero images (above the fold)
 * 2. Use lazy loading for images below the fold (default)
 * 3. Set explicit width/height to prevent CLS
 * 4. Use responsive srcset for different screen sizes
 * 5. Use AVIF format (20% smaller than WebP, 50% smaller than JPEG)
 * 6. Use blur placeholder to prevent CLS and improve perceived performance
 * 7. Use next/image's automatic optimization (don't manually optimize)
 * 8. Test images on slow 3G network to verify loading experience
 *
 * CORE WEB VITALS IMPACT:
 * - LCP: Priority loading + AVIF format → faster LCP
 * - CLS: Explicit dimensions + blur placeholder → prevents layout shift
 * - FCP: Lazy loading → faster first paint
 */
