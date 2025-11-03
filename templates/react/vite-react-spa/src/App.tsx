export function App() {
  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-4xl w-full">
        <h1 className="text-4xl font-bold mb-4">
          Vite 7 + React 19 + TypeScript
        </h1>
        <p className="text-lg mb-8">
          Built with SAP-020 (React Project Foundation)
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">Ultra-Fast HMR</h2>
            <p>Lightning-fast hot module replacement (10-50ms)</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">TypeScript Strict</h2>
            <p>Maximum type safety out of the box</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">TanStack Query</h2>
            <p>Server state management ready</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">React Router v6</h2>
            <p>Modern client-side routing</p>
          </div>
        </div>
      </div>
    </div>
  )
}
