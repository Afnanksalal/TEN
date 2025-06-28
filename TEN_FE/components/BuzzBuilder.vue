<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Buzz Builder</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Generate engaging content ideas and strategies to create buzz around your startup.
    </p>

    <form @submit.prevent="generateBuzz" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Buzz Details</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Your Startup's Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
          placeholder="e.g., NovaLaunch"
        />
      </div>

      <div>
        <label for="yourIndustry" class="block text-sm font-medium text-gray-700 mb-1">Your Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="yourIndustry"
          v-model="inputData.your_industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
          placeholder="e.g., SpaceTech, AI, Health & Wellness"
        />
      </div>

      <div>
        <label for="currentMilestones" class="block text-sm font-medium text-gray-700 mb-1">Current Milestones (Comma-separated) <span class="text-red-500">*</span></label>
        <textarea
          id="currentMilestones"
          v-model="inputData.current_milestones"
          required
          rows="3"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
          placeholder="e.g., Launched MVP, Secured 1000 users, Raised seed round, Featured in TechCrunch"
        ></textarea>
      </div>

      <div>
        <label for="keyMessage" class="block text-sm font-medium text-gray-700 mb-1">Key Message/Narrative <span class="text-red-500">*</span></label>
        <textarea
          id="keyMessage"
          v-model="inputData.key_message"
          required
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
          placeholder="What is the main message you want to convey about your startup right now?"
        ></textarea>
      </div>

      <div>
        <label for="targetAudience" class="block text-sm font-medium text-gray-700 mb-1">Target Audience <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="targetAudience"
          v-model="inputData.target_audience"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
          placeholder="e.g., Early Adopters, Investors, Potential Hires, B2B Customers"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Generating Buzz Ideas...
        </span>
        <span v-else>Generate Buzz Ideas</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="buzzOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Buzz Ideas for {{ buzzOutput.startup_name }}</h3>

      <div v-if="buzzOutput.suggestions && buzzOutput.suggestions.length > 0" class="space-y-8 mb-8">
        <div v-for="(suggestion, index) in buzzOutput.suggestions" :key="index" class="p-6 bg-white border border-amber-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <h4 class="text-2xl font-bold text-amber-700 mb-3">{{ suggestion.platform }}</h4>
          <p class="text-xl font-semibold text-gray-800 mb-3">{{ suggestion.title }}</p>

          <div class="mb-4">
            <h5 class="font-semibold text-gray-800 mb-2">Content Points:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(point, pIdx) in suggestion.content_points" :key="pIdx">{{ point }}</li>
            </ul>
          </div>

          <div v-if="suggestion.hashtags && suggestion.hashtags.length > 0" class="mb-4">
            <h5 class="font-semibold text-gray-800 mb-2">Hashtags:</h5>
            <div class="flex flex-wrap gap-2">
              <span v-for="(tag, tIdx) in suggestion.hashtags" :key="tIdx" class="bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-sm font-medium">
                {{ tag }}
              </span>
            </div>
          </div>

          <p v-if="suggestion.call_to_action" class="font-semibold text-gray-800">
            Call to Action: <span class="text-gray-700">{{ suggestion.call_to_action }}</span>
          </p>
        </div>
      </div>
      <p v-else class="text-center text-gray-600 italic mb-8">
        No buzz suggestions generated based on the provided information.
      </p>

      <!-- AI Tips -->
      <div v-if="buzzOutput.ai_tips && buzzOutput.ai_tips.length > 0" class="mt-6 p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h4 class="text-2xl font-semibold text-gray-800 mb-4 text-center">AI Tips for Maximizing Buzz</h4>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-4">
          <li v-for="(tip, index) in buzzOutput.ai_tips" :key="index">{{ tip }}</li>
        </ul>
      </div>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Generate New Buzz
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
const buzzOutput = ref(null);

// Function to define the initial/dummy state for the form inputs
const getInitialInputState = () => ({
  startup_name: "InnovateVerse VR",
  your_industry: "Virtual Reality Gaming",
  current_milestones: "Completed Beta Phase, Launched on Steam Early Access, Received 5-star reviews from major VR publications, Secured $1M Seed Round",
  key_message: "InnovateVerse VR is redefining immersive gaming with its unique open-world VR RPG that blends stunning graphics with player-driven narratives. We're creating a new standard for virtual reality experiences.",
  target_audience: "Core Gamers, VR Enthusiasts, Sci-Fi Fans, Early Adopters",
});

// Reactive variable for input data, initialized with dummy data
const inputData = reactive(getInitialInputState());

/**
 * Handles the submission of the form to generate buzz ideas.
 * It constructs the payload, performs client-side validation, and calls the API.
 */
const generateBuzz = async () => {
  loading.value = true;
  error.value = null;
  buzzOutput.value = null;

  // Prepare payload: convert comma-separated milestones string to a list
  const payload = {
    startup_name: inputData.startup_name.trim(),
    your_industry: inputData.your_industry.trim(),
    current_milestones: inputData.current_milestones.split(',').map(m => m.trim()).filter(m => m.length > 0),
    key_message: inputData.key_message.trim(),
    target_audience: inputData.target_audience.trim(),
  };

  // Basic client-side validation for required fields
  const requiredFields = ['startup_name', 'your_industry', 'current_milestones', 'key_message', 'target_audience'];
  const missingFields = requiredFields.filter(field => {
    if (field === 'current_milestones') {
      return payload.current_milestones.length === 0;
    }
    return !payload[field] || (typeof payload[field] === 'string' && payload[field].trim() === '');
  });

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }

  try {
    const data = await callApi('/api/v1/buzz-builder', 'POST', payload);
    buzzOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while generating buzz ideas. Please try again.";
  } finally {
    loading.value = false;
  }
};

/**
 * Resets the form inputs to their initial dummy state and clears results/errors.
 */
const resetForm = () => {
  Object.assign(inputData, getInitialInputState()); // Reset using the initial state function
  buzzOutput.value = null;
  error.value = null;
};
</script>