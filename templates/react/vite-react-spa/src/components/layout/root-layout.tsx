import { Outlet } from 'react-router-dom'

export function RootLayout() {
  return (
    <div className="min-h-screen">
      <header className="border-b p-4">
        <nav className="max-w-6xl mx-auto">
          <h1 className="text-xl font-bold">My Vite App</h1>
        </nav>
      </header>
      <main className="max-w-6xl mx-auto p-4">
        <Outlet />
      </main>
    </div>
  )
}
