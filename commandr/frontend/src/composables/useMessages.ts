import { ref } from 'vue';

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

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
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
      role: 'user',
      content,
      timestamp: new Date()
    })
    
    try {
      const responseContent = await sendMessage(content, temperature)
      messages.value.push({
        role: 'assistant',
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
