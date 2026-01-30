<template>
  <div class="flex h-[100dvh] bg-[#0a0a0a] text-gray-100 font-sans overflow-hidden relative selection:bg-blue-500/30">
    
    <aside 
      class="z-40 flex flex-col bg-black border-r border-white/10 transition-all duration-300 ease-in-out h-full absolute md:static top-0 left-0 overflow-hidden"
      :class="isSidebarOpen ? 'w-72 translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-full opacity-0 pointer-events-none'"
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
            {{ currentThreadId }}
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 flex flex-col relative min-w-0 bg-[#0a0a0a]">
      <header class="h-16 flex-none flex items-center justify-between px-6 border-b border-white/5 bg-[#0a0a0a]/90 backdrop-blur-md z-20">
        <div class="flex items-center gap-4">
          <button @click="isSidebarOpen = !isSidebarOpen" class="p-2 -ml-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
          </button>
          <span class="font-medium text-white tracking-wide">DeepSeek Assistant</span>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 scroll-smooth custom-scrollbar" ref="chatContainer">
        
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-[50vh] text-gray-600 space-y-6 opacity-60">
           <p class="text-sm font-mono">Ready to assist.</p>
        </div>

        <div v-for="(msg, index) in messages" :key="index" class="max-w-4xl mx-auto w-full group animate-fade-in-up">
          
          <div v-if="msg.role === 'user'" class="flex justify-end pl-20">
            <div class="bg-white text-slate-900 px-5 py-3 rounded-2xl rounded-tr-sm shadow-xl text-sm font-bold leading-relaxed break-words">
              {{ msg.content }}
            </div>
          </div>

          <div v-else class="flex gap-4 pr-10">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0 mt-1 shadow-lg shadow-blue-500/20">
              <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>

            <div class="flex-1 min-w-0 space-y-3">
              <div v-if="msg.steps && msg.steps.length > 0">
                <button @click="msg.isThinkingExpanded = !msg.isThinkingExpanded" class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-xs text-gray-400 hover:text-white transition-all">
                  <span>💭 深度思考</span>
                  <svg class="w-3 h-3 transition-transform" :class="msg.isThinkingExpanded ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div v-show="msg.isThinkingExpanded" class="mt-3 ml-2 pl-4 border-l border-white/10 space-y-3 animate-fade-in-down">
                  <div v-for="(step, sIndex) in msg.steps" :key="sIndex" class="bg-[#111] border border-white/5 rounded-lg p-3 text-[11px] font-mono">
                    <div class="text-blue-400 mb-1 font-bold tracking-widest uppercase">{{ step.tool }}</div>
                    <div class="text-gray-500 truncate mb-1">IN: {{ JSON.stringify(step.args) }}</div>
                    <div v-if="step.result" class="text-gray-300 mt-2 pt-2 border-t border-white/5">OUT: {{ step.result }}</div>
                  </div>
                </div>
              </div>

              <div v-if="msg.content" class="bg-[#151515] border border-white/5 rounded-2xl p-5 shadow-2xl">
                <div class="text-sm leading-7 text-gray-200 markdown-body break-words" v-html="renderMarkdown(msg.content)"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="h-48 w-full shrink-0"></div>

      </div>

      <footer 
        class="fixed bottom-0 left-0 right-0 z-50 bg-[#0a0a0a] border-t border-white/5 px-4 md:px-8 py-6 transition-all duration-300 ease-in-out"
        :class="isSidebarOpen ? 'md:left-auto md:w-[calc(100%-18rem)]' : 'md:left-0 md:w-full'"
      >
        <div class="max-w-3xl mx-auto">
          <div class="relative group">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl opacity-20 group-hover:opacity-40 transition duration-500 blur-md"></div>
            <div class="relative bg-[#0F0F0F] rounded-xl flex items-center p-1.5 border border-white/10 shadow-2xl">
              <input 
                v-model="inputMessage" 
                @keyup.enter="sendMessage"
                :disabled="isProcessing"
                type="text" 
                placeholder="Ask anything..."
                class="flex-1 bg-transparent border-none focus:ring-0 text-gray-100 placeholder-gray-600 text-sm px-4 py-3"
              >
              <button 
                @click="sendMessage"
                :disabled="!inputMessage || isProcessing"
                class="bg-white text-black hover:bg-gray-200 p-2.5 rounded-lg transition-all disabled:opacity-30 shrink-0"
              >
                <svg v-if="!isProcessing" class="w-5 h-5 transform rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
                <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" /></svg>
              </button>
            </div>
          </div>
          <p class="text-center mt-3 text-[10px] text-gray-600 font-mono tracking-tighter">POWERED BY LANGGRAPH & DEEPSEEK</p>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({ html: true, linkify: true });
const messages = ref([]);
const inputMessage = ref('');
const isProcessing = ref(false);
const chatContainer = ref(null);
const currentThreadId = ref("session_dark_final_v2");
const isSidebarOpen = ref(true);

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const renderMarkdown = (text) => md.render(text || '');

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isProcessing.value) return;

  const userText = inputMessage.value;
  messages.value.push({ role: 'user', content: userText });
  inputMessage.value = '';
  isProcessing.value = true;
  await scrollToBottom();

  const aiMsg = { 
    role: 'ai', 
    content: '', 
    steps: [],
    isThinkingExpanded: false, 
    isThinkingCompleted: false 
  };
  messages.value.push(aiMsg);

  try {
    const response = await fetch('http://localhost:8000/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input: userText, thread_id: currentThreadId.value })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) { aiMsg.isThinkingCompleted = true; break; }

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.replace('data: ', '');
          if (dataStr === '[DONE]') { aiMsg.isThinkingCompleted = true; break; }
          try {
            const data = JSON.parse(dataStr);
            if (data.type === 'tool_start') {
              aiMsg.steps.push({ tool: data.tool, args: data.args, result: null });
              await scrollToBottom();
            } else if (data.type === 'tool_result') {
              const step = aiMsg.steps.slice().reverse().find(s => s.tool === data.tool && !s.result);
              if (step) step.result = data.output;
              await scrollToBottom();
            } else if (data.type === 'answer') {
              aiMsg.content += data.content;
              aiMsg.isThinkingCompleted = true;
              await scrollToBottom();
            }
          } catch (e) { console.error(e); }
        }
      }
    }
  } catch (error) {
    aiMsg.content += "\n> Error connecting to server.";
    aiMsg.isThinkingCompleted = true;
  } finally {
    isProcessing.value = false;
  }
};

onMounted(() => { /* history logic here */ });
</script>

<style>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in-up { animation: fadeInUp 0.4s ease-out forwards; }
.markdown-body pre { background: #000 !important; border: 1px solid #333; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin: 1rem 0; }
.markdown-body code { color: #3b82f6; font-family: monospace; }
</style>