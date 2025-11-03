export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between text-sm">
        <h1 className="text-4xl font-bold mb-4">
          Welcome to Next.js 15 + React 19
        </h1>
        <p className="text-lg mb-8">
          Built with SAP-020 (React Project Foundation)
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">TypeScript Strict</h2>
            <p>Catch 40% more errors at compile time</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">TanStack Query</h2>
            <p>Server state management built-in</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">React Server Components</h2>
            <p>40-60% smaller client bundles</p>
          </div>

          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-2">Feature-Based Structure</h2>
            <p>Scalable architecture ready</p>
          </div>
        </div>

        <div className="mt-12">
          <h3 className="text-xl font-semibold mb-4">Next Steps:</h3>
          <ol className="list-decimal list-inside space-y-2">
            <li>Create your first feature in <code className="bg-gray-100 px-2 py-1 rounded">src/features/</code></li>
            <li>Add API routes in <code className="bg-gray-100 px-2 py-1 rounded">src/app/api/</code></li>
            <li>Install SAP-021 for testing setup</li>
            <li>Install SAP-022 for linting and formatting</li>
          </ol>
        </div>
      </div>
    </main>
  )
}
