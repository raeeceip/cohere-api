import customtkinter as ctk
from typing import Callable

class EnhancedInput(ctk.CTkTextbox):
    def __init__(self, master, placeholder: str = "", height: int = 100, **kwargs):
        super().__init__(master, height=height, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "gray70"
        self.default_fg_color = self._fg_color
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<Return>", self._on_return)
        
        self._show_placeholder()
    
    def _show_placeholder(self):
        if not self.get("1.0", "end-1c"):
            self.configure(fg_color=self.placeholder_color)
            self.insert("1.0", self.placeholder)
    
    def _on_focus_in(self, event):
        if self.get("1.0", "end-1c") == self.placeholder:
            self.delete("1.0", "end")
            self.configure(fg_color=self.default_fg_color)
    
    def _on_focus_out(self, event):
        self._show_placeholder()
    
    def _on_return(self, event):
        if self.on_submit and self.get("1.0", "end-1c") != self.placeholder:
            self.on_submit()
            return "break"