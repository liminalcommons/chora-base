import { ThemeProvider } from "@/providers/theme-provider"
import "./globals.css"

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"           // Use class-based dark mode
          defaultTheme="system"       // Default to system preference
          enableSystem                // Enable system preference detection
          disableTransitionOnChange   // Prevent flash on theme change
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
