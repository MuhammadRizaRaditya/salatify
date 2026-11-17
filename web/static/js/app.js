/* SALATIFY — Shared UI helpers */
import { getToken, getUser, removeToken, setUser } from './api.js';

export function toast(msg, type='success'){
  let el = document.getElementById('salatify-toast');
  if(!el){
    el = document.createElement('div');
    el.id = 'salatify-toast';
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.innerHTML = `<div class="icon">${type==='success'?'✓':'!'}</div><div>${escapeHtml(msg)}</div>`;
  el.style.display = 'flex';
  setTimeout(()=>{ el.style.display='none'; }, 3000);
}

export function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[c])); }

export function formatTimeISO(s){
  if(!s) return '--:--';
  try{ return s.substring(11,16); }catch{ return s; }
}

export function formatDateID(d){
  const opts={weekday:'long',year:'numeric',month:'long',day:'numeric'};
  return new Date(d).toLocaleDateString('id-ID', opts);
}

export function countdownTo(hhmm){
  const now = new Date();
  const [h,m] = hhmm.split(':').map(Number);
  const target = new Date(now); target.setHours(h,m,0,0);
  if(target <= now) target.setDate(target.getDate()+1);
  const sec = Math.max(0, Math.floor((target-now)/1000));
  const hh = Math.floor(sec/3600); const mm = Math.floor((sec%3600)/60); const ss = sec%60;
  return (hh>0?hh+':':'')+String(mm).padStart(2,'0')+':'+String(ss).padStart(2,'0');
}

export function updateCountdown(el, waktu){
  if(!el || !waktu) return;
  el.textContent = countdownTo(waktu);
}

export function setupNavbar(){
  const user = getUser();
  const links = document.querySelectorAll('.nav-links a');
  const guestBadge = document.getElementById('guest-badge');
  if(user && user.is_guest && guestBadge) guestBadge.style.display='inline-flex';
  // highlight active
  const path = window.location.pathname;
  links.forEach(a=>{
    if(path.includes(a.getAttribute('href'))) a.classList.add('active');
  });
}

export function setupAuthLinks(){
  const user = getUser();
  const authed = document.querySelectorAll('.auth-required');
  const guestOnly = document.querySelectorAll('.guest-only');
  const hasToken = !!getToken();
  authed.forEach(el=> el.style.display = hasToken ? '' : 'none');
  guestOnly.forEach(el=> el.style.display = hasToken && !user.is_guest ? '' : 'none');
  const logoutBtn = document.getElementById('btn-logout');
  if(logoutBtn){
    logoutBtn.onclick = async (e)=>{
      e.preventDefault();
      await users.logout();
      removeToken();
      toast('Berhasil keluar');
      window.location.href = '/web/login.html';
    };
  }
  const nameEl = document.getElementById('user-name');
  if(nameEl && user) nameEl.textContent = user.username;
}

export function requireAuth(){
  if(!getToken()){
    window.location.href = '/web/login.html';
    return false;
  }
  return true;
}

// PWA service worker registration
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/sw.js').catch(()=>{});
}
