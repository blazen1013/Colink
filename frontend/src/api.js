import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const fetchEmployees = async () => {
  const response = await api.get('/employees');
  return response.data;
};

export const fetchStatusOptions = async () => {
  const response = await api.get('/status-options');
  return response.data;
};

export const updateEmployee = async (empId, payload) => {
  const response = await api.put(`/employees/${empId}`, payload);
  return response.data;
};

export const updateEmployeeStatus = async (empId, payload) => {
  const response = await api.put(`/employees/${empId}/status`, payload);
  return response.data;
};

export const fetchMemberProfile = async (loginId) => {
  const response = await api.get(`/members/${encodeURIComponent(loginId)}`);
  return response.data;
};

export const updateMemberProfile = async (loginId, payload) => {
  const response = await api.put(`/members/${encodeURIComponent(loginId)}`, payload);
  return response.data;
};

export const updateMemberStatus = async (loginId, payload) => {
  const response = await api.put(
    `/members/${encodeURIComponent(loginId)}/status`,
    payload
  );
  return response.data;
};

export default api;
