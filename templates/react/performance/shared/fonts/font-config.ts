/**
 * Font Configuration (Next.js)
 *
 * SAP-025: React Performance Optimization
 *
 * This module provides font optimization for Next.js using next/font.
 *
 * Benefits:
 * - Self-hosted fonts (no external requests to Google Fonts)
 * - WOFF2 format (20-30% smaller than WOFF)
 * - Automatic subsetting (only include characters you use)
 * - font-display: optional (prevents layout shift)
 * - Preloading (faster FCP)
 *
 * @see https://nextjs.org/docs/app/building-your-application/optimizing/fonts
 */

import { Inter, Roboto_Mono, Playfair_Display } from 'next/font/google'
import localFont from 'next/font/local'

// ============================================
// GOOGLE FONTS
// ============================================

/**
 * Inter (Sans-serif)
 *
 * Modern, clean, highly readable.
 * Use for body text, UI elements.
 */
export const inter = Inter({
  // Subsets (only include languages you need)
  subsets: ['latin'],

  // Variable font (supports all weights with one file)
  variable: '--font-inter',

  // Font display strategy
  // - 'swap': Show fallback immediately, swap when custom font loads (prevents FOIT)
  // - 'optional': Show fallback if custom font doesn't load quickly (prevents layout shift)
  // - 'block': Block rendering until custom font loads (not recommended)
  display: 'swap',

  // Weight range (for variable fonts)
  // If not using variable font, specify weights: [400, 600, 700]
  weight: 'variable',

  // Preload (load font in <head> for faster FCP)
  preload: true,

  // Adjust font to match fallback metrics (prevents layout shift)
  adjustFontFallback: true,

  // Fallback font
  fallback: ['system-ui', 'arial'],
})

/**
 * Roboto Mono (Monospace)
 *
 * Monospace font for code blocks, technical content.
 */
export const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
  weight: 'variable',
  preload: true,
  adjustFontFallback: true,
  fallback: ['monospace'],
})

/**
 * Playfair Display (Serif)
 *
 * Elegant serif font for headings, titles.
 */
export const playfairDisplay = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
  weight: ['400', '700'], // Not a variable font, specify weights
  preload: true,
  adjustFontFallback: true,
  fallback: ['serif'],
})

// ============================================
// LOCAL FONTS (CUSTOM FONTS)
// ============================================

/**
 * Custom local font
 *
 * Use this for custom fonts not available on Google Fonts.
 * Place font files in public/fonts directory.
 *
 * @example
 * // public/fonts/custom-font.woff2
 * // public/fonts/custom-font-bold.woff2
 */
export const customFont = localFont({
  src: [
    {
      path: '../../../public/fonts/custom-font-regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../../../public/fonts/custom-font-bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: '../../../public/fonts/custom-font-italic.woff2',
      weight: '400',
      style: 'italic',
    },
  ],
  variable: '--font-custom',
  display: 'swap',
  preload: true,
  adjustFontFallback: true,
  fallback: ['system-ui', 'arial'],
})

// ============================================
// VARIABLE FONT (SINGLE FILE FOR ALL WEIGHTS)
// ============================================

/**
 * Variable font example
 *
 * Variable fonts support all weights (100-900) in a single file.
 * This reduces HTTP requests and total file size.
 *
 * @example
 * <p style={{ fontWeight: 300 }}>Light text</p>
 * <p style={{ fontWeight: 600 }}>Semibold text</p>
 * <p style={{ fontWeight: 900 }}>Black text</p>
 */
export const variableFont = localFont({
  src: '../../../public/fonts/variable-font.woff2',
  variable: '--font-variable',
  display: 'swap',
  preload: true,
  adjustFontFallback: true,
})

// ============================================
// FONT CLASS NAMES
// ============================================

/**
 * Font class names for use in components
 *
 * These are CSS variables that can be applied to any element.
 *
 * @example
 * // Apply to entire app
 * <html className={inter.variable}>
 *   <body className={inter.className}>
 *     <App />
 *   </body>
 * </html>
 *
 * @example
 * // Apply to specific elements
 * <h1 className={playfairDisplay.className}>Heading</h1>
 * <code className={robotoMono.className}>Code</code>
 */

// ============================================
// FONT STACK (FALLBACK FONTS)
// ============================================

/**
 * Font stacks with system font fallbacks
 *
 * Use these in Tailwind config or CSS for optimal fallback fonts.
 */
