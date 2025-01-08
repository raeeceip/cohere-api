import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv
from views.main_window import CohereAssistantGUI
from theme.cohere_theme import CohereTheme
from utils.hotkey_manager import HotkeyManager
from utils.logger import setup_logger

def setup_environment():
    """Set up the application environment"""
    # Set up logging
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Setting up application environment")
      
    # Ensure resource path is correct in built application
    if getattr(sys, 'frozen', False):
        application_path = Path(sys._MEIPASS)
    else:
        application_path = Path(__file__).parent
        
    resource_path = application_path / "resources"
    os.environ["RESOURCE_PATH"] = str(resource_path)
    
    # Load environment variables from root directory
    env_path = application_path.parent / ".env"
    logger.info(f"Looking for .env file at: {env_path}")
    if env_path.exists():
        logger.info("Found .env file, loading environment variables")
        load_dotenv(env_path)
    else:
        logger.warning(".env file not found")
    
    return application_path

def main():
    # Set up environment
    app_path = setup_environment()
    logger = logging.getLogger(__name__)
    
    try:
        # Set up theme
        logger.info("Setting up theme")
        CohereTheme.setup_theme()
        
        # Set up hotkey
        logger.info("Setting up hotkey")
        HotkeyManager.setup_command_r()
        
        # Get API key
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            logger.error("No COHERE_API_KEY found in environment variables")
            raise ValueError("COHERE_API_KEY not found")
        
        # Initialize application
        logger.info("Initializing application with API key")
        app = CohereAssistantGUI(api_key=api_key)
        
        # Run the application
        logger.info("Starting application")
        app.window.mainloop()

    except Exception as e:
        logger.error(f"Error starting application: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()