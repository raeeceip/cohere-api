// 1. App.vue - Main layout
<script setup lang="ts">
import { ref } from 'vue'
import ChatInput from './components/ChatInput.vue'
import ChatWindow from './components/ChatWindow.vue'
import SettingsButton from './components/SettingsButton.vue'
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
  <div class="app-container">
    <header class="app-header">
      <h1>CommandR</h1>
      <SettingsButton />
    </header>
    
    <main class="chat-container">
      <ChatWindow 
        :messages="messages" 
        :isLoading="isLoading" 
      />
      <ChatInput 
        @send="handleSendMessage"
        :isLoading="isLoading"
      />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: v-bind('cohereTheme.colors.background.DEFAULT');
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: v-bind('cohereTheme.spacing.md') v-bind('cohereTheme.spacing.lg');
  border-bottom: 1px solid v-bind('cohereTheme.colors.border.DEFAULT');
}

.app-header h1 {
  font-size: 1.25rem;
  font-weight: 600;
  color: v-bind('cohereTheme.colors.text.primary');
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>

