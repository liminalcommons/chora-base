# SAP-037: Real-Time Data Synchronization - Adoption Blueprint

**SAP ID**: SAP-037
**Version**: 1.0.0
**Status**: pilot
**Estimated Time**: 40 minutes
**Last Updated**: 2025-11-09

---

## Overview

This adoption blueprint provides **step-by-step instructions** for adding real-time data synchronization to your React application using one of four proven providers:

1. **Socket.IO** (15 min) - Bidirectional, self-hosted, full control
2. **Server-Sent Events (SSE)** (10 min) - Unidirectional, native, simple
3. **Pusher** (10 min) - Managed, developer-friendly, 100 connections free
4. **Ably** (15 min) - Enterprise-grade, global edge, 99.999% SLA

**Choose your path based on requirements**:
- Need bidirectional? NO → SSE (Option B)
- Need bidirectional? YES → Self-host? YES → Socket.IO (Option A)
- Need bidirectional? YES → Self-host? NO → Pusher (Option C) or Ably (Option D)

---

## Prerequisites

Before starting, ensure you have:

- [ ] React application (Next.js, Vite, or Create React App)
- [ ] TanStack Query installed (`@tanstack/react-query`)
- [ ] Node.js 18+ and npm/yarn
- [ ] Basic understanding of React hooks

**If TanStack Query not installed**:
```bash
npm install @tanstack/react-query
```

---

## Option A: Socket.IO (15 minutes)

**Best for**: Full control, bidirectional communication, self-hosted, cheaper at scale

### Step 1: Install Dependencies (2 min)

```bash
# Client library
npm install socket.io-client

# Server library (if you control backend)
npm install socket.io
```

---

### Step 2: Setup Socket.IO Server (5 min)

#### Option 2a: Next.js Custom Server

Create `server.js` in project root:

