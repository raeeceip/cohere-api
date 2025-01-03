import os
import sys
from pathlib import Path
from views.main_window import CohereAssistantGUI
from controllers.chat_controller import ChatController
from theme.cohere_theme import CohereTheme
from utils.hotkey_manager import HotkeyManager
from utils.logger import setup_logger
import logging 

def setup_environment():
    """Set up the application environment"""
    # Set up logging
    setup_logger()
      
    # Ensure resource path is correct in built application
    if getattr(sys, 'frozen', False):
        application_path = Path(sys._MEIPASS)
    else:
        application_path = Path(__file__).parent
        
    resource_path = application_path / "resources"
    os.environ["RESOURCE_PATH"] = str(resource_path)
    
    return application_path

def main():
    # Set up environment
    app_path = setup_environment()
    
    # Set up theme
    CohereTheme.setup_theme()
    
    # Set up hotkey
    HotkeyManager.setup_command_r()
    
    # Initialize application
    app = CohereAssistantGUI()
    key = os.getenv("COHERE_API_KEY")

    # Set up chat controller with Cohere API key
    chat_controller = ChatController(key)

    # Run the application
    app.run()


if __name__ == "__main__":
    main()