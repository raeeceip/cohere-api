<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'send', value: string): void
}>()

const message = ref('')

function handleSubmit() {
  if (message.value.trim() && !props.disabled) {
    emit('send', message.value.trim())
    message.value = ''
  }
}

function handleKeypress(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}
</script>

<template>
  <div class="p-4 bg-gray-700">
    <div class="flex space-x-4">
      <textarea
        v-model="message"
        :disabled="disabled"
        class="flex-1 p-2 bg-gray-800 text-white rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'opacity-50': disabled }"
        rows="3"
        :placeholder="disabled ? 'Please wait...' : 'Type your message...'"
        @keypress="handleKeypress"
      />
      <button
        :disabled="disabled || !message.trim()"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'opacity-50': disabled || !message.trim() }"
        @click="handleSubmit"
      >
        Send
      </button>
    </div>
  </div>
</template>