```javascript
const { createServer } = require('http');
const { Server } = require('socket.io');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

const PORT = process.env.PORT || 3000;

app.prepare().then(() => {
  const httpServer = createServer((req, res) => {
    handle(req, res);
  });

  const io = new Server(httpServer, {
    cors: {
      origin: process.env.NODE_ENV === 'production'
        ? 'https://yourdomain.com'
        : '*',
    },
  });

  // Connection handler
  io.on('connection', (socket) => {
    console.log('Client connected:', socket.id);

    // Example: Broadcast to all clients
    socket.on('message', (data) => {
      io.emit('message', data);
    });

    socket.on('disconnect', () => {
      console.log('Client disconnected:', socket.id);
    });
  });

  httpServer.listen(PORT, () => {
    console.log(`> Server listening on http://localhost:${PORT}`);
  });
});
```

Update `package.json`:

```json
{
  "scripts": {
    "dev": "node server.js",
    "build": "next build",
    "start": "NODE_ENV=production node server.js"
  }
}
```

---

#### Option 2b: Express Server (Separate Backend)

Create `server/index.js`:

```javascript
const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: '*' },
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  socket.on('message', (data) => {
    io.emit('message', data);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

const PORT = process.env.PORT || 3001;
httpServer.listen(PORT, () => {
  console.log(`Socket.IO server listening on http://localhost:${PORT}`);
});
```

Run server:

```bash
node server/index.js
```

---

### Step 3: Create Socket Context (3 min)

Create `lib/socket.tsx`:

```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const SocketContext = createContext<Socket | null>(null);

export function SocketProvider({ children }: { children: React.ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const socketInstance = io(process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:3000', {
      autoConnect: true,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    socketInstance.on('connect', () => {
      console.log('Socket.IO connected:', socketInstance.id);
    });

    socketInstance.on('disconnect', (reason) => {
      console.log('Socket.IO disconnected:', reason);
    });

    socketInstance.on('connect_error', (error) => {
      console.error('Socket.IO connection error:', error);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
}

export function useSocket() {
  const socket = useContext(SocketContext);
  if (!socket) {
    throw new Error('useSocket must be used within SocketProvider');
  }
  return socket;
}
```

---

### Step 4: Wrap App with Providers (2 min)

Update `app/layout.tsx` (Next.js App Router):

```typescript
import { SocketProvider } from '@/lib/socket';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './globals.css';

const queryClient = new QueryClient();

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={queryClient}>
          <SocketProvider>
            {children}
          </SocketProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
```

Or `src/main.tsx` (Vite):

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SocketProvider } from './lib/socket';
import App from './App';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <SocketProvider>
        <App />
      </SocketProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
```

---

### Step 5: Use Socket in Components (3 min)

```typescript
'use client';

import { useEffect } from 'react';
import { useQueryClient, useQuery } from '@tanstack/react-query';
import { useSocket } from '@/lib/socket';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

export default function TodoList() {
  const socket = useSocket();
  const queryClient = useQueryClient();

  // Fetch todos
  const { data: todos = [] } = useQuery<Todo[]>({
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then(res => res.json()),
  });

  // Real-time invalidation
  useEffect(() => {
    const invalidate = () => {
      queryClient.invalidateQueries(['todos']);
    };

    socket.on('todo:created', invalidate);
    socket.on('todo:updated', invalidate);
    socket.on('todo:deleted', invalidate);

    return () => {
      socket.off('todo:created', invalidate);
      socket.off('todo:updated', invalidate);
      socket.off('todo:deleted', invalidate);
    };
  }, [socket, queryClient]);

  return (
    <div>
      {todos.map(todo => (
        <div key={todo.id}>{todo.text}</div>
      ))}
    </div>
  );
}
```

---

### Step 6: Test Real-Time Sync (2 min)

1. Start server: `npm run dev`
2. Open http://localhost:3000 in **two browser windows** side-by-side
3. Trigger event in one window:
   ```typescript
   socket.emit('todo:created', { id: '1', text: 'Test' });
   ```
4. Verify event received in second window (check console logs)

---

**Total Time**: 15 minutes
**Next**: See protocol-spec.md for advanced patterns (presence tracking, offline queue, conflict resolution)

---

## Option B: Server-Sent Events (10 minutes)

**Best for**: Simple notifications, unidirectional (server → client), no library needed

### Step 1: Create SSE Hook (3 min)

Create `lib/useSSE.ts`:

```typescript
import { useEffect, useState } from 'react';

interface UseSSEOptions {
  reconnect?: boolean;
  reconnectInterval?: number;
}

export function useSSE<T>(
  url: string,
  eventName: string,
  options: UseSSEOptions = {}
) {
  const { reconnect = true, reconnectInterval = 3000 } = options;

  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let eventSource: EventSource | null = null;
    let reconnectTimeout: NodeJS.Timeout;

    const connect = () => {
      eventSource = new EventSource(url);

      eventSource.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('SSE connected:', url);
      };

      eventSource.addEventListener(eventName, (event) => {
        try {
          const parsedData: T = JSON.parse(event.data);
          setData(parsedData);
        } catch (err) {
          console.error('Failed to parse SSE data:', err);
        }
      });

      eventSource.onerror = (err) => {
        setIsConnected(false);
        setError(err as Error);
        eventSource?.close();

        if (reconnect) {
          console.log(`SSE reconnecting in ${reconnectInterval}ms...`);
          reconnectTimeout = setTimeout(connect, reconnectInterval);
        }
      };
    };

    connect();

    return () => {
      eventSource?.close();
      clearTimeout(reconnectTimeout);
    };
  }, [url, eventName, reconnect, reconnectInterval]);

  return { data, isConnected, error };
}
```

---

### Step 2: Create SSE API Route (4 min)

#### Next.js App Router

Create `app/api/events/route.ts`:

```typescript
import { NextRequest } from 'next/server';

export async function GET(req: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      // Send initial connection message
      controller.enqueue(
        encoder.encode(`event: connected\ndata: ${JSON.stringify({ timestamp: Date.now() })}\n\n`)
      );

      // Send events periodically (replace with real-time logic)
      const interval = setInterval(() => {
        const event = {
          id: Date.now().toString(),
          message: 'New event',
          timestamp: Date.now(),
        };

        controller.enqueue(
          encoder.encode(`event: message\ndata: ${JSON.stringify(event)}\n\n`)
        );
      }, 5000);

      // Cleanup on disconnect
      req.signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no', // Disable Nginx buffering
    },
  });
}
```

---

#### Express (Separate Backend)

```javascript
app.get('/api/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send initial message
  res.write(`event: connected\ndata: ${JSON.stringify({ timestamp: Date.now() })}\n\n`);

  // Send events periodically
  const interval = setInterval(() => {
    const event = {
      id: Date.now().toString(),
      message: 'New event',
      timestamp: Date.now(),
    };
    res.write(`event: message\ndata: ${JSON.stringify(event)}\n\n`);
  }, 5000);

  // Cleanup on disconnect
  req.on('close', () => {
    clearInterval(interval);
    res.end();
  });
});
```

---

### Step 3: Use SSE in Components (2 min)

```typescript
'use client';

import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useSSE } from '@/lib/useSSE';

interface Event {
  id: string;
  message: string;
  timestamp: number;
}

export default function Notifications() {
  const queryClient = useQueryClient();
  const { data: newEvent, isConnected } = useSSE<Event>('/api/events', 'message');

  // Invalidate queries on new events
  useEffect(() => {
    if (newEvent) {
      queryClient.invalidateQueries(['notifications']);
    }
  }, [newEvent, queryClient]);

  return (
    <div>
      <div>Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      {newEvent && (
        <div>
          New event: {newEvent.message} (ID: {newEvent.id})
        </div>
      )}
    </div>
  );
}
```

---

### Step 4: Test SSE (1 min)

1. Start server: `npm run dev`
2. Open http://localhost:3000
3. Check console for "SSE connected"
4. Verify events received every 5 seconds

---

**Total Time**: 10 minutes
**Limitations**: Unidirectional (server → client only), no binary data
**Next**: For bidirectional, use Socket.IO or Pusher

---

## Option C: Pusher (10 minutes)

**Best for**: Rapid prototyping, small-medium apps, 100 connections free, 6ms latency

### Step 1: Create Pusher Account (2 min)

1. Go to https://pusher.com/channels/signup
2. Sign up for free account
3. Create new app ("Channels")
4. Copy credentials:
   - `app_id`
   - `key`
   - `secret`
   - `cluster` (e.g., `us2`)

---

### Step 2: Install Pusher Client (1 min)

```bash
npm install pusher-js
```

---

### Step 3: Create Pusher Hook (3 min)

Create `lib/usePusher.ts`:

```typescript
'use client';

import { useEffect, useState } from 'react';
import Pusher from 'pusher-js';

let pusherInstance: Pusher | null = null;

export function usePusher(channelName: string, eventName: string) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    // Initialize Pusher (singleton)
    if (!pusherInstance) {
      pusherInstance = new Pusher(process.env.NEXT_PUBLIC_PUSHER_KEY!, {
        cluster: process.env.NEXT_PUBLIC_PUSHER_CLUSTER!,
      });
    }

    // Subscribe to channel
    const channel = pusherInstance.subscribe(channelName);

    // Bind to event
    channel.bind(eventName, setData);

    return () => {
      // Cleanup
      channel.unbind(eventName);
      pusherInstance?.unsubscribe(channelName);
    };
  }, [channelName, eventName]);

  return data;
}
```

---

### Step 4: Setup Environment Variables (1 min)

Create `.env.local`:

```
NEXT_PUBLIC_PUSHER_KEY=your_pusher_key
NEXT_PUBLIC_PUSHER_CLUSTER=us2
PUSHER_APP_ID=your_app_id
PUSHER_SECRET=your_secret
```

---

### Step 5: Trigger Events from Server (2 min)

Install Pusher server library:

```bash
npm install pusher
```

Create API route `app/api/todos/route.ts`:

```typescript
import Pusher from 'pusher';

const pusher = new Pusher({
  appId: process.env.PUSHER_APP_ID!,
  key: process.env.NEXT_PUBLIC_PUSHER_KEY!,
  secret: process.env.PUSHER_SECRET!,
  cluster: process.env.NEXT_PUBLIC_PUSHER_CLUSTER!,
  useTLS: true,
});

export async function POST(req: Request) {
  const body = await req.json();

  const newTodo = {
    id: Date.now().toString(),
    text: body.text,
    completed: false,
  };

  // Save to database (omitted)

  // Trigger Pusher event
  await pusher.trigger('todos', 'todo:created', newTodo);

  return Response.json(newTodo);
}
```

---

### Step 6: Use Pusher in Components (1 min)

```typescript
'use client';

import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { usePusher } from '@/lib/usePusher';

export default function TodoList() {
  const queryClient = useQueryClient();
  const newTodo = usePusher('todos', 'todo:created');

  useEffect(() => {
    if (newTodo) {
      queryClient.invalidateQueries(['todos']);
    }
  }, [newTodo, queryClient]);

  return <div>...</div>;
}
```

---

**Total Time**: 10 minutes
**Free Tier**: 100 connections, 200k messages/day
**Paid**: $49/month for 500 connections
**Next**: See protocol-spec.md for private channels and presence

---

## Option D: Ably (15 minutes)

**Best for**: Enterprise apps, global users, 99.999% SLA, 6M messages/month free

### Step 1: Create Ably Account (2 min)

1. Go to https://ably.com/signup
2. Sign up for free account
3. Create new app
4. Copy API key from "API Keys" tab

---

### Step 2: Install Ably Client (1 min)

```bash
npm install ably
```

---

### Step 3: Create Ably Hook (4 min)

Create `lib/useAbly.ts`:

```typescript
'use client';

import { useEffect, useState } from 'react';
import Ably from 'ably';

let ablyInstance: Ably.Realtime | null = null;

export function useAbly(channelName: string, eventName: string) {
  const [data, setData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Initialize Ably (singleton)
    if (!ablyInstance) {
      ablyInstance = new Ably.Realtime({
        key: process.env.NEXT_PUBLIC_ABLY_KEY!,
      });

      ablyInstance.connection.on('connected', () => {
        setIsConnected(true);
        console.log('Ably connected');
      });

      ablyInstance.connection.on('disconnected', () => {
        setIsConnected(false);
        console.log('Ably disconnected');
      });
    }

    // Get channel
    const channel = ablyInstance.channels.get(channelName);

    // Subscribe to event
    const handler = (message: Ably.Types.Message) => {
      setData(message.data);
    };

    channel.subscribe(eventName, handler);

    return () => {
      // Cleanup
      channel.unsubscribe(eventName, handler);
    };
  }, [channelName, eventName]);

  return { data, isConnected };
}
```

---

### Step 4: Setup Environment Variables (1 min)

Create `.env.local`:

```
NEXT_PUBLIC_ABLY_KEY=your_ably_api_key
ABLY_API_KEY=your_ably_api_key
```

---

### Step 5: Trigger Events from Server (4 min)

Install Ably server library:

```bash
npm install ably
```

Create API route `app/api/todos/route.ts`:

```typescript
import Ably from 'ably';

const ably = new Ably.Rest({
  key: process.env.ABLY_API_KEY!,
});

export async function POST(req: Request) {
  const body = await req.json();

  const newTodo = {
    id: Date.now().toString(),
    text: body.text,
    completed: false,
  };

  // Save to database (omitted)

  // Publish to Ably channel
  const channel = ably.channels.get('todos');
  await channel.publish('todo:created', newTodo);

  return Response.json(newTodo);
}
```

---

### Step 6: Use Ably in Components (2 min)

```typescript
'use client';

import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useAbly } from '@/lib/useAbly';

export default function TodoList() {
  const queryClient = useQueryClient();
  const { data: newTodo, isConnected } = useAbly('todos', 'todo:created');

  useEffect(() => {
    if (newTodo) {
      queryClient.invalidateQueries(['todos']);
    }
  }, [newTodo, queryClient]);

  return (
    <div>
      <div>Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      {/* Rest of component */}
    </div>
  );
}
```

---

### Step 7: Test Real-Time (1 min)

1. Start server: `npm run dev`
2. Open http://localhost:3000 in two browser windows
3. Create todo in one window
4. Verify todo appears in second window instantly

---

**Total Time**: 15 minutes
**Free Tier**: 6M messages/month, 200 connections
**Paid**: $29/month for 50M messages
**Next**: See protocol-spec.md for presence tracking and history

---

## Advanced Patterns (Optional)

### Add Reconnection Indicator (5 min)

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useSocket } from '@/lib/socket'; // or useAbly

export function ReconnectionBanner() {
  const socket = useSocket();
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
      setAttempt(0);
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    socket.on('reconnect_attempt', (attemptNumber) => {
      setAttempt(attemptNumber);
    });

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('reconnect_attempt');
    };
  }, [socket]);

  if (isConnected) return null;

  return (
    <div className="fixed top-0 left-0 right-0 bg-yellow-500 text-white p-2 text-center z-50">
      {attempt === 0 ? (
        'Connection lost. Reconnecting...'
      ) : (
        `Reconnecting... (attempt ${attempt}/5)`
      )}
    </div>
  );
}

// Usage in layout
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <SocketProvider>
          <ReconnectionBanner />
          {children}
        </SocketProvider>
      </body>
    </html>
  );
}
```

---

### Add Optimistic Updates (5 min)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useOptimisticTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newTodo: { text: string }) => {
      return fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTodo),
      }).then(res => res.json());
    },
    onMutate: async (newTodo) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries(['todos']);

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update
      queryClient.setQueryData(['todos'], (old: any[]) => [
        ...old,
        { id: 'temp-' + Date.now(), text: newTodo.text, completed: false },
      ]);

      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      // Refetch to ensure server state
      queryClient.invalidateQueries(['todos']);
    },
  });
}

// Usage
function TodoList() {
  const createTodo = useOptimisticTodo();

  return (
    <button onClick={() => createTodo.mutate({ text: 'New todo' })}>
      Add Todo (Optimistic)
    </button>
  );
}
```

