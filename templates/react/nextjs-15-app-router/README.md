# Next.js 15 + React 19 + TypeScript Starter

Built with **SAP-020 (React Project Foundation)** from chora-base.

## Features

- ⚡ **Next.js 15** with App Router and React Server Components
- ⚛️ **React 19** with latest features (Actions, use() hook)
- 🔷 **TypeScript** strict mode for maximum type safety
- 🎯 **TanStack Query v5** for server state management
- 🐻 **Zustand** for client UI state (optional, add when needed)
- 📝 **React Hook Form** + **Zod** for forms and validation
- 🎨 **Tailwind CSS** ready (add via SAP-024)
- 🧪 **Testing** ready (add via SAP-021)

## Quick Start

```bash
# Install dependencies (pnpm recommended)
pnpm install

# Start development server with Turbopack
pnpm dev

# Open http://localhost:3000
```

## Scripts

- `pnpm dev` - Start development server with Turbopack
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm type-check` - TypeScript type checking

## Project Structure

```
src/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── loading.tsx          # Loading UI
│   ├── error.tsx            # Error boundary
│   └── not-found.tsx        # 404 page
├── components/
│   ├── ui/                  # Shared UI components
│   └── providers/
│       └── query-provider.tsx  # TanStack Query setup
├── lib/
│   ├── api.ts               # API client (Axios + Zod)
│   └── utils.ts             # Utility functions
└── features/                # Feature-based organization
    └── .gitkeep
```

## Environment Variables

Copy `.env.example` to `.env.local` and configure:

```env
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

## Creating a Feature

Follow the feature-based architecture pattern:

```bash
mkdir -p src/features/users/{components,hooks,services,types}

# Create types
echo "export interface User { id: string; name: string; }" > src/features/users/types/user.types.ts

# Create service
# Create hook
# Create component
# Export public API in src/features/users/index.ts
```

See [SAP-020 Awareness Guide](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-foundation/awareness-guide.md) for complete workflow.

## Next Steps

1. **Add Testing** - Install [SAP-021 (React Testing)](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-testing/)
2. **Add Linting** - Install [SAP-022 (React Linting)](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-linting/)
3. **Add Styling** - Install [SAP-024 (React Styling)](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-styling/)

## Documentation

- [SAP-020 Protocol Spec](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-foundation/protocol-spec.md) - Architecture patterns
- [Next.js 15 Docs](https://nextjs.org/docs)
- [React 19 Docs](https://react.dev)
- [TanStack Query Docs](https://tanstack.com/query/latest)

## License

MIT
