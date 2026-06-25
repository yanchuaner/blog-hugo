const CACHE_NAME = 'blog-cache-v1';
const PRECACHE_ASSETS = [
  '/',
  '/offline.html',
  '/favicon.ico',
  '/manifest.json',
  '/fonts/inter-v12-latin-regular.woff2',
  '/fonts/noto-sans-sc-v26-chinese-simplified-regular.woff2'
];

// Install Event: Pre-cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Caching strategies
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // We only cache GET requests from our own origin
  if (request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  // Caching Strategy for Page Navigations (HTML pages)
  // Network-first: try network, fallback to cache. If both fail, show offline fallback page.
  if (request.mode === 'navigate' || request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cache the latest response for offline use
          const responseCopy = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseCopy);
          });
          return response;
        })
        .catch(() => {
          // Network failed, try serving from cache
          return caches.match(request).then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Fallback to offline page if not in cache
            return caches.match('/offline.html');
          });
        })
    );
    return;
  }

  // Caching Strategy for Hashed CSS/JS and Font files
  // Cache-first: since hashed assets and fonts are static and immutable, we can serve them from cache directly.
  const isStaticAsset = url.pathname.includes('/css/') || url.pathname.includes('/js/') || url.pathname.includes('/fonts/');
  if (isStaticAsset) {
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(request).then(response => {
          const responseCopy = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseCopy);
          });
          return response;
        });
      })
    );
    return;
  }

  // General Cache-First strategy for images and other resources
  event.respondWith(
    caches.match(request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(request).then(response => {
        // Only cache successful requests
        if (response.status === 200) {
          const responseCopy = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseCopy);
          });
        }
        return response;
      }).catch(() => {
        // Fallback for missing offline image
        if (request.destination === 'image') {
          return new Response(
            '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><rect x="3" y="3" width="18" height="18" rx="3"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="12" y2="17"/></svg>',
            { headers: { 'Content-Type': 'image/svg+xml' } }
          );
        }
      });
    })
  );
});
