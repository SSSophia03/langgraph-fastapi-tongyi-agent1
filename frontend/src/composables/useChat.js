import { ref } from 'vue';

export function useChat() {
  const messages = ref([]);
  const isProcessing = ref(false);
  const currentThreadId = ref("session_pro_v1");

  // 获取历史记录
  const fetchHistory = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/history/${currentThreadId.value}`);
      const json = await res.json();
      if (json.code === 200) {
        messages.value = json.data.map(msg => ({
          ...msg,
          steps: [],
          isThinkingExpanded: false,
          isThinkingCompleted: true
        }));
      }
    } catch (e) {
      console.error("Fetch history error", e);
    }
  };

  // 发送消息核心逻辑
  // onChunkReceived: 回调函数，用于通知 UI 滚动到底部
  const sendMessage = async (content, onChunkReceived) => {
    if (!content.trim() || isProcessing.value) return;

    const userText = content;
    // 1. 添加用户消息
    messages.value.push({ role: 'user', content: userText });

    if (onChunkReceived) await onChunkReceived();

    // 2. 预占位 AI 消息
    const aiMsg = {
      role: 'ai',
      content: '',
      steps: [],
      isThinkingExpanded: false,
      isThinkingCompleted: false
    };
    messages.value.push(aiMsg);
    isProcessing.value = true;

    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: userText,
          thread_id: currentThreadId.value
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          aiMsg.isThinkingCompleted = true;
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '');
            if (dataStr === '[DONE]') {
              aiMsg.isThinkingCompleted = true;
              break;
            }

            try {
              const data = JSON.parse(dataStr);

              if (data.type === 'tool_start') {
                aiMsg.steps.push({ tool: data.tool, args: data.args, result: null });
              } else if (data.type === 'tool_result') {
                const step = aiMsg.steps.slice().reverse().find(s => s.tool === data.tool && !s.result);
                if (step) step.result = data.output;
              } else if (data.type === 'answer') {
                aiMsg.content += data.content;
                aiMsg.isThinkingCompleted = true; // 开始说话时，通常意味着思考结束
              }

              // 触发 UI 更新（滚动）
              if (onChunkReceived) await onChunkReceived();

            } catch (e) {
              console.error('JSON Parse Error', e);
            }
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

  return {
    messages,
    isProcessing,
    currentThreadId,
    fetchHistory,
    sendMessage
  };
}