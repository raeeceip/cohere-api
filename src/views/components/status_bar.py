import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Helvetica", 11)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.api_status = ctk.CTkLabel(
            self,
            text="●",
            font=("Helvetica", 14),
            text_color="green"
        )
        self.api_status.pack(side="right", padx=10)
    
    def set_status(self, text: str, level: str = "info"):
        self.status_label.configure(text=text)
        color = {
            "info": "gray",
            "success": "green",
            "error": "red",
            "warning": "orange"
        }.get(level, "gray")
        self.api_status.configure(text_color=color)