
<script setup lang="ts">
import { defineProps, nextTick, onMounted, ref, watch } from 'vue';
import { cohereTheme } from '../styles/theme';

interface Message {
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
}

interface Props {
  messages: Message[]
}

const props = defineProps<Props>()
const messagesContainer = ref<HTMLDivElement | null>(null)

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})

watch(() => props.messages, () => {
  nextTick(scrollToBottom)
}, { deep: true })

const shouldShowTimestamp = (message: Message, previousMessage: Message | undefined) => {
  if (!previousMessage) {
    return true
  }

  const timeDifference = message.timestamp.getTime() - previousMessage.timestamp.getTime()
  return timeDifference > 1000 * 60 * 5
}

const formatMessageDate = (date: Date) => {
  return date.toLocaleString('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  })
}
</script>

<template>
  <div class="chat-window">
    <div ref="messagesContainer" class="messages-container">
      <div 
        v-for="(message, index) in messages" 
        :key="message.timestamp.getTime()"
        class="message-group"
      >
        <!-- Timestamp divider -->
        <div 
          v-if="index === 0 || shouldShowTimestamp(message, messages[index - 1])"
          class="timestamp-divider"
        >
          <span>{{ formatMessageDate(message.timestamp) }}</span>
        </div>

        <!-- Message -->
        <div 
          class="message-wrapper"
          :class="[message.role]"
        >
          <!-- Role indicator -->
          <div class="role-indicator">
            <div class="avatar" :class="[message.role]">
              {{ message.role === 'assistant' ? 'C' : 'Y' }}
            </div>
          </div>

          <!-- Message content -->
          <div class="message-content">
            <MessageContent :content="message.content" :role="message.role" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: v-bind('cohereTheme.colors.background.DEFAULT');
  border-radius: v-bind('cohereTheme.radii.lg');
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: v-bind('cohereTheme.spacing.lg');
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.md');
}

.message-group {
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.sm');
}

.timestamp-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: v-bind('cohereTheme.spacing['4xl']') 0;
}

.timestamp-divider span {
  font-size: 0.875rem;
  color: v-bind('cohereTheme.colors.text.secondary');
  background-color: v-bind('cohereTheme.colors.background.DEFAULT');
  padding: v-bind('cohereTheme.spacing.md') v-bind('cohereTheme.spacing['3xl']');
  border-radius: v-bind('cohereTheme.radii.full');
  border: 1px solid v-bind('cohereTheme.colors.border.light');
}

.message-wrapper {
  display: flex;
  gap: v-bind('cohereTheme.spacing['3xl']');
  max-width: 80%;
}

.message-wrapper.user {
  margin-left: auto;
}

.role-indicator {
  flex-shrink: 0;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: v-bind('cohereTheme.radii.full');
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.875rem;
}

.avatar.assistant {
  background-color: v-bind('cohereTheme.colors.primary.DEFAULT');
  color: v-bind('cohereTheme.colors.text.inverted');
}

.avatar.user {
  background-color: v-bind('cohereTheme.colors.background.secondary');
  color: v-bind('cohereTheme.colors.text.primary');
}

.message-content {
  background-color: v-bind('cohereTheme.colors.surface.raised');
  padding: v-bind('cohereTheme.spacing.lg');
  border-radius: v-bind('cohereTheme.radii.lg');
  border: 1px solid v-bind('cohereTheme.colors.border.DEFAULT');
  overflow-wrap: break-word;
}

.user .message-content {
  background-color: v-bind('cohereTheme.colors.primary.DEFAULT');
  color: v-bind('cohereTheme.colors.text.inverted');
  border: none;
}
</style>
