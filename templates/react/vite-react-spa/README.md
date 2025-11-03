# Vite 7 + React 19 + TypeScript SPA

Built with **SAP-020 (React Project Foundation)** from chora-base.

## Features

- ⚡ **Vite 7** - Lightning-fast dev server (< 100ms cold start)
- ⚛️ **React 19** - Latest React features
- 🔷 **TypeScript** strict mode
- 🎯 **TanStack Query v5** - Server state management
- 🐻 **Zustand** - Client UI state (optional)
- 🚦 **React Router v6** - Client-side routing
- 📝 **React Hook Form** + **Zod** - Forms and validation

## Quick Start

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Open http://localhost:5173
```

## Scripts

- `pnpm dev` - Start Vite dev server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build
- `pnpm type-check` - TypeScript type checking

## Project Structure

```
src/
├── main.tsx                 # Entry point
├── router.tsx               # React Router config
├── components/
│   ├── ui/                  # Shared UI components
│   └── layout/
│       └── root-layout.tsx  # Main layout
├── lib/
│   └── api.ts               # API client (Axios + Zod)
├── features/                # Feature-based organization
└── pages/                   # Page components
    ├── home-page.tsx
    └── not-found-page.tsx
```

## Environment Variables

Copy `.env.example` to `.env`:

```env
VITE_API_URL=http://localhost:3000/api
```

## Next Steps

1. **Add Testing** - Install SAP-021 (React Testing)
2. **Add Linting** - Install SAP-022 (React Linting)
3. **Add Styling** - Install SAP-024 (React Styling)

## Documentation

- [SAP-020 Docs](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/react-foundation/)
- [Vite Docs](https://vite.dev)
- [React Router Docs](https://reactrouter.com/)

## License

MIT
