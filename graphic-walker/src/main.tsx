import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Suppress defaultProps warnings from @kanaries/graphic-walker library
const originalError = console.error;
console.error = (...args: any[]) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('Support for defaultProps will be removed') ||
     args[0].includes('defaultProps'))
  ) {
    return;
  }
  originalError.call(console, ...args);
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
