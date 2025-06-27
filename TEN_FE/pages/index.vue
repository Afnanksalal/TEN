<template>
  <div class="min-h-screen bg-gradient-to-br from-white via-gray-50 to-green-50/20 text-gray-800 overflow-hidden">
    <!-- Header -->
    <header class="container mx-auto flex justify-between items-center py-6 px-4 sm:px-6">
      <NuxtLink to="/" class="flex items-center space-x-3">
        <img :src="dadqLogo" alt="TEN Logo" class="w-12 h-12" />
        <span class="text-4xl font-extrabold tracking-tight">T<span class="text-green-600">E</span>N</span>
      </NuxtLink>

      <!-- Glass Nav -->
      <nav
        class="hidden md:flex items-center space-x-8 px-8 py-3 rounded-full backdrop-blur-md bg-white/30 border border-white/40 shadow-lg text-lg font-semibold text-gray-800"
      >
        <a href="#risks" class="hover:text-green-600 transition duration-200">Risk</a>
        <a href="#reputation" class="hover:text-green-600 transition duration-200">Reputation</a>
        <a href="#match" class="hover:text-green-600 transition duration-200">Match</a>
        <a href="#about" class="hover:text-green-600 transition duration-200">About</a>
      </nav>

      <NuxtLink
        to="/dashboard"
        class="bg-green-600 text-white px-5 py-2 rounded-xl shadow-md hover:bg-green-700 transition"
      >
        Dashboard
      </NuxtLink>
    </header>

    <!-- Hero Section -->
    <section class="container mx-auto flex flex-col lg:flex-row items-center gap-12 px-4 sm:px-6 py-12">
      <!-- Text -->
      <div class="flex-1 space-y-6 animate-fade-in-up">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight">
          Empower Your <span class="bg-gradient-to-r from-green-500 to-blue-600 bg-clip-text text-transparent">Startup Journey</span><br />with Smart Insights
        </h1>
        <p class="text-lg text-gray-600">
          TEN provides first‑time entrepreneurs with powerful AI‑powered risk assessment, real‑time
          reputation monitoring, and smart investor matching — to help launch and scale with confidence.
        </p>
        <NuxtLink
          to="/dashboard"
          class="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transition"
        >
          Start Your Journey →
        </NuxtLink>
      </div>

      <!-- GIF -->
      <div class="flex-1 relative animate-fade-in-right">
        <img :src="bgGif" alt="Demo GIF" class="w-full rounded-3xl shadow-2xl border border-white/20" />
        <div class="absolute top-4 right-4 bg-white/90 rounded-xl p-3 shadow-lg animate-float">
          <span class="text-sm font-semibold text-green-600">Live Analysis</span>
        </div>
      </div>
    </section>

    <!-- Sections -->
    <section id="risks" class="py-12 md:py-20 bg-gray-50">
      <div class="container mx-auto px-4 sm:px-6 space-y-8">
        <h2 class="text-3xl font-bold text-center">1. Smart Risk Assessment</h2>
        <p class="text-center text-gray-600 max-w-3xl mx-auto">
          A clean, actionable risk‑profiling tool that helps first‑time entrepreneurs discover and prioritize business, market, and financial risks to make informed, resource‑efficient decisions.
        </p>
        <div
          class="max-w-4xl mx-auto bg-white/80 backdrop-blur-sm border border-gray-200 p-6 rounded-2xl shadow-lg hover:shadow-xl transition"
        >
          <ul class="list-disc ml-5 space-y-1 text-gray-700">
            <li>🔍 Identify viability, market, and financial risks early.</li>
            <li>📝 Actionable suggestions to mitigate top-priority threats.</li>
            <li>⚡ Rapid iterations & feedback for startup strategy.</li>
          </ul>
        </div>
      </div>
    </section>

    <section id="reputation" class="py-12 md:py-20">
      <div class="container mx-auto px-4 sm:px-6 space-y-8">
        <h2 class="text-3xl font-bold text-center">2. AI-Powered Reputation Analysis</h2>
        <p class="text-center text-gray-600 max-w-3xl mx-auto">
          Track and manage your startup’s online reputation in real time. Our AI scans social media, news, and public discussions to surface sentiment insights so you can act fast and stay informed.
        </p>
        <div
          class="max-w-4xl mx-auto bg-white/80 backdrop-blur-sm border border-gray-200 p-6 rounded-2xl shadow-lg hover:shadow-xl transition"
        >
          <ul class="list-disc ml-5 space-y-1 text-gray-700">
            <li>⚡ Instant reputation scores within seconds.</li>
            <li>🔑 Highlights trending sentiment and themes.</li>
            <li>📈 Proactive management of brand perception.</li>
          </ul>
        </div>
      </div>
    </section>

    <section id="match" class="py-12 md:py-20 bg-gray-50">
      <div class="container mx-auto px-4 sm:px-6 space-y-8">
        <h2 class="text-3xl font-bold text-center">3. Smart Startup–Investor Matching</h2>
        <p class="text-center text-gray-600 max-w-3xl mx-auto">
          Bridge the gap between founders and investors. Our platform matches based on risk appetite, industry focus, and investment criteria—empowering both sides for chance of success.
        </p>
        <div
          class="max-w-4xl mx-auto bg-white/80 backdrop-blur-sm border border-gray-200 p-6 rounded-2xl shadow-lg hover:shadow-xl transition"
        >
          <ul class="list-disc ml-5 space-y-1 text-gray-700">
            <li>🤝 Match algorithm based on risk profile and preference.</li>
            <li>💡 Pitch feedback loop from interested investors.</li>
            <li>🔍 Transparency via compatibility scoring.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer id="about" class="bg-gray-900 py-12 text-white">
      <div class="container mx-auto px-4 sm:px-6 space-y-4">
        <h3 class="text-xl font-semibold">About TEN</h3>
        <p class="text-gray-400 max-w-2xl">
          TEN empowers first-time entrepreneurs with intelligent tools that de-risk early-stage ventures. Our mission is to elevate the startup ecosystem by providing accessible, data-driven insights, enabling founders to build with confidence.
        </p>
        <p class="text-gray-400 text-sm">&copy; 2025 TEN. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useHead } from '#imports'
import dadqLogo from '@/assets/images/dadq.png'
import bgGif from '@/assets/images/bgvideo.gif'

useHead({
  title: 'TEN – AI Startup Intelligence Platform'
})
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out;
}
.animate-fade-in-right {
  animation: fadeInRight 0.8s ease-out;
}
.animate-float {
  animation: float 4s ease-in-out infinite;
}
</style>
