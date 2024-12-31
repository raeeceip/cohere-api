import customtkinter as ctk

class ConversationList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.conversations = {}
        
    def add_conversation(self, conv_id: str, title: str):
        if conv_id not in self.conversations:
            btn = ctk.CTkButton(
                self,
                text=title,
                command=lambda: self._on_select(conv_id)
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.conversations[conv_id] = btn
    
    def _on_select(self, conv_id: str):
        for btn in self.conversations.values():
            btn.configure(fg_color=("gray85", "gray25"))
        self.conversations[conv_id].configure(fg_color=("blue", "darkblue"))
        if self.on_select:
            self.on_select(conv_id)
