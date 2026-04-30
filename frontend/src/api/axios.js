const API_URL = import.meta.env.VITE_API_URL
async function refreshToken() {
  const res = await fetch(`${API_URL}/api/auth/token/refresh/`, {
    method: 'POST',
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Refresh failed');
  const data = await res.json();
  localStorage.setItem('access', data.access);
  return data.access;
}
async function request(url, options = {}, retry = true) {
  const token = localStorage.getItem('access');
  const res = await fetch(`${API_URL}/api${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    },
  });
  
  if (res.status === 401 && retry) {
    try {
      const newToken = await refreshToken();
      return request(url, {
        ...options,
        headers: {
          ...options.headers,
            Authorization: `Bearer ${newToken}`,
      },}, false);
    } catch {
      localStorage.removeItem('access');
      window.location.href = '/login?reason=expired';
      return;
    }
  }
  if (!res.ok) return Promise.reject(await res.json());
  return { data: await res.json() };
}

const api = {
  get: (url, options) => request(url, { method: 'GET', ...options }),
  post: (url, data, options) => request(url, { method: 'POST', body: JSON.stringify(data), ...options }),
  put: (url, data, options) => request(url, { method: 'PUT', body: JSON.stringify(data), ...options }),
  patch: (url, data, options) => request(url, { method: 'PATCH', body: JSON.stringify(data), ...options }),
  delete: (url, options) => request(url, { method: 'DELETE', ...options }),
};

const auth = {
  post: async (url, data) => {
    const res = await fetch(`${API_URL}/api/auth${url}`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) {
      const err = new Error('Auth error');
      err.response = { status: res.status, data: json };
      throw err;
    }
    return { data: json, status: res.status };
  },
};

export { api, auth };

