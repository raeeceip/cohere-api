import React from 'react';
import '../styles/theme.css';

interface ChatMessageProps {
    role: string;
    content: string;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ role, content }) => {
    return (
        <div className={`p-4 mb-4 rounded-lg ${role === 'user' ? 'bg-blue-600' : 'metallic-background'}`}>
            <div className="text-sm font-semibold mb-2">
                {role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div className="text-white">
                {content}
            </div>
        </div>
    );
};


export default ChatMessage;
