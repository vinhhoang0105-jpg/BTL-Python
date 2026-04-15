/**
 * Catalog API calls: departments, research fields.
 */

import client from './client';

export const catalogApi = {
  getDepartments: () =>
    client.get('/catalog/departments').then((r) => r.data),

  createDepartment: (data) =>
    client.post('/catalog/departments', data).then((r) => r.data),

  updateDepartment: (id, data) =>
    client.put(`/catalog/departments/${id}`, data).then((r) => r.data),

  getResearchFields: () =>
    client.get('/catalog/research-fields').then((r) => r.data),

  createResearchField: (data) =>
    client.post('/catalog/research-fields', data).then((r) => r.data),

  updateResearchField: (id, data) =>
    client.put(`/catalog/research-fields/${id}`, data).then((r) => r.data),
};
