export function HomePage() {
  return (
    <div className="py-8">
      <h1 className="text-4xl font-bold mb-4">Welcome to Vite + React</h1>
      <p className="text-lg mb-4">
        Your SPA is ready with TanStack Query, Zustand, and TypeScript strict mode.
      </p>
      <div className="space-y-2">
        <p>Next steps:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>Create features in <code className="bg-gray-100 px-2 py-1 rounded">src/features/</code></li>
          <li>Add routes in <code className="bg-gray-100 px-2 py-1 rounded">src/router.tsx</code></li>
          <li>Install SAP-021 for testing</li>
          <li>Install SAP-022 for linting</li>
        </ul>
      </div>
    </div>
  )
}
