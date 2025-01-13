// 4. Update LoadingIndicator.vue
<script setup lang="ts">
import { cohereTheme } from '../styles/theme'
</script>

<template>
  <div class="loading-container">
    <div class="loading-indicator">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  </div>
</template>

<style scoped>
.loading-container {
  padding: v-bind('cohereTheme.spacing.md');
  display: flex;
  justify-content: center;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: v-bind('cohereTheme.spacing.xs');
}

.dot {
  width: 8px;
  height: 8px;
  background-color: v-bind('cohereTheme.colors.primary.DEFAULT');
  border-radius: v-bind('cohereTheme.radii.full');
  opacity: 0.7;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); } 
  40% { transform: scale(1); }
}
</style>