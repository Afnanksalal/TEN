<!-- components/LandingPage.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <!-- Header -->
      <header class="flex justify-between items-center px-8 py-6">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-yellow-400 rounded-lg flex items-center justify-center">
            <span class="text-black font-bold text-sm">SE</span>
          </div>
          <span class="text-xl font-bold">TEN</span>
        </div>
        <nav class="hidden md:flex space-x-8">
          <a href="#" class="text-gray-300 hover:text-white transition-colors">Services</a>
          <a href="#" class="text-gray-300 hover:text-white transition-colors">Pricing</a>
          <a href="#" class="text-gray-300 hover:text-white transition-colors">About</a>
          <a href="#" class="text-gray-300 hover:text-white transition-colors">Insights</a>
          <a href="#" class="text-gray-300 hover:text-white transition-colors">Contact</a>
        </nav>
        <div class="flex items-center space-x-4">
          <button class="text-gray-300 hover:text-white transition-colors">Login</button>
          <button 
            @click="$emit('get-started')"
            class="bg-yellow-400 text-black px-6 py-2 rounded-lg font-medium hover:bg-yellow-300 transition-colors"
          >
            Get Started →
          </button>
        </div>
      </header>
  
      <!-- Hero Section -->
      <main class="container mx-auto px-8 py-20">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl md:text-6xl font-bold mb-8 leading-tight">
            All the must-haves of a<br>
            professional <span class="bg-yellow-400 text-black px-3 py-1 rounded-lg">startup platform.</span>
          </h1>
          
          <!-- Feature Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
            <!-- Risk Assessment Card -->
            <div class="bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm border border-gray-700 hover:border-gray-600 transition-all group">
              <div class="flex items-center justify-between mb-4">
                <div class="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center group-hover:bg-yellow-400 transition-colors">
                  <span class="text-lg">📊</span>
                </div>
                <div class="w-6 h-6 bg-gray-600 rounded-full flex items-center justify-center">
                  <span class="text-xs">→</span>
                </div>
              </div>
              <h3 class="text-xl font-semibold mb-2">Risk Assessment</h3>
              <p class="text-gray-400 text-sm leading-relaxed">
                Analyze market risks in real-time with our AI-powered risk assessment tools.
              </p>
            </div>
  
            <!-- Reputation Analysis Card -->
            <div class="bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm border border-gray-700 hover:border-gray-600 transition-all group">
              <div class="flex items-center justify-between mb-4">
                <div class="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center group-hover:bg-yellow-400 transition-colors">
                  <span class="text-lg">🌟</span>
                </div>
                <div class="w-6 h-6 bg-gray-600 rounded-full flex items-center justify-center">
                  <span class="text-xs">✓</span>
                </div>
              </div>
              <h3 class="text-xl font-semibold mb-2">Reputation Analysis</h3>
              <p class="text-gray-400 text-sm leading-relaxed">
                Monitor your startup's reputation across multiple channels and platforms.
              </p>
            </div>
  
            <!-- Investor Matching Card -->
            <div class="bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm border border-gray-700 hover:border-gray-600 transition-all group">
              <div class="flex items-center justify-between mb-4">
                <div class="w-10 h-10 bg-yellow-400 rounded-lg flex items-center justify-center">
                  <span class="text-lg text-black">🤝</span>
                </div>
                <div class="flex space-x-1">
                  <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div class="w-3 h-3 bg-gray-600 rounded-full"></div>
                </div>
              </div>
              <h3 class="text-xl font-semibold mb-2">Investor Matching</h3>
              <p class="text-gray-400 text-sm leading-relaxed">
                Connect with the right investors for your startup's growth stage.
              </p>
            </div>
  
            <!-- Pitch Feedback Card -->
            <div class="bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm border border-gray-700 hover:border-gray-600 transition-all group">
              <div class="flex items-center justify-between mb-4">
                <div class="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center group-hover:bg-yellow-400 transition-colors">
                  <span class="text-lg">🎤</span>
                </div>
                <div class="w-6 h-6 bg-gray-600 rounded-full flex items-center justify-center">
                  <span class="text-xs">⭐</span>
                </div>
              </div>
              <h3 class="text-xl font-semibold mb-2">Pitch Feedback</h3>
              <p class="text-gray-400 text-sm leading-relaxed">
                Get AI-powered feedback on your pitch deck and presentation.
              </p>
            </div>
          </div>
  
          <!-- CTA Section -->
          <div class="mt-20">
            <button 
              @click="$emit('get-started')"
              class="bg-yellow-400 text-black px-8 py-4 rounded-lg font-semibold text-lg hover:bg-yellow-300 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              Get Started with TEN  →
            </button>
            <p class="text-gray-400 mt-4">No credit card required • Free 14-day trial</p>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LandingPage',
    emits: ['get-started']
  }
  </script>