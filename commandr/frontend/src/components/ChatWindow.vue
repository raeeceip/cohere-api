<script setup lang="ts">
import { Message } from '../composables/useMessages';

interface Props {
  messages: Message[];
}

defineProps<Props>()
</script>

<template>
  <div class="chat-window">
    <div v-for="message in messages" :key="message.timestamp.getTime()" class="message">
      <div :class="['message-content', message.role]">
        {{ message.content }}
      </div>
      <div class="message-timestamp">
        {{ message.timestamp.toLocaleString() }}
      </div>
    </div>
  </div>
</template>
