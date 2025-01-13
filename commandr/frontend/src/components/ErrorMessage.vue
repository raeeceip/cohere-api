
<script setup lang="ts">
import { cohereTheme } from '@/styles/theme';
import { defineEmits, defineProps } from 'vue';
const props = defineProps<{
  message: string
}>()

const emit = defineEmits<{
  (e: 'retry'): void
}>()
</script>

<template>
  <div class="error-message">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="12"></line>
      <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
    <span>{{ props.message }}</span>
    <button @click="$emit('retry')" class="retry-button">
      Try Again
    </button>
  </div>
</template>

<style scoped>
.error-message {
  display: flex;
  align-items: center;
  gap: v-bind('cohereTheme.spacing.sm');
  padding: v-bind('cohereTheme.spacing.md');
  background-color: rgba(255, 82, 82, 0.1);
  border: 1px solid v-bind('cohereTheme.colors.status.error');
  border-radius: 8px;
  color: v-bind('cohereTheme.colors.status.error');
  margin: v-bind('cohereTheme.spacing.md') 0;
}

.retry-button {
  margin-left: auto;
  background-color: v-bind('cohereTheme.colors.status.error');
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 12px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.retry-button:hover {
  opacity: 0.9;
}
</style>

