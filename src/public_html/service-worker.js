// Keep the service worker up to date by letting the most recent script become the active service
// worker even if another is registered. This is acceptable since there is no API contract that
// could break between the web page and this service worker in the event a newer version of the
// service worker becomes active while the user is viewing an older version of the web page.
self.addEventListener('install', (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('push', (event) => {
  const message = event.data.json();
  console.log(message);
  event.waitUntil(
    self.registration.showNotification(message.title, {
      body: message.body,
      icon: '/icon-192.avif',
      tag: message.tag,
      timestamp: message.timestamp ? message.timestamp * 1000 : undefined,
    })
  );
});

self.addEventListener('pushsubscriptionchange', (event) => {});
