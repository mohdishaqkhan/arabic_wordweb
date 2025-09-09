// // When user submits a prompt
// fetch('/api/data', {
//   method: 'POST',
//   headers: { 'Content-Type': 'application/json' },
//   body: JSON.stringify({ prompt: userPrompt }) // userPrompt is what the user typed
// })
// .then(response => response.json())
// .then(data => {
//   // Handling api response here
// });
const CACHE_NAME = 'arabic-wordweb-cache-v1';
// List of all the files that make up your app shell, relative to the service worker's scope
const urlsToCache = [
  './arabic_wordweb_pwa.html',
  './manifest.json',
  // You would ideally place your icons in the 'icons' folder and list them here
  // './icons/icon-192x192.png',
  // './icons/icon-512x512.png',
  // './icons/icon-maskable-192x192.png',
  // './icons/icon-maskable-512x512.png',

  // External CDNs - it's generally good practice to cache these too
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
  'https://unpkg.com/react@18/umd/react.production.min.js',
  'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js',
  'https://unpkg.com/@babel/standalone/babel.min.js',
  'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js',
  'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js',
  'https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js'
];

// Install event: Caches the app shell
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('[Service Worker] Failed to cache during install:', error);
      })
  );
  self.skipWaiting(); // Forces the waiting service worker to become the active service worker
});

// Activate event: Cleans up old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  event.waitUntil(self.clients.claim()); // Take control of the page immediately
});

// Fetch event: Serves content from cache first, then falls back to network
self.addEventListener('fetch', event => {
  // Only handle GET requests and skip API calls for now (as they need fresh data)
  if (event.request.method === 'GET' && !event.request.url.includes('generativelanguage.googleapis.com')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          // Cache hit - return cached response
          if (response) {
            return response;
          }
          // No cache hit - fetch from network
          return fetch(event.request);
        })
        .catch(error => {
          console.error('[Service Worker] Fetch failed:', error);
          // You could return an offline page here if desired
        })
    );
  }
});



