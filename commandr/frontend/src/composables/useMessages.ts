import { ref } from 'vue';
import { Message } from '../types/message';

declare global {
  interface Window {
    go: {
      main: {
        App: {
          SendMessage(content: string, temperature: number): Promise<{ content: string }>;
        };
      };
    };
  }
}


export function useMessages() {
  const messages = ref<Message[]>([])

  const sendMessage = async (content: string, temperature: number) => {
    try {
      const response = await window.go.main.App.SendMessage(content, temperature)
      return response.content
    } catch (error) {
      console.error('Error:', error)
      throw error
    }
  }

  const addMessage = async (content: string, temperature: number) => {
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'user',
      sender: 'user',
      content,
      timestamp: new Date()
    })
    
    try {
      const responseContent = await sendMessage(content, temperature)
      messages.value.push({
        id: crypto.randomUUID(),
        role: 'assistant',
        sender: 'assistant',
        content: responseContent,
        timestamp: new Date()
      })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return {
    messages,
    sendMessage,
    addMessage
  }
}
