<script setup lang="ts">
  import { cohereTheme } from '@/styles/theme';
import { defineProps, nextTick, onMounted, ref, watch } from 'vue';
import { Message } from '../composables/useMessages';
  
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
  
  // Watch for new messages and scroll to bottom
  watch(() => props.messages, () => {
    nextTick(() => {
      scrollToBottom()
    })
  }, { deep: true })
</script>
  
  <template>
    <div ref="messagesContainer" class="chat-window">
      <div class="messages-container">
        <div 
          v-for="(message, index) in messages" 
          :key="message.timestamp.getTime()"
          class="message-wrapper"
          :class="{ 'user-message': message.role === 'user' }"
        >
          <!-- Timestamp for first message or when more than 5 minutes have passed -->
          <div 
            v-if="index === 0 || 
            (messages[index - 1].timestamp.getTime() - message.timestamp.getTime()) > 300000"
            class="timestamp"
          >
            {{ message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
          </div>
          
          <div class="message" :class="message.role">
            <div class="message-content">
              {{ message.content }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .chat-window {
    height: calc(100vh - 180px);
    overflow-y: auto;
    padding: v-bind('cohereTheme.spacing.md');
    background-color: v-bind('cohereTheme.colors.background');
    border: 1px solid v-bind('cohereTheme.colors.border');
    border-radius: 8px;
  }
  
  .messages-container {
    display: flex;
    flex-direction: column;
    gap: v-bind('cohereTheme.spacing.md');
  }
  
  .message-wrapper {
    display: flex;
    flex-direction: column;
    gap: v-bind('cohereTheme.spacing.xs');
    max-width: 80%;
  }
  
  .message-wrapper.user-message {
    align-self: flex-end;
  }
  
  .timestamp {
    font-size: 0.8rem;
    color: v-bind('cohereTheme.colors.text.secondary');
    text-align: center;
    margin: v-bind('cohereTheme.spacing.sm') 0;
  }
  
  .message {
    padding: v-bind('cohereTheme.spacing.md');
    border-radius: 12px;
    position: relative;
  }
  
  .message.user {
    background-color: v-bind('cohereTheme.colors.primary');
    color: v-bind('cohereTheme.colors.text.primary');
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  }
  
  .message.assistant {
    background-color: v-bind('cohereTheme.colors.surface');
    color: v-bind('cohereTheme.colors.text.primary');
    border-bottom-left-radius: 4px;
  }
  
  .message-content {
    white-space: pre-wrap;
    word-break: break-word;
  }
  </style>