export const fontStacks = {
  sans: [
    'var(--font-inter)',
    'system-ui',
    '-apple-system',
    'BlinkMacSystemFont',
    'Segoe UI',
    'Roboto',
    'Oxygen',
    'Ubuntu',
    'Cantarell',
    'Helvetica Neue',
    'Arial',
    'sans-serif',
  ],
  mono: [
    'var(--font-roboto-mono)',
    'ui-monospace',
    'SFMono-Regular',
    'Menlo',
    'Monaco',
    'Consolas',
    'Liberation Mono',
    'Courier New',
    'monospace',
  ],
  serif: [
    'var(--font-playfair)',
    'ui-serif',
    'Georgia',
    'Cambria',
    'Times New Roman',
    'Times',
    'serif',
  ],
}

// ============================================
// USAGE IN APP LAYOUT
// ============================================

/**
 * USAGE IN APP LAYOUT
 *
 * Apply fonts to your app layout:
 *
 * ```typescript
 * // app/layout.tsx
 * import { inter, robotoMono, playfairDisplay } from '@/lib/fonts'
 *
 * export default function RootLayout({ children }) {
 *   return (
 *     <html
 *       lang="en"
 *       className={`${inter.variable} ${robotoMono.variable} ${playfairDisplay.variable}`}
 *     >
 *       <body className={inter.className}>{children}</body>
 *     </html>
 *   )
 * }
 * ```
 */

// ============================================
// USAGE IN TAILWIND CONFIG
// ============================================

/**
 * USAGE IN TAILWIND CONFIG
 *
 * Add font variables to your Tailwind config:
 *
 * ```javascript
 * // tailwind.config.js
 * module.exports = {
 *   theme: {
 *     extend: {
 *       fontFamily: {
 *         sans: ['var(--font-inter)', 'system-ui', 'arial'],
 *         mono: ['var(--font-roboto-mono)', 'monospace'],
 *         serif: ['var(--font-playfair)', 'serif'],
 *       },
 *     },
 *   },
 * }
 * ```
 *
 * Then use in components:
 *
 * ```tsx
 * <h1 className="font-serif">Heading</h1>
 * <code className="font-mono">Code</code>
 * ```
 */

// ============================================
// FONT SUBSETTING
// ============================================

/**
 * FONT SUBSETTING
 *
 * next/font automatically subsets fonts to include only characters you use.
 * This reduces file size significantly.
 *
 * To manually specify characters to include:
 *
 * ```typescript
 * const inter = Inter({
 *   subsets: ['latin'],
 *   // Only include these Unicode ranges
 *   unicodeRange: 'U+0000-00FF, U+0131, U+0152-0153',
 * })
 * ```
 */

// ============================================
// PRELOADING FONTS
// ============================================

/**
 * PRELOADING FONTS
 *
 * next/font automatically preloads fonts when preload: true.
 * This adds <link rel="preload"> to <head>:
 *
 * ```html
 * <link
 *   rel="preload"
 *   href="/_next/static/media/inter.woff2"
 *   as="font"
 *   type="font/woff2"
 *   crossorigin="anonymous"
 * />
 * ```
 *
 * IMPORTANT: Only preload fonts used above the fold (1-2 fonts max).
 * Preloading too many fonts can slow down FCP.
 */

// ============================================
// FONT DISPLAY STRATEGIES
// ============================================

/**
 * FONT DISPLAY STRATEGIES
 *
 * | Strategy   | FOIT (Flash of Invisible Text) | FOUT (Flash of Unstyled Text) | CLS Risk |
 * |------------|--------------------------------|-------------------------------|----------|
 * | swap       | ❌ No                          | ✅ Yes                        | Medium   |
 * | optional   | ❌ No                          | Minimal                       | Low      |
 * | block      | ✅ Yes (3s)                    | ❌ No                         | High     |
 * | fallback   | ⚠️ Yes (100ms)                 | ⚠️ Yes (if >3s)               | Medium   |
 * | auto       | Browser default                | Browser default               | Varies   |
 *
 * RECOMMENDATION:
 * - Use 'swap' for most cases (prevents FOIT, minimal CLS)
 * - Use 'optional' for critical path fonts (prevents CLS entirely)
 */

// ============================================
// PERFORMANCE TIPS
// ============================================

/**
 * PERFORMANCE TIPS:
 *
 * 1. Use variable fonts (1 file for all weights)
 * 2. Subset fonts (only include characters you use)
 * 3. Use WOFF2 format (20-30% smaller than WOFF)
 * 4. Preload only above-the-fold fonts (1-2 fonts max)
 * 5. Use font-display: swap or optional (prevents FOIT)
 * 6. Self-host fonts (no external requests, faster)
 * 7. Use adjustFontFallback: true (prevents layout shift)
 * 8. Limit font weights (each weight = separate file for non-variable fonts)
 *
 * CORE WEB VITALS IMPACT:
 * - FCP: Preloading + self-hosting → faster first paint
 * - CLS: adjustFontFallback + font-display: optional → prevents layout shift
 * - LCP: Smaller font files → faster content rendering
 */
