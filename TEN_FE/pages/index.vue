<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-green-50/30 to-blue-50/20 text-gray-800 relative overflow-x-hidden">
    <!-- Background Decorative Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 -left-12 w-72 h-72 bg-green-400/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute -top-12 -right-12 w-72 h-72 bg-blue-400/10 rounded-full blur-3xl animate-float-delayed"></div>
      <div class="absolute bottom-0 right-20 w-64 h-64 bg-purple-400/10 rounded-full blur-3xl animate-float-slow"></div>
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-50 backdrop-blur-lg bg-white/80 border-b border-white/60 shadow-sm">
      <div class="container mx-auto flex justify-between items-center py-4 px-4 sm:px-6">
        <NuxtLink to="/" class="flex items-center space-x-3">
          <img :src="dadqLogo" alt="TEN Logo" class="w-10 h-10" />
          <span class="text-3xl font-extrabold tracking-tight">T<span class="text-green-600">E</span>N</span>
        </NuxtLink>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center space-x-8 text-md font-medium text-gray-700">
          <a href="#features" class="hover:text-green-600 transition duration-200">Features</a>
          <a href="#testimonials" class="hover:text-green-600 transition duration-200">Testimonials</a>
          <a href="#about" class="hover:text-green-600 transition duration-200">About</a>
        </nav>

        <NuxtLink
          to="/dashboard"
          class="bg-green-600 text-white px-5 py-2.5 rounded-xl font-semibold shadow-md hover:bg-green-700 transition duration-300 transform hover:scale-105"
        >
          Go to Dashboard
        </NuxtLink>
      </div>
    </header>

    <main class="relative z-10">
      <!-- Hero Section -->
      <section class="container mx-auto flex flex-col lg:flex-row items-center gap-12 px-4 sm:px-6 py-16 md:py-24 text-center lg:text-left">
        <!-- Text Content -->
        <div class="flex-1 space-y-6 animate-fade-in-up">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold leading-tight tracking-tighter">
            Empower Your <span class="bg-gradient-to-r from-green-500 to-blue-500 bg-clip-text text-transparent">Startup Journey</span><br />with AI Insights
          </h1>
          <p class="text-lg text-gray-600 max-w-xl mx-auto lg:mx-0">
            TEN provides first‑time entrepreneurs with powerful AI‑powered risk assessment, real‑time
            reputation monitoring, and smart investor matching — to help launch and scale with confidence.
          </p>
          <div class="flex justify-center lg:justify-start">
            <NuxtLink
              to="/dashboard"
              class="inline-flex items-center space-x-2 bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105"
            >
              <span>Get Started Free</span>
              <font-awesome-icon icon="arrow-right" class="w-4 h-4" />
            </NuxtLink>
          </div>
        </div>

        <!-- GIF Visual -->
        <div class="flex-1 relative animate-fade-in-right">
          <div class="relative w-full rounded-3xl shadow-2xl p-2 bg-gradient-to-br from-green-200 to-blue-200">
            <img :src="bgGif" alt="Demo GIF" class="w-full rounded-2xl border-4 border-white" />
          </div>
          <div class="absolute -top-4 -left-4 bg-white/90 backdrop-blur-sm rounded-xl p-3 shadow-lg animate-float">
            <span class="text-sm font-semibold text-green-600 flex items-center"><font-awesome-icon icon="star" class="w-4 h-4 mr-2 text-yellow-400"/> Top Rated</span>
          </div>
          <div class="absolute -bottom-4 -right-4 bg-white/90 backdrop-blur-sm rounded-xl p-3 shadow-lg animate-float-delayed">
            <span class="text-sm font-semibold text-blue-600 flex items-center"><font-awesome-icon icon="users" class="w-4 h-4 mr-2"/> 1000+ Founders</span>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section id="features" class="py-20 md:py-28 bg-gray-50/50">
        <div class="container mx-auto px-4 sm:px-6 space-y-12">
          <div class="text-center max-w-3xl mx-auto">
            <h2 class="text-3xl sm:text-4xl font-extrabold">All The Tools You Need To Succeed</h2>
            <p class="mt-4 text-lg text-gray-600">
              From ideation to investment, TEN provides a comprehensive suite of AI-powered tools designed to de-risk your venture and accelerate your growth.
            </p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div
              v-for="feature in features" :key="feature.id"
              class="bg-white/70 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-white/50 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >
              <div class="flex items-center space-x-4">
                <div :class="feature.iconBg" class="w-12 h-12 rounded-xl flex items-center justify-center text-white flex-shrink-0">
                  <font-awesome-icon :icon="feature.icon" class="w-6 h-6" />
                </div>
                <h3 class="text-lg font-bold text-gray-800">{{ feature.label }}</h3>
              </div>
              <p class="mt-4 text-gray-600 text-sm leading-relaxed">
                {{ feature.description }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Testimonials Section -->
      <section id="testimonials" class="py-20 md:py-28">
        <div class="container mx-auto px-4 sm:px-6">
            <div class="text-center max-w-3xl mx-auto">
                <h2 class="text-3xl sm:text-4xl font-extrabold">Loved by Founders Worldwide</h2>
                <p class="mt-4 text-lg text-gray-600">Don't just take our word for it. Here's what entrepreneurs are saying about their journey with TEN.</p>
            </div>
            <div class="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div class="bg-white/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-white/50">
                    <p class="text-gray-700 italic">"TEN's Risk Assessment was a game-changer. It helped us spot blind spots in our business plan we never would have seen otherwise. Essential for any first-time founder."</p>
                    <div class="mt-4 flex items-center">
                        <img src="https://i.pravatar.cc/150?img=11" alt="Avatar" class="w-12 h-12 rounded-full mr-4"/>
                        <div>
                            <p class="font-bold">David Rodriguez</p>
                            <p class="text-sm text-gray-500">CEO, InnovateTech</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-white/50">
                    <p class="text-gray-700 italic">"The Investor Match tool connected us with two angel investors who were a perfect fit for our niche. We closed our pre-seed round in under a month. Incredible!"</p>
                    <div class="mt-4 flex items-center">
                        <img src="https://i.pravatar.cc/150?img=32" alt="Avatar" class="w-12 h-12 rounded-full mr-4"/>
                        <div>
                            <p class="font-bold">Sarah Chen</p>
                            <p class="text-sm text-gray-500">Founder, Healthify</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </section>
      
      <!-- Final CTA Section -->
      <section class="py-20">
        <div class="container mx-auto px-4 sm:px-6">
            <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-2xl p-10 md:p-16 text-center text-white relative overflow-hidden">
                <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-white/10 rounded-full"></div>
                <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full"></div>
                <h2 class="text-3xl sm:text-4xl font-extrabold">Ready to Build Your Future?</h2>
                <p class="mt-4 text-lg opacity-90 max-w-2xl mx-auto">Join thousands of successful founders who started their journey with TEN. Get free access to our core tools today.</p>
                <NuxtLink to="/dashboard" class="mt-8 inline-block bg-white text-green-600 px-8 py-3 rounded-xl font-bold shadow-lg hover:bg-gray-100 transition duration-300 transform hover:scale-105">
                   Get Started
                </NuxtLink>
            </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer id="about" class="bg-gray-100/70 border-t border-gray-200/80">
      <div class="container mx-auto py-8 px-4 sm:px-6 text-center text-gray-600">
        <img :src="dadqLogo" alt="TEN Logo" class="w-12 h-12 mx-auto mb-4" />
        <p class="max-w-2xl mx-auto">
          TEN empowers first-time entrepreneurs with intelligent tools that de-risk early-stage ventures. Our mission is to elevate the startup ecosystem by providing accessible, data-driven insights.
        </p>
        <p class="mt-6 text-sm text-gray-500">© {{ new Date().getFullYear() }} TEN. All rights reserved.</p>
      </div>
    </footer>

    <!-- PWA Install Prompt Component -->
    <ClientOnly>
      <PwaInstallPrompt />
    </ClientOnly>
  </div>
</template>

<script setup>
import { useHead } from '#imports'
import dadqLogo from '@/assets/images/dadq.png'
import bgGif from '@/assets/images/bgvideo.gif'
// Import the PwaInstallPrompt component
import PwaInstallPrompt from '@/components/PwaInstallPrompt.vue'

useHead({
  title: 'TEN – AI Startup Intelligence Platform'
})

// Features data, mirrored from the dashboard for consistency
const features = [
  { id: 'risk', label: 'Risk Assessment', description: 'Evaluate startup risk factors and receive actionable insights.', icon: ['fas', 'briefcase'], iconBg: 'bg-gradient-to-r from-red-500 to-red-600' },
  { id: 'reputation', label: 'Reputation Analysis', description: 'Analyze brand reputation and market perception.', icon: ['fas', 'comment-dots'], iconBg: 'bg-gradient-to-r from-blue-500 to-blue-600' },
  { id: 'investors', label: 'Investor Match', description: 'Find investors aligned with your startup goals.', icon: ['fas', 'dollar-sign'], iconBg: 'bg-gradient-to-r from-green-500 to-green-600' },
  { id: 'pitch', label: 'Pitch Feedback', description: 'Get AI-generated feedback on your pitch deck.', icon: ['fas', 'file-alt'], iconBg: 'bg-gradient-to-r from-purple-500 to-purple-600' },
  { id: 'competitor', label: 'Competitor Radar', description: 'Identify and monitor competitors in real-time.', icon: ['fas', 'bullseye'], iconBg: 'bg-gradient-to-r from-orange-500 to-orange-600' },
  { id: 'traction', label: 'Traction Estimator', description: 'Forecast product traction and growth trends.', icon: ['fas', 'chart-line'], iconBg: 'bg-gradient-to-r from-indigo-500 to-indigo-600' },
  { id: 'legal', label: 'Legal Advice', description: 'Get personalized legal assistance for startups.', icon: ['fas', 'gavel'], iconBg: 'bg-gradient-to-r from-gray-600 to-gray-700' },
  { id: 'exit', label: 'Exit Strategy', description: 'Plan your business exit strategy with smart tools.', icon: ['fas', 'door-open'], iconBg: 'bg-gradient-to-r from-teal-500 to-teal-600' },
  { id: 'buzz', label: 'Buzz Builder', description: 'Generate social media buzz with automated tools.', icon: ['fas', 'bullhorn'], iconBg: 'bg-gradient-to-r from-pink-500 to-pink-600' },
  { id: 'talent', label: 'Talent Navigator', description: 'Find the right talent with AI-powered matching.', icon: ['fas', 'users'], iconBg: 'bg-gradient-to-r from-yellow-500 to-yellow-600' },
];
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
}
@keyframes float-delayed {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}
@keyframes float-slow {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-fade-in-up { animation: fadeInUp 0.8s ease-out both; }
.animate-fade-in-right { animation: fadeInRight 0.8s ease-out both; }
.animate-float { animation: float 4s ease-in-out infinite; }
.animate-float-delayed { animation: float-delayed 5s ease-in-out infinite 1s; }
.animate-float-slow { animation: float-slow 6s ease-in-out infinite 2s; }
</style>
