
<script setup lang="ts">
import { cohereTheme } from '@/styles/theme';
import { useSettings } from '../composables/useSettings';

const { settings, updateSettings } = useSettings()
</script>

<template>
  <div class="sidebar">
    <div class="logo">
      <h1>Command R</h1>
    </div>
    
    <div class="settings-section">
      <h2>Settings</h2>
      
      <div class="setting-item">
        <label>Temperature</label>
        <div class="slider-container">
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.1"
            :value="settings.temperature"
            @input="e => updateSettings({ temperature: parseFloat((e.target as HTMLInputElement).value) })"
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
            @change="e => updateSettings({ streamEnabled: (e.target as HTMLInputElement).checked })"
          />
          <span class="toggle-slider"></span>
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 300px;
  background-color: v-bind('cohereTheme.colors.surface');
  padding: v-bind('cohereTheme.spacing.lg');
  border-right: 1px solid v-bind('cohereTheme.colors.border');
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.xl');
}

.logo h1 {
  color: v-bind('cohereTheme.colors.text.primary');
  font-size: 1.5rem;
  font-weight: bold;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.lg');
}

.settings-section h2 {
  color: v-bind('cohereTheme.colors.text.secondary');
  font-size: 1rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: v-bind('cohereTheme.spacing.sm');
}

.setting-item label {
  color: v-bind('cohereTheme.colors.text.primary');
  font-size: 0.9rem;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: v-bind('cohereTheme.spacing.md');
}

input[type="range"] {
  flex-grow: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: v-bind('cohereTheme.colors.border');
  border-radius: 2px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: v-bind('cohereTheme.colors.primary');
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  background: v-bind('cohereTheme.colors.primary.light');
}

.value {
  color: v-bind('cohereTheme.colors.text.secondary');
  font-size: 0.9rem;
  min-width: 2.5em;
  text-align: right;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: v-bind('cohereTheme.colors.border');
  transition: .4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: v-bind('cohereTheme.colors.primary');
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}
</style>