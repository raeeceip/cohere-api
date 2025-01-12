
<script setup lang="ts">
import { cohereTheme } from '@/styles/theme';
import { defineEmits, ref } from 'vue';

const emit = defineEmits<{
  (e: 'send', message: string): void
}>()

const message = ref('')
const textareaRef = ref<HTMLTextAreaElement | null>(null)

const handleSubmit = () => {
  if (message.value.trim()) {
    emit('send', message.value)
    message.value = ''
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}

const adjustTextareaHeight = (e: Event) => {
  const textarea = e.target as HTMLTextAreaElement
  textarea.style.height = 'auto'
  textarea.style.height = `${textarea.scrollHeight}px`
}
</script>

<template>
  <div class="chat-input">
    <textarea
      ref="textareaRef"
      v-model="message"
      @keydown="handleKeydown"
      @input="adjustTextareaHeight"
      placeholder="Type your message..."
      rows="1"
    />
    <button 
      @click="handleSubmit"
      :disabled="!message.trim()"
      class="send-button"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" y1="2" x2="11" y2="13"></line>
        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.chat-input {
  position: relative;
  padding: v-bind('cohereTheme.spacing.md');
  background-color: v-bind('cohereTheme.colors.surface');
  border-radius: 8px;
  margin-top: v-bind('cohereTheme.spacing.md');
  display: flex;
  gap: v-bind('cohereTheme.spacing.md');
  align-items: flex-end;
}

textarea {
  flex-grow: 1;
  background-color: transparent;
  border: none;
  resize: none;
  color: v-bind('cohereTheme.colors.text.primary');
  font-size: 1rem;
  line-height: 1.5;
  max-height: 150px;
  padding: v-bind('cohereTheme.spacing.sm');
  outline: none;
}

textarea::placeholder {
  color: v-bind('cohereTheme.colors.text.secondary');
}

.send-button {
  background-color: v-bind('cohereTheme.colors.primary');
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: v-bind('cohereTheme.colors.text.primary');
  padding: v-bind('cohereTheme.spacing.xs');
}

.send-button:hover {
  background-color: v-bind('cohereTheme.colors.accent');
}

.send-button:disabled {
  background-color: v-bind('cohereTheme.colors.border');
  cursor: not-allowed;
  opacity: 0.7;
}
</style>

