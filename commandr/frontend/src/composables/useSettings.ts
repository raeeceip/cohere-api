import { ref } from 'vue';

interface Settings {
  temperature: number;
  streamEnabled: boolean;
}

export function useSettings() {
  const settings = ref<Settings>({
    temperature: 0.7,
    streamEnabled: true
  })

  const updateSettings = (newSettings: Partial<Settings>) => {
    settings.value = {
      ...settings.value,
      ...newSettings
    }
  }

  return {
    settings,
    updateSettings,
    updateTemperature: (value: number) => updateSettings({ temperature: value }),
    toggleStream: () => updateSettings({ streamEnabled: !settings.value.streamEnabled })
  }
}