<script setup lang="ts">
import { ref } from 'vue'
import { SendMessage } from '../../wailsjs/go/main/App'

const message = ref('')
const result = ref('')

async function handleSubmit() {
  try {
    const response = await SendMessage(message.value, 0.7)
    result.value = response.content
  } catch (error) {
    console.error('Error:', error)
    result.value = 'Error occurred while sending message'
  }
}
</script>

<template>
  <div>
    <input v-model="message" type="text" />
    <button @click="handleSubmit">Send</button>
    <p>{{ result }}</p>
  </div>
</template>

