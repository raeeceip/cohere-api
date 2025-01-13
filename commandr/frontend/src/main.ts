import { createApp } from 'vue'
import App from './App.vue'
import './styles/app.css'

// Make sure Wails runtime is ready
window.addEventListener('DOMContentLoaded', () => {
  document.documentElement.setAttribute('data-theme', 'light')
  createApp(App).mount('#app')
})