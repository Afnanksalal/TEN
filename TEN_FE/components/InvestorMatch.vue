<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-4xl mx-auto my-8">
    <h2 class="text-4xl font-extrabold text-gray-900 mb-4 text-center">Investor Matchmaker</h2>
    <p class="text-lg text-gray-700 mb-8 text-center">
      Find potential investors tailored to your startup's profile, risk level, and reputation.
    </p>

    <form @submit.prevent="matchInvestors" class="space-y-6 mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Your Startup's Funding Needs</h3>

      <!-- Input Fields -->
      <div>
        <label for="startupName" class="block text-sm font-medium text-gray-700 mb-1">Startup Name <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="startupName"
          v-model="inputData.startup_name"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm"
          placeholder="e.g., GreenTech Solutions"
        />
      </div>

      <div>
        <label for="industry" class="block text-sm font-medium text-gray-700 mb-1">Industry <span class="text-red-500">*</span></label>
        <input
          type="text"
          id="industry"
          v-model="inputData.industry"
          required
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm"
          placeholder="e.g., Renewable Energy, EdTech, DeepTech"
        />
      </div>

      <div>
        <label for="fundingSought" class="block text-sm font-medium text-gray-700 mb-1">Funding Sought (USD) <span class="text-red-500">*</span></label>
        <input
          type="number"
          id="fundingSought"
          v-model.number="inputData.funding_sought_usd"
          required
          min="1"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm"
          placeholder="e.g., 2000000 (2 Million)"
        />
      </div>

      <h3 class="text-2xl font-semibold text-gray-800 mt-8 mb-4">Risk & Reputation Summaries (Simulated for Demo)</h3>
      <p class="text-gray-700 mb-4">
        For a real application, these would ideally come from the <span class="font-semibold">Risk Assessment</span> and <span class="font-semibold">Reputation Analysis</span> tools.
        For this demo, please provide brief summaries below.
      </p>

      <div>
        <label for="riskProfileSummary" class="block text-sm font-medium text-gray-700 mb-1">Risk Profile Summary <span class="text-red-500">*</span></label>
        <textarea
          id="riskProfileSummary"
          v-model="inputData.risk_profile_summary"
          required
          rows="3"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm"
          placeholder="e.g., 'Overall high risk due to market volatility, but strong founder experience mitigates execution risk.' or 'Low risk, strong financial metrics and patented IP.'"
        ></textarea>
      </div>

      <div>
        <label for="reputationProfileSummary" class="block text-sm font-medium text-gray-700 mb-1">Reputation Profile Summary <span class="text-red-500">*</span></label>
        <textarea
          id="reputationProfileSummary"
          v-model="inputData.reputation_profile_summary"
          required
          rows="3"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm"
          placeholder="e.g., 'Excellent online sentiment, mostly positive press about innovative product. No major negative themes.' or 'Mixed sentiment due to early product bugs, but actively addressing feedback.'"
        ></textarea>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Finding Investors...
        </span>
        <span v-else>Find Investor Matches</span>
      </button>
    </form>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ error }}</span>
    </div>

    <div v-if="investorOutput" class="result-section p-6 border border-gray-200 rounded-lg bg-gray-50">
      <h3 class="text-3xl font-semibold text-gray-800 mb-6 text-center">Top Investor Matches for {{ investorOutput.startup_name }}</h3>

      <div class="space-y-6">
        <div v-for="match in investorOutput.matched_investors" :key="match.investor.id" class="p-6 bg-white border border-orange-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-2xl font-bold text-orange-700">{{ match.investor.name }}</h4>
            <div :class="matchScoreClass(match.match_score)" class="text-xl font-bold px-3 py-1 rounded-full">{{ match.match_score.toFixed(0) }}% Match</div>
          </div>

          <p class="text-gray-700 mb-4">
            {{ match.investor.name }} is a {{ match.investor.risk_tolerance.toLowerCase() }} risk investor focusing on {{ match.investor.preferred_industries.join(', ') }} with investments typically ranging from ${{ formatCurrency(match.investor.min_investment_usd) }} to ${{ formatCurrency(match.investor.max_investment_usd) }}.
          </p>
          <a v-if="match.investor.link" :href="match.investor.link" target="_blank" rel="noopener noreferrer" class="inline-flex items-center text-orange-600 hover:text-orange-800 font-medium">
            Visit Profile
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          </a>

          <div class="mt-4 mb-2">
            <h5 class="font-semibold text-gray-800 mb-2">Why it's a good match:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(reason, idx) in match.match_reasons" :key="idx">{{ reason }}</li>
            </ul>
          </div>

          <div v-if="match.gaps && match.gaps.length" class="mt-4">
            <h5 class="font-semibold text-gray-800 mb-2">Potential Gaps to Address:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(gap, idx) in match.gaps" :key="idx">{{ gap }}</li>
            </ul>
          </div>

          <div class="mt-4">
            <h5 class="font-semibold text-gray-800 mb-2">Investor's Feedback Focus:</h5>
            <ul class="list-disc list-inside text-gray-700 pl-4 space-y-1">
              <li v-for="(focus, idx) in match.investor.feedback_focus" :key="idx">{{ focus }}</li>
            </ul>
          </div>
        </div>
      </div>

      <p v-if="!investorOutput.matched_investors || investorOutput.matched_investors.length === 0" class="text-center text-gray-600 italic mt-8">
        No direct investor matches found based on your criteria. Try adjusting your profile or seeking different investor types.
      </p>

      <button @click="resetForm" class="w-full mt-8 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-colors">
        Find New Matches
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useApi } from '@/composables/useApi';

