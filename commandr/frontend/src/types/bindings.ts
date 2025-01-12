export interface AppBindings {
    SendMessage(message: string, temperature: number): Promise<ChatResponse>;
  }
  
  export interface ChatResponse {
    content: string;
    error?: string;
  }