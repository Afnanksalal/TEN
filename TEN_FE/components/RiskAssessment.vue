<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Startup Risk Assessment</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Analyze potential risks for your startup based on its profile.
    </p>

    <form @submit.prevent="analyzeRisk" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Startup Details for Risk Analysis</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="e.g., Innovate Solutions Inc."
        />
      </div>

      <div>
        <label for="industry" class="block text-sm font-medium text-gray-700 mb-1">Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="industry"
          v-model="inputData.industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="e.g., FinTech, SaaS, Biotechnology, E-commerce"
        />
      </div>

      <div>
        <label for="specificProductService" class="block text-sm font-medium text-gray-700 mb-1">Specific Product/Service Summary <span class="text-red-500">*</span></label>
        <textarea
          id="specificProductService"
          v-model="inputData.specific_product_service"
          required
          rows="3"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Briefly describe what your startup offers."
        ></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="marketSize" class="block text-sm font-medium text-gray-700 mb-1">Estimated Market Size (USD)</label>
          <input
            type="number"
            id="marketSize"
            v-model.number="inputData.market_size_usd"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 100000000 (100 Million)"
          />
        </div>
        <div>
          <label for="founderExperience" class="block text-sm font-medium text-gray-700 mb-1">Founder Relevant Experience (Years)</label>
          <input
            type="number"
            id="founderExperience"
            v-model.number="inputData.founder_experience_years"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 5"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="initialFunding" class="block text-sm font-medium text-gray-700 mb-1">Initial Funding Needed (USD)</label>
          <input
            type="number"
            id="initialFunding"
            v-model.number="inputData.initial_funding_needed_usd"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 500000"
          />
        </div>
        <div>
          <label for="hasMvp" class="block text-sm font-medium text-gray-700 mb-1">Has MVP?</label>
          <select
            id="hasMvp"
            v-model="inputData.has_mvp"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option :value="true">Yes</option>
            <option :value="false">No</option>
          </select>
        </div>
      </div>

      <div v-if="inputData.has_mvp">
        <label for="mvpStage" class="block text-sm font-medium text-gray-700 mb-1">MVP Stage Description</label>
        <textarea
          id="mvpStage"
          v-model="inputData.mvp_stage_description"
          rows="2"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Describe your MVP's current stage and functionality."
        ></textarea>
      </div>

      <div>
        <label for="ipStatus" class="block text-sm font-medium text-gray-700 mb-1">Intellectual Property Status</label>
        <input
          type="text"
          id="ipStatus"
          v-model="inputData.intellectual_property_status"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="e.g., Patent pending, Copyrighted, Trade secrets, None"
        />
      </div>

      <div>
        <label for="regulatoryEnvironment" class="block text-sm font-medium text-gray-700 mb-1">Regulatory Environment</label>
        <textarea
          id="regulatoryEnvironment"
          v-model="inputData.regulatory_environment"
          rows="2"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Describe relevant regulations or compliance requirements."
        ></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="burnRate" class="block text-sm font-medium text-gray-700 mb-1">Monthly Burn Rate (USD)</label>
          <input
            type="number"
            id="burnRate"
            v-model.number="inputData.burn_rate_usd_per_month"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 25000"
          />
        </div>
        <div>
          <label for="runway" class="block text-sm font-medium text-gray-700 mb-1">Runway (Months)</label>
          <input
            type="number"
            id="runway"
            v-model.number="inputData.runway_months"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 12"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="numCompetitors" class="block text-sm font-medium text-gray-700 mb-1">Number of Direct Competitors</label>
          <input
            type="number"
            id="numCompetitors"
            v-model.number="inputData.num_direct_competitors"
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="e.g., 3"
          />
        </div>
        <div>
          <label for="competitiveAdvantage" class="block text-sm font-medium text-gray-700 mb-1">Competitive Advantage</label>
          <textarea
            id="competitiveAdvantage"
            v-model="inputData.competitive_advantage"
            rows="2"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="What makes your startup stand out from competitors?"
          ></textarea>
        </div>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bggreen-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Analyzing Risks...
        </span>
        <span v-else>Analyze Risks</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="riskOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Risk Assessment Results for {{ riskOutput.startup_name }}</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- Overall Risk Score -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm flex flex-col justify-center items-center">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Overall Risk Score</h4>
          <div :class="overallRiskScoreClass(normalizedRiskScore)" class="text-5xl font-extrabold mb-2">{{ normalizedRiskScore.toFixed(1) }}/10</div>
          <p :class="riskLevelTextClass(overallRiskLevel)" class="text-xl font-medium">{{ overallRiskLevel }} Risk Level</p>
          <button @click="resetForm" class="mt-6 py-2 px-4 rounded-md font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
            Analyze New Startup
          </button>
        </div>

        <!-- Risk Factors Summary (Simplified from 'Categories') -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Risk Factors Summary</h4>
          <div class="space-y-3">
            <div
              v-for="(factor, index) in riskOutput.risk_factors"
              :key="index"
              :class="riskCategoryClass(factor.level)"
              class="flex justify-between items-center px-4 py-3 rounded-md"
            >
              <span class="font-medium text-gray-800">{{ factor.name }}</span>
              <span :class="riskLevelTextClass(factor.level)" class="font-bold capitalize">{{ factor.level }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Risks and Mitigation Strategies (Detailed) -->
      <div class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Detailed Risk Factors & Mitigation Strategies</h4>
        <div class="space-y-6">
          <div v-for="(risk, index) in riskOutput.risk_factors" :key="index" class="border-b pb-4 last:border-b-0 last:pb-0">
            <p class="font-semibold text-lg text-gray-800 mb-2">
              <span :class="riskLevelTextClass(risk.level)" class="mr-2 capitalize">{{ risk.level }}:</span> {{ risk.name }}
            </p>
            <p class="text-gray-700 ml-4">
              <span class="font-medium">Mitigation Strategy:</span> {{ risk.mitigation_suggestion }}
            </p>
          </div>
        </div>
      </div>

      <!-- General Recommendations -->
      <div class="mt-8 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">General Strategic Recommendations</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(tip, index) in riskOutput.recommendations" :key="index">{{ tip }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useApi } from '@/composables/useApi'; // Ensure this path is correct

const { callApi } = useApi();

// Reactive states
const loading = ref(false);
const error = ref(null);
const riskOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "Innovate Solutions Inc.",
  industry: "SaaS",
  specific_product_service: "A cloud-based CRM tool tailored for small and medium-sized businesses, focusing on ease of use and automated lead nurturing.",
  market_size_usd: 500000000, // $500 Million
  founder_experience_years: 8,
  initial_funding_needed_usd: 750000,
  has_mvp: true,
  mvp_stage_description: "MVP successfully launched with 50 beta users, core CRM functionalities (contact management, task assignment, basic reporting) are stable. Gathering feedback for next iteration.",
  intellectual_property_status: "Trademark for brand name registered, awaiting patent approval for unique lead scoring algorithm.",
  regulatory_environment: "General data privacy regulations (GDPR, CCPA) apply, requiring robust data handling and consent mechanisms.",
  burn_rate_usd_per_month: 30000,
  runway_months: 18,
  num_direct_competitors: 7,
  competitive_advantage: "Intuitive user interface designed for non-tech savvy users, coupled with an AI-powered lead nurturing module that personalizes outreach more effectively than competitors. Strong customer support reputation from beta users."
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

// Computed properties to derive values from API output
const normalizedRiskScore = computed(() => {
  if (!riskOutput.value || typeof riskOutput.value.overall_risk_score !== 'number') {
    return 0; // Default or loading state
  }
  // If score is out of 100, normalize to 10
  if (riskOutput.value.overall_risk_score > 10) {
    return riskOutput.value.overall_risk_score / 10;
  }
  return riskOutput.value.overall_risk_score;
});

const overallRiskLevel = computed(() => {
  const score = normalizedRiskScore.value;
  if (score >= 7.5) return 'High';
  if (score >= 4.0) return 'Medium';
  return 'Low';
});

/**
 * Maps a risk level string (e.g., 'low', 'medium', 'high') to a Tailwind background color class.
 * Ensures case-insensitivity.
 * @param {string} level - The risk level ('Low', 'Medium', 'High').
 * @returns {string} Tailwind CSS class for background color.
 */
const riskCategoryClass = (level) => {
  switch (level?.toLowerCase()) { // Use optional chaining for safety
    case 'low': return 'bg-green-50';
    case 'medium': return 'bg-yellow-50';
    case 'high': return 'bg-red-50';
    default: return 'bg-gray-100'; // Fallback
  }
};

/**
 * Maps a risk level string (e.g., 'low', 'medium', 'high') to a Tailwind text color class.
 * Ensures case-insensitivity.
 * @param {string} level - The risk level ('Low', 'Medium', 'High').
 * @returns {string} Tailwind CSS class for text color.
 */
const riskLevelTextClass = (level) => {
  switch (level?.toLowerCase()) { // Use optional chaining for safety
    case 'low': return 'text-green-600';
    case 'medium': return 'text-yellow-600';
    case 'high': return 'text-red-600';
    default: return 'text-gray-800'; // Fallback
  }
};

/**
 * Determines the overall risk score styling based on its normalized value.
 * @param {number} score - The normalized overall risk score (0-10).
 * @returns {string} Tailwind CSS class for text color.
 */
const overallRiskScoreClass = (score) => {
  if (score >= 7.5) return 'text-red-600';
  if (score >= 4.0) return 'text-yellow-600';
  return 'text-green-600';
};


/**
 * Handles the submission of the form to analyze risks.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const analyzeRisk = async () => {
  loading.value = true;
  error.value = null;
  riskOutput.value = null;

  // Construct payload by filtering out empty/null optional fields
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    // Only include if value is not null, undefined, or an empty string after trimming (for strings)
    // For numbers, explicitly check if they are valid numbers and not NaN
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '') && !(typeof value === 'number' && isNaN(value))) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'industry', 'specific_product_service'];
  const missingFields = requiredFields.filter(field => !payload[field]);

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }

  try {
    const data = await callApi('/api/v1/analyze-risk', 'POST', payload);
    riskOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while analyzing risks. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  riskOutput.value = null;
  error.value = null;
};
</script>