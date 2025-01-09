// src/components/ChatWindow.tsx
import { useEffect, useRef, useState } from 'react';
import { SendMessage } from '../../wailsjs/go/main/App';
import { Message, Settings } from '../types';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';

interface ChatWindowProps {
  settings: Settings;
}

export default function ChatWindow({ settings }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const respons = await SendMessage(content, settings.temperature);
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: respons.content,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'system',
        content: 'An error occurred while processing your message.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-800">
        {messages.map((message, index) => (
          <ChatMessage
            key={`${message.timestamp}-${index}`}
            role={message.role}
            content={message.content}
          />
        ))}
        {isLoading && (
          <div className="text-gray-400 text-center">
            <span className="animate-pulse">Processing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}