import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      'wailsjs': resolve(__dirname, '../wailsjs')
    }
  },
  server: {
    host: '127.0.0.1',
    port: 34115,
    strictPort: true,
    fs: {
      allow: ['..']
    }
  }
})