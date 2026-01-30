import { ref, reactive, nextTick } from 'vue';

export function useChat() {
  const messages = ref([]);
  const isProcessing = ref(false);
  const currentThreadId = ref("session1");

  const fetchHistory = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/history/${currentThreadId.value}`);
      const json = await res.json();
      if (json.code === 200) {
        messages.value = json.data.map(msg => ({
          ...msg,
          steps: msg.steps || [],
          isThinkingExpanded: false,
          isThinkingCompleted: true
        }));
      }
    } catch (e) {
      console.error("[Architecture] 历史记录获取失败:", e);
    }
  };


  const sendMessage = async (content, onChunkReceived) => {
    if (!content.trim() || isProcessing.value) return;

    const userText = content;
    // 1. 推送用户消息
    messages.value.push({ role: 'user', content: userText });
    if (onChunkReceived) await onChunkReceived();

    // 2. 创建高度响应式的 AI 消息对象
    const aiMsg = reactive({
      role: 'ai',
      content: '',
      steps: [],
      isThinkingExpanded: false,
      isThinkingCompleted: false
    });

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
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine || !trimmedLine.startsWith('data: ')) continue;

          const dataStr = trimmedLine.replace('data: ', '');
          if (dataStr === '[DONE]') {
            aiMsg.isThinkingCompleted = true;
            break;
          }

          try {
            const data = JSON.parse(dataStr);

            // 情况 A: 工具开始调用 (思考过程)
            if (data.type === 'tool_start') {
              // 使用数组展开运算符触发 Vue 的响应式更新
              aiMsg.steps = [...aiMsg.steps, {
                tool: data.tool,
                args: data.args,
                result: null
              }];
              // 自动展开思考过程，提升用户体验
              aiMsg.isThinkingExpanded = true;
            }
            // 情况 B: 工具返回结果
            else if (data.type === 'tool_result') {
              const stepIndex = aiMsg.steps.map(s => s.tool).lastIndexOf(data.tool);
              if (stepIndex !== -1) {
                // 精确更新对应步骤的结果
                aiMsg.steps[stepIndex].result = data.output;
              }
            }
            // 情况 C: 最终回答内容
            else if (data.type === 'answer') {
              aiMsg.content += data.content;
              // 只要开始生成回答，通常意味着思考告一段落
              if (!aiMsg.isThinkingCompleted) aiMsg.isThinkingCompleted = true;
            }

            // 触发 UI 滚动回调
            if (onChunkReceived) await nextTick(onChunkReceived);

          } catch (e) {
            console.warn('[Architecture] 流解析跳过坏帧:', e);
          }
        }
      }
    } catch (error) {
      console.error("[Architecture] 严重网络错误:", error);
      aiMsg.content += "\n\n> ⚠️ **系统提示**: 网络连接中断，请检查后端服务。";
    } finally {
      aiMsg.isThinkingCompleted = true;
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