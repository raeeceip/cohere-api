import customtkinter as ctk
import json
import os
from dotenv import load_dotenv
import cohere
import subprocess
from datetime import datetime
import pytz

class CohereAssistantGUI:
    def __init__(self):
        self.window = None
        self.setup_hotkey()
        
    def setup_hotkey(self):
        # This will be triggered by Command+R through system preferences
        self.create_window()
        
    def create_window(self):
        # Create the main window
        self.window = ctk.CTk()
        self.window.title("Cohere Assistant")
        self.window.geometry("1000x600")
        
        # Set the theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Create the main layout
        self.create_layout()
        
        # Initialize Cohere client
        load_dotenv()
        self.co = cohere.ClientV2()
        
        # Bind events
        self.bind_events()
        
        self.window.mainloop()
        
    def create_layout(self):
        # Create main container with grid layout
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Sidebar title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Settings",
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Temperature slider
        self.temp_label = ctk.CTkLabel(self.sidebar, text="Temperature:")
        self.temp_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.temperature = ctk.CTkSlider(self.sidebar, from_=0, to=1,
                                       number_of_steps=100)
        self.temperature.set(0.7)
        self.temperature.grid(row=2, column=0, padx=20, pady=(10, 0))
        
        # Streaming toggle
        self.stream_var = ctk.BooleanVar(value=True)
        self.stream_switch = ctk.CTkSwitch(self.sidebar, text="Stream Output",
                                         variable=self.stream_var)
        self.stream_switch.grid(row=3, column=0, padx=20, pady=(10, 0))
        
        # Create main content area
        self.main_content = ctk.CTkFrame(self.window)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        
        # Input area
        self.input_frame = ctk.CTkFrame(self.main_content)
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text = ctk.CTkTextbox(self.input_frame, height=100)
        self.input_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Output area
        self.output_frame = ctk.CTkFrame(self.main_content)
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        
        self.output_text = ctk.CTkTextbox(self.output_frame)
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Status bar
        self.status_bar = ctk.CTkLabel(self.window, text="Ready")
        self.status_bar.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 10))
        
    def bind_events(self):
        self.window.bind('<Return>', lambda e: self.generate_response())
        self.window.bind('<Command-k>', lambda e: self.clear_output())
        
    def generate_response(self):
        prompt = self.input_text.get("1.0", "end-1c").strip()
        if not prompt:
            self.status_bar.configure(text="Please enter a prompt")
            return
            
        self.output_text.delete("1.0", "end")
        self.status_bar.configure(text="Generating response...")
        self.window.update()
        
        # Check if it's a calendar-related request
        if any(word in prompt.lower() for word in ['schedule', 'meeting', 'calendar', 'appointment']):
            self.handle_calendar_request(prompt)
        else:
            self.handle_general_request(prompt)
            
    def handle_calendar_request(self, prompt):
        # First, ask Cohere to extract meeting details
        system_prompt = """You are a helpful assistant that extracts meeting details from user requests.
        Extract the meeting details and format them exactly as shown in this JSON template, nothing else:
        {
            "title": "meeting title",
            "date": "YYYY-MM-DD",
            "time": "HH:MM",
            "duration": 30
        }"""
        
        user_prompt = f"Extract meeting details from this request and respond only with the JSON: {prompt}"
        
        try:
            response = self.co.chat(
                model="command-r",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            # Get the text from the response and clean it
            response_text = response.message.content[0].text
            self.output_text.insert("end", f"Processing response: {response_text}\n\n")
            
            # Clean up the response text to remove markdown
            clean_text = response_text.replace("```json\n", "").replace("\n```", "")
            
            try:
                meeting_details = json.loads(clean_text)
            except json.JSONDecodeError as e:
                self.output_text.insert("end", f"Error parsing meeting details: {str(e)}\n")
                self.output_text.insert("end", f"Clean text was: {clean_text}\n")
                self.status_bar.configure(text="Error")
                return
            
            # Create Calendar event using AppleScript
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
            self.status_bar.configure(text="Meeting scheduled")
            
        except Exception as e:
            self.output_text.insert("end", f"Error scheduling meeting: {str(e)}")
            self.status_bar.configure(text="Error")
            
    def handle_general_request(self, prompt):
        try:
            if self.stream_var.get():
                self.stream_response(prompt)
            else:
                self.generate_complete_response(prompt)
        except Exception as e:
            self.status_bar.configure(text=f"Error: {str(e)}")
            
    def stream_response(self, prompt):
        response = self.co.chat_stream(
            model="command-r",
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature.get()
        )
        
        for event in response:
            if event.type == "content-delta":
                self.output_text.insert("end", event.delta.message.content.text)
                self.output_text.see("end")
                self.window.update()
        
        self.status_bar.configure(text="Response completed")
        
    def generate_complete_response(self, prompt):
        response = self.co.chat(
            model="command-r",
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature.get()
        )
        
        self.output_text.insert("end", response.message.content)
        self.status_bar.configure(text="Response completed")
        
    def clear_output(self):
        self.output_text.delete("1.0", "end")
        self.status_bar.configure(text="Ready")

if __name__ == "__main__":
    app = CohereAssistantGUI()