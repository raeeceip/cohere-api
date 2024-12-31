import cohere
from typing import Optional, AsyncGenerator, Dict
import logging
from models.conversation import Conversation

logger = logging.getLogger(__name__)

class ChatController:
    def __init__(self, api_key: str):
        self.co = cohere.Client(api_key)
        self.conversations: Dict[str, Conversation] = {}
        self.current_conversation: Optional[str] = None
    
    def create_conversation(self, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(str(len(self.conversations) + 1), title)
        self.conversations[conversation.id] = conversation
        self.current_conversation = conversation.id
        return conversation
    
    def get_current_conversation(self) -> Optional[Conversation]:
        if not self.current_conversation:
            return None
        return self.conversations.get(self.current_conversation)
    
    def switch_conversation(self, conversation_id: str) -> Optional[Conversation]:
        if conversation_id in self.conversations:
            self.current_conversation = conversation_id
            return self.conversations[conversation_id]
        return None

    async def generate_response(self, prompt: str, temperature: float = 0.7, stream: bool = True) -> AsyncGenerator[str, None]:
        try:
            conversation = self.get_current_conversation()
            if not conversation:
                conversation = self.create_conversation()
            
            conversation.add_message("user", prompt)
            
            message = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation.messages
            ]
            
            if stream:
                response = self.co.chat_stream(
                    model="command",
                    messages =message,
                    temperature=temperature
                )
                
                full_response = ""
                for event in response:
                    if event.event_type == "text-generation":
                        chunk = event.text
                        full_response += chunk
                        yield chunk
                
                conversation.add_message("assistant", full_response)
            else:
                response = self.co.chat(
                    model="command",
                    messages=messages,
                    temperature=temperature
                )
                
                conversation.add_message("assistant", response.text)
                yield response.text
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            yield f"Error: {str(e)}"