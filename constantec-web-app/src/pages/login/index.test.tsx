import { describe, expect, it, vi, beforeEach } from 'vitest'
import * as LoginModule from './index' // Point to the file with the export *

describe('<index />', () => {
  it('should export the login components', () => {
    // Check if 'Login' exists in the exported module
    expect(LoginModule.Login).toBeDefined()
  })
})