---

### Add Offline Queue (10 min)

```typescript
import { useEffect, useState, useCallback } from 'react';

interface QueuedMutation {
  id: string;
  type: 'create' | 'update' | 'delete';
  payload: any;
  timestamp: number;
}

export function useOfflineQueue(socket: Socket) {
  const [queue, setQueue] = useState<QueuedMutation[]>(() => {
    // Restore from localStorage
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('offline-queue');
      return saved ? JSON.parse(saved) : [];
    }
    return [];
  });

  const [isOnline, setIsOnline] = useState(socket.connected);

  // Track connection status
  useEffect(() => {
    socket.on('connect', () => setIsOnline(true));
    socket.on('disconnect', () => setIsOnline(false));

    return () => {
      socket.off('connect');
      socket.off('disconnect');
    };
  }, [socket]);

  // Persist queue to localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('offline-queue', JSON.stringify(queue));
    }
  }, [queue]);

  const queueMutation = useCallback((mutation: Omit<QueuedMutation, 'id' | 'timestamp'>) => {
    const fullMutation: QueuedMutation = {
      id: Date.now().toString(),
      timestamp: Date.now(),
      ...mutation,
    };

    if (isOnline) {
      // Execute immediately
      socket.emit('mutation', fullMutation);
    } else {
      // Queue for later
      setQueue(q => [...q, fullMutation]);
    }
  }, [isOnline, socket]);

  // Sync queue when reconnecting
  useEffect(() => {
    if (isOnline && queue.length > 0) {
      console.log(`Syncing ${queue.length} queued mutations`);

      // Replay mutations in order
      queue.forEach(mutation => {
        socket.emit('mutation', mutation);
      });

      // Clear queue
      setQueue([]);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('offline-queue');
      }
    }
  }, [isOnline, queue, socket]);

  return {
    queueMutation,
    pendingCount: queue.length,
    isOnline,
  };
}

// Usage
function TodoList() {
  const socket = useSocket();
  const { queueMutation, pendingCount, isOnline } = useOfflineQueue(socket);

  const createTodo = (text: string) => {
    queueMutation({
      type: 'create',
      payload: { text },
    });
  };

  return (
    <div>
      {!isOnline && (
        <div className="bg-yellow-100 p-2">
          Offline ({pendingCount} pending changes)
        </div>
      )}
      <button onClick={() => createTodo('New todo')}>Add Todo</button>
    </div>
  );
}
```

