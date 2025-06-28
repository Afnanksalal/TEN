<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header (Navbar) - Always full width and at the very top -->
    <header class="bg-white border-b border-gray-200 p-4 flex justify-between items-center shadow-sm sticky top-0 z-50 w-full h-16">
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
    <div class="flex flex-1 overflow-hidden relative">
      <!-- Mobile Overlay when sidebar is open -->
      <div
        v-if="isSidebarOpen && !isDesktop"
        class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
        @click="closeSidebar"
      ></div>

      <!-- Sidebar -->
      <aside
        :class="[
          'flex flex-col bg-white border-r border-gray-200 shadow-lg transition-all duration-300 ease-in-out z-40',
          // Mobile behavior - fixed positioning
          !isDesktop ? [
            'fixed top-16 left-0 bottom-0 h-full',
            isSidebarOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full'
          ] : [
            // Desktop behavior - relative positioning with proper width
            'relative h-full',
            isSidebarOpen ? 'w-64' : 'w-20'
          ]
        ]"
      >
        <!-- Sidebar Header -->
        <div class="p-4 flex items-center justify-center border-b border-gray-200 h-16 bg-white z-10 flex-shrink-0">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <!-- Large Compass Icon - Always visible -->
            <font-awesome-icon :icon="['fas', 'compass']" class="w-8 h-8 text-green-600" />
            <!-- "TEN" text - Visible when sidebar is open -->
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

        <!-- Sidebar Navigation Links -->
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
            <span 
              v-if="isSidebarOpen" 
              :class="[
                'whitespace-nowrap transition-opacity duration-300',
                isSidebarOpen ? 'opacity-100' : 'opacity-0'
              ]"
            >
              {{ item.label }}
            </span>
          </button>
        </nav>
      </aside>

      <!-- Main Content Container -->
      <div
        :class="[
          'flex flex-col flex-1 transition-all duration-300 ease-in-out min-w-0',
          // Mobile: no margin adjustment, overlay behavior
          !isDesktop ? 'ml-0' : [
            // Desktop: margin based on sidebar state
            isSidebarOpen ? 'ml-0' : 'ml-0'
          ]
        ]"
      >
        <!-- Main Content -->
        <main 
          :class="[
            'flex-1 overflow-y-auto transition-all duration-300',
            // Hide main content on mobile when sidebar is open
            !isDesktop && isSidebarOpen ? 'opacity-0 pointer-events-none' : 'opacity-100',
            // Padding adjustments
            'p-4 md:p-6'
          ]"
        >
          <div class="max-w-7xl mx-auto">
            <component :is="activeComponent" @change-tab="handleTabChange" />
          </div>
        </main>

        <!-- Bottom Navigation for Mobile (hidden on desktop) -->
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
const isSidebarOpen = ref(false) // Sidebar starts collapsed by default
const activeTab = ref('dashboard') // Default active tab
const isDesktop = ref(false)

// Function to toggle the sidebar's open/collapsed state
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// Function to close sidebar (for mobile overlay)
const closeSidebar = () => {
  if (!isDesktop.value) {
    isSidebarOpen.value = false
  }
}

// Function to handle tab changes
const handleTabChange = (tabId) => {
  activeTab.value = tabId
  // Close sidebar on mobile when navigating
  if (!isDesktop.value) {
    isSidebarOpen.value = false
  }
}

// Function to check the viewport width and update isDesktop
const checkViewport = () => {
  // Using 1024px as desktop breakpoint (lg: in Tailwind)
  isDesktop.value = window.innerWidth >= 1024
}

// Watcher to manage sidebar state when isDesktop changes
watch(isDesktop, (newValue, oldValue) => {
  // Close sidebar when switching to mobile
  if (!newValue && oldValue) {
    isSidebarOpen.value = false
  }
}, { immediate: true })

// Lifecycle hooks for managing event listeners
onMounted(() => {
  checkViewport()
  window.addEventListener('resize', checkViewport)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkViewport)
})

// Array defining the navigation items for the sidebar and bottom navigation
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

// Computed property to dynamically render the active component based on activeTab
const activeComponent = computed(() => tabComponents[activeTab.value] || Dashboard)
</script>

<style>
/* Global styles for body and html to remove default browser margins/padding */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Smooth transitions for mobile sidebar */
@media (max-width: 1023px) {
  .sidebar-mobile {
    transform: translateX(-100%);
  }
  
  .sidebar-mobile.open {
    transform: translateX(0);
  }
}

/* Ensure proper z-index stacking */
.z-30 { z-index: 30; }
.z-40 { z-index: 40; }
.z-50 { z-index: 50; }

/* Fix for desktop layout to prevent content shift */
@media (min-width: 1024px) {
  .main-layout {
    display: flex;
    width: 100%;
  }
}
</style>