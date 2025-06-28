<template>
  <div v-if="showPrompt" class="fixed bottom-4 left-1/2 -translate-x-1/2 bg-green-700 text-white p-4 rounded-lg shadow-xl flex items-center justify-between space-x-4 z-50 animate-bounce-in">
    <p class="font-semibold">Install TEN for a better experience!</p>
    <div class="flex space-x-2">
      <button @click="installPWA" class="bg-white text-green-700 px-4 py-2 rounded-lg font-bold hover:bg-gray-100 transition">
        Install
      </button>
      <button @click="dismissPrompt" class="text-white px-4 py-2 rounded-lg border border-white hover:bg-green-600 transition">
        Not now
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const installEvent = ref(null);
const showPrompt = ref(false); // Controls the visibility of our custom prompt
const LS_DISMISSED_KEY = 'pwa_install_dismissed';

onMounted(() => {
  // Check if the prompt has been dismissed before or if app is already installed
  const dismissed = localStorage.getItem(LS_DISMISSED_KEY);
  const isInstalled = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;

  if (dismissed || isInstalled) {
    showPrompt.value = false;
    return; // Don't show if already dismissed or installed
  }

  // Listen for the beforeinstallprompt event
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // Prevent the default browser prompt immediately
    installEvent.value = e; // Store the event
    showPrompt.value = true; // Show our custom prompt
    console.log('beforeinstallprompt fired, showing custom prompt.');
  });

  // Listener for when the app is installed
  window.addEventListener('appinstalled', () => {
    installEvent.value = null; // Clear the event
    showPrompt.value = false; // Hide our prompt
    localStorage.setItem(LS_DISMISSED_KEY, 'true'); // Mark as dismissed (since it's installed)
    console.log('PWA installed successfully!');
  });
});

const installPWA = () => {
  if (installEvent.value) {
    installEvent.value.prompt(); // Show the browser install prompt
    installEvent.value.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the PWA installation');
      } else {
        console.log('User dismissed the PWA installation');
        // If they dismissed the native prompt, we should still remember their choice
        localStorage.setItem(LS_DISMISSED_KEY, 'true');
      }
      installEvent.value = null; // Clear the event
      showPrompt.value = false; // Hide our prompt after user choice
    });
  }
};

const dismissPrompt = () => {
  showPrompt.value = false; // Hide our prompt
  localStorage.setItem(LS_DISMISSED_KEY, 'true'); // Remember that the user dismissed it
  console.log('PWA install prompt dismissed by user.');
};
</script>

<style scoped>
/* Same styles as before */
@keyframes bounceIn {
  0% {
    transform: translateY(100%) translateX(-50%) scale(0.5);
    opacity: 0;
  }
  70% {
    transform: translateY(-10%) translateX(-50%) scale(1.05);
    opacity: 1;
  }
  100% {
    transform: translateY(0) translateX(-50%) scale(1);
  }
}

.animate-bounce-in {
  animation: bounceIn 0.5s ease-out forwards;
}
</style>
