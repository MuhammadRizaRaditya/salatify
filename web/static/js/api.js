/* SALATIFY — API Client (JWT) */
const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8000'
  : window.location.origin;

const TOKEN_KEY = 'salatify_token';
const USER_KEY = 'salatify_user';

function setToken(t){ localStorage.setItem(TOKEN_KEY, t); }
function getToken(){ return localStorage.getItem(TOKEN_KEY); }
function removeToken(){ localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(USER_KEY); }
function setUser(u){ localStorage.setItem(USER_KEY, JSON.stringify(u)); }
function getUser(){ try{ return JSON.parse(localStorage.getItem(USER_KEY)||'null'); }catch{ return null; } }

async function api(path, { method='GET', body, auth=true, headers={} }={}){
  const h = { ...headers };
  if(auth && getToken()) h.Authorization = 'Bearer ' + getToken();
  if(body && !(body instanceof FormData)) h['Content-Type']='application/json';
  const res = await fetch(API_BASE + path, { method, headers: h, body: body ? (body instanceof FormData ? body : JSON.stringify(body)) : undefined });
  if(res.status === 401){
    removeToken();
    if(window.location.pathname.includes('/login') || window.location.pathname.includes('/register')) return null;
    window.location.href = '/web/login.html';
    return null;
  }
  if(!res.ok){
    let msg = 'Terjadi kesalahan';
    try{ msg = (await res.json()).detail || msg; }catch{}
    throw new Error(msg);
  }
  if(res.status === 204) return null;
  return res.json();
}

// Auth
export const auth = {
  register: (d) => api('/auth/register', { method:'POST', body: d, auth:false }),
  login: (d) => api('/auth/login', { method:'POST', body: d, auth:false }),
  guest: () => api('/auth/guest', { method:'POST', auth:false }),
  me: () => api('/auth/me'),
  logout: () => api('/auth/logout', { method:'POST' }),
};

// Doa
export const doa = {
  list: (params) => { const qs = new URLSearchParams(params).toString(); return api('/doa' + (qs?'?'+qs:'')); },
  detail: (id) => api('/doa/' + id),
  toggleFav: (id) => api('/doa/' + id + '/favorit', { method:'POST' }),
};

// Dzikir
export const dzikir = {
  list: (params) => { const qs = new URLSearchParams(params).toString(); return api('/dzikir' + (qs?'?'+qs:'')); },
  history: () => api('/dzikir/riwayat'),
  save: (d) => api('/dzikir/riwayat', { method:'POST', body: d }),
};

// Prayer
export const prayer = {
  today: (params) => { const qs = new URLSearchParams(params).toString(); return api('/prayer/jadwal' + (qs?'?'+qs:'')); },
  byDate: (tgl) => api('/prayer/jadwal/' + tgl),
  prefs: () => api('/prayer/preferensi'),
  setPrefs: (d) => api('/prayer/preferensi', { method:'PUT', body: d }),
};

// Qibla
export const qibla = {
  hitung: (d) => api('/qibla/hitung', { method:'POST', body: d }),
};

// Quran
export const quran = {
  list: (params) => { const qs = new URLSearchParams(params).toString(); return api('/quran/surah' + (qs?'?'+qs:'')); },
  detail: (id) => api('/quran/surah/' + id),
  toggleFav: (id) => api('/quran/surah/' + id + '/favorit', { method:'POST' }),
};

// Users / Settings
export const users = {
  me: () => api('/users/me'),
  changePassword: (oldp, newp) => api('/users/password', { method:'PUT', body: { old_password: oldp, new_password: newp } }),
  settings: () => api('/users/settings'),
  updateSettings: (d) => api('/users/settings', { method:'PUT', body: d }),
};

export { API_BASE, getToken, getUser, removeToken, setUser };
