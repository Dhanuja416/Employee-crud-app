import axios from 'axios';

// Create axios instance with base URL
// This avoids repeating 'http://localhost:5000/api' in every call
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API calls
export const employeeApi = {
  // Get all employees
  getAll: () => api.get('/employees'),
  
  // Get single employee
  getById: (id) => api.get(`/employees/${id}`),
  
  // Create employee
  create: (data) => api.post('/employees', data),
  
  // Update employee
  update: (id, data) => api.put(`/employees/${id}`, data),
  
  // Delete employee
  delete: (id) => api.delete(`/employees/${id}`),
};

export default api;