---

## Testing Your Setup

### Manual Testing Checklist

- [ ] **Connection test**: Open DevTools console, verify "Connected" log
- [ ] **Event test**: Trigger event in one browser window, verify received in another
- [ ] **Reconnection test**: Kill server, restart, verify auto-reconnect
- [ ] **Offline test**: Disable network, queue mutation, re-enable, verify sync
- [ ] **Performance test**: Send 100 events, verify <50ms latency (check Network tab)

---

### Automated Tests

#### Unit Test (Jest + React Testing Library)

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useSocket } from './useSocket';
import { io } from 'socket.io-client';

jest.mock('socket.io-client');

test('useSocket connects on mount', async () => {
  const mockSocket = {
    on: jest.fn(),
    connect: jest.fn(),
    disconnect: jest.fn(),
    connected: true,
  };

  (io as jest.Mock).mockReturnValue(mockSocket);

  const { result } = renderHook(() => useSocket());

  await waitFor(() => {
    expect(result.current).toBe(mockSocket);
  });
});
```

---

#### Integration Test (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('real-time sync between two clients', async ({ browser }) => {
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();

  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  // Create todo in page1
  await page1.fill('input[placeholder="Add todo"]', 'Test todo');
  await page1.click('button:has-text("Add")');

  // Verify appears in page2 within 5 seconds
  await expect(page2.locator('text=Test todo')).toBeVisible({ timeout: 5000 });
});
```

