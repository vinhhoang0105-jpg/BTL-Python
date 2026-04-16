/* SciRes API Client — vanilla JS */

const API = (() => {
  const BASE = window.API_BASE || 'http://localhost:8000/api';

  function token() { return localStorage.getItem('scires_token'); }
  function setToken(t) { localStorage.setItem('scires_token', t); }
  function clearToken() { localStorage.removeItem('scires_token'); localStorage.removeItem('scires_user'); }
  function getUser() { try { return JSON.parse(localStorage.getItem('scires_user')); } catch { return null; } }
  function setUser(u) { localStorage.setItem('scires_user', JSON.stringify(u)); }

  async function request(method, path, body) {
    const headers = { 'Content-Type': 'application/json' };
    const t = token();
    if (t) headers['Authorization'] = `Bearer ${t}`;
    const res = await fetch(BASE + path, {
      method, headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    if (res.status === 204) return null;
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
    return data;
  }

  return {
    token, setToken, clearToken, getUser, setUser,
    get:    (p)    => request('GET',    p),
    post:   (p, b) => request('POST',   p, b),
    put:    (p, b) => request('PUT',    p, b),
    delete: (p)    => request('DELETE', p),

    login: async (email, password) => {
      const data = await request('POST', '/auth/login', { email, password });
      setToken(data.access_token);
      const me = await request('GET', '/auth/me');
      setUser(me);
      return me;
    },
    logout: () => { clearToken(); location.href = '/'; },
  };
})();

// Helper to format status as badge
function badge(status) {
  const s = (status || '').toLowerCase().replace(/_/g, '_');
  return `<span class="badge badge-${s}">${status}</span>`;
}

function fmtDate(d) { return d ? new Date(d).toLocaleString('vi-VN') : '—'; }
function fmtDateShort(d) { return d ? new Date(d).toLocaleDateString('vi-VN') : '—'; }

// Show error/success
function showMsg(el, msg, type = 'error') {
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => el.innerHTML = '', 4000);
}

// Open / close modal
function openModal(id) { document.getElementById(id).style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
