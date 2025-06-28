<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header (Navbar) - Remains sticky -->
    <header class="bg-white border-b border-gray-200 p-4 flex justify-between items-center shadow-sm sticky top-0 z-50 w-full h-16">
      <button
        class="p-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring"
        @click="toggleSidebar"
        aria-label="Toggle Sidebar"
      >
        <font-awesome-icon :icon="['fas', 'bars']" class="w-6 h-6 text-gray-700" />
      </button>
      <div class="flex items-center space-x-3">
        <span class="text-xl font-extrabold text-gray-800">
          T<span class="text-green-600">EN</span>
        </span>
        <img src="~/assets/images/dadq.png" alt="TEN Logo" class="w-8 h-8 rounded-full object-cover" />
      </div>
    </header>

    <!-- Main Layout Container -->
    <div class="flex flex-1 overflow-hidden relative">
      <!-- Mobile Overlay -->
      <div
        v-if="isSidebarOpen && !isDesktop"
        class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
        @click="closeSidebar"
      ></div>

      <!-- Sidebar -->
      <aside
        :class="[
          'flex flex-col bg-white border-r border-gray-200 shadow-lg transition-all duration-300 ease-in-out z-40',
          !isDesktop ? [
            'fixed top-16 left-0 bottom-0', // Using flexbox to determine height
            isSidebarOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full'
          ] : [
            'relative h-full',
            isSidebarOpen ? 'w-64' : 'w-20'
          ]
        ]"
      >
        <!-- Sidebar Header (fixed) -->
        <div class="p-4 flex items-center justify-center border-b border-gray-200 h-16 bg-white z-10 flex-shrink-0">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <font-awesome-icon :icon="['fas', 'compass']" class="w-8 h-8 text-green-600" />
            <span 
              v-if="isSidebarOpen" 
              :class="[
                'text-2xl font-extrabold text-gray-800 whitespace-nowrap transition-opacity duration-300',
                isSidebarOpen ? 'opacity-100' : 'opacity-0'
              ]"
            >
              T<span class="text-green-600">EN</span>
            </span>
          </NuxtLink>
        </div>
        <!-- Sidebar Navigation (scrollable) -->
        <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
          <button
            v-for="item in navigationItems"
            :key="item.id"
            @click="handleTabChange(item.id)"
            :class="[
              'flex items-center p-3 rounded-xl transition-all duration-200 w-full',
              isSidebarOpen ? 'justify-start space-x-3' : 'justify-center',
              activeTab === item.id
                ? 'bg-green-100 text-green-800 font-semibold border border-green-300'
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <font-awesome-icon :icon="item.icon" class="w-5 h-5 flex-shrink-0" />
            <span v-if="isSidebarOpen" class="whitespace-nowrap transition-opacity duration-300">
              {{ item.label }}
            </span>
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <div
        :class="[
          'flex flex-col flex-1 transition-all duration-300 ease-in-out min-w-0',
          !isDesktop ? 'ml-0' : 'ml-0'
        ]"
      >
        <main 
          :class="[
            'flex-1 overflow-y-auto transition-all duration-300',
            !isDesktop && isSidebarOpen ? 'opacity-0 pointer-events-none' : 'opacity-100',
            'p-4 md:p-6'
          ]"
        >
          <div class="max-w-7xl mx-auto">
            <component :is="activeComponent" @change-tab="handleTabChange" />
          </div>
        </main>

        <!-- Bottom Navigation for Mobile -->
        <BottomNavigation
          v-if="!isDesktop"
          :active-tab="activeTab"
          :navigation-items="navigationItems"
          @tab-change="handleTabChange"
          :class="[
            'lg:hidden transition-all duration-300',
            !isDesktop && isSidebarOpen ? 'opacity-0 pointer-events-none' : 'opacity-100'
          ]"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import BottomNavigation from '@/components/BottomNavigation.vue';

// Import components for tabs
import Dashboard from '@/components/Dashboard.vue';
import RiskAssessment from '@/components/RiskAssessment.vue';
import ReputationAnalysis from '@/components/ReputationAnalysis.vue';
import InvestorMatch from '@/components/InvestorMatch.vue';
import PitchFeedback from '@/components/PitchFeedback.vue';
import CompetitorRadar from '@/components/CompetitorRadar.vue';
import TractionEstimator from '@/components/TractionEstimator.vue';
import LegalAssistance from '@/components/LegalAssistance.vue';
import ExitStrategyExplorer from '@/components/ExitStrategyExplorer.vue';
import BuzzBuilder from '@/components/BuzzBuilder.vue';
import TalentNavigator from '@/components/TalentNavigator.vue';

// Reactive state variables
const isSidebarOpen = ref(false);
const activeTab = ref('dashboard');
const isDesktop = ref(false);

// Toggle the sidebar
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Close sidebar (for overlay click)
const closeSidebar = () => {
  if (!isDesktop.value) {
    isSidebarOpen.value = false;
  }
};

// Handle tab changes from sidebar or dashboard cards
const handleTabChange = (tabId) => {
  activeTab.value = tabId;
  // Close sidebar on mobile when a tab is selected
  if (!isDesktop.value) {
    isSidebarOpen.value = false;
  }
};

// Handle viewport changes
const checkViewport = () => {
  isDesktop.value = window.innerWidth >= 1024;
};

// Watch for sidebar open on mobile to lock body scroll
watch([isSidebarOpen, isDesktop], ([newIsSidebarOpen, newIsDesktop]) => {
  if (!newIsDesktop && newIsSidebarOpen) {
    document.body.classList.add('body-scroll-lock');
  } else {
    document.body.classList.remove('body-scroll-lock');
  }
});

// Lifecycle hooks
onMounted(() => {
  checkViewport();
  window.addEventListener('resize', checkViewport);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkViewport);
  document.body.classList.remove('body-scroll-lock'); // Cleanup on unmount
});

// Sidebar navigation items
const navigationItems = [
  { id: 'dashboard', label: 'Dashboard', icon: ['fas', 'home'] },
  { id: 'risk', label: 'Risk Assessment', icon: ['fas', 'briefcase'] },
  { id: 'reputation', label: 'Reputation', icon: ['fas', 'comment-dots'] },
  { id: 'investors', label: 'Investor Match', icon: ['fas', 'dollar-sign'] },
  { id: 'pitch', label: 'Pitch Feedback', icon: ['fas', 'file-alt'] },
  { id: 'competitor', label: 'Competitor Radar', icon: ['fas', 'bullseye'] },
  { id: 'traction', label: 'Traction Estimator', icon: ['fas', 'chart-line'] },
  { id: 'legal', label: 'Legal Advice', icon: ['fas', 'gavel'] },
  { id: 'exit', label: 'Exit Strategy', icon: ['fas', 'door-open'] },
  { id: 'buzz', label: 'Buzz Builder', icon: ['fas', 'bullhorn'] },
  { id: 'talent', label: 'Talent Navigator', icon: ['fas', 'users'] },
];

// Map tabs to components
const tabComponents = {
  dashboard: Dashboard,
  risk: RiskAssessment,
  reputation: ReputationAnalysis,
  investors: InvestorMatch,
  pitch: PitchFeedback,
  competitor: CompetitorRadar,
  traction: TractionEstimator,
  legal: LegalAssistance,
  exit: ExitStrategyExplorer,
  buzz: BuzzBuilder,
  talent: TalentNavigator,
};

// Active component
const activeComponent = computed(() => tabComponents[activeTab.value] || Dashboard);
</script>

<style>
.body-scroll-lock {
  overflow: hidden;
}
</style>