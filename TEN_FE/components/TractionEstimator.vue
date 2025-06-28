<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Traction Estimator</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Benchmark your startup's growth metrics against industry averages and get AI-driven insights.
    </p>

    <form @submit.prevent="estimateTraction" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Startup's Growth Metrics</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Your Startup's Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
          placeholder="e.g., GrowthForge"
        />
      </div>

      <div>
        <label for="yourIndustry" class="block text-sm font-medium text-gray-700 mb-1">Your Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="yourIndustry"
          v-model="inputData.your_industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
          placeholder="e.g., SaaS, E-commerce, Mobile Gaming"
        />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="mau" class="block text-sm font-medium text-gray-700 mb-1">Monthly Active Users (MAU)</label>
          <input
            type="number"
            id="mau"
            v-model.number="inputData.monthly_active_users"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 50000"
          />
        </div>
        <div>
          <label for="mrr" class="block text-sm font-medium text-gray-700 mb-1">Monthly Recurring Revenue (MRR) USD</label>
          <input
            type="number"
            id="mrr"
            v-model.number="inputData.monthly_recurring_revenue_usd"
            min="0"
            step="0.01"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 150000"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="cac" class="block text-sm font-medium text-gray-700 mb-1">Customer Acquisition Cost (CAC) USD</label>
          <input
            type="number"
            id="cac"
            v-model.number="inputData.customer_acquisition_cost_usd"
            min="0"
            step="0.01"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 50"
          />
        </div>
        <div>
          <label for="ltv" class="block text-sm font-medium text-gray-700 mb-1">Customer Lifetime Value (LTV) USD</label>
          <input
            type="number"
            id="ltv"
            v-model.number="inputData.customer_lifetime_value_usd"
            min="0"
            step="0.01"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 300"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="churnRate" class="block text-sm font-medium text-gray-700 mb-1">Churn Rate (%)</label>
          <input
            type="number"
            id="churnRate"
            v-model.number="inputData.churn_rate_percent"
            min="0"
            max="100"
            step="0.1"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 5.2"
          />
        </div>
        <div>
          <label for="conversionRate" class="block text-sm font-medium text-gray-700 mb-1">Conversion Rate (%)</label>
          <input
            type="number"
            id="conversionRate"
            v-model.number="inputData.conversion_rate_percent"
            min="0"
            max="100"
            step="0.1"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="e.g., 2.5"
          />
        </div>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Estimating Traction...
        </span>
        <span v-else>Estimate Traction</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="tractionOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Traction Analysis for {{ tractionOutput.startup_name }}</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- Growth Health Score -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm flex flex-col justify-center items-center">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Overall Growth Health Score</h4>
          <div :class="healthScoreClass(tractionOutput.growth_health_score)" class="text-5xl font-extrabold mb-2">{{ tractionOutput.growth_health_score.toFixed(0) }}/100</div>
          <!-- Fix: Use healthScoreClass for color and healthScoreLevel for text -->
          <p :class="healthScoreClass(tractionOutput.growth_health_score)" class="text-xl font-medium text-center">{{ healthScoreLevel(tractionOutput.growth_health_score) }}</p>
        </div>

        <!-- Benchmarks -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Industry Benchmarks</h4>
          <div class="space-y-3">
            <div v-for="(benchmark, index) in tractionOutput.benchmarks" :key="index" class="flex justify-between items-center px-4 py-3 rounded-md bg-gray-50">
              <span class="font-medium text-gray-800">{{ benchmark.metric }}</span>
              <div class="text-right">
                <p class="text-gray-700 text-sm">Your Value: <span class="font-semibold">{{ formatMetric(benchmark.metric, benchmark.your_value) }}</span></p>
                <p class="text-gray-700 text-sm">Industry Avg: <span class="font-semibold">{{ formatMetric(benchmark.metric, benchmark.industry_average) }}</span></p>
                <p :class="benchmarkComparisonClass(benchmark.comparison)" class="text-sm font-semibold capitalize">{{ benchmark.comparison }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Insights -->
      <div class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">AI Insights & Tips</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(insight, index) in tractionOutput.ai_insights" :key="index">{{ insight }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Estimate New Traction
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useApi } from '@/composables/useApi';

const { callApi } = useApi();

// Reactive states
const loading = ref(false);
const error = ref(null);
const tractionOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "FinFlow Solutions",
  your_industry: "FinTech SaaS",
  monthly_active_users: 15000,
  monthly_recurring_revenue_usd: 75000,
  customer_acquisition_cost_usd: 120,
  customer_lifetime_value_usd: 1200,
  churn_rate_percent: 3.5,
  conversion_rate_percent: 4.1,
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Formats metric values for display (e.g., adds $, %, or handles integers).
 * @param {string} metricName - The name of the metric.
 * @param {number} value - The value to format.
 * @returns {string} Formatted string.
 */
const formatMetric = (metricName, value) => {
  if (value === null || value === undefined) return 'N/A';
  if (metricName.includes('USD')) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(value);
  }
  if (metricName.includes('Rate') || metricName.includes('Percent')) {
    return `${value.toFixed(1)}%`;
  }
  if (metricName.includes('Users')) {
    return new Intl.NumberFormat('en-US').format(value);
  }
  return value.toLocaleString(); // Default for other numbers
};

/**
 * Determines the Tailwind class for the overall health score.
 * @param {number} score - The growth health score (0-100).
 * @returns {string} Tailwind CSS class for text color.
 */
const healthScoreClass = (score) => {
  if (score >= 70) return 'text-green-600';
  if (score >= 40) return 'text-yellow-600';
  return 'text-red-600';
};

/**
 * Determines the descriptive level for the overall health score.
 * @param {number} score - The growth health score (0-100).
 * @returns {string} Descriptive level.
 */
const healthScoreLevel = (score) => {
  if (score >= 85) return 'Excellent Traction';
  if (score >= 70) return 'Strong Traction';
  if (score >= 50) return 'Moderate Traction';
  if (score >= 30) return 'Developing Traction';
  return 'Early Stage Traction';
};

/**
 * Determines the Tailwind class for benchmark comparison.
 * @param {string} comparison - The comparison string ('Above average', 'Below average', 'On par with average').
 * @returns {string} Tailwind CSS class for text color.
 */
const benchmarkComparisonClass = (comparison) => {
  switch (comparison?.toLowerCase()) {
    case 'above average': return 'text-green-600';
    case 'on par with average': return 'text-gray-600';
    case 'below average': return 'text-red-600';
    default: return 'text-gray-500';
  }
};

/**
 * Handles the submission of the form to estimate traction.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const estimateTraction = async () => {
  loading.value = true;
  error.value = null;
  tractionOutput.value = null;

  // Construct payload by filtering out null, undefined, empty strings, and NaN numbers
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '') && !(typeof value === 'number' && isNaN(value))) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'your_industry'];
  const missingFields = requiredFields.filter(field => !payload[field] || (typeof payload[field] === 'string' && payload[field].trim() === ''));

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }

  try {
    const data = await callApi('/api/v1/traction-estimator', 'POST', payload);
    tractionOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while estimating traction. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  tractionOutput.value = null;
  error.value = null;
};
</script>