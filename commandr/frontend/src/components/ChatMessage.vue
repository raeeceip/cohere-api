
<script setup lang="ts">
import { Bot, User } from 'lucide-vue-next';
import { defineProps } from 'vue';

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}
const props = defineProps<{
  message: Message
}>()

const IconComponent = props.message.role === 'user' ? User : Bot
</script>
<template>
  <div class="message" :class="[message.role]">
    <div class="avatar" :class="[message.role]">
      <div class="avatar-content">
        {{ message.role === 'assistant' ? 'C' : 'Y' }}
      </div>
    </div>
    <div class="content">
      <div class="bubble">
        {{ message.content }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  gap: 12px;
  margin: 8px 0;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.avatar-content {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.875rem;
}

.assistant .avatar-content {
  background-color: var(--primary);
  color: rgb(178, 74, 182);
}

.user .avatar-content {
  background-color: var(--background-secondary);
  color: #404040;
}

.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
  white-space: pre-wrap;
}

.assistant .bubble {
  background-color: var(--background-secondary);
  color: var(--text);
  border: 1px solid var(--border);
}

.user .bubble {
  background-color:  rgb(178, 74, 182);
  color:  #404040;
}

/* Dark theme specific styles */
.dark .assistant .bubble {
  background-color: #2D2D2D;
  border-color: #404040;
}

.dark .user .avatar-content {
  background-color: #2D2D2D;
  color: #FFFFFF;
}
</style>