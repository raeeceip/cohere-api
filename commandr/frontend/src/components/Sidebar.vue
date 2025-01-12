
<script setup lang="ts">
import { useSettings } from '../composables/useSettings';

const { settings, updateSettings } = useSettings()
</script>

<template>
  <div class="sidebar">
    <div class="settings">
      <h3>Settings</h3>
      <div class="setting">
        <label>Temperature</label>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          :value="settings.temperature"
          @input="e => updateSettings({ temperature: parseFloat((e.target as HTMLInputElement).value) })"
        />
        <span>{{ settings.temperature }}</span>
      </div>
      <div class="setting">
        <label>Stream Output</label>
        <input 
          type="checkbox"
          :checked="settings.streamEnabled"
          @change="e => updateSettings({ streamEnabled: (e.target as HTMLInputElement).checked })"
        />
      </div>
    </div>
  </div>
</template>