---

## Deployment Considerations

### Environment Variables (Production)

```bash
# Socket.IO
NEXT_PUBLIC_SOCKET_URL=https://api.yourdomain.com

# SSE (no env vars needed, uses relative URL)

# Pusher
NEXT_PUBLIC_PUSHER_KEY=your_production_key
NEXT_PUBLIC_PUSHER_CLUSTER=us2
PUSHER_APP_ID=your_production_app_id
PUSHER_SECRET=your_production_secret

# Ably
NEXT_PUBLIC_ABLY_KEY=your_production_key
ABLY_API_KEY=your_production_key
```

---

### CORS Configuration (Socket.IO)

```javascript
const io = new Server(httpServer, {
  cors: {
    origin: process.env.NODE_ENV === 'production'
      ? ['https://yourdomain.com']
      : '*',
    methods: ['GET', 'POST'],
    credentials: true,
  },
});
```

---

### Load Balancer (Socket.IO)

**Problem**: WebSocket connections must stick to same server.

**Solution**: Enable sticky sessions on load balancer (Nginx, AWS ALB).

**Nginx example**:

```nginx
upstream socket_nodes {
  ip_hash;
  server localhost:3001;
  server localhost:3002;
  server localhost:3003;
}

server {
  location /socket.io/ {
    proxy_pass http://socket_nodes;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}
```

