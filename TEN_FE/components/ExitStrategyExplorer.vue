<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Exit Strategy Explorer</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Discover potential exit strategies for your startup based on its profile and market dynamics.
    </p>

    <form @submit.prevent="exploreExitStrategy" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Startup Profile</h3>

      <!-- Input Fields based on ExitStrategyExplorerInput schema -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., QuantumLeap Innovations"
        />
      </div>

      <div>
        <label for="industry" class="block text-sm font-medium text-gray-700 mb-1">Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="industry"
          v-model="inputData.industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., Deep Tech / Quantum Computing"
        />
      </div>

      <div>
        <label for="businessModelSummary" class="block text-sm font-medium text-gray-700 mb-1">Business Model Summary <span class="text-red-500">*</span></label>
        <textarea
          id="businessModelSummary"
          v-model="inputData.business_model_summary"
          required
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Describe your startup's core offering, how it generates revenue, and its target market."
        ></textarea>
      </div>

      <div>
        <label for="fundingStage" class="block text-sm font-medium text-gray-700 mb-1">Funding Stage <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="fundingStage"
          v-model="inputData.funding_stage"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., Seed, Series A, Series B, Bootstrapped, Acquired"
        />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="currentRevenue" class="block text-sm font-medium text-gray-700 mb-1">Current Annual Revenue (USD)</label>
          <input
            type="number"
            id="currentRevenue"
            v-model.number="inputData.current_revenue_usd"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="e.g., 1500000"
          />
        </div>
        <div>
          <label for="monthlyActiveUsers" class="block text-sm font-medium text-gray-700 mb-1">Monthly Active Users / Customers</label>
          <input
            type="number"
            id="monthlyActiveUsers"
            v-model.number="inputData.monthly_active_users"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="e.g., 5000 for SaaS, 5 for enterprise"
          />
        </div>
      </div>

      <div>
        <label for="competitiveLandscape" class="block text-sm font-medium text-gray-700 mb-1">Competitive Landscape Summary</label>
        <textarea
          id="competitiveLandscape"
          v-model="inputData.competitive_landscape_summary"
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Briefly describe your main competitors and your position relative to them."
        ></textarea>
      </div>

      <div>
        <label for="ipStatus" class="block text-sm font-medium text-gray-700 mb-1">IP Status</label>
        <input
          type="text"
          id="ipStatus"
          v-model="inputData.ip_status"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., Patented core technology, patents pending, open source, trade secrets"
        />
      </div>

      <div>
        <label for="uniqueValueProposition" class="block text-sm font-medium text-gray-700 mb-1">Unique Value Proposition</label>
        <textarea
          id="uniqueValueProposition"
          v-model="inputData.unique_value_proposition"
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="What makes your startup unique and valuable? (e.g., proprietary tech, market niche, strong brand)"
        ></textarea>
      </div>

      <div>
        <label for="founderExitGoals" class="block text-sm font-medium text-gray-700 mb-1">Founder Exit Goals</label>
        <input
          type="text"
          id="founderExitGoals"
          v-model="inputData.founder_exit_goals"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., Maximize shareholder value, ensure technology continuity, quick exit, long-term play"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Exploring Strategies...
        </span>
        <span v-else>Explore Exit Strategies</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="exitOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Recommended Exit Strategies</h3>

      <div class="space-y-8">
        <div v-for="strategy in exitOutput.relevant_exit_strategies" :key="strategy.strategy_name" class="p-6 bg-white border border-indigo-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <h4 class="text-2xl font-bold text-indigo-700 mb-3">{{ strategy.strategy_name }}</h4>
          <p class="text-gray-700 mb-4 leading-relaxed">{{ strategy.description }}</p>

          <div class="mb-4">
            <h5 class="font-semibold text-gray-800 mb-2">Common Acquirer Types:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="acquirer in strategy.common_acquirer_types" :key="acquirer.type_name">
                <span class="font-medium">{{ acquirer.type_name }}:</span> {{ acquirer.description }}
              </li>
            </ul>
          </div>

          <div class="mb-4">
            <h5 class="font-semibold text-gray-800 mb-2">Key Attractiveness Metrics for this Strategy:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(metric, index) in strategy.attractiveness_metrics" :key="index">{{ metric }}</li>
            </ul>
          </div>

          <div>
            <h5 class="font-semibold text-gray-800 mb-2">Actionable Items for this Strategy:</h5>
            <ul class="list-decimal list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(item, index) in strategy.action_items" :key="index">{{ item.item }}</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="mt-8 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">General Strategic Planning Tips</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(tip, index) in exitOutput.strategic_planning_tips" :key="index">{{ tip }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Explore New Strategy
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useApi } from '@/composables/useApi'; // Ensure this path is correct

const { callApi } = useApi();

// Reactive states
const loading = ref(false);
const error = ref(null);
const exitOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "QuantumLeap Innovations",
  industry: "Deep Tech / Quantum Computing",
  business_model_summary: "QuantumLeap Innovations is developing novel quantum computing algorithms and hardware prototypes to solve complex optimization problems for logistics and financial modeling, offered as a cloud-based service with tiered subscriptions for enterprises. We focus on delivering high-performance solutions for complex real-world challenges in areas like logistics optimization, financial risk assessment, and drug discovery.",
  funding_stage: "Series A",
  current_revenue_usd: 1500000,
  monthly_active_users: 5, // For B2B enterprise, 5 active customers might be significant
  competitive_landscape_summary: "The quantum computing market is nascent but rapidly growing, with major tech giants (IBM, Google, Microsoft) and specialized startups (IonQ, Rigetti) as competitors. Our unique approach focuses on a hybrid quantum-classical architecture for specific industry verticals, offering superior performance for certain problem sets while leveraging existing infrastructure. Competition mainly involves large corporations with vast resources and a few well-funded startups. Our differentiator lies in proprietary error correction and specific industry focus.",
  ip_status: "Several core algorithms patented, additional patents pending for hardware designs. Strong IP portfolio covering both software and hardware aspects, providing significant competitive barriers.",
  unique_value_proposition: "Proprietary error-correction techniques leading to higher qubit stability and longer coherence times, enabling more complex quantum computations than competitors. Our cloud platform is also designed for seamless integration with existing enterprise classical systems, minimizing disruption and accelerating adoption. We offer a unique blend of cutting-edge research and practical, deployable solutions.",
  founder_exit_goals: "Primary goal is to maximize shareholder value through an acquisition by a large tech company or a strategic merger, preferably within 5-7 years, while ensuring the technology continues to be developed and commercialized under new ownership. Founders are also keen on seeing the technology reach its full potential and have a lasting impact.",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Handles the submission of the form to explore exit strategies.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const exploreExitStrategy = async () => {
  loading.value = true;
  error.value = null;
  exitOutput.value = null;

  // Construct payload by filtering out empty/null optional fields
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    // Only include if value is not null, undefined, or an empty string after trimming (for strings)
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '')) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'industry', 'business_model_summary', 'funding_stage'];
  const missingFields = requiredFields.filter(field => !payload[field]);

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }

  try {
    // callApi is assumed to handle base URL and any global API keys if needed
    const data = await callApi('/api/v1/exit-strategy-explorer', 'POST', payload);
    exitOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    // Display a more user-friendly error message
    error.value = err.message || "An unexpected error occurred while fetching exit strategies. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  exitOutput.value = null;
  error.value = null;
};
</script>