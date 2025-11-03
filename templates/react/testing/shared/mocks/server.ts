import { setupServer } from 'msw/node'
import { handlers } from './handlers'

/**
 * MSW Server for Node.js (tests)
 * This will intercept HTTP requests during testing
 *
 * @see https://mswjs.io/docs/integrations/node
 */
export const server = setupServer(...handlers)