---

### Monitoring (Recommended)

Track real-time metrics:

- Connection count (active clients)
- Message throughput (events/sec)
- Latency (p50, p95, p99)
- Error rate (failed connections, dropped messages)

**Example with Socket.IO**:

```typescript
io.on('connection', (socket) => {
  metrics.increment('connections.active');

  socket.on('disconnect', () => {
    metrics.decrement('connections.active');
  });

  socket.on('message', () => {
    metrics.increment('messages.received');
  });
});
```

---

## Troubleshooting

### Issue 1: "useSocket must be used within SocketProvider"

**Cause**: Component not wrapped in `SocketProvider`.

**Fix**: Ensure `SocketProvider` wraps entire app in `layout.tsx` or `main.tsx`.

---

### Issue 2: CORS Errors

**Cause**: Server doesn't allow client origin.

**Fix**: Add origin to CORS config:

```javascript
const io = new Server(httpServer, {
  cors: { origin: 'http://localhost:3000' },
});
```

---

### Issue 3: Events Not Received

**Cause**: Event names don't match (case-sensitive).

**Fix**: Ensure exact match:

```typescript
// Server
io.emit('todo:created', data);

// Client
socket.on('todo:created', handler); // Must match exactly
```

---

### Issue 4: High Latency

**Cause**: Self-hosted server far from users.

**Fix**: Use managed service (Pusher, Ably) with global edge network.

---

### Issue 5: Connection Drops Frequently

**Cause**: Load balancer not using sticky sessions.

**Fix**: Enable `ip_hash` (Nginx) or target group stickiness (AWS ALB).

---

## Next Steps

### Immediate (5-10 min)

- [ ] Add reconnection indicator (see Advanced Patterns)
- [ ] Test with two browser windows side-by-side
- [ ] Add basic error handling

### Short-term (1-2 hours)

- [ ] Implement optimistic updates for better UX
- [ ] Add offline queue for mutations
- [ ] Setup monitoring (connection count, latency)

### Long-term (2-4 hours)

- [ ] Add presence tracking (online users, typing indicators)
- [ ] Implement conflict resolution (LWW, OT, or CRDTs)
- [ ] Write integration tests (Playwright)
- [ ] Setup production monitoring (Datadog, Sentry)

---

## Support and Documentation

### Quick Reference

- **Socket.IO docs**: https://socket.io/docs/v4/
- **Pusher docs**: https://pusher.com/docs/channels/
- **Ably docs**: https://ably.com/docs/
- **TanStack Query**: https://tanstack.com/query/latest

### SAP-037 Documentation

- **Complete API reference**: See `protocol-spec.md`
- **Architecture and rationale**: See `capability-charter.md`
- **Agent patterns**: See `AGENTS.md`
- **Claude patterns**: See `CLAUDE.md`

### Community Support

- **Socket.IO Discord**: https://discord.gg/socketio
- **Pusher Community**: https://pusher.com/community
- **Ably Discussions**: https://github.com/ably/ably-js/discussions

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Four-provider setup guides (Socket.IO, SSE, Pusher, Ably)
  - TanStack Query integration
  - Advanced patterns (reconnection, optimistic updates, offline queue)
  - Testing and deployment guides

---

**Status**: Pilot
**Total Setup Time**: 10-15 minutes (provider-dependent)
**Time Savings**: 90.5% (5-7h → 40min)
**Success Criteria**: Connection established, real-time events synced, <50ms latency
