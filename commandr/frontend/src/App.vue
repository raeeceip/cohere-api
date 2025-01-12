// 1. Complete App.vue layout
// frontend/src/App.vue
<script setup lang="ts">
import { ref } from 'vue'
import ChatInput from './components/ChatInput.vue'
import ChatWindow from './components/ChatWindow.vue'
import LoadingIndicator from './components/LoadingIndicator.vue'
import Sidebar from './components/Sidebar.vue'
import { useMessages } from './composables/useMessages'
import { useSettings } from './composables/useSettings'
import { cohereTheme } from './styles/theme'

const { messages, addMessage } = useMessages()
const { settings } = useSettings()
const isLoading = ref(false)

const handleSendMessage = async (content: string) => {
  isLoading.value = true
  try {
    await addMessage(content, settings.value.temperature)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="app-layout">
    <Sidebar />
    <main class="main-content">
      <div class="chat-container">
        <ChatWindow :messages="messages" />
        <div class="input-container">
          <LoadingIndicator v-if="isLoading" />
          <ChatInput 
            @send="handleSendMessage" 
            :disabled="isLoading" 
          />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: v-bind('cohereTheme.colors.background');
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: v-bind('cohereTheme.spacing.lg');
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.md');
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.input-container {
  position: relative;
  margin-top: auto;
}
</style>

