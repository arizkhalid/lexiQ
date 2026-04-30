// src/api/axios.js
import axios from 'axios'
const API_URL = import.meta.env.VITE_API_URL
const api = axios.create({
  baseURL: `${API_URL}/api`,
})
const auth = axios.create({
  baseURL:  `${API_URL}/api/auth`,
  withCredentials: true,
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
});
api.interceptors.response.use((res) => res, async (error) => {
  const old = error.config;

  if (error.response?.status === 401 && !old._retry) {
    old._retry = true;
    try {
      const refreshRes = await auth.post("token/refresh/");
      const access = refreshRes.data.access;
      localStorage.setItem('access', access);
      original.headers.Authorization = `Bearer ${access}`
      return api(old);
    } catch {
      localStorage.removeItem("access");
      window.location.href = "/login?reason=expired";
    }
  }
  return Promise.reject(error);
})

export {api, auth}
