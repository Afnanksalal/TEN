<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Competitor Radar</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Track key competitors and identify emerging market trends.
    </p>

    <form @submit.prevent="getCompetitorRadar" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Startup's Profile</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Your Startup's Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm"
          placeholder="e.g., DataGuard Solutions"
        />
      </div>

      <div>
        <label for="yourIndustry" class="block text-sm font-medium text-gray-700 mb-1">Your Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="yourIndustry"
          v-model="inputData.your_industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm"
          placeholder="e.g., Cybersecurity, Cloud Computing, FinTech"
        />
      </div>

      <div>
        <label for="productServiceDescription" class="block text-sm font-medium text-gray-700 mb-1">Your Product/Service Description <span class="text-red-500">*</span></label>
        <textarea
          id="productServiceDescription"
          v-model="inputData.your_product_service_description"
          required
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-sky-500 focus:border-sky-500 sm:text-sm"
          placeholder="Describe your startup's core product or service in detail. Minimum 20 characters."
        ></textarea>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Scanning Competitors...
        </span>
        <span v-else>Launch Competitor Radar</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="competitorOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Competitor Intelligence for {{ competitorOutput.startup_name }}</h3>

      <div v-if="competitorOutput.tracked_competitors && competitorOutput.tracked_competitors.length > 0" class="space-y-6 mb-8">
        <div v-for="competitor in competitorOutput.tracked_competitors" :key="competitor.name" class="p-6 bg-white border border-sky-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h4 class="text-2xl font-bold text-sky-700 mb-1">{{ competitor.name }}</h4>
              <a v-if="competitor.website" :href="competitor.website" target="_blank" rel="noopener noreferrer" class="inline-flex items-center text-sky-600 hover:text-sky-800 text-sm font-medium">
                {{ competitor.website }}
                <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            </div>
            <div :class="hiringSurgeClass(competitor.hiring_surge_indication)" class="text-sm font-semibold px-3 py-1 rounded-full capitalize">
              Hiring: {{ competitor.hiring_surge_indication }}
            </div>
          </div>

          <p v-if="competitor.product_description" class="text-gray-700 mb-3"><span class="font-semibold">Product:</span> {{ competitor.product_description }}</p>
          <p v-if="competitor.value_proposition" class="text-gray-700 mb-3"><span class="font-semibold">Value Prop:</span> {{ competitor.value_proposition }}</p>
          <p v-if="competitor.target_market" class="text-gray-700 mb-3"><span class="font-semibold">Target Market:</span> {{ competitor.target_market }}</p>
          <p v-if="competitor.overall_summary" class="text-gray-700 mb-4"><span class="font-semibold">Summary:</span> {{ competitor.overall_summary }}</p>

          <div v-if="competitor.funding_rounds && competitor.funding_rounds.length > 0" class="mb-4">
            <h5 class="font-semibold text-gray-800 mb-2">Recent Funding:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(round, idx) in competitor.funding_rounds" :key="idx">{{ round }}</li>
            </ul>
          </div>

          <div v-if="competitor.press_mentions_summary && competitor.press_mentions_summary.length > 0">
            <h5 class="font-semibold text-gray-800 mb-2">Recent Press & News:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(mention, idx) in competitor.press_mentions_summary" :key="idx">{{ mention }}</li>
            </ul>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-600 italic mb-8">
        No specific competitors tracked or identified based on the provided information.
      </p>

      <!-- General Market Trends -->
      <div v-if="competitorOutput.general_market_trends && competitorOutput.general_market_trends.length > 0" class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">General Market Trends</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(trend, index) in competitorOutput.general_market_trends" :key="index">{{ trend }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Scan New Competitors
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
const competitorOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "SwiftData Analytics",
  your_industry: "Data Analytics Software",
  your_product_service_description: "SwiftData Analytics provides a real-time data processing and visualization platform for e-commerce businesses. Our solution helps identify customer behavior patterns and optimize sales funnels through intuitive dashboards and predictive analytics, aiming to reduce cart abandonment rates and increase conversion.",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Determines the Tailwind class for hiring surge indication.
 * @param {string} level - The hiring surge level ('High', 'Medium', 'Low', 'No indication').
 * @returns {string} Tailwind CSS class for background and text color.
 */
const hiringSurgeClass = (level) => {
  switch (level?.toLowerCase()) {
    case 'high': return 'bg-red-100 text-red-800';
    case 'medium': return 'bg-yellow-100 text-yellow-800';
    case 'low': return 'bg-green-100 text-green-800';
    case 'no indication': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

/**
 * Handles the submission of the form to get competitor radar analysis.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const getCompetitorRadar = async () => {
  loading.value = true;
  error.value = null;
  competitorOutput.value = null;

  // Construct payload
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '')) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'your_industry', 'your_product_service_description'];
  const missingFields = requiredFields.filter(field => !payload[field] || (typeof payload[field] === 'string' && payload[field].trim() === ''));

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields.`;
    loading.value = false;
    return;
  }
  if (payload.your_product_service_description.length < 20) {
      error.value = `Product/Service Description must be at least 20 characters.`;
      loading.value = false;
      return;
  }

  try {
    const data = await callApi('/api/v1/competitor-radar', 'POST', payload);
    competitorOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while fetching competitor data. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  competitorOutput.value = null;
  error.value = null;
};
</script>