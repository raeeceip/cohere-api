# src/models/conversation.py

from datetime import datetime
import pytz

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.timestamp = datetime.now(pytz.UTC)

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

class Conversation:
    def __init__(self, id: str, title: str = None):
        self.id = id
        self.title = title or "New Conversation"
        self.messages = []
        self.created_at = datetime.now(pytz.UTC)

    def add_message(self, role: str, content: str):
        message = Message(role, content)
        self.messages.append(message)
        return message

    def get_messages(self):
        return [msg.to_dict() for msg in self.messages]