<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Pitch Feedback Assistant</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Get AI-powered feedback and suggestions to refine your startup pitch.
    </p>

    <form @submit.prevent="getPitchFeedback" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Pitch Details</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
          placeholder="e.g., EcoInnovate"
        />
      </div>

      <div>
        <label for="pitchText" class="block text-sm font-medium text-gray-700 mb-1">Full Pitch Text <span class="text-red-500">*</span></label>
        <textarea
          id="pitchText"
          v-model="inputData.pitch_text"
          required
          rows="10"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
          placeholder="Paste your full pitch or executive summary here. Minimum 100 characters."
        ></textarea>
      </div>

      <h3 class="text-2xl font-semibold text-gray-800 mt-8 mb-4">Optional Context (Simulated for Demo)</h3>
      <p class="text-gray-700 mb-4">
        Providing summaries from the <span class="font-semibold">Risk Assessment</span>, <span class="font-semibold">Reputation Analysis</span>, and <span class="font-semibold">Investor Match</span> tools can help tailor the feedback.
      </p>

      <div>
        <label for="riskProfileSummary" class="block text-sm font-medium text-gray-700 mb-1">Risk Profile Summary (Optional)</label>
        <textarea
          id="riskProfileSummary"
          v-model="inputData.risk_profile_summary"
          rows="2"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
          placeholder="e.g., 'Medium risk, strong team but high market competition.'"
        ></textarea>
      </div>

      <div>
        <label for="reputationProfileSummary" class="block text-sm font-medium text-gray-700 mb-1">Reputation Profile Summary (Optional)</label>
        <textarea
          id="reputationProfileSummary"
          v-model="inputData.reputation_profile_summary"
          rows="2"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
          placeholder="e.g., 'Highly positive sentiment, praised for innovation. Few negative mentions.'"
        ></textarea>
      </div>

      <div>
        <label for="investorMatchSummary" class="block text-sm font-medium text-gray-700 mb-1">Investor Match Results Summary (Optional)</label>
        <textarea
          id="investorMatchSummary"
          v-model="inputData.investor_match_summary"
          rows="2"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
          placeholder="e.g., 'Matched with VCs interested in sustainability with high risk tolerance.'"
        ></textarea>
      </div>


      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Analyzing Pitch...
        </span>
        <span v-else>Get Pitch Feedback</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="pitchFeedbackOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Feedback for {{ pitchFeedbackOutput.startup_name }}'s Pitch</h3>

      <div class="space-y-8">
        <!-- General Feedback -->
        <div class="p-6 bg-white border border-emerald-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-bold text-emerald-700 mb-4">General Feedback</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
            <li v-for="(item, index) in pitchFeedbackOutput.feedback" :key="index">{{ item }}</li>
          </ul>
        </div>

        <!-- Suggestions for Improvement -->
        <div class="p-6 bg-white border border-emerald-200 rounded-lg shadow-sm">
          <h4 class="text-2xl font-bold text-emerald-700 mb-4">Suggestions for Improvement</h4>
          <ul class="list-decimal list-inside text-gray-700 space-y-2 pl-4">
            <li v-for="(item, index) in pitchFeedbackOutput.suggestions_for_improvement" :key="index">{{ item }}</li>
          </ul>
        </div>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Analyze Another Pitch
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
const pitchFeedbackOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "EcoInnovate Solutions",
  pitch_text: "EcoInnovate Solutions is developing a revolutionary smart irrigation system that uses AI to optimize water usage for agriculture, reducing waste by up to 60%. Our system integrates real-time weather data, soil moisture sensors, and crop-specific needs to deliver precise amounts of water, minimizing environmental impact and saving farmers significant costs. We have a working prototype and have completed successful pilot programs on three farms, demonstrating average water savings of 45%. Our team comprises experienced agritech engineers and AI specialists. We are seeking seed funding to scale production and expand our market reach. Our long-term vision is to become the leading provider of sustainable agricultural technology globally.",
  risk_profile_summary: "Medium risk, key challenges include initial hardware costs for farmers and regulatory approvals in some regions. Mitigated by strong ROI for farmers.",
  reputation_profile_summary: "Generally positive sentiment from pilot users and environmental groups, praising our commitment to sustainability. Some early concerns about integration complexity are being addressed.",
  investor_match_summary: "Identified several impact investors and VCs specializing in clean technology and sustainable agriculture. Matches indicate high alignment with our mission.",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Handles the submission of the form to get pitch feedback.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const getPitchFeedback = async () => {
  loading.value = true;
  error.value = null;
  pitchFeedbackOutput.value = null;

  // Construct the payload based on PitchFeedbackRequest schema
  // For the optional risk/reputation/investor_match_results,
  // we'll build dummy objects from the provided summaries.
  // In a real app, these would be the actual output objects from other tools.
  const payload = {
    startup_name: inputData.startup_name.trim(),
    pitch_text: inputData.pitch_text.trim(),
  };

  // Add optional profiles if summaries are provided
  if (inputData.risk_profile_summary && inputData.risk_profile_summary.trim().length > 0) {
    payload.risk_profile = {
      startup_name: inputData.startup_name.trim(),
      overall_risk_score: 5.0, // Dummy score
      risk_factors: [{ name: "Contextual Risk", level: "medium", mitigation_suggestion: inputData.risk_profile_summary.trim() }],
      recommendations: ["Based on provided risk context: " + inputData.risk_profile_summary.trim()],
    };
  }

  if (inputData.reputation_profile_summary && inputData.reputation_profile_summary.trim().length > 0) {
    payload.reputation_profile = {
      startup_name: inputData.startup_name.trim(),
      overall_sentiment_score: 0.7, // Dummy sentiment
      positive_themes: [], negative_themes: [], neutral_themes: [], // Empty as we don't have details
      actionable_insights: ["Based on provided reputation context: " + inputData.reputation_profile_summary.trim()],
      overall_reputation_review: "Good based on summary", // Dummy review
    };
  }

  if (inputData.investor_match_summary && inputData.investor_match_summary.trim().length > 0) {
    payload.investor_match_results = {
      startup_name: inputData.startup_name.trim(),
      matched_investors: [{ // Dummy investor match
        investor: { id: "dummy-investor-1", name: "Contextual VC", link: null, risk_tolerance: "medium", preferred_industries: [], min_investment_usd: 0, max_investment_usd: 0, feedback_focus: [] },
        match_score: 75,
        match_reasons: ["Based on provided investor context: " + inputData.investor_match_summary.trim()],
        gaps: []
      }]
    };
  }


  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'pitch_text'];
  const missingFields = requiredFields.filter(field => !payload[field] || (typeof payload[field] === 'string' && payload[field].trim() === ''));

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields.`;
    loading.value = false;
    return;
  }
  if (payload.pitch_text.length < 100) {
      error.value = `Pitch text must be at least 100 characters.`;
      loading.value = false;
      return;
  }


  try {
    const data = await callApi('/api/v1/pitch-feedback', 'POST', payload);
    pitchFeedbackOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while getting pitch feedback. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  pitchFeedbackOutput.value = null;
  error.value = null;
};
</script>