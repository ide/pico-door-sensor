const vapidPublicKey =
  'BP1ZvYiUs2YDFtbJu2weWZdBS4DFA0kKw3pFK6iMVV7zue-fmg_gJM8lEshHkbJO5KkiO8wYh15Xn8y0BZNpRCs';

// Keep the service worker up to date
navigator.serviceWorker.register('/service-worker.js', { type: 'module' }).then((registration) => {
  registration.update();
});

// Subscribe to notifications when the user wishes to do so
const subscribeButton = document.getElementById('subscribe-button');
subscribeButton.addEventListener('click', async () => {
  const subscriptionURL = getSensorSubscriptionURL();
  if (!subscriptionURL) {
    return;  
  }

  const serviceWorkerRegistration = await navigator.serviceWorker.ready;
  const pushSubscription = await serviceWorkerRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: vapidPublicKey,
  });

  await fetch(subscriptionURL, {
    method: 'post',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(pushSubscription.toJSON()),
  });
});


function getSensorSubscriptionURL() {
  const queryParameters = new URLSearchParams(location.search);
  const subscriptionURLString = queryParameters.get('sensor_subscription_url');
  if (subscriptionURLString) {
    try {
      return new URL(subscriptionURLString);
    } catch (error) {
      console.error(`Malformed sensor subscription URL: ${subscriptionURLString}`);
    }
  }
  return null;
}
