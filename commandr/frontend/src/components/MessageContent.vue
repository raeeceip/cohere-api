

<script setup lang="ts">
import { cohereTheme } from '@/styles/theme';
import { marked } from 'marked';
import { computed } from 'vue';

const props = defineProps<{
  content: string
}>()

const htmlContent = computed(() => {
  return marked(props.content, {
    breaks: true,
    gfm: true
  })
})
</script>

<template>
  <div class="message-content" v-html="htmlContent"></div>
</template>

<style>
.message-content {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-content p {
  margin: 0.5em 0;
}

.message-content p:first-child {
  margin-top: 0;
}

.message-content p:last-child {
  margin-bottom: 0;
}

.message-content code {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 2px 4px;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  font-size: 0.9em;
}

.message-content pre {
  background-color: rgba(0, 0, 0, 0.2);
  padding: v-bind('cohereTheme.spacing.md');
  border-radius: 8px;
  overflow-x: auto;
  margin: v-bind('cohereTheme.spacing.md') 0;
}

.message-content pre code {
  background-color: transparent;
  padding: 0;
}

.message-content a {
  color: v-bind('cohereTheme.colors.text.accent');
  text-decoration: none;
}

.message-content a:hover {
  text-decoration: underline;
}

.message-content ul, .message-content ol {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.message-content li {
  margin: 0.25em 0;
}
</style>