<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Talent Navigator</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Identify critical roles for your startup's growth and get AI-driven talent acquisition insights.
    </p>

    <form @submit.prevent="getTalentNavigation" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Startup's Team Needs</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Your Startup's Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-fuchsia-500 focus:border-fuchsia-500 sm:text-sm"
          placeholder="e.g., CodeCrafters"
        />
      </div>

      <div>
        <label for="yourIndustry" class="block text-sm font-medium text-gray-700 mb-1">Your Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="yourIndustry"
          v-model="inputData.your_industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-fuchsia-500 focus:border-fuchsia-500 sm:text-sm"
          placeholder="e.g., Software Development, Mobile App, AI/ML"
        />
      </div>

      <div>
        <label for="fundingStage" class="block text-sm font-medium text-gray-700 mb-1">Funding Stage <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="fundingStage"
          v-model="inputData.funding_stage"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-fuchsia-500 focus:border-fuchsia-500 sm:text-sm"
          placeholder="e.g., pre-seed, seed, Series A"
        />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="currentTeamSize" class="block text-sm font-medium text-gray-700 mb-1">Current Team Size <span class="text-red-500">*</span></label>
          <input
            type="number"
            id="currentTeamSize"
            v-model.number="inputData.current_team_size"
            required
            min="0"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-fuchsia-500 focus:border-fuchsia-500 sm:text-sm"
            placeholder="e.g., 3"
          />
        </div>
        <div>
          <label for="keyChallenge" class="block text-sm font-medium text-gray-700 mb-1">Key Challenge Talent Could Address <span class="text-red-500">*</span></label>
          <textarea
            id="keyChallenge"
            v-model="inputData.key_challenge"
            required
            rows="3"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-fuchsia-500 focus:border-fuchsia-500 sm:text-sm"
            placeholder="Describe the primary challenge or bottleneck your startup is facing that a new hire could resolve. Minimum 20 characters."
          ></textarea>
        </div>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-fuchsia-600 hover:bg-fuchsia-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-fuchsia-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Navigating Talent...
        </span>
        <span v-else>Navigate Talent Needs</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="talentOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Talent Insights for {{ talentOutput.startup_name }}</h3>

      <div v-if="talentOutput.recommended_roles && talentOutput.recommended_roles.length > 0" class="space-y-8 mb-8">
        <div v-for="(role, index) in talentOutput.recommended_roles" :key="index" class="p-6 bg-white border border-fuchsia-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <h4 class="text-2xl font-bold text-fuchsia-700 mb-3">{{ role.role_name }}</h4>
          <p class="text-gray-700 mb-4 leading-relaxed"><span class="font-semibold">Ideal Candidate:</span> {{ role.ideal_candidate_profile }}</p>

          <div v-if="role.interview_questions && role.interview_questions.length > 0">
            <h5 class="font-semibold text-gray-800 mb-2">Suggested Interview Questions:</h5>
            <ul class="list-decimal list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(question, qIdx) in role.interview_questions" :key="qIdx">{{ question.question }}</li>
            </ul>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-600 italic mb-8">
        No specific roles recommended based on the provided information.
      </p>

      <div v-if="talentOutput.team_building_tips && talentOutput.team_building_tips.length > 0" class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">General Team Building Tips</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(tip, index) in talentOutput.team_building_tips" :key="index">{{ tip.tip }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Analyze New Talent Needs
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
const talentOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "SynthGen AI",
  your_industry: "AI/Generative Media",
  funding_stage: "Seed",
  current_team_size: 4,
  key_challenge: "We need to accelerate the development of our core AI model to achieve better real-time generation quality and reduce latency, which is currently a bottleneck for user experience and scalability.",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Handles the submission of the form to get talent navigation insights.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const getTalentNavigation = async () => {
  loading.value = true;
  error.value = null;
  talentOutput.value = null;

  // Construct payload
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '') && !(typeof value === 'number' && isNaN(value))) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'your_industry', 'funding_stage', 'current_team_size', 'key_challenge'];
  const missingFields = requiredFields.filter(field => {
    if (typeof payload[field] === 'string') {
      return payload[field].trim() === '';
    }
    return payload[field] === null || payload[field] === undefined;
  });

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }
  if (payload.key_challenge.length < 20) {
      error.value = `Key Challenge must be at least 20 characters.`;
      loading.value = false;
      return;
  }

  try {
    const data = await callApi('/api/v1/talent-navigator', 'POST', payload);
    talentOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while navigating talent needs. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  talentOutput.value = null;
  error.value = null;
};
</script>