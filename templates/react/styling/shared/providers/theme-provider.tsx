"use client"

import * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"
import { type ThemeProviderProps } from "next-themes/dist/types"

/**
 * Theme Provider Component
 *
 * Wraps application with next-themes for dark mode support.
 * Must be a Client Component ('use client' directive).
 *
 * Features:
 * - System preference detection
 * - Manual theme toggle
 * - SSR-safe hydration
 * - localStorage persistence
 *
 * @example
 * // app/layout.tsx (Next.js 15)
 * import { ThemeProvider } from '@/providers/theme-provider'
 *
 * export default function RootLayout({ children }) {
 *   return (
 *     <html lang="en" suppressHydrationWarning>
 *       <body>
 *         <ThemeProvider
 *           attribute="class"
 *           defaultTheme="system"
 *           enableSystem
 *           disableTransitionOnChange
 *         >
 *           {children}
 *         </ThemeProvider>
 *       </body>
 *     </html>
 *   )
 * }
 *
 * @example
 * // main.tsx (Vite 7)
 * import { ThemeProvider } from './providers/theme-provider'
 *
 * ReactDOM.createRoot(document.getElementById('root')!).render(
 *   <React.StrictMode>
 *     <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
 *       <App />
 *     </ThemeProvider>
 *   </React.StrictMode>,
 * )
 */
export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
