# src/views/main_window.py
import customtkinter as ctk
import json
import os
from dotenv import load_dotenv
import cohere
import subprocess
import pytz
from PIL import Image
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from theme.cohere_theme import CohereTheme
from components.chat_message import ChatMessage
from components.status_bar import StatusBar

class CohereAssistantGUI:
    def __init__(self):
        self.window = None
        self.setup_window()
        
    def setup_window(self):
        self.window = ctk.CTk()
        self.window.title("Cohere Assistant")
        self.window.geometry("1200x800")
        
        CohereTheme.setup_theme("dark")
        self.colors = CohereTheme.COLORS
        
        self.create_layout()
        
        load_dotenv()
        self.co = cohere.ClientV2(os.getenv('COHERE_API_KEY'))
        self.messages = []
        
        self.bind_events()
        
        self.window.mainloop()
        
    def create_layout(self):
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_chat_area()
        
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["dark"]["metallic"],
            width=300,
            corner_radius=12
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sidebar.grid_propagate(False)
        
        title = ctk.CTkLabel(
            self.sidebar,
            text="Cohere Assistant",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["dark"]["text"]
        )
        title.pack(anchor="w", padx=20, pady=20)
        
        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self.colors["dark"]["border"]
        )
        divider.pack(fill="x", padx=20, pady=10)
        
        # Settings section
        settings = ctk.CTkLabel(
            self.sidebar,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["dark"]["text"]
        )
        settings.pack(anchor="w", padx=20, pady=(20, 10))
        
        temp_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        temp_label = ctk.CTkLabel(
            temp_frame,
            text="Temperature:",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["dark"]["text"]
        )
        temp_label.pack(anchor="w")
        
        self.temperature = ctk.CTkSlider(
            temp_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            progress_color=self.colors["primary"],
            button_color=self.colors["accent"]
        )
        self.temperature.set(0.7)
        self.temperature.pack(fill="x", pady=(5, 0))
        
        self.stream_var = ctk.BooleanVar(value=True)
        self.stream_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Stream Output",
            font=ctk.CTkFont(size=14),
            variable=self.stream_var,
            progress_color=self.colors["primary"],
            button_color=self.colors["accent"]
        )
        self.stream_switch.pack(anchor="w", padx=20, pady=10)
        
    def create_chat_area(self):
        self.chat_container = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["dark"]["metallic"],
            corner_radius=12
        )
        self.chat_container.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(1, weight=1)
        
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color=self.colors["dark"]["background"],
            corner_radius=8
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.messages_frame.grid_columnconfigure(0, weight=1)
        
        input_container = ctk.CTkFrame(
            self.chat_container,
            fg_color="transparent",
            height=120
        )
        input_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_container.grid_columnconfigure(0, weight=1)
        
        self.input_text = ctk.CTkTextbox(
            input_container,
            height=100,
            fg_color=self.colors["dark"]["background"],
            text_color=self.colors["dark"]["text"],
            font=ctk.CTkFont(size=14),
            border_width=1,
            corner_radius=8,
            wrap="word"
        )
        self.input_text.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.status_bar = StatusBar(self.chat_container)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        
    def bind_events(self):
        self.window.bind('<Return>', lambda e: self.generate_response())
        self.window.bind('<Command-k>', lambda e: self.clear_output())
        
    def add_message(self, role: str, content: str):
        message = {"role": role, "content": content}
        self.messages.append(message)
        
        msg_widget = ChatMessage(
            self.messages_frame,
            message
        )
        msg_widget.pack(fill="x", padx=10, pady=5)
        return msg_widget
        
    def generate_response(self):
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            return
            
        msg_widget = self.add_message("user", prompt)
        self.input_text.delete("1.0", "end")
        
        if "calendar" in prompt.lower():
            self.handle_calendar_request(prompt)
        else:
            if self.stream_var.get():
                self.stream_response(prompt)
            else:
                self.generate_complete_response(prompt)
                
    def stream_response(self, prompt):
        try:
            messages = [{"role": m["role"], "content": m["content"]} for m in self.messages]
            response = self.co.chat_stream(
                model="command",
                messages=messages,
                temperature=self.temperature.get()
            )
            
            current_response = ""
            msg_widget = None
            
            for event in response:
                if event.type == "content-delta":
                    chunk = event.delta.message.content.text
                    current_response += chunk
                    
                    if msg_widget is None:
                        msg_widget = self.add_message("assistant", current_response)
                    else:
                        msg_widget.update_message(current_response)
                        
                    self.window.update()
                    self.messages_frame._parent_canvas.yview_moveto(1.0)
            
            self.status_bar.set_status("Response completed", "success")
            
        except Exception as e:
            self.status_bar.set_status(f"Error: {str(e)}", "error")
            
    def generate_complete_response(self, prompt):
        try:
            messages = [{"role": m["role"], "content": m["content"]} for m in self.messages]
            response = self.co.chat(
                model="command",
                messages=messages,
                temperature=self.temperature.get()
            )
            
            self.add_message("assistant", response.text)
            self.status_bar.set_status("Response completed", "success")
            self.messages_frame._parent_canvas.yview_moveto(1.0)
            
        except Exception as e:
            self.status_bar.set_status(f"Error: {str(e)}", "error")

    def handle_calendar_request(self, prompt):
        try:
            system_prompt = """Extract meeting details and format as JSON:
            {
                "title": "meeting title",
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "duration": 30
            }"""
            
            response = self.co.chat(
                model="command",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Extract meeting details from: {prompt}"}
                ],
                temperature=0.1
            )
            
            meeting_details = json.loads(response.text)
            script = f'''
            tell application "Calendar"
                tell calendar "Calendar"
                    make new event at end with properties {{
                        summary: "{meeting_details['title']}",
                        start date: date "{meeting_details['date']} {meeting_details['time']}",
                        duration: {meeting_details['duration']} * minutes
                    }}
                end tell
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script])
            
            success_message = f"""Meeting scheduled successfully!
            Title: {meeting_details['title']}
            Date: {meeting_details['date']}
            Time: {meeting_details['time']}
            Duration: {meeting_details['duration']} minutes"""
            
            self.add_message("assistant", success_message)
            self.status_bar.set_status("Meeting scheduled", "success")
            
        except Exception as e:
            error_msg = str(e)
            self.add_message("assistant", f"Error scheduling meeting: {error_msg}")
            self.status_bar.set_status("Error", "error")
            
    def clear_output(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.messages = []
        self.input_text.delete("1.0", "end")
        self.status_bar.set_status("Ready", "info")

if __name__ == "__main__":
    app = CohereAssistantGUI()