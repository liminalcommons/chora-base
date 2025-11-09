import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider } from './providers/theme-provider'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
