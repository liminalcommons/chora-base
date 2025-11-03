import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

/**
 * MSW Worker for Browser (development)
 * Use this to enable API mocking in development mode
 *
 * To enable in development:
 * 1. Add to your main entry point (main.tsx or _app.tsx):
 *
 *    if (process.env.NODE_ENV === 'development') {
 *      const { worker } = await import('./mocks/browser')
 *      worker.start()
 *    }
 *
 * @see https://mswjs.io/docs/integrations/browser
 */
export const worker = setupWorker(...handlers)
