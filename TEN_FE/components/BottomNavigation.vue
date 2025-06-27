<!-- components/BottomNavigation.vue -->
<template>
  <footer class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
    <nav class="flex justify-around items-center h-20 px-2">
      <button
        v-for="item in navigationItems"
        :key="item.id"
        :class="[
          'flex flex-col items-center justify-center text-xs w-24 h-16 rounded-xl transition-all duration-300 transform',
          activeTab === item.id
            ? 'bg-green-600 text-white shadow-lg'
            : 'text-gray-500 hover:bg-green-100 hover:scale-105'
        ]"
      >
        <span class="text-lg mb-1">
          <component :is="item.icon" class="w-6 h-6" />
        </span>
        <span class="font-semibold text-sm">
          {{ item.label.split(' ')[0] }}
        </span>
      </button>
    </nav>
  </footer>
</template>

<script setup>
import IconHome from '@/assets/icons/IconHome.vue'
import IconRisk from '@/assets/icons/IconRisk.vue'
import IconReputation from '@/assets/icons/IconReputation.vue'
import IconInvestors from '@/assets/icons/IconInvestors.vue'
import IconPitch from '@/assets/icons/IconPitch.vue'

// Your component logic
</script>