import '@testing-library/jest-dom'
import { expect, beforeAll, afterEach, afterAll, vi } from 'vitest'
import * as matchers from '@testing-library/jest-dom/matchers'
import { server } from './mocks/server'

// This physically attaches the methods to Vitest's 'expect'
expect.extend(matchers)

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))

// Reset handlers so tests don't interfere with each other
afterEach(() => {
  server.resetHandlers()
  vi.clearAllMocks()
  localStorage.clear()
})

// Shut down the server when tests are done
afterAll(() => server.close())
