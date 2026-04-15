/**
 * Auth API calls: login, profile, change password.
 */

import client from './client';

export const authApi = {
  login: (email, password) =>
    client.post('/auth/login', { email, password }).then((r) => r.data),

  getProfile: () =>
    client.get('/auth/me').then((r) => r.data),

  changePassword: (currentPassword, newPassword) =>
    client.put('/auth/me/password', {
      current_password: currentPassword,
      new_password: newPassword,
    }).then((r) => r.data),
};
