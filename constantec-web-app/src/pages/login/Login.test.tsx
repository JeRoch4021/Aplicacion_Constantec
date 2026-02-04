import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Login } from './Login';

// describe('<Login />', () => {
//   it('should render the login form', () => {
//     render(<Login />);
//     // const emailInput = screen.getByLabelText(/email/i);
//     // const passwordInput = screen.getByLabelText(/password/i);
//     // const submitButton = screen.getByRole('button', { name: /log in/i });
//     screen.debug(undefined, 1000000000)
//     // expect(emailInput).toBeInTheDocument();
//     // expect(passwordInput).toBeInTheDocument();
//     // expect(submitButton).toBeInTheDocument();
//   });
// }