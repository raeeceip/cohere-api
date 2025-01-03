# src/views/main_window.py

# Core Python imports
import os
import json
import asyncio
import threading
from datetime import datetime, timedelta
from pathlib import Path
from queue import Queue
from typing import Optional, Dict, Any
import logging

# Third-party dependencies
import customtkinter as ctk
from dotenv import load_dotenv
import cohere
import pytz
from icalendar import Calendar, Event

# Local application imports
from theme.cohere_theme import CohereTheme
from components.chat_message import ChatMessage
from components.status_bar import StatusBar
from utils.validator import ResponseValidator, ValidationError

class CohereAssistantGUI:
    """Main application window and controller for the Cohere Assistant"""
    
    def __init__(self):
        self.window = None
        self.validator = ResponseValidator()
        self.event_queue = Queue()
        self.async_thread = None
        self.setup_window()
        
    # ============================================================================
    # Window Setup and Layout
    # ============================================================================
    
    def setup_window(self):
        """Initialize main window and components"""
        self.window = ctk.CTk()
        self.window.title("Command R")
        self.window.geometry("1200x800")
        
        # Set up theme and components
        CohereTheme.setup_theme("dark")
        self.colors = CohereTheme.COLORS
        self._create_layout()
        
        # Initialize Cohere client
        load_dotenv()
        self.co = cohere.ClientV2(os.getenv('COHERE_API_KEY'))
        self.messages = []
        
        # Bind events and start async handling
        self._bind_events()
        self._setup_async_handling()
        
        self.window.mainloop()
    
    def _setup_async_handling(self):
        """Set up async event handling"""
        self.async_thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.async_thread.start()
        self.window.after(100, self._process_event_queue)
    
    def _create_layout(self):
        """Create main application layout"""
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self._create_sidebar()
        self._create_chat_area()
    
    # ============================================================================
    # Sidebar Components
    # ============================================================================
    
    def _create_sidebar(self):
        """Create settings sidebar"""
        self.sidebar = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["dark"]["metallic"],
            width=300,
            corner_radius=12
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sidebar.grid_propagate(False)
        
        self._add_title()
        self._add_divider()
        self._add_settings()
    
    def _add_title(self):
        """Add application title to sidebar"""
        title = ctk.CTkLabel(
            self.sidebar,
            text="Command R",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["dark"]["text"]
        )
        title.pack(anchor="w", padx=20, pady=20)
    
    def _add_divider(self):
        """Add divider line in sidebar"""
        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self.colors["dark"]["border"]
        )
        divider.pack(fill="x", padx=20, pady=10)
    
    def _add_settings(self):
        """Add settings controls to sidebar"""
        # Settings header
        settings_label = ctk.CTkLabel(
            self.sidebar,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["dark"]["text"]
        )
        settings_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Temperature control
        self._add_temperature_control()
        
        # Stream toggle
        self._add_stream_toggle()
    
    def _add_temperature_control(self):
        """Add temperature slider control"""
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
    
    def _add_stream_toggle(self):
        """Add stream toggle switch"""
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
    
    # ============================================================================
    # Chat Area Components
    # ============================================================================
    
    def _create_chat_area(self):
        """Create main chat interface"""
        self.chat_container = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["dark"]["metallic"],
            corner_radius=12
        )
        self.chat_container.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(1, weight=1)
        
        self._create_messages_area()
        self._create_input_area()
        self._create_status_bar()
    
    def _create_messages_area(self):
        """Create scrollable messages area"""
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color=self.colors["dark"]["background"],
            corner_radius=8
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.messages_frame.grid_columnconfigure(0, weight=1)
    
    def _create_input_area(self):
        """Create chat input area"""
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
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = StatusBar(self.chat_container)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
    
    # ============================================================================
    # Event Handling
    # ============================================================================
    
    def _bind_events(self):
        """Bind keyboard events"""
        self.window.bind('<Return>', lambda e: self._handle_return(e))
        self.window.bind('<Command-k>', lambda e: self.clear_output())
    
    def _handle_return(self, event):
        """Handle return key press"""
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            return "break"  # Prevent default return behavior
        
        # Add message immediately
        self._add_message("user", prompt)
        self.input_text.delete("1.0", "end")
    
        # Schedule the async operation
        loop = asyncio.get_event_loop()
        loop.create_task(self._handle_chat_request(prompt))
    
        return "break"
    
    def _run_async_loop(self):
        """Run async event loop in separate thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_forever()
    
    def _process_event_queue(self):
        """Process events from async operations"""
        try:
            while True:
                event = self.event_queue.get_nowait()
                if event:
                    event_type = event.get("type")
                    data = event.get("data")
                    
                    if event_type == "message":
                        self._add_message(data["role"], data["content"])
                    elif event_type == "status":
                        self.status_bar.set_status(data["text"], data["level"])
                    elif event_type == "update":
                        msg_widget = data["widget"]
                        msg_widget.update_message(data["content"])
        except:
            pass
        finally:
            self.window.after(100, self._process_event_queue)
    
    # ============================================================================
    # Message Handling
    # ============================================================================
    
    def _add_message(self, role: str, content: str) -> ChatMessage:
        """Add a new message to the chat"""
        message = {"role": role, "content": content}
        self.messages.append(message)
        
        msg_widget = ChatMessage(self.messages_frame, message)
        msg_widget.pack(fill="x", padx=10, pady=5)
        return msg_widget
    
    def clear_output(self):
        """Clear all messages and reset input"""
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.messages = []
        self.input_text.delete("1.0", "end")
        self.status_bar.set_status("Ready", "info")
    
    # ============================================================================
    # Response Generation and Processing
    # ============================================================================
    
    async def generate_response(self):
        """Generate and validate response from Cohere"""
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            return
        self._add_message("user", prompt)
        self.input_text.delete("1.0", "end")

        # generate response
        messages = [{"role": m["role"], "content": m["content"]} for m in self.messages]
        response = self.co.chat(
            model="command",
            messages=messages,
            temperature=self.temperature.get()
        )

        # validate response
        validated_response = self.validator.validate_chat_response(response)
        self._add_message("assistant", validated_response)
        self.messages_frame._parent_canvas.yview_moveto(1.0)
    
        try:
            if "calendar" in prompt.lower() or "schedule" in prompt.lower():
                await self._handle_calendar_request(prompt)
            else:
                await self._handle_chat_request(prompt)
            
        except Exception as e:
            self.status_bar.set_status(f"Error: {str(e)}", "error")
    
    async def _handle_calendar_request(self, prompt: str):
        """Handle calendar-related requests"""
        try:
            # Validate and extract event details
            event = self.validator.validate_calendar_event(prompt)
            
            # Create calendar event
            try:
                cal = Calendar()
                event_obj = Event()
                
                start_dt = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
                
                event_obj.add('summary', event['title'])
                event_obj.add('dtstart', start_dt)
                event_obj.add('duration', timedelta(minutes=event['duration']))
                
                cal.add_component(event_obj)
                
                # Save to user's calendar directory
                calendar_dir = Path.home() / "Library" / "Calendars"
                calendar_dir.mkdir(parents=True, exist_ok=True)
                
                event_file = calendar_dir / f"{event['title'].replace(' ', '_')}.ics"
                with open(event_file, 'wb') as f:
                    f.write(cal.to_ical())
                
                success = True
                
            except Exception as e:
                success = False
            
            if success:
                response = f"""Meeting scheduled successfully!
                Title: {event['title']}
                Date: {event['date']}
                Time: {event['time']}
                Duration: {event['duration']} minutes"""
                
                self.event_queue.put({
                    "type": "message",
                    "data": {"role": "assistant", "content": response}
                })
                self.event_queue.put({
                    "type": "status",
                    "data": {"text": "Meeting scheduled", "level": "success"}
                })
            else:
                self.event_queue.put({
                    "type": "message",
                    "data": {"role": "assistant", "content": "Failed to create calendar event."}
                })
                self.event_queue.put({
                    "type": "status",
                    "data": {"text": "Error scheduling meeting", "level": "error"}
                })
                
        except ValidationError as e:
            self.event_queue.put({
                "type": "message",
                "data": {
                    "role": "assistant", 
                    "content": f"I couldn't understand the event details: {str(e)}"
                }
            })
            self.event_queue.put({
                "type": "status",
                "data": {"text": "Validation error", "level": "error"}
            })
    

    async def _handle_chat_request(self, prompt: str):
        """Handle general chat requests"""
        try:
            messages = [{"role": m["role"], "content": m["content"]} for m in self.messages]
            
            if self.stream_var.get():
                # Handle streaming response
                response = self.co.chat_stream(
                    model="command",
                    messages=messages,
                    temperature=self.temperature.get()
                )
                
                current_response = ""
                msg_widget = None
                
                for event in response:
                    if event.event_type == "text-generation":
                        chunk = event.text
                        current_response += chunk
                        
                        if msg_widget is None:
                            msg_widget = self._add_message("assistant", chunk)
                        else:
                            msg_widget.update_message(current_response)
                        
                        self.window.update()
                        self.messages_frame._parent_canvas.yview_moveto(1.0)
            else:
                # Handle complete response
                response = self.co.chat(
                    model="command",
                    messages=messages,
                    temperature=self.temperature.get()
                )
                
                self._add_message("assistant", response.text)
                self.messages_frame._parent_canvas.yview_moveto(1.0)
            
            self.status_bar.set_status("Response completed", "success")
            
        except Exception as e:
            self.status_bar.set_status(f"Error: {str(e)}", "error")

    async def _handle_streaming_response(self, messages: list):
        """Handle streaming response from Cohere"""
        response = self.co.chat_stream(
            model="command",
            messages=messages,
            temperature=self.temperature.get()
        )
        
        current_response = ""
        msg_widget = None
        
        for event in response:
            if event.event_type == "text-generation":
                chunk = event.text
                current_response += chunk
                
                # Validate the chunk
                validated_chunk = self.validator.validate_chat_response(chunk)
                
                if msg_widget is None:
                    self.event_queue.put({
                        "type": "message",
                        "data": {"role": "assistant", "content": validated_chunk}
                    })
                else:
                    self.event_queue.put({
                        "type": "update",
                        "data": {
                            "widget": msg_widget,
                            "content": current_response
                        }
                    })
    
    async def _handle_complete_response(self, messages: list):
        """Handle complete (non-streaming) response from Cohere"""
        response = self.co.chat(
            model="command",
            messages=messages,
            temperature=self.temperature.get()
        )
        
        # Validate complete response
        validated_response = self.validator.validate_chat_response(response.text)
        self.event_queue.put({
            "type": "message",
            "data": {"role": "assistant", "content": validated_response}
        })

    # ============================================================================
    # Error Handling
    # ============================================================================
    
    def _handle_error(self, error: Exception, context: str = None):
        """Central error handling method"""
        error_message = str(error)
        if context:
            error_message = f"{context}: {error_message}"
            
        logging.error(error_message)
        
        self.event_queue.put({
            "type": "status",
            "data": {"text": error_message, "level": "error"}
        })
    
    def _safe_call(self, func, *args, **kwargs):
        """Safely execute a function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self._handle_error(e, f"Error in {func.__name__}")
            return None

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start application
    app = CohereAssistantGUI()