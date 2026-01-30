<template>
  <footer class="sticky bottom-0 w-full z-40 bg-[#0a0a0a] border-t border-white/5 px-4 md:px-8 py-6">
    <div class="max-w-4xl mx-auto">
      <div class="relative group">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl opacity-20 group-hover:opacity-40 transition duration-500 blur-md"></div>
        <div class="relative bg-[#0F0F0F] rounded-xl flex items-center p-1.5 border border-white/10 shadow-2xl">
          <input 
            v-model="text" 
            @keyup.enter="handleSend"
            :disabled="isProcessing"
            type="text" 
            placeholder="Ask anything..."
            class="flex-1 bg-transparent border-none focus:ring-0 text-gray-100 placeholder-gray-600 text-sm px-4 py-3"
          >
          <button 
            @click="handleSend"
            :disabled="!text || isProcessing"
            class="bg-white text-black hover:bg-gray-200 p-2.5 rounded-lg transition-all disabled:opacity-30 shrink-0"
          >
            <svg v-if="!isProcessing" class="w-5 h-5 transform rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          </button>
        </div>
      </div>
      <p class="text-center mt-3 text-[10px] text-gray-600 font-mono tracking-tighter">POWERED BY LANGGRAPH & DEEPSEEK</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  isProcessing: Boolean
});

const emit = defineEmits(['send']);
const text = ref('');

const handleSend = () => {
  if (!text.value.trim() || props.isProcessing) return;
  emit('send', text.value);
  text.value = '';
};
</script>