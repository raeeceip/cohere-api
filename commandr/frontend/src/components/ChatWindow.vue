// 1. Update ChatWindow.vue
<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from 'vue'
import { Message } from '../types/message'
import ChatMessage from './ChatMessage.vue'

interface Props {
  messages: Message[]
  isLoading?: boolean
}

const props = defineProps<Props>()
const messagesContainer = ref<HTMLDivElement | null>(null)

// Ensure messages container exists
onMounted(() => {
  if (!messagesContainer.value) {
    console.error('Messages container not found')
    return
  }
  scrollToBottom(false)
})

// Scroll handling
const scrollToBottom = (smooth = true) => {
  if (!messagesContainer.value) return
  
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
      })
    }
  })
}

// Watch for new messages
watch(() => props.messages, (newMessages, oldMessages) => {
  if (!oldMessages || newMessages.length > oldMessages.length) {
    nextTick(() => scrollToBottom())
  }
}, { deep: true })

const formatTime = (date: Date) => {
  return new Intl.DateTimeFormat('en', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }).format(date)
}

// Group messages by time
const shouldShowTimestamp = (index: number) => {
  if (index === 0) return true
  
  const currentMsg = props.messages[index]
  const prevMsg = props.messages[index - 1]
  
  const timeDiff = currentMsg.timestamp.getTime() - prevMsg.timestamp.getTime()
  return timeDiff > 1000 * 60 * 5 // Show timestamp if messages are 5+ minutes apart
}
</script>

<template>
  <div class="chat-window">
    <div 
      ref="messagesContainer" 
      class="messages-container"
    >
      <!-- Empty state -->
      <div v-if="!messages.length" class="empty-state">
        <p>Start a conversation...</p>
      </div>

      <!-- Messages -->
      <template v-else>
        <div 
          v-for="(message, index) in messages" 
          :key="message.timestamp.getTime()"
          class="message-group"
        >
          <!-- Time divider -->
          <div 
            v-if="shouldShowTimestamp(index)" 
            class="time-divider"
          >
            <span>{{ formatTime(message.timestamp) }}</span>
          </div>

          <!-- Message -->
          <ChatMessage :message="message" />
        </div>
      </template>

      <!-- Loading state -->
      <div v-if="isLoading" class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--chat-bg);
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  scroll-behavior: smooth;
}

.message-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.time-divider {
  align-self: center;
  margin: 1rem 0;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.time-divider span {
  padding: 0.25rem 0.75rem;
  background: var(--divider-bg);
  border-radius: 999px;
  font-weight: 500;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.5rem;
  align-self: flex-start;
}

.typing-indicator span {
  width: 0.5rem;
  height: 0.5rem;
  background: var(--primary);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

:root {
  --chat-bg: #FFFFFF;
  --divider-bg: #F3F4F6;
  --primary: #6B4FBB;
  --text-secondary: #6B7280;
}

[data-theme="dark"] {
  --chat-bg: #1A1A1A;
  --divider-bg: #2D2D2D;
  --text-secondary: #A0A0A0;
}
</style>

