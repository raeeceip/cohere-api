
<script setup lang="ts">
import { useSettings } from '../composables/useSettings';
import { cohereTheme } from '../styles/theme';

const { settings, updateSettings } = useSettings()

defineEmits<{
  (e: 'close'): void
}>()
</script>

<template>
  <div class="settings-panel">
    <div class="panel-header">
      <h3>Settings</h3>
      <button class="close-button" @click="$emit('close')">×</button>
    </div>
    
    <div class="settings-content">
      <div class="setting-item">
        <label>Temperature</label>
        <div class="slider-container">
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.1"
            :value="settings.temperature"
            @input="e => updateSettings({ 
              temperature: parseFloat((e.target as HTMLInputElement).value) 
            })"
          />
          <span class="value">{{ settings.temperature.toFixed(1) }}</span>
        </div>
      </div>
      
      <div class="setting-item">
        <label>Stream Output</label>
        <label class="toggle">
          <input 
            type="checkbox"
            :checked="settings.streamEnabled"
            @change="e => updateSettings({ 
              streamEnabled: (e.target as HTMLInputElement).checked 
            })"
          />
          <span class="toggle-slider"></span>
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 300px;
  background: v-bind('cohereTheme.colors.background.DEFAULT');
  border: 1px solid v-bind('cohereTheme.colors.border.DEFAULT');
  border-radius: v-bind('cohereTheme.radii.lg');
  box-shadow: v-bind('cohereTheme.shadows.lg');
  z-index: 50;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: v-bind('cohereTheme.spacing.md');
  border-bottom: 1px solid v-bind('cohereTheme.colors.border.DEFAULT');
}

.panel-header h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: v-bind('cohereTheme.colors.text.primary');
  margin: 0;
}

.close-button {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  font-size: 1.25rem;
  color: v-bind('cohereTheme.colors.text.secondary');
  cursor: pointer;
  border-radius: v-bind('cohereTheme.radii.sm');
}

.close-button:hover {
  background-color: v-bind('cohereTheme.colors.background.secondary');
}

.settings-content {
  padding: v-bind('cohereTheme.spacing.md');
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.lg');
}

/* Reuse your existing setting-item styles from Sidebar.vue */
</style>

