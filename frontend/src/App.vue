<template>
  <div class="flex h-[100dvh] bg-[#0a0a0a] text-gray-100 font-sans overflow-hidden relative selection:bg-blue-500/30">
    
    <AppSidebar 
      :isOpen="isSidebarOpen" 
      :sessionId="currentThreadId" 
    />

    <main class="flex-1 flex flex-col relative min-w-0 bg-[#0a0a0a] transition-all duration-300">
      
      <AppHeader @toggleSidebar="isSidebarOpen = !isSidebarOpen" />

      <div class="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 scroll-smooth custom-scrollbar" ref="chatContainer">
        
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-[50vh] text-gray-600 space-y-6 opacity-60">
           <p class="text-sm font-mono">Ready to assist.</p>
        </div>

        <MessageItem 
          v-for="(msg, index) in messages" 
          :key="index" 
          :msg="msg" 
        />

        <div class="h-10 w-full shrink-0"></div>
      </div>

      <ChatInput 
        :isProcessing="isProcessing" 
        @send="handleSend" 
      />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import './assets/main.css';

import AppSidebar from './components/AppSidebar.vue';
import AppHeader from './components/AppHeader.vue';
import MessageItem from './components/MessageItem.vue';
import ChatInput from './components/ChatInput.vue';

import { useChat } from './composables/useChat';

const { messages, isProcessing, currentThreadId, fetchHistory, sendMessage } = useChat();

const isSidebarOpen = ref(true);
const chatContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// 处理发送
const handleSend = async (text) => {
  await scrollToBottom();
  // 传入 scrollToBottom 作为回调，实现流式输出时的自动滚动
  await sendMessage(text, scrollToBottom);
};

onMounted(() => {
  fetchHistory();
});
</script>