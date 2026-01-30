<template>
  <div class="max-w-4xl mx-auto w-full group animate-fade-in-up">
    <div v-if="msg.role === 'user'" class="flex justify-end pl-20">
      <div class="bg-white text-slate-900 px-5 py-3 rounded-2xl rounded-tr-sm shadow-xl text-sm font-bold leading-relaxed break-words">
        {{ msg.content }}
      </div>
    </div>

    <div v-else class="flex gap-4 pr-10">
      <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0 mt-1 shadow-lg shadow-blue-500/20">
        <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>

      <div class="flex-1 min-w-0 space-y-3">
        <div v-if="msg.steps && msg.steps.length > 0">
          <button 
            @click="msg.isThinkingExpanded = !msg.isThinkingExpanded" 
            class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-xs text-gray-400 hover:text-white transition-all"
          >
            <span>💭 深度思考</span>
            <svg class="w-3 h-3 transition-transform" :class="msg.isThinkingExpanded ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          
          <div v-show="msg.isThinkingExpanded" class="mt-3 ml-2 pl-4 border-l border-white/10 space-y-3">
            <div v-for="(step, sIndex) in msg.steps" :key="sIndex" class="bg-[#111] border border-white/5 rounded-lg p-3 text-[11px] font-mono">
              <div class="text-blue-400 mb-1 font-bold tracking-widest uppercase">{{ step.tool }}</div>
              <div class="text-gray-500 truncate mb-1">IN: {{ JSON.stringify(step.args) }}</div>
              <div v-if="step.result" class="text-gray-300 mt-2 pt-2 border-t border-white/5">OUT: {{ step.result }}</div>
            </div>
          </div>
        </div>

        <div v-if="msg.content" class="bg-[#151515] border border-white/5 rounded-2xl p-5 shadow-2xl">
          <div class="text-sm leading-7 text-gray-200 markdown-body break-words" v-html="renderedContent"></div>
        </div>
        <div v-else-if="!msg.isThinkingCompleted" class="flex gap-1 items-center p-2">
          <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce"></div>
          <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
          <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { renderMarkdown } from '../utils/markdown';

const props = defineProps({
  msg: { type: Object, required: true }
});

const renderedContent = computed(() => {
  return renderMarkdown(props.msg.content || '');
});
</script>