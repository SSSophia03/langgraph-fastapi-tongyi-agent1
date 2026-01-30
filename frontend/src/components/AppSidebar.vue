<template>
  <aside 
    class="z-40 flex flex-col bg-black border-r border-white/10 transition-all duration-300 ease-in-out h-full absolute md:relative top-0 left-0"
    :class="isOpen ? 'w-72 translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-full opacity-0'"
  >
    <div class="w-72 flex flex-col h-full min-w-[18rem]">
      <div class="p-5">
        <h1 class="text-xl font-bold flex items-center gap-3 tracking-wider text-white mb-8">
          <div class="w-8 h-8 rounded-lg bg-white flex items-center justify-center">
            <svg class="w-5 h-5 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          AGENT<span class="text-blue-500">.X</span>
        </h1>
        <div class="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-3 pl-1">Session</div>
        <div class="p-3 bg-white/5 rounded-xl border border-white/5 text-sm font-mono text-gray-300 truncate">
          {{ sessionId }}
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  sessionId: String
});
</script>