
<script setup lang="ts">
import { cohereTheme } from '@/styles/theme';
</script>

<template>
  <div class="loading-indicator">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>
</template>

<style scoped>
.loading-indicator {
  position: absolute;
  top: -24px;
  left: 16px;
  display: flex;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: v-bind('cohereTheme.colors.primary');
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0);
  } 
  40% { 
    transform: scale(1.0);
  }
}
</style>

