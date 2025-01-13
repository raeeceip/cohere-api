export interface Message {
    id: string;
    content: string;
    timestamp: Date;
    sender: 'user' | 'assistant';
    status?: 'sending' | 'sent' | 'error';
    role: 'user' | 'assistant';
}


export type MessageStatus = 'sending' | 'sent' | 'error';


export type MessageSender = 'user' | 'assistant';