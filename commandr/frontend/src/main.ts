import { createApp } from 'vue'
import App from './App.vue'
import './styles/app.css'

// Make sure Wails runtime is ready
window.addEventListener('DOMContentLoaded', () => {
  createApp(App).mount('#app')
})