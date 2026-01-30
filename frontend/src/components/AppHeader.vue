<template>
  <header class="h-16 flex-none flex items-center justify-between px-6 border-b border-white/5 bg-[#0a0a0a]/90 backdrop-blur-md z-50">
    <div class="flex items-center gap-4">
      <button 
        @click="$emit('toggleSidebar')" 
        class="p-2 -ml-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white transition-colors"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <span class="font-medium text-white tracking-wide">DeepSeek Assistant</span>
    </div>
  </header>
</template>

<script setup>
defineEmits(['toggleSidebar']);
</script>