/**
 * Responsive Design Patterns with Tailwind CSS
 *
 * Demonstrates mobile-first responsive design patterns using Tailwind's
 * breakpoint system and container queries.
 *
 * Breakpoints:
 * - sm: 640px  (small devices)
 * - md: 768px  (tablets)
 * - lg: 1024px (laptops)
 * - xl: 1280px (desktops)
 * - 2xl: 1536px (large desktops)
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

/**
 * Responsive Grid Example
 *
 * Mobile-first grid that adapts to screen size:
 * - Mobile: 1 column
 * - Tablet (md): 2 columns
 * - Desktop (lg): 3 columns
 * - Large Desktop (xl): 4 columns
 */
export function ResponsiveGrid() {
  const items = Array.from({ length: 8 }, (_, i) => i + 1)

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {items.map((item) => (
        <Card key={item}>
          <CardHeader>
            <CardTitle>Item {item}</CardTitle>
            <CardDescription>Responsive grid item</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              This card adapts to screen size.
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

/**
 * Responsive Typography Example
 *
 * Text size adapts to screen size for optimal readability.
 */
export function ResponsiveTypography() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold sm:text-3xl md:text-4xl lg:text-5xl">
        Responsive Heading
      </h1>
      <p className="text-sm sm:text-base md:text-lg">
        This paragraph text scales with screen size for optimal readability.
      </p>
    </div>
  )
}

/**
 * Responsive Layout Example
 *
 * Sidebar layout that stacks on mobile, side-by-side on desktop.
 */
export function ResponsiveLayout() {
  return (
    <div className="flex flex-col gap-4 lg:flex-row">
      {/* Sidebar - full width on mobile, 1/4 width on desktop */}
      <aside className="w-full space-y-4 lg:w-1/4">
        <Card>
          <CardHeader>
            <CardTitle>Sidebar</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">Stacks on mobile, sidebar on desktop.</p>
          </CardContent>
        </Card>
      </aside>

      {/* Main content - full width on mobile, 3/4 width on desktop */}
      <main className="w-full space-y-4 lg:w-3/4">
        <Card>
          <CardHeader>
            <CardTitle>Main Content</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">
              This layout adapts from single column (mobile) to two columns
              (desktop).
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}

/**
 * Responsive Navigation Example
 *
 * Horizontal buttons on desktop, vertical stack on mobile.
 */
export function ResponsiveNavigation() {
  return (
    <nav className="flex flex-col gap-2 sm:flex-row sm:items-center">
      <Button>Home</Button>
      <Button variant="outline">About</Button>
      <Button variant="outline">Services</Button>
      <Button variant="outline">Contact</Button>
    </nav>
  )
}

/**
 * Container Query Example
 *
 * Uses @container queries for component-based responsive design.
 * Component adapts based on container width, not viewport width.
 *
 * Note: Requires @container support (Tailwind v3.2+)
 */
export function ContainerQueryExample() {
  return (
    <div className="@container">
      <Card className="@sm:flex-row flex flex-col gap-4">
        <div className="@sm:w-1/3 w-full bg-muted p-4">
          <p className="text-sm">Image placeholder</p>
        </div>
        <div className="@sm:w-2/3 w-full">
          <CardHeader>
            <CardTitle>Container Queries</CardTitle>
            <CardDescription>Responds to container, not viewport</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              This card uses container queries to adapt based on its parent
              container width.
            </p>
          </CardContent>
        </div>
      </Card>
    </div>
  )
}

/**
 * Responsive Spacing Example
 *
 * Padding and margins adapt to screen size.
 */
export function ResponsiveSpacing() {
  return (
    <Card className="p-4 sm:p-6 md:p-8 lg:p-10">
      <CardHeader className="space-y-2 sm:space-y-4">
        <CardTitle>Responsive Spacing</CardTitle>
        <CardDescription>
          Padding increases on larger screens for better visual balance.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 sm:space-y-6">
        <p className="text-sm">
          This card uses responsive padding: 1rem on mobile, 1.5rem on tablet,
          2rem on desktop, 2.5rem on large desktop.
        </p>
      </CardContent>
    </Card>
  )
}

/**
 * Hide/Show on Breakpoints Example
 *
 * Show/hide elements based on screen size.
 */
export function ResponsiveVisibility() {
  return (
    <div className="space-y-4">
      {/* Only visible on mobile */}
      <Card className="lg:hidden">
        <CardHeader>
          <CardTitle>Mobile Only</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">This card is hidden on large screens.</p>
        </CardContent>
      </Card>

      {/* Only visible on desktop */}
      <Card className="hidden lg:block">
        <CardHeader>
          <CardTitle>Desktop Only</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">This card is hidden on mobile.</p>
        </CardContent>
      </Card>

      {/* Always visible, but content changes */}
      <Card>
        <CardHeader>
          <CardTitle className="block sm:hidden">Mobile View</CardTitle>
          <CardTitle className="hidden sm:block">Desktop View</CardTitle>
        </CardHeader>
      </Card>
    </div>
  )
}
