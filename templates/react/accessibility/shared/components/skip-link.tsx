/**
 * Skip Link Component
 *
 * WCAG 2.2 Level AA compliant skip link for keyboard navigation.
 *
 * Skip links allow keyboard users to bypass repetitive navigation and jump
 * directly to main content. Required by WCAG 2.4.1 Bypass Blocks.
 *
 * This component is:
 * - Visually hidden until focused (keyboard-only users see it)
 * - First focusable element on the page (Tab from URL bar)
 * - Links to main content ID (#main-content)
 * - Has clear focus indicator
 *
 * Based on WCAG 2.2 criteria:
 * - 2.4.1 Bypass Blocks (Level A)
 * - 2.4.7 Focus Visible (Level AA)
 *
 * Usage:
 * ```tsx
 * // app/layout.tsx or src/App.tsx
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         <SkipLink />
 *         <header>
 *           <nav>...</nav>
 *         </header>
 *         <main id="main-content">
 *           {children}
 *         </main>
 *       </body>
 *     </html>
 *   )
 * }
 * ```
 */

interface SkipLinkProps {
  /** Target element ID (default: 'main-content') */
  targetId?: string
  /** Link text (default: 'Skip to main content') */
  text?: string
  /** Optional className for styling customization */
  className?: string
}

export function SkipLink({
  targetId = 'main-content',
  text = 'Skip to main content',
  className = '',
}: SkipLinkProps) {
  return (
    <a
      href={`#${targetId}`}
      className={`sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-blue-600 focus:px-4 focus:py-2 focus:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${className}`}
    >
      {text}
    </a>
  )
}

/**
 * Example: Multiple Skip Links
 *
 * For complex layouts, provide multiple skip links:
 *
 * ```tsx
 * export default function Layout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         <SkipLink targetId="main-content" text="Skip to main content" />
 *         <SkipLink targetId="navigation" text="Skip to navigation" />
 *         <SkipLink targetId="footer" text="Skip to footer" />
 *
 *         <header>
 *           <nav id="navigation">...</nav>
 *         </header>
 *
 *         <main id="main-content">
 *           {children}
 *         </main>
 *
 *         <footer id="footer">...</footer>
 *       </body>
 *     </html>
 *   )
 * }
 * ```
 */

/**
 * Tailwind CSS Configuration
 *
 * The skip link uses the `sr-only` utility class (screen reader only).
 * Ensure this is defined in your Tailwind config:
 *
 * ```css
 * .sr-only {
 *   position: absolute;
 *   width: 1px;
 *   height: 1px;
 *   padding: 0;
 *   margin: -1px;
 *   overflow: hidden;
 *   clip: rect(0, 0, 0, 0);
 *   white-space: nowrap;
 *   border-width: 0;
 * }
 *
 * .not-sr-only {
 *   position: static;
 *   width: auto;
 *   height: auto;
 *   padding: 0;
 *   margin: 0;
 *   overflow: visible;
 *   clip: auto;
 *   white-space: normal;
 * }
 * ```
 *
 * This is included by default in Tailwind CSS.
 */

/**
 * Alternative: Native HTML Approach
 *
 * If not using React components, use plain HTML:
 *
 * ```html
 * <a href="#main-content" class="skip-link">
 *   Skip to main content
 * </a>
 *
 * <style>
 *   .skip-link {
 *     position: absolute;
 *     left: -9999px;
 *     top: auto;
 *     width: 1px;
 *     height: 1px;
 *     overflow: hidden;
 *   }
 *
 *   .skip-link:focus {
 *     position: fixed;
 *     top: 1rem;
 *     left: 1rem;
 *     width: auto;
 *     height: auto;
 *     padding: 0.5rem 1rem;
 *     background: #0066cc;
 *     color: #fff;
 *     z-index: 9999;
 *     border-radius: 0.25rem;
 *     outline: 2px solid #0066cc;
 *     outline-offset: 2px;
 *   }
 * </style>
 * ```
 */

