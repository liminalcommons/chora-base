/**
 * Vite Environment Types
 *
 * SAP-025: React Performance Optimization
 *
 * This file provides TypeScript types for Vite-specific features.
 *
 * @see https://vite.dev/guide/env-and-mode.html
 */

/// <reference types="vite/client" />

/**
 * Environment variables
 *
 * Define custom environment variables here for type safety.
 * All environment variables must be prefixed with VITE_ to be exposed to the client.
 *
 * @example
 * // .env
 * VITE_API_URL=https://api.example.com
 * VITE_ANALYTICS_ID=G-XXXXXXXXXX
 *
 * // Usage in code
 * const apiUrl = import.meta.env.VITE_API_URL
 */
interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  readonly VITE_ANALYTICS_ID?: string
  readonly VITE_SENTRY_DSN?: string
  readonly VITE_APP_VERSION?: string
  readonly VITE_APP_ENV?: 'development' | 'staging' | 'production'
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

/**
 * Image assets
 *
 * TypeScript types for importing images.
 *
 * @example
 * import logo from './logo.png'
 * <img src={logo} alt="Logo" />
 */
declare module '*.png' {
  const src: string
  export default src
}

declare module '*.jpg' {
  const src: string
  export default src
}

declare module '*.jpeg' {
  const src: string
  export default src
}

declare module '*.gif' {
  const src: string
  export default src
}

declare module '*.svg' {
  import type { FunctionComponent, SVGProps } from 'react'
  export const ReactComponent: FunctionComponent<SVGProps<SVGSVGElement>>
  const src: string
  export default src
}

declare module '*.webp' {
  const src: string
  export default src
}

declare module '*.avif' {
  const src: string
  export default src
}

/**
 * CSS Modules
 *
 * TypeScript types for CSS Modules.
 *
 * @example
 * import styles from './Button.module.css'
 * <button className={styles.primary}>Click me</button>
 */
declare module '*.module.css' {
  const classes: { readonly [key: string]: string }
  export default classes
}

declare module '*.module.scss' {
  const classes: { readonly [key: string]: string }
  export default classes
}

declare module '*.module.sass' {
  const classes: { readonly [key: string]: string }
  export default classes
}

/**
 * JSON files
 *
 * TypeScript types for importing JSON files.
 *
 * @example
 * import config from './config.json'
 */
declare module '*.json' {
  const value: any
  export default value
}

/**
 * Web Workers
 *
 * TypeScript types for Web Workers.
 *
 * @example
 * import MyWorker from './worker?worker'
 * const worker = new MyWorker()
 */
declare module '*?worker' {
  const workerConstructor: {
    new (): Worker
  }
  export default workerConstructor
}

declare module '*?worker&inline' {
  const workerConstructor: {
    new (): Worker
  }
  export default workerConstructor
}

/**
 * Raw imports
 *
 * Import files as raw strings.
 *
 * @example
 * import shaderCode from './shader.glsl?raw'
 */
declare module '*?raw' {
  const content: string
  export default content
}

/**
 * URL imports
 *
 * Import files as URLs.
 *
 * @example
 * import workletURL from './audio-worklet.js?url'
 */
declare module '*?url' {
  const url: string
  export default url
}
