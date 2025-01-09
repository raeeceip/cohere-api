export interface Settings {
    temperature: number;
    streamEnabled: boolean;
  }
  
  export interface Message {
    role: string;
    content: string;
    timestamp: string;
  }
  