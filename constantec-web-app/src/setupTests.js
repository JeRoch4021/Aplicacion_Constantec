import '@testing-library/jest-dom';
import { expect } from 'vitest';
import * as matchers from '@testing-library/jest-dom/matchers';

// This physically attaches the methods to Vitest's 'expect'
expect.extend(matchers);