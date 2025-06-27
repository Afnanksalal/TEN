<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header (Navbar) - Always full width and at the very top -->
    <header class="bg-white border-b border-gray-200 p-4 flex justify-between items-center shadow-sm sticky top-0 z-40 w-full h-16">
      <!-- Hamburger Button (always visible) -->
      <button
        class="p-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring"
        @click="toggleSidebar"
        aria-label="Toggle Sidebar"
      >
        <font-awesome-icon :icon="['fas', 'bars']" class="w-6 h-6 text-gray-700" />
      </button>

      <!-- Logo and TEN (aligned right) -->
      <div class="flex items-center space-x-3">
        <span class="text-xl font-extrabold text-gray-800">
          T<span class="text-green-600">EN</span>
        </span>
        <img src="~/assets/images/dadq.png" alt="TEN Logo" class="w-8 h-8 rounded-full object-cover" />
      </div>
    </header>

    <!-- Main Layout Container: Flex for Sidebar and Content -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside
        :class="[
          'flex flex-col bg-white border-r border-gray-200 shadow-lg transition-all duration-300 ease-in-out',
          'h-full', // Takes full height of its flex parent
          isSidebarOpen ? 'w-64' : 'w-20', // Controls width for both mobile and desktop collapsed/open states
        ]"
      >
        <!-- NEW: Collapsed Sidebar Header - Always visible with large icon -->
        <div class="p-4 flex items-center justify-center border-b border-gray-200 h-16 bg-white z-10 flex-shrink-0">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <!-- Large Compass Icon - Always visible in collapsed state -->
            <font-awesome-icon :icon="['fas', 'compass']" class="w-8 h-8 text-green-600" />
            <!-- "TEN" text - Only visible when sidebar is open -->
            <span v-if="isSidebarOpen" class="text-2xl font-extrabold text-gray-800 whitespace-nowrap">
              T<span class="text-green-600">EN</span>
            </span>
          </NuxtLink>
        </div>

        <!-- Sidebar Navigation Links -->
        <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
          <button
            v-for="item in navigationItems"
            :key="item.id"
            @click="activeTab = item.id"
            :class="[
              'flex items-center p-3 rounded-xl transition-all duration-200 w-full',
              isSidebarOpen ? 'justify-start space-x-3' : 'justify-center', // Center icons when collapsed, align left when open
              activeTab === item.id
                ? 'bg-green-100 text-green-800 font-semibold border border-green-300'
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <font-awesome-icon :icon="item.icon" class="w-5 h-5 flex-shrink-0" />
            <span v-if="isSidebarOpen" class="whitespace-nowrap">{{ item.label }}</span>
          </button>
        </nav>
      </aside>

      <!-- Main Content Container -->
      <div
        :class="[
          'flex flex-col flex-1 transition-all duration-300 ease-in-out',
          // Apply margin-left to push content away from the sidebar.
          // The image clearly shows the main content starts further in.
          // A consistent ml-20 or ml-24 might be appropriate, or dynamic based on sidebar width.
          // Let's try to match the image's overall offset, which appears larger than just 'w-20'.
          // Let's assume the collapsed sidebar is w-20, and the content starts with an effective ml-20
          // (which would then be a total offset of 40px from screen edge to text start).
          // Or, more simply: just add a consistent large left padding to main content.
        ]"
      >
        <main class="flex-1 overflow-y-auto p-4 pt-16 pl-24 pr-4">
          <!-- Added pl-24 to main: This creates the consistent offset from the left edge of the screen,
               which corresponds to the right edge of the collapsed sidebar plus some internal padding
               to match the "Welcome to TEN" text alignment in the image.
               pr-4 keeps right padding consistent. -->
          <div class="max-w-6xl mx-auto">
            <component :is="activeComponent" @change-tab="activeTab = $event" />
          </div>
        </main>

        <!-- Bottom Navigation for Mobile (hidden on desktop) -->
        <BottomNavigation
          :active-tab="activeTab"
          :navigation-items="navigationItems"
          @tab-change="newTab => activeTab = newTab"
          class="lg:hidden"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import BottomNavigation from '@/components/BottomNavigation.vue'

// Import your components for dynamic rendering
import Dashboard from '@/components/Dashboard.vue'
import RiskAssessment from '@/components/RiskAssessment.vue'
import ReputationAnalysis from '@/components/ReputationAnalysis.vue'
import InvestorMatch from '@/components/InvestorMatch.vue'
import PitchFeedback from '@/components/PitchFeedback.vue'
import CompetitorRadar from '@/components/CompetitorRadar.vue'
import TractionEstimator from '@/components/TractionEstimator.vue'
import LegalAssistance from '@/components/LegalAssistance.vue'
import ExitStrategyExplorer from '@/components/ExitStrategyExplorer.vue'
import BuzzBuilder from '@/components/BuzzBuilder.vue'
import TalentNavigator from '@/components/TalentNavigator.vue'

// Reactive state variables
const isSidebarOpen = ref(false) // Sidebar starts collapsed by default on all views
const activeTab = ref('dashboard') // Default active tab

// `isDesktop` flag is used for logic where behavior *differs* between mobile and desktop,
// but for sidebar open/close, the behavior is now unified via the hamburger.
const isDesktop = ref(false)

// Function to toggle the sidebar's open/collapsed state
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// Function to check the viewport width and update `isDesktop`
const checkViewport = () => {
  isDesktop.value = window.innerWidth >= 1024
}

// Watcher to manage sidebar state when `isDesktop` changes (e.g., on window resize)
watch(isDesktop, () => {
  // Always reset the sidebar to its collapsed state when viewport mode changes.
  // This ensures consistent behavior regardless of where the user resized from.
  isSidebarOpen.value = false;
}, { immediate: true }) // `immediate: true` runs the watcher once on component mount

// Lifecycle hooks for managing event listeners
onMounted(() => {
  checkViewport() // Perform initial check when component mounts
  window.addEventListener('resize', checkViewport) // Add event listener for window resize
})

onUnmounted(() => {
  window.removeEventListener('resize', checkViewport) // Clean up event listener on component unmount
})

// Array defining the navigation items for the sidebar and bottom navigation
const navigationItems = [
  { id: 'dashboard', label: 'Dashboard', icon: ['fas', 'home'] },
  { id: 'risk', label: 'Risk Assessment', icon: ['fas', 'briefcase'] },
  { id: 'reputation', label: 'Reputation', icon: ['fas', 'comment-dots'] },
  { id: 'investors', label: 'Investor Match', icon: ['fas', 'dollar-sign'] },
  { id: 'pitch', label: 'Pitch Feedback', icon: ['fas', 'file-alt'] },
  { id: 'competitor', label: 'Competitor Radar', icon: ['fas', 'satellite-dish'] },
  { id: 'traction', label: 'Traction Estimator', icon: ['fas', 'chart-line'] },
  { id: 'legal', label: 'Legal Advice', icon: ['fas', 'gavel'] },
  { id: 'exit', label: 'Exit Strategy', icon: ['fas', 'door-open'] },
  { id: 'buzz', label: 'Buzz Builder', icon: ['fas', 'bullhorn'] },
  { id: 'talent', label: 'Talent Navigator', icon: ['fas', 'users'] },
]

// Map of tab IDs to their corresponding Vue components for dynamic rendering
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
  talent: TalentNavigator
}

// Computed property to dynamically render the active component based on `activeTab`
const activeComponent = computed(() => tabComponents[activeTab.value] || Dashboard)
</script>

<style>
/* Global styles for body and html to remove default browser margins/padding */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Prevents horizontal scrollbar if any content accidentally overflows */
}
</style>