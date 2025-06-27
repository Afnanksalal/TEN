<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Startup Reputation Analysis</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Gain insights into your startup's sentiment and identify key themes.
    </p>

    <form @submit.prevent="analyzeReputation" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Reputation Input</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
          placeholder="e.g., Quantum Innovations"
        />
      </div>

      <div>
        <label for="founderTwitterHandle" class="block text-sm font-medium text-gray-700 mb-1">Founder's Twitter Handle (Optional)</label>
        <input
          type="text"
          id="founderTwitterHandle"
          v-model="inputData.founder_twitter_handle"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
          placeholder="e.g., @elonmusk (without the @)"
        />
      </div>

      <div>
        <label for="initialPitchText" class="block text-sm font-medium text-gray-700 mb-1">Initial Pitch/Description Text <span class="text-red-500">*</span></label>
        <textarea
          id="initialPitchText"
          v-model="inputData.initial_pitch_text"
          required
          rows="5"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
          placeholder="Provide a summary of your startup, its mission, and what it does. Min 50 characters."
        ></textarea>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Analyzing Reputation...
        </span>
        <span v-else>Analyze Reputation</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="reputationOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Reputation Analysis Results for {{ reputationOutput.startup_name }}</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- Reputation Score -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm flex flex-col justify-center items-center">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Overall Sentiment Score</h4>
          <div :class="sentimentScoreClass(normalizedSentimentScore)" class="text-5xl font-extrabold mb-2">{{ normalizedSentimentScore.toFixed(0) }}%</div>
          <p :class="sentimentReviewClass(normalizedSentimentScore)" class="text-xl font-medium text-center">{{ reputationOutput.overall_reputation_review }}</p>
        </div>

        <!-- Sentiment Breakdown -->
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm lg:col-span-2">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Sentiment Breakdown</h4>
          <div class="space-y-4">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-green-600 font-medium">Positive</span>
                <span class="font-bold">{{ positiveSentimentPercentage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="bg-green-500 h-2.5 rounded-full" :style="{ width: positiveSentimentPercentage + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-gray-600 font-medium">Neutral</span>
                <span class="font-bold">{{ neutralSentimentPercentage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="bg-gray-500 h-2.5 rounded-full" :style="{ width: neutralSentimentPercentage + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-red-600 font-medium">Negative</span>
                <span class="font-bold">{{ negativeSentimentPercentage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="bg-red-500 h-2.5 rounded-full" :style="{ width: negativeSentimentPercentage + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sentiment Themes -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div v-if="reputationOutput.positive_themes && reputationOutput.positive_themes.length" class="p-6 bg-white border border-green-200 rounded-lg shadow-sm">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Positive Themes</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-1 pl-4">
            <li v-for="(theme, index) in reputationOutput.positive_themes" :key="index">{{ theme }}</li>
          </ul>
        </div>
        <div v-if="reputationOutput.neutral_themes && reputationOutput.neutral_themes.length" class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Neutral Themes</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-1 pl-4">
            <li v-for="(theme, index) in reputationOutput.neutral_themes" :key="index">{{ theme }}</li>
          </ul>
        </div>
        <div v-if="reputationOutput.negative_themes && reputationOutput.negative_themes.length" class="p-6 bg-white border border-red-200 rounded-lg shadow-sm">
          <h4 class="text-xl font-semibold text-gray-800 mb-4">Negative Themes</h4>
          <ul class="list-disc list-inside text-gray-700 space-y-1 pl-4">
            <li v-for="(theme, index) in reputationOutput.negative_themes" :key="index">{{ theme }}</li>
          </ul>
        </div>
      </div>

      <!-- Actionable Insights -->
      <div class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Actionable Insights</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(insight, index) in reputationOutput.actionable_insights" :key="index">{{ insight }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Analyze New Reputation
      </button>
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
const reputationOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "SynthSphere AI",
  founder_twitter_handle: "ai_innovator", // Example handle, no @
  initial_pitch_text: "SynthSphere AI is developing a groundbreaking platform for personalized content generation using advanced neural networks. Our technology can create unique articles, marketing copy, and even short stories tailored to individual user preferences, revolutionizing digital media consumption and creation. We aim to empower creators and businesses with scalable, high-quality content at an unprecedented speed. Our core innovation lies in our proprietary multi-modal learning models that integrate text, image, and audio inputs to generate coherent and engaging outputs. We believe this will disrupt traditional content creation workflows.",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

// Computed properties for displaying sentiment scores as percentages
const normalizedSentimentScore = computed(() => {
  if (!reputationOutput.value) return 0;
  // API score is -1 to 1, normalize to 0-100%
  return ((reputationOutput.value.overall_sentiment_score + 1) / 2) * 100;
});

// For a rough breakdown, assuming themes imply proportion
// This is a simplification as the API only gives themes, not percentages.
// If the API provided positive_score, negative_score, neutral_score, use those directly.
// For now, we'll derive some example percentages.
const positiveSentimentPercentage = computed(() => {
    if (!reputationOutput.value) return 0;
    // Example: If sentiment is 0.7, map to ~80% positive
    return Math.min(100, Math.max(0, Math.round((normalizedSentimentScore.value / 100) * 100)));
});

const negativeSentimentPercentage = computed(() => {
    if (!reputationOutput.value) return 0;
    // Example: If sentiment is 0.7, map to ~10% negative
    return Math.min(100, Math.max(0, Math.round((1 - (normalizedSentimentScore.value / 100)) * 50)));
});

const neutralSentimentPercentage = computed(() => {
    if (!reputationOutput.value) return 0;
    // Remaining for neutral
    return 100 - positiveSentimentPercentage.value - negativeSentimentPercentage.value;
});


/**
 * Determines the overall sentiment score text color based on normalized score.
 * @param {number} score - The normalized sentiment score (0-100).
 * @returns {string} Tailwind CSS class for text color.
 */
const sentimentScoreClass = (score) => {
  if (score >= 70) return 'text-green-600';
  if (score >= 40) return 'text-yellow-600';
  return 'text-red-600';
};

/**
 * Determines the text color for the overall reputation review based on normalized score.
 * @param {number} score - The normalized sentiment score (0-100).
 * @returns {string} Tailwind CSS class for text color.
 */
const sentimentReviewClass = (score) => {
  return sentimentScoreClass(score); // Reuses the score color logic
};

/**
 * Handles the submission of the form to analyze reputation.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const analyzeReputation = async () => {
  loading.value = true;
  error.value = null;
  reputationOutput.value = null;

  // Trim founder_twitter_handle if provided
  if (inputData.founder_twitter_handle) {
    inputData.founder_twitter_handle = inputData.founder_twitter_handle.replace(/^@/, ''); // Remove leading @ if present
  }

  // Construct payload by filtering out empty/null optional fields
  const payload = {};
  for (const key in inputData) {
    const value = inputData[key];
    if (value !== null && value !== undefined && (typeof value !== 'string' || value.trim() !== '')) {
      payload[key] = typeof value === 'string' ? value.trim() : value;
    }
  }

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'initial_pitch_text'];
  const missingFields = requiredFields.filter(field => !payload[field] || (typeof payload[field] === 'string' && payload[field].length < 50 && field === 'initial_pitch_text'));

  if (missingFields.length > 0) {
    let errorMessage = "Please fill in all required fields.";
    if (missingFields.includes('initial_pitch_text') && payload.initial_pitch_text.length < 50) {
        errorMessage = "Initial Pitch/Description Text must be at least 50 characters.";
    }
    error.value = errorMessage;
    loading.value = false;
    return;
  }


  try {
    const data = await callApi('/api/v1/scan-reputation', 'POST', payload);
    reputationOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while analyzing reputation. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  reputationOutput.value = null;
  error.value = null;
};
</script>