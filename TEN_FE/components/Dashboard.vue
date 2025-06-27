<!-- components/Dashboard.vue -->
<template>
  <div class="animate-fade-in">
    <!-- Header -->
    <div class="mb-10 text-center">
      <h1 class="text-4xl font-extrabold text-gray-800 mb-3">Welcome to <span class="text-green-600">TEN</span></h1>
      <p class="text-lg text-gray-600">Explore 10 powerful tools tailored to boost your startup journey.</p>
    </div>

    <!-- Grid of Features with CTA -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="feature in features"
        :key="feature.id"
        class="bg-white shadow-lg rounded-xl p-6 border border-gray-100 hover:border-green-300 transition-all duration-300"
      >
        <div class="flex items-center space-x-3 mb-4">
          <font-awesome-icon :icon="feature.icon" class="text-green-600 w-6 h-6" />
          <h3 class="text-xl font-semibold text-gray-800">{{ feature.label }}</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">{{ feature.description }}</p>
        <button
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-all text-sm"
          @click="$emit('change-tab', feature.id)"
        >
          Go to {{ feature.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    id: 'risk',
    label: 'Risk Assessment',
    description: 'Evaluate your startup’s risk factors and receive actionable insights.',
    icon: ['fas', 'briefcase'],
  },
  {
    id: 'reputation',
    label: 'Reputation Analysis',
    description: 'Analyze your brand reputation and market perception.',
    icon: ['fas', 'comment-dots'],
  },
  {
    id: 'investors',
    label: 'Investor Match',
    description: 'Find investors that align with your startup goals.',
    icon: ['fas', 'dollar-sign'],
  },
  {
    id: 'pitch',
    label: 'Pitch Feedback',
    description: 'Upload your pitch deck and receive AI-generated feedback.',
    icon: ['fas', 'file-alt'],
  },
  {
    id: 'competitor',
    label: 'Competitor Radar',
    description: 'Identify and monitor your competitors in real-time.',
    icon: ['fas', 'satellite-dish'],
  },
  {
    id: 'traction',
    label: 'Traction Estimator',
    description: 'Forecast your product traction and growth trends.',
    icon: ['fas', 'chart-line'],
  },
  {
    id: 'legal',
    label: 'Legal Advice',
    description: 'Get personalized legal assistance tailored to startups.',
    icon: ['fas', 'gavel'],
  },
  {
    id: 'exit',
    label: 'Exit Strategy',
    description: 'Plan your business exit with smart strategic tools.',
    icon: ['fas', 'door-open'],
  },
  {
    id: 'buzz',
    label: 'Buzz Builder',
    description: 'Generate social media buzz with automated tools.',
    icon: ['fas', 'bullhorn'],
  },
  {
    id: 'talent',
    label: 'Talent Navigator',
    description: 'Find the right talent for your startup team.',
    icon: ['fas', 'users'],
  },
];
</script>

<style scoped>
.animate-fade-in {
  animation: fadeInUp 0.6s ease-out;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
