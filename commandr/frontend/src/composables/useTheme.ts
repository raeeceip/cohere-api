import { ref } from 'vue'

export type Theme = 'light' | 'dark'

const currentTheme = ref<Theme>('light')

export function useTheme() {
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
    document.documentElement.setAttribute('data-theme', currentTheme.value)
  }

  return {
    currentTheme,
    toggleTheme
  }
}
