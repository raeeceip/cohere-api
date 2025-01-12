<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ChatInput from './components/ChatInput.vue'
import ChatWindow from './components/ChatWindow.vue'
import Sidebar from './components/Sidebar.vue'
import { useMessages } from './composables/useMessages'
import { useSettings } from './composables/useSettings'

const { messages, addMessage } = useMessages()
const { settings } = useSettings()

const handleSendMessage = (content: string) => {
  addMessage(content, settings.value.temperature)
}
</script>

<template>
  <div class="app-container">
    <Sidebar />
    <main>
      <ChatWindow :messages="messages" />
      <ChatInput @send="handleSendMessage" />
    </main>
  </div>
</template>