/**
 * Testing Checklist
 *
 * Manual testing (automated tools won't catch skip link issues):
 *
 * 1. **Keyboard Navigation**:
 *    - Load page in browser
 *    - Press Tab key (first tab from URL bar)
 *    - Skip link should appear visually
 *    - Press Enter to activate
 *    - Focus should jump to main content
 *
 * 2. **Screen Reader**:
 *    - Enable NVDA/VoiceOver
 *    - Navigate to page
 *    - First element should be "Skip to main content, link"
 *    - Activate link
 *    - Should announce "main content" region
 *
 * 3. **Visual Appearance**:
 *    - Skip link should be invisible by default
 *    - When focused, should have clear visual indicator
 *    - Should meet 3:1 contrast ratio (WCAG 2.4.11 Focus Not Obscured)
 *    - Should not be obscured by other elements
 *
 * 4. **Target Element**:
 *    - Ensure target element has matching ID
 *    - Ensure target element can receive focus (add tabindex="-1" if needed)
 *    - Ensure target element is a landmark (<main>, <nav>, etc.)
 */

/**
 * Common Pitfall: Target Element Focus
 *
 * If the target element doesn't receive focus, add tabindex="-1":
 *
 * ```tsx
 * <main id="main-content" tabIndex={-1}>
 *   {children}
 * </main>
 * ```
 *
 * This allows the <main> element to receive programmatic focus
 * when the skip link is activated.
 */

/**
 * Example: Next.js App Router Layout
 *
 * ```tsx
 * // app/layout.tsx
 * import { SkipLink } from '@/components/skip-link'
 *
 * export default function RootLayout({
 *   children,
 * }: {
 *   children: React.ReactNode
 * }) {
 *   return (
 *     <html lang="en">
 *       <body>
 *         <SkipLink />
 *
 *         <header className="border-b">
 *           <nav>
 *             <a href="/">Home</a>
 *             <a href="/about">About</a>
 *             <a href="/contact">Contact</a>
 *           </nav>
 *         </header>
 *
 *         <main id="main-content" tabIndex={-1} className="container mx-auto py-8">
 *           {children}
 *         </main>
 *
 *         <footer className="border-t">
 *           <p>&copy; 2025 Company Name</p>
 *         </footer>
 *       </body>
 *     </html>
 *   )
 * }
 * ```
 */

/**
 * Example: Vite App
 *
 * ```tsx
 * // src/App.tsx
 * import { SkipLink } from './components/skip-link'
 *
 * function App() {
 *   return (
 *     <>
 *       <SkipLink />
 *
 *       <header>
 *         <nav>
 *           <a href="/">Home</a>
 *           <a href="/about">About</a>
 *         </nav>
 *       </header>
 *
 *       <main id="main-content" tabIndex={-1}>
 *         <h1>Welcome</h1>
 *         <p>This is the main content area.</p>
 *       </main>
 *
 *       <footer>
 *         <p>&copy; 2025 Company</p>
 *       </footer>
 *     </>
 *   )
 * }
 * ```
 */

/**
 * Testing Example (React Testing Library)
 *
 * Note: Skip link testing is primarily manual, but you can test basic rendering:
 *
 * ```typescript
 * import { render, screen } from '@testing-library/react'
 * import { SkipLink } from './skip-link'
 *
 * describe('SkipLink', () => {
 *   it('should render with correct href', () => {
 *     render(<SkipLink targetId="main-content" />)
 *
 *     const link = screen.getByText('Skip to main content')
 *     expect(link).toHaveAttribute('href', '#main-content')
 *   })
 *
 *   it('should use custom text and target', () => {
 *     render(
 *       <SkipLink
 *         targetId="navigation"
 *         text="Skip to navigation"
 *       />
 *     )
 *
 *     const link = screen.getByText('Skip to navigation')
 *     expect(link).toHaveAttribute('href', '#navigation')
 *   })
 * })
 * ```
 *
 * For full testing, use manual keyboard navigation (see Testing Checklist above).
 */