const { callApi } = useApi();

const loading = ref(false);
const error = ref(null);
const investorOutput = ref(null);

// Dummy data for inputs, including simplified risk/reputation summaries
const getInitialInputState = () => ({
  startup_name: "GreenTech Innovators",
  industry: "Renewable Energy",
  funding_sought_usd: 1500000, // 1.5 Million USD
  risk_profile_summary: "Overall medium risk due to early stage but strong team and clear market need. Key risks include regulatory changes and supply chain dependencies.",
  reputation_profile_summary: "Strong positive sentiment from early adopters and industry experts. Recent press mentions highlight our innovative approach to solar efficiency. No major negative sentiment.",
});

const inputData = reactive(getInitialInputState());

// Helper to format currency for display
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

// Dynamic class for match score background
const matchScoreClass = (score) => {
  if (score >= 80) return 'bg-green-100 text-green-800';
  if (score >= 50) return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
};

const matchInvestors = async () => {
  loading.value = true;
  error.value = null;
  investorOutput.value = null;

  // Basic client-side validation
  const requiredFields = ['startup_name', 'industry', 'funding_sought_usd', 'risk_profile_summary', 'reputation_profile_summary'];
  const missingFields = requiredFields.filter(field => !inputData[field] || (typeof inputData[field] === 'string' && inputData[field].trim() === ''));

  if (missingFields.length > 0) {
    error.value = `Please fill in all required fields: ${missingFields.map(f => f.replace(/_/g, ' ').toUpperCase()).join(', ')}.`;
    loading.value = false;
    return;
  }
  
  // Construct the payload matching InvestorMatchInput schema, 
  // fabricating RiskOutput and ReputationOutput from summaries for this demo.
  // In a real app with Pinia, you'd pull full objects here.
  const payload = {
    startup_name: inputData.startup_name.trim(),
    industry: inputData.industry.trim(),
    funding_sought_usd: inputData.funding_sought_usd,
    risk_profile: {
      startup_name: inputData.startup_name.trim(),
      overall_risk_score: 50.0, // Dummy score
      risk_factors: [ // Dummy risk factors
        { name: "Overall Risk", level: "medium", mitigation_suggestion: inputData.risk_profile_summary.trim() }
      ],
      recommendations: ["Based on your summary: " + inputData.risk_profile_summary.trim()],
    },
    reputation_profile: {
      startup_name: inputData.startup_name.trim(),
      overall_sentiment_score: 0.5, // Dummy sentiment
      positive_themes: ["Innovation", "Efficiency"], // Dummy themes
      negative_themes: [],
      neutral_themes: [],
      actionable_insights: ["Based on your summary: " + inputData.reputation_profile_summary.trim()],
      overall_reputation_review: "Positive outlook" // Dummy review
    }
  };

  try {
    const data = await callApi('/api/v1/match-investors', 'POST', payload);
    investorOutput.value = data;
  } catch (err) {
    console.error("API call error:", err);
    error.value = err.message || "An unexpected error occurred while finding investor matches. Please try again.";
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  Object.assign(inputData, getInitialInputState());
  investorOutput.value = null;
  error.value = null;
};
</script>