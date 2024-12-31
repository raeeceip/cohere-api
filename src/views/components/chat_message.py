import customtkinter as ctk

class ChatMessage(ctk.CTkFrame):
    def __init__(self, master, message: dict, **kwargs):
        super().__init__(master, **kwargs)
        
        self.role = message["role"]
        self.content = message["content"]
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Role indicator
        role_label = ctk.CTkLabel(
            self,
            text=self.role.capitalize(),
            font=("Helvetica", 12, "bold")
        )
        role_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Message content
        content_label = ctk.CTkLabel(
            self,
            text=self.content,
            wraplength=500,
            justify="left"
        )
        content_label.pack(anchor="w", padx=10, pady=(5, 10))
        
        # Timestamp if available
        if "timestamp" in self.message:
            time_label = ctk.CTkLabel(
                self,
                text=self.message["timestamp"].strftime("%H:%M"),
                font=("Helvetica", 10),
                text_color="gray"
            )
            time_label.pack(anchor="e", padx=10)