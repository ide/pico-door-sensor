// Keep the service worker up to date
navigator.serviceWorker.register('/service-worker.js', { type: 'module' }).then((registration) => {
  registration.update();
});

// Subscribe to notifications when the user wishes to do so
const subscribeButton = document.getElementById('subscribe-button');
subscribeButton.addEventListener('click', async () => {
  const serviceWorkerRegistration = await navigator.serviceWorker.ready;
  const pushSubscription = await serviceWorkerRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey:
      'BP1ZvYiUs2YDFtbJu2weWZdBS4DFA0kKw3pFK6iMVV7zue-fmg_gJM8lEshHkbJO5KkiO8wYh15Xn8y0BZNpRCs',
  });
  console.log(pushSubscription.toJSON());
});
