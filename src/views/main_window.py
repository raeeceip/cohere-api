# src/views/main_window.py

import customtkinter as ctk
import json
import os
from dotenv import load_dotenv
import cohere
import subprocess
from datetime import datetime
import pytz
from PIL import Image
from pathlib import Path

class CohereAssistantGUI:
    def __init__(self):
        self.window = None
        self.setup_window()
        
    def setup_window(self):
        # Create main window
        self.window = ctk.CTk()
        self.window.title("Cohere Assistant")
        self.window.geometry("1200x800")
        
        # Set theme
        self.setup_theme()
        
        # Create layout
        self.create_layout()
        
        # Initialize Cohere client
        load_dotenv()
        self.co = cohere.ClientV2(os.getenv('COHERE_API_KEY'))
        
        # Bind events
        self.bind_events()
        
        self.window.mainloop()
        
    def setup_theme(self):
        # Cohere colors
        self.colors = {
            "primary": "#7E6BD9",      # Cohere purple
            "secondary": "#5046E4",    # Deep purple
            "accent": "#FF7A5C",       # Coral accent
            "background": "#1A1B1E",   # Dark background
            "surface": "#2A2B2E",      # Surface color
            "text": "#FFFFFF",         # Text color
            "text_secondary": "#A0A0A0"  # Secondary text
        }
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
    def create_layout(self):
        # Configure grid
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Create sidebar with Cohere styling
        self.create_sidebar()
        
        # Create main chat area
        self.create_chat_area()
        
    def create_sidebar(self):
        # Sidebar container
        self.sidebar = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["surface"],
            width=300,
            corner_radius=20
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sidebar.grid_propagate(False)
        
        # Cohere logo/title
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        logo_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            logo_frame,
            text="Cohere Assistant",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["text"]
        )
        title.pack(anchor="w")
        
        # Settings section
        settings_label = ctk.CTkLabel(
            self.sidebar,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"]
        )
        settings_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Temperature control
        temp_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        temp_label = ctk.CTkLabel(
            temp_frame,
            text="Temperature:",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        temp_label.pack(anchor="w")
        
        self.temperature = ctk.CTkSlider(
            temp_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            progress_color=self.colors["primary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["secondary"]
        )
        self.temperature.set(0.7)
        self.temperature.pack(fill="x", pady=(5, 0))
        
        # Streaming toggle
        stream_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        stream_frame.pack(fill="x", padx=20, pady=10)
        
        self.stream_var = ctk.BooleanVar(value=True)
        self.stream_switch = ctk.CTkSwitch(
            stream_frame,
            text="Stream Output",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"],
            progress_color=self.colors["primary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["secondary"],
            variable=self.stream_var
        )
        self.stream_switch.pack(anchor="w")
        
    def create_chat_area(self):
        # Main chat container
        self.chat_container = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["surface"],
            corner_radius=20
        )
        self.chat_container.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(1, weight=1)
        
        # Input area
        self.input_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color="transparent"
        )
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text = ctk.CTkTextbox(
            self.input_frame,
            height=100,
            fg_color=self.colors["background"],
            text_color=self.colors["text"],
            font=ctk.CTkFont(size=14),
            border_color=self.colors["primary"],
            border_width=2,
            corner_radius=10
        )
        self.input_text.grid(row=0, column=0, sticky="ew")
        
        # Chat history area
        self.output_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color=self.colors["background"],
            corner_radius=10
        )
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        
        self.output_text = ctk.CTkTextbox(
            self.output_frame,
            fg_color="transparent",
            text_color=self.colors["text"],
            font=ctk.CTkFont(size=14),
            corner_radius=0
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self.chat_container,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.status_bar.grid(row=2, column=0, sticky="e", padx=20, pady=10)
        
    def bind_events(self):
        self.window.bind('<Return>', lambda _: self.generate_response())
        self.window.bind('<Command-k>', lambda _: self.clear_output())

    def generate_response(self):
        """Generate response based on user input"""
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            return
        
        self.output_text.insert("end", f"\nUser: {prompt}\n")

        if "calendar" in prompt:
            self.handle_calendar_request(self, prompt)
        else:
            if self.stream_var.get():
                self.stream_response(prompt)
            else:
                self.generate_complete_response(self, prompt)

    def stream_response(self, prompt):
        """Handle streaming responses using the updated Cohere SDK"""
        try:
            # Create message format
            messages = [{"role": "user", "content": prompt}]
            
            # Use chat_stream instead of chat with stream parameter
            response = self.co.chat_stream(
                model="command",
                messages=messages,
                temperature=self.temperature.get()
            )
            
            full_response = ""
            for event in response:
                if event.type == "content-delta":
                    chunk = event.delta.message.content.text
                    full_response += chunk
                    self.output_text.insert("end", chunk)
                    self.output_text.see("end")
                    self.window.update()
            
            self.status_bar.configure(
                text="Response completed",
                text_color=self.colors["text_secondary"]
            )
            
        except Exception as e:
            error_msg = str(e)
            self.status_bar.configure(
                text="Error occurred",
                text_color=self.colors["error"]
            )
            self.output_text.insert("end", f"\nError: {error_msg}")
            print(f"Streaming error: {error_msg}")

    def generate_complete_response(self, prompt):
        """Generate a complete response without streaming"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.co.chat(
                model="command",
                messages=messages,
                temperature=self.temperature.get()
            )
            
            self.output_text.insert("end", response.text)
            self.status_bar.configure(
                text="Response completed",
                text_color=self.colors["text_secondary"]
            )
                
        except Exception as e:
            error_msg = str(e)
            self.status_bar.configure(
                text="Error occurred",
                text_color=self.colors["error"]
            )
            self.output_text.insert("end", f"\nError: {error_msg}")
            print(f"Response error: {error_msg}")

    def handle_calendar_request(self, prompt):
        """Handle calendar-related requests"""
        try:
            system_prompt = """Extract meeting details and format as JSON:
            {
                "title": "meeting title",
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "duration": 30
            }"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract meeting details from: {prompt}"}
            ]
            
            response = self.co.chat(
                model="command",
                messages=messages,
                temperature=0.1
            )
            
            meeting_details = json.loads(response.text)
            
            # Create calendar event
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
            
            self.output_text.insert("end", success_message)
            self.status_bar.configure(
                text="Meeting scheduled",
                text_color=self.colors["success"]
            )
            
        except Exception as e:
            error_msg = str(e)
            self.output_text.insert("end", f"Error scheduling meeting: {error_msg}")
            self.status_bar.configure(
                text="Error",
                text_color=self.colors["error"]
            )




    
    def clear_output(self):
        self.output_text.delete("1.0", "end")
        self.input_text.delete("1.0", "end")
        self.status_bar.configure(text="Ready")

if __name__ == "__main__":
    app = CohereAssistantGUI()