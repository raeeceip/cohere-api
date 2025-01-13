
<script setup lang="ts">
import { Settings } from 'lucide-vue-next';
import { ref } from 'vue';
import { cohereTheme } from '../styles/theme';
import SettingsPanel from './SettingsPanel.vue';

const showSettings = ref(false)
</script>

<template>
  <div class="settings-container">
    <button 
      class="settings-button"
      @click="showSettings = !showSettings"
      :class="{ active: showSettings }"
    >
      <Settings :size="20" />
    </button>
    
    <Transition name="slide">
      <SettingsPanel 
        v-if="showSettings"
        @close="showSettings = false"
      />
    </Transition>
  </div>
</template>

<style scoped>
.settings-container {
  position: relative;
}

.settings-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: v-bind('cohereTheme.radii.md');
  background: transparent;
  color: v-bind('cohereTheme.colors.text.secondary');
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-button:hover {
  background-color: v-bind('cohereTheme.colors.background.secondary');
  color: v-bind('cohereTheme.colors.text.primary');
}

.settings-button.active {
  background-color: v-bind('cohereTheme.colors.primary.light');
  color: v-bind('cohereTheme.colors.text.inverted');
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

