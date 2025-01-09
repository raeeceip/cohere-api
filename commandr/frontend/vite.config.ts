// vite.config.ts
import react from '@vitejs/plugin-react';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'esnext',
    outDir: 'dist',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['@headlessui/react', '@heroicons/react'],
        },
      },
    },
  },
  server: {
    watch: {
      usePolling: true,
    },
    hmr: {
      overlay: true,
    },
  },
  esbuild: {
    jsxInject: `import React from 'react'`,
    legalComments: 'none',
    treeShaking: true,
  },
});