<script setup lang="ts">
defineProps<{
  role: string
  content: string
}>()
</script>

<template>
  <div
    :class="[
      'p-4 rounded-lg',
      role === 'user' ? 'bg-blue-600 ml-12' : 'bg-gray-700 mr-12'
    ]"
  >
    <div class="text-sm font-semibold mb-2 text-gray-200">
      {{ role === 'user' ? 'You' : 'Assistant' }}
    </div>
    <div class="text-white whitespace-pre-wrap">{{ content }}</div>
  </div>
</template>
