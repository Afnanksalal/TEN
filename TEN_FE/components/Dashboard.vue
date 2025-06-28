<!-- components/Dashboard.vue - Avatar removed as requested -->

<template>
  <div class="w-full min-h-screen bg-gradient-to-br from-gray-50 via-green-50/30 to-blue-50/20 relative overflow-hidden">
    <!-- Background Decorative Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-4 w-16 h-16 bg-gradient-to-r from-green-400/20 to-blue-400/20 rounded-full blur-xl animate-float"></div>
      <div class="absolute top-32 right-8 w-24 h-24 bg-gradient-to-r from-purple-400/15 to-pink-400/15 rounded-full blur-2xl animate-float-delayed"></div>
      <div class="absolute bottom-32 left-8 w-20 h-20 bg-gradient-to-r from-yellow-400/20 to-orange-400/20 rounded-full blur-xl animate-float-slow"></div>
    </div>

    <div class="relative z-10 animate-fade-in w-full">
      <!-- Enhanced Header Section -->
      <div class="text-center mb-6 px-4 pt-4">
        <!-- Main welcome avatar has been removed from here -->

        <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold my-4">
          <span class="bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
            Welcome to 
          </span>
          <span class="bg-gradient-to-r from-green-600 to-green-500 bg-clip-text text-transparent">
            TEN
          </span>
        </h1>
        
        <p class="text-sm sm:text-base md:text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed px-2">
          Explore <span class="font-semibold text-green-600">10 powerful tools</span> tailored to boost your startup journey
        </p>

        <!-- Stats Row -->
        <div class="flex justify-center space-x-4 sm:space-x-8 mt-4">
          <div class="text-center">
            <div class="text-lg sm:text-2xl font-bold text-green-600">10+</div>
            <div class="text-xs sm:text-sm text-gray-500">Tools</div>
          </div>
          <div class="text-center">
            <div class="text-lg sm:text-2xl font-bold text-blue-600">24/7</div>
            <div class="text-xs sm:text-sm text-gray-500">Support</div>
          </div>
          <div class="text-center">
            <div class="text-lg sm:text-2xl font-bold text-purple-600">AI</div>
            <div class="text-xs sm:text-sm text-gray-500">Powered</div>
          </div>
        </div>
      </div>

      <!-- Enhanced Grid of Features -->
      <div class="px-3 sm:px-4 pb-20 lg:pb-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 md:gap-6 max-w-7xl mx-auto">
          <div
            v-for="(feature, index) in features"
            :key="feature.id"
            class="group relative bg-white/90 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-white/50 shadow-lg hover:shadow-2xl transition-all duration-500 hover:scale-105 hover:-translate-y-1"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <!-- Gradient Border Effect -->
            <div class="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl sm:rounded-2xl p-[1px]"
                 :class="feature.gradientClass">
              <div class="bg-white rounded-xl sm:rounded-2xl w-full h-full"></div>
            </div>

            <!-- Content -->
            <div class="relative z-10">
              <!-- Icon with Custom SVG Character -->
              <div class="flex items-start space-x-3 mb-3">
                <div class="relative flex-shrink-0">
                  <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg transition-transform duration-300 group-hover:scale-110"
                       :class="feature.iconBg">
                    <font-awesome-icon :icon="feature.icon" class="text-white w-4 h-4 sm:w-5 sm:h-5" />
                  </div>
                  
                  <!-- Custom SVG Character -->
                  <div class="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:scale-110">
                    <component :is="feature.characterSvg" class="w-6 h-6 sm:w-8 sm:h-8" />
                  </div>
                </div>
                
                <div class="flex-1 min-w-0">
                  <h3 class="text-base sm:text-lg font-bold text-gray-800 group-hover:text-green-600 transition-colors duration-300 leading-tight">
                    {{ feature.label }}
                  </h3>
                </div>
              </div>

              <!-- Description -->
              <p class="text-gray-600 text-xs sm:text-sm mb-4 leading-relaxed">
                {{ feature.description }}
              </p>

              <!-- Enhanced CTA Button -->
              <button
                class="w-full px-3 py-2.5 sm:px-4 sm:py-3 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-700 hover:to-green-600 text-white rounded-lg sm:rounded-xl font-semibold text-xs sm:text-sm transition-all duration-300 transform hover:scale-105 hover:shadow-lg flex items-center justify-center space-x-2 group/btn"
                @click="$emit('change-tab', feature.id)"
              >
                <span>Explore {{ feature.shortLabel }}</span>
                <font-awesome-icon icon="arrow-right" class="w-3 h-3 sm:w-4 sm:h-4 transform group-hover/btn:translate-x-1 transition-transform duration-300" />
              </button>

              <!-- Usage Stats -->
              <div class="mt-2.5 flex items-center justify-between text-xs text-gray-500">
                <span class="flex items-center space-x-1">
                  <div class="w-1.5 h-1.5 bg-green-400 rounded-full"></div>
                  <span>{{ feature.usage }} users</span>
                </span>
                <span class="flex items-center space-x-1">
                  <font-awesome-icon icon="star" class="text-yellow-400 w-3 h-3" />
                  <span>{{ feature.rating }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Call to Action Section -->
        <div class="mt-8 sm:mt-12">
          <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl sm:rounded-2xl p-4 sm:p-6 text-white max-w-4xl mx-auto relative overflow-hidden">
            <!-- Background Pattern -->
            <div class="absolute inset-0 opacity-10">
              <div class="absolute top-2 left-2 text-2xl">🚀</div>
              <div class="absolute top-2 right-2 text-2xl">💰</div>
              <div class="absolute bottom-2 left-2 text-2xl">📈</div>
              <div class="absolute bottom-2 right-2 text-2xl">🎯</div>
            </div>

            <div class="relative z-10 text-center">
              <h2 class="text-lg sm:text-2xl font-bold mb-2 sm:mb-4">Ready to Scale Your Startup?</h2>
              <p class="text-sm sm:text-base opacity-90 mb-4 sm:mb-6">
  Join thousands of entrepreneurs using TEN
</p>
<div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
  <!-- Get Started Free Button -->
  <button 
    class="px-4 py-2.5 sm:px-6 sm:py-3 bg-white text-green-600 rounded-lg sm:rounded-xl font-semibold hover:bg-gray-50 transition-colors duration-300 text-sm sm:text-base">
    Get Started Free
  </button>
  
  <!-- Use API Button -->
  <a
    href="https://ten-be.koyeb.app/redoc"
    target="_blank"
    rel="noopener noreferrer"
    class="px-4 py-2.5 sm:px-6 sm:py-3 border-2 border-white text-white rounded-lg sm:rounded-xl font-semibold hover:bg-white hover:text-green-600 transition-all duration-300 text-sm sm:text-base"
  >
    Use API
  </a>
</div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Custom SVG Character Components
const RiskCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-bounce-slow">
      <circle cx="16" cy="16" r="15" fill="#EF4444" opacity="0.8"/>
      <path d="M12 12 L20 20 M20 12 L12 20" stroke="white" stroke-width="3" stroke-linecap="round"/>
      <circle cx="8" cy="8" r="3" fill="#FCD34D"/>
      <circle cx="24" cy="24" r="2" fill="#10B981"/>
    </svg>
  `
}

const ReputationCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-pulse">
      <circle cx="16" cy="16" r="15" fill="#3B82F6" opacity="0.8"/>
      <circle cx="12" cy="12" r="2" fill="white"/>
      <circle cx="20" cy="12" r="2" fill="white"/>
      <path d="M10 20 Q16 24 22 20" stroke="white" stroke-width="2" fill="none"/>
      <circle cx="8" cy="8" r="2" fill="#F59E0B"/>
      <circle cx="24" cy="8" r="2" fill="#F59E0B"/>
    </svg>
  `
}

const InvestorCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-bounce-slow">
      <circle cx="16" cy="16" r="15" fill="#10B981" opacity="0.8"/>
      <text x="16" y="20" text-anchor="middle" fill="white" font-size="16" font-weight="bold">$</text>
      <circle cx="8" cy="8" r="3" fill="#FCD34D"/>
      <circle cx="24" cy="8" r="3" fill="#FCD34D"/>
      <circle cx="8" cy="24" r="2" fill="#EF4444"/>
    </svg>
  `
}

const PitchCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-pulse">
      <circle cx="16" cy="16" r="15" fill="#8B5CF6" opacity="0.8"/>
      <rect x="10" y="10" width="12" height="8" rx="2" fill="white"/>
      <rect x="12" y="12" width="8" height="1" fill="#8B5CF6"/>
      <rect x="12" y="14" width="6" height="1" fill="#8B5CF6"/>
      <circle cx="6" cy="26" r="2" fill="#F59E0B"/>
    </svg>
  `
}

const CompetitorCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-bounce-slow">
      <circle cx="16" cy="16" r="15" fill="#F97316" opacity="0.8"/>
      <circle cx="16" cy="16" r="8" fill="none" stroke="white" stroke-width="2"/>
      <circle cx="16" cy="16" r="4" fill="white"/>
      <circle cx="16" cy="8" r="2" fill="#EF4444"/>
      <circle cx="8" cy="24" r="2" fill="#10B981"/>
    </svg>
  `
}

const TractionCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-pulse">
      <circle cx="16" cy="16" r="15" fill="#6366F1" opacity="0.8"/>
      <polyline points="8,22 12,18 16,14 20,10 24,6" stroke="white" stroke-width="3" fill="none"/>
      <circle cx="24" cy="6" r="2" fill="#10B981"/>
      <circle cx="8" cy="26" r="2" fill="#F59E0B"/>
    </svg>
  `
}

const LegalCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-bounce-slow">
      <circle cx="16" cy="16" r="15" fill="#6B7280" opacity="0.8"/>
      <rect x="12" y="8" width="8" height="12" rx="1" fill="white"/>
      <rect x="14" y="10" width="4" height="1" fill="#6B7280"/>
      <rect x="14" y="12" width="4" height="1" fill="#6B7280"/>
      <circle cx="16" y="24" r="2" fill="#F59E0B"/>
    </svg>
  `
}

const ExitCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-pulse">
      <circle cx="16" cy="16" r="15" fill="#14B8A6" opacity="0.8"/>
      <rect x="10" y="12" width="12" height="8" rx="2" fill="white"/>
      <circle cx="20" cy="16" r="1" fill="#14B8A6"/>
      <path d="M22 16 L26 16 M24 14 L26 16 L24 18" stroke="white" stroke-width="2" fill="none"/>
    </svg>
  `
}

const BuzzCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-bounce-slow">
      <circle cx="16" cy="16" r="15" fill="#EC4899" opacity="0.8"/>
      <polygon points="12,12 20,16 12,20" fill="white"/>
      <circle cx="6" cy="6" r="2" fill="#F59E0B"/>
      <circle cx="26" cy="6" r="2" fill="#F59E0B"/>
      <circle cx="6" cy="26" r="2" fill="#10B981"/>
    </svg>
  `
}

const TalentCharacter = {
  template: `
    <svg viewBox="0 0 32 32" class="animate-pulse">
      <circle cx="16" cy="16" r="15" fill="#EAB308" opacity="0.8"/>
      <circle cx="12" cy="12" r="3" fill="white"/>
      <circle cx="20" cy="12" r="3" fill="white"/>
      <circle cx="16" cy="22" r="3" fill="white"/>
      <circle cx="8" cy="8" r="2" fill="#10B981"/>
    </svg>
  `
}

const features = [
  {
    id: 'risk',
    label: 'Risk Assessment',
    shortLabel: 'Risk',
    description: 'Evaluate startup risk factors and receive actionable insights.',
    icon: ['fas', 'briefcase'],
    iconBg: 'bg-gradient-to-r from-red-500 to-red-600',
    gradientClass: 'from-red-500 to-pink-500',
    characterSvg: RiskCharacter,
    usage: '2.1k',
    rating: '4.8'
  },
  {
    id: 'reputation',
    label: 'Reputation Analysis',
    shortLabel: 'Reputation',
    description: 'Analyze brand reputation and market perception.',
    icon: ['fas', 'comment-dots'],
    iconBg: 'bg-gradient-to-r from-blue-500 to-blue-600',
    gradientClass: 'from-blue-500 to-cyan-500',
    characterSvg: ReputationCharacter,
    usage: '1.8k',
    rating: '4.7'
  },
  {
    id: 'investors',
    label: 'Investor Match',
    shortLabel: 'Investors',
    description: 'Find investors aligned with your startup goals.',
    icon: ['fas', 'dollar-sign'],
    iconBg: 'bg-gradient-to-r from-green-500 to-green-600',
    gradientClass: 'from-green-500 to-emerald-500',
    characterSvg: InvestorCharacter,
    usage: '3.2k',
    rating: '4.9'
  },
  {
    id: 'pitch',
    label: 'Pitch Feedback',
    shortLabel: 'Pitch',
    description: 'Upload pitch deck and receive AI-generated feedback.',
    icon: ['fas', 'file-alt'],
    iconBg: 'bg-gradient-to-r from-purple-500 to-purple-600',
    gradientClass: 'from-purple-500 to-pink-500',
    characterSvg: PitchCharacter,
    usage: '2.7k',
    rating: '4.6'
  },
  {
    id: 'competitor',
    label: 'Competitor Radar',
    shortLabel: 'Competitors',
    description: 'Identify and monitor competitors in real-time.',
    icon: ['fas', 'bullseye'],
    iconBg: 'bg-gradient-to-r from-orange-500 to-orange-600',
    gradientClass: 'from-orange-500 to-red-500',
    characterSvg: CompetitorCharacter,
    usage: '1.9k',
    rating: '4.5'
  },
  {
    id: 'traction',
    label: 'Traction Estimator',
    shortLabel: 'Traction',
    description: 'Forecast product traction and growth trends.',
    icon: ['fas', 'chart-line'],
    iconBg: 'bg-gradient-to-r from-indigo-500 to-indigo-600',
    gradientClass: 'from-indigo-500 to-blue-500',
    characterSvg: TractionCharacter,
    usage: '2.4k',
    rating: '4.8'
  },
  {
    id: 'legal',
    label: 'Legal Advice',
    shortLabel: 'Legal',
    description: 'Get personalized legal assistance for startups.',
    icon: ['fas', 'gavel'],
    iconBg: 'bg-gradient-to-r from-gray-600 to-gray-700',
    gradientClass: 'from-gray-500 to-slate-600',
    characterSvg: LegalCharacter,
    usage: '1.5k',
    rating: '4.7'
  },
  {
    id: 'exit',
    label: 'Exit Strategy',
    shortLabel: 'Exit',
    description: 'Plan business exit strategy with smart tools.',
    icon: ['fas', 'door-open'],
    iconBg: 'bg-gradient-to-r from-teal-500 to-teal-600',
    gradientClass: 'from-teal-500 to-cyan-500',
    characterSvg: ExitCharacter,
    usage: '980',
    rating: '4.9'
  },
  {
    id: 'buzz',
    label: 'Buzz Builder',
    shortLabel: 'Marketing',
    description: 'Generate social media buzz with automated tools.',
    icon: ['fas', 'bullhorn'],
    iconBg: 'bg-gradient-to-r from-pink-500 to-pink-600',
    gradientClass: 'from-pink-500 to-rose-500',
    characterSvg: BuzzCharacter,
    usage: '2.8k',
    rating: '4.6'
  },
  {
    id: 'talent',
    label: 'Talent Navigator',
    shortLabel: 'Talent',
    description: 'Find the right talent with AI-powered matching.',
    icon: ['fas', 'users'],
    iconBg: 'bg-gradient-to-r from-yellow-500 to-yellow-600',
    gradientClass: 'from-yellow-500 to-orange-500',
    characterSvg: TalentCharacter,
    usage: '2.3k',
    rating: '4.7'
  },
];
</script>

<style scoped>
.animate-fade-in {
  animation: fadeInUp 0.8s ease-out;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float 8s ease-in-out infinite 2s;
}

.animate-float-slow {
  animation: float 10s ease-in-out infinite 4s;
}

.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(60px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Google Pixel 7 specific optimizations (412px) */
@media (max-width: 413px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .group {
    padding: 1rem;
  }
  
  /* Ensure full width usage */
  .w-full {
    width: 100% !important;
  }
}

/* Tablet optimizations */
@media (min-width: 414px) and (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop optimizations */
@media (min-width: 769px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Force full width on mobile when sidebar is closed */
@media (max-width: 1023px) {
  .dashboard-container {
    width: 100vw !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
  }
}
</style>
