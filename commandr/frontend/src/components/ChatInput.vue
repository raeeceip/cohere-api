
<script setup lang="ts">
import { onMounted, ref } from 'vue';

const props = defineProps<{
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'send', message: string): void
}>()

const message = ref('')
const textareaRef = ref<HTMLTextAreaElement | null>(null)

const handleSubmit = () => {
  const trimmedMessage = message.value.trim()
  if (trimmedMessage && !props.isLoading) {
    emit('send', trimmedMessage)
    message.value = ''
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey && !props.isLoading) {
    e.preventDefault()
    handleSubmit()
  }
}

const adjustTextareaHeight = () => {
  if (!textareaRef.value) return
  
  textareaRef.value.style.height = 'auto'
  textareaRef.value.style.height = `${Math.min(textareaRef.value.scrollHeight, 200)}px`
}

onMounted(() => {
  if (textareaRef.value) {
    textareaRef.value.focus()
  }
})
</script>

<template>
  <div class="chat-input" :class="{ loading: isLoading }">
    <div class="input-container">
      <textarea
        ref="textareaRef"
        v-model="message"
        @keydown="handleKeydown"
        @input="adjustTextareaHeight"
        :placeholder="isLoading ? 'Please wait...' : 'Type your message...'"
        :disabled="isLoading"
        class="message-input"
        rows="1"
      />
      
      <button 
        @click="handleSubmit"
        :disabled="!message.trim() || isLoading"
        class="send-button"
      >
        <svg 
          v-if="!isLoading"
          viewBox="0 0 24 24" 
          fill="none" 
          class="send-icon"
        >
          <path 
            d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" 
            fill="currentColor"
          />
        </svg>
        <div v-else class="loading-spinner">
          <span></span>
        </div>
      </button>
    </div>

    <div class="input-footer">
      <span class="shortcut-hint">Press ⏎ to send</span>
      <span class="shortcut-hint">⇧ + ⏎ for new line</span>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  border-top: 1px solid var(--border-color);
  padding: 1rem;
  background: var(--input-bg);
}

.input-container {
  position: relative;
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  background: var(--input-area-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
}

.message-input {
  flex: 1;
  min-height: 24px;
  max-height: 200px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 0.9375rem;
  line-height: 1.5;
  resize: none;
  padding: 0;
}

.message-input:focus {
  outline: none;
}

.message-input::placeholder {
  color: var(--text-secondary);
}

.send-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  background: var(--primary);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-button:hover:not(:disabled) {
  background: var(--primary-dark);
}

.send-button:disabled {
  background: var(--disabled-bg);
  cursor: not-allowed;
}

.send-icon {
  width: 20px;
  height: 20px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.input-footer {
  margin-top: 0.5rem;
  padding: 0 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.shortcut-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

:root {
  --input-bg: #FFFFFF;
  --input-area-bg: #F9FAFB;
  --border-color: #E5E7EB;
  --primary: #6B4FBB;
  --primary-dark: #5A3FA3;
  --disabled-bg: #E5E7EB;
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
}

[data-theme="dark"] {
  --input-bg: #1A1A1A;
  --input-area-bg: #2D2D2D;
  --border-color: #404040;
  --disabled-bg: #404040;
  --text-primary: #F9FAFB;
  --text-secondary: #9CA3AF;
}

.loading {
  opacity: 0.7;
  pointer-events: none;
}
</style>