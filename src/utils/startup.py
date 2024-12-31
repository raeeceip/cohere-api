
import os
import sys
import logging
from pathlib import Path
import psutil

def initialize_application():
    """Initialize application environment and resources"""
    # Set up base paths
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent
    
    # Set up resource path
    resource_path = base_path / "resources"
    os.environ["RESOURCE_PATH"] = str(resource_path)
    
    # Set up logging
    log_path = base_path / "logs"
    log_path.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path / "commandr.log"),
            logging.StreamHandler()
        ]
    )
    
    # Load environment variables
    from dotenv import load_dotenv
    env_path = base_path / ".env"
    load_dotenv(env_path)
    
    return base_path

def check_api_key():
    """Check if Cohere API key is properly set"""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        logging.error("COHERE_API_KEY not found in environment variables")
        return False
    return True

def check_system_requirements():
    """Check system requirements for running the application"""
    requirements = {
        "python_version": "3.8",
        "memory_mb": 512,
        "disk_space_mb": 100
    }
    
    # Check Python version
    python_version = sys.version_info
    if python_version < tuple(map(int, requirements["python_version"].split("."))):
        logging.error(f"Python {requirements['python_version']} or higher is required")
        return False
    

    available_memory = psutil.virtual_memory().available / (1024 * 1024)
    if available_memory < requirements["memory_mb"]:
        logging.warning(f"Low memory available: {available_memory:.0f}MB")
    
    # Check disk space
    disk_usage = psutil.disk_usage(os.getcwd())
    available_space = disk_usage.free / (1024 * 1024)
    if available_space < requirements["disk_space_mb"]:
        logging.warning(f"Low disk space available: {available_space:.0f}MB")
    
    return True