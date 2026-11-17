const CACHE_NAME = 'salatify-v4';
const ASSETS = [
  '/web/index.html',
  '/web/login.html',
  '/web/register.html',
  '/web/dashboard.html',
  '/web/prayer.html',
  '/web/qibla.html',
  '/web/dzikir.html',
  '/web/doa.html',
  '/web/doa-detail.html',
  '/web/quran.html',
  '/web/settings.html',
  '/static/css/style.css',
  '/static/js/api.js',
  '/static/js/app.js',
  '/static/images/logo.png',
  '/static/images/logo-192.png',
  '/static/images/logo-512.png'
];

self.addEventListener('install', (e)=>{
  e.waitUntil(caches.open(CACHE_NAME).then((c)=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});

self.addEventListener('fetch', (e)=>{
  const url = new URL(e.request.url);
  if(url.origin === location.origin){
    e.respondWith(
      caches.match(e.request).then((r)=> r || fetch(e.request))
    );
  }
});

self.addEventListener('activate', (e)=>{
  e.waitUntil(
    caches.keys()
      .then((keys)=>Promise.all(keys.filter((k)=>k!==CACHE_NAME).map((k)=>caches.delete(k))))
      .then(()=>self.clients.claim())
  );
});
