<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Legal Assistance AI</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Get AI-driven recommendations on essential legal documents, licenses, and potential risks for your startup.
    </p>

    <form @submit.prevent="getLegalAssistance" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Startup's Legal Profile</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          placeholder="e.g., MediCare Connect"
        />
      </div>

      <div>
        <label for="industry" class="block text-sm font-medium text-gray-700 mb-1">Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="industry"
          v-model="inputData.industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          placeholder="e.g., HealthTech, E-commerce, FinTech, SaaS"
        />
      </div>

      <div>
        <label for="businessModelSummary" class="block text-sm font-medium text-gray-700 mb-1">Business Model Summary <span class="text-red-500">*</span></label>
        <textarea
          id="businessModelSummary"
          v-model="inputData.business_model_summary"
          required
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          placeholder="Describe what your business does and how it operates (e.g., 'mobile app for food delivery', 'sells organic skincare products online'). Minimum 50 characters."
        ></textarea>
      </div>

      <div>
        <label for="fundingStage" class="block text-sm font-medium text-gray-700 mb-1">Funding Stage <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="fundingStage"
          v-model="inputData.funding_stage"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          placeholder="e.g., ideation, pre-seed, seed, Series A, bootstrapped"
        />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="numFounders" class="block text-sm font-medium text-gray-700 mb-1">Number of Co-Founders <span class="text-red-500">*</span></label>
          <input
            type="number"
            id="numFounders"
            v-model.number="inputData.num_founders"
            required
            min="1"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
            placeholder="e.g., 2"
          />
        </div>
        <div>
          <label for="numEmployees" class="block text-sm font-medium text-gray-700 mb-1">Current Employees (excluding founders) <span class="text-red-500">*</span></label>
          <input
            type="number"
            id="numEmployees"
            v-model.number="inputData.num_employees"
            required
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
            placeholder="e.g., 5"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="handlesPersonalData" class="block text-sm font-medium text-gray-700 mb-1">Handles Personal Data? <span class="text-red-500">*</span></label>
          <select
            id="handlesPersonalData"
            v-model="inputData.handles_personal_data"
            required
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          >
            <option :value="true">Yes</option>
            <option :value="false">No</option>
          </select>
        </div>
        <div>
          <label for="sellsPhysicalProducts" class="block text-sm font-medium text-gray-700 mb-1">Sells Physical Products? <span class="text-red-500">*</span></label>
          <select
            id="sellsPhysicalProducts"
            v-model="inputData.sells_physical_products"
            required
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm"
          >
            <option :value="true">Yes</option>
            <option :value="false">No</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Getting Legal Advice...
        </span>
        <span v-else>Get Legal Assistance</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="legalOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Legal Recommendations for {{ legalOutput.startup_name }}</h3>

      <div class="space-y-8">
        <!-- Essential Documents -->
        <div class="p-6 bg-white border border-rose-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-bold text-rose-700 mb-4">Essential Legal Documents</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-3 pl-4">
            <li v-for="(doc, index) in legalOutput.essential_documents" :key="index">
              <span class="font-semibold">{{ doc.name }}:</span> {{ doc.description }}
              <p class="text-sm text-gray-600 mt-0.5">Rationale: {{ doc.relevance_reason }}</p>
            </li>
          </ul>
        </div>

        <!-- Industry Licenses & Certifications -->
        <div class="p-6 bg-white border border-rose-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-bold text-rose-700 mb-4">Industry-Specific Licenses & Certifications</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-3 pl-4">
            <li v-for="(cert, index) in legalOutput.industry_licenses_certs" :key="index">
              <span class="font-semibold">{{ cert.name }}:</span> {{ cert.description }}
              <p class="text-sm text-gray-600 mt-0.5">Rationale: {{ cert.relevance_reason }}</p>
            </li>
          </ul>
        </div>

        <!-- Key Legal Risks -->
        <div class="p-6 bg-white border border-rose-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-bold text-rose-700 mb-4">Key Legal Risks & Prevention</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-3 pl-4">
            <li v-for="(risk, index) in legalOutput.key_legal_risks" :key="index">
              <span class="font-semibold">{{ risk.name }}:</span> {{ risk.description }}
              <p class="text-sm text-gray-600 mt-0.5">Prevention: {{ risk.prevention_strategy }}</p>
            </li>
          </ul>
        </div>

        <!-- General Legal Advice -->
        <div class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">General Legal Advice</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
            <li v-for="(advice, index) in legalOutput.general_legal_advice" :key="index">{{ advice }}</li>
          </ul>
        </div>

        <!-- Disclaimer -->
        <div class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800 text-sm italic">
          {{ legalOutput.disclaimer }}
        </div>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Get New Legal Advice
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
const legalOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "HealthConnect AI",
  industry: "HealthTech",
  business_model_summary: "HealthConnect AI provides an AI-powered telemedicine platform that connects patients with doctors for virtual consultations and manages patient health records securely. We offer subscription plans for both patients and healthcare providers.",
  funding_stage: "Series A",
  num_founders: 3,
  num_employees: 15,
  handles_personal_data: true,
  sells_physical_products: false,
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Handles the submission of the form to get legal assistance.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const getLegalAssistance = async () => {
  loading.value = true;
  error.value = null;
  legalOutput.value = null;

  // Construct payload, ensure boolean values are correctly passed
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '')) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = [
    'startup_name', 'industry', 'business_model_summary', 'funding_stage',
    'num_founders', 'num_employees', 'handles_personal_data', 'sells_physical_products'
  ];
  const missingFields = requiredFields.filter(field => {
    // Specifically check for non-empty string for text fields, and presence for others
    if (typeof payload[field] === 'string') {
      return payload[field].trim() === '';
    }
    // For numbers/booleans, just check if they are defined
    return payload[field] === null || payload[field] === undefined;
  });

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }
  if (payload.business_model_summary.length < 50) {
      error.value = `Business Model Summary must be at least 50 characters.`;
      loading.value = false;
      return;
  }

  try {
    const data = await callApi('/api/v1/legal-assistance', 'POST', payload);
    legalOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while getting legal assistance. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  legalOutput.value = null;
  error.value = null;
};
</script>