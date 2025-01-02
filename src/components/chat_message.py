# src/components/chat_message.py
import customtkinter as ctk
from theme.cohere_theme import CohereTheme

class ChatMessage(ctk.CTkFrame):
    def __init__(self, master, message: dict, **kwargs):
        super().__init__(master, **kwargs)
        
        self.message = message
        self.colors = CohereTheme.get_message_colors(
            message["role"],
            ctk.get_appearance_mode()
        )
        
        self.configure(
            fg_color=self.colors["bg"],
            corner_radius=12,
            border_width=1,
            border_color=CohereTheme.COLORS["dark"]["border"]
        )
        
        self._create_widgets()
        self._update_content(message["content"])
    
    def _create_widgets(self):
        indicator = "You" if self.message["role"] == "user" else "Assistant"
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=16, pady=(12, 4))
        
        self.role_label = ctk.CTkLabel(
            self.header_frame,
            text=indicator,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text"]
        )
        self.role_label.pack(side="left")
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        
        self.content = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=self.colors["text"],
            height=20,
            activate_scrollbars=False,
            border_width=0
        )
        self.content.pack(fill="both", expand=True)
    
    def _update_content(self, text: str):
        self.content.configure(state="normal")
        self.content.delete("1.0", "end")
        self.content.insert("1.0", text)
        self.content.configure(state="disabled")
        
        # Adjust height based on content
        self.content.update()
        num_lines = self.content._textbox.count("1.0", "end", "displaylines")[0]
        self.content.configure(height=max(80, num_lines * 20))
        
    def update_message(self, text: str):
        self._update_content(text)
        self.message["content"] = text