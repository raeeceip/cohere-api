# src/views/main_window.py

import customtkinter as ctk
import json
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import cohere

logger = logging.getLogger(__name__)

class CohereAssistantGUI:
    def __init__(self, api_key=None):
        logger.info("Initializing Cohere Assistant GUI")
        self.window = None
        self.messages = []
        self.api_key = api_key
        self.setup_window()
        
    def setup_window(self):
        logger.info("Setting up main window")
        self.window = ctk.CTk()
        self.window.title("Command R")
        self.window.geometry("1200x800")
        
        # Set theme
        self.setup_theme()
        
        # Create layout
        self.create_layout()
        
        # Initialize Cohere client
        self._initialize_cohere_client()
        
        # Bind events
        self.bind_events()
        
    def _initialize_cohere_client(self):
        """Initialize Cohere client with proper error handling"""
        try:
            if not self.api_key:
                logger.debug("No API key provided, attempting to load from .env")
                load_dotenv()
                self.api_key = os.getenv('COHERE_API_KEY')
            
            if not self.api_key:
                logger.error("No Cohere API key found!")
                raise ValueError("Cohere API key not found. Please set COHERE_API_KEY environment variable.")
            
            logger.info("Initializing Cohere client")
            self.co = cohere.ClientV2(self.api_key)
            logger.info("Cohere client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {str(e)}")
            self.status_bar.configure(text="Failed to initialize Cohere client", text_color=self.colors["error"])
            raise

    def setup_theme(self):
        logger.debug("Setting up theme")
        self.colors = {
            "primary": "#7E6BD9",      # Cohere purple
            "secondary": "#5046E4",    # Deep purple
            "accent": "#FF7A5C",       # Coral accent
            "background": "#1A1B1E",   # Dark background
            "surface": "#2A2B2E",      # Surface color
            "text": "#FFFFFF",         # Text color
            "text_secondary": "#A0A0A0",  # Secondary text
            "error": "#FF4444",        # Error color
            "success": "#44FF44"       # Success color
        }
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
    def create_layout(self):
        logger.debug("Creating layout")
        # Configure grid
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Create sidebar and chat area
        self.create_sidebar()
        self.create_chat_area()
        
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["surface"],
            width=300,
            corner_radius=20
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sidebar.grid_propagate(False)
        
        title = ctk.CTkLabel(
            self.sidebar,
            text="Command R",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["text"]
        )
        title.pack(anchor="w", padx=20, pady=20)
        
        settings_label = ctk.CTkLabel(
            self.sidebar,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"]
        )
        settings_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Temperature control
        temp_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
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
            button_color=self.colors["accent"]
        )
        self.temperature.set(0.7)
        self.temperature.pack(fill="x", pady=(5, 0))
        
        # Streaming toggle
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
            fg_color=self.colors["surface"],
            corner_radius=20
        )
        self.chat_container.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(0, weight=1)
        
        # Output area
        self.output_text = ctk.CTkTextbox(
            self.chat_container,
            fg_color=self.colors["background"],
            text_color=self.colors["text"],
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Input area
        self.input_text = ctk.CTkTextbox(
            self.chat_container,
            height=100,
            fg_color=self.colors["background"],
            text_color=self.colors["text"],
            font=ctk.CTkFont(size=14),
            border_width=2,
            corner_radius=10
        )
        self.input_text.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self.chat_container,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.status_bar.grid(row=2, column=0, sticky="e", padx=20, pady=(0, 10))
        
    def bind_events(self):
        logger.debug("Binding events")
        self.window.bind('<Return>', self._handle_return)
        self.window.bind('<Command-k>', lambda e: self.clear_output())

    def _handle_return(self, event):
        """Handle return key press with proper logging"""
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            logger.debug("Empty prompt, ignoring")
            return "break"
        
        logger.info(f"Processing user input: {prompt}")
        self.output_text.insert("end", f"\nUser: {prompt}\n")
        self.output_text.see("end")
        
        # Clear input
        self.input_text.delete("1.0", "end")

        # Update status
        self.status_bar.configure(text="Generating response...", text_color=self.colors["text_secondary"])
        
        try:
            if self.stream_var.get():
                logger.info("Using streaming mode for response")
                self.stream_response(prompt)
            else:
                logger.info("Using complete response mode")
                self.generate_complete_response(prompt)
        except Exception as e:
            logger.error(f"Error handling response: {str(e)}")
            self.status_bar.configure(text="Error occurred", text_color=self.colors["error"])
        
        return "break"

    def stream_response(self, prompt):
            """Handle streaming responses with comprehensive logging"""
            try:
                logger.info("Starting stream response")
                
                # Create message for the API
                current_message = {"role": "user", "content": prompt}
                logger.debug(f"Sending message: {current_message}")
                
                response = self.co.chat_stream(
                    model="command-r-plus",  # Updated model name
                    messages=[current_message],
                    temperature=self.temperature.get()
                )
                
                # Prepare the UI for response
                self.output_text.insert("end", "Assistant: ")
                full_response = ""
                
                # Process the stream response
                for event in response:
                    logger.debug(f"Received event type: {event.type}")
                    if hasattr(event, 'text'):  # Check if event has text attribute
                        chunk = event.text
                        if chunk:  # Only process non-empty chunks
                            logger.debug(f"Processing chunk: {chunk}")
                            full_response += chunk
                            self.output_text.insert("end", chunk)
                            self.output_text.see("end")
                            self.window.update()
                
                # Add final formatting
                if full_response:
                    logger.info(f"Stream completed. Full response length: {len(full_response)}")
                    self.output_text.insert("end", "\n\n")
                    self.status_bar.configure(text="Response completed", text_color=self.colors["success"])
                else:
                    logger.warning("Stream completed but no response content received")
                    self.output_text.insert("end", "No response generated\n\n")
                    self.status_bar.configure(text="No response generated", text_color=self.colors["error"])
                
            except Exception as e:
                logger.error(f"Streaming error: {str(e)}", exc_info=True)
                self.output_text.insert("end", f"\nError: {str(e)}\n")
                self.status_bar.configure(text="Error occurred", text_color=self.colors["error"])

    def generate_complete_response(self, prompt):
            """Generate complete response with logging"""
            try:
                logger.info("Generating complete response")
                
                # Create message for the API
                current_message = {"role": "user", "content": prompt}
                logger.debug(f"Sending message: {current_message}")
                
                response = self.co.chat(
                    model="command-r-plus",  # Updated model name
                    messages=[current_message],
                    temperature=self.temperature.get()
                )
                
                if response and hasattr(response, 'text'):
                    logger.info("Response received")
                    logger.debug(f"Response content: {response.text}")
                    
                    self.output_text.insert("end", f"Assistant: {response.text}\n\n")
                    self.output_text.see("end")
                    self.status_bar.configure(text="Response completed", text_color=self.colors["success"])
                else:
                    logger.warning("No response content received")
                    self.output_text.insert("end", "No response generated\n\n")
                    self.status_bar.configure(text="No response generated", text_color=self.colors["error"])
                    
            except Exception as e:
                logger.error(f"Response error: {str(e)}", exc_info=True)
                self.output_text.insert("end", f"\nError: {str(e)}\n")
                self.status_bar.configure(text="Error occurred", text_color=self.colors["error"])
    def clear_output(self):
        logger.info("Clearing chat history")
        self.output_text.delete("1.0", "end")
        self.input_text.delete("1.0", "end")
        self.status_bar.configure(text="Ready", text_color=self.colors["text_secondary"])

    def run(self):
        """Start the application"""
        logger.info("Starting application mainloop")
        self.window.mainloop()